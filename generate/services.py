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
                for prompt in prompts:
                    for tag in tags_deleted:
                        # Eliminar las palabras o frases completas que coincidan con tags_deleted
                        prompt = re.sub(r'\b' + re.escape(tag) + r'\b', '', prompt)

                    # Filtrar espacios extra que puedan quedar
                    updated_prompts.append(' '.join(prompt.split()))

                return updated_prompts
    else:
        print("No existe el special name")
        return " "
    




def optimize_image(image_base64):
    """
    Convierte una imagen en base64 a formato JPEG con optimización de calidad y devuelve una lista.
    Muestra el tamaño de la imagen antes y después de la optimización.
    """
    # Decodificar la imagen Base64
    image_data = base64.b64decode(image_base64)
    
    # Mostrar el tamaño de la imagen original
    print(f"Tamaño de la imagen original: {len(image_data) / 1024:.2f} KB")
    
    # Abrir la imagen usando Pillow
    img = Image.open(BytesIO(image_data))
    
    # Convertir la imagen a formato JPEG (ajustar calidad según lo necesites)
    output = BytesIO()
    img.convert("RGB").save(output, format="JPEG", quality=80)  # Calidad 85 para optimizar el tamaño
    
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





                
                

            
