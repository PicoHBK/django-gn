from django.db import migrations


# BD-Night/ pasa entero al registro subido de tono. Los 8 que habia eran
# ropa de dormir mansa -pajamas, nightgown, chemise, robe- indistinguible de
# BD-Str/. Ahora la prenda es la misma pero abierta, transparente o caida:
#
#   see-through clothes 220.475   strap slip 52.536   lace trim 71.104
#   no bra 116.638                no panties 116.638  garter straps 114.496
#
# "strap slip" (52.536) es el tirante caido, que es lo que mas cambia el
# registro sin cambiar la prenda.
#
# Se suman 6: Lace, Slip, Sheer, Garter, Front Tie y Micro, con
# lace-trimmed bra (16.811), lace-trimmed panties (15.081), front-tie top
# (53.429), side-tie panties (48.452) y micro panties (3.184).
#
# Cuatro tags que parecian obvios NO existen: slip_dress, nightwear,
# sheer_legwear y lace-trimmed_legwear. Y teddy_(lingerie) tiene 141 posts.
#
# Ninguno lleva calzado y ninguno pasa de 4 codigos de color.
CAMBIOS = [['BD-Night/Pajamas', '(pajamas:1.1),pajama pants,shirt pajamas,midriff', '([blue] pajamas:1.55),\n(open pajamas:1.45),\n(strap slip:1.40),\n(no bra:1.40),\n([white] panties:1.35),\n(midriff:1.30)'], ['BD-Night/Pajamas Set', '([blue] pajamas:1.55),\n(long sleeves:1.30),\n([blue] pajama pants:1.40)', '([pink] pajamas:1.55),\n(unbuttoned:1.45),\n(open clothes:1.40),\n(no bra:1.40),\n(midriff:1.35),\n([pink] panties:1.30)'], ['BD-Night/Nightgown', '([white] nightgown:1.55),\n(see-through silhouette:1.30),\n(spaghetti straps:1.25)', '([white] nightgown:1.55),\n(see-through clothes:1.50),\n(see-through silhouette:1.40),\n(strap slip:1.40),\n(no bra:1.35)'], ['BD-Night/Chemise', '([black] chemise:1.55),\n(lace trim:1.35),\n(spaghetti straps:1.25)', '([black] chemise:1.55),\n(lace trim:1.45),\n(see-through clothes:1.45),\n(strap slip:1.35),\n(no panties:1.30)'], ['BD-Night/Robe', '([white] robe:1.50),\n(open robe:1.40),\n(loose belt:1.25)', '([white] robe:1.50),\n(open robe:1.55),\n(no bra:1.40),\n(no panties:1.35),\n(bare shoulders:1.30)'], ['BD-Night/Bathrobe', 'bathrobe,open robe,[white] robe,bathrobe,naked robe', '([white] bathrobe:1.50),\n(open robe:1.55),\n(loose belt:1.35),\n(no bra:1.40),\n(cleavage:1.30)'], ['BD-Night/Negligee', 'dark [black] negligee', '([black] negligee:1.55),\n(see-through clothes:1.50),\n(lace trim:1.40),\n(garter belt:1.35),\n(strap slip:1.30)'], ['BD-Night/Babydoll', 'babydoll,[black] babydoll,<lora:bikini_slider:-2>', '([pink] babydoll:1.55),\n(see-through clothes:1.45),\n(lace-trimmed panties:1.40),\n(frills:1.30),\n(underboob:1.30)']]

NUEVOS = [['BD-Night/Lace', '([black] lace-trimmed bra:1.55),\n([black] lace-trimmed panties:1.50),\n(lace trim:1.45),\n(lace:1.35),\n(garter straps:1.30)'], ['BD-Night/Slip', '([white] camisole:1.55),\n(strap slip:1.55),\n(no bra:1.45),\n(off shoulder:1.35),\n([white] panties:1.30)'], ['BD-Night/Sheer', '([white] see-through clothes:1.60),\n(see-through silhouette:1.50),\n(nightgown:1.35),\n(no bra:1.40),\n(no panties:1.35)'], ['BD-Night/Garter', '([black] garter belt:1.55),\n(garter straps:1.50),\n([black] thighhighs:1.40),\n(lace trim:1.35),\n(lingerie:1.35)'], ['BD-Night/Front Tie', '([red] front-tie top:1.55),\n([red] side-tie panties:1.50),\n(lingerie:1.35),\n(cleavage:1.25)'], ['BD-Night/Micro', '([black] micro panties:1.60),\n([black] camisole:1.45),\n(no bra:1.45),\n(strap slip:1.35),\n(midriff:1.30)']]


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, _viejo, nuevo in CAMBIOS:
        s = Special.objects.filter(name=nombre).first()
        if s is not None:
            s.prompt = nuevo
            s.save(update_fields=["prompt"])
    for nombre, prompt in NUEVOS:
        if Special.objects.filter(name=nombre).exists():
            continue
        Special.objects.create(name=nombre, tier="tier3", prompt=prompt)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()
    for nombre, viejo, _nuevo in CAMBIOS:
        s = Special.objects.filter(name=nombre).first()
        if s is not None:
            s.prompt = viejo
            s.save(update_fields=["prompt"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0072_reparar_fc"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
