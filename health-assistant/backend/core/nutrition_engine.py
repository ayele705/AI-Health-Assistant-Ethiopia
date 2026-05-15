"""
Nutrition Counseling Engine.
Covers acute malnutrition, IYCF (infant and young child feeding),
micronutrient deficiencies, and therapeutic feeding guidance for Ethiopia.
"""

# ── IYCF Guidelines ───────────────────────────────────────────────────────────
IYCF_GUIDANCE = {
    'en': {
        '0_6_months': {
            'title': 'Exclusive Breastfeeding (0–6 months)',
            'guidance': [
                'Breastfeed exclusively — no water, formula, or other foods.',
                'Feed on demand, at least 8–12 times per day.',
                'Ensure proper latch to prevent nipple pain.',
                'Skin-to-skin contact supports milk production.',
                'If mother is ill, continue breastfeeding unless advised otherwise by a health worker.',
            ],
        },
        '6_24_months': {
            'title': 'Complementary Feeding (6–24 months)',
            'guidance': [
                'Continue breastfeeding alongside complementary foods.',
                'Start with soft, mashed foods at 6 months.',
                'Gradually increase variety, texture, and frequency.',
                'Feed 2–3 times/day at 6–8 months; 3–4 times/day at 9–24 months.',
                'Include iron-rich foods: meat, fish, eggs, legumes, fortified porridge.',
                'Add vitamin A foods: orange/yellow vegetables, dark leafy greens.',
                'Avoid adding salt, sugar, or spices to infant food.',
            ],
        },
        'over_24_months': {
            'title': 'Family Foods (24+ months)',
            'guidance': [
                'Child can eat family foods with appropriate texture.',
                'Ensure 3 meals and 2 snacks per day.',
                'Include all food groups: grains, legumes, vegetables, fruits, animal products.',
                'Encourage hand washing before meals.',
            ],
        },
    },
    'am': {
        '0_6_months': {
            'title': 'ብቸኛ ጡት ማጥባት (0–6 ወር)',
            'guidance': [
                'ብቸኛ ጡት ያጥቡ — ውሃ፣ ፎርሙላ ወይም ሌሎች ምግቦች አይስጡ።',
                'ፍላጎት ሲኖር ቢያንስ በቀን 8–12 ጊዜ ያጥቡ።',
                'ትክክለኛ ጡጦ ያረጋግጡ።',
                'ቆዳ ለቆዳ ንክኪ የወተት ምርትን ይደግፋል።',
            ],
        },
        '6_24_months': {
            'title': 'ተጨማሪ ምግብ (6–24 ወር)',
            'guidance': [
                'ጡት ማጥባቱን ከተጨማሪ ምግቦች ጋር ይቀጥሉ።',
                'በ6 ወር ለስላሳ ምግቦችን ይጀምሩ።',
                'ብረት የሚሰጡ ምግቦችን ያካትቱ: ሥጋ፣ ዓሳ፣ እንቁላል፣ ጥራጥሬ።',
                'ቫይታሚን ኤ ምግቦችን ያካትቱ: ብርቱካናማ አትክልቶች።',
            ],
        },
        'over_24_months': {
            'title': 'የቤተሰብ ምግቦች (24+ ወር)',
            'guidance': [
                'ልጁ ተስማሚ ሸካራነት ያለው የቤተሰብ ምግብ መብላት ይችላል።',
                'በቀን 3 ምግቦች እና 2 መክሰስ ያረጋግጡ።',
            ],
        },
    },
    'om': {
        '0_6_months': {
            'title': 'Harma Qofa Hodhuu (ji\'a 0–6)',
            'guidance': [
                'Harma qofa hodhi — bishaani, foormulaa ykn nyaata biraa hin kenninaa.',
                "Gaafatameen hodhi, guyyaatti yeroo 8–12 hin xiqqaanne.",
                'Qabannaa sirrii mirkaneessi.',
                "Gogaa walitti dhiheessuu omisha harmaatii gargaara.",
            ],
        },
        '6_24_months': {
            'title': "Nyaata Dabalataa (ji'a 6–24)",
            'guidance': [
                'Harma hodhuu nyaata dabalataa waliin itti fufi.',
                "Ji'a 6tti nyaata laafaa jalqabi.",
                'Nyaata biroo dabaluu: foon, qurxummii, hanqaaquu, qamadii.',
                'Nyaata Vitamin A: kuduraa diimaa/dhadhaa, jiraata gurraacha.',
            ],
        },
        'over_24_months': {
            'title': "Nyaata Maatii (ji'a 24+)",
            'guidance': [
                'Daa\'imni nyaata maatii sararaa sirrii qabu nyaachuu danda\'a.',
                'Guyyaatti nyaata 3 fi qorichaa 2 mirkaneessi.',
                'Garee nyaata hunda dabaluu: midhaanota, qamadii, kuduraa, fuduraa.',
            ],
        },
    },
    'ti': {
        '0_6_months': {
            'title': 'ጥብቅ ምጥባው (0–6 ወርሒ)',
            'guidance': [
                'ጥብቅ ጡብ ኣጥቢ — ማይ፡ ፎርሙላ ወይ ካልእ ምግቢ ኣይሃቢ።',
                'ብጠለብ ኣጥቢ፡ ኣብ መዓልቲ ቢያንስ 8–12 ጊዜ።',
                'ቅኑዕ ምሓዝ ኣረጋግጽ።',
                'ቆርበት ምስ ቆርበት ምትንካፍ ምፍራይ ጸባ ይሕግዝ።',
            ],
        },
        '6_24_months': {
            'title': 'ተወሳኺ ምግቢ (6–24 ወርሒ)',
            'guidance': [
                'ጡብ ምጥባው ምስ ተወሳኺ ምግቢ ቀጽሎ።',
                'ኣብ 6 ወርሒ ለዋህ ምግቢ ጀምር።',
                'ምግቢ ሓጺን ዘለዎ ወሰኽ: ስጋ፡ ዓሳ፡ እንቋቑሖ፡ ጥራጥሬ።',
                'ምግቢ ቫይታሚን ኤ ወሰኽ: ብርቱካናዊ ኣሕምልቲ።',
            ],
        },
        'over_24_months': {
            'title': 'ምግቢ ስድራ (24+ ወርሒ)',
            'guidance': [
                'ቆልዓ ምግቢ ስድራ ምስ ቅኑዕ ሸካርነት ክበልዕ ይኽእል።',
                'ኣብ መዓልቲ 3 ምግቢ ን 2 ቁርሲ ኣረጋግጽ።',
                'ኩሎም ጉጅለ ምግቢ ወሰኽ: ጥራጥሬ፡ ኣሕምልቲ፡ ፍረ።',
            ],
        },
    },
    'sid': {
        '0_6_months': {
            'title': "Harma Qofa Hodhuu (ji'a 0–6)",
            'guidance': [
                'Harma qofa hodhi — bishaani ykn nyaata biraa hin kenninaa.',
                "Guyyaatti yeroo 8–12 hin xiqqaanne hodhi.",
                "Gogaa walitti dhiheessuu omisha harmaatii gargaara.",
            ],
        },
        '6_24_months': {
            'title': "Nyaata Dabalataa (ji'a 6–24)",
            'guidance': [
                'Harma hodhuu nyaata dabalataa waliin itti fufi.',
                "Ji'a 6tti nyaata laafaa jalqabi.",
                'Nyaata biroo dabaluu: foon, qurxummii, hanqaaquu.',
            ],
        },
        'over_24_months': {
            'title': "Nyaata Maatii (ji'a 24+)",
            'guidance': [
                "Daa'imni nyaata maatii nyaachuu danda'a.",
                'Guyyaatti nyaata 3 fi qorichaa 2 mirkaneessi.',
            ],
        },
    },
}

