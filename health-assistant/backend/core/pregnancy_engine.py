"""
Pregnancy follow-up engine.
Calculates gestational age, EDD, ANC schedule, and flags danger signs.
Based on WHO ANC guidelines and Ethiopia FMOH protocols.
"""
from datetime import date, timedelta


# WHO/Ethiopia recommended ANC visit schedule (minimum 8 contacts)
ANC_SCHEDULE = [
    {'visit': 1, 'weeks': 12,  'label_en': '1st Contact (before 12 weeks)',   'label_am': '1ኛ ጉብኝት (ከ12 ሳምንት በፊት)',  'key_actions_en': ['Confirm pregnancy', 'Blood pressure', 'Weight', 'Blood tests (HIV, syphilis, blood group)', 'Iron-folic acid', 'TT vaccine', 'Counsel on danger signs']},
    {'visit': 2, 'weeks': 20,  'label_en': '2nd Contact (20 weeks)',           'label_am': '2ኛ ጉብኝት (20 ሳምንት)',         'key_actions_en': ['Blood pressure', 'Weight', 'Fundal height', 'Fetal heart rate', 'Iron-folic acid', 'Anaemia check']},
    {'visit': 3, 'weeks': 26,  'label_en': '3rd Contact (26 weeks)',           'label_am': '3ኛ ጉብኝት (26 ሳምንት)',         'key_actions_en': ['Blood pressure', 'Weight', 'Fundal height', 'Fetal position', 'Iron-folic acid', 'TT vaccine 2nd dose']},
    {'visit': 4, 'weeks': 30,  'label_en': '4th Contact (30 weeks)',           'label_am': '4ኛ ጉብኝት (30 ሳምንት)',         'key_actions_en': ['Blood pressure', 'Weight', 'Fundal height', 'Fetal heart rate', 'Birth plan discussion']},
    {'visit': 5, 'weeks': 34,  'label_en': '5th Contact (34 weeks)',           'label_am': '5ኛ ጉብኝት (34 ሳምንት)',         'key_actions_en': ['Blood pressure', 'Weight', 'Fetal presentation', 'Birth preparedness', 'Emergency transport plan']},
    {'visit': 6, 'weeks': 36,  'label_en': '6th Contact (36 weeks)',           'label_am': '6ኛ ጉብኝት (36 ሳምንት)',         'key_actions_en': ['Blood pressure', 'Weight', 'Fetal presentation', 'Confirm birth plan', 'Danger signs review']},
    {'visit': 7, 'weeks': 38,  'label_en': '7th Contact (38 weeks)',           'label_am': '7ኛ ጉብኝት (38 ሳምንት)',         'key_actions_en': ['Blood pressure', 'Weight', 'Fetal heart rate', 'Labour signs counselling']},
    {'visit': 8, 'weeks': 40,  'label_en': '8th Contact (40 weeks)',           'label_am': '8ኛ ጉብኝት (40 ሳምንት)',         'key_actions_en': ['Blood pressure', 'Fetal presentation', 'Discuss post-dates management', 'Confirm emergency contacts']},
]

DANGER_SIGNS = [
    {'id': 'heavy_bleeding',    'sign_en': 'Heavy vaginal bleeding',                'sign_am': 'ከፍተኛ የብልት ደም መፍሰስ',    'urgency': 'emergency'},
    {'id': 'severe_headache',   'sign_en': 'Severe headache not relieved by rest',  'sign_am': 'ከፍተኛ ራስ ምታት',           'urgency': 'emergency'},
    {'id': 'blurred_vision',    'sign_en': 'Blurred or loss of vision',             'sign_am': 'ዕይታ መደበዘዝ ወይም ማጣት',        'urgency': 'emergency'},
    {'id': 'convulsions',       'sign_en': 'Convulsions / fits',                    'sign_am': 'ኩታ (መንቀጥቀጥ)',              'urgency': 'emergency'},
    {'id': 'high_bp',           'sign_en': 'BP ≥ 160/110 mmHg',                    'sign_am': 'ከፍተኛ የደም ግፊት (160/110+)',  'urgency': 'emergency'},
    {'id': 'no_fetal_movement', 'sign_en': 'No fetal movement for 12+ hours',      'sign_am': 'ፅንሱ ለ12+ ሰዓት አለመንቀሳቀስ',  'urgency': 'emergency'},
    {'id': 'fever',             'sign_en': 'High fever (above 38°C)',               'sign_am': 'ከፍተኛ ትኩሳት',              'urgency': 'urgent'},
    {'id': 'severe_vomiting',   'sign_en': 'Severe vomiting — unable to keep fluids','sign_am': 'ከፍተኛ ማስታወክ',            'urgency': 'urgent'},
    {'id': 'swollen_face_hands','sign_en': 'Sudden swelling of face, hands, or feet','sign_am': 'ፊት፣ እጅ ወይም እግር ድንገተኛ እብጠት','urgency': 'urgent'},
    {'id': 'difficulty_breathing','sign_en': 'Difficulty breathing',               'sign_am': 'የመተንፈስ ችግር',              'urgency': 'urgent'},
    {'id': 'water_breaking',    'sign_en': 'Water breaking before 37 weeks (PROM)','sign_am': 'ከ37 ሳምንት በፊት ውሃ መፍሰስ',  'urgency': 'urgent'},
    {'id': 'painful_urination', 'sign_en': 'Painful or burning urination',         'sign_am': 'ሲሸኑ ህመም ወይም ቃጠሎ',        'urgency': 'visit_soon'},
    {'id': 'anaemia_symptoms',  'sign_en': 'Extreme fatigue, pale skin, breathlessness','sign_am': 'ከፍተኛ ድካም፣ ፈዛዛ ቆዳ፣ ትንፋሽ ማጠር', 'urgency': 'visit_soon'},
]


