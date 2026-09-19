import re

from django.db import migrations


# La 0110 limpiaba tokens con formato (tag:peso). Las cuatro poses Immi-
# hechas a mano tienen los tags en texto plano ("imminent penetration,from
# behind,pov,..."), asi que sus gemelas -Guided nacieron todavia diciendo
# imminent. Se limpian en las dos formas.
FUERA = ("imminent penetration", "imminent vaginal", "imminent anal",
         "just the tip", "guided penetration")


def _limpiar(prompt):
    if "<neg:" in prompt:
        pos, neg = prompt.split("<neg:", 1)
        neg = "<neg:" + neg
    else:
        pos, neg = prompt, ""

    out = []
    for t in (x.strip() for x in pos.split(",")):
        if not t:
            continue
        m = re.match(r"^\(([^()]+?):[0-9.]+\)$", t)
        desnudo = m.group(1) if m else t
        if desnudo.strip().lower() in FUERA:
            continue
        out.append(t)
    return ",\n".join(out) + ("\n\n" + neg if neg else "")


def aplicar(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    for p in Pose.objects.filter(name__contains="Guided"):
        pos = p.prompt.split("<neg:")[0]
        if not any(f in pos.lower() for f in FUERA[:4]):
            continue
        limpio = _limpiar(p.prompt)
        # el bloque guided se vuelve a poner porque _limpiar lo saca tambien
        acto = "anal" if "Anal" in p.name else "vaginal"
        p.prompt = limpio.split("<neg:")[0].rstrip().rstrip(",") + (
            ",\n(guided penetration:1.75),\n(penis grab:1.45),\n"
            "(%s:1.40)" % acto
        ) + ("\n\n<neg:" + limpio.split("<neg:", 1)[1] if "<neg:" in limpio else "")
        p.save(update_fields=["prompt"])


def revertir(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [("generate", "0110_separar_guided")]

    operations = [migrations.RunPython(aplicar, revertir)]
