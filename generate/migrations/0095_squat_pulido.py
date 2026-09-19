from django.db import migrations


SOLO = """(solo:1.45),
(1girl:1.20),

<neg:
multiple girls:1.55,
2girls:1.55,
1boy:1.45,
multiple views:1.60,
zoom layer:1.60
>"""

# Las cuatro que venian de tier2 entraron al grupo Squat- tal cual estaban:
# sin pesos y sin el bloque solo que usan el resto de los grupos de tier1.
# Squat-Refined ademas traia "upright" y "chin_up", que no existen en
# Danbooru (0 posts cada uno); se reemplazan por el squat recatado real.
NUEVOS = {
    "Squat-Spread": "(squatting:1.70),\n(spread legs:1.45)",
    "Squat-Behind": "(squatting:1.70),\n(from behind:1.35),\n(from above:1.25)",
    "Squat-Below": "(squatting:1.70),\n(from below:1.40)",
    "Squat-Refined": (
        "(squatting:1.60),\n(knees together feet apart:1.45),\n"
        "(hand on own thigh:1.35),\n(contrapposto:1.20)"
    ),
}

VIEJOS = {
    "Squat-Spread": "squatting, spread legs",
    "Squat-Behind": "squatting,from behind,from above",
    "Squat-Below": "squatting,from below",
    "Squat-Refined": (
        "(squatting:1.50),(upright:1.35),(chin_up:1.30),"
        "(hand_on_own_thigh:1.35),(contrapposto:1.20)"
    ),
}


def aplicar(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    for nombre, cuerpo in NUEVOS.items():
        Pose.objects.filter(name=nombre).update(prompt=cuerpo + ",\n" + SOLO)


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    for nombre, cuerpo in VIEJOS.items():
        Pose.objects.filter(name=nombre).update(prompt=cuerpo)


class Migration(migrations.Migration):

    dependencies = [("generate", "0094_squat_tier1")]

    operations = [migrations.RunPython(aplicar, revertir)]
