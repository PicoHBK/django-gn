from django.db import migrations


# Se van "perspective" y "vanishing point" de la serie V. Medidos contra los
# dos encuadres, casi no existen en fotos de personaje:
#
#                     con full_body   con cowboy_shot
#   perspective            1.230             348
#   vanishing point          134              21
#
# Son tags de arquitectura y paisaje. Estaban de refuerzo y no reforzaban nada.
#
# Entran en su lugar los que si aparecen en los dos encuadres, que es el
# requisito: la vista tiene que servir igual con el pj de cuerpo entero o de
# la cintura para arriba.
#
#                     con full_body   con cowboy_shot
#   foreshortening        11.983           5.166
#   zoom layer            12.287           3.207
#   depth of field         7.308          15.959
#   blurry foreground      2.827           4.035
#   dutch angle            9.488          25.231
#
# Ninguna V lleva tags de encuadre ni de pose, a proposito: el encuadre lo
# decide el otro prompt y la vista tiene que poder montarse encima de
# cualquier pose.
#
# Cada V tiene un set de cinco tags que no se repite en ninguna otra.
CAMBIOS = [
    (
        'V1',
        # picado lateral con capas de profundidad
        '(from above:1.80),\n(from side:1.75),\n(foreshortening:1.70),\n(perspective:1.65),\n(vanishing point:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\nfrom behind:1.60,\ndutch angle:1.55\n>',
        '(from above:1.80),\n(from side:1.75),\n(foreshortening:1.70),\n(depth of field:1.60),\n(zoom layer:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\ndutch angle:1.55,\nfrom behind:1.60\n>',
    ),
    (
        'V2',
        # contrapicado lateral, escorzo fuerte
        '(from below:1.80),\n(from side:1.75),\n(foreshortening:1.75),\n(perspective:1.65),\n(vanishing point:1.60),\n\n<neg:\nfrom above:1.80,\nstraight-on:1.75,\nfrom behind:1.60,\ndutch angle:1.55\n>',
        '(from below:1.80),\n(from side:1.75),\n(foreshortening:1.80),\n(depth of field:1.60),\n(blurry foreground:1.50),\n\n<neg:\nfrom above:1.80,\nstraight-on:1.75,\ndutch angle:1.55,\nfrom behind:1.60\n>',
    ),
    (
        'V3',
        # 3/4 trasera espiando por delante
        '(from behind:1.80),\n(from side:1.75),\n(perspective:1.70),\n(foreshortening:1.60),\n(vanishing point:1.55),\n\n<neg:\nfrom above:1.70,\nfrom below:1.70,\nstraight-on:1.70,\ndutch angle:1.55\n>',
        '(from behind:1.80),\n(from side:1.75),\n(depth of field:1.65),\n(blurry foreground:1.60),\n(foreshortening:1.55),\n\n<neg:\nfrom above:1.70,\nfrom below:1.70,\nstraight-on:1.75,\ndutch angle:1.55\n>',
    ),
    (
        'V5',
        # picado trasero por capas
        '(from above:1.80),\n(from behind:1.75),\n(foreshortening:1.70),\n(perspective:1.65),\n(vanishing point:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\nfrom side:1.60,\ndutch angle:1.55\n>',
        '(from above:1.80),\n(from behind:1.75),\n(foreshortening:1.70),\n(zoom layer:1.60),\n(depth of field:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\ndutch angle:1.55,\nfrom side:1.60\n>',
    ),
    (
        'V6',
        # inclinada contrapicada con aberracion
        '(dutch angle:1.85),\n(from below:1.80),\n(foreshortening:1.75),\n(perspective:1.65),\n(vanishing point:1.55),\n\n<neg:\nfrom above:1.80,\nstraight-on:1.85\n>',
        '(dutch angle:1.85),\n(from below:1.80),\n(foreshortening:1.75),\n(depth of field:1.60),\n(chromatic aberration:1.50),\n\n<neg:\nfrom above:1.80,\nstraight-on:1.85\n>',
    ),
    (
        'V7',
        # inclinada trasera con primer plano
        '(dutch angle:1.85),\n(from behind:1.80),\n(perspective:1.70),\n(foreshortening:1.65),\n(chromatic aberration:1.50),\n\n<neg:\nstraight-on:1.85,\nfrom above:1.60,\nfrom below:1.60\n>',
        '(dutch angle:1.85),\n(from behind:1.80),\n(depth of field:1.65),\n(blurry foreground:1.55),\n(chromatic aberration:1.50),\n\n<neg:\nstraight-on:1.85,\nfrom above:1.60,\nfrom below:1.60\n>',
    ),
    (
        'V8',
        # escorzo picado con ojo de pez
        '(foreshortening:1.90),\n(from above:1.80),\n(perspective:1.75),\n(vanishing point:1.65),\n(fisheye:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\ndutch angle:1.55\n>',
        '(foreshortening:1.90),\n(from above:1.80),\n(fisheye:1.65),\n(depth of field:1.60),\n(zoom layer:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\ndutch angle:1.55\n>',
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
        ("generate", "0031_vistas_con_adicionales"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
