from django.db import migrations


# BD es de "body", y el subgrupo va con barra, como ya hacia BD-COS/. Los
# grupos que arme sueltos pasan a ser subgrupos de BD:
#
#   Only-    -> BD-Only/      una sola prenda encima
#   Seduct-  -> BD-Seduct/    combinaciones de dos prendas
#
# Y los 16 trajes nuevos, que habian quedado planos al lado de BD-Maid y
# BD-Nurse, se agrupan por familia:
#
#   BD-Jp/     Kimono, Yukata, Miko
#   BD-Fan/    Bunny, Santa, Witch, Angel, Magical, Bikini Armor
#   BD-Sport/  Cheer, Swimsuit, School Swim
#   BD-Work/   Military, Overalls
#   BD-Style/  Goth Lolita, Winter
#
# No se toca BD-COS/, que es el de personajes: 2B, Cammy, Chun-Li y demas.
#
# Ojo: esto renombra 42 specials y validate_special los busca por NOMBRE.
CAMBIOS = {'BD-Kimono': 'BD-Jp/Kimono', 'BD-Yukata': 'BD-Jp/Yukata', 'BD-Miko': 'BD-Jp/Miko', 'BD-Bunny': 'BD-Fan/Bunny', 'BD-Santa': 'BD-Fan/Santa', 'BD-Witch': 'BD-Fan/Witch', 'BD-Angel': 'BD-Fan/Angel', 'BD-Magical': 'BD-Fan/Magical', 'BD-Bikini Armor': 'BD-Fan/Bikini Armor', 'BD-Cheer': 'BD-Sport/Cheer', 'BD-Swimsuit': 'BD-Sport/Swimsuit', 'BD-School Swim': 'BD-Sport/School Swim', 'BD-Military': 'BD-Work/Military', 'BD-Overalls': 'BD-Work/Overalls', 'BD-Goth Lolita': 'BD-Style/Goth Lolita', 'BD-Winter': 'BD-Style/Winter', 'Only-Shirt': 'BD-Only/Shirt', 'Only-Sweater': 'BD-Only/Sweater', 'Only-Jacket': 'BD-Only/Jacket', 'Only-Coat': 'BD-Only/Coat', 'Only-Hoodie': 'BD-Only/Hoodie', 'Only-Kimono': 'BD-Only/Kimono', 'Only-Cape': 'BD-Only/Cape', 'Only-Scarf': 'BD-Only/Scarf', 'Only-Ribbon': 'BD-Only/Ribbon', 'Only-Bandage': 'BD-Only/Bandage', 'Only-Sheet': 'BD-Only/Sheet', 'Only-Overalls': 'BD-Only/Overalls', 'Only-Necktie': 'BD-Only/Necktie', 'Only-Suspenders': 'BD-Only/Suspenders', 'Only-Camisole': 'BD-Only/Camisole', 'Only-Thong': 'BD-Only/Thong', 'Only-Medias': 'BD-Only/Medias', 'Only-Gloves': 'BD-Only/Gloves', 'Seduct-Thong Sweater': 'BD-Seduct/Thong Sweater', 'Seduct-Thong Crop': 'BD-Seduct/Thong Crop', 'Seduct-Lingerie': 'BD-Seduct/Lingerie', 'Seduct-Open Shirt': 'BD-Seduct/Open Shirt', 'Seduct-Garter': 'BD-Seduct/Garter', 'Seduct-Bodystocking': 'BD-Seduct/Bodystocking', 'Seduct-Babydoll': 'BD-Seduct/Babydoll', 'Seduct-Camisole Set': 'BD-Seduct/Camisole Set'}


def _set(apps, invertir):
    Special = apps.get_model("generate", "Special")
    for viejo, nuevo in CAMBIOS.items():
        desde, hasta = (nuevo, viejo) if invertir else (viejo, nuevo)
        s = Special.objects.filter(name=desde).first()
        if s is not None:
            s.name = hasta
            s.save(update_fields=["name"])


def aplicar(apps, schema_editor):
    _set(apps, False)


def revertir(apps, schema_editor):
    _set(apps, True)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0055_agrupar_emotes"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
