from django.db import migrations


# DA: fuerza que los DOS personajes sean de piel morena.
#
# Es de las combinaciones mas raras que hay: dark-skinned_female junto a
# dark-skinned_male son 6.327 posts en Danbooru. El modelo tira por defecto
# al contraste, y eso tiene nombre propio: "interracial" (35.834 posts) se
# etiqueta justo cuando uno es oscuro y el otro claro. Por eso va negado
# fuerte: es el tag que compite, no un sinonimo de piel clara.
#
# Solo toca la piel. El acto lo sigue poniendo la pose, asi que DA se combina
# con cualquiera de tier2 para arriba.
NOMBRE = "DA"

PROMPT = """(dark-skinned female:1.75),
(dark-skinned male:1.75),
(dark skin:1.60),
(very dark skin:1.25),

<neg:
interracial:1.65,
pale skin:1.60,
white skin:1.55,
tanlines:1.30
>"""


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.update_or_create(
        name=NOMBRE, defaults={"prompt": PROMPT, "tier": "tier2"}
    )


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name=NOMBRE).delete()


class Migration(migrations.Migration):

    dependencies = [("generate", "0095_squat_pulido")]

    operations = [migrations.RunPython(aplicar, revertir)]
