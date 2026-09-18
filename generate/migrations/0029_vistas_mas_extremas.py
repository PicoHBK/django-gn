from django.db import migrations


# Rediseño de la serie V. La primera version se parecia demasiado entre si:
# cuatro de las siete eran "from behind" con una variante encima y tres
# compartian "dutch angle". El problema no era el peso, era que se pisaban.
#
# Ahora cada V se queda con UN eje distinto, llevado al extremo, y niega los
# otros con fuerza. El negativo es lo que hace el trabajo: si pedis "from
# below" sin negar "from above" y "straight-on", el modelo promedia y te
# devuelve la camara a la altura de los ojos, que es su default.
#
# Los dominantes van en 1.90. Si alguna quema o deforma, bajar ese numero a
# 1.75 antes que tocar el resto: el peso alto en tags de camara empieza a
# comerse la composicion.
CAMBIOS = [
    (
        'V1',
        # cenital: la camara justo arriba, mirando al piso
        '(from behind:1.75),\n(from side:1.60),\n\n<neg:\nstraight-on:1.70,\nfrom above:1.60,\nfrom below:1.60\n>',
        '(from above:1.90),\n(foreshortening:1.65),\n\n<neg:\nfrom below:1.85,\nstraight-on:1.80,\nfrom side:1.70,\nfrom behind:1.60\n>',
    ),
    (
        'V2',
        # la camara APOYADA en el piso, mirando para arriba
        '(from below:1.80),\n(from behind:1.65),\n\n<neg:\nfrom above:1.75,\nstraight-on:1.65,\nfrom side:1.50\n>',
        '(from below:1.90),\n(foreshortening:1.70),\n\n<neg:\nfrom above:1.85,\nstraight-on:1.80,\nfrom side:1.70,\nfrom behind:1.60\n>',
    ),
    (
        'V3',
        # perfil puro, 90 grados al costado
        '(dutch angle:1.80),\n(from behind:1.65),\n\n<neg:\nstraight-on:1.70,\nfrom side:1.50,\nfrom above:1.50\n>',
        '(from side:1.90),\n\n<neg:\nfrom behind:1.80,\nfrom above:1.80,\nfrom below:1.80,\nstraight-on:1.60\n>',
    ),
    (
        'V5',
        # espalda total, atras del todo
        '(dutch angle:1.75),\n(from below:1.70),\n\n<neg:\nfrom above:1.75,\nstraight-on:1.70\n>',
        '(from behind:1.90),\n\n<neg:\nfrom side:1.80,\nfrom above:1.80,\nfrom below:1.80,\nstraight-on:1.60\n>',
    ),
    (
        'V6',
        # camara rotada, horizonte torcido
        '(dutch angle:1.80),\n(from side:1.65),\n\n<neg:\nstraight-on:1.70,\nfrom behind:1.55,\nfrom above:1.50\n>',
        '(dutch angle:1.90),\n(perspective:1.60),\n\n<neg:\nstraight-on:1.85\n>',
    ),
    (
        'V7',
        # escorzo brutal, lo cercano enorme y lo lejano chico
        '(from above:1.80),\n(from behind:1.65),\n\n<neg:\nfrom below:1.75,\nstraight-on:1.65,\nfrom side:1.50\n>',
        '(foreshortening:1.90),\n(perspective:1.75),\n(vanishing point:1.55),\n\n<neg:\nstraight-on:1.80\n>',
    ),
    (
        'V8',
        # ojo de pez, todo curvado
        '(foreshortening:1.80),\n(from below:1.70),\n(perspective:1.55),\n\n<neg:\nfrom above:1.75,\nstraight-on:1.70\n>',
        '(fisheye:1.90),\n(perspective:1.70),\n(foreshortening:1.60),\n\n<neg:\nstraight-on:1.80\n>',
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
        ("generate", "0028_one_eye_pelo_no_mano"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
