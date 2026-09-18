from django.db import migrations


# Tags de ropa (vocabulario Danbooru/Illustrious) que faltaban en la lista de
# AA-Bare All. Solo prendas: nada de joyeria, pelo ni rasgos del personaje.
#
# deleteTags() en generate/services.py compara PALABRA COMPLETA contra cada
# token del prompt (y convierte "_" en espacio), asi que estos van en una sola
# palabra: "jacket" se lleva "cropped jacket", "pink jacket", "suit_jacket".
# Por eso tampoco sirven las de dos palabras y por eso hay singulares sueltos
# ("thighhigh" no lo cubre "thighhighs").
TAGS_ROPA = [
    # Torso y cuerpo entero
    'blouse', 'cardigan', 'hoodie', 'sweatshirt', 'pullover', 'tanktop',
    'halterneck', 'halter', 'bustier', 'corset', 'chemise', 'negligee',
    'nightgown', 'robe', 'yukata', 'cheongsam', 'qipao', 'sari',
    'dirndl', 'gakuran', 'blazer', 'waistcoat', 'poncho', 'cloak',
    'shawl', 'bolero', 'parka', 'windbreaker', 'raincoat', 'trenchcoat',
    'overcoat', 'jumper', 'smock', 'tabard', 'surcoat', 't-shirt',
    'tshirt', 'polo', 'toga', 'sundress', 'minidress', 'microdress',
    'pinafore', 'overalls', 'jumpsuit', 'romper', 'playsuit', 'onesie',
    # Parte de abajo
    'trousers', 'slacks', 'chaps', 'capri', 'culottes', 'hakama',
    'sarong', 'loincloth', 'fundoshi', 'bloomers', 'briefs', 'boxers',
    'underwear', 'lingerie', 'garter', 'garterbelt', 'petticoat',
    'tutu', 'sweatpants', 'joggers', 'buruma', 'spats', 'hotpants',
    'skort', 'kilt', 'pareo',
    # Interior y bano
    'monokini', 'tankini', 'microbikini', 'pasties', 'bandeau', 'nubra',
    'swimwear', 'sleepwear', 'nightwear', 'underbust', 'overbust',
    # Calzado y medias
    'shoes', 'shoe', 'boot', 'heel', 'pumps', 'loafers', 'sneaker',
    'geta', 'zori', 'okobo', 'wedges', 'flats', 'clogs', 'moccasins',
    'espadrilles', 'socks', 'kneehighs', 'thighhigh', 'tabi',
    'legwarmers', 'crocs', 'flip-flops', 'footwraps',
    # Cabeza
    'headdress', 'bonnet', 'bandana', 'visor', 'coronet', 'veil',
    'hairnet', 'hijab', 'turban', 'fedora', 'sombrero', 'nightcap',
    'earmuffs', 'goggles', 'sunglasses', 'eyepatch', 'monocle',
    'kerchief',
    # Correas, arnes y armadura
    'harness', 'holster', 'pouch', 'bandolier', 'armband', 'bracer',
    'epaulettes', 'pauldron', 'breastplate', 'greaves', 'chainmail',
    'gorget', 'ascot', 'cravat',
    # Modificadores de prenda
    'see-through', 'off-shoulder', 'backless', 'sideless', 'highleg',
    'lowleg', 'front-tie', 'criss-cross', 'cross-laced', 'pleated',
    'ruffled', 'lace', 'plaid', 'tartan', 'checkered', 'fishnet',
    'mesh', 'denim', 'velvet', 'satin', 'revealing', 'skimpy', 'outfit',
    'attire', 'costume', 'garment', 'gown', 'strapless',
    # Arreglos de la lista actual
    'choker',
]

SPECIAL = "AA-Bare All"


def agregar(apps, schema_editor):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")

    special = Special.objects.filter(name=SPECIAL).first()
    if special is None:
        return

    for nombre in TAGS_ROPA:
        tag, _ = Tag.objects.get_or_create(name=nombre)
        special.tags_deleted.add(tag)


def quitar(apps, schema_editor):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")

    special = Special.objects.filter(name=SPECIAL).first()
    if special is None:
        return

    # Solo desasocia; los Tag quedan por si otro special los usa.
    special.tags_deleted.remove(*Tag.objects.filter(name__in=TAGS_ROPA))


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0017_pose_special_enabled"),
    ]

    operations = [
        migrations.RunPython(agregar, quitar),
    ]
