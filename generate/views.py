import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import gc

from .models import (
    Pose,
    Skin,
    Emote,
    ImageType,
    Character,
    URLSD,
    Franchise,
    Special,
    Tag,
)
from .utils import modificar_json
from user_auth.models import Code
from django.db import transaction
from django.core.cache import cache

from rest_framework.permissions import IsAdminUser


from .serializers import (
    CharacterSerializers,
    SkinSerializers,
    PoseSerializers,
    EmoteSerializers,
    ImageTypeSerializers,
    FranchiseSerializers,
    SpecialSerializer,
    SkinSerializersAdmin,
    TagSerializers,
    SpecialSerializerAdmin,
    URLSDSerializers,
    PoseAdminSerializers,
    EmoteAdminSerializers,
)

from .services import check_tier, validate_special, optimize_image, check_tier_level, extract_neg_prompt, format_commas


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
                neg_prompts = []

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

                        if pose.prompt:  # Aseguramos que pose.prompt no sea None o vacío
                            cleaned_prompt = extract_neg_prompt(pose.prompt, neg_prompts)
                            prompts.append(cleaned_prompt)


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
                                cleaned_prompt = extract_neg_prompt(skin.prompt,neg_prompts)
                                prompts.append(cleaned_prompt)
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
                image_type_instance  = None
                if image_type:
                    image_type_instance = ImageType.objects.filter(
                        name=image_type
                    ).first()
                    if image_type_instance:
                        prompts.append(image_type_instance.prompt)

                specials_name = data.get("special")
                new_prompts = prompts
                if specials_name:
                    check_tier_lvl = check_tier_level(code_tier) + 1

                    print(f"lvl code {check_tier_lvl}")

                    # Limitar la cantidad de elementos que se recorrerán
                    max_elements = min(len(specials_name), check_tier_lvl * 2)
                    
                    for special_name in specials_name[
                        :max_elements
                    ]:  # Restringir la iteración
                        check_special = validate_special(
                            special_name, code_tier, new_prompts, neg_prompts
                        )
                        if check_special:
                            new_prompts = check_special
                        else:
                            return Response(
                                {
                                    "error": "The code does not have the required tier to access this Special."
                                },
                                status=status.HTTP_403_FORBIDDEN,
                            )

                # Concatenamos todos los prompts separados por comas
                concatenated_prompts = ", ".join(new_prompts)
                concatenated_neg_prompts = ", ".join(neg_prompts)


                # Solo si hay recursos válidos, realizamos la solicitud a la URL externa
                if prompts:
                    # Ruta del archivo JSON
                    file_path = "generate/plantilla.json"

                    # Modificamos el JSON con el concatenated_prompts
                    modified_data = modificar_json(
                        file_path,
                        concatenated_prompts,
                        concatenated_prompts,
                        concatenated_neg_prompts,
                        image_type_instance,
                    )
                    
                    print("Mandando..........")
                    
                    
                    modified_data["prompt"] = format_commas(modified_data["prompt"])
                    print(modified_data["prompt"])

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


                        return Response(
                            {
                                "images": response.json().get("images"),
                                "tier": code.tier,  # El tier del código
                                "uses_left": uses_left,  # Los usos restantes del código
                                "code": code.code,
                            },
                            status=status.HTTP_200_OK,
                        )
                    else:
                        # Imprimir el error en la consola
                        print(
                            f"Error: Received status code {response.status_code} with response: {response.text}"
                        )

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
            del data, prompts, neg_prompts, new_prompts, modified_data, response
            gc.collect()
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


