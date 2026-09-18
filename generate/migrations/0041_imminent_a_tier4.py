from django.db import migrations


# Las dos POVM con tags imminent se van a tier4, donde ya vive toda la
# familia Immi-*. El front bloquea tier4, asi que quedan guardadas pero fuera
# de circulacion.
CAMBIOS = [("POVM-Imminent", "tier4", "tier2"), ("POVM-Fellatio", "tier4", "tier2")]


def _set(apps, indice):
    Pose = apps.get_model("generate", "Pose")
    for cambio in CAMBIOS:
        p = Pose.objects.filter(name=cambio[0]).first()
        if p is None:
            continue
        p.tier = cambio[indice]
        p.save(update_fields=["tier"])


def aplicar(apps, schema_editor):
    _set(apps, 1)


def revertir(apps, schema_editor):
    _set(apps, 2)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0040_povm_intimo"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
