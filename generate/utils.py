import json
import re
def modificar_json(file_path, new_prompt, new_hr_prompt, neg_prompt, image_type, img_base_64):
    # Cargar el archivo JSON
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Crear una copia del diccionario original para no modificar la plantilla
    modified_data = data.copy()
    
    # Modificar los campos en la copia
    modified_data['prompt'] = new_prompt
    modified_data['hr_prompt'] = new_hr_prompt
    modified_data["negative_prompt"] = f"{modified_data['negative_prompt']},{neg_prompt}"
    
    if image_type:
        modified_data["width"] = image_type.width
        modified_data["height"] = image_type.height

    # Comprobar si img_base_64 es None
    if img_base_64 is None:
        # Si es None, borrar el atributo "ControlNet"
        if "alwayson_scripts" in modified_data and "ControlNet" in modified_data["alwayson_scripts"]:
            del modified_data["alwayson_scripts"]["ControlNet"]
    else:
        # Si img_base_64 existe, reemplazar el valor en el primer elemento de "args" dentro de "ControlNet"
        if "alwayson_scripts" in modified_data and "ControlNet" in modified_data["alwayson_scripts"]:
            control_net = modified_data["alwayson_scripts"]["ControlNet"]
            if "args" in control_net:
                args = control_net["args"]
                if args:
                    # Buscar el primer elemento donde "enabled" sea True
                    for arg in args:
                        if isinstance(arg, dict) and arg.get("enabled") is True:
                            # Asegurarnos de que "image" existe en el diccionario
                            if "image" in arg and arg["image"] is not None:
                                # Modificar solo el campo "image", manteniendo los demás atributos intactos
                                arg["image"]["image"] = img_base_64
                            break  # Solo modificamos el primer elemento encontrado
    
    # Retornar el diccionario modificado
    return modified_data


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


def check_tier_level(tier):
    """
    Convierte tier string a número.
    
    Args:
        tier (str): "tier1", "tier2", etc.
    
    Returns:
        int: Nivel numérico (0-4)
    """
    tier_map = {
        "tier1": 0,
        "tier2": 1,
        "tier3": 2,
        "tier4": 3,
        "tier5": 4,
    }
    return tier_map.get(tier, 0)


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
    from .models import Special
    from .utils import check_tier, extract_neg_prompt
    
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
            special = Special.objects.get(name=special_name)
            
            # Verificar tier
            if not check_tier(special.tier, code_tier):
                print(f"Tier check failed for {special_name}")
                return (None, False)
            
            # Procesar el prompt aplicando los colores
            processed_prompt = process_special_colors(special.prompt, colors)
            print(f"Processed prompt: {processed_prompt}")
            
            # Extraer negative prompts si existen
            cleaned_prompt = extract_neg_prompt(processed_prompt, neg_prompts)
            
            # Procesar tags_required (agregar prompts)
            for tag in special.tags_required.all():
                if tag.prompt:
                    tag_cleaned = extract_neg_prompt(tag.prompt, neg_prompts)
                    if tag_cleaned and tag_cleaned not in new_prompts:
                        new_prompts.append(tag_cleaned)
            
            # Procesar tags_deleted (eliminar prompts)
            for tag in special.tags_deleted.all():
                if tag.prompt:
                    # Intentar eliminar el prompt exacto o versiones limpias
                    prompts_to_remove = [tag.prompt, extract_neg_prompt(tag.prompt, [])]
                    for prompt_to_remove in prompts_to_remove:
                        if prompt_to_remove in new_prompts:
                            new_prompts.remove(prompt_to_remove)
            
            # Agregar el prompt procesado
            if cleaned_prompt and cleaned_prompt not in new_prompts:
                new_prompts.append(cleaned_prompt)
                
        except Special.DoesNotExist:
            print(f"Special not found: {special_name}")
            return (None, False)
        except Exception as e:
            print(f"Error processing special {special_name}: {str(e)}")
            return (None, False)
    
    return (new_prompts, True)