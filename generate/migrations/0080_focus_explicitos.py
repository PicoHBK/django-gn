from django.db import migrations


# Los focus explicitos que faltaban. No entraron con los otros 12 porque
# esos quedaron en tier2 y estos no van ahi.
#
# De la familia *_focus solo existen tres explicitos: pussy_focus (1.154),
# crotch_focus (1.990) y penis_focus (974). NO existen, con 0 posts:
# anus_focus, penetration_focus, sex_focus, nipple_focus, clitoris_focus,
# vaginal_focus ni pubic_hair_focus.
#
# Por eso Focus-Anus se arma con anus (169.161) + crotch focus, y la
# penetracion con vaginal (289.821) o anal (74.944), porque "penetration" a
# secas tampoco existe.
#
# Tier segun el criterio de siempre: anatomia explicita sin penetracion va a
# tier4, penetracion a tier5.
#
# Sin bloque negativo, igual que los otros doce del grupo.
NUEVOS = [('Focus-Pussy', '(pussy focus:1.50),\n(pussy:1.40),\n(clitoris:1.25),\n(spread legs:1.20)', 'tier4'), ('Focus-Crotch', '(crotch focus:1.50),\n(spread legs:1.30),\n(pussy:1.25)', 'tier4'), ('Focus-Anus', '(anus:1.50),\n(crotch focus:1.35),\n(ass focus:1.30),\n(spread ass:1.20)', 'tier4'), ('Focus-Penetration', '(vaginal:1.55),\n(pussy:1.40),\n(penis:1.35),\n(crotch focus:1.30),\n(cross-section:1.20)', 'tier5'), ('Focus-Anal', '(anal:1.55),\n(anus:1.40),\n(penis:1.35),\n(ass focus:1.30)', 'tier5')]


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, prompt, tier in NUEVOS:
        if Special.objects.filter(name=nombre).exists():
            continue
        Special.objects.create(name=nombre, tier=tier, prompt=prompt)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0079_focus_specials"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
