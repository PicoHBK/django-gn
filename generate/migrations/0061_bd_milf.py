from django.db import migrations


# BD-Milf/: los outfits tipicos del doujin, elegidos por volumen real:
#
#   turtleneck sweater 58.792   pencil skirt 55.433   blouse 50.250
#   ribbed sweater     48.434   sleeveless turtleneck 23.189
#   sundress           21.941   off-shoulder sweater  19.816
#   sweater dress      12.808   yoga pants  7.192     virgin killer 6.130
#   jersey              4.153   kappougi    3.015
#
# Solo ROPA, como pediste: ninguno lleva mature_female, milf, curvy ni nada
# de cuerpo. Eso se decide en el personaje, no en el vestuario. Verificado.
#
# Cuatro descartados por volumen: housewife (864), knit sweater (387),
# meat dress (5) y tracksuit, que directamente no existe en Danbooru. El
# equivalente real de tracksuit es jersey.
#
# Dos codigos de color en cada uno, y ninguno lleva calzado.
NUEVOS = [('BD-Milf/Ribbed', '([cream] ribbed sweater:1.55),\n(sweater:1.35),\n(skin tight:1.35),\n([black] pencil skirt:1.40)'), ('BD-Milf/Turtleneck', '([black] turtleneck sweater:1.55),\n(turtleneck:1.40),\n(skin tight:1.35),\n([grey] pencil skirt:1.40)'), ('BD-Milf/Sleeveless', '([white] sleeveless turtleneck:1.55),\n(turtleneck:1.35),\n(bare shoulders:1.30),\n([navy] pencil skirt:1.40)'), ('BD-Milf/Virgin Killer', '([white] virgin killer sweater:1.60),\n(backless outfit:1.40),\n(bare back:1.35),\n(meme attire:1.25)'), ('BD-Milf/Sweater Dress', '([beige] sweater dress:1.55),\n(long sleeves:1.30),\n([black] pantyhose:1.40)'), ('BD-Milf/Off Shoulder', '([pink] off-shoulder sweater:1.55),\n(bare shoulders:1.35),\n(collarbone:1.25),\n([white] pantyhose:1.35)'), ('BD-Milf/Kappougi', '([white] kappougi:1.55),\n(japanese clothes:1.35),\n(apron:1.35),\n([blue] kimono:1.30)'), ('BD-Milf/Blouse', '([white] blouse:1.55),\n(collared shirt:1.35),\n([black] pencil skirt:1.45),\n(pantyhose:1.35)'), ('BD-Milf/Sundress', '([yellow] sundress:1.55),\n(sleeveless dress:1.35),\n(bare shoulders:1.30),\n([white] cardigan:1.30)'), ('BD-Milf/Tight Dress', '([red] tight dress:1.55),\n(skin tight:1.40),\n(short dress:1.30),\n([black] pantyhose:1.40)'), ('BD-Milf/Jersey', '([navy] jersey:1.55),\n(track jacket:1.35),\n([navy] yoga pants:1.45),\n(skin tight:1.30)')]


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, prompt in NUEVOS:
        if Special.objects.filter(name=nombre).exists():
            continue
        Special.objects.create(name=nombre, tier="tier3", prompt=prompt)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0060_bd_films"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
