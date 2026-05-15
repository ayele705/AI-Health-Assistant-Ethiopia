"""
Symptom assessment engine.
Supports English, Amharic, Tigrinya, Oromo, Sidamo input with translation maps.
"""
from .knowledge_base import get_all_conditions

AMHARIC_SYMPTOM_MAP = {
    'ትኩሳት': 'fever', 'ከፍተኛ ትኩሳት': 'high fever', 'ራስ ምታት': 'headache',
    'ራስምታት': 'headache', 'ሳል': 'cough', 'ቀጣይ ሳል': 'persistent cough',
    'ማቅለሽለሽ': 'nausea', 'ማስታወክ': 'vomiting', 'ተቅማጥ': 'diarrhea',
    'ከፍተኛ ተቅማጥ': 'severe diarrhea', 'የሆድ ህመም': 'stomach pain',
    'የሆድ ቁርጠት': 'cramps', 'ድካም': 'fatigue', 'ድካምና': 'weakness',
    'ብርድ ብርድ': 'chills', 'ላብ': 'sweating', 'የሌሊት ላብ': 'night sweats',
    'የጡት ህመም': 'chest pain', 'የደረት ህመም': 'chest pain',
    'አስቸጋሪ መተንፈስ': 'difficulty breathing', 'ፈጣን መተንፈስ': 'rapid breathing',
    'የክብደት መቀነስ': 'weight loss', 'ደም በምራቅ': 'blood in sputum',
    'ቢጫ ቆዳ': 'jaundice', 'ቢጫ ዓይን': 'jaundice', 'ሽፍታ': 'rash',
    'ማሳከክ': 'itching', 'ማበጥ': 'swelling', 'የጡንቻ ህመም': 'muscle pain',
    'ቀይ ዓይን': 'red eyes', 'የዓይን ፈሳሽ': 'eye discharge', 'ድርቀት': 'dehydration',
    'ሽብርታ': 'convulsions', 'ደም በሰገራ': 'blood in stool',
    'ከፍተኛ ደም': 'severe bleeding', 'ደም መፍሰስ': 'severe bleeding',
    'ተደጋጋሚ ሽንት': 'frequent urination', 'ከፍተኛ ጥም': 'excessive thirst',
    'የዓይን ብዥታ': 'blurred vision', 'የጉሮሮ ህመም': 'sore throat',
    'አፍንጫ ፈሳሽ': 'runny nose', 'ማስነጠስ': 'sneezing',
    'የሰውነት ህመም': 'body aches', 'የቆዳ ቁስለት': 'skin sores',
    'ፈንጠዝያ': 'blisters', 'ቀይ ቆዳ': 'redness',
    'ምንም የፅንስ እንቅስቃሴ': 'no fetal movement', 'የወሊድ ህመም': 'labor pain',
    'ከፍተኛ ራስ ምታት': 'severe headache during pregnancy',
    'የሊምፍ ኖድ እብጠት': 'swollen lymph nodes',
}

