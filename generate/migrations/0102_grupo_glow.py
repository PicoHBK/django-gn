from django.db import migrations


# Grupo Glow-.
#
# El problema del grupo: los tags especificos de prenda brillante casi no
# existen. glowing_shoes 0, glowing_shirt 0, glowing_pants 0, glowing_skirt 0,
# glowing_dress 44, glowing_footwear 28, glowing_clothes 463. Tampoco hay tag
# neutro de region: topwear y bottomwear son 0.
#
# Los unicos fuertes son glowing (139.227) y glowing_eyes (62.670). Asi que el
# brillo lo cargan esos dos mas dos refuerzos que si tienen volumen:
# light_particles (81.302) y neon_trim (5.008), que es justo el aspecto que
# tiene la ropa que brilla. La prenda se nombra al final con peso bajo (1.15)
# solo para apuntar donde va el brillo, sin pisar lo que haya puesto BD-.
#
# Glow-Shoes NO nombra ningun calzado: el calzado lo decide el grupo FT- y el
# brillo se aplica sobre lo que FT- haya puesto. Es el mas debil del grupo por
# eso mismo, no hay tag con volumen que diga "calzado que brilla".
#
# El [color] lo reemplaza process_special_colors con el color que manda el
# front, igual que en BD-. Si no llega ninguno quedan los corchetes pelados y
# el default es cyan.
TIER = "tier1"

BASE = "(glowing:{}),\n(neon trim:1.40),\n(light particles:1.25)"

NUEVOS = [
    ("Glow-Eyes", "([cyan] glowing eyes:1.70),\n(glowing:1.30)"),
    ("Glow-Hair", "([cyan] glowing hair:1.65),\n(glowing:1.40),\n(light particles:1.30)"),
    ("Glow-Dress", "([cyan] glowing dress:1.55),\n(glowing clothes:1.50),\n"
                   + BASE.format("1.40") + ",\n(dress:1.15)"),
    ("Glow-Top", "([cyan] glowing shirt:1.50),\n(glowing clothes:1.50),\n"
                 + BASE.format("1.40") + ",\n(shirt:1.15)"),
    ("Glow-Bottom", "([cyan] glowing pants:1.50),\n(glowing clothes:1.50),\n"
                    + BASE.format("1.40") + ",\n(pants:1.15)"),
    ("Glow-Skirt", "([cyan] glowing skirt:1.50),\n(glowing clothes:1.50),\n"
                   + BASE.format("1.40") + ",\n(skirt:1.15)"),
    # sin nombrar calzado: eso lo decide FT-
    ("Glow-Shoes", "([cyan] glowing footwear:1.60),\n(glowing:1.45),\n"
                   "(neon trim:1.40),\n(light particles:1.30)"),
    ("Glow-All", "(glowing:1.65),\n(glowing clothes:1.55),\n"
                 "([cyan] glowing eyes:1.45),\n(glowing hair:1.35),\n"
                 "(neon trim:1.45),\n(light particles:1.35)"),
]


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, prompt in NUEVOS:
        Special.objects.update_or_create(
            name=nombre, defaults={"prompt": prompt, "tier": TIER}
        )


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n for n, _ in NUEVOS]).delete()


class Migration(migrations.Migration):

    dependencies = [("generate", "0101_md_cfnm")]

    operations = [migrations.RunPython(aplicar, revertir)]
