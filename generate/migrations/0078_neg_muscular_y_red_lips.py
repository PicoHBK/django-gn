from django.db import migrations


# Dos cosas.
#
# 1. Los seis ImageTypes niegan el cuerpo musculoso. Ojo: "muscular_woman"
#    NO existe en Danbooru, 0 posts. El real es "muscular_female" (38.443),
#    que va en 1.30 como pediste, mas "muscular" (198.683) en 1.20, que es el
#    generico y es el que mas aparece.
#
#    Cinco de los seis no tenian bloque <neg:> y se les crea; Full Body ya
#    tenia el de recorte y se le agrega al final. Esto recien funciona por el
#    cambio de la 0076 en views.py, que hizo que el ImageType pase por
#    extract_neg_prompt.
#
# 2. FC-Red Lips vuelve a su idea original: todo negro salvo los labios, y el
#    codigo de color queda solo ahi. Se usan los tags que existen:
#    black_eyeliner (2.479) y black_eyeshadow (2.934) si existen, pero
#    "beauty_mark" NO -0 posts-, asi que la marca es mole_under_eye
#    (251.034), que ademas es oscura por definicion.
#
#    Se saca "red lips" suelto y "lipstick": con [red] lips alcanza, y los
#    otros dos empujaban color fuera de los labios.
IMAGETYPES = [['Full Body', 'lazypos,\n(full body:1.60),\n(standing:1.20),\n(wide shot:1.35),\n\n<neg:\nfeet out of frame:1.60,\nhead out of frame:1.60,\ncropped legs:1.50,\nclose-up:1.45,\nportrait:1.40\n>', 'lazypos,\n(full body:1.60),\n(standing:1.20),\n(wide shot:1.35),\n\n<neg:\nfeet out of frame:1.60,\nhead out of frame:1.60,\ncropped legs:1.50,\nclose-up:1.45,\nportrait:1.40,\nmuscular female:1.30,\nmuscular:1.20\n>'], ['3:4', 'lazypos', 'lazypos,\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>'], ['Cowboy Shot', '(cowboy shot:1.6),lazypos', '(cowboy shot:1.6),lazypos,\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>'], ['1:1', 'lazypos', 'lazypos,\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>'], ['4:3', 'lazypos', 'lazypos,\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>'], ['Portrait', 'lazypos,(portrait:1.6),(close-up:1.2)', 'lazypos,(portrait:1.6),(close-up:1.2),\n\n<neg:\nmuscular female:1.30,\nmuscular:1.20\n>']]

RED_LIPS_VIEJO = '([red] lips:1.45),\n(red lips:1.40),\n(lipstick:1.35),\n(eyeliner:1.35),\n(eyeshadow:1.30),\n(eyelashes:1.25),\n(mole under eye:1.20)'

RED_LIPS_NUEVO = '([red] lips:1.45),\n(black eyeliner:1.40),\n(black eyeshadow:1.35),\n(eyeshadow:1.25),\n(eyelashes:1.25),\n(mole under eye:1.30)'


def aplicar(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Special = apps.get_model("generate", "Special")
    for nombre, _viejo, nuevo in IMAGETYPES:
        i = ImageType.objects.filter(name=nombre).first()
        if i is not None:
            i.prompt = nuevo
            i.save(update_fields=["prompt"])
    s = Special.objects.filter(name="FC-Red Lips").first()
    if s is not None:
        s.prompt = RED_LIPS_NUEVO
        s.save(update_fields=["prompt"])


def revertir(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Special = apps.get_model("generate", "Special")
    for nombre, viejo, _nuevo in IMAGETYPES:
        i = ImageType.objects.filter(name=nombre).first()
        if i is not None:
            i.prompt = viejo
            i.save(update_fields=["prompt"])
    s = Special.objects.filter(name="FC-Red Lips").first()
    if s is not None:
        s.prompt = RED_LIPS_VIEJO
        s.save(update_fields=["prompt"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0077_imagetype_buckets"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