# ── Micronutrient Deficiency Guidance ────────────────────────────────────────
MICRONUTRIENT_GUIDANCE = {
    'iron_deficiency': {
        'en': {
            'signs': ['Pale skin or eyes', 'Fatigue and weakness', 'Rapid heartbeat', 'Shortness of breath'],
            'foods': ['Red meat, liver', 'Legumes (lentils, beans)', 'Dark leafy greens (kale, spinach)', 'Fortified injera or porridge'],
            'tips': ['Eat vitamin C foods with iron-rich foods to improve absorption', 'Avoid tea/coffee with meals', 'Cook in iron pots'],
            'action': 'Refer for hemoglobin test if signs persist',
        },
        'am': {
            'signs': ['ፈዛዛ ቆዳ ወይም ዓይን', 'ድካምና ድካም', 'ፈጣን የልብ ምት'],
            'foods': ['ቀይ ሥጋ፣ ጉበት', 'ጥራጥሬ (ምስር፣ ባቄላ)', 'ጥቁር አረንጓዴ ቅጠሎች', 'ምሽት ወይም ገንፎ'],
            'tips': ['ቫይታሚን ሲ ምግቦችን ከብረት ምግቦች ጋር ይብሉ', 'ምግብ ጊዜ ሻይ/ቡና ያስወግዱ'],
            'action': 'ምልክቶቹ ከቀጠሉ ለሄሞግሎቢን ምርመራ ይላኩ',
        },
    },
    'vitamin_a_deficiency': {
        'en': {
            'signs': ['Night blindness', 'Dry eyes', 'Frequent infections', 'Slow wound healing'],
            'foods': ['Orange/yellow vegetables (carrots, pumpkin, sweet potato)', 'Dark leafy greens', 'Eggs, liver', 'Fortified foods'],
            'tips': ['Give vitamin A supplement every 6 months for children 6–59 months', 'Cook vegetables in oil to improve absorption'],
            'action': 'Refer for vitamin A supplementation if signs present',
        },
        'am': {
            'signs': ['የሌሊት ዕውርነት', 'ደረቅ ዓይኖች', 'ተደጋጋሚ ኢንፌክሽኖች'],
            'foods': ['ብርቱካናማ/ቢጫ አትክልቶች', 'ጥቁር አረንጓዴ ቅጠሎች', 'እንቁላል፣ ጉበት'],
            'tips': ['ለ6–59 ወር ልጆች በ6 ወር ቫይታሚን ኤ ይስጡ'],
            'action': 'ምልክቶቹ ካሉ ለቫይታሚን ኤ ሕክምና ይላኩ',
        },
    },
    'zinc_deficiency': {
        'en': {
            'signs': ['Poor growth', 'Frequent diarrhea', 'Skin rashes', 'Poor appetite'],
            'foods': ['Meat, poultry, fish', 'Legumes', 'Nuts and seeds', 'Whole grains'],
            'tips': ['Give zinc supplements during diarrhea treatment (10–20 mg/day for 10–14 days)', 'Soak legumes before cooking to improve zinc absorption'],
            'action': 'Give zinc with ORS during diarrhea',
        },
        'am': {
            'signs': ['ደካማ ዕድገት', 'ተደጋጋሚ ተቅማጥ', 'የቆዳ ሽፍታ'],
            'foods': ['ሥጋ፣ ዶሮ፣ ዓሳ', 'ጥራጥሬ', 'ለውዝ እና ዘሮች'],
            'tips': ['ተቅማጥ ሕክምና ወቅት ዚንክ ይስጡ (10–20 mg/ቀን ለ10–14 ቀናት)'],
            'action': 'ተቅማጥ ወቅት ዚንክ ከ ORS ጋር ይስጡ',
        },
    },
}

