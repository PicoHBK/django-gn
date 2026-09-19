from django.db import migrations


# Limpieza del grupo DO-, que son las acciones. Cuatro cosas.
#
# 1. SUBGRUPOS. Los 49 sueltos pasan a nueve:
#      DO-Arms/  brazos y manos      DO-Hold/  sosteniendo algo
#      DO-Face/  boca y cara         DO-Ges/   gestos
#      DO-Body/  cuerpo              DO-Pair/  de a dos
#      DO-Home/  domesticas          DO-Lewd/  explicitas
#      DO-Dark/  el del cuchillo, que no encaja en ningun otro lado
#
# 2. FUGA DE TIER. Ocho specials explicitos estaban en TIER2, que el front
#    muestra casi a todos: fellatio, licking_penis, masturbacion x2, dildo
#    x2, groping bajo la ropa y undressing con pussy. Mas el self wedgie.
#    Van a tier3 los de juguete y solo, a tier4 los de pareja.
#
# 3. PESOS. 47 de los 50 no tenian ninguno. Se le pone 1.45 al primer tag de
#    cada uno, que es el que define la accion.
#
# 4. 24 ACCIONES NUEVAS, por volumen real: v (238.895), holding food
#    (155.700), holding cup (112.018), hand on own chest (90.075), hand in
#    pocket (53.244), finger to mouth (52.500), heart hands (41.320), waving
#    (40.818), selfie (32.084), licking lips (31.193), adjusting hair
#    (27.616), reading (23.888), thumbs up (20.334), pointing at viewer
#    (17.851), biting (17.855), tying hair (13.056), covering face (10.408).
#
# Cinco que parecian obvios NO existen: covering_mouth, adjusting_glasses,
# peace_sign, checking_phone y texting. El de la V es solo "v".
SUBGRUPOS = [[469, 'DO-Arms Behind', 'DO-Arms/Behind', 'arms behind back', '(arms behind back:1.45)', 'tier2', 'tier2'], [452, 'DO-Arms Crossed', 'DO-Arms/Crossed', 'arms crossed', '(arms crossed:1.45)', 'tier2', 'tier2'], [500, 'DO-Arms behind H', 'DO-Arms/Behind Head', 'arms behind head', '(arms behind head:1.45)', 'tier2', 'tier2'], [609, 'DO-Arms up', 'DO-Arms/Up', 'arms up', '(arms up:1.45)', 'tier2', 'tier2'], [583, 'DO-Hands Hips', 'DO-Arms/Hips', 'hands on own hips', '(hands on own hips:1.45)', 'tier2', 'tier2'], [449, 'DO-Hands Embb', 'DO-Arms/Cheeks', 'hands on own cheeks,hands on own face', '(hands on own cheeks:1.45),hands on own face', 'tier2', 'tier2'], [447, 'DO-Index Fingers Together', 'DO-Arms/Index', 'index fingers together', '(index fingers together:1.45)', 'tier2', 'tier2'], [470, 'DO-Holding Con', 'DO-Hold/Condom', 'holding condom', '(holding condom:1.45)', 'tier2', 'tier2'], [480, 'DO-Holding Lollipop', 'DO-Hold/Lollipop', 'holding lollipop', '(holding lollipop:1.45)', 'tier2', 'tier2'], [555, 'DO-Holding Pillow', 'DO-Hold/Pillow', 'holding pillow', '(holding pillow:1.45)', 'tier2', 'tier2'], [511, 'DO-Holding Thong', 'DO-Hold/Thong', 'holding thong in hand', '(holding thong in hand:1.45)', 'tier2', 'tier2'], [551, 'DO-Holding wood', 'DO-Hold/Spoon', 'wooden spoon,holding one wooden spoon', '(wooden spoon:1.45),holding one wooden spoon', 'tier2', 'tier2'], [386, 'DO-Test P', 'DO-Hold/Test', 'holding pregnancy test,<neg:pregnant girl>', '(holding pregnancy test:1.45),<neg:pregnant girl>', 'tier2', 'tier2'], [489, 'DO-Carryn B', 'DO-Hold/Baby', 'carrying baby,mother and child,baby sleeping', '(carrying baby:1.45),mother and child,baby sleeping', 'tier2', 'tier2'], [553, 'DO-Giggle', 'DO-Face/Giggle', 'hand over mouth, giggle', '(hand over mouth:1.45),giggle', 'tier2', 'tier2'], [467, 'DO-HandGag', 'DO-Face/Gag', "hand over another's mouth,covering another's mouth", "(hand over another's mouth:1.45),covering another's mouth", 'tier2', 'tier2'], [688, 'DO-Shushing', 'DO-Face/Shush', 'shushing', '(shushing:1.45)', 'tier2', 'tier2'], [448, 'DO-Singing', 'DO-Face/Sing', 'musical note, humming', '(musical note:1.45),humming', 'tier2', 'tier2'], [399, 'DO-Talking', 'DO-Face/Talk', 'talk,talking', '(talk:1.45),talking', 'tier2', 'tier2'], [482, 'DO-Swalloging', 'DO-Face/Swallow', 'swallowing', '(swallowing:1.45)', 'tier2', 'tier2'], [492, 'DO-Suck Banana', 'DO-Face/Banana', 'eating banana,small banana,holding banana,open mouth', '(eating banana:1.45),small banana,holding banana,open mouth', 'tier2', 'tier2'], [585, 'DO-Eating Banana', 'DO-Face/Banana Lora', '<lora:Eating_Banana:1>,banana, eating banana,banana in mouth', '<lora:Eating_Banana:1>,banana,eating banana,banana in mouth', 'tier2', 'tier2'], [578, 'DO-Clapping', 'DO-Ges/Clap', 'clapping', '(clapping:1.45)', 'tier2', 'tier2'], [472, 'DO-Salute', 'DO-Ges/Salute', 'salute', '(salute:1.45)', 'tier2', 'tier2'], [575, 'DO-Offering', 'DO-Ges/Offer', 'reaching towards viewer,offering hand', '(reaching towards viewer:1.45),offering hand', 'tier2', 'tier2'], [800, 'DO-Trucking Hair', 'DO-Ges/Tuck Hair', 'tucking_hair', '(tucking_hair:1.45)', 'tier2', 'tier2'], [477, 'DO-Bent Over', 'DO-Body/Bent', 'bent over', '(bent over:1.45)', 'tier2', 'tier2'], [474, 'DO-Head Back', 'DO-Body/Head Back', 'head back', '(head back:1.45)', 'tier2', 'tier2'], [504, 'DO-Standing Split', 'DO-Body/Split', 'FFF_standing_split', '(FFF_standing_split:1.45)', 'tier2', 'tier2'], [496, 'DO-Cammy Stretch', 'DO-Body/Stretch', 'cammystretch, solo, stretching, standing, leaning forward, arms up, interlocked fingers, <lora:Cammy_Stretch__Pose_Trend_Concept__IllustriousXL_and_NoobAI:.7>', '(cammystretch:1.45),solo,stretching,standing,leaning forward,arms up,interlocked fingers,<lora:Cammy_Stretch__Pose_Trend_Concept__IllustriousXL_and_NoobAI:.7>', 'tier2', 'tier2'], [640, 'DO-Putting Shoe', 'DO-Body/Shoe', 'putting on footwear,sitting', '(putting on footwear:1.45),sitting', 'tier2', 'tier2'], [455, 'DO-Face To Face', 'DO-Pair/Face', 'face to face,(faceless:1.4)', 'face to face,(faceless:1.4)', 'tier2', 'tier2'], [453, 'DO-Income Hug', 'DO-Pair/Hug', 'incoming hug', '(incoming hug:1.45)', 'tier2', 'tier2'], [613, 'DO-Income Kiss', 'DO-Pair/Kiss Inc', 'incoming kiss ,puckered lips', '(incoming kiss:1.45),puckered lips', 'tier2', 'tier2'], [454, 'DO-Kiss', 'DO-Pair/Kiss', 'kiss,closed eyes', '(kiss:1.45),closed eyes', 'tier2', 'tier2'], [436, 'DO-Kiss French', 'DO-Pair/French', 'french kiss, kiss, saliva,bald,faceless', '(french kiss:1.45),kiss,saliva,bald,faceless', 'tier2', 'tier2'], [446, 'DO-Kiss Surp', 'DO-Pair/Surprise', 'surprise kiss', '(surprise kiss:1.45)', 'tier2', 'tier2'], [550, 'DO-Coocking', 'DO-Home/Cook', 'cooking', '(cooking:1.45)', 'tier2', 'tier2'], [721, 'DO-Watch Tv', 'DO-Home/Tv', 'watching_television', '(watching_television:1.45)', 'tier2', 'tier1'], [547, 'DO-Fing Assisted', 'DO-Lewd/Groping', 'groping hand under clothes', '(groping hand under clothes:1.45)', 'tier4', 'tier2'], [643, 'DO-Lick D', 'DO-Lewd/Lick Dildo', 'simulated fellatio,dildo', '(simulated fellatio:1.45),dildo', 'tier3', 'tier2'], [766, 'DO-Lick P', 'DO-Lewd/Lick Penis', 'licking_penis', '(licking_penis:1.45)', 'tier4', 'tier2'], [676, 'DO-Masta Fem', 'DO-Lewd/Mast', '(female masturbation:1.2), masturbation', '(female masturbation:1.2), masturbation', 'tier3', 'tier2'], [381, 'Do-Masta F', 'DO-Lewd/Mast 2', 'female masturbation', '(female masturbation:1.45)', 'tier3', 'tier2'], [645, 'DO-Simulation Dild', 'DO-Lewd/Sim Dildo', 'simulation fellation,licking dildo,pink dildo', '(simulation fellation:1.45),licking dildo,pink dildo', 'tier3', 'tier2'], [655, 'DO-Undressing', 'DO-Lewd/Undress', 'undressing,breast, pussy,clothes lift', '(undressing:1.45),breast,pussy,clothes lift', 'tier4', 'tier2'], [720, 'DOS-Fell', 'DO-Lewd/Fellatio', 'fellatio, oral,on couch,lying', '(fellatio:1.45),oral,on couch,lying', 'tier4', 'tier2'], [794, 'DO-SelfWeding', 'DO-Lewd/Wedgie', '<lora:LoRASelfWedgieAssIL11:.9>,self wedgie', '<lora:LoRASelfWedgieAssIL11:.9>,self wedgie', 'tier3', 'tier2'], [646, 'DO-Imminent Sui', 'DO-Dark/Knife', '(imminent suicide:1.4),holding knife,hands up', '(imminent suicide:1.4),holding knife,hands up', 'tier2', 'tier2']]

