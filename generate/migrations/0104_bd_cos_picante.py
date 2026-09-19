from django.db import migrations


# Correccion de la 0103. Al reparar los tags muertos saque de Juri y Leona
# "visible thong sides" y "exposed lower abdomen" sin reemplazarlos, pero esos
# no eran relleno: son los que hacen que el cosplay sea 70-80% fiel y no 100%,
# igual que midriff y lowleg. Se restauran.
#
# "visible thong sides" se reconstruye con micro thong (la regla del proyecto
# para todos los thongs de BD) mas panty straps (7.624) y lowleg (19.484).
# "exposed lower abdomen" ya lo cubria groin, se suma navel.
#
# Ademas se agrega lowleg a todos los que tienen lowleg pants: el tag suelto
# tiene diez veces mas volumen que lowleg_pants (1.797), asi que la cintura
# baja pega mucho mas fuerte.
#
# A Tsunade no se le agrega thong porque su propio <neg:> niega underwear.

NUEVOS = {
    "BD-COS/Juri": (
        "(white cropped vest:1.50),\n(cropped vest:1.40),\n(open vest:1.35),\n"
        "(vest:1.25),\n(midriff:1.40),\n([magenta] vest trim:1.30),\n"
        "(yoga pants:1.40),\n(lowleg pants:1.50),\n(lowleg:1.35),\n"
        "(puffy pants:1.45),\n(black pants:1.40),\n([magenta] trim:1.30),\n"
        "(micro thong:1.35),\n(panty straps:1.35),\n"
        "(groin:1.25),\n(navel:1.20)\n\n"
        "<neg:\ndress:1.50,\nskirt:1.50,\nshorts:1.50,\nleotard:1.50,\n"
        "bodysuit:1.50,\njumpsuit:1.50,\nshirt:1.50,\nt-shirt:1.50,\n"
        "blouse:1.50,\njacket:1.40,\ncoat:1.40\n>"
    ),
    "BD-COS/Leona": (
        "([yellow] crop top:1.50), (sleeveless crop top:1.40), (midriff:1.40), "
        "(lowleg pants:1.50), (lowleg:1.35), (camouflage:1.45), "
        "(cargo pants:1.40), (baggy pants:1.30), (utility belt:1.35), "
        "(pouches:1.30), (micro thong:1.35), (panty straps:1.35), "
        "(black gloves:1.30), (black armband:1.25), (black choker:1.20) "
        "<neg: dress:1.50, skirt:1.50, shorts:1.50, leotard:1.50, "
        "bodysuit:1.50, jumpsuit:1.50, shirt:1.50, t-shirt:1.50, blouse:1.50, "
        "high-waist pants:1.50>"
    ),
    "BD-COS/Sakura": (
        "([red] sleeveless shirt:1.50),\n(sleeveless top:1.45),\n"
        "(crop top:1.40),\n(midriff:1.50),\n\n(lowleg pants:1.70),\n"
        "(lowleg:1.40),\n(white pants:1.50),\n\n<neg:\npink hair:1.50,\n"
        "green eyes:1.50,\nforehead mark:1.50,\nred hairband:1.50,\n"
        "hairband:1.40,\nsakuraharuno:1.50\n>"
    ),
    "BD-COS/Tsunade": (
        "([green] haori:1.4), (gray crop top:1.4), (crop top:1.35), "
        "(sleeveless:1.25), (blue obi:1.25), ([blue] pants:1.3), "
        "(lowleg pants:1.35), (lowleg:1.35), (midriff:1.40), "
        "<neg:(dress:1.4),(skirt:1.4),(shorts:1.3),(short shorts:1.3),"
        "(jeans:1.3),(leggings:1.3),(bodysuit:1.3),(jumpsuit:1.3),"
        "(long sleeves:1.3),(shirt:1.3),(t-shirt:1.3),(blouse:1.3),"
        "(bra:1.2),(underwear:1.2)>"
    ),
    "BD-COS/Killjoy": (
        "([white] cropped shirt:1.30),\n([yellow] cropped jacket:1.30),\n"
        "(black lowleg pants:1.40),\n(lowleg:1.30),\n(midriff:1.25),\n"
        "(black-framed eyewear:1.20),\n(fingerless gloves:1.20),\n\n"
        "<neg:\n(hat:1.30),\n(beanie:1.30),\n(weapon:1.50),\n(gun:1.50)\n>"
    ),
}


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, prompt in NUEVOS.items():
        Special.objects.filter(name=nombre).update(prompt=prompt)


def revertir(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [("generate", "0103_bd_cos_reparar")]

    operations = [migrations.RunPython(aplicar, revertir)]
