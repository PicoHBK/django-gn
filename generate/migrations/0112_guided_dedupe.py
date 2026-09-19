import re

from django.db import migrations


# La 0111 saco los tags de imminent de las cuatro -Guided en texto plano pero
# les volvio a agregar el bloque guided, que la 0110 ya les habia puesto: por
# eso quedaron con penis grab y vaginal repetidos. Y a Guided-R-P-1 le seguia
# quedando "imminent rape", que no estaba en la lista de la 0111.
#
# Esta pasada reconstruye el bloque de una sola vez en TODAS las -Guided:
# saca cualquier forma de los tags del bloque (con parentesis o suelta),
# deduplica lo que queda respetando el orden, y agrega el bloque una vez.
BLOQUE = ("imminent penetration", "imminent vaginal", "imminent anal",
          "imminent rape", "just the tip", "guided penetration",
          "penis grab", "vaginal", "anal", "penis")


def _desnudo(token):
    m = re.match(r"^\(([^()]+?):[0-9.]+\)$", token)
    return (m.group(1) if m else token).strip().lower()


def aplicar(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    for p in Pose.objects.filter(name__contains="Guided"):
        prompt = p.prompt
        if "<neg:" in prompt:
            pos, neg = prompt.split("<neg:", 1)
            neg = "\n\n<neg:" + neg
        else:
            pos, neg = prompt, ""

        vistos, limpio = set(), []
        for t in (x.strip() for x in pos.split(",")):
            if not t:
                continue
            d = _desnudo(t)
            if d in BLOQUE or d in vistos:
                continue
            vistos.add(d)
            limpio.append(t)

        acto = "anal" if "Anal" in p.name else "vaginal"
        limpio += [
            "(guided penetration:1.75)",
            "(penis grab:1.45)",
            "(%s:1.40)" % acto,
            "(penis:1.35)",
        ]
        p.prompt = ",\n".join(limpio) + neg
        p.save(update_fields=["prompt"])


def revertir(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [("generate", "0111_guided_texto_plano")]

    operations = [migrations.RunPython(aplicar, revertir)]
