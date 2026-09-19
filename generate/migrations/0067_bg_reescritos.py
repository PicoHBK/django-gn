from django.db import migrations


# Los 24 BG- reescritos. Tres problemas:
#
# 1. NINGUNO tenia un solo peso. Eran tags pelados, asi que el fondo competia
#    de igual a igual con el personaje y la ropa.
#
# 2. TAGS MUERTOS. Once tags con 0 posts en Danbooru, y en tres casos era el
#    tag principal, o sea el special no hacia NADA:
#      BG-Gym          "gym" 0 posts, y "gymnasium" tampoco existe
#      BG-School Hall  "school_hallway" 0 posts, era su unico tag
#      BG-Motel        "motel_room" 0 posts
#    Y ademas: black_alley, shower, shower_room, chapel, mood_lighting,
#    warm_lighting, blue_hour, medical_cabinet, grassland, y el typo
#    "garage_interirlor".
#
# 3. SIN ESTRUCTURA. Ninguno decia si era interior o exterior. Ahora 12
#    llevan indoors (553.760) y 11 outdoors (812.433); BG-Night no lleva
#    ninguno porque es hora del dia, no lugar.
#
# BG-Balcony estaba escrito en prosa -"Open doorway framing the scene,
# wooden edges softly illuminated by a warm..."-. La doc de Illustrious dice
# que los tags rinden mucho mas que el lenguaje natural, asi que se pasa a
# tags.
#
# BG-Gym no tiene tag posible en Danbooru, asi que queda como vestuario:
# locker + bench + tiles. Es lo mas cercano con tags reales.
#
# BG-Rain tenia "wet clothes", que es ropa y no fondo, y ademas AA-Bare All
# se lo borraba. Se reemplaza por wet + puddle.
#
# No se usa depth of field ni blurry background a proposito: desenfocarian
# justo el fondo que estos specials existen para mostrar.
CAMBIOS = [['BG-Alley', 'alley, black alley', '(alley:1.50),\n(outdoors:1.35),\n(city:1.30),\n(night:1.25),\n(wall:1.20)'], ['BG-Azot', 'rooftop, railing, skyline', '(rooftop:1.50),\n(outdoors:1.35),\n(cityscape:1.40),\n(railing:1.30),\n(skyline:1.25)'], ['BG-Balcony', 'Open doorway framing the scene, wooden edges softly illuminated by a warm interior glow.  \nOutside, an expansive sky filled with shimmering stars, gentle streaks across the sky, and drifting glowing particles in deep teal and navy tones.  \nBeyond the doorway, a coastal town with warm lights scattered across rooftops, subtle reflections shimmering on windows.  \nFarther away, a calm coastline outlined by soft atmospheric light.  \nThe composition conveys cinematic depth, a dreamy atmosphere, emotional ambience, and soft painterly textures that emphasize the contrast between the warm interior and the cool exterior environment.', '(balcony:1.50),\n(outdoors:1.35),\n(railing:1.35),\n(window:1.25),\n(curtains:1.20)'], ['BG-Bathroom', 'bathroom, bathtub, shower, shower_room,', '(bathroom:1.50),\n(indoors:1.35),\n(bathtub:1.35),\n(shower head:1.30),\n(tiles:1.25),\n(mirror:1.20)'], ['BG-Classrom', 'classroom', '(classroom:1.50),\n(indoors:1.35),\n(desk:1.35),\n(chalkboard:1.30),\n(window:1.25)'], ['BG-Crunch', 'church, chapel, cathedral, interior, indoors', '(church:1.50),\n(indoors:1.35),\n(cathedral:1.30),\n(stained glass:1.35),\n(pew:1.20)'], ['BG-Dark Room', 'dark room, indoors, bed', '(dark room:1.50),\n(indoors:1.35),\n(bed:1.35),\n(darkness:1.30),\n(night:1.25)'], ['BG-Day', 'day,sky', '(day:1.45),\n(outdoors:1.35),\n(blue sky:1.40),\n(sunlight:1.30),\n(cloud:1.25)'], ['BG-Forest', 'forest, trees, path', '(forest:1.50),\n(outdoors:1.35),\n(tree:1.35),\n(nature:1.30),\n(dappled sunlight:1.25)'], ['BG-Garage', 'garage,garage_interirlor', '(garage:1.50),\n(indoors:1.35),\n(car:1.35),\n(tools:1.25),\n(shelf:1.20)'], ['BG-Garden', 'garden,flowers', '(garden:1.50),\n(outdoors:1.35),\n(flower:1.35),\n(bush:1.30),\n(sunlight:1.25)'], ['BG-Gym', 'gym', '(locker:1.45),\n(indoors:1.35),\n(bench:1.35),\n(tiles:1.25),\n(scenery:1.20)'], ['BG-Hospital Room', "doctor's office, examination table, medical cabinet", '(hospital:1.50),\n(indoors:1.35),\n(bed:1.35),\n(examination table:1.25),\n(window:1.20)'], ['BG-Hotel', 'hotel_room, bed, nightstand, window', '(hotel room:1.50),\n(indoors:1.35),\n(bed:1.40),\n(nightstand:1.30),\n(window:1.25),\n(lamp:1.20)'], ['BG-Kitchen', 'kitchen', '(kitchen:1.50),\n(indoors:1.35),\n(counter:1.30),\n(refrigerator:1.30),\n(sink:1.25)'], ['BG-Living', 'living_room, sofa, table, window', '(living room:1.50),\n(indoors:1.35),\n(couch:1.40),\n(table:1.25),\n(window:1.25)'], ['BG-Motel', 'motel_room, bed, nightstand, lamp, window,mood_lighting, warm_lighting, soft_glow, lamp_light, interior_design', '(hotel room:1.45),\n(indoors:1.35),\n(bed:1.40),\n(lamp:1.30),\n(nightstand:1.25),\n(darkness:1.25)'], ['BG-Night', '<lora:lightingSlider:-0.9>,late night,dark,blue hour', '<lora:lightingSlider:-0.9>,\n(night:1.50),\n(darkness:1.35),\n(dark:1.30)'], ['BG-Park', 'park,tree', '(park:1.50),\n(outdoors:1.35),\n(tree:1.35),\n(bench:1.30),\n(grass:1.30)'], ['BG-Prader', 'field, grassland, flowers', '(field:1.50),\n(outdoors:1.35),\n(grass:1.40),\n(flower:1.30),\n(blue sky:1.25)'], ['BG-Rain', 'rain,wet clothes', '(rain:1.50),\n(outdoors:1.35),\n(wet:1.40),\n(puddle:1.30),\n(rainy:1.20)'], ['BG-School Hall', 'school hallway', '(hallway:1.50),\n(indoors:1.35),\n(school:1.40),\n(locker:1.30),\n(window:1.25)'], ['BG-Sky', 'sky,clouds', '(sky:1.50),\n(outdoors:1.35),\n(cloud:1.40),\n(blue sky:1.35),\n(scenery:1.25)'], ['BG-Snow', 'snow, snowing', '(snow:1.50),\n(outdoors:1.35),\n(snowing:1.40),\n(winter:1.30),\n(tree:1.20)']]


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
        ("generate", "0066_thicc_flat"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
