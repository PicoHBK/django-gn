from django.db import migrations


# Tres arreglos.
#
# 1) PregSlider sin LoRA. Como ya no esta el slider para graduar, todo el
#    trabajo lo hacen los pesos, asi que suben. El problema del -Low era que
#    sin gradacion quedaba la panza entera: ahora big belly va negado fuerte
#    (1.60) y entran narrow waist y slender para que el cuerpo acompane la
#    etapa en vez de llevar una pelota pegada.
#
# 2) GaSlider firme en todas las versiones. -High tenia (sagging breasts:1.18)
#    y -Old (sagging breasts:1.25): ese era el pecho caido. Se sacan, se niega
#    sagging breasts en las tres y entra perky breasts (5.455), que es el
#    unico tag real de pecho firme; firm_breasts y upturned_breasts son 0.
#    La definicion la dan toned (60.994) y toned female (19.734). No se usa
#    muscular female porque todos los ImageType ya lo niegan en 1.3 y se
#    pelearian.
#    -Tee no se toca.
#
# 3) BD-COS/Tsunade: la prenda gris pasa a tener code de color. Queda con tres
#    [color], dentro del maximo de cuatro.

PREG = {
    "PregSlider-Low": (
        "(pregnant:1.30),\n(navel:1.20),\n(narrow waist:1.30),\n(slender:1.25)\n\n"
        "<neg:\nbig belly:1.60,\nplump:1.40,\nfat:1.35,\nobese:1.30\n>"
    ),
    "PregSlider-Normal": (
        "(pregnant:1.55),\n(navel:1.20),\n(narrow waist:1.20)\n\n"
        "<neg:\nbig belly:1.15,\nfat:1.25,\nobese:1.25\n>"
    ),
    "PregSlider-High": (
        "(pregnant:1.75),\n(big belly:1.60),\n(outie navel:1.35),\n"
        "(puffy nipples:1.25)\n\n<neg:\nfat:1.30,\nobese:1.30\n>"
    ),
}

FIRME = ("<neg:\nsagging breasts:1.55,\nplump:1.35,\nfat:1.35,\nobese:1.30\n>")

GA = {
    "GaSlider-High": (
        "<lora:StS_Age_Slider_Illustrious_v1:.5>,\n(mature female:1.50),\n"
        "(huge breasts:1.40),\n(perky breasts:1.40),\n(mole under eye:1.15),\n"
        "(narrow waist:1.35),\n(toned:1.30),\n(toned female:1.25)\n\n" + FIRME
    ),
    "GaSlider-Med": (
        "<lora:StS_Age_Slider_Illustrious_v1:-1>,\n(aged up:1.45),\n"
        "(medium breasts:1.35),\n(perky breasts:1.40),\n(narrow waist:1.35),\n"
        "(curvy:1.30),\n(toned:1.30),\n(toned female:1.25)\n\n" + FIRME
    ),
    "GaSlider-Old": (
        "<lora:StS_Age_Slider_Illustrious_v1:1.5>,\n(old woman:1.45),\n"
        "(mature female:1.35),\n(wrinkled skin:1.45),\n(grey hair:1.25),\n"
        "(perky breasts:1.40),\n(narrow waist:1.35),\n(curvy:1.30),\n"
        "(wide hips:1.28),\n(thick thighs:1.25),\n(toned:1.30),\n"
        "(toned female:1.25)\n\n" + FIRME
    ),
}

TSUNADE = (
    "([green] haori:1.4), ([gray] crop top:1.4), (crop top:1.35), "
    "(sleeveless:1.25), (blue obi:1.25), ([blue] pants:1.3), "
    "(lowleg pants:1.35), (lowleg:1.35), (midriff:1.40), "
    "<neg:(dress:1.4),(skirt:1.4),(shorts:1.3),(short shorts:1.3),"
    "(jeans:1.3),(leggings:1.3),(bodysuit:1.3),(jumpsuit:1.3),"
    "(long sleeves:1.3),(shirt:1.3),(t-shirt:1.3),(blouse:1.3),"
    "(bra:1.2),(underwear:1.2)>"
)


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, prompt in {**PREG, **GA}.items():
        Special.objects.filter(name=nombre).update(prompt=prompt)
    Special.objects.filter(name="BD-COS/Tsunade").update(prompt=TSUNADE)


def revertir(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [("generate", "0105_bd_harem")]

    operations = [migrations.RunPython(aplicar, revertir)]
