import json

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
