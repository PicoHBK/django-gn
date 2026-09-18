from django.db import migrations


# Las 5 posiciones de Danbooru que faltaban. No tenian ninguna pose, por eso
# no aparecieron en la reestructuracion de los 22 grupos: no habia nada que
# mover ni que borrar, son grupos nuevos enteros.
#
# Mismo patron: Gen con el tag principal en 1.75, mas POV, Above y Side, y el
# bloque del hombre en todas. Todo tier5.
#
# bear position tiene solo 342 posts en Danbooru, es la mas floja de las
# cinco y puede no resolver bien.
NUEVAS = [['Reclining-Gen', '(reclining:1.75),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['Reclining-POV', '(reclining:1.75),\n(pov:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['Reclining-Above', '(reclining:1.75),\n(from above:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['Reclining-Side', '(reclining:1.75),\n(from side:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '4:3'], ['LegsOverHead-Gen', '(legs over head:1.75),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['LegsOverHead-POV', '(legs over head:1.75),\n(pov:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['LegsOverHead-Above', '(legs over head:1.75),\n(from above:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['LegsOverHead-Side', '(legs over head:1.75),\n(from side:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '4:3'], ['Amazon-Gen', '(amazon position:1.75),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['Amazon-POV', '(amazon position:1.75),\n(pov:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['Amazon-Above', '(amazon position:1.75),\n(from above:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['Amazon-Side', '(amazon position:1.75),\n(from side:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '4:3'], ['RevSquatCowgirl-Gen', '(reverse squatting cowgirl position:1.75),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['RevSquatCowgirl-POV', '(reverse squatting cowgirl position:1.75),\n(pov:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['RevSquatCowgirl-Above', '(reverse squatting cowgirl position:1.75),\n(from above:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['RevSquatCowgirl-Side', '(reverse squatting cowgirl position:1.75),\n(from side:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '4:3'], ['Bear-Gen', '(bear position:1.75),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['Bear-POV', '(bear position:1.75),\n(pov:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['Bear-Above', '(bear position:1.75),\n(from above:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['Bear-Side', '(bear position:1.75),\n(from side:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '4:3']]


def aplicar(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")
    tipos = {i.name: i for i in ImageType.objects.all()}
    for nombre, prompt, tipo in NUEVAS:
        if Pose.objects.filter(name=nombre).exists():
            continue
        Pose.objects.create(
            name=nombre, prompt=prompt, tier="tier5", img_type=tipos.get(tipo)
        )


def revertir(apps, schema_editor):
    Pose = apps.get_model("generate", "Pose")
    Pose.objects.filter(name__in=[n[0] for n in NUEVAS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0043_grupos_por_posicion"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
