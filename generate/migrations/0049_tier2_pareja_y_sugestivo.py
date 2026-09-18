from django.db import migrations


# Tier2: pareja sin nada explicito, y ella sola insinuando.
#
# Pair-  el hombre aparece, asi que el bloque va REFORZADO: faceless male en
#        1.75, faceless 1.70 y bald 1.65, bastante por encima del 1.45/1.35
#        que usan los tiers de arriba. En tier2 se le ve mucho mas la cara
#        porque no hay un acto que la tape.
#
# Sug-   ella sola, con el bloqueo de "solo" y sin hombre. Incluye el
#        fellatio gesture (6.273), que es simular el acto sin que pase nada,
#        y las posturas que insinuan: crawling, bent over, arched back,
#        all fours, top-down bottom-up.
#
# "imminent kiss" cae aca y no en POV: el wiki lo define como el momento
# antes de que DOS PERSONAJES se besen, que es exactamente una pose de
# pareja. Para el beso a la camara esta kissing_viewer, en el grupo POVM.
#
# Ningun tag de expresion: quedo afuera "seductive smile" (15.788) aunque
# encajaba tematicamente. La emocion va por el modulo de Emote.
#
# Entre <> por AA-Bare All: skirt lift, clothes lift y carrying over
# shoulder. Sus palabras -skirt, clothes, shoulder- estan en los
# tags_deleted del special de desnudar.
NUEVAS = [['Pair-Hug', '(hug:1.75),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4', 'tier2'], ['Pair-HugBehind', '(hug from behind:1.80),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '3:4', 'tier2'], ['Pair-Kiss', '(kiss:1.75),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', 'Portrait', 'tier2'], ['Pair-French', '(french kiss:1.80),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', 'Portrait', 'tier2'], ['Pair-Imminent', '(imminent kiss:1.80),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', 'Portrait', 'tier2'], ['Pair-Princess', '(princess carry:1.80),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', 'Full Body', 'tier2'], ['Pair-Carry', '(carrying:1.75),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', 'Full Body', 'tier2'], ['Pair-Piggy', '(piggyback:1.80),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', 'Full Body', 'tier2'], ['Pair-Shoulder', '<(carrying over shoulder:1.80)>,\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', 'Full Body', 'tier2'], ['Pair-Hands', '(holding hands:1.75),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier2'], ['Pair-Dance', '(dancing:1.75),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', 'Full Body', 'tier2'], ['Pair-Face', "(hand on another's face:1.75),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)", 'Portrait', 'tier2'], ['Pair-Headpat', '(headpat:1.75),\n(faceless male:1.75),\n(faceless:1.70),\n(bald:1.65),\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', 'Portrait', 'tier2'], ['Sug-Fell', '(fellatio gesture:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Portrait', 'tier2'], ['Sug-Crawl', '(crawling:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '4:3', 'tier2'], ['Sug-AllFours', '(all fours:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '4:3', 'tier2'], ['Sug-TopDown', '(top-down bottom-up:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '4:3', 'tier2'], ['Sug-Bent', '(bent over:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '4:3', 'tier2'], ['Sug-Arch', '(arched back:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '4:3', 'tier2'], ['Sug-Spread', '(spread legs:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '1:1', 'tier2'], ['Sug-Squat', '(squatting:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier2'], ['Sug-Kneel', '(kneeling:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier2'], ['Sug-Stomach', '(on stomach:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '4:3', 'tier2'], ['Sug-Undress', '(undressing:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier2'], ['Sug-SkirtLift', '<(skirt lift:1.80)>,\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier2'], ['Sug-ClothesLift', '<(clothes lift:1.80)>,\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier2'], ['Sug-Back', '(looking back:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier2']]


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
        ("generate", "0048_sub_domme_y_faltantes"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