class CharacterEditById(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        try:
            character = Character.objects.get(id=id)
            serializer = CharacterSerializers(
                character, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Character.DoesNotExist:
            return Response(
                {"error": f"Character '{id}' not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class CharacterDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        try:
            # Intenta obtener el personaje con el ID proporcionado
            character = Character.objects.get(id=id)
            character.delete()  # Elimina el personaje
            return Response(
                {"message": f"Character with id '{id}' has been deleted."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Character.DoesNotExist:
            # Si no se encuentra el personaje con el ID proporcionado
            return Response(
                {"error": f"Character '{id}' not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class CharacterCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = CharacterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#################################################################
class SkinListByCharacterView(APIView):
    def get(self, request, name):
        character = Character.objects.get(name=name)
        skins = Skin.objects.filter(character=character)
        serializer = SkinSerializers(skins, many=True)
        return Response(serializer.data)


class SkinListByCharacterAdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, name):
        character = Character.objects.get(name=name)
        skins = Skin.objects.filter(character=character)
        serializer = SkinSerializersAdmin(skins, many=True)
        return Response(serializer.data)


class SkinEditByEditView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        print(request.data)
        try:
            skin = Skin.objects.get(id=id)
            serializer = SkinSerializersAdmin(skin, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Skin.DoesNotExist:
            return Response(
                {"error": f"Skin '{id}' not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class SkinDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        try:
            skin = Skin.objects.get(id=id)
            skin.delete()
            return Response(
                {"message": f"Skin with id '{id}' has been deleted."},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Skin.DoesNotExist:
            return Response(
                {"error": f"Skin '{id}' not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class SkinCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = SkinSerializersAdmin(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


########################################


class PoseListPreviewView(APIView):
    def get(self, request):
        poses = Pose.objects.all()[:4]
        serializer = PoseSerializers(poses, many=True)
        return Response(serializer.data)


class PoseListAllView(APIView):
    def get(self, request):
        poses = Pose.objects.all()
        serializer = PoseSerializers(poses, many=True)
        return Response(serializer.data)


class PoseListAdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        poses = Pose.objects.all()
        serializer = PoseAdminSerializers(poses, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class PoseEditByIdView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        try:
            pose = Pose.objects.get(id=id)
        except Pose.DoesNotExist:
            return Response(
                {"error": "Pose not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = PoseAdminSerializers(pose, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PoseDeleteByIdView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        try:
            pose = Pose.objects.get(id=id)
        except Pose.DoesNotExist:
            return Response(
                {"error": "Pose not found."}, status=status.HTTP_404_NOT_FOUND
            )

        pose.delete()
        return Response(
            {"message": "Pose deleted successfully."}, status=status.HTTP_204_NO_CONTENT
        )


class PoseCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = PoseAdminSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


############################################


class EmoteListView(APIView):
    def get(self, request):
        emotes = Emote.objects.all()
        serializer = EmoteSerializers(emotes, many=True)
        return Response(serializer.data)


class EmoteListAdminView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        emotes = Emote.objects.all()
        serializer = EmoteAdminSerializers(emotes, many=True)
        return Response(serializer.data)


class EmoteEditByIdView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        try:
            emote = Emote.objects.get(id=id)
        except Emote.DoesNotExist:
            return Response(
                {"error": "Emote not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = EmoteAdminSerializers(emote, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmoteDeleteByIdView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        try:
            emote = Emote.objects.get(id=id)
        except Emote.DoesNotExist:
            return Response(
                {"error": "Emote not found."}, status=status.HTTP_404_NOT_FOUND
            )

        emote.delete()
        return Response(
            {"message": "Emote deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


class EmoteCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = EmoteAdminSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


############################################


class ImageTypeListView(APIView):
    def get(self, request):
        image_types = ImageType.objects.all()
        serializer = ImageTypeSerializers(image_types, many=True)
        return Response(serializer.data)


#################################################################


class FranchiseCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = FranchiseSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FranchiseDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        try:
            franchise = Franchise.objects.get(id=id)  # Buscar la franquicia por su id
            franchise.delete()  # Eliminar la franquicia
            return Response(
                {"detail": "Franchise deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Franchise.DoesNotExist:
            return Response(
                {"detail": "Franchise not found"}, status=status.HTTP_404_NOT_FOUND
            )


class FranchiseListView(APIView):
    def get(self, request):
        franchises = Franchise.objects.all()
        serializer = FranchiseSerializers(franchises, many=True)
        return Response(serializer.data)


class FranchiseEditById(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        try:
            # Obtener la franquicia de la base de datos
            franchise = Franchise.objects.get(id=id)

            # Mostrar los datos recibidos
            print("Received data:", request.data)

            # Serializar los datos y validarlos (con partial=True para permitir actualizaciones parciales)
            serializer = FranchiseSerializers(
                franchise, data=request.data, partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # Mostrar errores si la validación falla
                print("Validation errors:", serializer.errors)
                return Response(
                    {"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST
                )

        except Franchise.DoesNotExist:
            return Response(
                {"error": f"Franchise '{id}' not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


#################################################################


class SpecialListView(APIView):
    """
    Lista todos los objetos de Special.
    """

    def get(self, request):
        specials = Special.objects.all()  # Obtiene todos los objetos Special
        serializer = SpecialSerializer(specials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpecialListAdminView(APIView):
    """
    Lista todos los objetos de Special para el admin
    """

    permission_classes = [IsAdminUser]

    def get(self, request):
        specials = Special.objects.all()  # Obtiene todos los objetos Special
        serializer = SpecialSerializerAdmin(specials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SpecialCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = SpecialSerializerAdmin(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecialEditByIdView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        try:
            # Intenta obtener el objeto "Special" por su id
            special = Special.objects.get(id=id)

            # Serializa los datos del objeto y valida los datos recibidos
            serializer = SpecialSerializerAdmin(
                special, data=request.data, partial=True
            )

            if serializer.is_valid():  # Si los datos son válidos
                serializer.save()  # Guarda los cambios en la base de datos
                return Response(
                    serializer.data, status=status.HTTP_200_OK
                )  # Devuelve los datos actualizados

            else:  # Si los datos no son válidos
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )  # Devuelve los errores

        except (
            Special.DoesNotExist
        ):  # Excepción específica si el objeto no se encuentra
            return Response(
                {"error": "Special not found."}, status=status.HTTP_404_NOT_FOUND
            )  # Mensaje de error si no se encuentra el objeto
        except Exception as e:  # Captura cualquier otra excepción inesperada
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )  # Mensaje de error para excepciones no controladas # Devuelve un mensaje de error si el objeto no se encuentra


class SpecialDeleteByIdView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        try:
            special = Special.objects.get(
                id=id
            )  # Obtiene el objeto "Special" por su id
            special.delete()  # Elimina el objeto "Special" de la base de datos
            return Response(
                {"detail": "Special deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )  # Devuelve un mensaje de confirmación si la eliminación es exitosa

        except (
            Special.DoesNotExist
        ):  # Excepción específica si el objeto no se encuentra
            return Response(
                {"error": "Special not found."}, status=status.HTTP_404_NOT_FOUND
            )  # Mensaje de error si no se encuentra el objeto
        except Exception as e:  # Captura cualquier otra excepción inesperada
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )  # Mensaje de error para excepciones no controladas # Devuelve un mensaje de error si el objeto no se encuentra


##########################################################


class TagListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        tags = Tag.objects.all()
        serializer = TagSerializers(tags, many=True)
        return Response(serializer.data)


class TagEditViewById(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, id):
        try:
            tag = Tag.objects.get(id=id)
            serializer = TagSerializers(tag, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except Tag.DoesNotExist:
            return Response(
                {"detail": "Tag not found"}, status=status.HTTP_404_NOT_FOUND
            )


class TagDeleteById(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        try:
            tag = Tag.objects.get(id=id)
            tag.delete()
            return Response(
                {"detail": "Tag deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Tag.DoesNotExist:
            return Response(
                {"detail": "Tag not found"}, status=status.HTTP_404_NOT_FOUND
            )


class TagCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = TagSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#######################################################
class URLSDEditView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request):
        try:
            # Obtener el único objeto URLSD
            urlsd = URLSD.objects.last()  # Asume que solo hay uno, toma el último
            if not urlsd:
                return Response(
                    {"detail": "No URLSD instance found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Validar que solo se reciba el atributo 'url'
            if "url" not in request.data:
                return Response(
                    {"detail": "Invalid payload, 'url' is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            serializer = URLSDSerializers(urlsd, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
