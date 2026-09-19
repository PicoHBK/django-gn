from django.db import migrations


# El grupo FT- tenia un problema de fondo: FT-Plat, FT-Plat Pum y FT-Sandals
# son EL MISMO TACO tres veces. Los tres piden platform, stiletto y needle
# heels; lo unico que cambia es el color y el orden. No eran tres opciones,
# era una.
#
# Se suman 14 tipos realmente distintos, por volumen real:
#   sandals 152.716   thigh boots 124.228   sneakers 97.160   loafers 85.107
#   knee boots 84.515 mary janes 57.204     ankle boots 25.193
#   tabi 25.274       geta 23.405           slippers 23.348   uwabaki 10.393
#   okobo 8.068       roller skates 4.637   combat/cowboy boots ~2.200
#
# Arreglos:
#   - FT-Plat, FT-Plat Pum y FT-Sandals arrancaban con un backtick suelto,
#     el mismo bug de BD-COS/Tsunade y GaSlider-Med.
#   - FT-Slides usaba "thong_sandals", que no existe en Danbooru: 0 posts.
#     Pasa a flip-flops (8.369), que ya tenia al lado.
#   - FT-Barefoot estaba en tier2 y los otros cinco en tier1.
#
# Descartados por inexistentes: zori, rain boots, school shoes, athletic
# shoes, pointe shoes, espadrilles, knee high boots y toeless footwear.
# kitten heels existe pero con 90 posts.
#
# Un codigo de color en cada uno.
ARREGLOS = [['FT-Plat', '`([white] platform heels:1.45), (stiletto heels:1.3), (platforms heels:1.55), (very high heels:1.25), (arched feet:1.15)', '([white] platform heels:1.45), (stiletto heels:1.3), (platforms heels:1.55), (very high heels:1.25), (arched feet:1.15)'], ['FT-Plat Pum', '`([white] platform_pumps:1.45), (stiletto_heels:1.3), (needle_heels:1.25), (very_high_heels:1.25), (arched_feet:1.15), <neg:(pumps:1.2),(sandals:1.3),(flat_shoes:1.3),(multiple_straps:1.4),(ankle_straps:1.3),(bows:1.3),(ribbons:1.3),(ornaments:1.3),(latex:1.3)>`', '([white] platform_pumps:1.45), (stiletto_heels:1.3), (needle_heels:1.25), (very_high_heels:1.25), (arched_feet:1.15), <neg:(pumps:1.2),(sandals:1.3),(flat_shoes:1.3),(multiple_straps:1.4),(ankle_straps:1.3),(bows:1.3),(ribbons:1.3),(ornaments:1.3),(latex:1.3)>'], ['FT-Sandals', '`([black] high_heel_sandals:1.4), (stiletto_heels:1.3), (needle_heels:1.25), (very_high_heels:1.25), (arched_feet:1.15), (open_toe:1.3), (visible_toes:1.2), (lace-up_sandals:1.25), (long_straps:1.2), (leg_straps:1.2), (knee-high_straps:1.2), (knee-high_sandals:1.2), <neg:(platform_pumps:1.3),(pumps:1.3),(closed_toe:1.3),(boots:1.3),(thick_sole:1.3),(latex:1.3)>`', '([black] high_heel_sandals:1.4), (stiletto_heels:1.3), (needle_heels:1.25), (very_high_heels:1.25), (arched_feet:1.15), (open_toe:1.3), (visible_toes:1.2), (lace-up_sandals:1.25), (long_straps:1.2), (leg_straps:1.2), (knee-high_straps:1.2), (knee-high_sandals:1.2), <neg:(platform_pumps:1.3),(pumps:1.3),(closed_toe:1.3),(boots:1.3),(thick_sole:1.3),(latex:1.3)>'], ['FT-Slides', 'thong sandals,flip-flops', '([black] flip-flops:1.55),\n(sandals:1.35),\n(toeless footwear:1.20)']]

TIER = [['FT-Barefoot', 'tier1', 'tier2']]

NUEVOS = [['FT-Thigh Boots', '([black] thigh boots:1.60),\n(boots:1.35),\n(thighhighs:1.20)'], ['FT-Knee Boots', '([brown] knee boots:1.60),\n(boots:1.35),\n(zipper:1.15)'], ['FT-Ankle Boots', '([black] ankle boots:1.60),\n(boots:1.35),\n(heel:1.20)'], ['FT-Combat Boots', '([black] combat boots:1.60),\n(boots:1.40),\n(cross-laced:1.25),\n(lace-up boots:1.25)'], ['FT-Cowboy Boots', '([brown] cowboy boots:1.60),\n(boots:1.35),\n(western:1.20)'], ['FT-Sneakers', '([white] sneakers:1.60),\n(shoes:1.30),\n(socks:1.20)'], ['FT-Loafers', '([brown] loafers:1.60),\n(shoes:1.30),\n(socks:1.20)'], ['FT-Mary Janes', '([black] mary janes:1.60),\n(shoes:1.30),\n(ankle strap:1.25)'], ['FT-Sandals Flat', '([tan] sandals:1.60),\n(flat sandals:1.30),\n(open-toe shoes:1.25)'], ['FT-Slippers', '([pink] slippers:1.60),\n(indoors:1.20)'], ['FT-Geta', '([black] geta:1.60),\n(japanese clothes:1.25),\n(tabi:1.30)'], ['FT-Okobo', '([red] okobo:1.60),\n(geta:1.35),\n(japanese clothes:1.25)'], ['FT-Uwabaki', '([white] uwabaki:1.60),\n(school:1.25),\n(socks:1.20)'], ['FT-Skates', '([white] roller skates:1.60),\n(skates:1.30),\n(socks:1.20)']]


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, _viejo, nuevo in ARREGLOS:
        s = Special.objects.filter(name=nombre).first()
        if s is not None:
            s.prompt = nuevo
            s.save(update_fields=["prompt"])
    for nombre, nuevo, _viejo in TIER:
        s = Special.objects.filter(name=nombre).first()
        if s is not None:
            s.tier = nuevo
            s.save(update_fields=["tier"])
    for nombre, prompt in NUEVOS:
        if Special.objects.filter(name=nombre).exists():
            continue
        Special.objects.create(name=nombre, tier="tier1", prompt=prompt)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()
    for nombre, viejo, _nuevo in ARREGLOS:
        s = Special.objects.filter(name=nombre).first()
        if s is not None:
            s.prompt = viejo
            s.save(update_fields=["prompt"])
    for nombre, _nuevo, viejo in TIER:
        s = Special.objects.filter(name=nombre).first()
        if s is not None:
            s.tier = viejo
            s.save(update_fields=["tier"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0070_poses_propos"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
