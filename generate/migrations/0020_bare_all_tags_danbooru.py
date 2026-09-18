from django.db import migrations


# Tercera tanda para AA-Bare All. Sale de cruzar el grafo de implicaciones de
# Danbooru (46.028 implicaciones activas, BFS desde las raices de ropa = 2.118
# tags) contra lo que ya borrabamos: quedaban 194 sin cubrir, y casi todos eran
# variantes de color de estas pocas palabras.
#
# Fuera a proposito:
#   hairband, ear, cat, dog, rabbit, bear -> pelo y rasgos, van en otro special
#   single   -> se lleva "single hair bun", "single sidelock"
#   sock     -> se lleva "sock_bun hairystle"
#   plate    -> se lleva holding_plate, license_plate, empty_plate (vajilla)
#   mail     -> se lleva email, mailbox, blackmail
#   teddy    -> se lleva teddy bear
#   crotch   -> es cuerpo, aunque "crotch plate" sea armadura
#   knight, samurai -> son el personaje, no la prenda
#   gloved   -> borraria el token entero de "gloved handjob"
TAGS_DANBOORU = [
    # Prendas que faltaban (japonesas, chinas, de dormir)
    'pajamas', 'pajama', 'happi', 'changpao', 'hanfu', 'ruqun', 'kappougi',
    'tangzhuang', 'qungua', 'shiroshouzoku', 'shiromuku', 'gakuseibou',
    'tokkoufuku', 'sukajan', 'bodystocking', 'tights', 'jodhpurs',
    'bikesuit', 'lolita', 'maid', 'telnyashka', 'kataginu',
    # Sombreros y calzado que faltaban
    'ushanka', 'bicorne', 'biretta', 'eboshi', 'uwabaki', 'flops', 'kepi',
    # Armadura: piezas que "armor" no alcanza porque son palabra propia
    'pauldrons', 'cuirass', 'sabaton', 'sabatons', 'tasset', 'tassets',
    'boobplate', 'faulds', 'greave', 'helm', 'menpu', 'menpoo', 'suneate',
    'stahlhelm', 'kabuto',
    # Singulares y plurales que la lista no cubria
    'gauntlet', 'vambrace', 'glove', 'belts', 'kneehigh',
    # Prenda fuera de sitio o a medio quitar
    'unworn', 'pantyshot', 'gunbelt',
]

SPECIAL = "AA-Bare All"


def agregar(apps, schema_editor):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")

    special = Special.objects.filter(name=SPECIAL).first()
    if special is None:
        return

    for nombre in TAGS_DANBOORU:
        tag, _ = Tag.objects.get_or_create(name=nombre)
        special.tags_deleted.add(tag)


def quitar(apps, schema_editor):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")

    special = Special.objects.filter(name=SPECIAL).first()
    if special is None:
        return

    # Solo desasocia; los Tag quedan por si otro special los usa.
    special.tags_deleted.remove(*Tag.objects.filter(name__in=TAGS_DANBOORU))


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0019_bare_all_tags_exposicion"),
    ]

    operations = [
        migrations.RunPython(agregar, quitar),
    ]
