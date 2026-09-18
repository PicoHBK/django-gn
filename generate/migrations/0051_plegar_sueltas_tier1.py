from django.db import migrations


# Plegado de las poses sueltas de tier1 a los grupos que ya existen. 82 de 89.
#
# Las que llevan hombre se van a tier2 junto a Pair-, porque tier1 quedo
# definido como "ella casi siempre sola": los Kiss-*, Hugg-*, Carrying-*,
# Lap-*, Whispering y Proposal.
#
# Las normales se pliegan a Move-, Lean-, Look-, Arms- y Daily- en tier1, y
# las que insinuan a Sug- en tier2: Crawling-Front (que duplicaba a
# Sug-Crawl), Lying-Spread, Sit-Spread Legs, Tesk y Tesk-8.
#
# El sufijo dice de donde viene: -L1, -L2 para las que traen LORA, -V1, -V2
# para las que no. Asi en el front se ve cual es la version entrenada.
#
# Quedan 7 sueltas a proposito, cada una por un motivo:
#   397 Aaa            es "no person, landscape", una utilidad, no una pose
#   678 Lotus          "lotus position" es pose de yoga Y posicion sexual, y
#                      el prompt trae dark-skin male: hay que decidirlo a mano
#   710 Wrestiling     "head between thighs", no esta claro si es tier2 o 4
#   694, 728           loras de personaje especifico, no de pose
#   734 MaD            trae "child" en el prompt, no lo toco sin que lo mires
#   798 Tesk-6         dice "topless", hay que revisar si va a tier1
MOVER = [[418, 'Carrying', 'Pair-Princess-V1', 'tier2'], [563, 'Carrying-AS-UP', 'Pair-Shoulder-L1', 'tier2'], [660, 'Carrying-Piggyback', 'Pair-Piggy-L1', 'tier2'], [581, 'Carrying-RUN', 'Pair-Carry-V1', 'tier2'], [677, 'Carrying-Pov', 'Pair-Princess-L1', 'tier2'], [449, 'Hand-HeadPat', 'Pair-Headpat-V1', 'tier2'], [763, 'Hugg-CryGirl', 'Pair-Hug-L1', 'tier2'], [566, 'Hugg-From Behind', 'Pair-HugBehind-V1', 'tier2'], [548, 'Hugg-From Side', 'Pair-Hug-V1', 'tier2'], [697, 'Hugg-Jump Inc', 'Pair-Hug-L2', 'tier2'], [676, 'Hugg-Lora 2', 'Pair-Hug-L3', 'tier2'], [675, 'Hugg-Lora-1', 'Pair-HugBehind-L1', 'tier2'], [466, 'Kiss-After', 'Pair-Kiss-L1', 'tier2'], [467, 'Kiss-French', 'Pair-French-L1', 'tier2'], [468, 'Kiss-Imminent', 'Pair-Imminent-L1', 'tier2'], [469, 'Kiss-Implied', 'Pair-Kiss-L2', 'tier2'], [715, 'Kiss-Mejil', 'Pair-Kiss-L3', 'tier2'], [350, 'Kiss-N', 'Pair-Kiss-L4', 'tier2'], [470, 'Kiss-Sloppysmooch', 'Pair-French-L2', 'tier2'], [760, 'Kiss-Surprised', 'Pair-Kiss-V1', 'tier2'], [790, 'Test KISS', 'Pair-Kiss-V2', 'tier2'], [654, 'Lap Pillow', 'Pair-Lap-V1', 'tier2'], [709, 'Lap-Lora', 'Pair-Lap-L1', 'tier2'], [655, 'Lap-Sitting Woman in Male', 'Pair-Lap-V2', 'tier2'], [695, 'LeaningOnPerson-v1', 'Pair-Lean-L1', 'tier2'], [613, 'Lying-OnAnother', 'Pair-Lying-V1', 'tier2'], [558, 'Proposal-From Side', 'Pair-Proposal-V1', 'tier2'], [727, 'Proposal-Final', 'Pair-Proposal-L1', 'tier2'], [805, 'Tesk-13', 'Pair-Sofa-V1', 'tier2'], [806, 'Tesk-14', 'Pair-Sofa-L1', 'tier2'], [768, 'Whispering', 'Pair-Whisper-V1', 'tier2'], [668, 'Whispering-L', 'Pair-Whisper-L1', 'tier2'], [577, 'Do-Fight-Kick', 'Pair-Fight-L1', 'tier2'], [451, 'Running', 'Move-Run-V1', 'tier1'], [453, 'Running-From Behind', 'Move-Run-Behind', 'tier1'], [452, 'Running-From Side', 'Move-Run-Side', 'tier1'], [611, 'Walking-From Behind', 'Move-Walk-Behind', 'tier1'], [381, 'Walking-From Side', 'Move-Walk-Side', 'tier1'], [586, 'Leg Lift', 'Move-LegLift', 'tier1'], [587, 'Leg Lift-Behind', 'Move-LegLift-Behind', 'tier1'], [634, 'Yoga-2', 'Move-Yoga-L1', 'tier1'], [635, 'Yoga-3', 'Move-Yoga-L2', 'tier1'], [711, 'Yoga-Body Brige', 'Move-Yoga-L3', 'tier1'], [643, 'CobraPose-From Side', 'Move-Cobra-L1', 'tier1'], [644, 'CobraPose-Front', 'Move-Cobra-L2', 'tier1'], [640, 'DownWard-From Behind', 'Move-Dog-Behind', 'tier1'], [639, 'DownWard-From Side', 'Move-Dog-Side', 'tier1'], [641, 'DownWard-Front', 'Move-Dog-Front', 'tier1'], [351, 'Sit', 'Lean-Sit-V1', 'tier1'], [699, 'Sit-Wariza', 'Lean-Sit-Wariza', 'tier1'], [702, 'SeizaWariza-Sei Front', 'Lean-Sit-Seiza', 'tier1'], [807, 'Sofa-Sittting', 'Lean-Sofa', 'tier1'], [669, 'Chair-Sit Front', 'Lean-Chair-L1', 'tier1'], [670, 'Chair-Sit Back', 'Lean-Chair-L2', 'tier1'], [671, 'Chair-Sit Strad Back', 'Lean-Chair-L3', 'tier1'], [672, 'Chair-Sit Strad Front', 'Lean-Chair-L4', 'tier1'], [673, 'Chair-Sit Strad Side', 'Lean-Chair-L5', 'tier1'], [352, 'Lying', 'Lean-Lying-V1', 'tier1'], [569, 'Lying-Back-From above', 'Lean-Lying-Above', 'tier1'], [825, 'Lying-Hand on Hips', 'Lean-Lying-Hips', 'tier1'], [557, 'Lying-on Stomach', 'Lean-Lying-Stomach', 'tier1'], [674, 'Lying-Back Lora', 'Lean-Lying-L1', 'tier1'], [461, 'Kneeling-Front', 'Lean-Kneel-V1', 'tier1'], [555, 'Kneeling-From Behind', 'Lean-Kneel-Behind', 'tier1'], [556, 'Kneeling-From Below', 'Lean-Kneel-Below', 'tier1'], [549, 'Do-Dogeza', 'Lean-Dogeza', 'tier1'], [519, 'Peeking Out', 'Look-PeekOut-V1', 'tier1'], [658, 'Looking Down v2', 'Look-Down-L1', 'tier1'], [659, 'Looking Down v3', 'Look-Down-L2', 'tier1'], [348, 'Side', 'Look-Side-V1', 'tier1'], [716, 'Pointing-At the viewer', 'Arms-Point-V1', 'tier1'], [553, 'Reaching Hand', 'Arms-Reach', 'tier1'], [736, 'Hmps', 'Arms-Self', 'tier1'], [692, 'Drunking', 'Daily-Drunk-L1', 'tier1'], [656, 'Regrigerator Search', 'Daily-Fridge-L1', 'tier1'], [754, 'Open Door', 'Daily-Door', 'tier1'], [612, 'Crawling-Front', 'Sug-Crawl-V1', 'tier2'], [457, 'Sit-Spread Legs', 'Sug-Spread-V1', 'tier2'], [413, 'Lying-Spread', 'Sug-Spread-V2', 'tier2'], [792, 'Tesk', 'Sug-Bent-V1', 'tier2'], [800, 'Tesk-8', 'Sug-Sexy', 'tier2'], [465, 'Income-Kiss', 'Sug-Kiss-L1', 'tier2']]


def _set(apps, indice_nombre, indice_tier):
    Pose = apps.get_model("generate", "Pose")
    for cambio in MOVER:
        p = Pose.objects.filter(pk=cambio[0]).first()
        if p is None:
            continue
        p.name = cambio[indice_nombre]
        p.tier = cambio[indice_tier] if indice_tier else "tier1"
        p.save(update_fields=["name", "tier"])


def aplicar(apps, schema_editor):
    _set(apps, 2, 3)


def revertir(apps, schema_editor):
    _set(apps, 1, None)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0050_tier1_normal_y_fugas"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
