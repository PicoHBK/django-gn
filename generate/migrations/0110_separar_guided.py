import re

from django.db import migrations


# Los -Immi mezclaban tres momentos distintos en el mismo prompt:
#
#   imminent penetration (21.836) "penetration is about to occur, but hasn't
#                                  happened yet"     -> todavia no entro
#   guided penetration   (1.843)  "someone, usually the person being
#                                  penetrated, guiding another's penetration"
#                                                    -> la guia ella
#   just the tip         (2.367)  "only the tip of a penis is penetrating"
#                                                    -> ya entro, apenas
#
# Se separan. Los -Immi se quedan solo con el momento previo y ahora llevan el
# agarre del hombre (torso grab 13.799; hip_grab es alias). En anal el agarre
# es grabbing another's ass (30.994).
#
# Y nace la familia -Guided, donde la mano es de ella: guided penetration mas
# penis grab (7.676).
#
# "just the tip" sale de los -Immi por definicion: si entro la punta, ya no es
# inminente. No se recicla en ningun lado; si se quiere queda libre para un
# grupo propio.
#
# Todo se genera desde la base filtrando por prompt, no por nombre: asi
# Cunni-Immi y Paiz-Immi quedan afuera, que son inminencia de otra cosa y no
# de penetracion.

QUITAR = {"guided penetration", "just the tip"}
IMMI = {"imminent penetration", "imminent vaginal", "imminent anal"}

AGARRE_HOMBRE = "(torso grab:1.40),\n(hands on another's hips:1.35)"
AGARRE_ANAL = "(grabbing another's ass:1.40),\n(torso grab:1.35)"


def _partes(prompt):
    if "<neg:" in prompt:
        pos, resto = prompt.split("<neg:", 1)
        return pos, "<neg:" + resto
    return prompt, ""


def _tokens(pos):
    return [t.strip() for t in pos.split(",") if t.strip()]


def _sin(tokens, nombres):
    out = []
    for t in tokens:
        m = re.match(r"^\(([^()]+?):[0-9.]+\)$", t)
        if m and m.group(1) in nombres:
            continue
        out.append(t)
    return out


def _armar(tokens, neg, extra):
    cuerpo = ",\n".join(tokens)
    if extra:
        cuerpo += ",\n" + extra
    return cuerpo + ("\n\n" + neg if neg else "")


def aplicar(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")

    base = list(Pose.objects.filter(prompt__icontains="imminent penetration"))

    for p in base:
        pos, neg = _partes(p.prompt)
        toks = _tokens(pos)
        es_anal = any("imminent anal" in t for t in toks)

        # 1) limpiar el -Immi y darle el agarre del hombre
        limpio = _sin(toks, QUITAR)
        agarre = AGARRE_ANAL if es_anal else AGARRE_HOMBRE
        if "torso grab" not in pos:
            p.prompt = _armar(limpio, neg, agarre)
        else:
            p.prompt = _armar(limpio, neg, "")
        p.save(update_fields=["prompt"])

        # 2) el gemelo -Guided, con la mano de ella
        nombre = p.name.replace("Immi", "Guided", 1)
        if nombre == p.name:
            continue
        # se saca penis tambien porque el bloque de abajo lo vuelve a poner
        sin_immi = _sin(_sin(toks, QUITAR), IMMI | {"penis"})
        acto = "anal" if es_anal else "vaginal"
        bloque = (
            "(guided penetration:1.75),\n(penis grab:1.45),\n"
            "(%s:1.40),\n(penis:1.35)" % acto
        )
        Pose.objects.update_or_create(
            name=nombre,
            defaults={
                "prompt": _armar(sin_immi, neg, bloque),
                "tier": p.tier,
                "img_type": p.img_type,
            },
        )


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    Pose.objects.filter(prompt__icontains="guided penetration").filter(
        name__contains="Guided"
    ).delete()


class Migration(migrations.Migration):

    dependencies = [("generate", "0109_pov_jobs_immi")]

    operations = [migrations.RunPython(aplicar, revertir)]
