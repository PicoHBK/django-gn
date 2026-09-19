from django.db import migrations


# Full Body dejaba la cabeza y los pies pegados al borde. Se arregla por los
# dos lados:
#
#   POSITIVO  (wide shot:1.35) tira la camara para atras. Es el tag real para
#             que el sujeto ocupe menos cuadro: 23.925 posts.
#   NEGATIVO  head out of frame (29.305), feet out of frame (240.557) y
#             cropped legs (72.237) son EXACTAMENTE el recorte que se veia.
#             feet out of frame con 240 mil posts es de los mas entrenados
#             que hay, asi que negarlo pesa.
#
# El <neg:> aca recien funciona por el cambio en views.py: hasta ahora el
# prompt del ImageType se appendeaba crudo, sin pasar por extract_neg_prompt,
# asi que un bloque negativo se habria ido literal al positivo. Lo mismo
# pasaba con el Emote.
#
# Tambien se le pone peso a "standing", que estaba pelado.
NOMBRE = "Full Body"

VIEJO = "lazypos,standing, (full body:1.5)"

NUEVO = (
    "lazypos,\n"
    "(full body:1.60),\n"
    "(standing:1.20),\n"
    "(wide shot:1.35),\n"
    "\n"
    "<neg:\n"
    "feet out of frame:1.60,\n"
    "head out of frame:1.60,\n"
    "cropped legs:1.50,\n"
    "close-up:1.45,\n"
    "portrait:1.40\n"
    ">"
)


def aplicar(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    i = ImageType.objects.filter(name=NOMBRE).first()
    if i is not None:
        i.prompt = NUEVO
        i.save(update_fields=["prompt"])


def revertir(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    i = ImageType.objects.filter(name=NOMBRE).first()
    if i is not None:
        i.prompt = VIEJO
        i.save(update_fields=["prompt"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0075_micro_thong"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
