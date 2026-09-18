from django.db import migrations


# Siete subgrupos nuevos de BD, con las prendas clasicas de Danbooru:
#
#   BD-Night/  dormir: pajamas (40.985), nightgown, chemise, robe
#   BD-Swim/   bano: bikini (704.102), string, side-tie (125.370),
#              front-tie, frilled, o-ring
#   BD-Latex/  segunda piel: bodysuit (184.074), latex, leather, shiny
#   BD-Cul/    cultural: qipao (78.241), hanbok, dirndl, ao dai
#   BD-Form/   formal: evening gown, cocktail, business suit, office lady
#   BD-Exp/    explicitas: underboob (128.440), cleavage cutout (122.691),
#              highleg leotard, pasties, crotchless, backless, navel cutout,
#              reverse bunnysuit, bodypaint
#   BD-Str/    calle: hoodie (199.456), cardigan, tank top, t-shirt, jeans
#
# Doce planos se pliegan al subgrupo que les corresponde en vez de duplicar:
# Pajamas, BD-Negligee, BD-Bathrobe y BD-Babydoll a BD-Night/; BD-Micro,
# BD-Ribbon Micro y BD-Slingshot a BD-Swim/; BD-Cop y BD-Sexy Leotard a
# BD-Latex/; BD-Chinese Dress a BD-Cul/; BD-Suite Office y BD-Office S a
# BD-Form/.
#
# Cuatro tags que parecen obvios NO existen en Danbooru y por eso no se usan:
# see-through (0), cutout (0), cheongsam (0) y sling bikini (0). Los reales
# son see-through_clothes, clothing_cutout, qipao y slingshot_swimsuit.
#
# Ninguno lleva calzado y ninguno pasa de 4 codigos de color, verificado.
NUEVOS = [['BD-Night/Pajamas Set', '([blue] pajamas:1.55),\n(long sleeves:1.30),\n([blue] pajama pants:1.40)'], ['BD-Night/Nightgown', '([white] nightgown:1.55),\n(see-through silhouette:1.30),\n(spaghetti straps:1.25)'], ['BD-Night/Chemise', '([black] chemise:1.55),\n(lace trim:1.35),\n(spaghetti straps:1.25)'], ['BD-Night/Robe', '([white] robe:1.50),\n(open robe:1.40),\n(loose belt:1.25)'], ['BD-Swim/Bikini', '([red] bikini:1.55),\n(bikini:1.35),\n(halterneck:1.25)'], ['BD-Swim/String', '([black] string bikini:1.60),\n(side-tie bikini bottom:1.40)'], ['BD-Swim/Side Tie', '([white] side-tie bikini bottom:1.60),\n([white] bikini top:1.45)'], ['BD-Swim/Front Tie', '([pink] front-tie bikini top:1.60),\n(bikini:1.35),\n(cleavage:1.20)'], ['BD-Swim/Frilled', '([yellow] frilled bikini:1.55),\n(frills:1.35),\n(bikini:1.30)'], ['BD-Swim/O-Ring', '([black] o-ring bikini:1.60),\n(o-ring:1.40),\n(highleg bikini:1.30)'], ['BD-Latex/Bodysuit', '([black] bodysuit:1.55),\n(skin tight:1.40),\n(covered navel:1.25)'], ['BD-Latex/Catsuit', '([black] latex bodysuit:1.60),\n(latex:1.45),\n(shiny clothes:1.35),\n(skin tight:1.30)'], ['BD-Latex/Leather', '([black] leather:1.55),\n(leather bodysuit:1.40),\n(shiny clothes:1.30)'], ['BD-Latex/Shiny', '([purple] shiny clothes:1.55),\n(skin tight:1.40),\n(bodysuit:1.30)'], ['BD-Cul/Qipao', '([red] qipao:1.55),\n(chinese clothes:1.40),\n(side slit:1.35),\n(mandarin collar:1.25)'], ['BD-Cul/Hanbok', '([pink] hanbok:1.55),\n(korean clothes:1.40),\n([white] jeogori:1.30)'], ['BD-Cul/Dirndl', '([green] dirndl:1.55),\n(apron:1.35),\n(puffy sleeves:1.30),\n(cleavage:1.20)'], ['BD-Cul/Ao Dai', '([white] ao dai:1.55),\n(vietnamese clothes:1.35),\n(side slit:1.30)'], ['BD-Form/Gown', '([black] evening gown:1.55),\n(long dress:1.40),\n(bare shoulders:1.30),\n(side slit:1.25)'], ['BD-Form/Cocktail', '([red] cocktail dress:1.55),\n(short dress:1.40),\n(strapless:1.30)'], ['BD-Form/Business', '([grey] business suit:1.55),\n(suit:1.40),\n(collared shirt:1.30),\n(pencil skirt:1.35)'], ['BD-Form/Office Lady', '([black] office lady:1.50),\n(pencil skirt:1.45),\n([white] collared shirt:1.35)'], ['BD-Exp/Crotchless', '([black] crotchless panties:1.60),\n(crotchless:1.45),\n(garter belt:1.30)'], ['BD-Exp/Pasties', '([black] pasties:1.60),\n(pasties:1.45),\n(micro thong:1.35)'], ['BD-Exp/Underboob', '([white] crop top:1.50),\n(underboob:1.55),\n(midriff:1.30)'], ['BD-Exp/Cleavage Cutout', '([black] dress:1.50),\n(cleavage cutout:1.55),\n(clothing cutout:1.35)'], ['BD-Exp/Navel Cutout', '([red] bodysuit:1.50),\n(navel cutout:1.55),\n(clothing cutout:1.35)'], ['BD-Exp/Backless', '([white] backless outfit:1.55),\n(backless dress:1.40),\n(bare back:1.30)'], ['BD-Exp/Highleg', '([black] highleg leotard:1.60),\n(highleg:1.40),\n(leotard:1.30)'], ['BD-Exp/Reverse Bunny', '([black] reverse bunnysuit:1.60),\n(detached collar:1.35),\n(wrist cuffs:1.25)'], ['BD-Exp/Bodypaint', '([gold] bodypaint:1.60),\n(bodypaint:1.45),\n(covered nipples:1.30)'], ['BD-Str/Hoodie', '([grey] hoodie:1.55),\n(drawstring:1.25),\n([blue] denim shorts:1.40)'], ['BD-Str/Jeans', '([blue] jeans:1.50),\n(denim:1.35),\n([white] tank top:1.45)'], ['BD-Str/Tee', '([white] t-shirt:1.55),\n(short sleeves:1.30),\n([blue] miniskirt:1.40)'], ['BD-Str/Cardigan', '([beige] cardigan:1.55),\n(open cardigan:1.35),\n([white] camisole:1.40)'], ['BD-Str/Tank', '([black] tank top:1.55),\n(bare shoulders:1.30),\n([blue] denim shorts:1.40)']]

