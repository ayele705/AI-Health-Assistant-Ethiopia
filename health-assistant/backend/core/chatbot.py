"""
Conversational chatbot logic.
Manages multi-turn symptom interview sessions (in-memory for prototype).
"""
from .symptom_engine import assess

# In-memory session store: session_id -> state dict
_sessions: dict = {}

QUESTIONS_EN = [
    "Hello! I'm your health assistant. What is your main symptom today?",
    "How long have you had this symptom? (e.g. 1 day, 3 days)",
    "Do you have any other symptoms? (e.g. fever, cough, headache — or type 'no')",
    "What is your age?",
    "Are you male or female?",
]

QUESTIONS_AM = [
    "ሰላም! እኔ የጤና ረዳትዎ ነኝ። ዛሬ ዋናው ምልክትዎ ምንድን ነው?",
    "ይህ ምልክት ለምን ያህል ጊዜ ነበርዎ? (ለምሳሌ 1 ቀን፣ 3 ቀናት)",
    "ሌሎች ምልክቶች አሉዎ? (ለምሳሌ ትኩሳት፣ ሳል፣ ራስ ምታት — ወይም 'የለም' ይጻፉ)",
    "ዕድሜዎ ስንት ነው?",
    "ወንድ ነዎ ወይስ ሴት?",
]

QUESTIONS_TI = [
    "ሰላም! ሓጋዚ ጥዕናኻ እየ። ሎሚ ዋና ምልክትካ እንታይ እዩ?",
    "እዚ ምልክት ክንደይ ጊዜ ኣለካ? (ንኣብነት 1 መዓልቲ፣ 3 መዓልቲ)",
    "ካልእ ምልክታት ኣለካ? (ንኣብነት ረስኒ፣ ሳዕዓል፣ ቃንዛ ርእሲ — ወይ 'ኣይፋል' ጸሓፍ)",
    "ዕድሜኻ ክንደይ እዩ?",
    "ተባዕታይ ዲኻ ወይ ኣንስታይ?",
]

QUESTIONS_OM = [
    "Akkam! Gargaaraa fayyaa keetii dha. Har'a mallattoo ijoo kee maali?",
    "Mallattoon kun yeroo meeqa si waliin jira? (fkn guyyaa 1, guyyaa 3)",
    "Mallattoo biraa qabdaa? (fkn ho'a, qufaa, dhukkuba mataa — ykn 'lakki' barreessi)",
    "Umurii kee meeqa?",
    "Dhiira moo dhalaa?",
]

QUESTIONS_SID = [
    "Akkam! Gargaaraa fayyaa keetii dha. Har'a mallattoo ijoo kee maali?",
    "Mallattoon kun yeroo meeqa? (fkn guyyaa 1, guyyaa 3)",
    "Mallattoo biraa qabdaa? (fkn ho'a, qufaa — ykn 'lakki' barreessi)",
    "Umurii kee meeqa?",
    "Dhiira moo dhalaa?",
]

QUESTIONS_SO = [
    "Salaan! Kaaliyahaagu caafimaadkaaga ayaan ahay. Maanta calaamadaada ugu weyn maxay tahay?",
    "Muddo intee le'eg ayaad calaamaddan qabteen? (tusaale 1 maalin, 3 maalin)",
    "Ma leedahay calaamado kale? (tusaale qandho, qufac, madax xanuun — ama 'maya' qor)",
    "Da'daadu meeqa?",
    "Nin ma tahay mise naag?",
]

QUESTIONS_AA = [
    "Salaan! Caafimaadkaaga kaaliyahaagu ayaan ahay. Maanta calaamadaada ugu weyn maxay?",
    "Muddo intee le'eg ayaad calaamaddan qabteen?",
    "Ma leedahay calaamado kale? (ama 'maya' qor)",
    "Da'daadu meeqa?",
    "Nin ma tahay mise naag?",
]

QUESTIONS_WAL = [
    "Akkam! Gargaaraa fayyaa keetii dha. Har'a mallattoo ijoo kee maali?",
    "Mallattoon kun yeroo meeqa? (fkn guyyaa 1, guyyaa 3)",
    "Mallattoo biraa qabdaa? (ykn 'lakki' barreessi)",
    "Umurii kee meeqa?",
    "Dhiira moo dhalaa?",
]

QUESTIONS_HAD = [
    "Akkam! Gargaaraa fayyaa keetii dha. Har'a mallattoo ijoo kee maali?",
    "Mallattoon kun yeroo meeqa? (fkn guyyaa 1, guyyaa 3)",
    "Mallattoo biraa qabdaa? (ykn 'lakki' barreessi)",
    "Umurii kee meeqa?",
    "Dhiira moo dhalaa?",
]

LANG_QUESTIONS = {
    'en': QUESTIONS_EN,
    'am': QUESTIONS_AM,
    'ti': QUESTIONS_TI,
    'om': QUESTIONS_OM,
}

# "no" equivalents per language
NO_WORDS = {'no', 'none', 'የለም', 'አይ', 'ኣይፋል', 'lakki', 'nope', 'maya', 'miti'}

# sex word maps per language
MALE_WORDS   = {'male', 'man', 'boy', 'ወንድ', 'm', 'ተባዕታይ', 'dhiira', '1', 'nin'}
FEMALE_WORDS = {'female', 'woman', 'girl', 'ሴት', 'f', 'ኣንስታይ', 'dhalaa', '2', 'naag'}


def get_questions(language: str) -> list:
    return LANG_QUESTIONS.get(language, QUESTIONS_EN)


def start_session(session_id: str, language: str = 'en') -> dict:
    _sessions[session_id] = {
        'language': language,
        'step': 0,
        'symptoms': [],
        'duration': '',
        'age': 25,
        'sex': 'unknown',
        'done': False,
    }
    questions = get_questions(language)
    return {'message': questions[0], 'step': 0, 'done': False}


def process_message(session_id: str, user_input: str) -> dict:
    if session_id not in _sessions:
        return {'error': 'Session not found. Please start a new session.'}

    state = _sessions[session_id]
    lang = state['language']
    step = state['step']
    questions = get_questions(lang)

    # Store answer for current step
    text = user_input.strip()

    if step == 0:
        # Primary symptom
        state['symptoms'].append(text)
    elif step == 1:
        # Duration
        state['duration'] = text
    elif step == 2:
        # Additional symptoms
        if text.lower() not in NO_WORDS:
            extras = [s.strip() for s in text.replace(',', ' ').split() if len(s.strip()) > 2]
            state['symptoms'].extend(extras)
    elif step == 3:
        # Age
        try:
            state['age'] = int(''.join(filter(str.isdigit, text))) or 25
        except ValueError:
            state['age'] = 25
    elif step == 4:
        # Sex
        lower = text.lower()
        if lower in MALE_WORDS:
            state['sex'] = 'male'
        elif lower in FEMALE_WORDS:
            state['sex'] = 'female'

    state['step'] += 1

    # If all questions answered, run assessment
    if state['step'] >= len(questions):
        state['done'] = True
        result = assess(
            symptoms=state['symptoms'],
            age=state['age'],
            sex=state['sex'],
            language=lang,
        )
        result['done'] = True
        result['collected_symptoms'] = state['symptoms']
        return result

    # Otherwise ask next question
    return {
        'message': questions[state['step']],
        'step': state['step'],
        'done': False,
    }


def get_session(session_id: str) -> dict | None:
    return _sessions.get(session_id)
