from django.db import migrations


# Repaso de los 14 BD-COS. Nueve tenian algo roto.
#
# El grave es Killjoy: su bloque <neg:> negaba face, head, hair, skin, body,
# arms, hands y legs. La intencion parece haber sido "que solo importe la
# ropa", pero en un negativo eso le pide al modelo que NO dibuje la cara ni el
# cuerpo de la persona. Ademas pedia black-framed eyewear en el positivo y
# negaba glasses, que es su padre: se cancelaban entre si.
#
# El resto son tags de 0 posts y alias. Un alias cuenta posts al consultarlo
# pero nunca apareci como caption de entrenamiento, asi que en el prompt vale
# lo mismo que un tag muerto:
#   chinese dress / cheongsam / china dress  -> qipao
#   low-rise pants                           -> lowleg pants
#   hip lines                                -> groin
# Muertos sin reemplazo (0 posts y sin alias): lace-trimmed, high-neck dress,
# chest cutout, high slit, fitted gloves, robotic gloves, corset top,
# deep neckline, exposed midriff, sleeveless vest, open front vest,
# bare skin under vest, visible thong sides, color-blocked pants, white panels,
# simple top, simple pants, straight pants, camo pants, tactical belt,
# exposed lower abdomen, lowrise_pants.
#
# Juri y Ashley eran los dos unicos sin bloque <neg:>, asi que nada impedia que
# les apareciera un vestido encima del conjunto. Se les agrega uno.

