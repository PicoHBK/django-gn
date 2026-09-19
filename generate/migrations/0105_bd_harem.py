from django.db import migrations


# Subgrupo BD-Harem: estilo arabe, bailarina de harem y egipcio, en la linea
# de "mujer de compania". Explicito, y todo thong es micro thong como el resto
# de BD.
#
# Lo que NO existe y por eso no aparece: belly_dancer 0, egyptian_clothes 0,
# topless 0 (el canonico es topless_female, 89.023), egyptian 8, scarab 178,
# nemes 231, pharaoh 159 y genie 671: demasiado raros para que el modelo los
# haya aprendido.
#
# see-through y sheer_clothes son ALIAS de see-through_clothes (220.540), asi
# que va el canonico. Ojo que BD-Seduct/Babydoll y /Bodystocking todavia usan
# el alias.
#
# El egipcio de verdad lo carga usekh_collar (3.380), que es el collar ancho,
# no los tags con "egyptian" adentro.
#
# Sin calzado: eso lo decide FT-.
TIER = "tier3"

NEG = ("<neg:\ndress:1.50,\nlong skirt:1.45,\nbra:1.40,\nshirt:1.45,\n"
       "jacket:1.45,\narmor:1.40,\ncovered nipples:1.40,\ncensored:1.45\n>")

NUEVOS = [
    # la bailarina clasica: pelvic curtain + harem pants + monedas
    ("BD-Harem/Dancer",
     "([red] harem outfit:1.55),\n([gold] pelvic curtain:1.45),\n"
     "(harem pants:1.40),\n(bandeau:1.35),\n(coin:1.30),\n(gold trim:1.30),\n"
     "(armlet:1.30),\n(anklet:1.25),\n(underboob:1.40),\n(cameltoe:1.30),\n"
     "(navel:1.25),\n(revealing clothes:1.35)"),
    # todo transparente
    ("BD-Harem/Veil",
     "([purple] harem outfit:1.50),\n(see-through clothes:1.60),\n"
     "(mouth veil:1.45),\n(veil:1.35),\n(harem pants:1.40),\n"
     "([purple] micro thong:1.40),\n(nipples:1.45),\n(areolae:1.25),\n"
     "(gold trim:1.25),\n(armlet:1.25)"),
    # egipcio: el collar ancho es el tag que lo dice
    ("BD-Harem/Egypt",
     "(usekh collar:1.55),\n([gold] micro bikini:1.50),\n"
     "([gold] pelvic curtain:1.45),\n(circlet:1.35),\n(armlet:1.35),\n"
     "(anklet:1.30),\n(ankh:1.25),\n(gold trim:1.35),\n(underboob:1.35),\n"
     "(cameltoe:1.30),\n(navel piercing:1.25)"),
    # la version con tocado, pecho al aire
    ("BD-Harem/Pharaoh",
     "([gold] headdress:1.50),\n(usekh collar:1.50),\n(topless female:1.55),\n"
     "(breasts out:1.45),\n(nipples:1.40),\n([white] loincloth:1.40),\n"
     "(pelvic curtain:1.35),\n(circlet:1.30),\n(armlet:1.30),\n"
     "(gold trim:1.30)"),
    # bikini de monedas y cadenas
    ("BD-Harem/Coin",
     "([gold] micro bikini:1.55),\n(coin:1.45),\n(bandeau:1.35),\n"
     "(chain necklace:1.35),\n(head chain:1.30),\n(navel piercing:1.30),\n"
     "([gold] armlet:1.30),\n(anklet:1.25),\n(underboob:1.40),\n"
     "(sideboob:1.30),\n(cameltoe:1.30)"),
    # la mujer de compania: collar, cadenas y casi nada encima
    ("BD-Harem/Concubine",
     "([black] harem outfit:1.45),\n(see-through clothes:1.55),\n"
     "(collar:1.40),\n(chain necklace:1.35),\n([black] micro thong:1.45),\n"
     "(pasties:1.35),\n(breasts out:1.40),\n(nipples:1.40),\n"
     "(revealing clothes:1.40),\n(armlet:1.25)"),
    # el o-ring arriba, harem pants abajo
    ("BD-Harem/Genie",
     "([teal] o-ring top:1.55),\n([teal] harem pants:1.45),\n"
     "(o-ring bikini:1.40),\n(circlet:1.35),\n(armlet:1.30),\n(veil:1.30),\n"
     "(underboob:1.40),\n(sideboob:1.35),\n(navel:1.25),\n(gold trim:1.25)"),
    # el mas explicito del subgrupo
    ("BD-Harem/Bare",
     "(topless female:1.60),\n(breasts out:1.50),\n(nipples:1.45),\n"
     "(areolae:1.30),\n([gold] pelvic curtain:1.45),\n"
     "([gold] micro thong:1.45),\n(usekh collar:1.35),\n(armlet:1.30),\n"
     "(anklet:1.30),\n(head chain:1.25),\n(cameltoe:1.30)"),
]


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, cuerpo in NUEVOS:
        Special.objects.update_or_create(
            name=nombre,
            defaults={"prompt": cuerpo + "\n\n" + NEG, "tier": TIER},
        )


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n for n, _ in NUEVOS]).delete()


class Migration(migrations.Migration):

    dependencies = [("generate", "0104_bd_cos_picante")]

    operations = [migrations.RunPython(aplicar, revertir)]
