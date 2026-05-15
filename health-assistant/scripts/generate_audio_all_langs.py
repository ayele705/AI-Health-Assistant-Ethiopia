"""
Generate audio for all 9 languages using Windows TTS.
Languages without native TTS voice fall back to English audio.
"""
import os, pyttsx3

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'public', 'audio')

# Tips in all 9 languages (fallback to English where translation unavailable)
TIPS = {
    'malaria': {
        'en':  "Malaria prevention. Sleep under a mosquito net every night. Remove standing water near your home. If you have fever or chills, visit your health center immediately.",
        'am':  "ወባ መከላከያ። በየሌሊቱ ከወባ አጥር ስር ተኙ። ቤትዎ አቅራቢያ ቆሞ ያለ ውሃ ያስወግዱ። ትኩሳት ካለዎ ወዲያውኑ ጤና ጣቢያ ይሂዱ።",
        'om':  "Ittisa malaariyaa. Halkan hunda jalatti neetii malaariyaa ciisi. Bishaan dhaabbate kaasi. Yoo ho'aa qabaatte, giddugala fayyaa deemi.",
        'ti':  "Malaria prevention. Sleep under a mosquito net every night. Remove standing water. If you have fever, visit your health center.",
        'sid': "Malaria prevention. Sleep under a mosquito net every night. Remove standing water near your home. Visit health center if you have fever.",
        'so':  "Malaria prevention. Sleep under a mosquito net every night. Remove standing water near your home. Visit health center if you have fever.",
        'aa':  "Malaria prevention. Sleep under a mosquito net every night. Remove standing water near your home. Visit health center if you have fever.",
        'wal': "Malaria prevention. Sleep under a mosquito net every night. Remove standing water near your home. Visit health center if you have fever.",
        'had': "Malaria prevention. Sleep under a mosquito net every night. Remove standing water near your home. Visit health center if you have fever.",
    },
    'diarrhoea': {
        'en':  "Diarrhoea prevention. Wash hands with soap before eating and after the toilet. Drink only clean boiled water. Give oral rehydration solution to children with diarrhoea.",
        'am':  "ተቅማጥ መከላከያ። ከመብላትዎ በፊት እና መጸዳጃ ቤት ከተጠቀሙ በኋላ እጅዎን ይታጠቡ። ንጹህ የተፈላ ውሃ ብቻ ይጠጡ። ህፃን ተቅማጥ ካለበት ORS ይስጡ።",
        'om':  "Ittisa kaasaa. Soorota dura fi mana fincaanii booda harka dhiqi. Bishaan danfifame qofa dhugdi. Daa'imni kaasaa qabaate ORS kenni.",
        'ti':  "Diarrhoea prevention. Wash hands with soap before eating and after toilet. Drink only clean boiled water. Give ORS to children with diarrhoea.",
        'sid': "Diarrhoea prevention. Wash hands with soap before eating and after toilet. Drink only clean boiled water. Give ORS to children with diarrhoea.",
        'so':  "Diarrhoea prevention. Wash hands with soap before eating and after toilet. Drink only clean boiled water. Give ORS to children with diarrhoea.",
        'aa':  "Diarrhoea prevention. Wash hands with soap before eating and after toilet. Drink only clean boiled water. Give ORS to children with diarrhoea.",
        'wal': "Diarrhoea prevention. Wash hands with soap before eating and after toilet. Drink only clean boiled water. Give ORS to children with diarrhoea.",
        'had': "Diarrhoea prevention. Wash hands with soap before eating and after toilet. Drink only clean boiled water. Give ORS to children with diarrhoea.",
    },
    'maternal': {
        'en':  "Maternal health. Attend four antenatal visits during pregnancy. Eat nutritious food and take iron tablets. Deliver at a health facility. Know danger signs: heavy bleeding, severe headache, blurred vision.",
        'am':  "የእናቶች ጤና። በእርግዝና ወቅት አራት ቅድመ ወሊድ ምርመራ ያድርጉ። ምግብ ይብሉ እና ብረት ክኒን ይውሰዱ። ወሊድ በጤና ጣቢያ ያድርጉ። አደጋ ምልክቶችን ይወቁ።",
        'om':  "Fayyaa haadha. Ulfaa yeroo daawwannaa dursaa dhalootaa afur argadhu. Nyaata fuduraa nyaadhu fi qorichaa fudhu. Dhalootaaf giddugala fayyaa deemi.",
        'ti':  "Maternal health. Attend four antenatal visits. Eat nutritious food and take iron tablets. Deliver at a health facility. Know danger signs.",
        'sid': "Maternal health. Attend four antenatal visits. Eat nutritious food and take iron tablets. Deliver at a health facility. Know danger signs.",
        'so':  "Maternal health. Attend four antenatal visits. Eat nutritious food and take iron tablets. Deliver at a health facility. Know danger signs.",
        'aa':  "Maternal health. Attend four antenatal visits. Eat nutritious food and take iron tablets. Deliver at a health facility. Know danger signs.",
        'wal': "Maternal health. Attend four antenatal visits. Eat nutritious food and take iron tablets. Deliver at a health facility. Know danger signs.",
        'had': "Maternal health. Attend four antenatal visits. Eat nutritious food and take iron tablets. Deliver at a health facility. Know danger signs.",
    },
    'nutrition': {
        'en':  "Child nutrition. Breastfeed exclusively for six months. After six months add soft nutritious foods. Feed your child five times daily. Include eggs, beans, vegetables and fruits.",
        'am':  "የህፃናት አመጋገብ። ለስድስት ወራት ብቻ ጡት ያጥቡ። ከስድስት ወር በኋላ ለስላሳ ምግቦችን ያስተዋውቁ። ህፃኑን በቀን አምስት ጊዜ ይመግቡ።",
        'om':  "Nyaata daa'imaa. Ji'a jaha jalqabaa harma qofa hoosiisi. Ji'a jaha booda nyaata laafaa galchi. Guyyaa shanitti nyaachisi.",
        'ti':  "Child nutrition. Breastfeed exclusively for six months. After six months add soft nutritious foods. Feed your child five times daily.",
        'sid': "Child nutrition. Breastfeed exclusively for six months. After six months add soft nutritious foods. Feed your child five times daily.",
        'so':  "Child nutrition. Breastfeed exclusively for six months. After six months add soft nutritious foods. Feed your child five times daily.",
        'aa':  "Child nutrition. Breastfeed exclusively for six months. After six months add soft nutritious foods. Feed your child five times daily.",
        'wal': "Child nutrition. Breastfeed exclusively for six months. After six months add soft nutritious foods. Feed your child five times daily.",
        'had': "Child nutrition. Breastfeed exclusively for six months. After six months add soft nutritious foods. Feed your child five times daily.",
    },
    'vaccination': {
        'en':  "Vaccination. Vaccines protect children from measles, polio and tuberculosis. Follow the vaccination schedule. Bring your child's vaccination card to every visit. Vaccines are free at health facilities.",
        'am':  "ክትባት። ክትባቶች ልጅዎን ከኩፍኝ፣ ፖሊዮ እና ሳንባ ነቀርሳ ይጠብቃሉ። የክትባት ሰሌዳ ይከተሉ። ክትባቶች ነፃ ናቸው።",
        'om':  "Talaallii. Talaalliin daa'ima kee dhukkuba irraa eega. Karoora talaallii hordofi. Talaalliin bilisaa dha.",
        'ti':  "Vaccination. Vaccines protect children from measles, polio and tuberculosis. Follow the vaccination schedule. Vaccines are free.",
        'sid': "Vaccination. Vaccines protect children from measles, polio and tuberculosis. Follow the vaccination schedule. Vaccines are free.",
        'so':  "Vaccination. Vaccines protect children from measles, polio and tuberculosis. Follow the vaccination schedule. Vaccines are free.",
        'aa':  "Vaccination. Vaccines protect children from measles, polio and tuberculosis. Follow the vaccination schedule. Vaccines are free.",
        'wal': "Vaccination. Vaccines protect children from measles, polio and tuberculosis. Follow the vaccination schedule. Vaccines are free.",
        'had': "Vaccination. Vaccines protect children from measles, polio and tuberculosis. Follow the vaccination schedule. Vaccines are free.",
    },
    'hygiene': {
        'en':  "Hand hygiene. Wash hands with soap for 20 seconds before eating, after toilet, and after caring for sick people. Clean hands save lives.",
        'am':  "የእጅ ንፅህና። ከመብላትዎ፣ መጸዳጃ ቤት ከተጠቀሙ እና ታማሚ ሰው ከተንከባከቡ በኋላ እጅዎን ለ20 ሰከንድ ይታጠቡ። ንጹህ እጆች ህይወት ያድናሉ።",
        'om':  "Qulqullina harkaa. Soorota dura, mana fincaanii booda, fi nama dhukkubsate kunuunsu booda harka saabunaan dhiqi. Harkii qulqulluu lubbuu baraaruuf.",
        'ti':  "Hand hygiene. Wash hands with soap for 20 seconds before eating, after toilet, and after caring for sick people. Clean hands save lives.",
        'sid': "Hand hygiene. Wash hands with soap for 20 seconds before eating, after toilet, and after caring for sick people. Clean hands save lives.",
        'so':  "Hand hygiene. Wash hands with soap for 20 seconds before eating, after toilet, and after caring for sick people. Clean hands save lives.",
        'aa':  "Hand hygiene. Wash hands with soap for 20 seconds before eating, after toilet, and after caring for sick people. Clean hands save lives.",
        'wal': "Hand hygiene. Wash hands with soap for 20 seconds before eating, after toilet, and after caring for sick people. Clean hands save lives.",
        'had': "Hand hygiene. Wash hands with soap for 20 seconds before eating, after toilet, and after caring for sick people. Clean hands save lives.",
    },
}

