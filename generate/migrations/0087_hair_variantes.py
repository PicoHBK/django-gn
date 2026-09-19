from django.db import migrations


# 14 specials de pelo nuevos, todos muy distintos entre si y de los cinco que
# habia. La mitad rompe el molde: los cinco anteriores forzaban pelo largo
# sin excepcion, y estos cuatro fuerzan CORTO -bob cut (139.652), pixie cut,
# wolf cut (7.848) y undercut (22.803)-, negando el largo en vez del corto.
#
# Los atados: twintails (1.240.323), twin braids (249.841), side ponytail
# (236.390), single braid (184.551), low twintails (165.024), drill hair
# (132.002) y half updo (59.869).
#
# Los de textura: wavy hair (150.078), messy hair (92.304) y hime cut
# (31.843), que son los que cambian la forma sin atar nada.
#
# El tag principal va entre <> cuando su palabra esta en los propios
# tags_deleted del special: twintails, braid, drill, updo, hime y ponytail se
# borran del personaje pero no de si mismos. Los de corte -bob, pixie, wolf,
# undercut- no lo necesitan.
#
# Los siete recogidos llevan ademas el bloque de mechones sueltos en el
# negativo: sidelocks (942.850), hair flaps, floating hair y messy hair. Es
# lo que aprendimos con Hair-Bun.
NUEVOS = [['Hair-Bob', '(bob cut:1.85),\n(short hair:1.55),\n(blunt bangs:1.30),\n(short hair:1.55),\n\n<neg:\ntwintails:1.50,\nponytail:1.50,\nhair bun:1.45,\nlong hair:1.55,\nvery long hair:1.60,\nabsurdly long hair:1.65\n>', ['ponytail', 'twintails', 'twintail', 'bun', 'braid', 'braids', 'updo', 'drill', 'drills', 'hime', 'intakes', 'pigtails', 'dreadlocks', 'afro', 'ribbon', 'horns']], ['Hair-Pixie', '(pixie cut:1.85),\n(very short hair:1.55),\n(short hair:1.40),\n(short hair:1.55),\n\n<neg:\ntwintails:1.50,\nponytail:1.50,\nbraid:1.45,\nlong hair:1.55,\nvery long hair:1.60,\nabsurdly long hair:1.65\n>', ['ponytail', 'twintails', 'twintail', 'bun', 'braid', 'braids', 'updo', 'drill', 'drills', 'hime', 'intakes', 'pigtails', 'dreadlocks', 'afro', 'ribbon', 'horns']], ['Hair-Wolf', '(wolf cut:1.85),\n(messy hair:1.45),\n(layered hair:1.30),\n(short hair:1.55),\n\n<neg:\nstraight hair:1.45,\nhair bun:1.40,\nlong hair:1.55,\nvery long hair:1.60,\nabsurdly long hair:1.65\n>', ['ponytail', 'twintails', 'twintail', 'bun', 'braid', 'braids', 'updo', 'drill', 'drills', 'hime', 'intakes', 'pigtails', 'dreadlocks', 'afro', 'ribbon', 'horns']], ['Hair-Undercut', '(undercut:1.85),\n(sidecut:1.50),\n(asymmetrical hair:1.45),\n(short hair:1.55),\n\n<neg:\ntwintails:1.45,\nhair bun:1.40,\nlong hair:1.55,\nvery long hair:1.60,\nabsurdly long hair:1.65\n>', ['ponytail', 'twintails', 'twintail', 'bun', 'braid', 'braids', 'updo', 'drill', 'drills', 'hime', 'intakes', 'pigtails', 'dreadlocks', 'afro', 'ribbon', 'horns']], ['Hair-Twintails', '<(twintails:1.85)>,\n(two side up:1.40),\n(hair tie:1.25),\n(long hair:1.50),\n\n<neg:\nponytail:1.55,\nhair bun:1.50,\nbraid:1.45,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55,\nsidelocks:1.55,\nhair flaps:1.55,\nfloating hair:1.50,\nmessy hair:1.60\n>', ['ponytail', 'twintail', 'bun', 'braid', 'braids', 'updo', 'drill', 'drills', 'hime', 'intakes', 'pigtails', 'dreadlocks', 'afro', 'ribbon', 'horns']], ['Hair-Low Twin', '<(low twintails:1.85)>,\n(twintails:1.50),\n(hair tie:1.25),\n(long hair:1.50),\n\n<neg:\nhigh ponytail:1.50,\nhair bun:1.45,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55,\nsidelocks:1.55,\nhair flaps:1.55,\nfloating hair:1.50,\nmessy hair:1.60\n>', ['ponytail', 'twintail', 'bun', 'braid', 'braids', 'updo', 'drill', 'drills', 'hime', 'intakes', 'pigtails', 'dreadlocks', 'afro', 'ribbon', 'horns']], ['Hair-Side Pony', '<(side ponytail:1.85)>,\n(one side up:1.45),\n(hair tie:1.25),\n(long hair:1.50),\n\n<neg:\nhigh ponytail:1.50,\ntwintails:1.50,\nhair bun:1.45,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55,\nsidelocks:1.55,\nhair flaps:1.55,\nfloating hair:1.50,\nmessy hair:1.60\n>', ['twintails', 'twintail', 'bun', 'braid', 'braids', 'updo', 'drill', 'drills', 'hime', 'intakes', 'pigtails', 'dreadlocks', 'afro', 'ribbon', 'horns']], ['Hair-Braid', '<(single braid:1.85)>,\n(braid:1.50),\n(hair tie:1.25),\n(long hair:1.50),\n\n<neg:\ntwintails:1.50,\nponytail:1.45,\nhair bun:1.45,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55,\nsidelocks:1.55,\nhair flaps:1.55,\nfloating hair:1.50,\nmessy hair:1.60\n>', ['ponytail', 'twintails', 'twintail', 'bun', 'braids', 'updo', 'drill', 'drills', 'hime', 'intakes', 'pigtails', 'dreadlocks', 'afro', 'ribbon', 'horns']], ['Hair-Twin Braids', '<(twin braids:1.85)>,\n(braid:1.50),\n(low twintails:1.35),\n(long hair:1.50),\n\n<neg:\nponytail:1.50,\nhair bun:1.45,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55,\nsidelocks:1.55,\nhair flaps:1.55,\nfloating hair:1.50,\nmessy hair:1.60\n>', ['ponytail', 'twintails', 'twintail', 'bun', 'braid', 'updo', 'drill', 'drills', 'hime', 'intakes', 'pigtails', 'dreadlocks', 'afro', 'ribbon', 'horns']], ['Hair-Drills', '<(drill hair:1.85)>,\n(twin drills:1.60),\n(ringlets:1.30),\n(long hair:1.50),\n\n<neg:\nstraight hair:1.50,\nponytail:1.45,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55\n>', ['ponytail', 'twintails', 'twintail', 'bun', 'braid', 'braids', 'updo', 'drills', 'hime', 'intakes', 'pigtails', 'dreadlocks', 'afro', 'ribbon', 'horns']], ['Hair-Half Up', '<(half updo:1.85)>,\n(one side up:1.35),\n(hair tie:1.25),\n(long hair:1.50),\n\n<neg:\nhair bun:1.45,\ntwintails:1.45,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55\n>', ['ponytail', 'twintails', 'twintail', 'bun', 'braid', 'braids', 'drill', 'drills', 'hime', 'intakes', 'pigtails', 'dreadlocks', 'afro', 'ribbon', 'horns']], ['Hair-Messy', '(messy hair:1.85),\n(hair flaps:1.40),\n(floating hair:1.30),\n(long hair:1.50),\n\n<neg:\nstraight hair:1.55,\nhair bun:1.50,\nponytail:1.45,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55\n>', ['ponytail', 'twintails', 'twintail', 'bun', 'braid', 'braids', 'updo', 'drill', 'drills', 'hime', 'intakes', 'pigtails', 'dreadlocks', 'afro', 'ribbon', 'horns']], ['Hair-Wavy', '(wavy hair:1.85),\n(curly hair:1.45),\n(voluminous:1.20),\n(long hair:1.50),\n\n<neg:\nstraight hair:1.60,\nhair bun:1.45,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55\n>', ['ponytail', 'twintails', 'twintail', 'bun', 'braid', 'braids', 'updo', 'drill', 'drills', 'hime', 'intakes', 'pigtails', 'dreadlocks', 'afro', 'ribbon', 'horns']], ['Hair-Hime', '<(hime cut:1.85)>,\n(blunt bangs:1.50),\n(sidelocks:1.45),\n(straight hair:1.35),\n(long hair:1.50),\n\n<neg:\nmessy hair:1.55,\nhair bun:1.45,\nponytail:1.45,\nshort hair:1.50,\nmedium hair:1.35,\nvery long hair:1.35,\nabsurdly long hair:1.55\n>', ['ponytail', 'twintails', 'twintail', 'bun', 'braid', 'braids', 'updo', 'drill', 'drills', 'intakes', 'pigtails', 'dreadlocks', 'afro', 'ribbon', 'horns']]]


def aplicar(apps, schema_editor):
    Tag = apps.get_model("generate", "Tag")
    Special = apps.get_model("generate", "Special")
    for nombre, prompt, dels in NUEVOS:
        if Special.objects.filter(name=nombre).exists():
            continue
        s = Special.objects.create(name=nombre, tier="tier1", prompt=prompt)
        for t in dels:
            tag, _ = Tag.objects.get_or_create(name=t)
            s.tags_deleted.add(tag)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0086_variante_after"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
