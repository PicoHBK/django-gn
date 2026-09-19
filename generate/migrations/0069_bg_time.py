from django.db import migrations


# BG-Time/: la hora del dia sale de BG-Amb/, que queda solo para clima y
# efectos. Antes estaban mezclados: "Rain" y "Sunset" no son lo mismo, y
# tiene sentido poder combinar uno de cada grupo.
#
# Se mudan Day, Night, Sunset y Sunrise, y se suman cinco que faltaban:
# Morning (4.475), Evening (13.466), Dusk (6.115), Twilight (9.004) y
# Dawn (1.779).
#
# Cinco horas que parecen obvias NO existen en Danbooru: noon, afternoon,
# midnight, daytime y nighttime, todas en 0. Y golden_hour tiene 384 posts,
# inservible; el equivalente real es twilight o evening.
#
# BG-Amb/ queda con 13: Rain, Snow, Sky, Fog, Wind, Storm, Moonlight, Stars,
# Fireworks, Sakura, Autumn, Particles y Sunbeam.
MOVER = {'BG-Amb/Day': 'BG-Time/Day', 'BG-Amb/Night': 'BG-Time/Night', 'BG-Amb/Sunset': 'BG-Time/Sunset', 'BG-Amb/Sunrise': 'BG-Time/Sunrise'}

NUEVOS = [('BG-Time/Morning', '(morning:1.50),\n(outdoors:1.35),\n(sunlight:1.40),\n(blue sky:1.30),\n(sunbeam:1.25)'), ('BG-Time/Evening', '(evening:1.50),\n(outdoors:1.35),\n(orange sky:1.40),\n(gradient sky:1.30),\n(cloudy sky:1.20)'), ('BG-Time/Dusk', '(dusk:1.50),\n(twilight:1.40),\n(outdoors:1.35),\n(gradient sky:1.35),\n(darkness:1.20)'), ('BG-Time/Twilight', '(twilight:1.55),\n(outdoors:1.35),\n(gradient sky:1.40),\n(orange sky:1.30),\n(cloud:1.20)'), ('BG-Time/Dawn', '(dawn:1.50),\n(sunrise:1.40),\n(outdoors:1.35),\n(gradient sky:1.30),\n(sunbeam:1.25)')]


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for viejo, nuevo in MOVER.items():
        s = Special.objects.filter(name=viejo).first()
        if s is not None:
            s.name = nuevo
            s.save(update_fields=["name"])
    for nombre, prompt in NUEVOS:
        if Special.objects.filter(name=nombre).exists():
            continue
        Special.objects.create(name=nombre, tier="tier4", prompt=prompt)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()
    for viejo, nuevo in MOVER.items():
        s = Special.objects.filter(name=nuevo).first()
        if s is not None:
            s.name = viejo
            s.save(update_fields=["name"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0068_bg_ambiente_y_lugares"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
