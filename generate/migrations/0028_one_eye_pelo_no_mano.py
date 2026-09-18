from django.db import migrations


# Hair-One Eye tapaba el ojo con la MANO, no con el pelo.
#
# La culpa era de "covering one eye". El wiki de Danbooru lo define asi:
# "Covering one eye with a hand or an object held over the face. This should
# be the result of a deliberate action." O sea el tag pide justamente el gesto
# de taparse, que es lo contrario de lo que queriamos.
#
# El correcto es "one eye covered" (74.037 posts), que el mismo wiki manda
# usar "if the eye is simply covered with no apparent intent, such as by
# hair". Es pasivo: el ojo queda tapado sin que el personaje haga nada.
#
# Y "covering one eye" pasa al negativo junto con las manos y la cara, para
# que no vuelva por otro lado. "hair over eyes" tambien, que es cuando el pelo
# tapa LOS DOS ojos.
#
# El positivo no lleva ninguna frase con "covering one eye" adentro: si no,
# estaria pidiendo y negando la misma secuencia de tokens al mismo tiempo.
NOMBRE = "Hair-One Eye"

VIEJO = '<(hair over one eye:1.70)>,\n(covering one eye:1.60),\n(long hair:1.50),\n\n<neg:\nhair between eyes:1.40,\ncenter part:1.40,\nside part:1.30,\nhair behind ears:1.30,\nshort hair:1.45,\nmedium hair:1.30,\nvery long hair:1.30,\nabsurdly long hair:1.50\n>'

NUEVO = '<(hair over one eye:1.70)>,\n(one eye covered:1.60),\n(long hair:1.50),\n\n<neg:\ncovering one eye:1.70,\nhand on own face:1.60,\ncovering face:1.55,\nhand over eye:1.60,\neyepatch:1.55,\nhair over eyes:1.50,\nhair between eyes:1.40,\ncenter part:1.40,\nside part:1.30,\nhair behind ears:1.30,\nshort hair:1.45,\nmedium hair:1.30,\nvery long hair:1.30,\nabsurdly long hair:1.50\n>'


def _set(apps, prompt):
    Special = apps.get_model("generate", "Special")
    s = Special.objects.filter(name=NOMBRE).first()
    if s is None:
        return
    s.prompt = prompt
    s.save(update_fields=["prompt"])


def aplicar(apps, schema_editor):
    _set(apps, NUEVO)


def revertir(apps, schema_editor):
    _set(apps, VIEJO)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0027_vistas_de_camara"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
