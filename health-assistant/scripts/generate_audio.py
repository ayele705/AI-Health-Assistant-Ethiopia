"""
Generate audio health tips using Windows TTS (pyttsx3).
Creates MP3-compatible WAV files for all supported languages.
Run from: health-assistant/scripts/
"""
import os
import sys
import pyttsx3

# Output directory
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'public', 'audio')

# Health tip scripts per category
TIPS = {
    'malaria': {
        'en': "Malaria prevention tip. Sleep under a mosquito net every night. Remove standing water near your home. Wear long sleeves in the evening. If you have fever, chills, or headache, visit your health center immediately.",
        'am': "ወባ መከላከያ ምክር። በየሌሊቱ ከወባ አጥር ስር ተኙ። ቤትዎ አቅራቢያ ቆሞ ያለ ውሃ ያስወግዱ። ምሽት ላይ ረዥም እጅጌ ያለው ልብስ ይልበሱ። ትኩሳት፣ ብርድ ወይም ራስ ምታት ካለዎ ወዲያውኑ ጤና ጣቢያ ይሂዱ።",
        'om': "Gorsa ittisa malaariyaa. Halkan hunda jalatti neetii malaariyaa ciisi. Bishaan dhaabbate mana kee bira jiru kaasi. Galgala uffata harka dheeraa uffadhu. Yoo ho'aa, qorraa, ykn mataa dhukkubu qabaatte, giddugala fayyaa deemi.",
        'ti': "ምኽሪ ምክልኻል ወባ። ኩሉ ለይቲ ትሕቲ መርበብ ወባ ድቀስ። ኣብ ቀረባ ቤትካ ዘሎ ዝቖመ ማይ ኣወግድ። ምሸት ናይ ነዊሕ ኢድ ክዳን ልበስ። ረስኒ፣ ቁሪ ወይ ቃንዛ ርእሲ እንተሃልዩካ ናብ ጥዕና ጣቢያ ኺድ።",
    },
    'diarrhoea': {
        'en': "Diarrhoea prevention tip. Always wash your hands with soap before eating and after using the toilet. Drink only clean, boiled, or treated water. Keep food covered and eat freshly prepared meals. If a child has diarrhoea, give oral rehydration solution immediately.",
        'am': "ተቅማጥ መከላከያ ምክር። ከመብላትዎ በፊት እና መጸዳጃ ቤት ከተጠቀሙ በኋላ ሁልጊዜ እጅዎን በሳሙና ይታጠቡ። ንጹህ፣ የተፈላ ወይም የታከመ ውሃ ብቻ ይጠጡ። ምግብ ተሸፍኖ ይቀመጥ። ህፃን ተቅማጥ ካለበት ወዲያውኑ ORS ይስጡ።",
        'om': "Gorsa ittisa kaasaa. Soorota dura fi mana fincaanii booda harka saabunaan dhiqi. Bishaan qulqulluu, danfifame, ykn qorichaan qulqulleeffame qofa dhugdi. Nyaata haguugi. Daa'imni kaasaa qabaate, ORS hatattamaan kenni.",
        'ti': "ምኽሪ ምክልኻል ተቅማጥ። ቅድሚ ምብላዕ ድሕሪ መጸዳዲ ምጥቃም ኢድካ ብሳሙና ሕጸብ። ጽሩይ፣ ዝፈልሐ ወይ ዝተሓከመ ማይ ጥራይ ስተ። ምግቢ ሸፊንካ ሓዞ። ቆልዓ ተቅማጥ እንተሃልዩዎ ወዲያ ORS ሃቦ።",
    },
    'maternal': {
        'en': "Maternal health tip. Every pregnant woman should attend at least four antenatal care visits. Eat nutritious food including vegetables, fruits, and protein. Take iron and folic acid tablets as prescribed. Deliver at a health facility with a skilled birth attendant. Know the danger signs: heavy bleeding, severe headache, blurred vision, and swelling.",
        'am': "የእናቶች ጤና ምክር። እያንዳንዱ እርጉዝ ሴት ቢያንስ አራት ቅድመ ወሊድ ምርመራ ማድረግ አለባት። አትክልት፣ ፍራፍሬ እና ፕሮቲን ያካተተ ምግብ ይብሉ። ብረት እና ፎሊክ አሲድ ክኒን ይውሰዱ። ወሊድ በጤና ጣቢያ ያድርጉ። አደጋ ምልክቶችን ይወቁ።",
        'om': "Gorsa fayyaa haadha. Dubartiin ulfaa hunda xiqqaate daawwannaa dursaa dhalootaa afur argachuu qabdi. Nyaata fuduraa, kuduraa fi pirootiinii of keessaa qabu nyaadhu. Qorichaa biroo fi fooliik aasidii fudhu. Dhalootaaf giddugala fayyaa deemi.",
        'ti': "ምኽሪ ጥዕና ኣደ። ኩሉ ጥንስቲ ሰበይቲ ቅድሚ ወሊድ ቢያንስ ኣርባዕተ ምርመራ ክትገብር ኣለዋ። ሕሩይ ምግቢ ብሉዕ። ናይ ሓጺን ክኒን ውሰዲ። ኣብ ጥዕና ጣቢያ ወልዲ። ናይ ሓደጋ ምልክታት ፍለጢ።",
    },
    'nutrition': {
        'en': "Child nutrition tip. Breastfeed your baby exclusively for the first six months. After six months, introduce soft, nutritious foods while continuing to breastfeed. Feed your child five times a day. Include eggs, beans, vegetables, and fruits in their diet. A well-nourished child grows strong and fights disease.",
        'am': "የህፃናት አመጋገብ ምክር። ህፃንዎን ለመጀመሪያዎቹ ስድስት ወራት ብቻ ጡት ያጥቡ። ከስድስት ወር በኋላ ለስላሳ ምግቦችን ያስተዋውቁ። ህፃኑን በቀን አምስት ጊዜ ይመግቡ። እንቁላል፣ ባቄላ፣ አትክልት እና ፍራፍሬ ያካትቱ።",
        'om': "Gorsa nyaata daa'imaa. Ji'a jaha jalqabaa daa'ima kee harma qofa hoosiisi. Ji'a jaha booda nyaata laafaa galchi. Guyyaa shanitti daa'ima kee nyaachisi. Hanqaaquu, baaqelaa, kuduraa fi fuduraa galchi.",
        'ti': "ምኽሪ ምምጋብ ቆልዑ። ቆልዓኻ ን6 ወርሒ ጥራይ ጸባ ኣጥቡ። ድሕሪ 6 ወርሒ ለዋህ ምግቢ ጀምር። ቆልዓ ኣብ መዓልቲ 5 ጊዜ ምገቦ። እንቋቑሖ፣ ባቄላ፣ ኣሕምልቲ ወሲኽካ ሃቦ።",
    },
    'vaccination': {
        'en': "Vaccination tip. Vaccines protect your child from dangerous diseases like measles, polio, and tuberculosis. Follow the vaccination schedule given by your health worker. Bring your child's vaccination card to every visit. Vaccines are safe and free at government health facilities. A vaccinated child is a protected child.",
        'am': "ክትባት ምክር። ክትባቶች ልጅዎን ከኩፍኝ፣ ፖሊዮ እና ሳንባ ነቀርሳ ይጠብቃሉ። የጤና ሠራተኛዎ የሰጡዎትን የክትባት ሰሌዳ ይከተሉ። የልጅዎን የክትባት ካርድ ሁልጊዜ ይዘው ይምጡ። ክትባቶች ደህና እና ነፃ ናቸው።",
        'om': "Gorsa talaallii. Talaalliin daa'ima kee dhukkuba akka haxaawwee, pooliyoo fi qufaa irraa eega. Karoora talaallii ogeessa fayyaa kee kenneef hordofi. Kaardii talaallii daa'ima kee daawwannaa hundaaf fidi. Talaalliin nagaa fi bilisaa dha.",
        'ti': "ምኽሪ ክታበት። ክታበት ቆልዓኻ ካብ ሕሱር ሕማማት ይከላኸለሉ። ናይ ክታበት መደብ ሰዓቦ። ናይ ክታበት ካርድ ሒዝካ ምጻእ። ክታበት ድሕሩ ኣብ ናይ መንግስቲ ጥዕና ጣቢያ ናጻ እዩ።",
    },
    'hygiene': {
        'en': "Hand hygiene tip. Wash your hands with soap and clean water for at least 20 seconds. Always wash before eating, before preparing food, after using the toilet, and after caring for a sick person. If soap is not available, use ash or hand sanitizer. Clean hands save lives.",
        'am': "የእጅ ንፅህና ምክር። እጅዎን ቢያንስ ለ20 ሰከንድ በሳሙና እና ንጹህ ውሃ ይታጠቡ። ከመብላትዎ፣ ምግብ ከማዘጋጀትዎ፣ መጸዳጃ ቤት ከተጠቀሙ እና ታማሚ ሰው ከተንከባከቡ በኋላ ሁልጊዜ ይታጠቡ። ንጹህ እጆች ህይወት ያድናሉ።",
        'om': "Gorsa qulqullina harkaa. Harka kee saabunaa fi bishaan qulqulluun xiqqaate sekondii 20 dhiqi. Soorota dura, nyaata qopheessuu dura, mana fincaanii booda, fi nama dhukkubsate kunuunsu booda harka dhiqi. Harkii qulqulluu lubbuu baraaruuf.",
        'ti': "ምኽሪ ጽሬት ኢድ። ኢድካ ብሳሙናን ጽሩይ ማይን ቢያንስ 20 ሰከንድ ሕጸብ። ቅድሚ ምብላዕ፣ ምግቢ ቅድሚ ምድላው፣ ድሕሪ መጸዳዲ ምጥቃም ሕጸብ። ጽሩይ ኢዳ ህይወት ይድሕን።",
    },
}

