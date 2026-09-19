from django.db import migrations


# Los sliders de edad, para que la edad se NOTE y no dependa solo del LoRA.
#
# Casi todo lo que pedian estaba muerto en Danbooru:
#   adult 0   woman 0   young woman 0   mature woman 0
# GaSlider-Med pedia los tres primeros y GaSlider-High el cuarto, asi que
# ninguno de los dos aportaba un solo tag vivo. Los reales son mature_female
# (49.926), aged_up (37.098) y old_woman (3.703).
#
# Para las marcas de edad pasa lo mismo: "wrinkles" a secas no existe, ni
# eye_bags, age_spots, laugh_lines o nasolabial_folds. El unico real es
# wrinkled_skin (4.656), que es el que se usa, en peso bajo para High
# -pocas arrugas- y alto para Old.
#
# Del lado joven tampoco existen youthful, baby_face, smooth_skin ni
# round_face. Por eso GaSlider-Med se apoya en aged_up: el LoRA en -1 baja la
# edad y aged_up la sostiene del lado adulto.
#
# Cuerpo comun en los tres, con los tags que si existen: narrow waist
# (16.301), curvy (76.981), wide hips (58.773), thick thighs (161.548) y
# toned (60.968). No se usan slim, flat stomach ni hourglass figure: 0 posts.
#
# Se agrega GaSlider-Old, que completa la escala hacia mayor: el LoRA en 1.5
# contra el 0.5 de High.
#
# GaSlider-Tee queda como estaba, no se toca.
CAMBIOS = [['GaSlider-High', '<lora:StS_Age_Slider_Illustrious_v1:.5>,(mature woman:1.3),(narrow waist:1.2)', '<lora:StS_Age_Slider_Illustrious_v1:.5>,\n(mature female:1.50),\n(huge breasts:1.40),\n(wrinkled skin:1.22),\n(sagging breasts:1.18),\n(mole under eye:1.15),\n(narrow waist:1.35),\n(curvy:1.30),\n(wide hips:1.28),\n(thick thighs:1.25),\n(toned:1.20)'], ['GaSlider-Med', "`<lora:StS_Age_Slider_Illustrious_v1:-1>, (adult:1.5), (woman:1.4), (young woman:1.35), (healthy complexion:1.15), <neg:(mature woman:1.3),(teen:1.3),(adolescent:1.3),(baby face:1.3),(wrinkles:1.3),(facial wrinkles:1.3),(crow's feet:1.3),(nasolabial folds:1.3),(sagging skin:1.3)>`", '<lora:StS_Age_Slider_Illustrious_v1:-1>,\n(aged up:1.45),\n(medium breasts:1.35),\n(shiny skin:1.30),\n(narrow waist:1.35),\n(curvy:1.30),\n(wide hips:1.28),\n(thick thighs:1.25),\n(toned:1.20)']]

NUEVOS = [['GaSlider-Old', '<lora:StS_Age_Slider_Illustrious_v1:1.5>,\n(old woman:1.45),\n(mature female:1.35),\n(wrinkled skin:1.45),\n(grey hair:1.25),\n(sagging breasts:1.25),\n(narrow waist:1.35),\n(curvy:1.30),\n(wide hips:1.28),\n(thick thighs:1.25),\n(toned:1.20)']]


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
