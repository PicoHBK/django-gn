from django.db import migrations


# Todos los specials de pelo pasan a forzar pelo largo, como ya hacia
# Hair-Ponytail: largo en el positivo, "short hair"/"medium hair" en el
# negativo, y los dos tambien como tags_deleted para arrancarselos al
# personaje si los trae.
#
# Van como tag de dos palabras a proposito: deleteTags los borra por
# coincidencia exacta del token, que es como los escriben las skins
# ("short hair" suelto aparece en 33 de ellas).
LARGO = ["short hair", "medium hair"]

CAMBIOS = [
    (
        "Hair-Blunt",
        # viejo
        "<(blunt bangs:1.70)>,\n(straight bangs:1.45),\n(even bangs:1.40),\n"
        "(thick bangs:1.25),\n\n<neg:\nside-swept bangs:1.50,\n"
        "swept bangs:1.50,\nasymmetrical bangs:1.50,\nparted bangs:1.50\n>",
        # nuevo
        "<(blunt bangs:1.70)>,\n(straight bangs:1.45),\n(even bangs:1.40),\n"
        "(thick bangs:1.25),\n(very long hair:1.55),\n(long hair:1.30),\n\n"
        "<neg:\nside-swept bangs:1.50,\nswept bangs:1.50,\n"
        "asymmetrical bangs:1.50,\nparted bangs:1.50,\nshort hair:1.45,\n"
        "medium hair:1.30\n>",
    ),
    (
        "Hair-One Eye",
        "<(hair over one eye:1.70)>,\n(very long hair:1.50),\n"
        "(covering one eye:1.60),\n\n<neg:\nhair between eyes:1.40,\n"
        "center part:1.40,\nside part:1.30,\nhair behind ears:1.30\n>",
        "<(hair over one eye:1.70)>,\n(very long hair:1.60),\n"
        "(covering one eye:1.60),\n(long hair:1.30),\n\n"
        "<neg:\nhair between eyes:1.40,\ncenter part:1.40,\n"
        "side part:1.30,\nhair behind ears:1.30,\nshort hair:1.45,\n"
        "medium hair:1.30\n>",
    ),
    (
        "Hair-Bun",
        "<(hair bun:1.70)>,\n<(single hair bun:1.60)>,\n"
        "(hair pulled back:1.50),\n(slicked back hair:1.40),\n"
        "(hair up:1.35),\n(forehead:1.30),\n\n<neg:\nhair down:1.50,\n"
        "loose hair:1.50,\ndouble bun:1.45,\ntwintails:1.50,\n"
        "ponytail:1.45,\nbangs:1.45,\nsidelocks:1.40,\n"
        "hair over one eye:1.40,\nmessy hair:1.40,\n"
        "hair between eyes:1.30\n>",
        "<(hair bun:1.70)>,\n<(single hair bun:1.60)>,\n"
        "(hair pulled back:1.50),\n(slicked back hair:1.40),\n"
        "(hair up:1.35),\n(very long hair:1.50),\n(forehead:1.30),\n\n"
        "<neg:\nhair down:1.50,\nloose hair:1.50,\ndouble bun:1.45,\n"
        "twintails:1.50,\nponytail:1.45,\nbangs:1.45,\nsidelocks:1.40,\n"
        "hair over one eye:1.40,\nmessy hair:1.40,\n"
        "hair between eyes:1.30,\nshort hair:1.45,\nmedium hair:1.30\n>",
    ),
    (
        "Hair-Tsunade",
        "<(curtained hair:1.70)>,\n<(parted bangs:1.55)>,\n"
        "(center part:1.40),\n(hair framing face:1.35),\n(long hair:1.25),\n"
        "\n<neg:\nblunt bangs:1.50,\nstraight bangs:1.45,\n"
        "hair intakes:1.45,\nswept bangs:1.40,\nasymmetrical bangs:1.40,\n"
        "hair over one eye:1.40\n>",
        "<(curtained hair:1.70)>,\n<(parted bangs:1.55)>,\n"
        "(center part:1.40),\n(hair framing face:1.35),\n"
        "(very long hair:1.60),\n(absurdly long hair:1.30),\n"
        "\n<neg:\nblunt bangs:1.50,\nstraight bangs:1.45,\n"
        "hair intakes:1.45,\nswept bangs:1.40,\nasymmetrical bangs:1.40,\n"
        "hair over one eye:1.40,\nshort hair:1.45,\nmedium hair:1.30\n>",
    ),
]


def aplicar(apps, schema_editor):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")

    for nombre, _viejo, nuevo in CAMBIOS:
        s = Special.objects.filter(name=nombre).first()
        if s is None:
            continue
        s.prompt = nuevo
        s.save(update_fields=["prompt"])
        for t in LARGO:
            tag, _ = Tag.objects.get_or_create(name=t)
            s.tags_deleted.add(tag)


def revertir(apps, schema_editor):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")

    for nombre, viejo, _nuevo in CAMBIOS:
        s = Special.objects.filter(name=nombre).first()
        if s is None:
            continue
        s.prompt = viejo
        s.save(update_fields=["prompt"])
        s.tags_deleted.remove(*Tag.objects.filter(name__in=LARGO))


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0024_hair_ponytail_solo_cola"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
