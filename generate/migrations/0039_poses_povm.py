from django.db import migrations


# Grupo POVM: la camara es el hombre, y en todos es de piel oscura.
#
# "male pov" NO es un tag: es un alias activo de "pov", asi que al etiquetar
# se convierte en pov y el modelo nunca vio esa secuencia. Los specials 450
# (POV-M-Caught) y 451 (POV-Pen) lo usan y esa parte no hace nada.
#
# Tampoco hay tag de POV masculino, porque en Danbooru es el default: solo
# etiquetan "female_pov" (9.044) cuando es la excepcion. Por eso lo masculino
# se arma con pov + dark-skinned male + hetero, y "female pov" va al negativo
# para que la camara no se le pase a ella.
#
# Descartados por no combinar con dark-skinned male: pov_breasts (3 posts
# juntos) y pov_legs (40). pov_peephole quedo afuera porque pisa a Spy-KeyHole.
#
# Aca NO va el bloqueo de "solo" que tienen Focus- y Presenting-: hay un
# hombre en escena por definicion. Se bloquea que se multipliquen las mujeres
# y el clon del mismo pj, nada mas.
NEG = (
    "<neg:\n"
    "female pov:1.60,\n"
    "multiple girls:1.55,\n"
    "2girls:1.55,\n"
    "multiple boys:1.50,\n"
    "multiple views:1.60,\n"
    "zoom layer:1.60\n"
    ">"
)

BASE = "(pov:1.60),\n%s\n(dark-skinned male:1.50),\n(hetero:1.30),\n(1girl:1.20),\n\n" + NEG

# (linea propia, nombre, ImageType, posts del tag principal)
POSES = [
    ("(pov hands:1.60),", "POVM-Hands", "Cowboy Shot", 48598),
    ("(pov crotch:1.60),", "POVM-Crotch", "1:1", 31832),
    ("(pov hands:1.50),\n(disembodied hand:1.50),", "POVM-Grab", "Cowboy Shot", 23018),
    ("(pov doorway:1.60),", "POVM-Doorway", "3:4", 3715),
    ("(pov across table:1.60),", "POVM-Table", "4:3", 3578),
    ("(pov across bed:1.60),", "POVM-Bed", "4:3", 1235),
]


def aplicar(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")

    tipos = {i.name: i for i in ImageType.objects.all()}

    for linea, nombre, tipo, _posts in POSES:
        if Pose.objects.filter(name=nombre).exists():
            continue
        Pose.objects.create(
            name=nombre,
            prompt=BASE % linea,
            tier="tier2",
            img_type=tipos.get(tipo),
        )


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    Pose.objects.filter(name__in=[p[1] for p in POSES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0038_unificar_panties"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
