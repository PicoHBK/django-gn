from django.db import migrations


# Las poses Focus- pasan a ser de una sola persona.
#
# "solo" al positivo (7.080.923 posts) y al negativo los que meten gente de
# mas. Entre ellos "solo focus", que suena a lo que queremos pero es lo
# contrario: el wiki lo define como "an image containing multiple people, but
# focused on only a single person". Justamente permite que haya otros.
#
# Tambien van al negativo "zoom layer" y "multiple views", que son los que
# duplican al MISMO personaje, el mismo problema que tenia la serie V.
#
# Aca si se puede negar 1boy y multiple girls, al reves que en las V: una pose
# de focus es de un cuerpo y nada mas. Las poses de a dos, como la familia
# SFB-*, no se tocan.
CAMBIOS = [
    (
        'Focus-Armpits',
        '(armpit focus:1.5)',
        '(armpit focus:1.5),\n(solo:1.45),\n\n<neg:\nmultiple girls:1.60,\n2girls:1.60,\nmultiple boys:1.55,\n1boy:1.45,\nsolo focus:1.50,\nmultiple views:1.60,\nzoom layer:1.60\n>',
    ),
    (
        'Focus-Ass',
        '(ass focus:1.5)',
        '(ass focus:1.5),\n(solo:1.45),\n\n<neg:\nmultiple girls:1.60,\n2girls:1.60,\nmultiple boys:1.55,\n1boy:1.45,\nsolo focus:1.50,\nmultiple views:1.60,\nzoom layer:1.60\n>',
    ),
    (
        'Focus-Back',
        '(back focus:1.5)',
        '(back focus:1.5),\n(solo:1.45),\n\n<neg:\nmultiple girls:1.60,\n2girls:1.60,\nmultiple boys:1.55,\n1boy:1.45,\nsolo focus:1.50,\nmultiple views:1.60,\nzoom layer:1.60\n>',
    ),
    (
        'Focus-Breasts',
        '(breast focus:1.5)',
        '(breast focus:1.5),\n(solo:1.45),\n\n<neg:\nmultiple girls:1.60,\n2girls:1.60,\nmultiple boys:1.55,\n1boy:1.45,\nsolo focus:1.50,\nmultiple views:1.60,\nzoom layer:1.60\n>',
    ),
    (
        'Focus-Face',
        '(eye focus:1.5),(looking at viewer:1.3)',
        '(eye focus:1.5),(looking at viewer:1.3),\n(solo:1.45),\n\n<neg:\nmultiple girls:1.60,\n2girls:1.60,\nmultiple boys:1.55,\n1boy:1.45,\nsolo focus:1.50,\nmultiple views:1.60,\nzoom layer:1.60\n>',
    ),
    (
        'Focus-Feet',
        '(foot focus:1.5)',
        '(foot focus:1.5),\n(solo:1.45),\n\n<neg:\nmultiple girls:1.60,\n2girls:1.60,\nmultiple boys:1.55,\n1boy:1.45,\nsolo focus:1.50,\nmultiple views:1.60,\nzoom layer:1.60\n>',
    ),
    (
        'Focus-Hands',
        '(hand focus:1.5)',
        '(hand focus:1.5),\n(solo:1.45),\n\n<neg:\nmultiple girls:1.60,\n2girls:1.60,\nmultiple boys:1.55,\n1boy:1.45,\nsolo focus:1.50,\nmultiple views:1.60,\nzoom layer:1.60\n>',
    ),
    (
        'Focus-Hips',
        '(hip focus:1.5)',
        '(hip focus:1.5),\n(solo:1.45),\n\n<neg:\nmultiple girls:1.60,\n2girls:1.60,\nmultiple boys:1.55,\n1boy:1.45,\nsolo focus:1.50,\nmultiple views:1.60,\nzoom layer:1.60\n>',
    ),
    (
        'Focus-Legs',
        '(leg focus:1.5)',
        '(leg focus:1.5),\n(solo:1.45),\n\n<neg:\nmultiple girls:1.60,\n2girls:1.60,\nmultiple boys:1.55,\n1boy:1.45,\nsolo focus:1.50,\nmultiple views:1.60,\nzoom layer:1.60\n>',
    ),
    (
        'Focus-Thighs',
        '(thigh focus:1.5)',
        '(thigh focus:1.5),\n(solo:1.45),\n\n<neg:\nmultiple girls:1.60,\n2girls:1.60,\nmultiple boys:1.55,\n1boy:1.45,\nsolo focus:1.50,\nmultiple views:1.60,\nzoom layer:1.60\n>',
    ),
]


def _set(apps, indice):
    Pose = apps.get_model("generate", "Pose")
    for cambio in CAMBIOS:
        p = Pose.objects.filter(name=cambio[0]).first()
        if p is None:
            continue
        p.prompt = cambio[indice]
        p.save(update_fields=["prompt"])


def aplicar(apps, schema_editor):
    _set(apps, 2)


def revertir(apps, schema_editor):
    _set(apps, 1)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0035_v_sin_clon_y_v9"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