PLEGAR = {'Pajamas': 'BD-Night/Pajamas', 'BD-Negligee': 'BD-Night/Negligee', 'BD-Micro': 'BD-Swim/Micro', 'BD-Ribbon Micro': 'BD-Swim/Ribbon', 'BD-Slingshot': 'BD-Swim/Slingshot', 'BD-Chinese Dress': 'BD-Cul/Chinese', 'BD-Cop': 'BD-Latex/Cop', 'BD-Sexy Leotard': 'BD-Latex/Leotard', 'BD-Suite Office': 'BD-Form/Suit', 'BD-Office S': 'BD-Form/Office', 'BD-Bathrobe': 'BD-Night/Bathrobe', 'BD-Babydoll': 'BD-Night/Babydoll'}


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for viejo, nuevo in PLEGAR.items():
        s = Special.objects.filter(name=viejo).first()
        if s is not None:
            s.name = nuevo
            s.save(update_fields=["name"])
    for nombre, prompt in NUEVOS:
        if Special.objects.filter(name=nombre).exists():
            continue
        Special.objects.create(name=nombre, tier="tier3", prompt=prompt)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()
    for viejo, nuevo in PLEGAR.items():
        s = Special.objects.filter(name=nuevo).first()
        if s is not None:
            s.name = viejo
            s.save(update_fields=["name"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0057_smile_default"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
