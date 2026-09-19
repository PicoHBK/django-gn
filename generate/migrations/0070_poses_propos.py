from django.db import migrations


# Grupo Propos-: pedida de casamiento, tier2.
#
# "marriage_proposal" existe como tag propio (1.346 posts) y es el que manda
# en casi todas. Lo acompañan wedding ring (21.643), holding ring (780),
# ring box (661), bouquet (42.746) y bridal veil (22.447).
#
# Ojo: "one_knee" NO existe en Danbooru, que es la pose clasica de la pedida.
# Se arma con kneeling (157.610). Tampoco existen engagement_ring,
# wedding_band, love_confession ni "proposal" a secas.
#
# Propos-Bride y Propos-Bouquet van con bloqueo de solo: son ella sola. El
# resto lleva el bloque del hombre reforzado de tier2, con faceless male en
# 1.75, porque aca se le ve la cara mas que en ningun otro grupo.
#
# "bridal veil" y "wedding dress" van entre <> en las tres que los usan:
# veil y dress estan en los tags_deleted de AA-Bare All, y las poses entran
# ANTES que los specials, asi que ahi si las alcanza el borrado -al reves de
# lo que pasa con los BD-, que entran despues-.
#
# Se pliegan al grupo las dos que ya existian sueltas en Pair-.
NUEVAS = [['Propos-Gen', '(marriage proposal:1.80),\n(kneeling:1.50),\n(holding ring:1.45),\n(ring box:1.35),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4'], ['Propos-POV', '(marriage proposal:1.75),\n(pov:1.70),\n(holding ring:1.55),\n(ring box:1.40),\n(pov hands:1.35),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['Propos-Kneel', '(kneeling:1.70),\n(marriage proposal:1.65),\n(ring box:1.40),\n(looking up:1.30),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', 'Full Body'], ['Propos-Ring', '(wedding ring:1.70),\n(holding ring:1.60),\n(interlocked fingers:1.45),\n(holding hands:1.40),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['Propos-Accept', '(happy tears:1.60),\n(marriage proposal:1.55),\n(holding hands:1.45),\n(wedding ring:1.40),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', 'Portrait'], ['Propos-Side', '(marriage proposal:1.70),\n(from side:1.60),\n(kneeling:1.45),\n(holding ring:1.40),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '4:3'], ['Propos-Above', '(marriage proposal:1.70),\n(from above:1.60),\n(kneeling:1.45),\n(ring box:1.35),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['Propos-Church', '(wedding:1.70),\n(church:1.55),\n<(bridal veil:1.45)>,\n(indoors:1.30),\n(stained glass:1.25),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4'], ['Propos-Bride', '(bride:1.70),\n<(wedding dress:1.60)>,\n<(bridal veil:1.50)>,\n(holding bouquet:1.40),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Full Body'], ['Propos-Bouquet', '(holding bouquet:1.70),\n(bouquet:1.55),\n<(bridal veil:1.40)>,\n<(wedding dress:1.35)>,\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4']]

MOVER = {'Pair-Proposal-V1': 'Propos-V1', 'Pair-Proposal-L1': 'Propos-L1'}


def aplicar(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")
    tipos = {i.name: i for i in ImageType.objects.all()}
    for viejo, nuevo in MOVER.items():
        p = Pose.objects.filter(name=viejo).first()
        if p is not None:
            p.name = nuevo
            p.save(update_fields=["name"])
    for nombre, prompt, tipo in NUEVAS:
        if Pose.objects.filter(name=nombre).exists():
            continue
        Pose.objects.create(
            name=nombre, prompt=prompt, tier="tier2", img_type=tipos.get(tipo)
        )


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    Pose.objects.filter(name__in=[n[0] for n in NUEVAS]).delete()
    for viejo, nuevo in MOVER.items():
        p = Pose.objects.filter(name=nuevo).first()
        if p is not None:
            p.name = viejo
            p.save(update_fields=["name"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0069_bg_time"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
