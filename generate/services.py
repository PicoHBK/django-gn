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
    img_resized.convert("RGB").save(output, format="JPEG", quality=70)  # Ajustar calidad según necesidad
    
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
            # Caso 1: Coincidencia exacta
            if tag.strip() == remove.strip():
                shouldRemove = True
                print(f"¡Borrado! (coincidencia exacta): '{tag}'")
                break
            
            # Caso 2: Tag dentro de paréntesis
            if tag.startswith("(") and tag.endswith(")"):
                tag_content = tag[1:-1].split(":")[0].strip()
                # Comprobar si el tag a eliminar está como palabra completa en el contenido
                if remove in tag_content.split():
                    shouldRemove = True
                    print(f"¡Borrado! (palabra en paréntesis): '{tag}'")
                    break
            
            # Caso 3: Tag como palabra completa en el string
            words_in_tag = tag.lower().replace("_", " ").split()
            if remove.lower() in words_in_tag:
                shouldRemove = True
                print(f"¡Borrado! (palabra en tag): '{tag}'")
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



def process_special_colors(prompt, colors):
    """
    Reemplaza los placeholders [c1], [c2], [c3]... con los colores proporcionados.
    Si no hay suficientes colores, elimina los placeholders sobrantes.
    
    Args:
        prompt (str): Prompt con placeholders tipo "[c1] shirt, [c2] pants"
        colors (list): Lista de colores ["black", "gold"]
    
    Returns:
        str: Prompt con colores aplicados o placeholders eliminados
    """
    if not colors:
        # Si no hay colores, eliminar todos los [cN] y sus espacios
        result = re.sub(r'\[c\d+\]\s*', '', prompt)
        # Limpiar espacios y comas duplicadas
        result = re.sub(r'\s*,\s*,\s*', ', ', result)
        result = re.sub(r'^\s*,\s*|\s*,\s*$', '', result)
        return result.strip()
    
    # Encontrar todos los placeholders [c1], [c2], etc.
    placeholders = re.findall(r'\[c(\d+)\]', prompt)
    
    result = prompt
    for placeholder in placeholders:
        index = int(placeholder) - 1  # [c1] = index 0
        
        if index < len(colors):
            # Reemplazar [cN] con el color correspondiente
            result = result.replace(f'[c{placeholder}]', colors[index])
        else:
            # Eliminar [cN] si no hay color para ese índice
            result = re.sub(rf'\[c{placeholder}\]\s*', '', result)
    
    # Limpiar espacios y comas duplicadas
    result = re.sub(r'\s*,\s*,\s*', ', ', result)
    result = re.sub(r'^\s*,\s*|\s*,\s*$', '', result)
    
    return result.strip()


def validate_and_process_specials(additional_specials, code_tier, existing_prompts, neg_prompts):
    """
    Procesa el array additionalSpecial del body, validando tier y aplicando colores.
    
    Args:
        additional_specials (list): Array de objetos con estructura {"name": "...", "active": bool, "colors": [...]}
        code_tier (str): Tier del código (ej: "tier3")
        existing_prompts (list): Lista de prompts existentes para agregar
        neg_prompts (list): Lista de prompts negativos
    
    Returns:
        tuple: (list de prompts actualizados, bool de éxito)
    """
    new_prompts = existing_prompts.copy()
    
    # Calcular cuántos specials puede usar según el tier
    tier_level = check_tier_level(code_tier)
    max_specials = (tier_level + 1) * 4
    
    # Filtrar solo los activos
    active_specials = [s for s in additional_specials if s.get("active", False)]
    
    # Limitar según el tier
    specials_to_process = active_specials[:max_specials]
    
    print(f"Processing {len(specials_to_process)} active specials (max: {max_specials})")
    
    for special_data in specials_to_process:
        special_name = special_data.get("name")
        colors = special_data.get("colors", [])
        
        print(f"Processing special: {special_name} with colors: {colors}")
        
        try:
            # Buscar el Special en la base de datos
            special = Special.objects.filter(name=special_name).first()
            
            if not special:
                print(f"Special not found: {special_name}")
                return (None, False)
            
            # Verificar tier
            if not check_tier(special.tier, code_tier):
                print(f"Tier check failed for {special_name}")
                return (None, False)
            
            # Procesar el prompt aplicando los colores
            processed_prompt = process_special_colors(special.prompt, colors)
            print(f"Processed prompt: {processed_prompt}")
            
            # Extraer negative prompts si existen
            cleaned_prompt = extract_neg_prompt(processed_prompt, neg_prompts)
            new_prompts.append(cleaned_prompt)
            
            # Obtener tags_required y tags_deleted
            tags = []
            tags_deleted = []
            
            if hasattr(special, 'tags_required') and special.tags_required.exists():
                tags = [tag.name for tag in special.tags_required.all()]
            
            if hasattr(special, 'tags_deleted') and special.tags_deleted.exists():
                tags_deleted = [tag.name for tag in special.tags_deleted.all()]
            
            # Verificar si al menos uno de los tags está presente en algún prompt
            found_tag = False
            for prompt in new_prompts:
                if any(tag in prompt for tag in tags):
                    found_tag = True
                    break
            
            # Si no se encontró ningún tag, agregar un tag aleatorio
            if not found_tag and tags:
                random_tag = random.choice(tags)
                new_prompts.append(f"({random_tag}:1.2)")
                print(f"Added random tag: {random_tag}")
            
            # Depurar los prompts eliminando tags_deleted
            formatted_prompts = transform_description_list(new_prompts)
            new_prompts = deleteTags(tags_deleted, formatted_prompts)
                
        except Exception as e:
            print(f"Error processing special {special_name}: {str(e)}")
            import traceback
            traceback.print_exc()
            return (None, False)
    
    return (new_prompts, True)

                
                

            
