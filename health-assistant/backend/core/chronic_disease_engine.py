"""
Chronic Disease Management Engine.
Covers hypertension and diabetes follow-up reminders,
medication adherence tracking, and danger sign alerts for Ethiopia context.
"""

# ── Hypertension ──────────────────────────────────────────────────────────────
HTN_STAGES = {
    'normal':       {'systolic': (0, 120),   'diastolic': (0, 80)},
    'elevated':     {'systolic': (120, 130), 'diastolic': (0, 80)},
    'stage1':       {'systolic': (130, 140), 'diastolic': (80, 90)},
    'stage2':       {'systolic': (140, 180), 'diastolic': (90, 120)},
    'crisis':       {'systolic': (180, 999), 'diastolic': (120, 999)},
}

HTN_MESSAGES = {
    'normal': {
        'en': 'Blood pressure is normal. Continue healthy lifestyle.',
        'am': 'የደም ግፊት መደበኛ ነው። ጤናማ አኗኗር ይቀጥሉ።',
        'om': 'Dhiibbaa dhiigaa normal dha. Jireenyaa fayyaa itti fufi.',
        'ti': 'ጸቕጢ ደም ንቡር ኢዩ። ጥዑይ ናብራ ቀጽሎ።',
    },
    'elevated': {
        'en': 'Blood pressure is slightly elevated. Reduce salt, exercise, and monitor.',
        'am': 'የደም ግፊት ትንሽ ከፍ ብሏል። ጨው ይቀንሱ፣ ይንቀሳቀሱ።',
        'om': "Dhiibbaan dhiigaa xiqqoo ol ka'e. Soogidda hir'isi, sochoo'i.",
        'ti': 'ጸቕጢ ደም ቁሩብ ልዑል ኢዩ። ጨው ቀንስ፡ ምንቅስቓስ ግበር።',
    },
    'stage1': {
        'en': 'Stage 1 hypertension. Visit health center for assessment and possible medication.',
        'am': 'ደረጃ 1 ከፍተኛ ደም ግፊት። ለምርመራ ወደ ጤና ጣቢያ ይሂዱ።',
        'om': "Sadarkaa 1 dhiibbaa dhiigaa ol ka'e. Giddugala fayyaa deemi.",
        'ti': 'ደረጃ 1 ልዑል ጸቕጢ ደም። ናብ ጥዕና ጣቢያ ኺድ።',
    },
    'stage2': {
        'en': 'Stage 2 hypertension. Visit health center TODAY. Medication is likely needed.',
        'am': 'ደረጃ 2 ከፍተኛ ደም ግፊት። ዛሬ ወደ ጤና ጣቢያ ይሂዱ።',
        'om': "Sadarkaa 2 dhiibbaa dhiigaa ol ka'e. Har'a giddugala fayyaa deemi.",
        'ti': 'ደረጃ 2 ልዑል ጸቕጢ ደም። ሎሚ ናብ ጥዕና ጣቢያ ኺድ።',
    },
    'crisis': {
        'en': '[EMERGENCY] HYPERTENSIVE CRISIS. Go to hospital IMMEDIATELY. Call 907.',
        'am': '[EMERGENCY] አስቸኳይ ከፍተኛ ደም ግፊት። ወዲያውኑ ሆስፒታል ይሂዱ። 907 ይደውሉ።',
        'om': '[EMERGENCY] Balaa dhiibbaa dhiigaa. Hospitaala ARIIFATEE deemi. 907 bilbili.',
        'ti': '[EMERGENCY] ህጹጽ ልዑል ጸቕጢ ደም። ወዲኡ ሆስፒታል ኺድ። 907 ደውል።',
    },
}

