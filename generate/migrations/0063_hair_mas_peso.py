from django.db import migrations


# Los specials de pelo suben de peso, y Hair-Bun ademas tenia dos tags
# MUERTOS que eran justo los que debian recoger el pelo:
#
#   "slicked back hair"  0 posts en Danbooru, estaba en el positivo
#   "loose hair"         0 posts, estaba en el negativo
#
# Por eso el rodete salia desarmado y el pelo del personaje seguia como venia:
# el special no estaba pidiendo ni negando nada.
#
# Lo que si recoge el pelo, con su volumen:
#   hair pulled back 11.738   updo 10.806   hair up 16.532   hair tie 33.700
#
# Y lo que hay que NEGAR para que no queden mechones sueltos, que es la parte
# que faltaba del todo:
#   sidelocks 942.850   floating hair 194.878   hair flaps 56.811
#   messy hair 92.284   hair down 44.195
#
# sidelocks con 942.850 posts es el mas importante de los cinco: son los
# mechones a los costados de la cara, y si no se niegan aparecen siempre.
#
# Los dominantes pasan de 1.70 a 1.85, y a 1.90 en Hair-Bun y Hair-Ponytail,
# que son los dos que tienen que ganarle al pelo que trae el personaje.
CAMBIOS = [['Hair-Bun', '<(hair bun:1.70)>,\n<(single hair bun:1.60)>,\n(hair pulled back:1.50),\n(slicked back hair:1.40),\n(hair up:1.35),\n(forehead:1.30),\n(long hair:1.50),\n\n<neg:\nhair down:1.50,\nloose hair:1.50,\ndouble bun:1.45,\ntwintails:1.50,\nponytail:1.45,\nbangs:1.45,\nsidelocks:1.40,\nhair over one eye:1.40,\nmessy hair:1.40,\nhair between eyes:1.30,\nshort hair:1.45,\nmedium hair:1.30,\nvery long hair:1.30,\nabsurdly long hair:1.50\n>', '<(hair bun:1.90)>,\n<(single hair bun:1.80)>,\n(hair pulled back:1.70),\n(updo:1.60),\n(hair up:1.55),\n(hair tie:1.30),\n(forehead:1.35),\n(long hair:1.50),\n\n<neg:\nsidelocks:1.60,\nhair flaps:1.60,\nfloating hair:1.55,\nmessy hair:1.70,\nhair down:1.70,\ndouble bun:1.50,\ntwintails:1.55,\nponytail:1.50,\nbangs:1.50,\nhair over one eye:1.45,\nhair between eyes:1.40,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55\n>'], ['Hair-Ponytail', '<(high ponytail:1.70)>,\n(hair tie:1.20),\n(long hair:1.50),\n\n<neg:\nlow ponytail:1.50,\nside ponytail:1.50,\nshort ponytail:1.50,\nfolded ponytail:1.40,\ntwintails:1.50,\nhair bun:1.40,\nhair down:1.45,\nshort hair:1.45,\nvery long hair:1.30,\nabsurdly long hair:1.50\n>', '<(high ponytail:1.90)>,\n(hair pulled back:1.65),\n(hair tie:1.35),\n(long hair:1.50),\n\n<neg:\nsidelocks:1.60,\nhair flaps:1.60,\nfloating hair:1.55,\nmessy hair:1.70,\nhair down:1.70,\nlow ponytail:1.55,\nside ponytail:1.55,\nshort ponytail:1.50,\nfolded ponytail:1.40,\ntwintails:1.55,\nhair bun:1.45,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55\n>'], ['Hair-Blunt', '<(blunt bangs:1.70)>,\n(straight bangs:1.45),\n(even bangs:1.40),\n(thick bangs:1.25),\n(long hair:1.50),\n\n<neg:\nside-swept bangs:1.50,\nswept bangs:1.50,\nasymmetrical bangs:1.50,\nparted bangs:1.50,\nshort hair:1.45,\nmedium hair:1.30,\nvery long hair:1.30,\nabsurdly long hair:1.50\n>', '<(blunt bangs:1.85)>,\n(straight bangs:1.60),\n(even bangs:1.50),\n(thick bangs:1.40),\n(long hair:1.50),\n\n<neg:\nside-swept bangs:1.60,\nswept bangs:1.60,\nasymmetrical bangs:1.55,\nparted bangs:1.55,\nmessy hair:1.50,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55\n>'], ['Hair-One Eye', '<(hair over one eye:1.70)>,\n(one eye covered:1.60),\n(long hair:1.50),\n\n<neg:\ncovering one eye:1.70,\nhand on own face:1.60,\ncovering face:1.55,\nhand over eye:1.60,\neyepatch:1.55,\nhair over eyes:1.50,\nhair between eyes:1.40,\ncenter part:1.40,\nside part:1.30,\nhair behind ears:1.30,\nshort hair:1.45,\nmedium hair:1.30,\nvery long hair:1.30,\nabsurdly long hair:1.50\n>', '<(hair over one eye:1.85)>,\n(one eye covered:1.70),\n(long hair:1.50),\n\n<neg:\ncovering one eye:1.70,\nhand on own face:1.60,\nhand over eye:1.60,\ncovering face:1.55,\neyepatch:1.55,\nhair over eyes:1.50,\nhair between eyes:1.45,\ncenter part:1.40,\nside part:1.35,\nhair behind ears:1.40,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55\n>'], ['Hair-Tsunade', '<(curtained hair:1.70)>,\n<(parted bangs:1.55)>,\n(center part:1.40),\n(hair framing face:1.35),\n(long hair:1.50),\n\n<neg:\nblunt bangs:1.50,\nstraight bangs:1.45,\nhair intakes:1.45,\nswept bangs:1.40,\nasymmetrical bangs:1.40,\nhair over one eye:1.40,\nshort hair:1.45,\nmedium hair:1.30,\nvery long hair:1.30,\nabsurdly long hair:1.50\n>', '<(curtained hair:1.85)>,\n<(parted bangs:1.70)>,\n(center part:1.50),\n(hair framing face:1.45),\n(long hair:1.50),\n\n<neg:\nblunt bangs:1.60,\nstraight bangs:1.55,\nhair intakes:1.55,\nswept bangs:1.50,\nasymmetrical bangs:1.50,\nhair over one eye:1.45,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55\n>']]


def _set(apps, indice):
    Special = apps.get_model("generate", "Special")
    for c in CAMBIOS:
        s = Special.objects.filter(name=c[0]).first()
        if s is not None:
            s.prompt = c[indice]
            s.save(update_fields=["prompt"])


def aplicar(apps, schema_editor):
    _set(apps, 2)


def revertir(apps, schema_editor):
    _set(apps, 1)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0062_films_reveladoras"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
