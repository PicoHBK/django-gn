from django.db import migrations


# Reparacion de los 12 FC-. Cuatro tags muertos, una fuga de tier y pesos
# que no hacian nada.
#
# TAGS CON 0 POSTS EN DANBOORU:
#   stream_cry        en FC-Crying        -> streaming tears (13.323)
#   heavy_makeup      en FC-Makeup High   -> era su tag principal, asi que el
#                                            "High" no hacia nada. Ahora
#                                            makeup + eyeshadow + eyeliner +
#                                            lipstick, todos con peso.
#   scared_expression en FC-Org
#   smokey_eyeshadow  en FC-Red Lips      existe con 86 posts, inservible
#
# FC-Org tenia ademas una COMA DOBLE ("female orgasm,,scared"), que mete un
# token vacio, y "scared expression screaming" pegado sin coma, o sea un solo
# token que no existe.
#
# FC-Red Lips arrancaba Y terminaba con un backtick suelto. Es el cuarto
# lugar con ese mismo bug, despues de BD-COS/Tsunade, GaSlider-Med y los tres
# FT- de tacos.
#
# FUGA DE TIER: FC-Org es "orgasm, female orgasm" y estaba en TIER1, el tier
# que el front muestra a todos. Pasa a tier5.
#
# PESOS: seis de los doce no tenian ninguno, y los que tenian estaban en 1.1
# o 1.2, apenas por encima de 1, que es casi no pedir nada. Ahora el
# dominante va en 1.45-1.55.
ARREGLOS = [['FC-Blush', 'blush', '(blush:1.45)'], ['FC-Closed Eyes', '(closed eyes:1.1)', '(closed eyes:1.45)'], ['FC-Con Pup', '(constricted pupils:1.1)', '(constricted pupils:1.45)'], ['FC-Crying', 'stream cry,crying,(tears:1.4)', '(crying:1.50),\n(streaming tears:1.45),\n(tears:1.40)'], ['FC-Facing V', 'facing viewer', '(facing viewer:1.45)'], ['FC-Half-C-E', 'half-closed eyes', '(half-closed eyes:1.45)'], ['FC-Look Another', 'looking at another', '(looking at another:1.45)'], ['FC-Look At TV', '(looking at viewer:1.2)', '(looking at viewer:1.45)'], ['FC-Makeup High', 'heavy_makeup,makeup', '(makeup:1.55),\n(eyeshadow:1.40),\n(eyeliner:1.35),\n(lipstick:1.35)'], ['FC-Open Mouth', '(open mouth:1.5)', '(open mouth:1.50)'], ['FC-Org', 'orgasm,closed eyes,blush,female orgasm,,scared expression screaming, open mouth,head back', '(orgasm:1.55),\n(female orgasm:1.45),\n(closed eyes:1.35),\n(blush:1.35),\n(screaming:1.30),\n(open mouth:1.35),\n(head back:1.30)'], ['FC-Red Lips', '`([red] lips:1.3), (black eyeliner:1.3), (black smokey eyeshadow:1.2), (black eyeshadow under eye:1.15), (eyelashes:1.2), (beauty mark:1.25)`', '([red] lips:1.45),\n(red lips:1.40),\n(lipstick:1.35),\n(eyeliner:1.35),\n(eyeshadow:1.30),\n(eyelashes:1.25),\n(mole under eye:1.20)']]

TIER = [['FC-Org', 'tier5', 'tier1']]


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


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
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
        ("generate", "0071_ft_calzado"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