TIGRINYA_SYMPTOM_MAP = {
    'ረስኒ': 'fever', 'ልዑል ረስኒ': 'high fever', 'ቃንዛ ርእሲ': 'headache',
    'ሳዕዓል': 'cough', 'ቀጻሊ ሳዕዓል': 'persistent cough',
    'ምድንጋጽ': 'nausea', 'ምትፋእ': 'vomiting', 'ተምሲ': 'diarrhea',
    'ከቢድ ተምሲ': 'severe diarrhea', 'ቃንዛ ከብዲ': 'stomach pain',
    'ድኻም': 'fatigue', 'ድኽነት': 'weakness', 'ርዕደት': 'chills',
    'ምላዕ': 'sweating', 'ለይቲ ምላዕ': 'night sweats',
    'ቃንዛ ደረት': 'chest pain', 'ጸገም ምስትንፋስ': 'difficulty breathing',
    'ቅልጡፍ ምስትንፋስ': 'rapid breathing', 'ምጉዳል ክብደት': 'weight loss',
    'ደም ኣብ ምራቕ': 'blood in sputum', 'ቢጫ ቆርበት': 'jaundice',
    'ቢጫ ዓይኒ': 'jaundice', 'ሕበጥ': 'rash', 'ሕርቃን': 'itching',
    'ምሕባጥ': 'swelling', 'ቃንዛ ጭዋዳ': 'muscle pain',
    'ቀይሕ ዓይኒ': 'red eyes', 'ፈሳሲ ዓይኒ': 'eye discharge',
    'ምድረቕ': 'dehydration', 'ምንቅጥቃጥ': 'convulsions',
    'ደም ኣብ ሽንቲ': 'blood in stool', 'ከቢድ ደም': 'severe bleeding',
    'ተደጋጋሚ ሽንቲ': 'frequent urination', 'ልዑል ጽምኢ': 'excessive thirst',
    'ዝሓሸ ምርኣይ': 'blurred vision', 'ቃንዛ ጎሮሮ': 'sore throat',
    'ፈሳሲ ኣፍንጫ': 'runny nose', 'ምስዓስ': 'sneezing',
    'ቃንዛ ኣካላት': 'body aches', 'ቁስሊ ቆርበት': 'skin sores',
}

OROMO_SYMPTOM_MAP = {
    "ho'a": 'fever', "ho'a ol'aanaa": 'high fever', 'dhukkuba mataa': 'headache',
    'qufaa': 'cough', 'qufaa itti fufe': 'persistent cough',
    'dhukkubbii garaa': 'nausea', 'hanqaaquu': 'vomiting', 'garaa kaasaa': 'diarrhea',
    'dhukkuba garaa': 'stomach pain', 'dadhabii': 'fatigue', 'laafina': 'weakness',
    'qorraa': 'chills', 'dafqa': 'sweating', 'dafqa halkan': 'night sweats',
    'dhukkuba laphee': 'chest pain', 'rakkoo hafuura': 'difficulty breathing',
    'hafuura ariifataa': 'rapid breathing', "hir'ina ulfaatina": 'weight loss',
    'dhiiga afaan': 'blood in sputum', 'gogaa dhadhaa': 'jaundice',
    'qoree': 'rash', "hoo'ina": 'itching', 'dhiita': 'swelling',
    'dhukkuba mucha': 'muscle pain', 'ija diimaa': 'red eyes',
    'gogaa': 'dehydration', 'raafama': 'convulsions',
    'dhiiga fincaan': 'blood in stool', 'dhiiga cimaa': 'severe bleeding',
    "fincaan baay'ee": 'frequent urination', 'dheebuu cimaa': 'excessive thirst',
    'arguu dadhabuu': 'blurred vision', 'dhukkuba qoonqoo': 'sore throat',
    'finyaan': 'runny nose', 'dhukkuba gogaa': 'skin sores',
}

ALL_MAPS = [AMHARIC_SYMPTOM_MAP, TIGRINYA_SYMPTOM_MAP, OROMO_SYMPTOM_MAP]

SOMALI_SYMPTOM_MAP = {
    'qandho': 'fever', 'qandho xoog leh': 'high fever', 'madax xanuun': 'headache',
    'qufac': 'cough', 'qufac joogto ah': 'persistent cough',
    'calool xanuun': 'nausea', 'matag': 'vomiting', 'gudaha socda': 'diarrhea',
    'xanuun calool': 'stomach pain', 'daciifnimo': 'fatigue', 'jilicsan': 'weakness',
    'qabow': 'chills', 'dhadhanka': 'sweating', 'xanuun laab': 'chest pain',
    'neefsiga dhibaato': 'difficulty breathing', 'neefsiga degdeg': 'rapid breathing',
    'miisaanka hoos': 'weight loss', 'jaundice': 'jaundice', 'hargab': 'rash',
    'xakamaynta': 'itching', 'bararug': 'swelling', 'muruq xanuun': 'muscle pain',
    'indhaha cas': 'red eyes', 'biyo indhaha': 'eye discharge', 'engegid': 'dehydration',
    'qanqan': 'convulsions', 'dhiig saxaraha': 'blood in stool',
    'dhiig badan': 'severe bleeding', 'kaadi badan': 'frequent urination',
    'harraad badan': 'excessive thirst', 'aragga dhib': 'blurred vision',
    'cunaha xanuun': 'sore throat', 'san socda': 'runny nose',
    'jirka xanuun': 'body aches', 'maqaarka xanuun': 'skin sores',
}

