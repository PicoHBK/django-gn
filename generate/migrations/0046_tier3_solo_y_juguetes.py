from django.db import migrations


# Tier3: solo y juguetes. Obsceno pero sin partner, que es lo que lo separa
# de tier4 (actos de a dos sin penetracion) y tier5 (penetracion).
#
# Mast- pasa entero a tier3 y es SOLO de mujer: lleva el bloqueo de "solo"
# con su negativo, sin bloque del hombre.
#
# MastM- es la de el, y por eso va siempre con (pov:1.70): si no se ve desde
# su punto de vista, no entra en tier3.
#
# Correcciones de la tanda anterior, que habian quedado mal clasificadas:
#   Mast-L3 y Mast-L5 -> Dildo-L1/L2. Son dildo riding con LORA propio, no
#       masturbacion a mano.
#   Mast-L1 y Mast-L4 -> Mutual-L1/L2. Son mutual masturbation, o sea de a
#       dos, asi que no son solo y se quedan en tier4.
#   Mast-L2 -> MastM-L1. Es male masturbation con male pov.
#   "Riding-Dil Behong" -> Dildo-R1. Estaba en tier1, o sea el front se lo
#       mostraba a cualquiera.
#   MAST-1, MAST-3, MAST-Leaning Back y MAST-Wet pant -> Mast-V1/V2/V3 y
#       Mast-E2. Eran masturbacion femenina en tier5, y ademas el prefijo en
#       mayuscula convivia con Mast- en el front como si fueran dos grupos.
#
# "fingering" entra aca como Mast-Fing: en solitario es masturbacion. El
# fingering asistido o de a dos sigue siendo tier5.
NUEVAS = [['Mast-Clothes', '(masturbation through clothes:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Mast-Under', '(masturbation under clothes:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Mast-Implied', '(implied masturbation:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Mast-After', '(after masturbation:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Mast-Public', '(public masturbation:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Mast-Fing', '(fingering:1.70),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['MastM-POV', '(male masturbation:1.75),\n(pov:1.70),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(1boy:1.20)', '1:1', 'tier3'], ['Dildo-Gen', '(dildo:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Dildo-Riding', '(dildo riding:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Dildo-Huge', '(huge dildo:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Dildo-Double', '(double dildo:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Dildo-Clothes', '(dildo under clothes:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Dildo-Panties', '(dildo under panties:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Vib-Gen', '(vibrator:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Vib-Remote', '(remote control vibrator:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Vib-Egg', '(egg vibrator:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Vib-Clothes', '(vibrator under clothes:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Vib-Panties', '(vibrator under panties:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Vib-Thighhighs', '(vibrator in thighhighs:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Vib-Nipple', '(vibrator on nipple:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '3:4', 'tier3'], ['Toy-Gen', '(sex toy:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '1:1', 'tier3'], ['Toy-Anal', '(anal beads:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '1:1', 'tier3'], ['Toy-Wand', '(hitachi magic wand:1.80),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '1:1', 'tier3'], ['Insert-Gen', '(object insertion:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '1:1', 'tier3'], ['Insert-Vaginal', '(vaginal object insertion:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '1:1', 'tier3'], ['Insert-Anal', '(anal object insertion:1.75),\n(solo:1.45),\n(1girl:1.20),\n\n<neg:\nmultiple girls:1.55,\n2girls:1.55,\n1boy:1.45,\nmultiple views:1.60,\nzoom layer:1.60\n>', '1:1', 'tier3'], ['Mutual-Gen', '(mutual masturbation:1.80),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1', 'tier4']]

MOVER = [[500, 'Mast-E2', 'tier3'], [383, 'Mast-V1', 'tier3'], [813, 'Mast-V2', 'tier3'], [571, 'Mast-V3', 'tier3'], [425, 'MastM-L1', 'tier3'], [537, 'Dildo-L1', 'tier3'], [820, 'Dildo-L2', 'tier3'], [756, 'Dildo-R1', 'tier3'], [385, 'Mutual-L1', 'tier4'], [540, 'Mutual-L2', 'tier4']]

A_TIER3 = ['Mast-Gen', 'Mast-Female', 'Mast-E1']


def aplicar(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")
    tipos = {i.name: i for i in ImageType.objects.all()}

    for pk, nuevo, tier in MOVER:
        p = Pose.objects.filter(pk=pk).first()
        if p is None:
            continue
        p.name, p.tier = nuevo, tier
        p.save(update_fields=["name", "tier"])

    Pose.objects.filter(name__in=A_TIER3).update(tier="tier3")

    for nombre, prompt, tipo, tier in NUEVAS:
        if Pose.objects.filter(name=nombre).exists():
            continue
        Pose.objects.create(
            name=nombre, prompt=prompt, tier=tier, img_type=tipos.get(tipo)
        )


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")

    Pose.objects.filter(name__in=[n[0] for n in NUEVAS]).delete()
    Pose.objects.filter(name__in=A_TIER3).update(tier="tier4")

    viejos = {425: ("Mast-L2", "tier4"), 537: ("Mast-L3", "tier4"),
              820: ("Mast-L5", "tier4"), 756: ("Riding-Dil Behong", "tier1"),
              385: ("Mast-L1", "tier4"), 540: ("Mast-L4", "tier4"),
              500: ("MAST-Leaning Back", "tier5"), 383: ("MAST-1", "tier5"),
              813: ("MAST-3", "tier5"), 571: ("MAST-Wet pant", "tier5")}
    for pk, (nombre, tier) in viejos.items():
        p = Pose.objects.filter(pk=pk).first()
        if p is None:
            continue
        p.name, p.tier = nombre, tier
        p.save(update_fields=["name", "tier"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0045_grupos_de_actos"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
