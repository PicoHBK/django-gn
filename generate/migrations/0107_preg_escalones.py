from django.db import migrations


# Las tres etapas salian iguales porque el tamano de la panza no lo da el peso
# de (pregnant). Su wiki dice "use this tag only when the character has a
# visibly pregnant belly": es binario. Subirlo o bajarlo cambia cuanta
# confianza le pone el modelo, no cuantos meses.
#
# La escala real son tres tags distintos que Danbooru define como NO
# solapados:
#   implied_pregnancy (1.112) "suggests pregnancy, but the character is not
#                              visibly pregnant"
#   belly             (23.550) "somewhat plump, but not as large or pronounced
#                              as a big belly"
#   big_belly         (8.409)  "larger than a typical pregnant belly"
# y el wiki de belly remata: "Don't tag big bellies as belly, as the tags
# don't overlap".
#
# Por eso cada etapa ademas NIEGA los marcadores de las otras dos: es lo que
# hace que se vean distintas en vez de converger todas en la panza maxima.
#
# No hay vocabulario por meses donde agarrarse: baby_bump, maternity,
# slightly_pregnant, early_pregnancy, third_trimester, plump_belly y potbelly
# son todos 0 y sin alias.

NUEVOS = {
    # temprana: se intuye, todavia no es panza de embarazo
    "PregSlider-Low": (
        "(implied pregnancy:1.55),\n(belly:1.40),\n(pregnant:1.15),\n"
        "(navel:1.20),\n(narrow waist:1.30),\n(slender:1.20)\n\n"
        "<neg:\nbig belly:1.70,\nplump:1.30,\nfat:1.35,\nobese:1.30\n>"
    ),
    # media: la panza de embarazo tipica, ni mas ni menos
    "PregSlider-Normal": (
        "(pregnant:1.60),\n(navel:1.20),\n(narrow waist:1.20)\n\n"
        "<neg:\nbig belly:1.45,\nbelly:1.25,\nimplied pregnancy:1.40,\n"
        "fat:1.25,\nobese:1.25\n>"
    ),
    # full term: mas grande que la tipica, que es justo lo que define big belly
    "PregSlider-High": (
        "(pregnant:1.70),\n(big belly:1.65),\n(outie navel:1.35),\n"
        "(puffy nipples:1.25)\n\n"
        "<neg:\nbelly:1.50,\nimplied pregnancy:1.50,\nnarrow waist:1.30,\n"
        "fat:1.30,\nobese:1.30\n>"
    ),
}


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, prompt in NUEVOS.items():
        Special.objects.filter(name=nombre).update(prompt=prompt)


def revertir(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [("generate", "0106_preg_ga_tsunade")]

    operations = [migrations.RunPython(aplicar, revertir)]
