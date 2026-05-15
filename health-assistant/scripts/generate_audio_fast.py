"""
Fast audio generation — queues all files in one pyttsx3 session.
"""
import os, pyttsx3

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'public', 'audio')

TIPS = {
    'malaria':     {'en': "Malaria prevention. Sleep under a mosquito net every night. Remove standing water near your home. If you have fever or chills, visit your health center immediately.", 'am': "ወባ መከላከያ። በየሌሊቱ ከወባ አጥር ስር ተኙ። ቤትዎ አቅራቢያ ቆሞ ያለ ውሃ ያስወግዱ። ትኩሳት ካለዎ ወዲያውኑ ጤና ጣቢያ ይሂዱ።", 'om': "Ittisa malaariyaa. Halkan hunda jalatti neetii malaariyaa ciisi. Bishaan dhaabbate kaasi. Yoo ho'aa qabaatte, giddugala fayyaa deemi.", 'ti': "ምክልኻል ወባ። ኩሉ ለይቲ ትሕቲ መርበብ ወባ ድቀስ። ዝቖመ ማይ ኣወግድ። ረስኒ እንተሃልዩካ ናብ ጥዕና ጣቢያ ኺድ።"},
    'diarrhoea':   {'en': "Diarrhoea prevention. Wash hands with soap before eating and after the toilet. Drink only clean boiled water. Give oral rehydration solution to children with diarrhoea.", 'am': "ተቅማጥ መከላከያ። ከመብላትዎ በፊት እና መጸዳጃ ቤት ከተጠቀሙ በኋላ እጅዎን ይታጠቡ። ንጹህ የተፈላ ውሃ ብቻ ይጠጡ። ህፃን ተቅማጥ ካለበት ORS ይስጡ።", 'om': "Ittisa kaasaa. Soorota dura fi mana fincaanii booda harka dhiqi. Bishaan danfifame qofa dhugdi. Daa'imni kaasaa qabaate ORS kenni.", 'ti': "ምክልኻል ተቅማጥ። ቅድሚ ምብላዕ ድሕሪ መጸዳዲ ኢድካ ሕጸብ። ዝፈልሐ ማይ ጥራይ ስተ። ቆልዓ ተቅማጥ እንተሃልዩዎ ORS ሃቦ።"},
    'maternal':    {'en': "Maternal health. Attend four antenatal visits during pregnancy. Eat nutritious food and take iron tablets. Deliver at a health facility. Know danger signs: heavy bleeding, severe headache, blurred vision.", 'am': "የእናቶች ጤና። በእርግዝና ወቅት አራት ቅድመ ወሊድ ምርመራ ያድርጉ። ምግብ ይብሉ እና ብረት ክኒን ይውሰዱ። ወሊድ በጤና ጣቢያ ያድርጉ። አደጋ ምልክቶችን ይወቁ።", 'om': "Fayyaa haadha. Ulfaa yeroo daawwannaa dursaa dhalootaa afur argadhu. Nyaata fuduraa nyaadhu fi qorichaa fudhu. Dhalootaaf giddugala fayyaa deemi.", 'ti': "ጥዕና ኣደ። ኣብ ጥንሲ ኣርባዕተ ምርመራ ቅድሚ ወሊድ ግበሪ። ሕሩይ ምግቢ ብሉዒ። ኣብ ጥዕና ጣቢያ ወልዲ።"},
    'nutrition':   {'en': "Child nutrition. Breastfeed exclusively for six months. After six months add soft nutritious foods. Feed your child five times daily. Include eggs, beans, vegetables and fruits.", 'am': "የህፃናት አመጋገብ። ለስድስት ወራት ብቻ ጡት ያጥቡ። ከስድስት ወር በኋላ ለስላሳ ምግቦችን ያስተዋውቁ። ህፃኑን በቀን አምስት ጊዜ ይመግቡ።", 'om': "Nyaata daa'imaa. Ji'a jaha jalqabaa harma qofa hoosiisi. Ji'a jaha booda nyaata laafaa galchi. Guyyaa shanitti nyaachisi.", 'ti': "ምምጋብ ቆልዑ። ን6 ወርሒ ጥራይ ጸባ ኣጥቡ። ድሕሪ 6 ወርሒ ለዋህ ምግቢ ጀምር። ቆልዓ ኣብ መዓልቲ 5 ጊዜ ምገቦ።"},
    'vaccination': {'en': "Vaccination. Vaccines protect children from measles, polio and tuberculosis. Follow the vaccination schedule. Bring your child's vaccination card to every visit. Vaccines are free at health facilities.", 'am': "ክትባት። ክትባቶች ልጅዎን ከኩፍኝ፣ ፖሊዮ እና ሳንባ ነቀርሳ ይጠብቃሉ። የክትባት ሰሌዳ ይከተሉ። ክትባቶች ነፃ ናቸው።", 'om': "Talaallii. Talaalliin daa'ima kee dhukkuba irraa eega. Karoora talaallii hordofi. Talaalliin bilisaa dha.", 'ti': "ክታበት። ክታበት ቆልዓኻ ካብ ሕሱር ሕማማት ይከላኸለሉ። ናይ ክታበት መደብ ሰዓቦ። ክታበት ናጻ እዩ።"},
    'hygiene':     {'en': "Hand hygiene. Wash hands with soap for 20 seconds before eating, after toilet, and after caring for sick people. Clean hands save lives.", 'am': "የእጅ ንፅህና። ከመብላትዎ፣ መጸዳጃ ቤት ከተጠቀሙ እና ታማሚ ሰው ከተንከባከቡ በኋላ እጅዎን ለ20 ሰከንድ ይታጠቡ። ንጹህ እጆች ህይወት ያድናሉ።", 'om': "Qulqullina harkaa. Soorota dura, mana fincaanii booda, fi nama dhukkubsate kunuunsu booda harka saabunaan dhiqi. Harkii qulqulluu lubbuu baraaruuf.", 'ti': "ጽሬት ኢድ። ቅድሚ ምብላዕ፣ ድሕሪ መጸዳዲ ምጥቃም ኢድካ ብሳሙና ሕጸብ። ጽሩይ ኢዳ ህይወት ይድሕን።"},
}

LANGS = ['en', 'am', 'om', 'ti']

engine = pyttsx3.init()
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)
engine.setProperty('volume', 1.0)

jobs = []
for lang in LANGS:
    lang_dir = os.path.join(PUBLIC_DIR, lang)
    os.makedirs(lang_dir, exist_ok=True)
    for cat, scripts in TIPS.items():
        text = scripts.get(lang, scripts['en'])
        out = os.path.join(lang_dir, f'{cat}_01.mp3')
        if not os.path.exists(out):
            engine.save_to_file(text, out)
            jobs.append((lang, cat, out))
            print(f'  Queued: {lang}/{cat}')
        else:
            print(f'  Skip:   {lang}/{cat}')

print(f'\nRunning TTS for {len(jobs)} files...')
engine.runAndWait()

ok = sum(1 for _, _, p in jobs if os.path.exists(p))
print(f'Done. {ok}/{len(jobs)} files created.')
