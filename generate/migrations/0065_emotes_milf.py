from django.db import migrations


# Grupo Milf- de emotes: la version madura de cada emocion.
#
# Lo que las separa de las del grupo general no es la emocion sino el
# REGISTRO. Las de Smile-, Cry- o Mad- son expresiones abiertas; estas son
# contenidas, y eso se logra con tres tags:
#
#   half-closed eyes 144.945   la mirada relajada, esta en 6 de las 10
#   narrowed eyes     10.809   el enojo sin gritar
#   looking down     139.799   mirar desde arriba
#
# Milf-Angry es justo eso: annoyed + narrowed eyes + raised eyebrow en vez
# del angry + clenched teeth que usa Mad-Angry.
#
# Cuatro tags que parecian obvios NO existen en Danbooru: gentle_smile,
# wry_smile, condescending y tired, los cuatro en 0. Para la calida se usa
# motherly (1.576), que si existe, y para el cansancio sigh (4.560).
#
# Sin maquillaje a proposito: lipstick y eyeshadow marcarian el registro
# adulto pero no son emocion, y pisarian la skin del personaje.
NUEVOS = [['Milf-Worried', '(worried:1.50),(light blush:1.40),(half-closed eyes:1.30),(frown:1.20)'], ['Milf-Angry', '(annoyed:1.50),(narrowed eyes:1.45),(raised eyebrow:1.35),(frown:1.30),(half-closed eyes:1.25)'], ['Milf-Smug', '(smug:1.55),(half-closed eyes:1.40),(looking down:1.35),(closed mouth:1.20)'], ['Milf-Gentle', '(motherly:1.50),(smile:1.35),(closed eyes:1.30),(head tilt:1.20)'], ['Milf-Seductive', '(seductive smile:1.50),(half-closed eyes:1.45),(parted lips:1.30),(looking at viewer:1.25)'], ['Milf-Tired', '(sigh:1.50),(half-closed eyes:1.45),(looking down:1.30),(parted lips:1.20)'], ['Milf-Scolding', '(serious:1.50),(frown:1.40),(raised eyebrow:1.35),(narrowed eyes:1.30)'], ['Milf-Flustered', '(light blush:1.50),(averting eyes:1.40),(parted lips:1.30),(half-closed eyes:1.20)'], ['Milf-Disappointed', '(disappointed:1.50),(sad smile:1.40),(looking down:1.35),(closed eyes:1.20)'], ['Milf-Teasing', '(smug:1.50),(head tilt:1.35),(hand on own cheek:1.30),(half-closed eyes:1.35)']]


def aplicar(apps, schema_editor):
    Emote = apps.get_model("generate", "Emote")
    for nombre, prompt in NUEVOS:
        if Emote.objects.filter(name=nombre).exists():
            continue
        Emote.objects.create(name=nombre, prompt=prompt)


def revertir(apps, schema_editor):
    Emote = apps.get_model("generate", "Emote")
    Emote.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0064_age_slider_tags_reales"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
