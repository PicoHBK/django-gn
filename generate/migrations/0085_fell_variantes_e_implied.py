from django.db import migrations


# Dos cosas en tier4.
#
# 1. Diez variantes nuevas de Fell-. Las que tenia eran todas del mismo lado
#    -deepthroat, irrumatio, gesture, after- y ninguna cambiaba el cuerpo ni
#    el encuadre. Las nuevas cruzan el acto con la postura:
#
#      ass focus 46.402   from behind 331.090   kneeling 157.620
#      squatting 138.286  all fours 81.054      top-down bottom-up 28.897
#
#    Mas cuatro de la familia propia que faltaban: penis on face (8.657),
#    penis awe (8.344), imminent fellatio (3.486) y testicle sucking (1.901).
#
# 2. El grupo Implied-, que era el que faltaba. Es todo lo sugerido sin
#    mostrar: implied sex (14.434), implied futanari aparte, implied kiss
#    (1.905), implied fellatio (1.977), implied masturbation (1.397),
#    implied pregnancy (1.112), implied paizuri (855) e implied handjob (556).
#
#    Implied-Mast va con bloqueo de solo; el resto con el bloque del hombre.
#
# "implied_anal" no existe, 0 posts, y implied_footjob tiene 148.
NUEVOS = [['Fell-Ass', '(fellatio:1.70),\n(ass focus:1.60),\n(from behind:1.45),\n(ass:1.35),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Fell-Squat', '(fellatio:1.70),\n(squatting:1.60),\n(ass focus:1.45),\n(knees apart:1.20),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Fell-Kneel', '(fellatio:1.70),\n(kneeling:1.60),\n(looking up:1.35),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Fell-TopDown', '(fellatio:1.70),\n(top-down bottom-up:1.60),\n(ass focus:1.50),\n(ass:1.35),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Fell-AllFours', '(fellatio:1.70),\n(all fours:1.60),\n(ass focus:1.50),\n(from behind:1.35),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Fell-Head', "(fellatio:1.70),\n(hand on another's head:1.55),\n(head grab:1.45),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)", '1:1', 'tier4'], ['Fell-Awe', '(penis awe:1.70),\n(fellatio gesture:1.45),\n(looking up:1.30),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Fell-On Face', '(penis on face:1.70),\n(fellatio:1.40),\n(cum on face:1.30),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Fell-Testicle', '(testicle sucking:1.70),\n(fellatio:1.40),\n(testicles:1.35),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Fell-Imminent', '(imminent fellatio:1.70),\n(fellatio gesture:1.45),\n(open mouth:1.30),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Implied-Sex', '(implied sex:1.70),\n(sex:1.30),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Implied-Fellatio', '(implied fellatio:1.70),\n(fellatio gesture:1.40),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Implied-Kiss', '(implied kiss:1.70),\n(imminent kiss:1.40),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Implied-Paizuri', '(implied paizuri:1.70),\n(paizuri:1.35),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Implied-Handjob', '(implied handjob:1.70),\n(handjob:1.35),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4'], ['Implied-Mast', '(implied masturbation:1.70),\n(masturbation:1.35),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '1:1', 'tier4'], ['Implied-Pregnancy', '(implied pregnancy:1.70),\n(pregnant:1.30),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4']]


def aplicar(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")
    tipos = {i.name: i for i in ImageType.objects.all()}
    for nombre, prompt, tipo, tier in NUEVOS:
        if Pose.objects.filter(name=nombre).exists():
            continue
        Pose.objects.create(
            name=nombre, prompt=prompt, tier=tier, img_type=tipos.get(tipo)
        )


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    Pose.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0084_close_acto_y_anal"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
