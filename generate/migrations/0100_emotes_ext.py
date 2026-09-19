from django.db import migrations


# 12 emotes nuevos para el grupo Ext-, que es el del ambito subido de tono.
#
# El que pidio el usuario es Ext-Surprise: la cara del momento de la
# penetracion sorpresa. Ya existe Fear-Shocked con surprised + wide-eyed +
# open mouth, pero ese lee como miedo; este suma nose blush, full-face blush
# y trembling para que lea como placer, no como susto.
#
# Descartados por no existir (0 posts): bedroom_eyes, pained_expression,
# defeated, pleasure.
# Descartados por ser demasiado raros para que el modelo los haya aprendido:
# ecstasy (166), gasp (320), begging (797), sobbing (892).
NUEVOS = [
    # el pedido: sorpresa de placer, no de miedo
    ("Ext-Surprise", "(surprised:1.55),(wide-eyed:1.40),(open mouth:1.40),"
                     "(nose blush:1.40),(full-face blush:1.30),(trembling:1.30)"),
    # boca muy abierta, garganta a la vista
    ("Ext-Gasp", "(open mouth:1.50),(uvula:1.45),(surprised:1.30),"
                 "(heavy breathing:1.30)"),
    ("Ext-Moan", "(moaning:1.60),(open mouth:1.40),(half-closed eyes:1.30),"
                 "(nose blush:1.25)"),
    ("Ext-Heart Moan", "(heart-shaped pupils:1.50),(moaning:1.45),"
                       "(open mouth:1.30),(full-face blush:1.30)"),
    ("Ext-Naughty", "(naughty face:1.60),(smirk:1.30),(half-closed eyes:1.25)"),
    ("Ext-Smirk", "(smirk:1.55),(naughty face:1.35),(half-closed eyes:1.30)"),
    ("Ext-Aroused", "(aroused:1.60),(heavy breathing:1.40),(nose blush:1.35),"
                    "(half-closed eyes:1.25)"),
    # la cara apretada, de aguantar
    ("Ext-Wince", "(wince:1.60),(furrowed brow:1.40),(clenched teeth:1.30),"
                  "(closed eyes:1.20)"),
    ("Ext-Pain", "(grimace:1.55),(furrowed brow:1.45),(clenched teeth:1.40),"
                 "(tearing up:1.25)"),
    # lagrimas de placer, no de tristeza: por eso el blush y no el frown
    ("Ext-Tears", "(tearing up:1.55),(full-face blush:1.35),"
                  "(half-closed eyes:1.25),(nose blush:1.25)"),
    ("Ext-Shame", "(humiliation:1.60),(embarrassed:1.40),(full-face blush:1.35),"
                  "(averting eyes:1.25)"),
    ("Ext-Break", "(mind break:1.65),(empty eyes:1.40),(rolling eyes:1.30),"
                  "(drooling:1.25)"),
]


def aplicar(apps, schema_editor):
    Emote = apps.get_model("generate", "Emote")
    for nombre, prompt in NUEVOS:
        Emote.objects.update_or_create(name=nombre, defaults={"prompt": prompt})


def revertir(apps, schema_editor):
    Emote = apps.get_model("generate", "Emote")
    Emote.objects.filter(name__in=[n for n, _ in NUEVOS]).delete()


class Migration(migrations.Migration):

    dependencies = [("generate", "0099_pregslider_etapas")]

    operations = [migrations.RunPython(aplicar, revertir)]
