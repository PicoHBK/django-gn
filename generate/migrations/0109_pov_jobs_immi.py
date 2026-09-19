from django.db import migrations


# POV para los jobs de tier4 y para los imminent penetration.
#
# Los imminent no se escriben a mano: se generan desde la base. Por cada
# X-Immi nace un X-ImmiPOV y por cada X-ImmiAnal un X-ImmiAnalPOV, copiando el
# prompt existente e inyectando el bloque POV en la parte POSITIVA, antes del
# <neg:>. Asi cualquier grupo de posicion que se agregue despues hereda la
# misma forma sin tocar esta migracion.
#
# Los jobs si van a mano porque cada uno pide un angulo distinto: el footjob
# se mira desde abajo con foot focus, el paizuri de frente y desde arriba, el
# handjob tiene tres angulos utiles.
#
# Canonicos: foot_focus (feet_focus es alias) y pov (male_pov es alias de pov,
# por eso no se usa).

POV_IMMI = "(pov:1.70),\n(looking at viewer:1.35),\n(solo focus:1.30)"

COLA = """(dark-skinned male:1.50),
(faceless male:1.45),
(bald:1.35),
(hetero:1.30),
(1boy:1.20),
(1girl:1.20)"""

JOBS = [
    ("ArmpitSex-POV", "(armpit sex:1.70),\n(pov:1.75),\n(looking at viewer:1.35)"),
    ("ButtJob-POV", "(buttjob:1.70),\n(pov:1.75),\n(from behind:1.40),\n(ass focus:1.35)"),
    ("FootJob-POV", "(footjob:1.70),\n(pov:1.75),\n(foot focus:1.45),\n(looking at viewer:1.30)"),
    ("FootJob-POV Below", "(footjob:1.70),\n(pov:1.70),\n(from below:1.50),\n(foot focus:1.45)"),
    ("FootJob-POV Rev", "(reverse footjob:1.70),\n(pov:1.75),\n(foot focus:1.45)"),
    ("HairJob-POV", "(hairjob:1.70),\n(pov:1.75),\n(looking at viewer:1.35)"),
    ("HandJob-POV", "(handjob:1.70),\n(pov:1.75),\n(pov hands:1.40),\n(looking at viewer:1.35)"),
    ("HandJob-POV Above", "(handjob:1.70),\n(pov:1.70),\n(from above:1.50),\n(looking up:1.35)"),
    ("HandJob-POV Double", "(double handjob:1.70),\n(pov:1.75),\n(pov hands:1.40),\n(looking at viewer:1.30)"),
    ("Paiz-POV", "(paizuri:1.70),\n(pov:1.75),\n(looking at viewer:1.35)"),
    ("Paiz-POV Above", "(paizuri:1.70),\n(pov:1.70),\n(from above:1.50),\n(looking up:1.35)"),
    ("Paiz-POV Immi", "(imminent paizuri:1.70),\n(paizuri:1.40),\n(pov:1.75),\n(penis:1.35)"),
    ("PussyJob-POV", "(pussyjob:1.70),\n(pov:1.75),\n(pov crotch:1.40)"),
    ("PussyJob-POV Frot", "(frottage:1.70),\n(pov:1.75),\n(pov crotch:1.40)"),
    ("ThighSex-POV", "(thigh sex:1.70),\n(pov:1.75),\n(pov crotch:1.40)"),
    ("ThighSex-POV Knee", "(kneepit sex:1.70),\n(pov:1.75),\n(from behind:1.35)"),
]


def _inyectar_pov(prompt):
    """Mete el bloque POV al final de la parte positiva, nunca dentro del neg."""
    if "<neg:" in prompt:
        pos, resto = prompt.split("<neg:", 1)
        return pos.rstrip().rstrip(",") + ",\n" + POV_IMMI + "\n\n<neg:" + resto
    return prompt.rstrip().rstrip(",") + ",\n" + POV_IMMI


def aplicar(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")

    # jobs, a mano
    gen = Pose.objects.filter(name="HandJob-Gen").first()
    it = gen.img_type if gen else None
    for nombre, cuerpo in JOBS:
        Pose.objects.update_or_create(
            name=nombre,
            defaults={"prompt": cuerpo + ",\n" + COLA, "tier": "tier4", "img_type": it},
        )

    # imminent, generados desde los que ya existen
    for sufijo in ("-Immi", "-ImmiAnal"):
        for p in Pose.objects.filter(name__endswith=sufijo):
            Pose.objects.update_or_create(
                name=p.name + "POV",
                defaults={
                    "prompt": _inyectar_pov(p.prompt),
                    "tier": p.tier,
                    "img_type": p.img_type,
                },
            )


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    Pose.objects.filter(name__in=[n for n, _ in JOBS]).delete()
    Pose.objects.filter(name__endswith="-ImmiPOV").delete()
    Pose.objects.filter(name__endswith="-ImmiAnalPOV").delete()


class Migration(migrations.Migration):

    dependencies = [("generate", "0108_grupo_milf")]

    operations = [migrations.RunPython(aplicar, revertir)]
