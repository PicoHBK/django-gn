from django.db import migrations


# Se saca (shiny skin:1.20) del positivo de los seis ImageTypes y se niega.
#
# La piel glossy venia de ahi: "shiny_skin" (158.027) es el UNICO tag real de
# ese efecto. Todo lo que uno esperaria que existiera no existe, 0 posts:
# oiled_body, oil, glossy, glistening, wet_skin, body_oil, reflective_skin,
# plastic, latex_skin, smooth_skin y skin_texture.
#
# Por eso no alcanzaba con negarlo: quedaba pedido en el positivo y negado en
# el negativo al mismo tiempo, y eso se anula. Hay que sacarlo de un lado.
#
# Al negativo van ademas los otros cuatro que empujan a piel de plastico:
# shiny (4.816), glowing skin (373), 3d (29.970), realistic (32.745) y
# photorealistic (1.799). Los tres ultimos son los que sacan al modelo del
# registro anime, que es donde ese brillo se ve peor.
CAMBIOS = [['Full Body', 'lazypos,\n(full body:1.60),\n(standing:1.20),\n(wide shot:1.35),\n(shiny skin:1.20),\n\n<neg:\nfeet out of frame:1.60,\nhead out of frame:1.60,\ncropped legs:1.50,\nclose-up:1.45,\nportrait:1.40,\nmuscular female:1.30,\nmuscular:1.20\n>', 'lazypos,\n(full body:1.60),\n(standing:1.20),\n(wide shot:1.35),\n\n<neg:\nfeet out of frame:1.60,\nhead out of frame:1.60,\ncropped legs:1.50,\nclose-up:1.45,\nportrait:1.40,\nmuscular female:1.30,\nmuscular:1.20,\nshiny skin:1.35,\nshiny:1.25,\nglowing skin:1.25,\n3d:1.30,\nrealistic:1.25,\nphotorealistic:1.30\n>'], ['3:4', 'lazypos,\n(shiny skin:1.20),\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>', 'lazypos,\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20,\nshiny skin:1.35,\nshiny:1.25,\nglowing skin:1.25,\n3d:1.30,\nrealistic:1.25,\nphotorealistic:1.30\n>'], ['Cowboy Shot', '(cowboy shot:1.6),lazypos,\n(shiny skin:1.20),\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>', '(cowboy shot:1.6),lazypos,\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20,\nshiny skin:1.35,\nshiny:1.25,\nglowing skin:1.25,\n3d:1.30,\nrealistic:1.25,\nphotorealistic:1.30\n>'], ['1:1', 'lazypos,\n(shiny skin:1.20),\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>', 'lazypos,\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20,\nshiny skin:1.35,\nshiny:1.25,\nglowing skin:1.25,\n3d:1.30,\nrealistic:1.25,\nphotorealistic:1.30\n>'], ['4:3', 'lazypos,\n(shiny skin:1.20),\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>', 'lazypos,\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20,\nshiny skin:1.35,\nshiny:1.25,\nglowing skin:1.25,\n3d:1.30,\nrealistic:1.25,\nphotorealistic:1.30\n>'], ['Portrait', 'lazypos,(portrait:1.6),(close-up:1.2),\n(shiny skin:1.20),\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>', 'lazypos,(portrait:1.6),(close-up:1.2),\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20,\nshiny skin:1.35,\nshiny:1.25,\nglowing skin:1.25,\n3d:1.30,\nrealistic:1.25,\nphotorealistic:1.30\n>']]


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
        ("generate", "0091_shiny_skin"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
