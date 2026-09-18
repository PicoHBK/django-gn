from django.db import migrations


# Grupo HC (hardcore), tier5. No existia: es lo mas fuerte del catalogo y
# tiene que quedar fuera del front, ruteado al otro back.
#
# 23 variantes en cuatro familias, con los posts de Danbooru al lado:
#
#   intensidad  rough sex (4.751), ahegao (28.708), rolling eyes (23.286),
#               fucked silly (10.635), cum overflow (41.151), sex machine
#   multiples   group sex (83.133), threesome (44.272), gangbang (25.033),
#               ffm/mmf threesome (18.758/18.502), double penetration
#               (14.598), orgy (8.813), spitroast (6.934), triple (1.882)
#   interno     x-ray (17.584), cross-section (18.690), stomach bulge
#               (16.997), internal cumshot (12.600), cervix (4.691)
#   sujecion    bdsm (88.424), bondage (74.541), restrained (70.864),
#               bound wrists (30.146), tentacle sex (14.986)
#
# El bloque del hombre va en dos sabores: las de un hombre llevan
# (1boy:1.20), y las de varios lo cambian por (multiple boys:1.35), porque
# 1boy le pelearia al gangbang o a la orgia. HC-Tentacle no lleva hombre.
#
# "(rope:1.50)" de HC-Bondage va entre <> a proposito: "rope" esta en los
# tags_deleted de AA-Bare All, asi que sin las llaves angulares el special de
# desnudar le borraba la soga. Es el mismo truco que usan los specials de pelo.
#
# No se le puso "torn clothes" a HC-Rough por lo mismo: AA-Bare All se lleva
# ese token entero, y ademas el pj ya esta desnudo.
NUEVAS = [['HC-Gen', '(rough sex:1.80),\n(sex:1.40),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['HC-Rough', '(rough sex:1.85),\n(sweat:1.20),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['HC-Ahegao', '(ahegao:1.80),\n(rolling eyes:1.60),\n(tongue out:1.40),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['HC-Silly', '(fucked silly:1.85),\n(ahegao:1.50),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['HC-Cum', '(cum overflow:1.80),\n(excessive cum:1.70),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['HC-Machine', '(sex machine:1.85),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4'], ['HC-Group', '(group sex:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(multiple boys:1.35),\n(1girl:1.25)', '4:3'], ['HC-Threesome', '(threesome:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(multiple boys:1.35),\n(1girl:1.25)', '4:3'], ['HC-MMF', '(mmf threesome:1.80),\n(threesome:1.50),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(multiple boys:1.35),\n(1girl:1.25)', '4:3'], ['HC-FFM', '(ffm threesome:1.80),\n(threesome:1.50),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(multiple boys:1.35),\n(1girl:1.25)', '4:3'], ['HC-Gangbang', '(gangbang:1.85),\n(group sex:1.50),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(multiple boys:1.35),\n(1girl:1.25)', '4:3'], ['HC-Orgy', '(orgy:1.85),\n(group sex:1.50),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(multiple boys:1.35),\n(1girl:1.25)', '4:3'], ['HC-Spitroast', '(spitroast:1.85),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(multiple boys:1.35),\n(1girl:1.25)', '4:3'], ['HC-DP', '(double penetration:1.85),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(multiple boys:1.35),\n(1girl:1.25)', '1:1'], ['HC-TP', '(triple penetration:1.85),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(multiple boys:1.35),\n(1girl:1.25)', '1:1'], ['HC-Xray', '(x-ray:1.80),\n(cross-section:1.70),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['HC-Bulge', '(stomach bulge:1.85),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['HC-Internal', '(internal cumshot:1.80),\n(cum in pussy:1.50),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['HC-Cervix', '(cervix:1.85),\n(uterus:1.60),\n(cross-section:1.50),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['HC-Bdsm', '(bdsm:1.80),\n(restrained:1.50),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4'], ['HC-Bondage', '(bondage:1.80),\n<(rope:1.50)>,\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4'], ['HC-Restrained', '(restrained:1.80),\n(bound wrists:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4'], ['HC-Tentacle', '(tentacle sex:1.85),\n(tentacles:1.60),\n(1girl:1.25)', '3:4']]


def aplicar(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")
    tipos = {i.name: i for i in ImageType.objects.all()}
    for nombre, prompt, tipo in NUEVAS:
        if Pose.objects.filter(name=nombre).exists():
            continue
        Pose.objects.create(
            name=nombre, prompt=prompt, tier="tier5", img_type=tipos.get(tipo)
        )


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    Pose.objects.filter(name__in=[n[0] for n in NUEVAS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0046_tier3_solo_y_juguetes"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
