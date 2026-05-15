"""
Localization Service — multilingual strings for English, Amharic, Oromo, and Tigrinya.
Falls back: requested lang -> am -> en
"""
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

SUPPORTED_LANGUAGES = ['en', 'am', 'om', 'ti']


def get_safe_message(language: str) -> str:
    """Get safe uncertainty message. Falls back to English for unsupported languages."""
    return SAFE_MESSAGES.get(language, SAFE_MESSAGES['en'])


def get_ivr_menu(language: str) -> dict:
    """Get IVR menu strings. Falls back to English for unsupported languages."""
    return IVR_MENUS.get(language, IVR_MENUS['en'])

# Safe-uncertainty messages per language
SAFE_MESSAGES = {
    'en': "I'm not sure — please contact your nearest health worker or visit your local health center.",
    'am': "እርግጠኛ አይደለሁም — እባክዎ ወደ ቅርብ ጤና ሠራተኛ ይሂዱ ወይም ወደ ጤና ጣቢያ ይደውሉ።",
    'om': "Hin beeku — ogeessa fayyaa ykn buufata fayyaa dhiyoo deemi.",
    'ti': "ኣይፈልጥን — ናብ ቀረባ ሰራሕተኛ ጥዕና ወይ ጥዕና ጣቢያ ኪድ።",
}

# IVR menu prompts per language (≤10 seconds when spoken at normal pace)
IVR_MENUS = {
    'en': {
        'welcome': "Welcome to Health Assistant. Press 1 for English.",
        'lang_select': "Select language: 1 English, 2 Amharic, 3 Oromo, 4 Tigrinya.",
        'symptom_prompt': "What is your main symptom? Press 1 Fever, 2 Cough, 3 Stomach pain, 4 Other. Press 0 to repeat.",
        'duration_prompt': "How many days? Press 1 for one day, 2 for two to three days, 3 for more than three days.",
        'other_symptoms': "Do you have other symptoms? Press 1 Yes, 2 No.",
        'age_prompt': "Your age group: Press 1 under 5, 2 child 5 to 17, 3 adult 18 to 59, 4 elder 60 plus.",
        'sex_prompt': "Press 1 for Male, 2 for Female.",
        'emergency': "EMERGENCY. Go to a health facility NOW. Call your nearest hospital.",
        'result_intro': "Based on your symptoms, here is your health guidance.",
        'sms_offer': "Press 1 to receive this result by SMS.",
        'repeat': "Press 0 to repeat this message.",
        'goodbye': "Thank you. Stay safe. Goodbye.",
    },
    'am': {
        'welcome': "ወደ ጤና ረዳት እንኳን ደህና መጡ። ለአማርኛ 2 ይጫኑ።",
        'lang_select': "ቋንቋ ይምረጡ፡ 1 እንግሊዝኛ፣ 2 አማርኛ፣ 3 ኦሮምኛ፣ 4 ትግርኛ።",
        'symptom_prompt': "ዋናው ምልክትዎ ምንድን ነው? 1 ትኩሳት፣ 2 ሳል፣ 3 የሆድ ህመም፣ 4 ሌላ። ለድጋሚ 0።",
        'duration_prompt': "ለምን ያህል ቀናት? 1 አንድ ቀን፣ 2 ሁለት ወይም ሶስት ቀናት፣ 3 ከሶስት ቀን በላይ።",
        'other_symptoms': "ሌሎች ምልክቶች አሉዎ? 1 አዎ፣ 2 አይ።",
        'age_prompt': "የዕድሜ ክልልዎ፡ 1 ከ5 ዓመት በታች፣ 2 ልጅ 5-17፣ 3 ጎልማሳ 18-59፣ 4 አዛውንት 60+።",
        'sex_prompt': "1 ወንድ፣ 2 ሴት።",
        'emergency': "አስቸኳይ። ወዲያውኑ ወደ ጤና ጣቢያ ይሂዱ።",
        'result_intro': "ምልክቶቹ ላይ ተመስርቶ የጤና መመሪያ ይኸውና።",
        'sms_offer': "ውጤቱን በSMS ለመቀበል 1 ይጫኑ።",
        'repeat': "ለድጋሚ 0 ይጫኑ።",
        'goodbye': "አመሰግናለሁ። ጤና ይስጥልን።",
    },
    'om': {
        'welcome': "Gargaaraa Fayyaatti baga nagaan dhuftan. Afaan Oromoof 3 tuqi.",
        'lang_select': "Afaan filadhu: 1 Inglizii, 2 Amaaraa, 3 Oromoo, 4 Tigrinya.",
        'symptom_prompt': "Mallattoo ijoo kee maali? 1 Ho\'a, 2 Qufaa, 3 Dhukkuba garaa, 4 Kan biraa. 0 irra deebi\'i.",
        'duration_prompt': "Guyyaa meeqa? 1 guyyaa tokko, 2 guyyaa 2-3, 3 guyyaa 3 ol.",
        'other_symptoms': "Mallattoo biraa qabdaa? 1 Eyyee, 2 Lakki.",
        'age_prompt': "Umurii: 1 waggaa 5 gadii, 2 daa\'ima 5-17, 3 ga\'eela 18-59, 4 jaarsa 60+.",
        'sex_prompt': "1 Dhiira, 2 Dhalaa.",
        'emergency': "ARIIFACHIISAA. Amma buufata fayyaa deemi.",
        'result_intro': "Mallattoolee kee irratti hundaa\'uun gorsa fayyaa kee asii jira.",
        'sms_offer': "Bu\'aa SMS\'n argachuuf 1 tuqi.",
        'repeat': "Irra deebi\'uuf 0 tuqi.",
        'goodbye': "Galatoomi. Nagaan turi.",
    },
    'ti': {
        'welcome': "ናብ ሓጋዚ ጥዕና እንቋዕ ብደሓን መጻእካ። ትግርኛ ንምምራጽ 4 ጠውቕ።",
        'lang_select': "ቋንቋ ምረጽ: 1 እንግሊዝ, 2 ኣምሓርኛ, 3 ኦሮምኛ, 4 ትግርኛ።",
        'symptom_prompt': "ዋና ምልክትካ እንታይ እዩ? 1 ረስኒ, 2 ሳዕዓል, 3 ቃንዛ ከብዲ, 4 ካልእ። 0 ደጊም።",
        'duration_prompt': "ክንደይ መዓልቲ? 1 ሓደ መዓልቲ, 2 ክልተ ወይ ሰለስተ, 3 ልዕሊ ሰለስተ።",
        'other_symptoms': "ካልእ ምልክታት ኣለካ? 1 እወ, 2 ኣይፋል።",
        'age_prompt': "ዕድሜ: 1 ትሕቲ 5, 2 ቆልዓ 5-17, 3 ዓቢ 18-59, 4 ኣረጋዊ 60+።",
        'sex_prompt': "1 ተባዕታይ, 2 ኣንስታይ።",
        'emergency': "ህጹጽ። ሕጂ ናብ ጥዕና ጣቢያ ኪድ።",
        'result_intro': "ብምልክታትካ ዝተሞርኮሰ ምኽሪ ጥዕና ኣሎ።",
        'sms_offer': "ብSMS ንምቕባል 1 ጠውቕ።",
        'repeat': "ንምድጋም 0 ጠውቕ።",
        'goodbye': "የቐንየለይ። ጥዕና ይሃብካ።",
    },
}

