from django.db import migrations


# Los sliders de edad con tags reales y un cuerpo comun.
#
# Casi ningun tag de edad adulta existe en Danbooru, y los que usaban estos
# specials estaban TODOS en cero:
#
#   adult 0   woman 0   young woman 0   mature woman 0   older female 0
#
# GaSlider-Med pedia (adult:1.5), (woman:1.4) y (young woman:1.35): los tres
# muertos, asi que no aportaba nada mas que el LoRA. GaSlider-High pedia
# (mature woman:1.3), tambien muerto. Los unicos reales son mature_female
# (49.926), aged_up (37.098) y old_woman (3.703).
#
# Lo mismo del lado del cuerpo: slim, flat stomach, hourglass figure,
# voluptuous y athletic tienen 0 posts. El cuerpo comun se arma con los que
# si existen: narrow waist (16.301), curvy (76.981), wide hips (58.773),
# toned (60.968), thick thighs (161.548) y large breasts.
#
# Se agrega GaSlider-Old, que faltaba: la escala tenia el tramo hacia mayor
# sin cubrir, el LoRA en 1.5 contra el 0.5 de High.
#
# De paso, GaSlider-Med arrancaba con un backtick suelto, el mismo bug que
# tenia BD-COS/Tsunade.
CAMBIOS = [['GaSlider-High', '<lora:StS_Age_Slider_Illustrious_v1:.5>,(mature woman:1.3),(narrow waist:1.2)', '<lora:StS_Age_Slider_Illustrious_v1:.5>,\n(mature female:1.45),\n(aged up:1.30),\n(narrow waist:1.35),\n(curvy:1.30),\n(wide hips:1.25),\n(toned:1.20),\n(thick thighs:1.20),\n(large breasts:1.20)'], ['GaSlider-Med', "`<lora:StS_Age_Slider_Illustrious_v1:-1>, (adult:1.5), (woman:1.4), (young woman:1.35), (healthy complexion:1.15), <neg:(mature woman:1.3),(teen:1.3),(adolescent:1.3),(baby face:1.3),(wrinkles:1.3),(facial wrinkles:1.3),(crow's feet:1.3),(nasolabial folds:1.3),(sagging skin:1.3)>`", '<lora:StS_Age_Slider_Illustrious_v1:-1>,\n(aged up:1.45),\n(narrow waist:1.35),\n(curvy:1.30),\n(wide hips:1.25),\n(toned:1.20),\n(thick thighs:1.20),\n(large breasts:1.20)']]

NUEVOS = [['GaSlider-Old', '<lora:StS_Age_Slider_Illustrious_v1:1.5>,\n(old woman:1.45),\n(mature female:1.35),\n(narrow waist:1.35),\n(curvy:1.30),\n(wide hips:1.25),\n(toned:1.20),\n(thick thighs:1.20),\n(large breasts:1.20)']]


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, _viejo, nuevo in CAMBIOS:
        s = Special.objects.filter(name=nombre).first()
        if s is not None:
            s.prompt = nuevo
            s.save(update_fields=["prompt"])
    for nombre, prompt in NUEVOS:
        if Special.objects.filter(name=nombre).exists():
            continue
        Special.objects.create(name=nombre, tier="tier5", prompt=prompt)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()
    for nombre, viejo, _nuevo in CAMBIOS:
        s = Special.objects.filter(name=nombre).first()
        if s is not None:
            s.prompt = viejo
            s.save(update_fields=["prompt"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0063_hair_mas_peso"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
