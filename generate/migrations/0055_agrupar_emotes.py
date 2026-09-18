from django.db import migrations


# Los emotes pasan a grupos, con UN solo guion como Crazy-Juri:
#
#   Ext-    extasis, el grupo nuevo: ahegao, torogao, orgasm, fucked silly,
#           heart-shaped pupils, empty eyes, drooling, steaming body
#   Smile-  sonrisa en todas sus formas, de happy a evil
#   Cry-    llanto
#   Shy-    verguenza
#   Mad-    enojo y asco
#   Fear-   miedo y sorpresa
#   Rest-   sueno y borrachera
#   Sad-    tristeza
#   Null-   sin expresion, pensando, confundida
#   Eto-    el lora de ah-eto-bleh
#
# 21 emotes nuevos. Los de Ext- salen del vocabulario real: orgasm (25.799),
# female orgasm (14.983), fucked silly (10.635), heart-shaped pupils
# (120.948), empty eyes (50.591), drooling (80.785), steaming body (43.004).
#
# "eyes rolled back" NO existe en Danbooru, 0 posts. El que sirve para ese
# efecto es "rolling eyes" (23.286), que ya usa Ext-Silly.
RENOMBRAR = [[60, 'Ahegao-High', 'Ext-Ahegao'], [61, 'Ahegao-Normal', 'Ext-Ahegao Soft'], [50, 'Toro', 'Ext-Torogao'], [44, 'Crazy', 'Ext-Crazy'], [68, 'Crazy-Juri', 'Ext-Crazy Juri'], [29, 'Smile', 'Smile-Gen'], [38, 'Grin', 'Smile-Grin'], [53, 'Laugh', 'Smile-Laugh'], [51, 'Excited', 'Smile-Excited'], [59, 'Evil Smile', 'Smile-Evil'], [56, 'N Smile', 'Smile-Nervous'], [65, 'Smile-Sed', 'Smile-Seductive'], [64, 'Smile S', 'Smile-Bite'], [67, 'Lip Biting', 'Smile-Lip Bite'], [30, 'Crying', 'Cry-Gen'], [41, 'Grin-C', 'Cry-Grin'], [57, 'Cry Em', 'Cry-Embarrassed'], [42, 'Embarrassed', 'Shy-Embarrassed'], [62, 'Bashful', 'Shy-Bashful'], [40, 'Ave', 'Shy-Averting'], [45, 'Pout', 'Shy-Pout'], [55, 'Hmph', 'Mad-Annoyed'], [35, 'Defiance', 'Mad-Defiant'], [37, 'Disgust-1', 'Mad-Disgust Low'], [47, 'Disgust-2', 'Mad-Disgust Mid'], [48, 'Disgust-3', 'Mad-Disgust High'], [39, 'Scared', 'Fear-Scared'], [63, 'Shock', 'Fear-Shocked'], [31, 'Surprised', 'Fear-Surprised'], [43, 'Sleep', 'Rest-Sleeping'], [54, 'Sleepy', 'Rest-Sleepy'], [36, 'Yawning', 'Rest-Yawn'], [33, 'Sad', 'Sad-Gen'], [49, 'NaN', 'Null-Neutral'], [66, 'Expressionless', 'Null-Expressionless'], [46, 'Eto', 'Eto-Gen']]

NUEVOS = [['Ext-Orgasm', '(orgasm:1.55),(female orgasm:1.40),(trembling:1.30),(nose blush:1.25)'], ['Ext-Silly', '(fucked silly:1.60),(rolling eyes:1.45),(tongue out:1.30),(drooling:1.30)'], ['Ext-Heart', '(heart-shaped pupils:1.55),(blush:1.35)'], ['Ext-Blank', '(empty eyes:1.50),(blank eyes:1.40),(trembling:1.25)'], ['Ext-Drool', '(drooling:1.55),(saliva:1.40),(tongue out:1.30)'], ['Ext-Steam', '(steaming body:1.50),(nose blush:1.40),(trembling:1.25)'], ['Smile-Smug', '(smug:1.50),(grin:1.30)'], ['Smile-Happy', '(happy:1.45),(smile:1.35),(closed eyes:1.20)'], ['Smile-Wink', '(one eye closed:1.50),(smile:1.35)'], ['Smile-Lick', '(licking lips:1.50),(tongue out:1.30)'], ['Cry-Scream', '(screaming:1.50),(tears:1.35),(clenched teeth:1.25)'], ['Shy-Gen', '(shy:1.50),(light blush:1.35)'], ['Shy-Flustered', '(flustered:1.50),(full-face blush:1.40),(averting eyes:1.25)'], ['Mad-Angry', '(angry:1.50),(frown:1.35),(clenched teeth:1.25)'], ['Mad-Serious', '(serious:1.50),(frown:1.25)'], ['Mad-Shout', '(shouting:1.50),(open mouth:1.35),(angry:1.30)'], ['Fear-Worried', '(worried:1.50),(nervous:1.35),(sweatdrop:1.25)'], ['Rest-Drunk', '(drunk:1.50),(blush:1.35),(half-closed eyes:1.25)'], ['Sad-Bored', '(bored:1.50),(expressionless:1.25)'], ['Null-Thinking', '(thinking:1.50),(closed eyes:1.20)'], ['Null-Confused', '(confused:1.50),(sweatdrop:1.25)']]


def aplicar(apps, schema_editor):
    Emote = apps.get_model("generate", "Emote")
    for pk, _viejo, nuevo in RENOMBRAR:
        e = Emote.objects.filter(pk=pk).first()
        if e is not None:
            e.name = nuevo
            e.save(update_fields=["name"])
    for nombre, prompt in NUEVOS:
        if Emote.objects.filter(name=nombre).exists():
            continue
        Emote.objects.create(name=nombre, prompt=prompt)


def revertir(apps, schema_editor):
    Emote = apps.get_model("generate", "Emote")
    Emote.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()
    for pk, viejo, _nuevo in RENOMBRAR:
        e = Emote.objects.filter(pk=pk).first()
        if e is not None:
            e.name = viejo
            e.save(update_fields=["name"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0054_only_seduct_sin_calzado"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
