"""
Consent Manager — bilingual informed-consent scripts and logic.
Supports: en, am, om, ti
"""

CONSENT_SCRIPTS = {
    'en': {
        'text': (
            "Before we begin, I need your permission. "
            "This assistant will ask about your symptoms to give health guidance. "
            "We collect only: symptoms, age range, sex, and language. "
            "We do NOT collect your name or phone number. "
            "Your data is stored securely and used only to help you. "
            "You can stop and delete your data at any time. "
            "Do you agree? Press 1 or say YES to continue."
        ),
        'agree_keywords': ['yes', 'agree', '1', 'ok', 'okay'],
        'withdraw_keywords': ['no', 'stop', 'cancel', 'withdraw', '0'],
        'caregiver_prompt': (
            "Are you answering on behalf of someone else? "
            "Press 2 or say CAREGIVER to use Caregiver Mode."
        ),
        'minor_warning': (
            "It looks like you may be under 18. "
            "Please ask a trusted adult to help you use this assistant. "
            "Press 3 or say HELP to find a community health volunteer near you."
        ),
        'withdraw_confirm': (
            "Your session has been stopped and all data deleted. "
            "Thank you. Stay safe."
        ),
        'disclaimer': (
            "️ This is not a clinical diagnosis. "
            "Always consult a qualified health worker for medical decisions."
        ),
    },
    'am': {
        'text': (
            "ከመጀመራችን በፊት ፈቃድዎ ያስፈልጋል። "
            "ይህ ረዳት ምልክቶችዎን ይጠይቃል። "
            "የምንሰበስበው፡ ምልክቶች፣ የዕድሜ ክልል፣ ጾታ እና ቋንቋ ብቻ ነው። "
            "ስምዎን ወይም ስልክ ቁጥርዎን አንሰበስብም። "
            "ለመቀጠል 1 ይጫኑ ወይም አዎ ይበሉ።"
        ),
        'agree_keywords': ['አዎ', 'እሺ', '1', 'yes'],
        'withdraw_keywords': ['አይ', 'አቁም', '0', 'no'],
        'caregiver_prompt': (
            "ለሌላ ሰው ምላሽ እየሰጡ ነው? "
            "2 ይጫኑ ወይም 'ተንከባካቢ' ይበሉ።"
        ),
        'minor_warning': (
            "ዕድሜዎ ከ18 ዓመት በታች ሊሆን ይችላል። "
            "እባክዎ የሚያምኑት አዋቂ ሰው ይጠይቁ።"
        ),
        'withdraw_confirm': (
            "ክፍለ ጊዜዎ ተቋርጧል እና ሁሉም ውሂብ ተሰርዟል። ጤና ይስጥልን።"
        ),
        'disclaimer': (
            "️ ይህ ክሊኒካዊ ምርመራ አይደለም። "
            "ሁልጊዜ ለህክምና ውሳኔ ብቁ የጤና ሠራተኛ ያማክሩ።"
        ),
    },
    'om': {
        'text': (
            "Jalqabuun dura hayyama keessan barbaachisa. "
            "Gargaaraan kun mallattoolee keessan gaafata. "
            "Odeeffannoo walitti qabnu: mallattoolee, umurii, saala fi afaan qofa. "
            "Maqaa ykn lakkoofsa bilbilaa hin walitti qabu. "
            "Itti fufuuf 1 tuqi ykn EYYEE jedhi."
        ),
        'agree_keywords': ['eyyee', 'haa ta\'u', '1', 'yes'],
        'withdraw_keywords': ['lakki', 'dhaabi', '0', 'no'],
        'caregiver_prompt': "Nama biraa bakka bu\'uun deebii kennaa jirtaa? 2 tuqi.",
        'minor_warning': "Umuriin kee waggaa 18 gadii ta\'uu danda\'a. Obboleessa/obboleettii amantaa qabu gaafadhu.",
        'withdraw_confirm': "Marii kee dhaabame. Odeeffannoon hundi haaqame. Nagaan turi.",
        'disclaimer': "️ Kun dhukkuba adda baasuu miti. Ogeessa fayyaa mariisi.",
    },
    'ti': {
        'text': (
            "ቅድሚ ምጅማርና ፍቓድኩም የድሊ። "
            "እዚ ሓጋዚ ምልክታትኩም ክሓትት እዩ። "
            "ዝእክቦ ሓበሬታ፡ ምልክታት፣ ዕድሜ፣ ጾታን ቋንቋን ጥራይ እዩ። "
            "ንምቕጻል 1 ጠውቑ ወይ እወ በሉ።"
        ),
        'agree_keywords': ['እወ', 'ሕራይ', '1', 'yes'],
        'withdraw_keywords': ['ኣይፋል', 'ደው', '0', 'no'],
        'caregiver_prompt': "ንካልእ ሰብ ትምልስ ኣለኻ? 2 ጠውቕ።",
        'minor_warning': "ዕድሜኻ ትሕቲ 18 ክኸውን ይኽእል። ዝኣምኖ ዓቢ ሰብ ሕተት።",
        'withdraw_confirm': "ኣኼባኻ ተቋሪጹ። ኩሉ ሓበሬታ ተሰሪዙ። ጥዕና ይሃብካ።",
        'disclaimer': "️ እዚ ክሊኒካዊ ምርመራ ኣይኮነን። ሓኪም ወይ ሰራሕተኛ ጥዕና ተወከስ።",
    },
}


def get_consent_script(language: str) -> dict:
    return CONSENT_SCRIPTS.get(language, CONSENT_SCRIPTS['en'])


def check_consent_response(user_input: str, language: str) -> str:
    """Returns 'agree', 'withdraw', 'caregiver', or 'unknown'."""
    text = user_input.strip().lower()
    script = get_consent_script(language)
    if text in [k.lower() for k in script['agree_keywords']]:
        return 'agree'
    if text in [k.lower() for k in script['withdraw_keywords']]:
        return 'withdraw'
    if text in ['2', 'caregiver', 'ተንከባካቢ', 'bakka bu\'uu']:
        return 'caregiver'
    return 'unknown'