HTN_DANGER_SIGNS = {
    'en': ['Severe headache', 'Blurred vision', 'Chest pain', 'Difficulty breathing',
           'Nausea/vomiting', 'Confusion', "Nosebleed that won't stop"],
    'am': ['ከባድ ራስ ምታት', 'ደበዘዘ ዕይታ', 'የደረት ህመም', 'የትንፋሽ ችግር',
           'ማቅለሽለሽ/ማስታወክ', 'ግራ መጋባት', 'የማይቆም የአፍንጫ ደም'],
    'om': ['Mataa dhukkuba cimaa', 'Arguu dadhabuu', 'Laphee dhukkuba',
           'Rakkoo hafuura', 'Mataa naasuu', 'Funyaan dhiiguu'],
    'ti': ['ከቢድ ቃንዛ ርእሲ', 'ዝሓሸ ምርኣይ', 'ቃንዛ ደረት', 'ጸገም ምስትንፋስ',
           'ምድንጋጽ', 'ምዕዋት ኣፍንጫ'],
}

# ── Diabetes ──────────────────────────────────────────────────────────────────
DM_MESSAGES = {
    'hypoglycemia': {
        'en': '[WARNING] Low blood sugar. Eat or drink something sweet immediately (sugar water, juice, candy). If unconscious, call 907.',
        'am': '[WARNING] ዝቅተኛ የደም ስኳር። ወዲያውኑ ጣፋጭ ነገር ይብሉ ወይም ይጠጡ (የስኳር ውሃ፣ ጭማቂ)። ንቃተ ህሊና ሲጠፋ 907 ይደውሉ።',
        'om': "[WARNING] Sukkaara dhiigaa gadi. Waan mi'aawaa nyaadhu ykn dhugdi. Yoo of wallaalee 907 bilbili.",
        'ti': '[WARNING] ትሑት ሽኮር ደም። ወዲኡ ጥዑም ነገር ብላዕ ወይ ስተ። ዘይንቁ እንተኾይኑ 907 ደውል።',
    },
    'hyperglycemia': {
        'en':  'High blood sugar. Take medication as prescribed, drink water, avoid sugary foods. Visit health center if >300 mg/dL.',
        'am':  'ከፍተኛ የደም ስኳር። መድሃኒት እንደታዘዘ ይውሰዱ፣ ውሃ ይጠጡ። >300 mg/dL ከሆነ ወደ ጤና ጣቢያ ይሂዱ።',
        'om':  "Sukkaara dhiigaa ol ka'e. Qoricha fudhadi, bishaani dhugdi. >300 mg/dL yoo ta'e giddugala fayyaa deemi.",
        'ti':  'ልዑል ሽኮር ደም። መድሃኒት ከምዝተሓዝ ውሰድ፡ ማይ ስተ። >300 mg/dL እንተኾይኑ ናብ ጥዕና ጣቢያ ኺድ።',
        'sid': "Sukkaara dhiigaa ol ka'e. Qoricha fudhadi, bishaani dhugdi. Giddugala fayyaa deemi.",
    },
    'normal': {
        'en': 'Blood sugar is in target range. Continue medication and healthy diet.',
        'am': 'የደም ስኳር ዒላማ ክልል ውስጥ ነው። መድሃኒት እና ጤናማ አመጋገብ ይቀጥሉ።',
        'om': 'Sukkaara dhiigaa kaayyoo keessa jira. Qoricha fi nyaata fayyaa itti fufi.',
        'ti': 'ሽኮር ደም ኣብ ዒላማ ኢዩ። መድሃኒት ጥዑይ ምግቢ ቀጽሎ።',
    },
}

DM_DANGER_SIGNS = {
    'en': ['Extreme thirst', 'Frequent urination', 'Blurred vision', 'Slow-healing wounds',
           'Numbness in feet/hands', 'Fruity breath odor', 'Confusion or unconsciousness'],
    'am': ['ከፍተኛ ጥም', 'ተደጋጋሚ ሽንት', 'ደበዘዘ ዕይታ', 'ቀስ ብሎ የሚፈወስ ቁስለት',
           'እጅ/እግር ደንዝዞ መሰማት', 'ፍሬ መሰል ሽታ ያለው ትንፋሽ', 'ግራ መጋባት ወይም ንቃተ ህሊና ማጣት'],
    'om': ["Dheebuu cimaa", "Fincaan baay'ee", 'Arguu dadhabuu', 'Madaa fayyuu dadhabuu',
           'Miila/harka dhibamuu', 'Hafuura mi\'aawaa', 'Mataa naasuu'],
    'ti': ['ልዑል ጽምኢ', 'ተደጋጋሚ ሽንቲ', 'ዝሓሸ ምርኣይ', 'ቁስሊ ዘይፍወስ',
           'ምዕዋት ኣእጋር/ኢድ', 'ሽታ ፍረ ምስትንፋስ', 'ምድንጋጽ'],
}

