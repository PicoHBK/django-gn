from django.db import migrations


# Las seis medidas pasan a los buckets nativos de SDXL. El modelo se entreno
# en 9 resoluciones fijas de ~1 megapixel, y generar fuera de esas es lo que
# produce cabezas duplicadas, cuerpos estirados y mal encuadre.
#
#   Full Body    800x1200 ->  832x1216   +5% px
#   3:4          876x1100 ->  896x1152   +7%
#   Cowboy Shot  800x1100 ->  832x1216  +15%
#   1:1          912x1050 -> 1024x1024   +7%
#   4:3         1100x876  -> 1152x896    +7%
#   Portrait     720x720  -> 1024x1024 +102%
#
# Portrait era el caso grave: 518.400 pixeles contra el millon del bucket, o
# sea a menos de la mitad. Su ratio ya era 1:1 exacto, asi que sube sin
# cambiar proporcion.
#
# "1:1" va a 1024x1024 aunque su bucket mas cercano por ratio sea 896x1152:
# ese ya lo usa "3:4" y quedarian identicos. Ademas 1024x1024 es lo que su
# nombre promete, porque 912x1050 nunca fue cuadrado.
#
# Quedan tres canvas compartidos -Full Body y Cowboy Shot en 832x1216, 1:1 y
# Portrait en 1024x1024- pero cada uno conserva su prompt propio, que es lo
# que los diferencia: cowboy shot, full body o portrait + close-up.
MEDIDAS = [
    ("Full Body", 832, 1216, 800, 1200),
    ("3:4", 896, 1152, 876, 1100),
    ("Cowboy Shot", 832, 1216, 800, 1100),
    ("1:1", 1024, 1024, 912, 1050),
    ("4:3", 1152, 896, 1100, 876),
    ("Portrait", 1024, 1024, 720, 720),
]


def _set(apps, i_w, i_h):
    ImageType = apps.get_model("generate", "ImageType")
    for m in MEDIDAS:
        i = ImageType.objects.filter(name=m[0]).first()
        if i is None:
            continue
        i.width, i.height = m[i_w], m[i_h]
        i.save(update_fields=["width", "height"])


def aplicar(apps, schema_editor):
    _set(apps, 1, 2)


def revertir(apps, schema_editor):
    _set(apps, 3, 4)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0076_full_body_margen"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
