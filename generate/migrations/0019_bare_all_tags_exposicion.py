from django.db import migrations


# Segunda tanda para AA-Bare All: los descriptores de exposicion parcial, los
# acoples de prenda y los plurales/singulares que faltaban. Son tags que solo
# tienen sentido con ropa puesta, asi que estorban en un render desnudo.
#
# Quedaron fuera a proposito, por colision: "exposure" (mata el lora
# Shirt_lift-_Assisted_exposure), "open", "pull", "lift", "thigh",
# "partially", "undressing", "peek", "naked" y "clothed" se llevan poses.
TAGS_EXPOSICION = [
    # Exposicion parcial: solo describen piel que la ropa deja ver
    'bare', 'underboob', 'exposed',
    # Acoples y aberturas de prenda
    'cutout', 'cutouts', 'detached', 'sheer', 'seethrough', 'crotchless',
    'unbuttoned', 'buttoned', 'unzipped', 'untied', 'undressed',
    'malfunction',
    # Zettai ryouiki (el hueco entre falda y medias)
    'zettai', 'ryouiki',
    # Plurales/singulares que la lista actual no cubre
    'straps', 'panty',
]

SPECIAL = "AA-Bare All"


def agregar(apps, schema_editor):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")

    special = Special.objects.filter(name=SPECIAL).first()
    if special is None:
        return

    for nombre in TAGS_EXPOSICION:
        tag, _ = Tag.objects.get_or_create(name=nombre)
        special.tags_deleted.add(tag)


def quitar(apps, schema_editor):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")

    special = Special.objects.filter(name=SPECIAL).first()
    if special is None:
        return

    # Solo desasocia; los Tag quedan por si otro special los usa.
    special.tags_deleted.remove(*Tag.objects.filter(name__in=TAGS_EXPOSICION))


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0018_bare_all_tags_ropa"),
    ]

    operations = [
        migrations.RunPython(agregar, quitar),
    ]
