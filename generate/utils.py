# utils.py

import json

def modificar_json(file_path, new_prompt, new_hr_prompt, image_type):
    # Cargar el archivo JSON
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Modificar los campos
    data['prompt'] = new_prompt
    data['hr_prompt'] = new_hr_prompt
    
    if image_type == "portrait" :
        data["width"] = 500
        data["height"] = 500
    if image_type == "full-body" :
        data["width"] = 448
        data["height"] = 888
    if image_type == "cowboy" :
        data["width"] = 500
        data["height"] = 700
    
    # Guardar el archivo JSON actualizado
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    # Retornar el diccionario modificado
    return data