DM_DIET_TIPS = {
    'en': [
        'Eat small, frequent meals (5–6 times/day)',
        'Choose whole grains over refined (teff injera, whole wheat)',
        'Include vegetables at every meal',
        'Limit sugar, honey, and sweet drinks',
        'Avoid skipping meals — this causes blood sugar swings',
        'Drink water instead of sugary drinks',
        'Limit white rice, white bread, and potatoes',
    ],
    'am': [
        'ትንሽ ተደጋጋሚ ምግቦችን ይብሉ (5–6 ጊዜ/ቀን)',
        'ሙሉ ጥራጥሬ ይምረጡ (ጤፍ ዳቦ፣ ሙሉ ስንዴ)',
        'በእያንዳንዱ ምግብ አትክልቶችን ያካትቱ',
        'ስኳር፣ ማር እና ጣፋጭ መጠጦችን ይቀንሱ',
        'ምግብ አይዝለሉ — ይህ የደም ስኳር መዋዠቅ ያስከትላል',
    ],
    'om': [
        "Nyaata xiqqaa yeroo baay'ee nyaadhu (5–6 dafqa/guyyaa)",
        'Midhaanota guutuu filadhu',
        'Nyaata hunda keessatti kuduraa dabaluu',
        "Sukkaara, damma fi dhugaatii mi'aawaa hir'isi",
        'Nyaata hin dhabsisin',
    ],
    'ti': [
        'ንኡስ ተደጋጋሚ ምግቢ ብላዕ (5–6 ጊዜ/መዓልቲ)',
        'ምሉእ ጥራጥሬ ምረጽ (ጤፍ ዳቦ፣ ምሉእ ስርናይ)',
        'ኣብ ነፍሲ ወከፍ ምግቢ ኣሕምልቲ ወሰኽ',
        'ሽኮር፡ ማዓር፡ ጥዑም መስተ ቀንስ',
        'ምግቢ ኣይዝለፍ',
    ],
    'sid': [
        "Nyaata xiqqaa yeroo baay'ee nyaadhu (5–6 dafqa/guyyaa)",
        'Midhaanota guutuu filadhu',
        "Sukkaara fi dhugaatii mi'aawaa hir'isi",
    ],
}


def assess_blood_pressure(systolic: int, diastolic: int, language: str = 'en') -> dict:
    """Classify blood pressure and return guidance."""
    stage = 'normal'
    if systolic >= 180 or diastolic >= 120:
        stage = 'crisis'
    elif systolic >= 140 or diastolic >= 90:
        stage = 'stage2'
    elif systolic >= 130 or diastolic >= 80:
        stage = 'stage1'
    elif systolic >= 120:
        stage = 'elevated'

    return {
        'systolic': systolic,
        'diastolic': diastolic,
        'stage': stage,
        'message': HTN_MESSAGES[stage].get(language, HTN_MESSAGES[stage]['en']),
        'danger_signs': HTN_DANGER_SIGNS.get(language, HTN_DANGER_SIGNS['en']),
        'urgent': stage == 'crisis',
        'refer': stage in ('stage2', 'crisis'),
    }


def assess_blood_glucose(glucose_mgdl: float, fasting: bool = True, language: str = 'en') -> dict:
    """Classify blood glucose and return guidance."""
    if fasting:
        if glucose_mgdl < 70:
            status = 'hypoglycemia'
        elif glucose_mgdl <= 130:
            status = 'normal'
        else:
            status = 'hyperglycemia'
    else:  # post-meal
        if glucose_mgdl < 70:
            status = 'hypoglycemia'
        elif glucose_mgdl <= 180:
            status = 'normal'
        else:
            status = 'hyperglycemia'

    return {
        'glucose_mgdl': glucose_mgdl,
        'fasting': fasting,
        'status': status,
        'message': DM_MESSAGES[status].get(language, DM_MESSAGES[status]['en']),
        'danger_signs': DM_DANGER_SIGNS.get(language, DM_DANGER_SIGNS['en']),
        'diet_tips': DM_DIET_TIPS.get(language, DM_DIET_TIPS['en']),
        'urgent': status == 'hypoglycemia' or glucose_mgdl > 300,
    }


