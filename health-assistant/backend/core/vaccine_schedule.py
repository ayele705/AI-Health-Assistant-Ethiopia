"""
Ethiopia EPI (Expanded Programme on Immunization) vaccine schedule engine.
Based on Ethiopia Federal Ministry of Health EPI schedule 2023.
"""
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


# Ethiopia EPI schedule — each entry: id, name, due_at (weeks/months from birth), doses
ETHIOPIA_EPI_SCHEDULE = [
    {'id': 'bcg',           'name': 'BCG',                    'due_weeks': 0,   'due_months': 0,    'doses': 1, 'description_en': 'Bacillus Calmette-Guérin — protects against tuberculosis meningitis and miliary TB in children.'},
    {'id': 'opv_0',         'name': 'OPV 0 (Birth Dose)',     'due_weeks': 0,   'due_months': 0,    'doses': 1, 'description_en': 'Oral Polio Vaccine birth dose — protects against poliomyelitis.'},
    {'id': 'hepb_0',        'name': 'HepB 0 (Birth Dose)',    'due_weeks': 0,   'due_months': 0,    'doses': 1, 'description_en': 'Hepatitis B birth dose — must be given within 24 hours of birth to prevent mother-to-child transmission.'},
    {'id': 'dpt_hepb_hib_1','name': 'DPT-HepB-Hib 1',        'due_weeks': 6,   'due_months': 1.5,  'doses': 3, 'description_en': 'Diphtheria, Pertussis, Tetanus, Hepatitis B, Haemophilus influenzae type b — 1st dose.'},
    {'id': 'opv_1',         'name': 'OPV 1',                  'due_weeks': 6,   'due_months': 1.5,  'doses': 3, 'description_en': 'Oral Polio Vaccine — 1st dose.'},
    {'id': 'pcv_1',         'name': 'PCV 1',                  'due_weeks': 6,   'due_months': 1.5,  'doses': 3, 'description_en': 'Pneumococcal Conjugate Vaccine — 1st dose. Protects against pneumonia and meningitis.'},
    {'id': 'rota_1',        'name': 'Rotavirus 1',            'due_weeks': 6,   'due_months': 1.5,  'doses': 2, 'description_en': 'Rotavirus vaccine — 1st dose. Protects against severe diarrhea.'},
    {'id': 'dpt_hepb_hib_2','name': 'DPT-HepB-Hib 2',        'due_weeks': 10,  'due_months': 2.5,  'doses': 3, 'description_en': 'DPT-HepB-Hib — 2nd dose.'},
    {'id': 'opv_2',         'name': 'OPV 2',                  'due_weeks': 10,  'due_months': 2.5,  'doses': 3, 'description_en': 'Oral Polio Vaccine — 2nd dose.'},
    {'id': 'pcv_2',         'name': 'PCV 2',                  'due_weeks': 10,  'due_months': 2.5,  'doses': 3, 'description_en': 'Pneumococcal Conjugate Vaccine — 2nd dose.'},
    {'id': 'rota_2',        'name': 'Rotavirus 2',            'due_weeks': 10,  'due_months': 2.5,  'doses': 2, 'description_en': 'Rotavirus vaccine — 2nd dose.'},
    {'id': 'dpt_hepb_hib_3','name': 'DPT-HepB-Hib 3',        'due_weeks': 14,  'due_months': 3.5,  'doses': 3, 'description_en': 'DPT-HepB-Hib — 3rd dose.'},
    {'id': 'opv_3',         'name': 'OPV 3',                  'due_weeks': 14,  'due_months': 3.5,  'doses': 3, 'description_en': 'Oral Polio Vaccine — 3rd dose.'},
    {'id': 'pcv_3',         'name': 'PCV 3',                  'due_weeks': 14,  'due_months': 3.5,  'doses': 3, 'description_en': 'Pneumococcal Conjugate Vaccine — 3rd dose.'},
    {'id': 'ipv',           'name': 'IPV (Inactivated Polio)','due_weeks': 14,  'due_months': 3.5,  'doses': 1, 'description_en': 'Inactivated Polio Vaccine — given with 3rd DPT dose.'},
    {'id': 'measles_1',     'name': 'Measles-Rubella 1',      'due_weeks': 36,  'due_months': 9,    'doses': 2, 'description_en': 'Measles-Rubella vaccine — 1st dose at 9 months.'},
    {'id': 'vita_1',        'name': 'Vitamin A (1st)',         'due_weeks': 36,  'due_months': 9,    'doses': 1, 'description_en': 'Vitamin A supplementation — 100,000 IU at 9 months.'},
    {'id': 'measles_2',     'name': 'Measles-Rubella 2',      'due_weeks': 72,  'due_months': 18,   'doses': 2, 'description_en': 'Measles-Rubella vaccine — 2nd dose at 18 months.'},
    {'id': 'vita_2',        'name': 'Vitamin A (2nd)',         'due_weeks': 72,  'due_months': 18,   'doses': 1, 'description_en': 'Vitamin A supplementation — 200,000 IU at 18 months.'},
    {'id': 'dpt_booster',   'name': 'DPT Booster',            'due_weeks': 72,  'due_months': 18,   'doses': 1, 'description_en': 'DPT booster dose at 18 months.'},
]


def get_due_date(dob: date, due_months: float) -> date:
    """Calculate vaccine due date from date of birth and months offset."""
    whole_months = int(due_months)
    extra_days = int((due_months - whole_months) * 30)
    d = dob + relativedelta(months=whole_months) + timedelta(days=extra_days)
    return d


def get_vaccine_schedule(dob: date, given_vaccine_ids: list = None) -> dict:
    """
    Return full vaccine schedule for a child with due dates,
    status (given/due/upcoming/overdue), and next due vaccines.
    """
    given_ids = set(given_vaccine_ids or [])
    today = date.today()
    schedule = []
    overdue = []
    due_soon = []   # due within next 4 weeks
    upcoming = []

    for v in ETHIOPIA_EPI_SCHEDULE:
        due_date = get_due_date(dob, v['due_months'])
        is_given = v['id'] in given_ids
        days_until = (due_date - today).days

        if is_given:
            status = 'given'
        elif due_date < today:
            status = 'overdue'
            overdue.append(v['name'])
        elif days_until <= 28:
            status = 'due_soon'
            due_soon.append({'name': v['name'], 'due_date': due_date.isoformat(), 'days_until': days_until})
        else:
            status = 'upcoming'
            upcoming.append({'name': v['name'], 'due_date': due_date.isoformat()})

        schedule.append({
            'id': v['id'],
            'name': v['name'],
            'due_date': due_date.isoformat(),
            'status': status,
            'description_en': v['description_en'],
            'days_until': days_until if not is_given else None,
        })

    completion_pct = round(len(given_ids) / len(ETHIOPIA_EPI_SCHEDULE) * 100)

    return {
        'schedule': schedule,
        'overdue': overdue,
        'due_soon': due_soon,
        'upcoming_count': len(upcoming),
        'completion_percent': completion_pct,
        'total_vaccines': len(ETHIOPIA_EPI_SCHEDULE),
        'given_count': len(given_ids),
        'alert': len(overdue) > 0,
        'alert_message_en': f'{len(overdue)} vaccine(s) overdue: {", ".join(overdue)}' if overdue else '',
        'alert_message_am': f'{len(overdue)} ክትባቶች ዘግይተዋል።' if overdue else '',
    }