# ── SAM/MAM Therapeutic Feeding ───────────────────────────────────────────────
THERAPEUTIC_FEEDING = {
    'SAM': {
        'en': {
            'title': 'Severe Acute Malnutrition (SAM)',
            'criteria': 'MUAC < 11.5 cm OR weight-for-height Z-score < -3 OR bilateral oedema',
            'action': 'REFER IMMEDIATELY to health center for RUTF (Ready-to-Use Therapeutic Food)',
            'home_care': [
                'Continue breastfeeding if child is breastfed',
                'Give RUTF as prescribed — do not share with other family members',
                'Bring child for weekly follow-up',
                'Watch for danger signs: not eating, vomiting, fever, swelling',
            ],
        },
        'am': {
            'title': 'ከባድ አጣዳፊ የምግብ ዕጦት (SAM)',
            'criteria': 'MUAC < 11.5 ሴ.ሜ ወይም ሁለቱም እግሮች ያብጣሉ',
            'action': 'ወዲያውኑ ወደ ጤና ጣቢያ ይላኩ ለ RUTF ሕክምና',
            'home_care': [
                'ጡት ማጥባቱን ይቀጥሉ',
                'RUTF እንደታዘዘ ይስጡ',
                'ለሳምንታዊ ክትትል ያምጡ',
            ],
        },
    },
    'MAM': {
        'en': {
            'title': 'Moderate Acute Malnutrition (MAM)',
            'criteria': 'MUAC 11.5–12.4 cm OR weight-for-height Z-score -2 to -3',
            'action': 'Enroll in supplementary feeding program; refer to health center',
            'home_care': [
                'Increase meal frequency to 5 times per day',
                'Add energy-dense foods: oil, groundnut paste, eggs',
                'Give micronutrient supplements as prescribed',
                'Return for monthly growth monitoring',
            ],
        },
        'am': {
            'title': 'መካከለኛ አጣዳፊ የምግብ ዕጦት (MAM)',
            'criteria': 'MUAC 11.5–12.4 ሴ.ሜ',
            'action': 'ወደ ተጨማሪ ምግብ ፕሮግራም ይመዝግቡ',
            'home_care': [
                'የምግብ ድግግሞሽ ወደ 5 ጊዜ ይጨምሩ',
                'ኃይል ሰጪ ምግቦችን ያካትቱ: ዘይት፣ ቅቤ፣ እንቁላል',
                'ለወርሃዊ ዕድገት ክትትል ይምጡ',
            ],
        },
    },
}


