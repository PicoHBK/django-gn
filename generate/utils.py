import json

def modificar_json(file_path, new_prompt, new_hr_prompt, neg_prompt, image_type):
    # Cargar el archivo JSON
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Crear una copia del diccionario original para no modificar la plantilla
    modified_data = data.copy()
    
    # Modificar los campos en la copia
    modified_data['prompt'] = new_prompt
    modified_data['hr_prompt'] = new_hr_prompt
    modified_data["negative_prompt"] = f"{modified_data['negative_prompt']},{neg_prompt}"
    
    if image_type == "Portrait":
        modified_data["width"] = 500
        modified_data["height"] = 500
    elif image_type == "Full Body":
        modified_data["width"] = 448
        modified_data["height"] = 888
    elif image_type == "Cowboy Shot":
        modified_data["width"] = 500
        modified_data["height"] = 700
    
    # Retornar el diccionario modificado
    return modified_data
