from django.db import migrations


# ThiccSlider-Flat: el extremo opuesto del slider, que faltaba. Las tres
# variantes que habia iban de .6 a 2, todas del mismo lado; esta usa el LoRA
# en -2 para ir para el otro.
#
# Los tags que la acompañan son los que existen: flat chest (237.914),
# small breasts (720.410), skinny (11.561), narrow waist (16.301), narrow
# hips (921), flat ass (3.860) y slim legs (1.278). No se usan slender, thin,
# lithe, visible ribs ni small ass: 0 posts los cinco.
#
# NO lleva "petite" ni ningun tag de edad a proposito. Es un slider de
# contextura, no de edad; para eso esta la familia GaSlider.
#
# De paso, ThiccSlider-Low estaba en tier1 y sus dos hermanos en tier5. Era
# el unico de los 27 sliders fuera de tier5.
NUEVOS = [('ThiccSlider-Flat', '<lora:thicc_v1.2-illu_done:-2>,\n(skinny:1.50),\n(flat chest:1.45),\n(small breasts:1.35),\n(narrow waist:1.40),\n(narrow hips:1.30),\n(flat ass:1.25),\n(slim legs:1.25),\n(collarbone:1.20)')]

TIER = [['ThiccSlider-Low', 'tier5', 'tier1']]


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, prompt in NUEVOS:
        if Special.objects.filter(name=nombre).exists():
            continue
        Special.objects.create(name=nombre, tier="tier5", prompt=prompt)
    for nombre, nuevo, _viejo in TIER:
        s = Special.objects.filter(name=nombre).first()
        if s is not None:
            s.tier = nuevo
            s.save(update_fields=["tier"])


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()
    for nombre, _nuevo, viejo in TIER:
        s = Special.objects.filter(name=nombre).first()
        if s is not None:
            s.tier = viejo
            s.save(update_fields=["tier"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0065_emotes_milf"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
