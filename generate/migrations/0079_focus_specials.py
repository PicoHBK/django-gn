from django.db import migrations


# El grupo Focus- de SPECIALS queda completo en tier2. Ya existia a medias
# con dos: Focus-Ass y Focus-Thighs, los dos en tier1.
#
# Focus-Thighs seguia usando "thighs_focus", que NO existe en Danbooru -la
# familia es toda singular, el real es thigh_focus (1.272)-. O sea llevaba
# todo este tiempo sin hacer nada. Se arregla de paso.
#
# Los 10 nuevos van con el focus en 1.50 y tags de apoyo abajo, SIN bloque
# negativo, como pediste: estos suman, no restan. Los Focus- de POSES, que
# son otra cosa, siguen con su bloqueo de solo.
#
# Focus-Face usa eye_focus (4.235) porque "face_focus" no existe, 0 posts.
# Focus-Lips usa mouth_focus (461), el mas flojo de la familia.
ARREGLOS = [['Focus-Ass', '(ass focus:1.5)', '(ass focus:1.50),\n(ass:1.35),\n(from behind:1.20)', 'tier2', 'tier1'], ['Focus-Thighs', '(thighs_focus:1.5)', '(thigh focus:1.50),\n(thighs:1.35),\n(thick thighs:1.25)', 'tier2', 'tier1']]

NUEVOS = [['Focus-Face', '(eye focus:1.50),\n(looking at viewer:1.35),\n(eyelashes:1.25),\n(lips:1.20)'], ['Focus-Breasts', '(breast focus:1.50),\n(breasts:1.35),\n(cleavage:1.30),\n(collarbone:1.20)'], ['Focus-Hips', '(hip focus:1.50),\n(hips:1.35),\n(wide hips:1.25)'], ['Focus-Feet', '(foot focus:1.50),\n(feet:1.35),\n(soles:1.25),\n(toes:1.20)'], ['Focus-Back', '(back focus:1.50),\n(back:1.35),\n(bare back:1.25),\n(shoulder blades:1.20)'], ['Focus-Hands', '(hand focus:1.50),\n(hands:1.35),\n(fingers:1.25),\n(nails:1.20)'], ['Focus-Armpits', '(armpit focus:1.50),\n(armpit:1.35),\n(arms up:1.30),\n(arms behind head:1.20)'], ['Focus-Legs', '(leg focus:1.50),\n(legs:1.35),\n(thighs:1.25),\n(knees:1.20)'], ['Focus-Navel', '(navel focus:1.50),\n(navel:1.40),\n(stomach:1.30),\n(midriff:1.20)'], ['Focus-Lips', '(mouth focus:1.50),\n(lips:1.40),\n(parted lips:1.30),\n(lipstick:1.20)']]


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, _viejo, nuevo, tier, _viejo_tier in ARREGLOS:
        s = Special.objects.filter(name=nombre).first()
        if s is not None:
            s.prompt, s.tier = nuevo, tier
            s.save(update_fields=["prompt", "tier"])
    for nombre, prompt in NUEVOS:
        if Special.objects.filter(name=nombre).exists():
            continue
        Special.objects.create(name=nombre, tier="tier2", prompt=prompt)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()
    for nombre, viejo, _nuevo, _tier, viejo_tier in ARREGLOS:
        s = Special.objects.filter(name=nombre).first()
        if s is not None:
            s.prompt, s.tier = viejo, viejo_tier
            s.save(update_fields=["prompt", "tier"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0078_neg_muscular_y_red_lips"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
