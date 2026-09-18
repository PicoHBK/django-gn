from django.db import migrations


# Grupo de prueba del rediseno por posicion: mating press.
#
# Patron: un "Gen" que es solo el tag principal con peso alto para que sea
# general, mas variantes de camara. En TODAS va el bloque del hombre:
# dark-skinned male, y faceless male + bald para que no se le vea la cara.
# Todo tier5.
#
# Las que tienen LORA o embedding se conservan y pasan al grupo con nombre
# nuevo; se les completa el bloque del male donde faltaba. Las que no tienen
# ningun asset entrenado se borran: el Gen nuevo cubre la posicion.
#
# Nota: 400 y 493 no tienen LORA pero si embeddings (FFF_after_mating_press y
# FFF_mating_press), que son igual de entrenados, asi que se conservan con
# prefijo E- en vez de L-.
#
# Ojo: renombrar cambia como las encuentra el front, que busca por nombre en
# views.py:329.
NUEVAS = [['MatPress-Gen', '(mating press:1.75),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['MatPress-POV', '(mating press:1.75),\n(pov:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['MatPress-Above', '(mating press:1.75),\n(from above:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '1:1'], ['MatPress-Side', '(mating press:1.75),\n(from side:1.60),\n(dark-skinned male:1.50),\n(faceless male:1.45),\n(bald:1.35),\n(hetero:1.30),\n(1boy:1.20),\n(1girl:1.20)', '4:3']]

RENOMBRAR = [[390, 'Matting-P', 'MatPress-L-Above', 'tier5', 'mating press ,from above, blush, 1boy, closed mouth, nipples, closed eyes, ass, hetero, sweat, lying, penis, pussy, sex, spread legs, cum, on back,vaginal, arms up, toes, hug, cum in pussy,from above, orgasm, (boy on top:1.3), deep penetration, mating press,1boy,<lora:mating-press-from-above-v3-illustriousxl-lora-nochekaiser:.8>,dark-skinned male,naked male,bald', 'mating press ,from above, blush, 1boy, closed mouth, nipples, closed eyes, ass, hetero, sweat, lying, penis, pussy, sex, spread legs, cum, on back,vaginal, arms up, toes, hug, cum in pussy,from above, orgasm, (boy on top:1.3), deep penetration, mating press,1boy,<lora:mating-press-from-above-v3-illustriousxl-lora-nochekaiser:.8>,dark-skinned male,naked male,bald,(faceless male:1.45)'], [419, 'Matting-P-Lock', 'MatPress-L-Above-Soft', 'tier5', '<lora:mating-press-from-above-v3-illustriousxl-lora-nochekaiser:.3>,mating press ,from above, blush, 1boy, closed mouth, closed eyes, ass, hetero, sweat, lying, penis, pussy, sex, spread legs, on back,vaginal, arms up,hug,orgasm, futon, (boy on top:1.3), deep penetration, mating press,1boy,leg lock, dark-skinned male,bald', '<lora:mating-press-from-above-v3-illustriousxl-lora-nochekaiser:.3>,mating press ,from above, blush, 1boy, closed mouth, closed eyes, ass, hetero, sweat, lying, penis, pussy, sex, spread legs, on back,vaginal, arms up,hug,orgasm, futon, (boy on top:1.3), deep penetration, mating press,1boy,leg lock, dark-skinned male,bald,(faceless male:1.45)'], [773, 'Matting-side lora', 'MatPress-L-Side', 'tier5', '<lora:mating-press-from-side-v4-illustriousxl-lora-nochekaiser:1>, mating press from side, mating press, arm support, blush, open mouth, 1boy, nipples, hetero, sweat, completely nude, uncensored, lying, penis, pussy, tongue, solo focus, tongue out, sex, on back, vaginal, saliva, bed, on bed, bed sheet, veins, legs up, missionary, boy on top,dark-skinned male,bald,faceless,faceless male', '<lora:mating-press-from-side-v4-illustriousxl-lora-nochekaiser:1>, mating press from side, mating press, arm support, blush, open mouth, 1boy, nipples, hetero, sweat, completely nude, uncensored, lying, penis, pussy, tongue, solo focus, tongue out, sex, on back, vaginal, saliva, bed, on bed, bed sheet, veins, legs up, missionary, boy on top,dark-skinned male,bald,faceless,faceless male'], [819, 'Matting-2 View', 'MatPress-L-Loss', 'tier5', 'ILMPV1.0, instant loss, instant loss 2koma, sex, mating press,<lora:Mating_Press_Instant_Loss_-_Vertical_r1-000006:.9>, dark-skinned male', 'ILMPV1.0, instant loss, instant loss 2koma, sex, mating press,<lora:Mating_Press_Instant_Loss_-_Vertical_r1-000006:.9>, dark-skinned male,(faceless male:1.45),(bald:1.35)'], [400, 'After Met', 'MatPress-E-After', 'tier4', '(embedding:FFF_after_mating_press)', '(embedding:FFF_after_mating_press),(dark-skinned male:1.50),(faceless male:1.45),(bald:1.35)'], [493, 'Matting-Start', 'MatPress-E-Start', 'tier5', 'FFF_mating_press,dark-skinned male', 'FFF_mating_press,dark-skinned male,(faceless male:1.45),(bald:1.35)']]

BORRAR = [[420, 'Matting-Press-Lock-Side', 'tier5', '4:3', 'mating press  blush, 1boy, closed eyes, ass, hetero, sweat, lying, penis, pussy, sex, spread legs, cum, on back,vaginal, arms up, hug, cum in pussy, from side orgasm, boy on top, deep penetration,mating press,1boy,leg lock,kiss,french kiss,(dark-skinned male:1.4),faceless,faceless male,bald'], [450, 'Matting-onBack', 'tier5', '1:1', '1girl, 1boy, vaginal, sex, mating press, cum overlow, deep penetration, huge penis, dark-skin male, faceless, faceless male,bald'], [602, 'Matting-Press-NL', 'tier5', '3:4', '(mating press:1.1),dark-skin male,bald,faceless,from above,lying'], [603, 'Matting-Press-Original', 'tier5', '1:1', 'mating press,dark-skin male,bald,faceless,ass,anus,lying,on back'], [610, 'Immi-Mat-2', 'tier4', '3:4', '(mating press:1.2), (imminent penetration:1.1),penis, dark-skinned male,bald,(faceless:1.5),faceless male,lying'], [679, 'Matting-L1 V1 An', 'tier5', '4:3', 'mating press anal,penis, deep penetration, 1girl, 1boy, mating press position, legs up, legs raised, legs behind shoulders, folded legs, deep penetration, full body press, face to face, intimate position,dark-skin male,faceless,faceless male,bald']]


def aplicar(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")
    tipos = {i.name: i for i in ImageType.objects.all()}

    for pk, _viejo_n, nuevo_n, _tier, _viejo_p, nuevo_p in RENOMBRAR:
        p = Pose.objects.filter(pk=pk).first()
        if p is None:
            continue
        p.name = nuevo_n
        p.prompt = nuevo_p
        p.tier = "tier5"
        if p.img_type_id is None:
            # la 419 estaba sin ImageType
            p.img_type = tipos.get("1:1")
        p.save(update_fields=["name", "prompt", "tier", "img_type"])

    Pose.objects.filter(pk__in=[b[0] for b in BORRAR]).delete()

    for nombre, prompt, tipo in NUEVAS:
        if Pose.objects.filter(name=nombre).exists():
            continue
        Pose.objects.create(
            name=nombre, prompt=prompt, tier="tier5", img_type=tipos.get(tipo)
        )


def revertir(apps, schema_editor):
    ImageType = apps.get_model("generate", "ImageType")
    Pose = apps.get_model("generate", "Pose")
    tipos = {i.name: i for i in ImageType.objects.all()}

    Pose.objects.filter(name__in=[n[0] for n in NUEVAS]).delete()

    for pk, viejo_n, _nuevo_n, tier, viejo_p, _nuevo_p in RENOMBRAR:
        p = Pose.objects.filter(pk=pk).first()
        if p is None:
            continue
        p.name = viejo_n
        p.prompt = viejo_p
        p.tier = tier
        p.save(update_fields=["name", "prompt", "tier"])

    for pk, nombre, tier, tipo, prompt in BORRAR:
        if not Pose.objects.filter(name=nombre).exists():
            Pose.objects.create(
                name=nombre, prompt=prompt, tier=tier, img_type=tipos.get(tipo)
            )


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0041_imminent_a_tier4"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
