from django.db import migrations


# Hair-Tsunade: el flequillo que se levanta en arco y cae a los costados de la
# frente. En Danbooru el tag es "curtained hair" (no "hair intakes", que son
# los scoops que nacen arriba de la cabeza). Sale en 122 de los 2.472 posts de
# Tsunade, unas 9 veces mas de lo que le tocaria por frecuencia: es el rasgo
# que la define, y por eso el special lleva su nombre.
#
# Los tokens propios van entre <> porque el special se borra "bangs" a si
# mismo para quitarle al personaje el flequillo que traiga.
#
# El negativo NO lleva "forehead": la marca de Tsunade es un forehead_mark y
# negar la frente se la apagaria.
NUEVO = {
    "name": "Hair-Tsunade",
    "tier": "tier1",
    "prompt": (
        "<(curtained hair:1.70)>,\n"
        "<(parted bangs:1.55)>,\n"
        "(center part:1.40),\n"
        "(hair framing face:1.35),\n"
        "(long hair:1.25),\n"
        "\n"
        "<neg:\n"
        "blunt bangs:1.50,\n"
        "straight bangs:1.45,\n"
        "hair intakes:1.45,\n"
        "swept bangs:1.40,\n"
        "asymmetrical bangs:1.40,\n"
        "hair over one eye:1.40\n"
        ">"
    ),
    "del": [
        "bangs", "fringe", "ponytail", "twintails", "twintail", "bun",
        "braid", "braids", "updo", "sidelocks", "sidelock", "ahoge",
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
        ("generate", "0022_hair_bun"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