def get_adherence_reminder(medication: str, condition: str, language: str = 'en') -> str:
    """Generate a medication adherence reminder message."""
    msgs = {
        'en':  f"Reminder: Take your {medication} for {condition} as prescribed. Consistent medication keeps you healthy.",
        'am':  f"ማስታወሻ: ለ{condition} {medication} እንደታዘዘ ይውሰዱ። ቀጣይ መድሃኒት ጤናዎን ይጠብቃል።",
        'om':  f"Yaadachiisa: {condition} dhaaf {medication} fudhachuu itti fufi. Qoricha fudhachuun fayyaa kee eega.",
        'ti':  f"ዘኪሮ: ን{condition} {medication} ከምዝተሓዝ ውሰድ። ቀጻሊ መድሃኒት ጥዕናኻ ይሕሉ።",
        'sid': f"Yaadachiisa: {condition} dhaaf {medication} fudhachuu itti fufi. Fayyaa kee eega.",
    }
    return msgs.get(language, msgs['en'])


def get_chronic_disease_checklist(condition: str, language: str = 'en') -> dict:
    """Return a self-monitoring checklist for a chronic condition."""
    checklists = {
        'hypertension': {
            'en': {
                'title': 'Hypertension Self-Monitoring',
                'items': [
                    'Take blood pressure medication every day at the same time',
                    'Measure blood pressure weekly if possible',
                    'Reduce salt in cooking',
                    'Walk 30 minutes most days',
                    'Avoid smoking and alcohol',
                    'Eat more fruits and vegetables',
                    'Attend monthly health center follow-up',
                ],
                'danger_signs': HTN_DANGER_SIGNS['en'],
            },
            'am': {
                'title': 'የደም ግፊት ራስ-ክትትል',
                'items': [
                    'ሁልጊዜ በተመሳሳይ ሰዓት የደም ግፊት መድሃኒት ይውሰዱ',
                    'ከተቻለ ሳምንታዊ የደም ግፊት ይለኩ',
                    'ምግብ ውስጥ ጨው ይቀንሱ',
                    'አብዛኛዎቹ ቀናት 30 ደቂቃ ይራመዱ',
                    'ሲጋራ እና አልኮሆልን ያስወግዱ',
                ],
                'danger_signs': HTN_DANGER_SIGNS['am'],
            },
        },
        'diabetes': {
            'en': {
                'title': 'Diabetes Self-Monitoring',
                'items': [
                    'Take diabetes medication every day as prescribed',
                    'Check blood sugar regularly if you have a glucometer',
                    'Follow the diabetes diet plan',
                    'Check feet daily for wounds or sores',
                    'Exercise regularly (30 min/day)',
                    'Attend monthly health center follow-up',
                    'Never skip meals',
                ],
                'danger_signs': DM_DANGER_SIGNS['en'],
                'diet_tips': DM_DIET_TIPS['en'],
            },
            'am': {
                'title': 'የስኳር ህመም ራስ-ክትትል',
                'items': [
                    'ሁልጊዜ እንደታዘዘ የስኳር ህመም መድሃኒት ይውሰዱ',
                    'ግሉኮሜትር ካለዎ ደም ስኳር በየጊዜው ይለኩ',
                    'የስኳር ህመም አመጋገብ ዕቅድ ይከተሉ',
                    'ቁስለት ወይም ቁስሎች ለማየት ሁልጊዜ እግሮቹን ይፈትሹ',
                    'ምግብ አይዝለሉ — ይህ የደም ስኳር መዋዠቅ ያስከትላል',
                ],
                'danger_signs': DM_DANGER_SIGNS['am'],
                'diet_tips': DM_DIET_TIPS['am'],
            },
        },
    }
    data = checklists.get(condition.lower(), {})
    return data.get(language, data.get('en', {}))