def get_iycf_guidance(age_months: int, language: str = 'en') -> dict:
    """Return IYCF guidance for a child's age."""
    lang_data = IYCF_GUIDANCE.get(language, IYCF_GUIDANCE['en'])
    if age_months < 6:
        key = '0_6_months'
    elif age_months <= 24:
        key = '6_24_months'
    else:
        key = 'over_24_months'
    return lang_data.get(key, IYCF_GUIDANCE['en'][key])


def get_micronutrient_guidance(deficiency: str, language: str = 'en') -> dict:
    """Return guidance for a specific micronutrient deficiency."""
    data = MICRONUTRIENT_GUIDANCE.get(deficiency, {})
    return data.get(language, data.get('en', {}))


def get_therapeutic_feeding_protocol(status: str, language: str = 'en') -> dict:
    """Return therapeutic feeding protocol for SAM or MAM."""
    data = THERAPEUTIC_FEEDING.get(status.upper(), {})
    return data.get(language, data.get('en', {}))


def assess_nutrition_risk(age_months: int, muac_cm: float = None,
                           breastfed: bool = None, language: str = 'en') -> dict:
    """Quick nutrition risk assessment."""
    risks = []
    recommendations = []

    if muac_cm is not None:
        if muac_cm < 11.5:
            risks.append('SAM')
            recommendations.append(get_therapeutic_feeding_protocol('SAM', language))
        elif muac_cm < 12.5:
            risks.append('MAM')
            recommendations.append(get_therapeutic_feeding_protocol('MAM', language))

    if age_months < 6 and breastfed is False:
        risks.append('not_exclusively_breastfed')

    iycf = get_iycf_guidance(age_months, language)

    return {
        'age_months': age_months,
        'muac_cm': muac_cm,
        'risks': risks,
        'iycf_guidance': iycf,
        'therapeutic_protocols': recommendations,
        'urgent': 'SAM' in risks,
    }
