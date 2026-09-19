from django.db import migrations


# PregSlider estaba roto: -Low y -Normal tenian el MISMO peso de LoRA (:1) y
# solo se diferenciaban en si llevaban (pregnant:1) o no. O sea que eran dos
# etapas, no tres, y la "temprana" no era mas temprana: era la misma panza sin
# el tag que la nombra.
#
# Ahora si hay progresion real: la escala la marca el peso del LoRA (0.6 / 1.6
# / 3.0) y los tags acompanan.
#
# "pregnancy" no es tag de Danbooru (0 posts) pero se queda en las tres: es el
# trigger del LoRA y sacarlo podria desactivarlo.
#
# Descartados por no existir: huge_belly, swollen_belly, late_pregnancy y
# flat_stomach, los cuatro con 0 posts. Y stomach_bulge (17.004) NO se usa:
# ese es el bulto por penetracion, no el embarazo.
LORA = "<lora:pregnancy_slider:{}>"

NUEVO = {
    # temprana: apenas se nota. big belly negado para que no se adelante.
    "PregSlider-Low": (
        LORA.format("0.6") + ",\npregnancy,\n(pregnant:1.15)\n\n"
        "<neg:\nbig belly:1.45,\nplump:1.20\n>"
    ),
    # media: panza clara, sin los rasgos del final.
    "PregSlider-Normal": (
        LORA.format("1.6") + ",\npregnancy,\n(pregnant:1.40)\n\n"
        "<neg:\nbig belly:1.20\n>"
    ),
    # full term: panza grande y los rasgos del ultimo tramo.
    "PregSlider-High": (
        LORA.format("3") + ",\npregnancy,\n(pregnant:1.60),\n(big belly:1.50),\n"
        "(outie navel:1.30),\n(puffy nipples:1.20)"
    ),
}

ANTERIOR = {
    "PregSlider-Low": "<lora:pregnancy_slider:1>,pregnancy",
    "PregSlider-Normal": "<lora:pregnancy_slider:1>,pregnancy, (pregnant:1)",
    "PregSlider-High": "<lora:pregnancy_slider:3>,pregnancy,(pregnant:1)",
}


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, prompt in NUEVO.items():
        Special.objects.filter(name=nombre).update(prompt=prompt)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for nombre, prompt in ANTERIOR.items():
        Special.objects.filter(name=nombre).update(prompt=prompt)


class Migration(migrations.Migration):

    dependencies = [("generate", "0098_da_mas_oscuro")]

    operations = [migrations.RunPython(aplicar, revertir)]
