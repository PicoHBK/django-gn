from django.db import migrations


# La serie V pasa a ser siete PARES distintos. Antes tenia vistas basicas
# sueltas, que ya existen como specials propios y estaba duplicando:
#
#   727 ▲ (from above)   728 ▼ (from below)   729 ◀ (from side)
#   856 Fb (from behind) 433 From Below,Behind
#
# Por eso tampoco se usa "from below + from behind": eso es el 433.
#
# Cada V es una combinacion unica de dos direcciones, o de una direccion con
# un tag de camara (dutch angle, foreshortening), mas un refuerzo de
# perspectiva. Entre parentesis, los posts reales de Danbooru que tiene esa
# combinacion: por debajo de ~3.000 el modelo no la resuelve.
#
# Ojo: "low angle" y "high angle" NO son tags de Danbooru, 0 posts los dos.
# El 433 tiene un "low angle" suelto que no hace nada. Los reales son
# "from below" y "from above".
#
# El negativo niega la direccion opuesta en los dos ejes. Es lo que hace la
# fuerza: sin el, el modelo promedia y deja la camara a la altura de los ojos.
CAMBIOS = [
    (
        'V1',
        # picado lateral: arriba y al costado  (4532 posts)
        '(from above:1.90),\n(foreshortening:1.65),\n\n<neg:\nfrom below:1.85,\nstraight-on:1.80,\nfrom side:1.70,\nfrom behind:1.60\n>',
        '(from above:1.80),\n(from side:1.75),\n(perspective:1.60),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.70,\nfrom behind:1.60\n>',
    ),
    (
        'V2',
        # contrapicado lateral: desde abajo y al costado  (3340 posts)
        '(from below:1.90),\n(foreshortening:1.70),\n\n<neg:\nfrom above:1.85,\nstraight-on:1.80,\nfrom side:1.70,\nfrom behind:1.60\n>',
        '(from below:1.80),\n(from side:1.75),\n(foreshortening:1.65),\n\n<neg:\nfrom above:1.80,\nstraight-on:1.70,\nfrom behind:1.60\n>',
    ),
    (
        'V3',
        # 3/4 trasera: atras y corrido al costado  (10662 posts)
        '(from side:1.90),\n\n<neg:\nfrom behind:1.80,\nfrom above:1.80,\nfrom below:1.80,\nstraight-on:1.60\n>',
        '(from behind:1.80),\n(from side:1.75),\n(perspective:1.55),\n\n<neg:\nfrom above:1.70,\nfrom below:1.70,\nstraight-on:1.65\n>',
    ),
    (
        'V5',
        # picado trasero: desde arriba y por detras  (5666 posts)
        '(from behind:1.90),\n\n<neg:\nfrom side:1.80,\nfrom above:1.80,\nfrom below:1.80,\nstraight-on:1.60\n>',
        '(from above:1.80),\n(from behind:1.75),\n(foreshortening:1.60),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.70,\nfrom side:1.60\n>',
    ),
    (
        'V6',
        # inclinada contrapicada: torcida y desde abajo  (7918 posts)
        '(dutch angle:1.90),\n(perspective:1.60),\n\n<neg:\nstraight-on:1.85\n>',
        '(dutch angle:1.85),\n(from below:1.75),\n(foreshortening:1.65),\n\n<neg:\nfrom above:1.80,\nstraight-on:1.85\n>',
    ),
    (
        'V7',
        # inclinada trasera: torcida y por detras  (8235 posts)
        '(foreshortening:1.90),\n(perspective:1.75),\n(vanishing point:1.55),\n\n<neg:\nstraight-on:1.80\n>',
        '(dutch angle:1.85),\n(from behind:1.75),\n(perspective:1.60),\n\n<neg:\nstraight-on:1.85,\nfrom above:1.60,\nfrom below:1.60\n>',
    ),
    (
        'V8',
        # escorzo picado: deformado y desde arriba  (5302 posts)
        '(fisheye:1.90),\n(perspective:1.70),\n(foreshortening:1.60),\n\n<neg:\nstraight-on:1.80\n>',
        '(foreshortening:1.85),\n(from above:1.75),\n(perspective:1.70),\n(vanishing point:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75\n>',
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
        ("generate", "0029_vistas_mas_extremas"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
