from django.db import migrations


# Reparacion de los specials BD-, tres cosas.
#
# 1. TIER. Los 80 quedan en tier3. Se mueven 13 que estaban en tier5 y uno en
#    tier1. OJO con dos: BD-Nad es "naked, completely nude, nude" y
#    BD-Only Thighhighs es "naked, completely nude" con medias. El segundo
#    estaba en TIER1, o sea el front se lo mostraba a cualquiera; el primero
#    baja de tier5 a tier3, asi que pasa a ser mas visible que antes.
#
# 2. CODIGOS DE COLOR. Maximo 2 por special. Seis tenian mas y el tercero en
#    adelante nunca recibia color: process_special_colors reparte los colores
#    en orden y el front manda los que manda. A los sobrantes se les saca el
#    corchete y el color queda fijo, que es lo que ya pasaba en la practica.
#
#    De paso, BD-COS/Tsunade tenia un backtick suelto al principio y al final
#    del prompt.
#
# 3. OUTFITS NUEVOS. 16, cada uno de una familia distinta y no variantes del
#    mismo: japones (kimono, yukata, miko), disfraz (bunny, santa, witch,
#    angel, magical girl), deporte (cheerleader, swimsuit, school swim),
#    trabajo (military, overalls), estilo (gothic lolita, winter) y fantasia
#    (bikini armor). Todos con maximo 2 codigos de color y con peso, siguiendo
#    el formato de los BD-COS.
A_TIER3 = [[378, 'BD-A', 'tier5'], [372, 'BD-B', 'tier5'], [382, 'BD-C', 'tier5'], [383, 'BD-D', 'tier5'], [361, 'BD-E', 'tier5'], [385, 'BD-F', 'tier5'], [391, 'BD-G', 'tier5'], [608, 'BD-H', 'tier5'], [615, 'BD-I', 'tier5'], [363, 'BD-Micro', 'tier5'], [356, 'BD-Nad', 'tier5'], [784, 'BD-Only Thighhighs', 'tier1'], [375, 'BD-Slingshot', 'tier5'], [656, 'BD-Tank Thon', 'tier5']]

CODIGOS = [[378, 'BD-A', 'micro jeans,[white] camisole,[blue] jeans,midriff,micro thong, highleg thong,[black] thong,bare shoulders,bare neck,cleavage, sleeveless', 'micro jeans,[white] camisole,[blue] jeans,midriff,micro thong, highleg thong,black thong,bare shoulders,bare neck,cleavage, sleeveless'], [608, 'BD-H', '[white] sweater,[blue] jeans,[pink] apron,bare shoulders', '[white] sweater,[blue] jeans,pink apron,bare shoulders'], [740, 'BD-Casual 2', '[black] hoodie, [white] crop_top, [purple] tight_shorts, black thighhighs', '[black] hoodie, white crop_top, [purple] tight_shorts, black thighhighs'], [852, 'BD-COS/Hinata', '([lavender] cropped jacket:1.4),\n(cropped jacket:1.3),\n([white] crop top:1.35),\n(white shirt:1.25),\n(long sleeves:1.2),\n([dark blue] jeans:1.35),\n(lowleg:1.2),\n(midriff:1.3),\n\n<neg:\n(shorts:1.5),\n(pleated shorts:1.5),\n(skirt:1.4),\n(dress:1.4),\n(leggings:1.3),\n(pants:1.2),\n(bodysuit:1.3),\n(jumpsuit:1.3),\n(hoodie:1.3),\n(t-shirt:1.2),\n(blouse:1.2)\n>', '([lavender] cropped jacket:1.4),\n(cropped jacket:1.3),\n(white crop top:1.35),\n(white shirt:1.25),\n(long sleeves:1.2),\n([dark blue] jeans:1.35),\n(lowleg:1.2),\n(midriff:1.3),\n\n<neg:\n(shorts:1.5),\n(pleated shorts:1.5),\n(skirt:1.4),\n(dress:1.4),\n(leggings:1.3),\n(pants:1.2),\n(bodysuit:1.3),\n(jumpsuit:1.3),\n(hoodie:1.3),\n(t-shirt:1.2),\n(blouse:1.2)\n>'], [834, 'BD-COS/Juri', '(white cropped vest:1.50),(open front vest:1.45),(sleeveless vest:1.35),(deep neckline:1.35),(exposed midriff:1.35),(bare skin under vest:1.50),([magenta] vest accents:1.30),([magenta] vest trim:1.25),(yoga pants:1.40),(lowleg_pants:1.50),(puffy pants:1.45),(low-rise pants:1.45),(exposed lower abdomen:1.40),(black pants:1.40),(white panels:1.35),([magenta] accents:1.30),([magenta] trim:1.25),(color-blocked pants:1.30),(visible thong sides:1.30),(hip lines:1.20)', '(white cropped vest:1.50),(open front vest:1.45),(sleeveless vest:1.35),(deep neckline:1.35),(exposed midriff:1.35),(bare skin under vest:1.50),([magenta] vest accents:1.30),(magenta vest trim:1.25),(yoga pants:1.40),(lowleg_pants:1.50),(puffy pants:1.45),(low-rise pants:1.45),(exposed lower abdomen:1.40),(black pants:1.40),(white panels:1.35),([magenta] accents:1.30),(magenta trim:1.25),(color-blocked pants:1.30),(visible thong sides:1.30),(hip lines:1.20)'], [851, 'BD-COS/Tsunade', '`([green] haori:1.4), ([gray] crop_top:1.4), (crop_top:1.35), (sleeveless:1.25), ([blue] obi:1.25), ([blue] pants:1.3), (lowrise_pants:1.3), (midriff:1.35), <neg:(dress:1.4),(skirt:1.4),(shorts:1.3),(short_shorts:1.3),(jeans:1.3),(leggings:1.3),(bodysuit:1.3),(jumpsuit:1.3),(long_sleeves:1.3),(shirt:1.3),(t-shirt:1.3),(blouse:1.3),(bra:1.2),(underwear:1.2)>`', '([green] haori:1.4), (gray crop_top:1.4), (crop_top:1.35), (sleeveless:1.25), (blue obi:1.25), ([blue] pants:1.3), (lowrise_pants:1.3), (midriff:1.35), <neg:(dress:1.4),(skirt:1.4),(shorts:1.3),(short_shorts:1.3),(jeans:1.3),(leggings:1.3),(bodysuit:1.3),(jumpsuit:1.3),(long_sleeves:1.3),(shirt:1.3),(t-shirt:1.3),(blouse:1.3),(bra:1.2),(underwear:1.2)>']]

