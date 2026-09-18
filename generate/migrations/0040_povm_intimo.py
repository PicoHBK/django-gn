from django.db import migrations


# El grupo POVM pasa a ser de acciones contra la camara, sin objetos.
#
# Se van las tres que eran escenario y no accion: POVM-Doorway, POVM-Table y
# POVM-Bed. Entran las que la pj HACE hacia el que mira.
#
# La correccion que importa: "incoming kiss" no existe y "imminent_kiss" no es
# lo que parece. El wiki lo define como "the moment just before when TWO
# CHARACTERS are about to kiss", y aclara aparte: "not to be confused with
# imminent kiss, which is between two characters and not the viewer". El que
# apunta a la camara es "kissing_viewer".
#
# Los numeros entre parentesis son posts junto a "pov". La familia *_viewer
# tiene poco volumen ahi (el corpus de POV es sobre todo explicito), asi que
# las cuatro de accion van con peso alto para compensar. La unica con volumen
# real es imminent_penetration.
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

BORRAR = ["POVM-Doorway", "POVM-Table", "POVM-Bed"]

# (linea propia, nombre, ImageType, posts junto a pov)
NUEVAS = [
    # la mas solida de todas
    ("(imminent penetration:1.70),\n(imminent vaginal:1.40),",
     "POVM-Imminent", "1:1", 3445),
    # el wiki la ejemplifica con "beckoning": te llama, te lleva
    ("(reaching towards viewer:1.75),\n(beckoning:1.40),",
     "POVM-Reach", "Cowboy Shot", 2217),
    ("(imminent fellatio:1.70),", "POVM-Fellatio", "1:1", 636),
    # el beso A LA CAMARA, no entre dos
    ("(kissing viewer:1.80),", "POVM-Kiss", "Portrait", 191),
    ("(hugging viewer:1.80),", "POVM-Hug", "Cowboy Shot", 208),
    ("(attacking viewer:1.80),\n(punching viewer:1.50),",
     "POVM-Attack", "Cowboy Shot", 245),
]


def aplicar(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")

    Pose.objects.filter(name__in=BORRAR).delete()

    tipos = {i.name: i for i in ImageType.objects.all()}
    for linea, nombre, tipo, _posts in NUEVAS:
        if Pose.objects.filter(name=nombre).exists():
            continue
        Pose.objects.create(
            name=nombre,
            prompt=BASE % linea,
            tier="tier2",
            img_type=tipos.get(tipo),
        )


def revertir(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")

    Pose.objects.filter(name__in=[n[1] for n in NUEVAS]).delete()

    tipos = {i.name: i for i in ImageType.objects.all()}
    for linea, nombre, tipo in [
        ("(pov doorway:1.60),", "POVM-Doorway", "3:4"),
        ("(pov across table:1.60),", "POVM-Table", "4:3"),
        ("(pov across bed:1.60),", "POVM-Bed", "4:3"),
    ]:
        if not Pose.objects.filter(name=nombre).exists():
            Pose.objects.create(
                name=nombre,
                prompt=BASE % linea,
                tier="tier2",
                img_type=tipos.get(tipo),
            )


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0039_poses_povm"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
