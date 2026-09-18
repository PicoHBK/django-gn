from django.db import migrations


# Correccion de largo: los specials pedian "very long hair" y "absurdly long
# hair" y el pelo salia hasta el piso. Segun el wiki de Danbooru:
#
#   long hair            de los hombros a MENOS que la cintura
#   very long hair       "longer than the waist", de la cintura a los pies
#   absurdly long hair   mas largo que el personaje, o sea el piso
#
# Para largo hasta la cintura el tag es "long hair" a secas. Los otros dos
# pasan al negativo, y ademas entran como tags_deleted para arrancarle al
# personaje su propio tag de largo: si la skin trae "very long hair" en el
# positivo, pelea contra el negativo y gana ella.
LARGO_DE_MAS = ["very long hair", "absurdly long hair"]

CAMBIOS = [
    (
        'Hair-Blunt',
        # viejo
        '<(blunt bangs:1.70)>,\n(straight bangs:1.45),\n(even bangs:1.40),\n(thick bangs:1.25),\n(very long hair:1.55),\n(long hair:1.30),\n\n<neg:\nside-swept bangs:1.50,\nswept bangs:1.50,\nasymmetrical bangs:1.50,\nparted bangs:1.50,\nshort hair:1.45,\nmedium hair:1.30\n>',
        # nuevo
        '<(blunt bangs:1.70)>,\n(straight bangs:1.45),\n(even bangs:1.40),\n(thick bangs:1.25),\n(long hair:1.50),\n\n<neg:\nside-swept bangs:1.50,\nswept bangs:1.50,\nasymmetrical bangs:1.50,\nparted bangs:1.50,\nshort hair:1.45,\nmedium hair:1.30,\nvery long hair:1.30,\nabsurdly long hair:1.50\n>',
    ),
    (
        'Hair-One Eye',
        # viejo
        '<(hair over one eye:1.70)>,\n(very long hair:1.60),\n(covering one eye:1.60),\n(long hair:1.30),\n\n<neg:\nhair between eyes:1.40,\ncenter part:1.40,\nside part:1.30,\nhair behind ears:1.30,\nshort hair:1.45,\nmedium hair:1.30\n>',
        # nuevo
        '<(hair over one eye:1.70)>,\n(covering one eye:1.60),\n(long hair:1.50),\n\n<neg:\nhair between eyes:1.40,\ncenter part:1.40,\nside part:1.30,\nhair behind ears:1.30,\nshort hair:1.45,\nmedium hair:1.30,\nvery long hair:1.30,\nabsurdly long hair:1.50\n>',
    ),
    (
        'Hair-Ponytail',
        # viejo
        '<(high ponytail:1.70)>,\n(very long hair:1.60),\n(absurdly long hair:1.40),\n(hair tie:1.20),\n\n<neg:\nlow ponytail:1.50,\nside ponytail:1.50,\nshort ponytail:1.50,\nfolded ponytail:1.40,\ntwintails:1.50,\nhair bun:1.40,\nhair down:1.45,\nshort hair:1.45\n>',
        # nuevo
        '<(high ponytail:1.70)>,\n(hair tie:1.20),\n(long hair:1.50),\n\n<neg:\nlow ponytail:1.50,\nside ponytail:1.50,\nshort ponytail:1.50,\nfolded ponytail:1.40,\ntwintails:1.50,\nhair bun:1.40,\nhair down:1.45,\nshort hair:1.45,\nvery long hair:1.30,\nabsurdly long hair:1.50\n>',
    ),
    (
        'Hair-Bun',
        # viejo
        '<(hair bun:1.70)>,\n<(single hair bun:1.60)>,\n(hair pulled back:1.50),\n(slicked back hair:1.40),\n(hair up:1.35),\n(very long hair:1.50),\n(forehead:1.30),\n\n<neg:\nhair down:1.50,\nloose hair:1.50,\ndouble bun:1.45,\ntwintails:1.50,\nponytail:1.45,\nbangs:1.45,\nsidelocks:1.40,\nhair over one eye:1.40,\nmessy hair:1.40,\nhair between eyes:1.30,\nshort hair:1.45,\nmedium hair:1.30\n>',
        # nuevo
        '<(hair bun:1.70)>,\n<(single hair bun:1.60)>,\n(hair pulled back:1.50),\n(slicked back hair:1.40),\n(hair up:1.35),\n(forehead:1.30),\n(long hair:1.50),\n\n<neg:\nhair down:1.50,\nloose hair:1.50,\ndouble bun:1.45,\ntwintails:1.50,\nponytail:1.45,\nbangs:1.45,\nsidelocks:1.40,\nhair over one eye:1.40,\nmessy hair:1.40,\nhair between eyes:1.30,\nshort hair:1.45,\nmedium hair:1.30,\nvery long hair:1.30,\nabsurdly long hair:1.50\n>',
    ),
    (
        'Hair-Tsunade',
        # viejo
        '<(curtained hair:1.70)>,\n<(parted bangs:1.55)>,\n(center part:1.40),\n(hair framing face:1.35),\n(very long hair:1.60),\n(absurdly long hair:1.30),\n\n<neg:\nblunt bangs:1.50,\nstraight bangs:1.45,\nhair intakes:1.45,\nswept bangs:1.40,\nasymmetrical bangs:1.40,\nhair over one eye:1.40,\nshort hair:1.45,\nmedium hair:1.30\n>',
        # nuevo
        '<(curtained hair:1.70)>,\n<(parted bangs:1.55)>,\n(center part:1.40),\n(hair framing face:1.35),\n(long hair:1.50),\n\n<neg:\nblunt bangs:1.50,\nstraight bangs:1.45,\nhair intakes:1.45,\nswept bangs:1.40,\nasymmetrical bangs:1.40,\nhair over one eye:1.40,\nshort hair:1.45,\nmedium hair:1.30,\nvery long hair:1.30,\nabsurdly long hair:1.50\n>',
    ),
]


def _aplicar(apps, indice_prompt, agregar_tags):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")

    for cambio in CAMBIOS:
        nombre = cambio[0]
        s = Special.objects.filter(name=nombre).first()
        if s is None:
            continue
        s.prompt = cambio[indice_prompt]
        s.save(update_fields=["prompt"])
        if agregar_tags:
            for t in LARGO_DE_MAS:
                tag, _ = Tag.objects.get_or_create(name=t)
                s.tags_deleted.add(tag)
        else:
            s.tags_deleted.remove(*Tag.objects.filter(name__in=LARGO_DE_MAS))


def aplicar(apps, schema_editor):
    _aplicar(apps, 2, True)


def revertir(apps, schema_editor):
    _aplicar(apps, 1, False)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0025_hair_siempre_largo"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
