from django.db import migrations


# Limpieza del modulo de Emote. 34 de 36 tocados; quedan como estan solo Eto
# (46) y Crazy-Juri (68), que ya estaban bien.
#
# TAGS QUE NO EXISTEN. Cuatro emotes apuntaban a tags con 0 posts en Danbooru:
#   defiance  -> se reemplaza por determined + serious + frown
#   laugh     -> laughing (23.000)
#   shocked   -> surprised + wide-eyed + open mouth
#   bashful   -> light blush + averting eyes + parted lips
# Y tres parciales: frowning -> frown, teary_eyes -> tears,
# lip_biting -> biting own lip.
#
# PESOS ROTOS. Disgust-1, 2 y 3 escribian "disgust:.6" SIN parentesis. En
# A1111 eso no es un peso, es texto literal: los tres estaban sin efecto.
#
# SIN PESO. 30 de 36 eran tags pelados. Ahora todos llevan peso, el principal
# entre 1.35 y 1.60 segun cuanto tenga que dominar la cara.
#
# PROMPT VACIO. El emote "NaN" (49) tenia como prompt una sola coma, que suma
# un token vacio al prompt final. Pasa a llamarse Neutral con expressionless.
#
# DUPLICADO. Ahegao-High y Ahegao-Normal tenian el prompt identico, el mismo
# lora en :2. Ahora Normal va en :1, que es lo que el nombre promete: el lora
# es un slider.
#
# CONTRADICCION. Smile-Sed pedia "seductive, confident, mischievous, hesitant,
# worried" todo junto. Seductora y preocupada a la vez se anulan. Queda como
# Seductive con seductive smile + smug + biting own lip.
#
# Tambien se le saca "solo" a Surprised: es un tag de composicion, no de cara,
# y no tiene nada que hacer en un emote.
#
# Ojo: esto renombra emotes y views.py los busca por NOMBRE.
CAMBIOS = [[29, 'Smile', 'smile', 'Smile', '(smile:1.35)'], [30, 'Crying', 'crying,tears', 'Crying', '(crying:1.45),(tears:1.30)'], [31, 'Surprised', '(surprised:1),wide-eyed,o_o,solo', 'Surprised', '(surprised:1.45),(wide-eyed:1.30),(o_o:1.20)'], [33, 'Sad', 'sad', 'Sad', '(sad:1.45),(frown:1.25)'], [35, 'Defiance', 'defiance', 'Defiant', '(determined:1.50),(serious:1.30),(frown:1.20)'], [36, 'Yawning', 'yawning', 'Yawning', '(yawning:1.45),(open mouth:1.20)'], [37, 'Disgust-1', 'disgust:.6', 'Disgust Low', '(disgust:1.20)'], [38, 'Grin', 'grin', 'Grin', '(grin:1.35)'], [39, 'Scared', 'scared', 'Scared', '(scared:1.45),(wide-eyed:1.25)'], [40, 'Ave', '(averting eyes:1.3),blush, half-closed eyes', 'Averting Eyes', '(averting eyes:1.40),(blush:1.25),(half-closed eyes:1.20)'], [41, 'Grin-C', 'grin,tears', 'Grin Crying', '(grin:1.35),(tears:1.30)'], [43, 'Sleep', 'sleep,closed eyes', 'Sleeping', '(sleeping:1.45),(closed eyes:1.30)'], [45, 'Pout', ':t,pout', 'Pout', '(pout:1.45),:t'], [47, 'Disgust-2', 'disgust:.8,shaded face', 'Disgust Mid', '(disgust:1.40),(shaded face:1.20)'], [48, 'Disgust-3', 'disgust:1.4,angry,shaded face', 'Disgust High', '(disgust:1.60),(angry:1.30),(shaded face:1.25)'], [49, 'NaN', ',', 'Neutral', '(expressionless:1.30)'], [50, 'Toro', 'torogao', 'Torogao', '(torogao:1.50)'], [51, 'Excited', 'excited', 'Excited', '(excited:1.50),(open mouth:1.20)'], [53, 'Laugh', 'laugh', 'Laughing', '(laughing:1.45),(open mouth:1.25)'], [54, 'Sleepy', 'sleepy', 'Sleepy', '(sleepy:1.45),(half-closed eyes:1.30)'], [55, 'Hmph', 'pout, looking away, annoyed, tsundere', 'Annoyed', '(annoyed:1.45),(pout:1.30),(looking away:1.20),(tsundere:1.15)'], [56, 'N Smile', 'nervous smile, sweatdrop, embarrassed, worried', 'Nervous Smile', '(nervous:1.45),(smile:1.25),(sweatdrop:1.30),(embarrassed:1.20)'], [57, 'Cry Em', 'embarrassed, pouting, teary-eyed, frowning', 'Crying Embarrassed', '(embarrassed:1.40),(pout:1.25),(tears:1.35),(frown:1.20)'], [59, 'Evil Smile', 'evil smile,shaded face', 'Evil Smile', '(evil smile:1.50),(shaded face:1.25)'], [62, 'Bashful', '(bashful:1.4)', 'Bashful', '(light blush:1.45),(averting eyes:1.35),(parted lips:1.20)'], [63, 'Shock', '(shocked:1.1)', 'Shocked', '(surprised:1.60),(wide-eyed:1.40),(open mouth:1.30)'], [64, 'Smile S', 'smile, (lip_biting:1.5)', 'Smile Biting Lip', '(smile:1.30),(biting own lip:1.50)'], [65, 'Smile-Sed', 'seductive,confident,mischievous,hesitant,worried,biting_own_lip', 'Seductive', '(seductive smile:1.50),(smug:1.25),(biting own lip:1.30)'], [66, 'Expressionless', 'expressionless', 'Expressionless', '(expressionless:1.45)'], [42, 'Embarrassed', '<lora:ShySlider:1>,blushing,embarrassed', 'Embarrassed', '<lora:ShySlider:1>,(blush:1.35),(embarrassed:1.40)'], [44, 'Crazy', 'gesugao, crazy smile, crazy eyes glowing,<lora:Crazy_Expression_Crazy_Face_Creepy_Expression_Creepy_Face_Gesugao_PonyILSDSDXL:.05>', 'Crazy', '<lora:Crazy_Expression_Crazy_Eyes:1>,(gesugao:1.40),(crazy smile:1.50),(crazy eyes:1.30),(glowing eyes:1.20)'], [60, 'Ahegao-High', '<lora:StS_IllustXL_Ahegao_Slider_v0.9:2>', 'Ahegao High', '<lora:StS_IllustXL_Ahegao_Slider_v0.9:2>,(ahegao:1.50)'], [61, 'Ahegao-Normal', '<lora:StS_IllustXL_Ahegao_Slider_v0.9:2>', 'Ahegao Normal', '<lora:StS_IllustXL_Ahegao_Slider_v0.9:1>,(ahegao:1.25)'], [67, 'Lip Biting', '<lora:lipBite_v1_r:.7>,biting own lip,seductive,confident,mischievous,hesitant,worried', 'Lip Biting', '<lora:lipBite_v1_r:.7>,(biting own lip:1.50),(seductive smile:1.30)']]


def _set(apps, i_nombre, i_prompt):
    Emote = apps.get_model("generate", "Emote")
    for c in CAMBIOS:
        e = Emote.objects.filter(pk=c[0]).first()
        if e is None:
            continue
        e.name, e.prompt = c[i_nombre], c[i_prompt]
        e.save(update_fields=["name", "prompt"])


def aplicar(apps, schema_editor):
    _set(apps, 3, 4)


def revertir(apps, schema_editor):
    _set(apps, 1, 2)


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0051_plegar_sueltas_tier1"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