NUEVOS = {
    # lace-trimmed -> lace trim | high-neck dress -> turtleneck
    # chest cutout -> cleavage cutout | high slit -> side slit
    "BD-COS/2B": (
        "([black] dress:1.50), (turtleneck:1.35), (short dress:1.40), "
        "(side slit:1.40), (clothing cutout:1.35), (cleavage cutout:1.30), "
        "(lace trim:1.25), (puffy sleeves:1.40), (juliet sleeves:1.35), "
        "(feather trim:1.35), (long sleeves:1.25), (black gloves:1.30), "
        "(black thighhighs:1.30) <neg: long dress:1.50, floor-length dress:1.50, "
        "maxi dress:1.50, pants:1.50, shorts:1.50, skirt:1.30, bodysuit:1.40, "
        "leotard:1.40, shirt:1.50, t-shirt:1.50, blouse:1.50>"
    ),
    # fitted gloves muerto; en el neg, robotic gloves muerto y metal gloves
    # con 663 posts no frena nada: gauntlets y armor ya cubren eso
    "BD-COS/Cammy": (
        "([green] leotard:1.50), (highleg leotard:1.40), (red gloves:1.30), "
        "(long gloves:1.30), (thigh straps:1.25), (utility belt:1.20) "
        "<neg: gauntlets:1.50, arm guards:1.40, armor:1.40, pants:1.50, "
        "shorts:1.50, skirt:1.50, dress:1.50, shirt:1.50, t-shirt:1.50, "
        "jacket:1.40, coat:1.40>"
    ),
    # Chinese dress es alias de qipao: el canonico pasa al frente
    "BD-COS/Chun-Li": (
        "([black] sleeveless dress:1.50), (qipao:1.45), (highleg:1.35), "
        "(side slit:1.30), (gold trim:1.30), (gold sash:1.30), "
        "(red rope belt:1.25) <neg: pantyhose:1.50, thighhighs:1.50, "
        "stockings:1.50, pants:1.50, shorts:1.50, skirt:1.40, sleeves:1.50, "
        "long sleeves:1.50>"
    ),
    # corset top muerto; corset solo ya es el tag real
    "BD-COS/Ivy": (
        "([purple] corset:1.50), (bare shoulders:1.30), (long gloves:1.35), "
        "(fingerless gloves:1.25), ([purple] pants:1.45), (tight pants:1.40), "
        "(high-waist pants:1.30), (belt:1.25) <neg: dress:1.50, skirt:1.50, "
        "shorts:1.50, leotard:1.50, bodysuit:1.50, jumpsuit:1.50, shirt:1.50, "
        "t-shirt:1.50, blouse:1.50, cape:1.50, coat:1.40>"
    ),
    # el mas roto: 8 tokens muertos de ~20, y sin bloque <neg:>
    "BD-COS/Juri": (
        "(white cropped vest:1.50),\n(cropped vest:1.40),\n(open vest:1.35),\n"
        "(vest:1.25),\n(midriff:1.40),\n([magenta] vest trim:1.30),\n"
        "(yoga pants:1.40),\n(lowleg pants:1.50),\n(puffy pants:1.45),\n"
        "(black pants:1.40),\n([magenta] trim:1.30),\n(groin:1.20)\n\n"
        "<neg:\ndress:1.50,\nskirt:1.50,\nshorts:1.50,\nleotard:1.50,\n"
        "bodysuit:1.50,\njumpsuit:1.50,\nshirt:1.50,\nt-shirt:1.50,\n"
        "blouse:1.50,\njacket:1.40,\ncoat:1.40\n>"
    ),
    # camo pants -> camouflage | tactical belt -> utility belt
    "BD-COS/Leona": (
        "([yellow] crop top:1.50), (sleeveless crop top:1.40), (midriff:1.40), "
        "(lowleg pants:1.50), (camouflage:1.45), (cargo pants:1.40), "
        "(baggy pants:1.30), (utility belt:1.35), (pouches:1.30), "
        "(black gloves:1.30), (black armband:1.25), (black choker:1.20) "
        "<neg: dress:1.50, skirt:1.50, shorts:1.50, leotard:1.50, "
        "bodysuit:1.50, jumpsuit:1.50, shirt:1.50, t-shirt:1.50, blouse:1.50, "
        "high-waist pants:1.50>"
    ),
    # tenia tres muertos seguidos: simple top, simple pants, straight pants
    "BD-COS/Sakura": (
        "([red] sleeveless shirt:1.50),\n(sleeveless top:1.45),\n"
        "(crop top:1.40),\n(midriff:1.50),\n\n(lowleg pants:1.70),\n"
        "(white pants:1.50),\n\n<neg:\npink hair:1.50,\ngreen eyes:1.50,\n"
        "forehead mark:1.50,\nred hairband:1.50,\nhairband:1.40,\n"
        "sakuraharuno:1.50\n>"
    ),
    # lowrise_pants ni siquiera resuelve; el canonico es lowleg pants
    "BD-COS/Tsunade": (
        "([green] haori:1.4), (gray crop top:1.4), (crop top:1.35), "
        "(sleeveless:1.25), (blue obi:1.25), ([blue] pants:1.3), "
        "(lowleg pants:1.3), (midriff:1.35), <neg:(dress:1.4),(skirt:1.4),"
        "(shorts:1.3),(short shorts:1.3),(jeans:1.3),(leggings:1.3),"
        "(bodysuit:1.3),(jumpsuit:1.3),(long sleeves:1.3),(shirt:1.3),"
        "(t-shirt:1.3),(blouse:1.3),(bra:1.2),(underwear:1.2)>"
    ),
    # sacar la anatomia del negativo y glasses, que peleaba con el positivo
    "BD-COS/Killjoy": (
        "([white] cropped shirt:1.30),\n([yellow] cropped jacket:1.30),\n"
        "(black lowleg pants:1.40),\n(black-framed eyewear:1.20),\n"
        "(fingerless gloves:1.20),\n\n<neg:\n(hat:1.30),\n(beanie:1.30),\n"
        "(weapon:1.50),\n(gun:1.50)\n>"
    ),
    # la frase entera no es tag: se parte en los dos que si existen
    "BD-COS/Ashley": (
        "([orange] sleeveless turtleneck:1.60),\n(turtleneck sweater:1.35),\n"
        "([green] plaid skirt:1.5),\n(pantyhose:1.3),\n(necklace:1.15),\n"
        "(earrings:1.1)\n\n<neg:\npants:1.50,\nshorts:1.50,\ndress:1.45,\n"
        "leotard:1.45,\nbodysuit:1.45,\nlong sleeves:1.30\n>"
    ),
}


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, prompt in NUEVOS.items():
        Special.objects.filter(name=nombre).update(prompt=prompt)


def revertir(apps, schema_editor):
    # los prompts previos quedan en el backup diario; este data migration no
    # los recrea porque eran justamente los rotos
    pass


class Migration(migrations.Migration):

    dependencies = [("generate", "0102_grupo_glow")]

    operations = [migrations.RunPython(aplicar, revertir)]