AFAR_SYMPTOM_MAP = {
    'qandho': 'fever', 'madax xanuun': 'headache', 'qufac': 'cough',
    'calool xanuun': 'stomach pain', 'matag': 'vomiting', 'gudaha socda': 'diarrhea',
    'daciifnimo': 'fatigue', 'qabow': 'chills', 'xanuun laab': 'chest pain',
    'neefsiga dhibaato': 'difficulty breathing', 'bararug': 'swelling',
    'indhaha cas': 'red eyes', 'engegid': 'dehydration', 'qanqan': 'convulsions',
    'dhiig badan': 'severe bleeding', 'harraad badan': 'excessive thirst',
}

WOLAYTTA_SYMPTOM_MAP = {
    "ho'a": 'fever', "ho'a ol'aanaa": 'high fever', 'dhukkuba mataa': 'headache',
    'qufaa': 'cough', 'hanqaaquu': 'vomiting', 'garaa kaasaa': 'diarrhea',
    'dhukkuba garaa': 'stomach pain', 'dadhabii': 'fatigue', 'qorraa': 'chills',
    'dhukkuba laphee': 'chest pain', 'rakkoo hafuura': 'difficulty breathing',
    'dhiita': 'swelling', 'ija diimaa': 'red eyes', 'gogaa': 'dehydration',
    'raafama': 'convulsions', 'dhiiga cimaa': 'severe bleeding',
    'dheebuu cimaa': 'excessive thirst', 'dhukkuba gogaa': 'skin sores',
}

HADIYYA_SYMPTOM_MAP = {
    "ho'a": 'fever', 'dhukkuba mataa': 'headache', 'qufaa': 'cough',
    'hanqaaquu': 'vomiting', 'garaa kaasaa': 'diarrhea',
    'dhukkuba garaa': 'stomach pain', 'dadhabii': 'fatigue',
    'dhukkuba laphee': 'chest pain', 'rakkoo hafuura': 'difficulty breathing',
    'dhiita': 'swelling', 'gogaa': 'dehydration', 'raafama': 'convulsions',
    'dhiiga cimaa': 'severe bleeding',
}

ALL_MAPS = [
    AMHARIC_SYMPTOM_MAP, TIGRINYA_SYMPTOM_MAP, OROMO_SYMPTOM_MAP,
    SOMALI_SYMPTOM_MAP, AFAR_SYMPTOM_MAP, WOLAYTTA_SYMPTOM_MAP, HADIYYA_SYMPTOM_MAP,
]


def translate_symptoms(symptoms: list) -> list:
    translated = []
    for s in symptoms:
        s_strip = s.strip()
        s_lower = s_strip.lower()
        matched = False
        for m in ALL_MAPS:
            if s_strip in m:
                translated.append(m[s_strip])
                matched = True
                break
            if s_lower in m:
                translated.append(m[s_lower])
                matched = True
                break
        if not matched:
            translated.append(s_lower)
    return translated


def get_age_group(age: int) -> str:
    if age < 5:
        return 'children_under_5'
    if age >= 60:
        return 'elderly'
    return 'adult'


