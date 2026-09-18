from django.db import migrations


# Hair-Bun: pelo recogido entero hacia atras con un rodete, nada suelto.
#
# Los tokens propios van entre <> por la misma razon que en Hair-Ponytail:
# el special se borra "bun" a si mismo para quitarle al personaje sus rodetes
# (double bun, bun cover), asi que el nuestro tiene que quedar fuera del
# alcance de deleteTags.
NUEVO = {
    "name": "Hair-Bun",
    "tier": "tier1",
    "prompt": (
        "<(hair bun:1.70)>,\n"
        "<(single hair bun:1.60)>,\n"
        "(hair pulled back:1.50),\n"
        "(slicked back hair:1.40),\n"
        "(hair up:1.35),\n"
        "(forehead:1.30),\n"
        "\n"
        "<neg:\n"
        "hair down:1.50,\n"
        "loose hair:1.50,\n"
        "double bun:1.45,\n"
        "twintails:1.50,\n"
        "ponytail:1.45,\n"
        "bangs:1.45,\n"
        "sidelocks:1.40,\n"
        "hair over one eye:1.40,\n"
        "messy hair:1.40,\n"
        "hair between eyes:1.30\n"
        ">"
    ),
    "del": [
        "bun", "ponytail", "twintails", "twintail", "braid", "braids",
        "updo", "sidelocks", "sidelock", "ahoge", "bangs", "fringe",
        "hime", "drill", "drills", "intakes", "pigtails", "dreadlocks",
        "afro", "ribbon", "horns",
    ],
}


def aplicar(apps, schema_editor):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")

    if Special.objects.filter(name=NUEVO["name"]).exists():
        return

    nuevo = Special.objects.create(
        name=NUEVO["name"], tier=NUEVO["tier"], prompt=NUEVO["prompt"]
    )
    for nombre in NUEVO["del"]:
        tag, _ = Tag.objects.get_or_create(name=nombre)
        nuevo.tags_deleted.add(tag)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name=NUEVO["name"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0021_hair_ponytail_y_limpieza"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
