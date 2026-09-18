from django.db import migrations


# Grupo Focus: solo los *_focus mas usados de Danbooru y solo de mujer, todos
# tier1, cada uno con el ImageType cuya proporcion le corresponde.
#
# Fuera: penis_focus y pectoral_focus por ser de hombre. Fuera tambien la cola
# larga de la familia, que existe pero casi no se usa: mouth_focus (461),
# clothes_focus (743), navel_focus (825), hair_focus (890), footwear_focus
# (1.111).
#
# OJO, la familia es TODA SINGULAR. Estos no existen (0 posts):
#   thighs_focus, feet_focus, breasts_focus, legs_focus, face_focus
# Por eso el special Focus-Thighs (pk 732) no hace nada: dice thighs_focus.
#
# "face focus" no existe, asi que Focus-Face se arma con eye_focus mas la
# mirada, y el recorte lo pone el ImageType Portrait, que ya trae
# (portrait:1.6) y (close-up:1.2) en su propio prompt.
#
# El peso 1.5 es el que ya usan los Focus- que tenias.
#
# (tag, nombre, ImageType, posts en danbooru)
POSES = [
    ("(eye focus:1.5),(looking at viewer:1.3)", "Focus-Face", "Portrait", 4235),
    ("(breast focus:1.5)", "Focus-Breasts", "Cowboy Shot", 4351),
    ("(back focus:1.5)", "Focus-Back", "Cowboy Shot", 2840),
    ("(ass focus:1.5)", "Focus-Ass", "4:3", 46383),
    ("(hip focus:1.5)", "Focus-Hips", "4:3", 16246),
    ("(hand focus:1.5)", "Focus-Hands", "1:1", 2824),
    ("(armpit focus:1.5)", "Focus-Armpits", "1:1", 4354),
    ("(thigh focus:1.5)", "Focus-Thighs", "3:4", 1272),
    ("(foot focus:1.5)", "Focus-Feet", "3:4", 37824),
    ("(leg focus:1.5)", "Focus-Legs", "Full Body", 811),
]


def aplicar(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")

    tipos = {i.name: i for i in ImageType.objects.all()}

    for prompt, nombre, tipo, _posts in POSES:
        if Pose.objects.filter(name=nombre).exists():
            continue
        Pose.objects.create(
            name=nombre,
            prompt=prompt,
            tier="tier1",
            img_type=tipos.get(tipo),
        )


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    Pose.objects.filter(name__in=[p[1] for p in POSES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0033_v4_acercarse_a_la_camara"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