NUEVOS = [['DO-Arms/Thumbs', '(thumbs up:1.45)'], ['DO-Arms/V', '(v:1.45)'], ['DO-Arms/Heart', '(heart hands:1.50)'], ['DO-Arms/Pocket', '(hand in pocket:1.45)'], ['DO-Arms/Chest', '(hand on own chest:1.45)'], ['DO-Ges/Wave', '(waving:1.45)'], ['DO-Ges/Beckon', '(beckoning:1.50)'], ['DO-Ges/Point', '(pointing at viewer:1.45)'], ['DO-Ges/Ok', '(ok sign:1.50)'], ['DO-Face/Finger', '(finger to mouth:1.50)'], ['DO-Face/Lick Lips', '(licking lips:1.50)'], ['DO-Face/Blow Kiss', '(blowing kiss:1.50)'], ['DO-Face/Cover', '(covering face:1.50)'], ['DO-Face/Bite', '(biting:1.45)'], ['DO-Hold/Cup', '(holding cup:1.45)'], ['DO-Hold/Food', '(holding food:1.45)'], ['DO-Home/Selfie', '(selfie:1.50)'], ['DO-Home/Read', '(reading:1.45)'], ['DO-Home/Makeup', '(applying makeup:1.50)'], ['DO-Home/Brush', '(brushing hair:1.50)'], ['DO-Body/Adjust', '(adjusting clothes:1.45)'], ['DO-Body/Hair', '(adjusting hair:1.45)'], ['DO-Body/Tie Hair', '(tying hair:1.50)'], ['DO-Body/Stretch 2', '(stretching:1.45)']]


def aplicar(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    for pk, _viejo, nuevo, _vp, np_, tier, _vt in SUBGRUPOS:
        s = Special.objects.filter(pk=pk).first()
        if s is not None:
            s.name, s.prompt, s.tier = nuevo, np_, tier
            s.save(update_fields=["name", "prompt", "tier"])
    for nombre, prompt in NUEVOS:
        if Special.objects.filter(name=nombre).exists():
            continue
        Special.objects.create(name=nombre, tier="tier2", prompt=prompt)


def revertir(apps, schema_editor):
    Special = apps.get_model("generate", "Special")
    Special.objects.filter(name__in=[n[0] for n in NUEVOS]).delete()
    for pk, viejo, _nuevo, vp, _np, _tier, vt in SUBGRUPOS:
        s = Special.objects.filter(pk=pk).first()
        if s is not None:
            s.name, s.prompt, s.tier = viejo, vp, vt
            s.save(update_fields=["name", "prompt", "tier"])


class Migration(migrations.Migration):

    dependencies = [
        ("generate", "0082_tier5_close"),
    ]

    operations = [
        migrations.RunPython(aplicar, revertir),
    ]
