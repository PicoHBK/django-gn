from django.db import migrations


# DA v2: el efecto salia flojo porque "dark skin" es un tag RELATIVO. El wiki
# de Danbooru lo dice literal: "skin darker than the usual Eurasian skin tone
# [...] sometimes due to a tan". O sea que dark-skinned + peso medio te da
# bronceado, no piel oscura.
#
# El extremo real de la escala es "very dark skin" (18.147 posts): "even darker
# than dark skin". Ese pasa a ser el tag principal con el peso mas alto.
#
# Y "tan" (78.946) va al negativo: es el efecto debil que estaba ganando.
#
# Descartados: "ebony" es un alias de very dark skin (post_count 0), asi que
# ese token nunca estuvo en los captions; "light skin" tiene 0 posts.
# "black skin" se niega flojo porque es piel negra SIN nada de marron, que da
# el look de monstruo en vez de persona.
NOMBRE = "DA"

PROMPT = """(very dark skin:1.80),
(dark-skinned female:1.70),
(dark-skinned male:1.70),
(dark skin:1.55),

<neg:
interracial:1.65,
tan:1.60,
tanlines:1.50,
pale skin:1.60,
white skin:1.55,
colored skin:1.40,
grey skin:1.35,
black skin:1.30,
two-tone skin:1.25
>"""

ANTERIOR = """(dark-skinned female:1.75),
(dark-skinned male:1.75),
(dark skin:1.60),
(very dark skin:1.25),

<neg:
interracial:1.65,
pale skin:1.60,
white skin:1.55,
tanlines:1.30
>"""


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name=NOMBRE).update(prompt=PROMPT)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name=NOMBRE).update(prompt=ANTERIOR)


class Migration(migrations.Migration):

    dependencies = [("generate", "0097_fell_variantes")]

    operations = [migrations.RunPython(aplicar, revertir)]
