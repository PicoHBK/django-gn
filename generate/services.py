from .models import Special
import random
import re

from PIL import Image
import base64
from io import BytesIO


def check_tier(resource_tier, code_tier):
    tiers_order = ["tier1", "tier2", "tier3", "tier4", "tier5"]
    try:
        resource_tier_index = tiers_order.index(resource_tier)
        code_tier_index = tiers_order.index(code_tier)
        print(resource_tier_index, code_tier_index)
        return code_tier_index >= resource_tier_index
    except ValueError:
        return False

def check_tier_level(code_tier):
    tiers_order = ["tier1", "tier2", "tier3", "tier4", "tier5"]
    try:
        code_tier_index = tiers_order.index(code_tier)
        return code_tier_index

    except ValueError:
        return False






def validate_special(special_name, code_tier, prompts,neg_prompts):
    if special_name:
        special = Special.objects.filter(name=special_name).first()
        if special:
            if not check_tier(special.tier, code_tier):
                print("No cumplio el tier")
                return " "
            else:
                # Obtener los prompts, si existen
                claned_prompt= extract_neg_prompt(special.prompt, neg_prompts)
                prompts.append(claned_prompt)

                # Verificar si existen tags_required y tags_deleted, si no, usamos listas vacías
                tags = []
                tags_deleted = []

                if hasattr(special, 'tags_required') and special.tags_required.exists():
                    tags = [tag.name for tag in special.tags_required.all()]

                if hasattr(special, 'tags_deleted') and special.tags_deleted.exists():
                    tags_deleted = [tag.name for tag in special.tags_deleted.all()]

                # Verificar si al menos uno de los tags está presente en algún prompt
                found_tag = False
                for prompt in prompts:
                    if any(tag in prompt for tag in tags):
                        found_tag = True
                        break  # Salir del bucle si se encuentra un tag en algún prompt

                # Si no se encontró ningún tag, agregar un tag aleatorio a la lista de prompts
                if not found_tag and tags:
                    random_tag = random.choice(tags)
                    prompts.append(f"({random_tag}:1.2)")  # Agregar el tag aleatorio

                # Depurar los prompts eliminando todas las palabras o cadenas que coincidan con tags_deleted
                updated_prompts = []             
                formated_prompts = transform_description_list(prompts)
                
                updated_prompts=deleteTags(tags_deleted,formated_prompts)
                
    
                return updated_prompts
    else:
        print("No existe el special name")
        return " "
    




def optimize_image(image_base64):
    """
    Convierte una imagen en base64 a formato JPEG con optimización de calidad y reduce su resolución a la mitad.
    Devuelve una lista con la imagen optimizada en Base64.
    """
    # Decodificar la imagen Base64
    image_data = base64.b64decode(image_base64)
    
    # Mostrar el tamaño de la imagen original
    print(f"Tamaño de la imagen original: {len(image_data) / 1024:.2f} KB")
    
    # Abrir la imagen usando Pillow
    img = Image.open(BytesIO(image_data))
    
    # Reducir la resolución de la imagen a la mitad
    new_size = (img.width // 2, img.height // 2)
    img_resized = img.resize(new_size, Image.ANTIALIAS)
    
    # Convertir la imagen a formato JPEG con calidad optimizada
    output = BytesIO()
    img_resized.convert("RGB").save(output, format="JPEG", quality=80)  # Ajustar calidad según necesidad
    
    # Codificar la imagen optimizada en Base64
    output.seek(0)
    optimized_image_base64 = base64.b64encode(output.read()).decode('utf-8')
    
    # Mostrar el tamaño de la imagen optimizada
    optimized_image_data = base64.b64decode(optimized_image_base64)
    print(f"Tamaño de la imagen optimizada: {len(optimized_image_data) / 1024:.2f} KB")
    
    # Crear una lista que contiene la imagen optimizada en Base64
    return [optimized_image_base64]


def extract_neg_prompt(main_string, neg_prompts):
    # Encuentra todo el contenido dentro de <neg:...> y lo agrega a la lista
    matches = re.findall(r'<neg:(.*?)>', main_string)
    
    # Agrega cada coincidencia a la lista de neg_prompts
    for match in matches:
        neg_prompts.append(match)
    
    # Elimina las coincidencias de la cadena principal
    main_string = re.sub(r'<neg:.*?>', '', main_string).strip()
    
    return main_string



def deleteTags(tagsToRemove, tags):
    if not tagsToRemove:
        return tags

    result = []
    tagsToRemoveSet = set(tagsToRemove)

    for tag in tags:
        shouldRemove = False
        for remove in tagsToRemoveSet:
            # Caso 1: Coincidencia exacta (ej: "leggins" == "leggins")
            if tag.strip() == remove.strip():
                shouldRemove = True
                print(f"¡Borrado! (coincidencia exacta): '{tag}'")
                break
            
            # Caso 2: Tag dentro de paréntesis, con o sin peso (ej: "(leggins:1.6)" o "(leggins)")
            if tag.startswith("(") and tag.endswith(")"):
                tag_content = tag[1:-1].split(":")[0].strip()  # Extrae "leggins" de "(leggins:1.6)"
                if tag_content == remove:
                    shouldRemove = True
                    print(f"¡Borrado! (coincidencia en paréntesis): '{tag}'")
                    break
            
            # Caso 3: Tag como subcadena (ej: "black leggins" contiene "leggins")
            if remove in tag.split():  # Busca palabras individuales, no subcadenas parciales
                shouldRemove = True
                print(f"¡Borrado! (subcadena): '{tag}'")
                break

        if not shouldRemove:
            result.append(tag)

    return result

def condicion_exacta(cadena, tag):
    # Verificar si la cadena coincide exactamente con el tag
    return tag == cadena

def condicion_parentesis(cadena, tag):
    # Verificar si el tag está rodeado por paréntesis y no tiene espacios adicionales antes o después
    return cadena == f"({tag})" or (cadena.startswith('(') and cadena.endswith(')') and cadena[1:-1] == tag)

def condicion_subcadena(cadena, tag):
    # Verificar si la subcadena existe en la cadena y está rodeada por espacios o es el inicio/final de la cadena
    if tag in cadena:
        start_index = cadena.find(tag)
        end_index = start_index + len(tag)

        # Si está al principio o al final de la cadena
        if start_index == 0 or end_index == len(cadena):
            return True

        # Verificar que haya un espacio antes y después del tag
        if (cadena[start_index - 1] == ' ' or cadena[start_index - 1] == '(') and \
           (cadena[end_index] == ' ' or cadena[end_index] == ')'):
            return True
        
    return False
def condicion_dos_puntos(cadena, tag):
    # Verificar si el tag está precedido por un espacio y seguido de ":"
    return f" {tag}:" in cadena




def transform_description_list(input_list):
    # Crear una lista para almacenar los nuevos elementos
    formatted_list = []
    
    # Iterar sobre cada elemento en la lista original
    for item in input_list:
        # Dividir el elemento por comas si las tiene y quitar espacios innecesarios
        split_items = [sub_item.strip() for sub_item in item.split(',')]
        # Agregar los elementos divididos a la lista final
        formatted_list.extend(split_items)
    
    # Retornar la lista formateada
    return formatted_list

def format_commas(text):
    # Eliminar espacios y saltos de línea antes y después de las comas
    formatted_text = re.sub(r'\s*,\s*', ',', text)
    # Eliminar saltos de línea adicionales
    formatted_text = re.sub(r'\n', '', formatted_text)
    return formatted_text

                
                

            