OUTFITS = [['BD-Kimono', '([red] kimono:1.50),\n(japanese clothes:1.45),\n([gold] obi:1.35),\n(wide sleeves:1.30),\n(long kimono:1.25)'], ['BD-Yukata', '([blue] yukata:1.50),\n(japanese clothes:1.40),\n([white] obi:1.30),\n(summer festival:1.20)'], ['BD-Bunny', '([black] playboy bunny:1.55),\n(leotard:1.40),\n(detached collar:1.35),\n(wrist cuffs:1.30),\n([black] pantyhose:1.30),\n(rabbit ears:1.35)'], ['BD-Magical', '([pink] magical girl:1.55),\n(frilled dress:1.40),\n(puffy sleeves:1.30),\n([white] thighhighs:1.30),\n(hair ribbon:1.20)'], ['BD-Military', '([olive] military uniform:1.50),\n(military:1.35),\n(belt:1.30),\n([black] boots:1.30),\n(epaulettes:1.25)'], ['BD-Swimsuit', '([navy] one-piece swimsuit:1.55),\n(swimsuit:1.35),\n(highleg swimsuit:1.30),\n([white] name tag:1.20)'], ['BD-School Swim', '([navy] school swimsuit:1.55),\n(one-piece swimsuit:1.40),\n(name tag:1.25)'], ['BD-Santa', '([red] santa costume:1.55),\n(fur trim:1.35),\n(santa hat:1.35),\n([black] belt:1.25),\n(capelet:1.20)'], ['BD-Overalls', '([blue] overalls:1.50),\n(denim:1.35),\n([white] shirt:1.30),\n(rolled up sleeves:1.20)'], ['BD-Angel', '([white] dress:1.50),\n(angel:1.45),\n(angel wings:1.40),\n(halo:1.35),\n([gold] sash:1.20)'], ['BD-Winter', '([beige] winter clothes:1.50),\n(coat:1.40),\n(scarf:1.35),\n([brown] gloves:1.25),\n(long sleeves:1.20)'], ['BD-Cheer', '([red] cheerleader:1.55),\n(crop top:1.35),\n(pleated skirt:1.35),\n([white] socks:1.25),\n(midriff:1.30)'], ['BD-Witch', '([black] witch:1.55),\n(witch hat:1.45),\n(cape:1.35),\n([purple] dress:1.30),\n(long sleeves:1.20)'], ['BD-Goth Lolita', '([black] gothic lolita:1.55),\n(frills:1.40),\n(lace trim:1.35),\n([white] apron:1.25),\n(headdress:1.30)'], ['BD-Bikini Armor', '([silver] bikini armor:1.55),\n(armor:1.40),\n(pauldrons:1.30),\n([brown] belt:1.25),\n(gauntlets:1.25)'], ['BD-Miko', '([red] hakama:1.50),\n(miko:1.50),\n([white] kimono:1.35),\n(wide sleeves:1.30),\n(ribbon-trimmed sleeves:1.20)']]


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")

    for pk, _n, _viejo_tier in A_TIER3:
        s = Special.objects.filter(pk=pk).first()
        if s is not None:
            s.tier = "tier3"
            s.save(update_fields=["tier"])

    for pk, _n, _viejo, nuevo in CODIGOS:
        s = Special.objects.filter(pk=pk).first()
        if s is not None:
            s.prompt = nuevo
            s.save(update_fields=["prompt"])

    for nombre, prompt in OUTFITS:
        if Special.objects.filter(name=nombre).exists():
            continue
        Special.objects.create(name=nombre, tier="tier3", prompt=prompt)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")

    Special.objects.filter(name__in=[o[0] for o in OUTFITS]).delete()

    for pk, _n, viejo_tier in A_TIER3:
        s = Special.objects.filter(pk=pk).first()
        if s is not None:
            s.tier = viejo_tier
            s.save(update_fields=["tier"])

    for pk, _n, viejo, _nuevo in CODIGOS:
        s = Special.objects.filter(pk=pk).first()
        if s is not None:
            s.prompt = viejo
            s.save(update_fields=["prompt"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0052_limpiar_emotes"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
