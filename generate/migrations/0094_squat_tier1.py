from django.db import migrations


# Las poses de squatting "planas" (la persona en cuclillas, sola) se van a
# tier1. Las que tienen "squat" en el prompt pero son posiciones sexuales
# (SquatCowgirl-*, RevSquatCowgirl-*, Fell-Squat, Dildo-*, Impli-*, Immi-*,
# MASTA-SQUAT, Doggy-L2) se quedan en su tier: solo comparten la palabra.
RENOMBRAR = {
    "Squatting-Angle": "Squat-Spread",
    "Squatting-From Behind": "Squat-Behind",
    "Squatting-From Below": "Squat-Below",
    "RollBack-Squatting Refined": "Squat-Refined",
}

# Estas pasan a tier1 (las renombradas + Sug-Squat, que se queda con su
# nombre porque pertenece al grupo Sug-).
A_TIER1 = list(RENOMBRAR.values()) + ["Sug-Squat"]

SOLO = """(solo:1.45),
(1girl:1.20),

<neg:
multiple girls:1.55,
2girls:1.55,
1boy:1.45,
multiple views:1.60,
zoom layer:1.60
>"""

NUEVAS = [
    ("Squat-Gen", "(squatting:1.75)"),
    ("Squat-M", "(squatting:1.60),\n(m legs:1.70),\n(spread legs:1.40)"),
    ("Squat-Knees", "(squatting:1.65),\n(knees together feet apart:1.70)"),
    ("Squat-Hold", "(squatting:1.60),\n(holding own leg:1.70),\n(spread legs:1.35)"),
    ("Squat-Hug", "(squatting:1.60),\n(hugging own legs:1.70),\n(knees up:1.30)"),
    ("Squat-Arms", "(squatting:1.60),\n(arms between legs:1.70)"),
    ("Squat-Knee Up", "(squatting:1.60),\n(knee up:1.65),\n(leg lift:1.35)"),
    ("Squat-Legs Up", "(squatting:1.55),\n(legs up:1.70),\n(spread legs:1.40)"),
    ("Squat-One Knee", "(on one knee:1.75),\n(kneeling:1.40)"),
    ("Squat-Fetal", "(fetal position:1.75),\n(hugging own legs:1.45)"),
    ("Squat-Crossed", "(sitting:1.45),\n(crossed legs:1.70),\n(indian style:1.45)"),
    ("Squat-Wariza", "(wariza:1.75),\n(sitting:1.40)"),
    ("Squat-Yokozuwari", "(yokozuwari:1.75),\n(sitting:1.40)"),
    ("Squat-Seiza", "(seiza:1.75),\n(sitting:1.40)"),
]

# "knees apart" no existe en Danbooru (0 posts): el token estaba muerto.
FIX_MUERTO = [("Fell-Squat", "(knees apart:1.20)", "(knees together feet apart:1.30)")]


def aplicar(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    ImageType = apps.get_model("generate", "ImageType")

    for viejo, nuevo in RENOMBRAR.items():
        Pose.objects.filter(name=viejo).update(name=nuevo)

    Pose.objects.filter(name__in=A_TIER1).update(tier="tier1")

    it = ImageType.objects.filter(name__icontains="full body").first()
    for nombre, cuerpo in NUEVAS:
        Pose.objects.update_or_create(
            name=nombre,
            defaults={"prompt": cuerpo + ",\n" + SOLO, "tier": "tier1", "img_type": it},
        )

    for nombre, viejo, nuevo in FIX_MUERTO:
        for p in Pose.objects.filter(name=nombre):
            if viejo in p.prompt:
                p.prompt = p.prompt.replace(viejo, nuevo)
                p.save(update_fields=["prompt"])


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")

    Pose.objects.filter(name__in=[n for n, _ in NUEVAS]).delete()

    for nombre, viejo, nuevo in FIX_MUERTO:
        for p in Pose.objects.filter(name=nombre):
            if nuevo in p.prompt:
                p.prompt = p.prompt.replace(nuevo, viejo)
                p.save(update_fields=["prompt"])

    Pose.objects.filter(name__in=A_TIER1).update(tier="tier2")
    for viejo, nuevo in RENOMBRAR.items():
        Pose.objects.filter(name=nuevo).update(name=viejo)


class Migration(migrations.Migration):

    dependencies = [("generate", "0093_blunt_y_one_eye")]

    operations = [migrations.RunPython(aplicar, revertir)]
