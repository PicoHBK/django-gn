from django.db import migrations


# Deja la familia de pelo en tres: Hair-Blunt (857), Hair-One Eye (858) y este
# Hair-Ponytail nuevo, que combina cola alta con blunt bangs.
#
# Convencion, la misma de Hair-Blunt:
#   <(tag:peso)>  el tag principal va entre <> para que no lo alcancen los
#                 tags_deleted. deleteTags() compara palabra completa y trata
#                 aparte lo que abre "(" y cierra ")"; envuelto en <> ninguna
#                 de las dos reglas lo toca. Es lo que permite borrar
#                 "ponytail" y "bangs" del personaje sin borrar los nuestros.
#   <neg:...>     rivales con peso, que extract_neg_prompt manda al negativo.
#   tags_deleted  peinados que traiga el pj y que deben desaparecer.
NUEVO = {
    "name": "Hair-Ponytail",
    "tier": "tier1",
    "prompt": (
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
    ),
    # Sin "ponytail" propio en riesgo: el nuestro va entre <>.
    "del": [
        "ponytail", "twintails", "twintail", "bun", "braid", "braids",
        "updo", "sidelocks", "sidelock", "ahoge", "bangs", "fringe",
        "hime", "drill", "drills", "intakes", "pigtails", "dreadlocks",
        "afro", "ribbon", "horns",
    ],
}

# Los viejos de pelo que se van. Se guardan enteros para poder revertir.
BORRAR = [
    (
        "Hair-Ponytail", "tier1",
        "high ponytail,ponytail,<neg:side locks,sideburns,hair flaps>", [],
    ),
    (
        "Blun Bangs Hair", "tier1",
        "<(blunt bangs:1.2)>,(long hair:1.3),straight hair ,"
        "<neg:(horn hair,hair bun,cow horns )>",
        ["horns", "bun", "ribbon", "ponytail"],
    ),
    ("Hair-Ahoge", "tier1", "ahoge", []),
    (
        "Hair-Jess", "tier1",
        "long_hair, wavy_hair, side_part, hair_over_one_eye, "
        "over_one_shoulder, red_hair, voluminous_hair", [],
    ),
    (
        "Hair-Super Pony", "tier1",
        "<lora:super_ponytail_illst:.9>,super high ponytail, superp0nytail, "
        "high ponytail, top ponytail, long ponytail", [],
    ),
]


def aplicar(apps, schema_editor):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")

    # Primero los viejos: el 471 se llama igual que el nuevo y
    # validate_special() resuelve por nombre con .first(), asi que si
    # convivieran ganaria el de pk menor.
    for nombre, _tier, _prompt, _tags in BORRAR:
        Special.objects.filter(name=nombre).delete()

    nuevo = Special.objects.create(
        name=NUEVO["name"], tier=NUEVO["tier"], prompt=NUEVO["prompt"]
    )
    for nombre in NUEVO["del"]:
        tag, _ = Tag.objects.get_or_create(name=nombre)
        nuevo.tags_deleted.add(tag)


def revertir(apps, schema_editor):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")

    Special.objects.filter(name=NUEVO["name"]).delete()

    for nombre, tier, prompt, tags in BORRAR:
        s = Special.objects.create(name=nombre, tier=tier, prompt=prompt)
        for t in tags:
            tag, _ = Tag.objects.get_or_create(name=t)
            s.tags_deleted.add(tag)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0020_bare_all_tags_danbooru"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
