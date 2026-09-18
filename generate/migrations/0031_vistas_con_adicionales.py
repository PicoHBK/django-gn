from django.db import migrations


# La serie V pasa a cinco tags por vista. El par de direcciones es la base y
# encima van los adicionales de camara, que es lo que hace que la vista se
# note: foreshortening deforma segun la distancia, perspective marca la fuga,
# vanishing point la refuerza.
#
# "low angle" y "high angle" NO existen en Danbooru (0 posts los dos). Lo que
# en fotografia se llama asi, aca se dice "from below" y "from above".
#
# Las que no son inclinadas niegan "dutch angle" a proposito: es lo que las
# separa de V6 y V7, que si van torcidas.
#
# Si alguna sale mezclada o deformada de mas, el primer numero a bajar es el
# del tag dominante. Apilar varios tags de camara arriba de 1.7 compite por
# atencion y en algun punto degrada.
CAMBIOS = [
    (
        'V1',
        # picado lateral
        '(from above:1.80),\n(from side:1.75),\n(perspective:1.60),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.70,\nfrom behind:1.60\n>',
        '(from above:1.80),\n(from side:1.75),\n(foreshortening:1.70),\n(perspective:1.65),\n(vanishing point:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\nfrom behind:1.60,\ndutch angle:1.55\n>',
    ),
    (
        'V2',
        # contrapicado lateral
        '(from below:1.80),\n(from side:1.75),\n(foreshortening:1.65),\n\n<neg:\nfrom above:1.80,\nstraight-on:1.70,\nfrom behind:1.60\n>',
        '(from below:1.80),\n(from side:1.75),\n(foreshortening:1.75),\n(perspective:1.65),\n(vanishing point:1.60),\n\n<neg:\nfrom above:1.80,\nstraight-on:1.75,\nfrom behind:1.60,\ndutch angle:1.55\n>',
    ),
    (
        'V3',
        # 3/4 trasera
        '(from behind:1.80),\n(from side:1.75),\n(perspective:1.55),\n\n<neg:\nfrom above:1.70,\nfrom below:1.70,\nstraight-on:1.65\n>',
        '(from behind:1.80),\n(from side:1.75),\n(perspective:1.70),\n(foreshortening:1.60),\n(vanishing point:1.55),\n\n<neg:\nfrom above:1.70,\nfrom below:1.70,\nstraight-on:1.70,\ndutch angle:1.55\n>',
    ),
    (
        'V5',
        # picado trasero
        '(from above:1.80),\n(from behind:1.75),\n(foreshortening:1.60),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.70,\nfrom side:1.60\n>',
        '(from above:1.80),\n(from behind:1.75),\n(foreshortening:1.70),\n(perspective:1.65),\n(vanishing point:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\nfrom side:1.60,\ndutch angle:1.55\n>',
    ),
    (
        'V6',
        # inclinada contrapicada
        '(dutch angle:1.85),\n(from below:1.75),\n(foreshortening:1.65),\n\n<neg:\nfrom above:1.80,\nstraight-on:1.85\n>',
        '(dutch angle:1.85),\n(from below:1.80),\n(foreshortening:1.75),\n(perspective:1.65),\n(vanishing point:1.55),\n\n<neg:\nfrom above:1.80,\nstraight-on:1.85\n>',
    ),
    (
        'V7',
        # inclinada trasera
        '(dutch angle:1.85),\n(from behind:1.75),\n(perspective:1.60),\n\n<neg:\nstraight-on:1.85,\nfrom above:1.60,\nfrom below:1.60\n>',
        '(dutch angle:1.85),\n(from behind:1.80),\n(perspective:1.70),\n(foreshortening:1.65),\n(chromatic aberration:1.50),\n\n<neg:\nstraight-on:1.85,\nfrom above:1.60,\nfrom below:1.60\n>',
    ),
    (
        'V8',
        # escorzo picado
        '(foreshortening:1.85),\n(from above:1.75),\n(perspective:1.70),\n(vanishing point:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75\n>',
        '(foreshortening:1.90),\n(from above:1.80),\n(perspective:1.75),\n(vanishing point:1.65),\n(fisheye:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\ndutch angle:1.55\n>',
    ),
]


def _set(apps, indice):
    Special = apps.get_model("generate", "Special")
    for cambio in CAMBIOS:
        s = Special.objects.filter(name=cambio[0]).first()
        if s is None:
            continue
        s.prompt = cambio[indice]
        s.save(update_fields=["prompt"])


def aplicar(apps, schema_editor):
    _set(apps, 2)


def revertir(apps, schema_editor):
    _set(apps, 1)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0030_vistas_combinadas"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
