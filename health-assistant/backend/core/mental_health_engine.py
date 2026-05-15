"""
Mental Health Screening Engine.
PHQ-2 depression screen + GAD-2 anxiety screen with culturally adapted messaging.
Includes referral guidance and crisis response for Ethiopia context.
"""

# ── PHQ-2 Questions ───────────────────────────────────────────────────────────
PHQ2_QUESTIONS = {
    'en': [
        "Over the past 2 weeks, how often have you felt little interest or pleasure in doing things?",
        "Over the past 2 weeks, how often have you felt down, depressed, or hopeless?",
    ],
    'am': [
        "ባለፉት 2 ሳምንታት ምን ያህል ጊዜ ነገሮችን ለማድረግ ፍላጎት ወይም ደስታ አልተሰማዎትም?",
        "ባለፉት 2 ሳምንታት ምን ያህል ጊዜ ተስፋ ቢስ ወይም ሀዘን ተሰምቶዎታል?",
    ],
    'om': [
        "Torban 2 darban keessatti, yeroo meeqa wantoota gochuu keessatti fedhii ykn gammachuu dhabde?",
        "Torban 2 darban keessatti, yeroo meeqa gadda, gaddaa, ykn abdii kutannaa dhagahde?",
    ],
    'ti': [
        "ኣብ ዝሓለፈ 2 ሰሙናት፡ ክንደይ ጊዜ ኣብ ምግባር ነገራት ድሌት ወይ ሓጎስ ኣይተሰምዓካን?",
        "ኣብ ዝሓለፈ 2 ሰሙናት፡ ክንደይ ጊዜ ጓሂ፡ ጭንቀት ወይ ተስፋ ምቑራጽ ተሰምዓካ?",
    ],
}

# ── GAD-2 Questions ───────────────────────────────────────────────────────────
GAD2_QUESTIONS = {
    'en': [
        "Over the past 2 weeks, how often have you felt nervous, anxious, or on edge?",
        "Over the past 2 weeks, how often have you not been able to stop or control worrying?",
    ],
    'am': [
        "ባለፉት 2 ሳምንታት ምን ያህል ጊዜ ነርቭ፣ ጭንቀት ወይም ስጋት ተሰምቶዎታል?",
        "ባለፉት 2 ሳምንታት ምን ያህል ጊዜ ስጋቶን ማቆም ወይም መቆጣጠር አልቻሉም?",
    ],
    'om': [
        "Torban 2 darban keessatti, yeroo meeqa yaaddoo, sodaa, ykn rifannaa dhagahde?",
        "Torban 2 darban keessatti, yeroo meeqa yaaddoo dhaabuu ykn to'achuu hin dandeenye?",
    ],
    'ti': [
        "ኣብ ዝሓለፈ 2 ሰሙናት፡ ክንደይ ጊዜ ጭንቀት፡ ሻቕሎት ወይ ምስቓቕ ተሰምዓካ?",
        "ኣብ ዝሓለፈ 2 ሰሙናት፡ ክንደይ ጊዜ ሻቕሎትካ ምቁጽጻር ኣይከኣልካን?",
    ],
}

SCORE_OPTIONS = {
    'en': ['Not at all (0)', 'Several days (1)', 'More than half the days (2)', 'Nearly every day (3)'],
    'am': ['ጭራሽ አይደለም (0)', 'ጥቂት ቀናት (1)', 'ከግማሽ ቀናት በላይ (2)', 'ሁሉም ቀናት ማለት ይቻላል (3)'],
    'om': ['Gonkumaa miti (0)', 'Guyyoota muraasa (1)', 'Guyyoota walakkaa ol (2)', "Guyyaa hunda jechuun ni danda'ama (3)"],
    'ti': ['ፈጺሙ ኣይኮነን (0)', 'ሒደት መዓልታት (1)', 'ካብ ፍርቂ መዓልታት ንላዕሊ (2)', 'ኩሉ ቀን ማለት ይከኣል (3)'],
}

# ── Interpretation ────────────────────────────────────────────────────────────

def interpret_phq2(score: int, language: str = 'en') -> dict:
    """Interpret PHQ-2 score (0-6). Score ≥3 = positive screen."""
    if score >= 3:
        level = 'positive'
        msgs = {
            'en': "Your answers suggest you may be experiencing depression. This is common and treatable. Please speak with a health worker.",
            'am': "መልሶቹ ድብርት ሊኖርብዎ እንደሚችል ያሳያሉ። ይህ የተለመደ ሲሆን ሊታከም ይችላል። እባክዎ ከጤና ሠራተኛ ጋር ያነጋግሩ።",
            'om': "Deebiin kee gaddaa qabda jedha. Kun baay'ee mul'ata, fayyuu danda'a. Ogeessa fayyaa mariisi.",
            'ti': "መልስታትካ ጓሂ ከምዘሎካ ይሕብር። እዚ ልሙድ ኮይኑ ክፍወስ ይኽእል። ምስ ሰራሕተኛ ጥዕና ዘረባ ግበር።",
        }
        action = 'refer_to_health_worker'
    else:
        level = 'negative'
        msgs = {
            'en': "Your answers do not suggest significant depression at this time. Continue to monitor how you feel.",
            'am': "መልሶቹ አሁን ከፍተኛ ድብርት አለ አያሳዩም። ስሜቶን መከታተሉን ይቀጥሉ።",
            'om': "Deebiin kee yeroo kana gaddaa guddaa hin agarsiisu. Haala kee hordofuu itti fufi.",
            'ti': "መልስታትካ ሕጂ ዓቢ ጓሂ ከምዘሎካ ኣይሕብርን። ስምዒትካ ምክትታል ቀጽሎ።",
        }
        action = 'monitor'

    return {
        'screen': 'PHQ-2',
        'score': score,
        'level': level,
        'message': msgs.get(language, msgs['en']),
        'action': action,
    }


