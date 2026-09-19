from django.db import migrations


# Piel brillante en los seis ImageTypes. El tag es shiny_skin (158.009), que
# es el real: "glossy skin" y "smooth skin" no existen en Danbooru.
#
# Va en 1.20 y como ultimo tag del positivo, antes del bloque <neg:>, asi no
# le compite al encuadre de cada tipo.
CAMBIOS = [['Full Body', 'lazypos,\n(full body:1.60),\n(standing:1.20),\n(wide shot:1.35),\n\n<neg:\nfeet out of frame:1.60,\nhead out of frame:1.60,\ncropped legs:1.50,\nclose-up:1.45,\nportrait:1.40,\nmuscular female:1.30,\nmuscular:1.20\n>', 'lazypos,\n(full body:1.60),\n(standing:1.20),\n(wide shot:1.35),\n(shiny skin:1.20),\n\n<neg:\nfeet out of frame:1.60,\nhead out of frame:1.60,\ncropped legs:1.50,\nclose-up:1.45,\nportrait:1.40,\nmuscular female:1.30,\nmuscular:1.20\n>'], ['3:4', 'lazypos,\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>', 'lazypos,\n(shiny skin:1.20),\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>'], ['Cowboy Shot', '(cowboy shot:1.6),lazypos,\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>', '(cowboy shot:1.6),lazypos,\n(shiny skin:1.20),\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>'], ['1:1', 'lazypos,\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>', 'lazypos,\n(shiny skin:1.20),\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>'], ['4:3', 'lazypos,\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>', 'lazypos,\n(shiny skin:1.20),\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>'], ['Portrait', 'lazypos,(portrait:1.6),(close-up:1.2),\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>', 'lazypos,(portrait:1.6),(close-up:1.2),\n(shiny skin:1.20),\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>']]


def _set(apps, indice):
    ImageType = apps.get_model("generate", "ImageType")
    for c in CAMBIOS:
        i = ImageType.objects.filter(name=c[0]).first()
        if i is not None:
            i.prompt = c[indice]
            i.save(update_fields=["prompt"])


def aplicar(apps, schema_editor):
    _set(apps, 2)


def revertir(apps, schema_editor):
    _set(apps, 1)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0090_immi_close"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
