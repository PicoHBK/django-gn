from django.db import migrations


# Hair-Blunt y Hair-One Eye, los dos tuyos.
#
# BLUNT. Tres de sus cuatro tags del positivo estaban MUERTOS en Danbooru:
#   straight_bangs 0   even_bangs 0   thick_bangs 18
# y en el negativo, side-swept_bangs tambien 0. Solo funcionaba blunt_bangs
# (430.907). Por eso nunca salia "ultra perfecto": pedia una cosa sola.
#
# Ahora blunt bangs va en 1.95 y lo acompañan tags reales: blunt_ends
# (52.875), que es justo el corte recto de las puntas, straight_hair
# (102.363) y long_bangs (47.834).
#
# Y el negativo pasa a tener los rivales que SI existen, con parted_bangs
# (313.913), swept_bangs (163.260), crossed_bangs (109.034), curtained_hair
# (50.637), asymmetrical_bangs (48.206), choppy y diagonal. Mas
# hair_between_eyes (1.793.801), que es el mechon suelto entre los ojos y es
# lo que mas arruina un blunt parejo.
#
# Largo: hasta la cintura, o sea long_hair.
#
# ONE EYE. Pasa a pelo hasta los muslos, que en la escala de Danbooru ya no
# es long_hair sino very_long_hair (1.419.594): "longer than the waist,
# ranging to as far down as the feet".
#
# Ojo con esto: very long hair estaba en sus propios tags_deleted desde la
# 0026, cuando todo el pelo iba a la cintura. Si lo dejaba, el special se
# borraba el tag que acababa de pedir. Se saca de la lista.
BLUNT = ['<(blunt bangs:1.85)>,\n(straight bangs:1.60),\n(even bangs:1.50),\n(thick bangs:1.40),\n(long hair:1.50),\n\n<neg:\nside-swept bangs:1.60,\nswept bangs:1.60,\nasymmetrical bangs:1.55,\nparted bangs:1.55,\nmessy hair:1.50,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55\n>', '<(blunt bangs:1.95)>,\n(blunt ends:1.60),\n(straight hair:1.50),\n<(long bangs:1.40)>,\n(long hair:1.55),\n\n<neg:\nparted bangs:1.70,\nswept bangs:1.70,\ncrossed bangs:1.65,\ncurtained hair:1.60,\nasymmetrical bangs:1.60,\nchoppy bangs:1.55,\ndiagonal bangs:1.55,\nhair between eyes:1.50,\nmessy hair:1.50,\nsidelocks:1.45,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.40,\nabsurdly long hair:1.55\n>', ['ponytail', 'twintails', 'braid', 'updo', 'short hair', 'medium hair', 'very long hair', 'absurdly long hair'], ['absurdly long hair', 'bangs', 'braid', 'fringe', 'intakes', 'medium hair', 'ponytail', 'short hair', 'sidelocks', 'twintails', 'updo', 'very long hair']]

ONE_EYE = ['<(hair over one eye:1.85)>,\n(one eye covered:1.70),\n(long hair:1.50),\n\n<neg:\ncovering one eye:1.70,\nhand on own face:1.60,\nhand over eye:1.60,\ncovering face:1.55,\neyepatch:1.55,\nhair over eyes:1.50,\nhair between eyes:1.45,\ncenter part:1.40,\nside part:1.35,\nhair behind ears:1.40,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55\n>', '<(hair over one eye:1.90)>,\n(one eye covered:1.75),\n(very long hair:1.60),\n(long hair:1.35),\n\n<neg:\ncovering one eye:1.70,\nhand on own face:1.60,\nhand over eye:1.60,\ncovering face:1.55,\neyepatch:1.55,\nhair over eyes:1.50,\nhair between eyes:1.45,\ncenter part:1.40,\nside part:1.35,\nhair behind ears:1.40,\nshort hair:1.55,\nmedium hair:1.45,\nabsurdly long hair:1.50\n>', ['short hair', 'medium hair', 'very long hair', 'absurdly long hair'], ['absurdly long hair', 'bangs', 'fringe', 'medium hair', 'short hair']]


def _set(apps, i_prompt, i_dels):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")
    for nombre, datos in [("Hair-Blunt", BLUNT), ("Hair-One Eye", ONE_EYE)]:
        s = Special.objects.filter(name=nombre).first()
        if s is None:
            continue
        s.prompt = datos[i_prompt]
        s.save(update_fields=["prompt"])
        s.tags_deleted.clear()
        for t in datos[i_dels]:
            tag, _ = Tag.objects.get_or_create(name=t)
            s.tags_deleted.add(tag)


def aplicar(apps, schema_editor):
    _set(apps, 1, 3)


def revertir(apps, schema_editor):
    _set(apps, 0, 2)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0092_negar_shiny_skin"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
