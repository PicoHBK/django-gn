from django.db import migrations


# Los 13 grupos que faltaban, incluidos sumisa y dominante.
#
# "submissive" NO existe como tag en Danbooru: no hay familia de sumision. El
# grupo Sub- se arma indirecto con kneeling (157.604), leash (38.929), collar
# (280.056), pet play, humiliation, bowing y head grab. Para lo contrario si
# hay tags directos: femdom (21.779) y assertive female (18.514).
#
# NINGUN grupo lleva tags de expresion: nada de blush, smug, crying, naughty
# face, torogao ni ahegao. La emocion va por el modulo de Emote.
#
# Cum- era el hueco mas grande: tenia 3 variantes y la familia tiene doce,
# con cum in pussy (144.913) y pussy juice (154.492) entre las mas usadas de
# todo el vocabulario. Las dos que implican penetracion, cum in pussy y cum
# in ass, van a tier5; el resto del grupo queda en tier4.
#
# Tokens entre <> por AA-Bare All: collar, leash, rope y "cum on clothes". Los
# cuatro tienen palabras que estan en los tags_deleted del special de
# desnudar, asi que sin las llaves angulares se los borraba.
NUEVAS = [['Sub-Gen', '(kneeling:1.75),\n(bowing:1.40),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4', 'tier4'], ['Sub-Leash', '<(leash:1.75)>,\n(viewer holding leash:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4', 'tier4'], ['Sub-Collar', '<(collar:1.80)>,\n<(leash:1.50)>,\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4', 'tier4'], ['Sub-Pet', '(pet play:1.80),\n<(collar:1.50)>,\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4', 'tier4'], ['Sub-Humil', '(humiliation:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4', 'tier4'], ['Sub-Head', "(head grab:1.75),\n(hands on another's head:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)", '3:4', 'tier4'], ['Domme-Gen', '(femdom:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4', 'tier4'], ['Domme-Assert', '(assertive female:1.80),\n(femdom:1.50),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4', 'tier4'], ['Domme-Leash', '(holding leash:1.80),\n<(leash:1.60)>,\n(femdom:1.50),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4', 'tier4'], ['Domme-POV', '(viewer on leash:1.80),\n(pov:1.70),\n(femdom:1.50),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4', 'tier4'], ['Cum-Facial', '(facial:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Cum-Mouth', '(cum in mouth:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Cum-Drip', '(cumdrip:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Cum-Ejac', '(ejaculation:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Cum-Hair', '(cum on hair:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Cum-Clothes', '<(cum on clothes:1.80)>,\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Cum-Ass', '(cum on ass:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Cum-Tongue', '(cum on tongue:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Cum-Juice', '(pussy juice:1.75),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Cum-Squirt', '(female ejaculation:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Cum-InPussy', '(cum in pussy:1.85),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier5'], ['Cum-InAss', '(cum in ass:1.85),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier5'], ['Anal-Gen', '(anal:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '4:3', 'tier5'], ['Anal-Cum', '(anal:1.70),\n(cum in ass:1.70),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '4:3', 'tier5'], ['Clothed-Sex', '(clothed sex:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4', 'tier4'], ['Clothed-CFNM', '(clothed female nude male:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4', 'tier4'], ['After-Sex', '(after sex:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['After-Vaginal', '(after vaginal:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['After-Drip', '(after sex:1.60),\n(cumdrip:1.75),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Condom-Gen', '(condom:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Condom-Used', '(used condom:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Oral-Gen', '(oral:1.75),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Oral-Breast', '(breast sucking:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Public-Gen', '(public indecency:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Public-Exhib', '(exhibitionism:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Shibari-Gen', '(shibari:1.85),\n<(rope:1.60)>,\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier5'], ['Lact-Gen', '(lactation:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '1:1', 'tier4']]


def aplicar(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")
    tipos = {i.name: i for i in ImageType.objects.all()}
    for nombre, prompt, tipo, tier in NUEVAS:
        if Pose.objects.filter(name=nombre).exists():
            continue
        Pose.objects.create(
            name=nombre, prompt=prompt, tier=tier, img_type=tipos.get(tipo)
        )


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    Pose.objects.filter(name__in=[n[0] for n in NUEVAS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0047_grupo_hardcore"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
