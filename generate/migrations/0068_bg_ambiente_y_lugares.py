from django.db import migrations


# BG-Amb/: subgrupo nuevo para lo que no es un lugar sino el ambiente. Los
# cinco que ya eran clima u hora del dia se mudan ahi -Rain, Snow, Night,
# Day y Sky- y se suman doce.
#
# Los de ambiente son los unicos BG que SI llevan depth of field y bokeh
# (Fog y Particles): ahi el desenfoque es el efecto buscado, al reves que en
# los de lugar, donde taparia lo que el special existe para mostrar.
#
# 18 lugares nuevos, por volumen real: beach (133.363), stairs (36.866),
# mountain (32.387), pool (26.598), onsen (24.920), bedroom (20.868), ruins
# (15.056), street (11.692), train interior (11.560), river (10.928), stage
# (9.484), library (7.178), bar (6.837), shrine (6.303), car interior
# (6.231), restaurant (5.408), cafe (4.651) y office (4.253).
#
# Descartados por volumen: nightclub (354), laundromat (611), supermarket
# (721), parking lot (698), attic (97), basement (118), barn (514) y
# greenhouse (884). Y "hot spring" no existe, el real es "onsen".
#
# Los parentesis de "bar (place)" y "star (sky)" van escapados, si no A1111
# los lee como grupos de enfasis.
MOVER = {'BG-Rain': 'BG-Amb/Rain', 'BG-Snow': 'BG-Amb/Snow', 'BG-Night': 'BG-Amb/Night', 'BG-Day': 'BG-Amb/Day', 'BG-Sky': 'BG-Amb/Sky'}

NUEVOS = [['BG-Amb/Sunset', '(sunset:1.50),\n(outdoors:1.35),\n(orange sky:1.35),\n(twilight:1.30),\n(lens flare:1.25)'], ['BG-Amb/Sunrise', '(sunrise:1.50),\n(outdoors:1.35),\n(dawn:1.35),\n(sunbeam:1.30),\n(cloud:1.25)'], ['BG-Amb/Fog', '(fog:1.55),\n(outdoors:1.35),\n(overcast:1.30),\n(depth of field:1.25)'], ['BG-Amb/Wind', '(wind:1.50),\n(outdoors:1.35),\n(falling petals:1.35),\n(motion blur:1.20)'], ['BG-Amb/Storm', '(lightning:1.50),\n(storm:1.45),\n(outdoors:1.35),\n(rain:1.40),\n(dark clouds:1.30)'], ['BG-Amb/Moonlight', '(moonlight:1.50),\n(full moon:1.45),\n(night:1.40),\n(outdoors:1.35),\n(darkness:1.25)'], ['BG-Amb/Stars', '(starry sky:1.55),\n(night:1.40),\n(outdoors:1.35),\n(star \\(sky\\):1.25)'], ['BG-Amb/Fireworks', '(fireworks:1.55),\n(night:1.40),\n(outdoors:1.35),\n(light particles:1.25)'], ['BG-Amb/Sakura', '(cherry blossoms:1.55),\n(outdoors:1.35),\n(falling petals:1.45),\n(petals:1.35),\n(tree:1.25)'], ['BG-Amb/Autumn', '(autumn leaves:1.55),\n(outdoors:1.35),\n(autumn:1.35),\n(tree:1.30),\n(orange theme:1.20)'], ['BG-Amb/Particles', '(light particles:1.55),\n(lens flare:1.40),\n(backlighting:1.35),\n(bokeh:1.25)'], ['BG-Amb/Sunbeam', '(sunbeam:1.50),\n(dappled sunlight:1.45),\n(sunlight:1.35),\n(light rays:1.30)'], ['BG-Beach', '(beach:1.50),\n(outdoors:1.35),\n(ocean:1.40),\n(sand:1.35),\n(horizon:1.25)'], ['BG-Pool', '(pool:1.50),\n(water:1.40),\n(outdoors:1.35),\n(poolside:1.30),\n(reflection:1.20)'], ['BG-Onsen', '(onsen:1.50),\n(water:1.35),\n(steam:1.35),\n(rock:1.25),\n(outdoors:1.35)'], ['BG-Bedroom', '(bedroom:1.50),\n(indoors:1.35),\n(bed:1.40),\n(window:1.25),\n(lamp:1.20)'], ['BG-Library', '(library:1.50),\n(indoors:1.35),\n(bookshelf:1.40),\n(book:1.30),\n(desk:1.25)'], ['BG-Cafe', '(cafe:1.50),\n(indoors:1.35),\n(table:1.35),\n(chair:1.30),\n(window:1.25)'], ['BG-Restaurant', '(restaurant:1.50),\n(indoors:1.35),\n(table:1.35),\n(chair:1.30),\n(plate:1.20)'], ['BG-Office', '(office:1.50),\n(indoors:1.35),\n(desk:1.40),\n(computer:1.30),\n(window:1.25)'], ['BG-Bar', '(bar \\(place\\):1.50),\n(indoors:1.35),\n(counter:1.35),\n(bottle:1.30),\n(dim lighting:1.25)'], ['BG-Stage', '(stage:1.50),\n(indoors:1.35),\n(stage lights:1.40),\n(spotlight:1.35),\n(microphone:1.20)'], ['BG-Train', '(train interior:1.50),\n(indoors:1.35),\n(window:1.35),\n(seat:1.30),\n(handrail:1.20)'], ['BG-Car', '(car interior:1.50),\n(indoors:1.35),\n(seat:1.35),\n(window:1.30),\n(steering wheel:1.20)'], ['BG-Shrine', '(shrine:1.50),\n(outdoors:1.35),\n(torii:1.40),\n(stairs:1.25),\n(tree:1.20)'], ['BG-Ruins', '(ruins:1.50),\n(outdoors:1.35),\n(rubble:1.35),\n(overgrown:1.30),\n(scenery:1.25)'], ['BG-Mountain', '(mountain:1.50),\n(outdoors:1.35),\n(scenery:1.40),\n(sky:1.30),\n(cloud:1.25)'], ['BG-River', '(river:1.50),\n(outdoors:1.35),\n(water:1.40),\n(tree:1.30),\n(rock:1.20)'], ['BG-Street', '(street:1.50),\n(outdoors:1.35),\n(city:1.40),\n(road:1.30),\n(building:1.25)'], ['BG-Stairs', '(stairs:1.50),\n(indoors:1.35),\n(railing:1.35),\n(wall:1.25)']]


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
        Special.objects.create(name=nombre, tier="tier4", prompt=prompt)


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
        ("generate", "0067_bg_reescritos"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
