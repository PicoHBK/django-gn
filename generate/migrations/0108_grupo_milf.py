from django.db import migrations


# Grupo Milf-: poses de mujer elegante y sensual, en tier2 (sugerente).
# El nombre estaba libre en Pose; los Milf- que ya existen son del modulo
# Emote, que es otra tabla, asi que no se pisan.
#
# La que pidio el usuario es Milf-Recline: acostada de costado con las piernas
# cruzadas y la mano sobre la cadera. hand_on_own_hip tiene 230.631 posts, es
# de los gestos mejor aprendidos que hay.
#
# El grupo es solo postura. La edad la sigue poniendo GaSlider, la expresion
# el modulo Emote y el calzado FT-: no se toca nada de eso desde aca.
#
# Canonicos: on_side (lying_on_side es alias) y head_rest (chin_rest es alias).

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
    # la pedida
    ("Milf-Recline", "(lying:1.60),\n(on side:1.50),\n(crossed legs:1.55),\n"
                     "(hand on own hip:1.55),\n(reclining:1.35),\n(arm support:1.30)"),
    ("Milf-Recline Back", "(lying:1.60),\n(on back:1.50),\n(crossed legs:1.45),\n"
                          "(hand on own hip:1.45),\n(arched back:1.30)"),
    ("Milf-Head Rest", "(lying:1.55),\n(on side:1.50),\n(head rest:1.60),\n"
                       "(crossed legs:1.40),\n(arm support:1.35)"),
    ("Milf-Stomach", "(lying:1.55),\n(on stomach:1.55),\n(arm support:1.40),\n"
                     "(crossed ankles:1.40),\n(feet up:1.35),\n(looking back:1.30)"),
    ("Milf-Arch", "(lying:1.55),\n(on back:1.50),\n(arched back:1.60),\n"
                  "(legs together:1.35),\n(hand on own chest:1.35)"),
    ("Milf-Bed", "(lying:1.55),\n(on bed:1.55),\n(on side:1.45),\n"
                 "(crossed legs:1.40),\n(head rest:1.40)"),
    # sentadas
    ("Milf-Crossed", "(sitting:1.50),\n(crossed legs:1.65),\n"
                     "(hand on own thigh:1.40),\n(leaning back:1.30)"),
    ("Milf-Couch", "(sitting:1.45),\n(on couch:1.55),\n(crossed legs:1.50),\n"
                   "(arm support:1.35),\n(leaning back:1.35)"),
    ("Milf-Cheek", "(sitting:1.45),\n(hand on own cheek:1.60),\n(elbow rest:1.45),\n"
                   "(crossed legs:1.40)"),
    ("Milf-Leg Up", "(sitting:1.45),\n(leg up:1.60),\n(hand on own thigh:1.40),\n"
                    "(thigh gap:1.30)"),
    ("Milf-Knees", "(sitting:1.45),\n(knees up:1.55),\n(arm support:1.40),\n"
                   "(legs apart:1.30)"),
    # de pie, con el gesto arriba del standing para no pisar ese modulo
    ("Milf-Hips", "(hand on own hip:1.70),\n(contrapposto:1.40),\n"
                  "(crossed legs:1.30),\n(standing:1.30)"),
    ("Milf-Both Hips", "(hands on own hips:1.70),\n(leaning back:1.35),\n"
                       "(contrapposto:1.30),\n(standing:1.30)"),
    ("Milf-Arms", "(crossed arms:1.65),\n(arm under breasts:1.55),\n"
                  "(contrapposto:1.35),\n(standing:1.30)"),
]


def aplicar(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    ImageType = apps.get_model("generate", "ImageType")
    it = ImageType.objects.filter(name__icontains="full body").first()
    for nombre, cuerpo in NUEVAS:
        Pose.objects.update_or_create(
            name=nombre,
            defaults={"prompt": cuerpo + ",\n" + SOLO, "tier": "tier2", "img_type": it},
        )


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    Pose.objects.filter(name__in=[n for n, _ in NUEVAS]).delete()


class Migration(migrations.Migration):

    dependencies = [("generate", "0107_preg_escalones")]

    operations = [migrations.RunPython(aplicar, revertir)]
