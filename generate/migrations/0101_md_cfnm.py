from django.db import migrations


# MD (CFNM: clothed female nude male) tenia dos problemas.
#
# 1) "naked male" no existe: 0 posts. Tampoco nude_male, male_nudity, clothed
#    ni fully_clothed, los cinco en 0. El unico tag real que dice esto es
#    clothed_female_nude_male (60.303), asi que todo el concepto cuelga de ese
#    token y por eso sube a 1.70: no tiene con quien repartirse el peso.
#
# 2) Estaba en tier1, que es lo que el front muestra a cualquiera. El tag
#    implica un hombre desnudo; el grupo Fell- usa este mismo tag y esta en
#    tier4. Se corrige la fuga.
#
# Mejoras: penis + uncensored para que la desnudez del hombre se vea en vez de
# quedar censurada o fuera de cuadro, y el espejo clothed_male_nude_female
# (11.654) al negativo, que es el competidor real: el modelo confunde las dos
# composiciones todo el tiempo porque son identicas salvo quien esta vestido.
NOMBRE = "MD"

PROMPT = """(clothed female nude male:1.70),
(penis:1.35),
(uncensored:1.30)

<neg:
clothed male nude female:1.55,
censored:1.45,
mosaic censoring:1.40,
bar censor:1.40
>"""

ANTERIOR = "(clothed_female_nude_male:1.6),(naked male:1.3)"


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name=NOMBRE).update(prompt=PROMPT, tier="tier4")


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name=NOMBRE).update(prompt=ANTERIOR, tier="tier1")


class Migration(migrations.Migration):

    dependencies = [("generate", "0100_emotes_ext")]

    operations = [migrations.RunPython(aplicar, revertir)]
