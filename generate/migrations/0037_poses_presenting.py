from django.db import migrations


# Grupo Presenting, tier2. Es la otra forma de dirigir la atencion a una parte
# del cuerpo: en vez de que la camara enfoque (*_focus), es la pj la que la
# muestra. El wiki lo define como "a character displaying their body, or
# emphasizing part of their body, in a sexually risque manner".
#
# Va el prefijo "own" en todos a proposito. Sin el, "presenting foot" (1.591)
# significa que OTRO le presenta el pie, no ella. Por eso el special 687
# "Ass Focus" esta mal: usa "presenting ass" en vez de "presenting own ass".
#
# Fuera: presenting_pawpads (833, es furry), presenting_another's_body (500,
# son dos personas) y presenting_bra (357, muy poco).
#
# Mismo bloqueo de una sola persona que las poses Focus-, incluido
# "solo focus" en el negativo, que permite que haya otros y no lo queremos.
NEG = (
    "<neg:\n"
    "multiple girls:1.60,\n"
    "2girls:1.60,\n"
    "multiple boys:1.55,\n"
    "1boy:1.45,\n"
    "solo focus:1.50,\n"
    "multiple views:1.60,\n"
    "zoom layer:1.60\n"
    ">"
)

# (tag, nombre, ImageType, posts en danbooru)
POSES = [
    ("presenting own body", "Presenting-Body", "Full Body", 21521),
    ("presenting own armpit", "Presenting-Armpit", "Cowboy Shot", 16303),
    ("presenting own breasts", "Presenting-Breasts", "Cowboy Shot", 2572),
    ("presenting own ass", "Presenting-Ass", "4:3", 3278),
    ("presenting own anus", "Presenting-Anus", "4:3", 722),
    ("presenting own pussy", "Presenting-Pussy", "1:1", 3124),
    ("presenting removed panties", "Presenting-Panties", "1:1", 1174),
    ("presenting own foot", "Presenting-Foot", "3:4", 6037),
]


def aplicar(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")

    tipos = {i.name: i for i in ImageType.objects.all()}

    for tag, nombre, tipo, _posts in POSES:
        if Pose.objects.filter(name=nombre).exists():
            continue
        Pose.objects.create(
            name=nombre,
            prompt="(%s:1.5),\n(solo:1.45),\n\n%s" % (tag, NEG),
            tier="tier2",
            img_type=tipos.get(tipo),
        )


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    Pose.objects.filter(name__in=[p[1] for p in POSES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0036_focus_solo_una_persona"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
