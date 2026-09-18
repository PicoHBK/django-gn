from django.db import migrations


# "Smile" vuelve a llamarse asi, sin grupo. Es el que el front manda por
# defecto, y al renombrarlo a Smile-Gen en la 0055 le rompi esa llamada:
# views.py busca los emotes por nombre con filter(name=...).first(), asi que
# un nombre que no existe devuelve None y el emote no se aplica.
#
# Es la excepcion a la regla del guion: los otros 56 van agrupados, este no.


def aplicar(apps, schema_editor):
    Emote = apps.get_model("generate", "Emote")
    e = Emote.objects.filter(name="Smile-Gen").first()
    if e is not None:
        e.name = "Smile"
        e.save(update_fields=["name"])


def revertir(apps, schema_editor):
    Emote = apps.get_model("generate", "Emote")
    e = Emote.objects.filter(name="Smile").first()
    if e is not None:
        e.name = "Smile-Gen"
        e.save(update_fields=["name"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0056_bd_subgrupos"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
