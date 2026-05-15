"""
USSD/IVR state machine engine.
Drives: LanguageSelect → SymptomMenu → GuidanceResult → SMSOffer
All responses ≤160 chars per page. Sessions logged with SHA-256 hash (no PII).
"""
import hashlib
from core.symptom_engine import assess
from core.knowledge_base import get_facilities
from core.geolocation import find_nearest_facilities

# ── Language menu ─────────────────────────────────────────────────────────────
LANGUAGE_MENU = {
    'en': 'CON Welcome to Health Assistant\n1. English\n2. Amharic\n3. Oromo\n4. Tigrinya',
    'am': 'CON እንኳን ደህና መጡ\n1. English\n2. አማርኛ\n3. Oromo\n4. Tigrinya',
    'om': "CON Baga nagaan dhuftan\n1. English\n2. Amharic\n3. Oromoo\n4. Tigrinya",
    'ti': 'CON ሰላም ምጻእ\n1. English\n2. Amharic\n3. Oromo\n4. ትግርኛ',
}
LANG_MAP = {'1': 'en', '2': 'am', '3': 'om', '4': 'ti'}

# ── Symptom menu ──────────────────────────────────────────────────────────────
SYMPTOM_MENU = {
    'en': 'CON Select your main symptom:\n1. Fever\n2. Cough\n3. Stomach pain\n4. Difficulty breathing\n5. Other',
    'am': 'CON ዋና ምልክትዎን ይምረጡ:\n1. ትኩሳት\n2. ሳል\n3. የሆድ ህመም\n4. የትንፋሽ ችግር\n5. ሌላ',
    'om': "CON Mallattoo filadhu:\n1. Ho'aa\n2. Qufaa\n3. Dhukkuba garaa\n4. Rakkoo hafuura\n5. Kan biraa",
    'ti': 'CON ምልክትካ ምረጽ:\n1. ረስኒ\n2. ሳዕዓል\n3. ቃንዛ ከብዲ\n4. ጸገም ምስትንፋስ\n5. ካልእ',
}
SYMPTOM_MAP = {
    '1': 'fever', '2': 'cough', '3': 'stomach pain',
    '4': 'difficulty breathing', '5': 'other symptoms',
}

# ── Guidance templates ────────────────────────────────────────────────────────
GUIDANCE = {
    'emergency': {
        'en': 'END EMERGENCY: Go to hospital NOW. Call 907.',
        'am': 'END አስቸኳይ: አሁን ሆስፒታል ይሂዱ። 907 ይደውሉ።',
        'om': 'END Ariifachiisaa: Hospitaala deemi. 907 bilbili.',
        'ti': 'END ህጹጽ: ሕጂ ሆስፒታል ኺድ። 907 ደውል።',
    },
    'visit_health_center': {
        'en': 'END Visit your nearest health center today. Bring this message.',
        'am': 'END ዛሬ ወደ ቅርብ ጤና ጣቢያ ይሂዱ።',
        'om': "END Har'a giddugala fayyaa dhiyoo deemi.",
        'ti': 'END ሎሚ ናብ ቀረባ ጥዕና ጣቢያ ኺድ።',
    },
    'self_care': {
        'en': 'END Rest, drink fluids, monitor symptoms. See HEW if worse.',
        'am': 'END ያርፉ፣ ፈሳሽ ይጠጡ። ካልተሻሉ ጤና ሠራተኛ ያነጋግሩ።',
        'om': 'END Boqo, bishaan dhugdi. Yoo hammaate HEW quunnamii.',
        'ti': 'END ዕረፍ፣ ፈሳሺ ስተ። ዝኸፍአ እንተኾይኑ HEW ርኸቦ።',
    },
}

SMS_OFFER = {
    'en': 'CON Send result as SMS?\n1. Yes\n2. No',
    'am': 'CON ውጤቱን SMS ይላኩ?\n1. አዎ\n2. አይ',
    'om': 'CON Firii SMS erguu?\n1. Eeyyee\n2. Lakki',
    'ti': 'CON ውጽኢት SMS ስደድ?\n1. እወ\n2. ኣይፋሉን',
}


def hash_session(session_id: str) -> str:
    return hashlib.sha256(session_id.encode()).hexdigest()


def process_ussd(session_id: str, phone: str, text: str, service_code: str = '') -> dict:
    """
    Process a USSD request and return the response text + session log data.
    text is the accumulated input string from Africa's Talking (e.g. '1*2').
    """
    steps = [s.strip() for s in text.split('*')] if text else []
    lang  = 'en'
    symptom = None
    urgency = None

    # Step 0: language selection
    if len(steps) == 0 or steps[0] == '':
        return {
            'response': LANGUAGE_MENU.get('en'),
            'session_hash': hash_session(session_id),
            'lang': '',
            'symptom': '',
            'urgency': '',
            'completed': False,
        }

    lang = LANG_MAP.get(steps[0], 'en')

    # Step 1: symptom selection
    if len(steps) == 1:
        return {
            'response': SYMPTOM_MENU.get(lang, SYMPTOM_MENU['en']),
            'session_hash': hash_session(session_id),
            'lang': lang,
            'symptom': '',
            'urgency': '',
            'completed': False,
        }

    symptom_key = steps[1]
    symptom     = SYMPTOM_MAP.get(symptom_key, 'other symptoms')

    # Step 2: guidance result
    if len(steps) == 2:
        result  = assess([symptom], age=25, sex='unknown', language=lang)
        urgency = result.get('urgency', 'self_care')
        guidance_text = GUIDANCE.get(urgency, GUIDANCE['self_care']).get(lang, GUIDANCE['self_care']['en'])

        # Append nearest facility for emergency
        if urgency == 'emergency':
            facilities = get_facilities()
            if facilities:
                f = facilities[0]
                phone_str = f.get('phone', '907')
                guidance_text = guidance_text.replace('907', phone_str)

        # Offer SMS if not emergency
        if urgency != 'emergency':
            return {
                'response': SMS_OFFER.get(lang, SMS_OFFER['en']),
                'session_hash': hash_session(session_id),
                'lang': lang,
                'symptom': symptom,
                'urgency': urgency,
                'completed': False,
                '_guidance': guidance_text,
            }

        return {
            'response': guidance_text,
            'session_hash': hash_session(session_id),
            'lang': lang,
            'symptom': symptom,
            'urgency': urgency,
            'completed': True,
            'sms_sent': False,
        }

    # Step 3: SMS offer response
    if len(steps) >= 3:
        result  = assess([symptom], age=25, sex='unknown', language=lang)
        urgency = result.get('urgency', 'self_care')
        guidance_text = GUIDANCE.get(urgency, GUIDANCE['self_care']).get(lang, GUIDANCE['self_care']['en'])
        sms_choice = steps[2]
        sms_sent   = sms_choice == '1'

        end_msg = guidance_text.replace('CON ', 'END ')
        return {
            'response': end_msg,
            'session_hash': hash_session(session_id),
            'lang': lang,
            'symptom': symptom,
            'urgency': urgency,
            'completed': True,
            'sms_sent': sms_sent,
            'sms_phone': phone if sms_sent else '',
            'sms_body': guidance_text.replace('END ', '').replace('CON ', '') if sms_sent else '',
        }

    return {
        'response': 'END Thank you. Stay healthy.',
        'session_hash': hash_session(session_id),
        'lang': lang,
        'symptom': symptom or '',
        'urgency': urgency or '',
        'completed': True,
        'sms_sent': False,
    }
