from django.db import migrations


# Tres specials de pelo se estaban borrando tags a si mismos: sus propios
# tags_deleted incluian la palabra de un tag de su positivo.
#
#   Hair-Bun          (updo:1.60)          y borraba "updo"
#   Hair-Twin Braids  (braid:1.50) y
#                     (low twintails:1.35) y borraba "braid" y "twintails"
#   Hair-Drills       (twin drills:1.60)   y borraba "drills"
#
# El de Hair-Bun venia de la 0063 y llevaba varias migraciones asi: el tag
# que mas ayudaba a recoger el pelo se borraba solo.
#
# Se arregla envolviendolos en <>, que es lo que ya hacen los tags
# principales de todos los specials de pelo.
FIX = {'Hair-Bun': [['(updo:1.60)', '<(updo:1.60)>']], 'Hair-Twin Braids': [['(braid:1.50)', '<(braid:1.50)>'], ['(low twintails:1.35)', '<(low twintails:1.35)>']], 'Hair-Drills': [['(twin drills:1.60)', '<(twin drills:1.60)>']]}


def _set(apps, invertir):
    Special = apps.get_model("generate", "Special")
    for nombre, cambios in FIX.items():
        s = Special.objects.filter(name=nombre).first()
        if s is None:
            continue
        p = s.prompt
        for viejo, nuevo in cambios:
            desde, hasta = (nuevo, viejo) if invertir else (viejo, nuevo)
            p = p.replace(desde, hasta)
        s.prompt = p
        s.save(update_fields=["prompt"])


def aplicar(apps, schema_editor):
    _set(apps, False)


def revertir(apps, schema_editor):
    _set(apps, True)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0087_hair_variantes"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
