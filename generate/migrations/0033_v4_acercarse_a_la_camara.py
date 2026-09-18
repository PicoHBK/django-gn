from django.db import migrations


# V4: el pj se acerca al lente y la cara manda.
#
# No hay tag de camara para esto. Probados y descartados por inexistentes:
# "close to viewer", "face focus", "face to face", "looking down at viewer"
# (0 posts los cuatro). "eye focus" existe pero es solo de primer plano: 95
# posts con full_body y 30 con cowboy_shot, no sirve.
#
# El unico que da el efecto y sobrevive a los dos encuadres es
# "leaning forward": 20.200 con full_body, 30.525 con cowboy_shot.
#
# Es la unica V que toca al sujeto y no solo a la camara. No habia otra forma:
# para que la cara se acerque al lente, alguien se tiene que mover. El resto
# del stack es camara pura, y "foreshortening" en 1.90 es lo que hace que lo
# mas cercano (la cara) salga grande y el cuerpo se vaya para atras.
#
# No lleva "close-up" ni "portrait" a proposito. Esos recortan al rostro y
# romperian la regla de la serie: la vista tiene que andar igual con el pj en
# full body o en cowboy shot.
NOMBRE = "V4"

PROMPT = (
    "(foreshortening:1.90),\n"
    "(leaning forward:1.75),\n"
    "(looking at viewer:1.70),\n"
    "(depth of field:1.65),\n"
    "(blurry background:1.55),\n"
    "\n"
    "<neg:\n"
    "facing away:1.80,\n"
    "from behind:1.75,\n"
    "wide shot:1.70,\n"
    "from above:1.55,\n"
    "from below:1.55\n"
    ">"
)


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    if Special.objects.filter(name=NOMBRE).exists():
        return
    Special.objects.create(name=NOMBRE, tier="tier1", prompt=PROMPT)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name=NOMBRE).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0032_vistas_tags_de_personaje"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
