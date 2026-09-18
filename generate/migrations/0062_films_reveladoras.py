from django.db import migrations


# BD-Films/ pasa a ser la version REVELADORA, no el uniforme normal con
# lenceria debajo. La formula anterior -prenda de oficio + open clothes +
# lace trim- daba un uniforme comun entreabierto, que es casi lo mismo que
# BD-Maid o BD-Nurse. Ahora la prenda misma es la minima:
#
#   thong 55.149        microskirt 27.805     underboob 128.441
#   micro bikini 60.062 micro shorts 18.609   cleavage cutout 122.693
#   revealing clothes 71.196   highleg 167.691   no bra 124.739
#
# BD-Films/Maid usa "maid bikini" (7.082), que es literalmente el arquetipo
# y existe como tag propio.
#
# Ojo: "micro skirt" NO existe en Danbooru, 0 posts. El real es "microskirt",
# todo junto. Tampoco existen "skimpy" ni "bikini top".
#
# Siguen con 2 codigos de color y sin calzado.
CAMBIOS = [['BD-Films/Maid', '([black] maid:1.55),\n(maid apron:1.45),\n(maid headdress:1.40),\n(open clothes:1.40),\n([white] lace trim:1.35),\n(garter belt:1.30),\n(thighhighs:1.25)', '([black] maid bikini:1.60),\n(maid headdress:1.45),\n(waist apron:1.35),\n([white] thong:1.45),\n(underboob:1.40),\n(revealing clothes:1.35)'], ['BD-Films/Nurse', '([white] nurse:1.55),\n(nurse cap:1.40),\n(open clothes:1.45),\n(unbuttoned:1.35),\n([pink] lace trim:1.35),\n(garter belt:1.30)', '([white] nurse:1.45),\n(nurse cap:1.40),\n(microskirt:1.50),\n(cleavage cutout:1.45),\n([white] thong:1.40),\n(underboob:1.35),\n(revealing clothes:1.35)'], ['BD-Films/Doctor', '([white] lab coat:1.55),\n(open lab coat:1.45),\n(stethoscope:1.30),\n([black] lace trim:1.35),\n(garter belt:1.30),\n(thighhighs:1.25)', '([white] lab coat:1.50),\n(open lab coat:1.40),\n([black] micro bikini:1.55),\n(midriff:1.40),\n(revealing clothes:1.40)'], ['BD-Films/Police', '([blue] policewoman:1.55),\n(police:1.40),\n(open shirt:1.45),\n(unbuttoned shirt:1.40),\n([black] garter belt:1.35),\n(pencil skirt:1.30)', '([blue] police:1.45),\n(open shirt:1.45),\n(no bra:1.45),\n([black] micro shorts:1.50),\n(midriff:1.40),\n(revealing clothes:1.35)'], ['BD-Films/Teacher', '([grey] pencil skirt:1.50),\n(teacher:1.45),\n(open shirt:1.45),\n(unbuttoned shirt:1.40),\n([black] lace trim:1.30),\n(garter belt:1.30)', '([grey] microskirt:1.55),\n(open shirt:1.45),\n(no bra:1.45),\n([black] thong:1.45),\n(underboob:1.35),\n(revealing clothes:1.35)'], ['BD-Films/Secretary', '([black] office lady:1.50),\n(pencil skirt:1.45),\n(open shirt:1.45),\n(unbuttoned shirt:1.40),\n([white] lace trim:1.30),\n(garter belt:1.30)', '([black] microskirt:1.55),\n(open shirt:1.45),\n(cleavage cutout:1.45),\n([white] thong:1.40),\n(garter straps:1.35),\n(revealing clothes:1.35)'], ['BD-Films/Schoolgirl', '([navy] school uniform:1.55),\n(serafuku:1.40),\n(pleated skirt:1.40),\n(open clothes:1.45),\n([white] lace trim:1.30),\n(thighhighs:1.25)', '([navy] serafuku:1.45),\n(microskirt:1.50),\n(crop top:1.45),\n(midriff:1.40),\n([white] thong:1.40),\n(underboob:1.35)'], ['BD-Films/Gym', '([red] gym uniform:1.55),\n(sports bra:1.40),\n(open clothes:1.40),\n(midriff:1.35),\n([white] lace trim:1.25)', '([red] sports bra:1.50),\n(micro shorts:1.50),\n(midriff:1.45),\n(underboob:1.40),\n([white] thong:1.35),\n(revealing clothes:1.35)'], ['BD-Films/Cheer', '([pink] cheerleader:1.55),\n(crop top:1.40),\n(pleated skirt:1.40),\n(open clothes:1.35),\n([white] garter belt:1.30)', '([pink] crop top:1.50),\n(microskirt:1.50),\n(midriff:1.45),\n(underboob:1.40),\n([white] thong:1.35),\n(revealing clothes:1.35)'], ['BD-Films/Bunny', '([black] playboy bunny:1.55),\n(rabbit ears:1.40),\n(detached collar:1.35),\n(wrist cuffs:1.30),\n([black] fishnet pantyhose:1.35)', '([black] playboy bunny:1.50),\n(highleg leotard:1.50),\n(rabbit ears:1.40),\n(detached collar:1.30),\n([black] fishnet pantyhose:1.35),\n(revealing clothes:1.30)'], ['BD-Films/Nun', '([black] nun:1.55),\n(habit:1.35),\n(open clothes:1.45),\n([white] lace trim:1.35),\n(garter belt:1.30)', '([black] nun:1.45),\n(revealing clothes:1.50),\n(cleavage cutout:1.45),\n(microskirt:1.45),\n([white] thong:1.40),\n(sideboob:1.35)'], ['BD-Films/Waitress', '([black] waitress:1.55),\n(apron:1.40),\n(open clothes:1.40),\n(miniskirt:1.35),\n([white] lace trim:1.30),\n(garter belt:1.25)', '([black] waitress:1.45),\n(frilled apron:1.40),\n(microskirt:1.50),\n(crop top:1.40),\n(midriff:1.40),\n([white] thong:1.35)']]


def _set(apps, indice):
    Special = apps.get_model("generate", "Special")
    for c in CAMBIOS:
        s = Special.objects.filter(name=c[0]).first()
        if s is not None:
            s.prompt = c[indice]
            s.save(update_fields=["prompt"])


def aplicar(apps, schema_editor):
    _set(apps, 2)


def revertir(apps, schema_editor):
    _set(apps, 1)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0061_bd_milf"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