def calculate_edd(lmp: date) -> date:
    """Naegele's rule: EDD = LMP + 280 days (40 weeks)."""
    return lmp + timedelta(days=280)


def gestational_age_weeks(lmp: date) -> float:
    """Calculate gestational age in weeks from LMP."""
    days = (date.today() - lmp).days
    return round(days / 7, 1)


def get_trimester(weeks: float) -> str:
    if weeks < 14:
        return 'first'
    if weeks < 28:
        return 'second'
    return 'third'


def get_anc_schedule(lmp: date, completed_visits: int = 0) -> dict:
    """Return ANC schedule with due dates and completion status."""
    today = date.today()
    ga_weeks = gestational_age_weeks(lmp)
    edd = calculate_edd(lmp)
    schedule = []
    next_visit = None

    for i, v in enumerate(ANC_SCHEDULE):
        due_date = lmp + timedelta(weeks=v['weeks'])
        is_done = i < completed_visits
        is_overdue = not is_done and due_date < today
        days_until = (due_date - today).days

        entry = {
            'visit_number': v['visit'],
            'label_en': v['label_en'],
            'label_am': v['label_am'],
            'due_date': due_date.isoformat(),
            'status': 'done' if is_done else ('overdue' if is_overdue else 'upcoming'),
            'days_until': days_until if not is_done else None,
            'key_actions_en': v['key_actions_en'],
        }
        schedule.append(entry)
        if not is_done and next_visit is None:
            next_visit = entry

    weeks_remaining = max(0, round((edd - today).days / 7, 1))

    return {
        'gestational_age_weeks': ga_weeks,
        'trimester': get_trimester(ga_weeks),
        'edd': edd.isoformat(),
        'weeks_remaining': weeks_remaining,
        'completed_visits': completed_visits,
        'total_visits': len(ANC_SCHEDULE),
        'schedule': schedule,
        'next_visit': next_visit,
        'overdue_visits': sum(1 for s in schedule if s['status'] == 'overdue'),
    }


def check_bp_danger(systolic: int, diastolic: int, ga_weeks: float) -> dict | None:
    """Flag hypertensive disorders of pregnancy."""
    if systolic >= 160 or diastolic >= 110:
        return {'level': 'emergency', 'message_en': f'BP {systolic}/{diastolic} — SEVERE HYPERTENSION. Give magnesium sulfate and refer immediately.',
                'message_am': 'ከፍተኛ የደም ግፊት — ወዲያውኑ ሆስፒታል ይሂዱ። ማግኒዥየም ሰልፌት ያስፈልጋል።'}
    if (systolic >= 140 or diastolic >= 90) and ga_weeks >= 20:
        return {'level': 'urgent', 'message_en': f'BP {systolic}/{diastolic} — Pre-eclampsia suspected. Refer to health centre urgently.',
                'message_am': 'ቅድመ-ኤክላምፕሲያ ሊሆን ይችላል። ወደ ጤና ጣቢያ ይሂዱ።'}
    return None


def get_danger_signs_list(language: str = 'en') -> list:
    """Return all pregnancy danger signs."""
    return [{'id': d['id'],
             'sign': d.get(f'sign_{language}', d['sign_en']),
             'urgency': d['urgency']} for d in DANGER_SIGNS]
