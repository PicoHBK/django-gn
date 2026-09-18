from django.db import migrations


# Se unifica el duplicado de panties. Quedan dos poses haciendo lo mismo:
# Presenting-P (740), con un LORA entrenado para eso, y Presenting-Panties
# (868), que creamos con el tag "presenting removed panties" (1.174 posts).
#
# Gana la del LORA: un LORA entrenado especifico le gana a un tag de ese
# volumen. Pero se le pasa lo bueno de la otra, el tag de Danbooru y el
# bloqueo de una sola persona, y despues se borra la nueva.
#
# No se le cambia el nombre a la 740 aunque "Presenting-P" quede raro al lado
# del resto del grupo: views.py:329 busca las poses por NOMBRE, asi que un
# rename le rompe el front a cualquiera que la tenga guardada.
NOMBRE = "Presenting-P"

VIEJO = '<lora:presenting panties v0.1 ILL:.85>,holding panties,holding underwear,hp,holding microthong'

NUEVO = '<lora:presenting panties v0.1 ILL:.85>,holding panties,holding underwear,hp,holding microthong,\n(presenting removed panties:1.40),\n(solo:1.45),\n\n<neg:\nmultiple girls:1.60,\n2girls:1.60,\nmultiple boys:1.55,\n1boy:1.45,\nsolo focus:1.50,\nmultiple views:1.60,\nzoom layer:1.60\n>'

BORRAR = "Presenting-Panties"

BORRADA = (
    "(presenting removed panties:1.5),\n(solo:1.45),\n\n<neg:\n"
    "multiple girls:1.60,\n2girls:1.60,\nmultiple boys:1.55,\n1boy:1.45,\n"
    "solo focus:1.50,\nmultiple views:1.60,\nzoom layer:1.60\n>"
)


def aplicar(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    p = Pose.objects.filter(name=NOMBRE).first()
    if p is not None:
        p.prompt = NUEVO
        p.save(update_fields=["prompt"])
    Pose.objects.filter(name=BORRAR).delete()


def revertir(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")
    p = Pose.objects.filter(name=NOMBRE).first()
    if p is not None:
        p.prompt = VIEJO
        p.save(update_fields=["prompt"])
    if not Pose.objects.filter(name=BORRAR).exists():
        Pose.objects.create(
            name=BORRAR,
            prompt=BORRADA,
            tier="tier2",
            img_type=ImageType.objects.filter(name="1:1").first(),
        )


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0037_poses_presenting"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
