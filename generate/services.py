from .models import Special
import random
import re


def check_tier(resource_tier, code_tier):
    tiers_order = ["tier1", "tier2", "tier3", "tier4", "tier5"]
    try:
        resource_tier_index = tiers_order.index(resource_tier)
        code_tier_index = tiers_order.index(code_tier)
        print(resource_tier_index, code_tier_index)
        return code_tier_index >= resource_tier_index
    except ValueError:
        return False






def validate_special(special_name, code_tier, prompts):
    if special_name:
        special = Special.objects.filter(name=special_name).first()
        if special:
            if not check_tier(special.tier, code_tier):
                return " "
            else:
                # Obtener los nombres de los tags como una lista de strings
                prompts.append(special.prompt)
                tags = [tag.name for tag in special.tags_required.all()]
                tags_deleted = [tag.name for tag in special.tags_deleted.all()]  # Obtener los tags eliminados

                # Verificar si al menos uno de los tags está presente en cada elemento de prompts
                found_tag = False  # Variable para verificar si se encontró algún tag

                for prompt in prompts:
                    if any(tag in prompt for tag in tags):
                        found_tag = True
                        break  # Salir del bucle si se encuentra un tag en algún prompt

                # Si no se encontró ningún tag, agregar un tag aleatorio a la lista prompts
                if not found_tag:
                    random_tag = random.choice(tags)
                    prompts.append(f"({random_tag}:1.2)")  # Agregar el tag aleatorio

                # Depurar los prompts eliminando todas las palabras o cadenas que coincidan con los tags eliminados
                updated_prompts = []
                for prompt in prompts:
                    # Usamos expresiones regulares para eliminar las coincidencias con tags_deleted
                    for tag in tags_deleted:
                        # Eliminar las palabras o frases completas que coincidan con tags_deleted
                        prompt = re.sub(r'\b' + re.escape(tag) + r'\b', '', prompt)

                    # Filtrar espacios extra que puedan quedar
                    updated_prompts.append(' '.join(prompt.split()))

                return updated_prompts
    else:
        return " "


                
                

            