# Simple Mode symptom text labels (used as pictogram fallback)
SYMPTOM_PICTOGRAMS = {
    'fever':                'Fever',
    'cough':                'Cough',
    'headache':             'Headache',
    'stomach pain':         'Stomach Pain',
    'diarrhea':             'Diarrhea',
    'vomiting':             'Vomiting',
    'fatigue':              'Fatigue',
    'difficulty breathing': 'Breathing Difficulty',
    'chest pain':           'Chest Pain',
    'rash':                 'Rash',
    'weight loss':          'Weight Loss',
    'dizziness':            'Dizziness',
    'default':              'Symptom',
}

URGENCY_PICTOGRAMS = {
    'emergency':           'EMERGENCY',
    'visit_health_center': 'Visit Health Center',
    'self_care':           'Self-Care',
}

def get_symptom_pictogram(symptom: str) -> str:
    return SYMPTOM_PICTOGRAMS.get(symptom.lower(), SYMPTOM_PICTOGRAMS['default'])


def get_urgency_pictogram(urgency: str) -> str:
    return URGENCY_PICTOGRAMS.get(urgency, '')


def localize(key: str, strings: dict, language: str, fallback_chain=('am', 'en')) -> str:
    """Get a localized string with fallback chain."""
    val = strings.get(f'{key}_{language}')
    if val:
        return val
    for fb in fallback_chain:
        val = strings.get(f'{key}_{fb}')
        if val:
            return val
    return strings.get(key, '')