ALL_LANGS = ['en', 'am', 'om', 'ti', 'sid', 'so', 'aa', 'wal', 'had']

engine = pyttsx3.init()
voices = engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)
engine.setProperty('volume', 1.0)

jobs = []
for lang in ALL_LANGS:
    lang_dir = os.path.join(PUBLIC_DIR, lang)
    os.makedirs(lang_dir, exist_ok=True)
    for cat, scripts in TIPS.items():
        text = scripts.get(lang, scripts['en'])
        out = os.path.join(lang_dir, f'{cat}_01.mp3')
        if not os.path.exists(out) or os.path.getsize(out) < 1000:
            engine.save_to_file(text, out)
            jobs.append((lang, cat, out))
            print(f'  Queued: {lang}/{cat}')
        else:
            print(f'  Skip:   {lang}/{cat} ({os.path.getsize(out)//1024}KB)')

print(f'\nRunning TTS for {len(jobs)} files...')
engine.runAndWait()

ok = sum(1 for _, _, p in jobs if os.path.exists(p) and os.path.getsize(p) > 1000)
print(f'Done. {ok}/{len(jobs)} files created successfully.')
print(f'Total audio files: {sum(1 for _ in __import__("pathlib").Path(PUBLIC_DIR).rglob("*.mp3"))}')
