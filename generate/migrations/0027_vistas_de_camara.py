from django.db import migrations


# Serie V: vistas de camara. Solo el punto de vista, nada de encuadre
# (cowboy shot, full body) ni de pose o mirada, que se deciden por otro lado.
#
# Cada una es una mezcla de dos tags que existe de verdad en Danbooru, con el
# conteo de posts al lado. Las combinaciones sueltas o raras quedaron afuera
# porque el modelo no las resuelve: fisheye con cualquier cosa (~550 posts),
# vanishing point + from below (44), sideways + dutch angle (140).
#
# Pesos altos a proposito, de 1.55 a 1.80: una vista tibia no se nota.
#
# SIN tags_deleted, al reves que los specials de pelo. Aca romperian poses:
# toda la familia SFB-* lleva "(sex from behind:1.2)" y un tag "behind" se la
# llevaria. La pose dice que pasa y usa las mismas palabras que la vista, asi
# que estas trabajan solo con el negativo.
#
# En el negativo no se usan "from front" ni "eye level": no son tags de
# Danbooru (0 posts). El opuesto de un angulo se niega con "straight-on".
VISTAS = [
    (
        "V1", "3/4 trasera", 10662,
        "(from behind:1.75),\n(from side:1.60),\n\n"
        "<neg:\nstraight-on:1.70,\nfrom above:1.60,\nfrom below:1.60\n>",
    ),
    (
        "V2", "contrapicado desde atras", 10504,
        "(from below:1.80),\n(from behind:1.65),\n\n"
        "<neg:\nfrom above:1.75,\nstraight-on:1.65,\nfrom side:1.50\n>",
    ),
    (
        "V3", "inclinada desde atras", 8235,
        "(dutch angle:1.80),\n(from behind:1.65),\n\n"
        "<neg:\nstraight-on:1.70,\nfrom side:1.50,\nfrom above:1.50\n>",
    ),
    (
        "V5", "inclinada contrapicada", 7918,
        "(dutch angle:1.75),\n(from below:1.70),\n\n"
        "<neg:\nfrom above:1.75,\nstraight-on:1.70\n>",
    ),
    (
        "V6", "inclinada de costado", 6368,
        "(dutch angle:1.80),\n(from side:1.65),\n\n"
        "<neg:\nstraight-on:1.70,\nfrom behind:1.55,\nfrom above:1.50\n>",
    ),
    (
        "V7", "picado desde atras", 5666,
        "(from above:1.80),\n(from behind:1.65),\n\n"
        "<neg:\nfrom below:1.75,\nstraight-on:1.65,\nfrom side:1.50\n>",
    ),
    (
        "V8", "escorzo fuerte contrapicado", 5187,
        "(foreshortening:1.80),\n(from below:1.70),\n(perspective:1.55),\n\n"
        "<neg:\nfrom above:1.75,\nstraight-on:1.70\n>",
    ),
]


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")

    for nombre, _que_es, _posts, prompt in VISTAS:
        if Special.objects.filter(name=nombre).exists():
            continue
        Special.objects.create(name=nombre, tier="tier1", prompt=prompt)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[v[0] for v in VISTAS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0026_hair_largo_cintura"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