LANGUAGES = list(next(iter(TIPS.values())).keys())


def generate_audio():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Use the first available voice (Windows SAPI)
    if voices:
        engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 150)   # speaking rate
    engine.setProperty('volume', 1.0)

    generated = 0
    skipped = 0

    for lang in LANGUAGES:
        lang_dir = os.path.join(PUBLIC_DIR, lang)
        os.makedirs(lang_dir, exist_ok=True)

        for category, scripts in TIPS.items():
            text = scripts.get(lang) or scripts.get('en')  # fallback to English
            out_path = os.path.join(lang_dir, f'{category}_01.mp3')

            if os.path.exists(out_path):
                print(f'  SKIP (exists): {out_path}')
                skipped += 1
                continue

            # pyttsx3 saves as WAV; rename to .mp3 (browsers accept WAV with .mp3 extension for basic playback)
            wav_path = out_path.replace('.mp3', '.wav')
            try:
                engine.save_to_file(text, wav_path)
                engine.runAndWait()
                # Rename WAV to MP3 (content is WAV but browser Audio element handles it)
                if os.path.exists(wav_path):
                    os.rename(wav_path, out_path)
                    size = os.path.getsize(out_path)
                    print(f'  OK [{lang}/{category}] {size//1024}KB -> {out_path}')
                    generated += 1
                else:
                    print(f'  WARN: file not created for {lang}/{category}')
            except Exception as e:
                print(f'  ERROR [{lang}/{category}]: {e}')

    print(f'\nDone. Generated: {generated}, Skipped: {skipped}')
    print(f'Audio files saved to: {os.path.abspath(PUBLIC_DIR)}')


if __name__ == '__main__':
    print('Generating audio health tips...')
    print(f'Output: {os.path.abspath(PUBLIC_DIR)}\n')
    generate_audio()