def interpret_gad2(score: int, language: str = 'en') -> dict:
    """Interpret GAD-2 score (0-6). Score ≥3 = positive screen."""
    if score >= 3:
        level = 'positive'
        msgs = {
            'en': "Your answers suggest you may be experiencing anxiety. Please speak with a health worker who can help.",
            'am': "መልሶቹ ጭንቀት ሊኖርብዎ እንደሚችል ያሳያሉ። ሊረዳዎ ከሚችል ጤና ሠራተኛ ጋር ያነጋግሩ።",
            'om': "Deebiin kee yaaddoo qabda jedha. Ogeessa fayyaa si gargaaruu danda'u mariisi.",
            'ti': "መልስታትካ ሻቕሎት ከምዘሎካ ይሕብር። ምስ ሰራሕተኛ ጥዕና ዘረባ ግበር።",
        }
        action = 'refer_to_health_worker'
    else:
        level = 'negative'
        msgs = {
            'en': "Your answers do not suggest significant anxiety at this time.",
            'am': "መልሶቹ አሁን ከፍተኛ ጭንቀት አለ አያሳዩም።",
            'om': "Deebiin kee yeroo kana yaaddoo guddaa hin agarsiisu.",
            'ti': "መልስታትካ ሕጂ ዓቢ ሻቕሎት ከምዘሎካ ኣይሕብርን።",
        }
        action = 'monitor'

    return {
        'screen': 'GAD-2',
        'score': score,
        'level': level,
        'message': msgs.get(language, msgs['en']),
        'action': action,
    }


def crisis_response(language: str = 'en') -> dict:
    """Return crisis support message for suicidal ideation."""
    msgs = {
        'en': "If you are having thoughts of harming yourself, please tell a trusted person immediately and go to your nearest health center. You are not alone.",
        'am': "ራስዎን ለመጉዳት ሀሳብ ካለዎ፣ ወዲያውኑ ለሚያምኑት ሰው ይናገሩ እና ወደ ቅርብ ጤና ጣቢያ ይሂዱ። ብቻዎን አይደሉም።",
        'om': "Of miidhuuf yaada yoo qabaatte, namni amanamaa tokko itti himi, buufata fayyaa dhiyoo deemi. Kophaa miti.",
        'ti': "ነብስኻ ንምጉዳእ ሓሳብ እንተሃልዩካ፡ ንዝኣምኖ ሰብ ወዲኡ ንገሮ ናብ ቀረባ ጥዕና ጣቢያ ኺድ። ጥራይካ ኣይኮንካን።",
    }
    return {
        'crisis': True,
        'message': msgs.get(language, msgs['en']),
        'action': 'emergency_referral',
        'hotline': '907',
    }


def run_mental_health_screen(phq2_scores: list, gad2_scores: list, language: str = 'en') -> dict:
    """
    Run both PHQ-2 and GAD-2 screens.
    phq2_scores: list of 2 ints (0-3 each)
    gad2_scores: list of 2 ints (0-3 each)
    """
    phq2_total = sum(phq2_scores[:2]) if len(phq2_scores) >= 2 else 0
    gad2_total = sum(gad2_scores[:2]) if len(gad2_scores) >= 2 else 0

    phq2_result = interpret_phq2(phq2_total, language)
    gad2_result = interpret_gad2(gad2_total, language)

    needs_referral = phq2_result['action'] == 'refer_to_health_worker' or \
                     gad2_result['action'] == 'refer_to_health_worker'

    cultural_note = {
        'en': "Mental health is part of overall health. Seeking help is a sign of strength, not weakness.",
        'am': "የአዕምሮ ጤና የጠቅላላ ጤና አካል ነው። እርዳታ መጠየቅ ጥንካሬ ምልክት ነው።",
        'om': "Fayyaan sammuu fayyaa waliigalaa keessaa tokko. Gargaarsa gaafachuun jabina mallattoo dha.",
        'ti': "ጥዕና ኣእምሮ ካብ ሓፈሻዊ ጥዕና ሓደ ኢዩ። ሓገዝ ምሕታት ምልክት ጥንካረ ኢዩ።",
    }

    return {
        'phq2': phq2_result,
        'gad2': gad2_result,
        'needs_referral': needs_referral,
        'cultural_note': cultural_note.get(language, cultural_note['en']),
        'questions': {
            'phq2': PHQ2_QUESTIONS.get(language, PHQ2_QUESTIONS['en']),
            'gad2': GAD2_QUESTIONS.get(language, GAD2_QUESTIONS['en']),
            'options': SCORE_OPTIONS.get(language, SCORE_OPTIONS['en']),
        },
    }


def get_screen_questions(language: str = 'en') -> dict:
    """Return all screening questions for the frontend to render."""
    return {
        'phq2_questions': PHQ2_QUESTIONS.get(language, PHQ2_QUESTIONS['en']),
        'gad2_questions': GAD2_QUESTIONS.get(language, GAD2_QUESTIONS['en']),
        'score_options': SCORE_OPTIONS.get(language, SCORE_OPTIONS['en']),
        'language': language,
    }
