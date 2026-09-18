from django.db import migrations


# Tier1: lo normal, y ella casi siempre sola. Tres cosas a la vez.
#
# 1. FUGAS. Habia contenido explicito en tier1, que es el tier que el front
#    muestra a todos. Tesk-1 tenia "rough sex, ahegao, fucked from behind" y
#    Tesk-4 "extreme deepthroat". Nueve poses se van al tier que les
#    corresponde. Tesk-8 se queda: matcheaba por "sexy pose", no por sex.
#
# 2. DEDUP. Cuatro poses sueltas que ya hacian lo mismo que un grupo nuevo se
#    pliegan en vez de duplicarse: Do-Cooking, Do-Falling, Contrapposto y
#    Leaning Forward.
#
# 3. GRUPOS. Move-, Look-, Daily-, Arms- y Lean-, todos con el bloqueo de
#    "solo" porque en tier1 ella va sola.
#
# NO se usa el tag "standing" en ningun lado: ya lo pone el ImageType
# "Full Body", que trae "lazypos, standing, (full body:1.5)" en su prompt.
#
# "against wall" tampoco, porque ya existe el grupo de posicion Wall-.
NUEVAS = [['Move-Walk', '(walking:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Full Body', 'tier1'], ['Move-Run', '(running:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Full Body', 'tier1'], ['Move-Jump', '(jumping:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Full Body', 'tier1'], ['Move-Stretch', '(stretching:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Full Body', 'tier1'], ['Move-Float', '(floating:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Full Body', 'tier1'], ['Move-Fly', '(flying:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Full Body', 'tier1'], ['Move-Swim', '(swimming:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Full Body', 'tier1'], ['Look-Peek', '(peeking:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Portrait', 'tier1'], ['Look-PeekOut', '(peeking out:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Portrait', 'tier1'], ['Look-Up', '(looking up:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Portrait', 'tier1'], ['Look-Down', '(looking down:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Portrait', 'tier1'], ['Look-Away', '(looking away:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Portrait', 'tier1'], ['Look-Side', '(looking to the side:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', 'Portrait', 'tier1'], ['Daily-Eat', '(eating:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Daily-Drink', '(drinking:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Daily-Read', '(reading:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Daily-Sleep', '(sleeping:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Daily-Yawn', '(yawning:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Daily-Phone', '(holding phone:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Daily-Selfie', '(selfie:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Daily-Umbrella', '(holding umbrella:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Arms-Up', '(arms up:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Arms-Behind', '(arms behind back:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Arms-Head', '(arms behind head:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Arms-Crossed', '(crossed arms:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Arms-Wave', '(waving:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Arms-Point', '(pointing:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Arms-Salute', '(salute:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Lean-Back', '(leaning back:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Lean-Sit', '(sitting:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Lean-Bed', '(on bed:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1'], ['Lean-Chair', '(on chair:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier1']]

PLEGAR = [[580, 'Do-Cooking', 'Daily-Cook'], [554, 'Do-Falling', 'Move-Fall'], [777, 'Contrapposto', 'Lean-Contra'], [719, 'Leaning Forward', 'Lean-Forward']]

FUGAS = [[601, 'Hugg-Face in AS', 'tier5', 'tier1'], [793, 'Tesk-1', 'tier5', 'tier1'], [636, 'Sit-FaceSitting', 'tier4', 'tier1'], [794, 'Tesk-2', 'tier4', 'tier1'], [796, 'Tesk-4', 'tier4', 'tier1'], [802, 'Tesk-10', 'tier4', 'tier1'], [804, 'Tesk-12', 'tier4', 'tier1'], [688, 'Breast Smother', 'tier2', 'tier1'], [712, 'Yoga-Body Brige Front', 'tier2', 'tier1']]


def aplicar(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")
    tipos = {i.name: i for i in ImageType.objects.all()}

    for pk, _viejo, nuevo in PLEGAR:
        p = Pose.objects.filter(pk=pk).first()
        if p is not None:
            p.name = nuevo
            p.save(update_fields=["name"])

    for pk, _n, nuevo_tier, _viejo_tier in FUGAS:
        p = Pose.objects.filter(pk=pk).first()
        if p is not None:
            p.tier = nuevo_tier
            p.save(update_fields=["tier"])

    for nombre, prompt, tipo, tier in NUEVAS:
        if Pose.objects.filter(name=nombre).exists():
            continue
        Pose.objects.create(
            name=nombre, prompt=prompt, tier=tier, img_type=tipos.get(tipo)
        )


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")

    Pose.objects.filter(name__in=[n[0] for n in NUEVAS]).delete()

    for pk, viejo, _nuevo in PLEGAR:
        p = Pose.objects.filter(pk=pk).first()
        if p is not None:
            p.name = viejo
            p.save(update_fields=["name"])

    for pk, _n, _nuevo_tier, viejo_tier in FUGAS:
        p = Pose.objects.filter(pk=pk).first()
        if p is not None:
            p.tier = viejo_tier
            p.save(update_fields=["tier"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0049_tier2_pareja_y_sugestivo"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