def score_condition(condition: dict, symptoms_en: list, age: int, sex: str) -> float:
    condition_symptoms = [s.lower() for s in condition.get('symptoms', [])]
    if not condition_symptoms:
        return 0.0
    matches = sum(1 for s in symptoms_en if s in condition_symptoms)
    if matches == 0:
        return 0.0
    overlap = matches / len(condition_symptoms)
    score = overlap * condition.get('prevalence_weight', 1.0)
    risk_factors = condition.get('risk_factors', {})
    age_group = get_age_group(age)
    if age_group in risk_factors:
        score *= risk_factors[age_group]
    if sex == 'female':
        if 'female' in risk_factors:
            score *= risk_factors['female']
        if 'pregnant' in risk_factors and condition.get('category') == 'maternal':
            score *= risk_factors['pregnant']
    elif sex == 'male':
        if condition.get('category') == 'maternal':
            return 0.0
    return score


def check_emergency_signs(symptoms_en: list, conditions: list, language: str) -> list:
    alerts = []
    for condition in conditions:
        emergency_signs = [s.lower() for s in condition.get('emergency_signs_en', [])]
        for s in symptoms_en:
            if any(s in sign or sign in s for sign in emergency_signs):
                # Pick best available language for signs, fallback chain: lang -> am -> en
                lang_key = f'emergency_signs_{language}'
                am_key   = 'emergency_signs_am'
                en_key   = 'emergency_signs_en'
                signs = (condition.get(lang_key)
                         or condition.get(am_key)
                         or condition.get(en_key, []))
                # Pick best available language for condition name
                name = (_get_localized(condition, 'name', language)
                        or condition.get('name_en', ''))
                alerts.append({
                    'condition': name,
                    'signs': signs,
                })
                break
    return alerts


def _get_localized(condition: dict, field: str, language: str) -> str:
    """Get localized field with fallback to am then en."""
    val = condition.get(f'{field}_{language}')
    if val:
        return val
    val = condition.get(f'{field}_am')
    if val:
        return val
    return condition.get(f'{field}_en', '')


def assess(symptoms: list, age: int = 25, sex: str = 'unknown', language: str = 'en') -> dict:
    symptoms_en = translate_symptoms(symptoms)
    conditions = get_all_conditions()
    emergency_alerts = check_emergency_signs(symptoms_en, conditions, language)

    scored = []
    for condition in conditions:
        score = score_condition(condition, symptoms_en, age, sex)
        if score > 0:
            scored.append((score, condition))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:3]

    no_match_msgs = {
        'en': 'No matching conditions found. If symptoms persist, please visit a health center.',
        'am': 'ምልክቶቹ ከምንም ሁኔታ ጋር አልተዛመዱም። ምልክቶቹ ከቀጠሉ ወደ ጤና ጣቢያ ይሂዱ።',
        'ti': 'ምልክታት ምስ ዝኾነ ሕማም ኣይተዛመደን። ምልክታት እንተቐጺሉ ናብ ጥዕና ጣቢያ ኪድ።',
        'om': "Mallattoon hin argamne. Mallattoon itti fufe yoo ta'e buufata fayyaa deemi.",
    }

    if not top:
        return {
            'message': no_match_msgs.get(language, no_match_msgs['en']),
            'conditions': [],
            'urgency': 'self_care',
            'emergency_alerts': emergency_alerts,
        }

    top_condition = top[0][1]
    results = []
    for score, cond in top:
        results.append({
            'id': cond['id'],
            'name': _get_localized(cond, 'name', language),
            'description': _get_localized(cond, 'description', language),
            'self_care': _get_localized(cond, 'self_care', language),
            'urgency': cond.get('urgency'),
            'score': round(score, 2),
        })

    top_name = _get_localized(top_condition, 'name', language)
    msg_templates = {
        'en': f'Your symptoms may be related to {top_name}.',
        'am': f'ምልክቶቹ ከ{top_name} ጋር ሊዛመዱ ይችላሉ።',
        'ti': f'ምልክታትካ ምስ {top_name} ክዛመድ ይኽእል።',
        'om': f"Mallattooleen kee {top_name} waliin walqabatuu danda'a.",
    }

    return {
        'message': msg_templates.get(language, msg_templates['en']),
        'conditions': results,
        'urgency': top_condition.get('urgency', 'self_care'),
        'emergency_alerts': emergency_alerts,
    }
