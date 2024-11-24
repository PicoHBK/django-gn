import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Pose, Skin, Emote, ImageType, Character, URLSD, Franchise, Special
from .utils import modificar_json
from user_auth.models import Code
from django.db import transaction
from django.core.cache import cache


from .serializers import (
    CharacterSerializers,
    SkinSerializers,
    PoseSerializers,
    EmoteSerializers,
    ImageTypeSerializers,
    FranchiseSerializers,
    SpecialSerializer,
)

from .services import check_tier, validate_special,optimize_image,check_tier_level


class ConcatenatePromptsView(APIView):
    def post(self, request):
        # Verificamos si la vista está bloqueada usando el cache de Django
        if cache.get("view_locked"):
            return Response(
                {"error": "The view is currently locked. Please try again later."},
                status=status.HTTP_423_LOCKED,
            )

        # Bloqueamos la vista para que solo un cliente pueda acceder a la vez
        cache.set("view_locked", True, timeout=60)  # El bloqueo durará 60 segundos
        print(cache.get("view_locked"))

        try:
            # Recibimos el payload de la solicitud
            data = request.data
            request_code = data.get("code")

            # Intentamos obtener el código desde la base de datos
            with (
                transaction.atomic()
            ):  # Aseguramos que todo se haga en una única transacción
                # Bloqueamos el código para que solo una solicitud pueda modificarlo a la vez
                code = Code.objects.select_for_update().get(code=request_code)

                if not code.is_valid():
                    return Response(
                        {"error": "The code has no uses left."},
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )

                # Verificamos si el código tiene un atributo 'tier'
                code_tier = code.tier
                if not code_tier:
                    return Response(
                        {"error": "The code does not have a valid tier."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                # Inicializamos una lista para almacenar los prompts encontrados
                prompts = []

                # Buscamos en el modelo 'Pose' usando el valor de 'pose' del payload
                pose_name = data.get("pose")

                if pose_name:
                    pose = Pose.objects.filter(name=pose_name).first()
                    if pose:
                        if not check_tier(pose.tier, code_tier):
                            return Response(
                                {
                                    "error": "The code does not have the required tier to access this pose."
                                },
                                status=status.HTTP_403_FORBIDDEN,
                            )
                        prompts.append(pose.prompt)

                # Buscamos el 'Character' usando el valor de 'character' del payload
                character_name = data.get("character")
                if character_name:
                    try:
                        # Usamos .get() para obtener un solo 'Character', ya que solo esperamos uno
                        character = Character.objects.get(name=character_name)

                        if not check_tier(character.tier, code_tier):
                            return Response(
                                {
                                    "error": "The code does not have the required tier to access this character"
                                },
                                status=status.HTTP_403_FORBIDDEN,
                            )

                        # Buscamos la 'Skin' usando el valor de 'skin' del payload, pero solo si pertenece al 'Character' encontrado
                        skin_name = data.get("skin")
                        if skin_name:
                            skin = Skin.objects.filter(
                                character=character, name=skin_name
                            ).first()
                            if skin:
                                if not check_tier(skin.tier, code_tier):
                                    return Response(
                                        {
                                            "error": "The code does not have the required tier to access this skin"
                                        },
                                        status=status.HTTP_403_FORBIDDEN,
                                    )
                                prompts.append(skin.prompt)
                            else:
                                return Response(
                                    {
                                        "error": "Skin not found for the given character."
                                    },
                                    status=status.HTTP_404_NOT_FOUND,
                                )
                        else:
                            return Response(
                                {"error": "Skin name is required."},
                                status=status.HTTP_400_BAD_REQUEST,
                            )

                    except Character.DoesNotExist:
                        return Response(
                            {"error": "Character not found."},
                            status=status.HTTP_404_NOT_FOUND,
                        )

                # Buscamos en el modelo 'Emote' usando el valor de 'emotion' del payload
                emotion = data.get("emotion")
                if emotion:
                    emote = Emote.objects.filter(name=emotion).first()
                    if emote:
                        prompts.append(emote.prompt)

                # Buscamos en el modelo 'ImageType' usando el valor de 'image' del payload
                image_type = data.get("image")
                if image_type:
                    image_type_instance = ImageType.objects.filter(
                        name=image_type
                    ).first()
                    if image_type_instance:
                        prompts.append(image_type_instance.prompt)

                specials_name = data.get("special")
                if specials_name:
                    check_tier_lvl = check_tier_level(code_tier) + 1
                    
                    print(f"lvl code {check_tier_lvl}")
                    
                    # Limitar la cantidad de elementos que se recorrerán
                    max_elements = min(len(specials_name), check_tier_lvl)
                    for special_name in specials_name[:max_elements]:  # Restringir la iteración
                        check_special = validate_special(special_name, code_tier, prompts)
                        if check_special:
                            print(str(check_special))
                        else:
                            return Response(
                                {
                                    "error": "The code does not have the required tier to access this Special."
                                },
                                status=status.HTTP_403_FORBIDDEN,
                            )

                        
                    
                    
                """ check_special = validate_special(special_name, code_tier, prompts)
                if check_special:
                    print(str(check_special))
                else:
                    return Response(
                        {
                            "error": "The code does not have the required tier to access this Special."
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    ) """

                # Concatenamos todos los prompts separados por comas
                concatenated_prompts = ", ".join(prompts)

                # Solo si hay recursos válidos, realizamos la solicitud a la URL externa
                if prompts:
                    # Ruta del archivo JSON
                    file_path = "generate/plantilla.json"

                    # Modificamos el JSON con el concatenated_prompts
                    modified_data = modificar_json(
                        file_path,
                        concatenated_prompts,
                        concatenated_prompts,
                        image_type,
                    )

                    # Realizamos una solicitud a otra URL con el JSON modificado como payload
                    url = f"{URLSD.objects.latest('id').url}/sdapi/v1/txt2img"
                    response = requests.post(url, json=modified_data)

                    # Verificamos si la solicitud fue exitosa
                    if response.status_code == 200:
                        # Si la respuesta es exitosa, calculamos los usos restantes y devolvemos la respuesta
                        uses_left = code.max_uses - code.uses

                        # Intentamos usar el código (solo puede ser usado una vez)
                        if not code.use_code():
                            return Response(
                                {"error": "Failed to use the code. Please try again."},
                                status=status.HTTP_400_BAD_REQUEST,
                            )

                        img_optimized = optimize_image(response.json().get("images")[0])

                        return Response(
                            {
                                "images": img_optimized,
                                "tier": code.tier,  # El tier del código
                                "uses_left": uses_left,  # Los usos restantes del código
                                "code": code.code,
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        return Response(
                            {"error": "The AI is unavailable. Please try again later."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    # Si no hay recursos válidos, no usamos el código y devolvemos un error
                    return Response(
                        {
                            "error": "No valid resources found or you do not have the required tier."
                        },
                        status=status.HTTP_403_FORBIDDEN,
                    )

        except Code.DoesNotExist:
            # Si el código no existe, manejamos la excepción y devolvemos un error
            return Response(
                {"error": "Invalid code."}, status=status.HTTP_401_UNAUTHORIZED
            )

        finally:
            # Liberamos el bloqueo de la vista después de la ejecución
            cache.delete("view_locked")


#####


#############################################
############################################


class CharacterListView(APIView):
    def get(self, request):
        # Obtener personajes aleatorios sin filtrar
        characters = Character.objects.all().order_by("?")[:10]

        # Ordenar los resultados por `tier` (de menor a mayor)
        characters = sorted(characters, key=lambda x: x.tier)

        # Serializar los datos
        serializer = CharacterSerializers(characters, many=True)
        return Response(serializer.data)


class CharactersByFranchise(APIView):
    def get(self, request, id):
        try:
            franchise = Franchise.objects.get(id=id)
        except Franchise.DoesNotExist:
            return Response(
                {"error": f"Franchise '{id}' not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        characters = Character.objects.filter(franchise=franchise)
        serializer = CharacterSerializers(characters, many=True)
        return Response(serializer.data)


#################################################################
class SkinListByCharacterView(APIView):
    def get(self, request, name):
        character = Character.objects.get(name=name)
        skins = Skin.objects.filter(character=character)
        serializer = SkinSerializers(skins, many=True)
        return Response(serializer.data)


class PoseListView(APIView):
    def get(self, request):
        poses = Pose.objects.all()
        serializer = PoseSerializers(poses, many=True)
        return Response(serializer.data)


class EmoteListView(APIView):
    def get(self, request):
        emotes = Emote.objects.all()
        serializer = EmoteSerializers(emotes, many=True)
        return Response(serializer.data)


class ImageTypeListView(APIView):
    def get(self, request):
        image_types = ImageType.objects.all()
        serializer = ImageTypeSerializers(image_types, many=True)
        return Response(serializer.data)


class FranchiseListView(APIView):
    def get(self, request):
        franchises = Franchise.objects.all()
        serializer = FranchiseSerializers(franchises, many=True)
        return Response(serializer.data)


class SpecialListView(APIView):
    """
    Lista todos los objetos de Special.
    """

    def get(self, request):
        specials = Special.objects.all()  # Obtiene todos los objetos Special
        serializer = SpecialSerializer(specials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
