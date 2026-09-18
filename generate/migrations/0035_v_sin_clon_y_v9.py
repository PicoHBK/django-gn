from django.db import migrations


# Dos arreglos en la serie V.
#
# 1. Se va "zoom layer" del positivo de V1, V5 y V8. Era el que metia al
#    personaje duplicado. El wiki de Danbooru lo dice literal: "an additional
#    layer that magnifies part of the illustration, usually a character...
#    commonly used for backgrounds in character art". Le estabamos pidiendo la
#    copia ampliada en el fondo. Lo reemplaza "blurry background".
#
#    "zoom layer" y "multiple views" pasan al negativo de las nueve.
#
#    NO se niega "multiple girls" ni se fuerza "solo" a proposito: la familia
#    SFB-* son poses de dos personas legitimas y se romperian. zoom layer y
#    multiple views son especificamente el clon del mismo pj, no un segundo
#    personaje.
#
# 2. Nace V9, el contrapicado extremo: la camara en el piso mirando para
#    arriba. "low angle" no existe en Danbooru (0 posts), el tag es
#    "from below", aca en 1.90 con foreshortening en 1.85 para que la
#    deformacion de la distancia haga sentir lo bajo que esta la camara.
CAMBIOS = [
    (
        'V1',
        '(from above:1.80),\n(from side:1.75),\n(foreshortening:1.70),\n(depth of field:1.60),\n(zoom layer:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\ndutch angle:1.55,\nfrom behind:1.60\n>',
        '(from above:1.80),\n(from side:1.75),\n(foreshortening:1.70),\n(depth of field:1.60),\n(blurry background:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\ndutch angle:1.55,\nfrom behind:1.60,\nzoom layer:1.70,\nmultiple views:1.70\n>',
    ),
    (
        'V2',
        '(from below:1.80),\n(from side:1.75),\n(foreshortening:1.80),\n(depth of field:1.60),\n(blurry foreground:1.50),\n\n<neg:\nfrom above:1.80,\nstraight-on:1.75,\ndutch angle:1.55,\nfrom behind:1.60\n>',
        '(from below:1.80),\n(from side:1.75),\n(foreshortening:1.80),\n(depth of field:1.60),\n(blurry foreground:1.50),\n\n<neg:\nfrom above:1.80,\nstraight-on:1.75,\ndutch angle:1.55,\nfrom behind:1.60,\nzoom layer:1.70,\nmultiple views:1.70\n>',
    ),
    (
        'V3',
        '(from behind:1.80),\n(from side:1.75),\n(depth of field:1.65),\n(blurry foreground:1.60),\n(foreshortening:1.55),\n\n<neg:\nfrom above:1.70,\nfrom below:1.70,\nstraight-on:1.75,\ndutch angle:1.55\n>',
        '(from behind:1.80),\n(from side:1.75),\n(depth of field:1.65),\n(blurry foreground:1.60),\n(foreshortening:1.55),\n\n<neg:\nfrom above:1.70,\nfrom below:1.70,\nstraight-on:1.75,\ndutch angle:1.55,\nzoom layer:1.70,\nmultiple views:1.70\n>',
    ),
    (
        'V4',
        '(foreshortening:1.90),\n(leaning forward:1.75),\n(looking at viewer:1.70),\n(depth of field:1.65),\n(blurry background:1.55),\n\n<neg:\nfacing away:1.80,\nfrom behind:1.75,\nwide shot:1.70,\nfrom above:1.55,\nfrom below:1.55\n>',
        '(foreshortening:1.90),\n(leaning forward:1.75),\n(looking at viewer:1.70),\n(depth of field:1.65),\n(blurry background:1.55),\n\n<neg:\nfacing away:1.80,\nfrom behind:1.75,\nwide shot:1.70,\nfrom above:1.55,\nfrom below:1.55,\nzoom layer:1.70,\nmultiple views:1.70\n>',
    ),
    (
        'V5',
        '(from above:1.80),\n(from behind:1.75),\n(foreshortening:1.70),\n(zoom layer:1.60),\n(depth of field:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\ndutch angle:1.55,\nfrom side:1.60\n>',
        '(from above:1.80),\n(from behind:1.75),\n(foreshortening:1.70),\n(depth of field:1.55),\n(blurry background:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\ndutch angle:1.55,\nfrom side:1.60,\nzoom layer:1.70,\nmultiple views:1.70\n>',
    ),
    (
        'V6',
        '(dutch angle:1.85),\n(from below:1.80),\n(foreshortening:1.75),\n(depth of field:1.60),\n(chromatic aberration:1.50),\n\n<neg:\nfrom above:1.80,\nstraight-on:1.85\n>',
        '(dutch angle:1.85),\n(from below:1.80),\n(foreshortening:1.75),\n(depth of field:1.60),\n(chromatic aberration:1.50),\n\n<neg:\nfrom above:1.80,\nstraight-on:1.85,\nzoom layer:1.70,\nmultiple views:1.70\n>',
    ),
    (
        'V7',
        '(dutch angle:1.85),\n(from behind:1.80),\n(depth of field:1.65),\n(blurry foreground:1.55),\n(chromatic aberration:1.50),\n\n<neg:\nstraight-on:1.85,\nfrom above:1.60,\nfrom below:1.60\n>',
        '(dutch angle:1.85),\n(from behind:1.80),\n(depth of field:1.65),\n(blurry foreground:1.55),\n(chromatic aberration:1.50),\n\n<neg:\nstraight-on:1.85,\nfrom above:1.60,\nfrom below:1.60,\nzoom layer:1.70,\nmultiple views:1.70\n>',
    ),
    (
        'V8',
        '(foreshortening:1.90),\n(from above:1.80),\n(fisheye:1.65),\n(depth of field:1.60),\n(zoom layer:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\ndutch angle:1.55\n>',
        '(foreshortening:1.90),\n(from above:1.80),\n(fisheye:1.65),\n(depth of field:1.60),\n(blurry background:1.55),\n\n<neg:\nfrom below:1.80,\nstraight-on:1.75,\ndutch angle:1.55,\nzoom layer:1.70,\nmultiple views:1.70\n>',
    ),
]

V9_PROMPT = (
    "(from below:1.90),\n"
    "(foreshortening:1.85),\n"
    "(depth of field:1.60),\n"
    "(blurry background:1.50),\n"
    "\n"
    "<neg:\n"
    "from above:1.90,\n"
    "straight-on:1.85,\n"
    "from side:1.55,\n"
    "zoom layer:1.70,\n"
    "multiple views:1.70\n"
    ">"
)


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, _viejo, nuevo in CAMBIOS:
        s = Special.objects.filter(name=nombre).first()
        if s is None:
            continue
        s.prompt = nuevo
        s.save(update_fields=["prompt"])
    if not Special.objects.filter(name="V9").exists():
        Special.objects.create(name="V9", tier="tier1", prompt=V9_PROMPT)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, viejo, _nuevo in CAMBIOS:
        s = Special.objects.filter(name=nombre).first()
        if s is None:
            continue
        s.prompt = viejo
        s.save(update_fields=["prompt"])
    Special.objects.filter(name="V9").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0034_poses_focus"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
