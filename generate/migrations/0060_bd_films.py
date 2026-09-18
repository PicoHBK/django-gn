from django.db import migrations


# BD-Films/: los arquetipos de pelicula, con la formula que ya usabas en
# BD-Nuser Trim -prenda de oficio + lenceria debajo + ropa abierta-, pero
# armada con tags reales en vez de a mano.
#
# La lenceria entra por (open clothes:1.40) mas lace trim y garter belt, que
# es lo que hace que la prenda de oficio se vea abierta y deje ver lo de
# abajo. open_clothes tiene 756.893 posts, es de los tags mas entrenados que
# hay.
#
# Cuatro oficios que parecen obvios NO existen en Danbooru: secretary (0),
# stewardess (0), receptionist (0) y bunny_girl (0). Por eso BD-Films/Secretary
# se arma con office_lady (22.776) y BD-Films/Bunny con playboy_bunny
# (148.516). Otros tres existen pero son inservibles por volumen: librarian
# (106), babysitter (105) y masseuse (24).
#
# Dos codigos de color en cada uno: uno para la prenda de oficio y otro para
# la lenceria. Ninguno lleva calzado.
NUEVOS = [['BD-Films/Maid', '([black] maid:1.55),\n(maid apron:1.45),\n(maid headdress:1.40),\n(open clothes:1.40),\n([white] lace trim:1.35),\n(garter belt:1.30),\n(thighhighs:1.25)'], ['BD-Films/Nurse', '([white] nurse:1.55),\n(nurse cap:1.40),\n(open clothes:1.45),\n(unbuttoned:1.35),\n([pink] lace trim:1.35),\n(garter belt:1.30)'], ['BD-Films/Doctor', '([white] lab coat:1.55),\n(open lab coat:1.45),\n(stethoscope:1.30),\n([black] lace trim:1.35),\n(garter belt:1.30),\n(thighhighs:1.25)'], ['BD-Films/Police', '([blue] policewoman:1.55),\n(police:1.40),\n(open shirt:1.45),\n(unbuttoned shirt:1.40),\n([black] garter belt:1.35),\n(pencil skirt:1.30)'], ['BD-Films/Teacher', '([grey] pencil skirt:1.50),\n(teacher:1.45),\n(open shirt:1.45),\n(unbuttoned shirt:1.40),\n([black] lace trim:1.30),\n(garter belt:1.30)'], ['BD-Films/Secretary', '([black] office lady:1.50),\n(pencil skirt:1.45),\n(open shirt:1.45),\n(unbuttoned shirt:1.40),\n([white] lace trim:1.30),\n(garter belt:1.30)'], ['BD-Films/Schoolgirl', '([navy] school uniform:1.55),\n(serafuku:1.40),\n(pleated skirt:1.40),\n(open clothes:1.45),\n([white] lace trim:1.30),\n(thighhighs:1.25)'], ['BD-Films/Gym', '([red] gym uniform:1.55),\n(sports bra:1.40),\n(open clothes:1.40),\n(midriff:1.35),\n([white] lace trim:1.25)'], ['BD-Films/Cheer', '([pink] cheerleader:1.55),\n(crop top:1.40),\n(pleated skirt:1.40),\n(open clothes:1.35),\n([white] garter belt:1.30)'], ['BD-Films/Bunny', '([black] playboy bunny:1.55),\n(rabbit ears:1.40),\n(detached collar:1.35),\n(wrist cuffs:1.30),\n([black] fishnet pantyhose:1.35)'], ['BD-Films/Nun', '([black] nun:1.55),\n(habit:1.35),\n(open clothes:1.45),\n([white] lace trim:1.35),\n(garter belt:1.30)'], ['BD-Films/Waitress', '([black] waitress:1.55),\n(apron:1.40),\n(open clothes:1.40),\n(miniskirt:1.35),\n([white] lace trim:1.30),\n(garter belt:1.25)']]


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, prompt in NUEVOS:
        if Special.objects.filter(name=nombre).exists():
            continue
        Special.objects.create(name=nombre, tier="tier3", prompt=prompt)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0059_only_negar_ropa"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
