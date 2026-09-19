from django.db import migrations


# Cola estandar del grupo Fell-, copiada tal cual de Fell-Gen.
COLA = """(dark-skinned male:1.50),
(faceless male:1.45),
(bald:1.35),
(hetero:1.30),
(1boy:1.20),
(1girl:1.20)"""

# Sin tags de expresion: la emocion la pone el modulo Emote.
# "tongue out" y "open mouth" si van, porque ahi son parte del acto.
NUEVAS = [
    # --- encuadre cerrado: que se vea poco y el foco sea la cara ---
    ("Fell-Upper", "(fellatio:1.70),\n(upper body:1.70),\n(cropped torso:1.40)"),
    ("Fell-Portrait", "(fellatio:1.60),\n(portrait:1.70),\n(close-up:1.45)"),
    ("Fell-Eyes", "(fellatio:1.70),\n(eye contact:1.70),\n(looking at viewer:1.45),\n(upper body:1.35)"),
    ("Fell-Cheek", "(fellatio:1.70),\n(cheek bulge:1.75),\n(close-up:1.40)"),
    ("Fell-Up", "(fellatio:1.70),\n(looking up:1.60),\n(from above:1.45),\n(upper body:1.35)"),
    # --- POV ---
    ("Fell-POV", "(fellatio:1.70),\n(pov:1.75),\n(looking at viewer:1.45),\n(pov hands:1.30)"),
    ("Fell-POV Deep", "(deepthroat:1.70),\n(pov:1.75),\n(looking at viewer:1.40)"),
    ("Fell-POV Lick", "(licking penis:1.70),\n(pov:1.75),\n(tongue out:1.35)"),
    ("Fell-POV Immi", "(imminent fellatio:1.70),\n(pov:1.75),\n(open mouth:1.35)"),
    ("Fell-POV Up", "(fellatio:1.70),\n(pov:1.70),\n(looking up:1.50),\n(from above:1.35)"),
    # --- actos que faltaban ---
    ("Fell-Kiss", "(kissing penis:1.75),\n(close-up:1.35)"),
    ("Fell-Smell", "(smelling penis:1.75),\n(penis on face:1.30)"),
    ("Fell-Balls", "(licking testicle:1.75),\n(testicles:1.40)"),
    ("Fell-Hair", "(fellatio:1.70),\n(grabbing another's hair:1.65),\n(hair pull:1.45),\n(head grab:1.30)"),
    ("Fell-On Head", "(penis on head:1.75),\n(fellatio gesture:1.35)"),
    ("Fell-Swallow", "(cum in mouth:1.70),\n(gokkun:1.60),\n(after fellatio:1.35)"),
    ("Fell-Tongue", "(cum on tongue:1.75),\n(tongue out:1.50),\n(after fellatio:1.30)"),
    ("Fell-Stealth", "(fellatio:1.70),\n(stealth sex:1.70),\n(under table:1.50)"),
    ("Fell-Huge", "(fellatio:1.70),\n(huge penis:1.60),\n(size difference:1.45),\n(veiny penis:1.30)"),
    ("Fell-Clothed", "(fellatio:1.70),\n(clothed female nude male:1.65)"),
]


def aplicar(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    gen = Pose.objects.filter(name="Fell-Gen").first()
    it = gen.img_type if gen else None

    for nombre, cuerpo in NUEVAS:
        Pose.objects.update_or_create(
            name=nombre,
            defaults={"prompt": cuerpo + ",\n" + COLA, "tier": "tier4", "img_type": it},
        )


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    Pose.objects.filter(name__in=[n for n, _ in NUEVAS]).delete()


class Migration(migrations.Migration):

    dependencies = [("generate", "0096_special_da")]

    operations = [migrations.RunPython(aplicar, revertir)]
