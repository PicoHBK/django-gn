from django.db import migrations


# BD-Bath/: lo que se usa en el baño, en el mismo registro subido de tono que
# BD-Night/ y BD-Films/, no la version mansa.
#
# El eje es la humedad, que es lo que sube el tono sin agregar prendas:
#   wet 196.045   see-through clothes 220.475   steam 75.796
#   towel 76.719  naked towel 18.440            partially submerged 47.256
#   wet shirt 21.539   wet hair 20.556          water drop 34.791
#
# Tres censuras "de situacion" que el modelo entiende y quedan mejor que
# nada: steam censor (4.076), convenient censoring (50.721) y el agua misma.
#
# Cuatro tags que parecian obvios NO existen: bath_towel, hot_spring
# -el real es onsen-, after_bath y towel_only. Y shower a secas tampoco
# existe: son showering (6.614) y shower head (5.058).
#
# BD-Towel, que estaba suelto y plano, se pliega al subgrupo.
NUEVOS = [('BD-Bath/Towel', '(naked towel:1.60),\n([white] towel:1.45),\n(wet:1.35),\n(cleavage:1.30),\n(bare shoulders:1.30)'), ('BD-Bath/Towel Head', '(naked towel:1.55),\n(towel on head:1.50),\n([white] towel:1.40),\n(wet hair:1.35),\n(bare shoulders:1.25)'), ('BD-Bath/Wet Shirt', '([white] wet shirt:1.60),\n(see-through clothes:1.50),\n(no bra:1.45),\n(wet:1.35),\n(nipples:1.25)'), ('BD-Bath/Wet Swimsuit', '([black] wet swimsuit:1.60),\n(see-through clothes:1.45),\n(wet:1.40),\n(water drop:1.30)'), ('BD-Bath/Steam', '(steam:1.60),\n(nude:1.45),\n(steam censor:1.40),\n(wet:1.35),\n(wet hair:1.30)'), ('BD-Bath/Soap', '(soap bubbles:1.60),\n(soap:1.45),\n(convenient censoring:1.40),\n(wet:1.35),\n(nude:1.30)'), ('BD-Bath/Onsen', '(onsen:1.55),\n(partially submerged:1.50),\n([white] towel:1.40),\n(steam:1.40),\n(wet hair:1.30)'), ('BD-Bath/Shower', '(showering:1.55),\n(shower head:1.50),\n(wet hair:1.45),\n(water drop:1.35),\n(nude:1.30)'), ('BD-Bath/Submerged', '(partially submerged:1.60),\n(bathtub:1.45),\n(wet hair:1.40),\n(water:1.30),\n(nude:1.30)'), ('BD-Bath/Dripping', '(dripping:1.55),\n(water drop:1.50),\n(wet:1.45),\n(wet hair:1.40),\n(nude:1.30)')]

MOVER = {'BD-Towel': 'BD-Bath/Towel Classic'}


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for viejo, nuevo in MOVER.items():
        s = Special.objects.filter(name=viejo).first()
        if s is not None:
            s.name = nuevo
            s.save(update_fields=["name"])
    for nombre, prompt in NUEVOS:
        if Special.objects.filter(name=nombre).exists():
            continue
        Special.objects.create(name=nombre, tier="tier3", prompt=prompt)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()
    for viejo, nuevo in MOVER.items():
        s = Special.objects.filter(name=nuevo).first()
        if s is not None:
            s.name = viejo
            s.save(update_fields=["name"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0073_bd_night_subido"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
