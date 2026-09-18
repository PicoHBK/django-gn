from django.db import migrations


# Hair-Ponytail pasa a ser solo la cola: se le saca el blunt bangs.
#
# Como ahora el special no opina sobre el frente, tampoco le borra "bangs" ni
# "sidelocks" al personaje: le respeta su flequillo y solo le cambia el pelo
# de atras. Los tags_deleted quedan en las familias que no pueden convivir con
# una sola cola alta.
#
# El largo va con "very long hair" y "absurdly long hair" porque en Danbooru
# no existen "long_ponytail" ni "very_long_ponytail" (0 posts las dos).
NOMBRE = "Hair-Ponytail"

NUEVO_PROMPT = (
    "<(high ponytail:1.70)>,\n"
    "(very long hair:1.60),\n"
    "(absurdly long hair:1.40),\n"
    "(hair tie:1.20),\n"
    "\n"
    "<neg:\n"
    "low ponytail:1.50,\n"
    "side ponytail:1.50,\n"
    "short ponytail:1.50,\n"
    "folded ponytail:1.40,\n"
    "twintails:1.50,\n"
    "hair bun:1.40,\n"
    "hair down:1.45,\n"
    "short hair:1.45\n"
    ">"
)

# "short hair" y "medium hair" van como tag de dos palabras a proposito:
# deleteTags los borra por coincidencia exacta del token, que es como los
# escriben las skins. Sin eso el pj de pelo corto pelea con la cola larga.
NUEVOS_TAGS = [
    "ponytail", "twintails", "twintail", "bun", "braid", "braids",
    "updo", "pigtails", "drill", "drills", "dreadlocks", "afro", "hime",
    "short hair", "medium hair",
]

VIEJO_PROMPT = (
    "<(high ponytail:1.70)>,\n"
    "<(blunt bangs:1.70)>,\n"
    "<(straight bangs:1.45)>,\n"
    "(long hair:1.35),\n"
    "(hair tie:1.20),\n"
    "\n"
    "<neg:\n"
    "low ponytail:1.50,\n"
    "side ponytail:1.50,\n"
    "twintails:1.50,\n"
    "hair bun:1.40,\n"
    "side-swept bangs:1.50,\n"
    "swept bangs:1.50,\n"
    "parted bangs:1.50,\n"
    "asymmetrical bangs:1.40,\n"
    "hair down:1.40\n"
    ">"
)

VIEJOS_TAGS = [
    "ponytail", "twintails", "twintail", "bun", "braid", "braids",
    "updo", "sidelocks", "sidelock", "ahoge", "bangs", "fringe",
    "hime", "drill", "drills", "intakes", "pigtails", "dreadlocks",
    "afro", "ribbon", "horns",
]


def _set(apps, prompt, tags):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")

    s = Special.objects.filter(name=NOMBRE).first()
    if s is None:
        return

    s.prompt = prompt
    s.save(update_fields=["prompt"])

    s.tags_deleted.clear()
    for nombre in tags:
        tag, _ = Tag.objects.get_or_create(name=nombre)
        s.tags_deleted.add(tag)


def aplicar(apps, schema_editor):
    _set(apps, NUEVO_PROMPT, NUEVOS_TAGS)


def revertir(apps, schema_editor):
    _set(apps, VIEJO_PROMPT, VIEJOS_TAGS)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0023_hair_tsunade"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
