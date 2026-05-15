"""
Supply Chain / Stock Tracking Engine.
Allows HEWs to report medicine and supply shortages at health posts.
"""
from datetime import date

ESSENTIAL_SUPPLIES = [
    {'id': 'ors',          'name_en': 'ORS Sachets',              'name_am': 'ORS ፓኬቶች',          'category': 'medicines',   'unit': 'sachets'},
    {'id': 'amoxicillin',  'name_en': 'Amoxicillin 250mg',        'name_am': 'አሞክሲሲሊን 250mg',     'category': 'medicines',   'unit': 'tablets'},
    {'id': 'cotrimoxazole','name_en': 'Cotrimoxazole 480mg',       'name_am': 'ኮትሪሞክሳዞል 480mg',    'category': 'medicines',   'unit': 'tablets'},
    {'id': 'paracetamol',  'name_en': 'Paracetamol 500mg',        'name_am': 'ፓራሲታሞል 500mg',      'category': 'medicines',   'unit': 'tablets'},
    {'id': 'iron_folic',   'name_en': 'Iron/Folic Acid',          'name_am': 'ብረት/ፎሊክ አሲድ',       'category': 'medicines',   'unit': 'tablets'},
    {'id': 'vitamin_a',    'name_en': 'Vitamin A Capsules',       'name_am': 'ቫይታሚን ኤ ካፕሱሎች',    'category': 'medicines',   'unit': 'capsules'},
    {'id': 'zinc',         'name_en': 'Zinc Tablets',             'name_am': 'ዚንክ ጡባዊዎች',         'category': 'medicines',   'unit': 'tablets'},
    {'id': 'malaria_rdt',  'name_en': 'Malaria RDT Kits',         'name_am': 'ወባ RDT ኪቶች',         'category': 'diagnostics', 'unit': 'kits'},
    {'id': 'act',          'name_en': 'ACT (Artemether-Lumefantrine)', 'name_am': 'ACT ወባ መድሃኒት', 'category': 'medicines',   'unit': 'courses'},
    {'id': 'muac_tape',    'name_en': 'MUAC Tape',                'name_am': 'MUAC ቴፕ',             'category': 'equipment',   'unit': 'pieces'},
    {'id': 'gloves',       'name_en': 'Examination Gloves',       'name_am': 'የምርመራ ጓንቶች',        'category': 'supplies',    'unit': 'pairs'},
    {'id': 'condoms',      'name_en': 'Male Condoms',             'name_am': 'ወንድ ኮንዶሞች',          'category': 'fp',          'unit': 'pieces'},
    {'id': 'depo',         'name_en': 'Depo-Provera Injection',   'name_am': 'ዴፖ-ፕሮቬራ መርፌ',       'category': 'fp',          'unit': 'vials'},
    {'id': 'oxytocin',     'name_en': 'Oxytocin Injection',       'name_am': 'ኦክሲቶሲን መርፌ',         'category': 'maternal',    'unit': 'vials'},
    {'id': 'misoprostol',  'name_en': 'Misoprostol Tablets',      'name_am': 'ሚዞፕሮስቶል ጡባዊዎች',     'category': 'maternal',    'unit': 'tablets'},
]

STOCK_LEVELS = {
    'out_of_stock': {'en': 'Out of stock', 'am': 'ክምችት አልቋል', 'om': 'Kuusaa dhumee', 'ti': 'ዕቃ ወዲኡ'},
    'critical':     {'en': 'Critical (< 1 week supply)', 'am': 'ወሳኝ (< 1 ሳምንት)', 'om': 'Hamilee (< 1 torban)', 'ti': 'ወሳኒ (< 1 ሰሙን)'},
    'low':          {'en': 'Low (1–2 weeks supply)', 'am': 'ዝቅተኛ (1–2 ሳምንት)', 'om': 'Gadi (1–2 torban)', 'ti': 'ትሑት (1–2 ሰሙን)'},
    'adequate':     {'en': 'Adequate (> 2 weeks supply)', 'am': 'በቂ (> 2 ሳምንት)', 'om': 'Gahaa (> 2 torban)', 'ti': 'ኣኻሊ (> 2 ሰሙን)'},
}


def get_supply_list(language: str = 'en') -> list:
    """Return the list of essential supplies with localized names."""
    result = []
    for s in ESSENTIAL_SUPPLIES:
        name_key = f'name_{language}' if language in ('am', 'om', 'ti') else 'name_en'
        result.append({
            'id': s['id'],
            'name': s.get(name_key, s['name_en']),
            'category': s['category'],
            'unit': s['unit'],
        })
    return result


def classify_stock_level(quantity: int, weekly_consumption: int) -> str:
    """Classify stock level based on quantity and weekly consumption."""
    if quantity <= 0:
        return 'out_of_stock'
    if weekly_consumption <= 0:
        return 'adequate'
    weeks_remaining = quantity / weekly_consumption
    if weeks_remaining < 1:
        return 'critical'
    elif weeks_remaining < 2:
        return 'low'
    return 'adequate'


def build_shortage_report(reports: list, kebele: str, hew_name: str, language: str = 'en') -> dict:
    """
    Build a shortage report from a list of stock reports.
    Each report: { supply_id, quantity, weekly_consumption }
    """
    shortages = []
    for r in reports:
        level = classify_stock_level(r.get('quantity', 0), r.get('weekly_consumption', 1))
        if level in ('out_of_stock', 'critical', 'low'):
            supply = next((s for s in ESSENTIAL_SUPPLIES if s['id'] == r['supply_id']), None)
            if supply:
                name_key = f'name_{language}' if language in ('am', 'om', 'ti') else 'name_en'
                shortages.append({
                    'supply_id': r['supply_id'],
                    'name': supply.get(name_key, supply['name_en']),
                    'level': level,
                    'level_label': STOCK_LEVELS[level].get(language, STOCK_LEVELS[level]['en']),
                    'quantity': r.get('quantity', 0),
                    'unit': supply['unit'],
                    'category': supply['category'],
                })

    urgent = [s for s in shortages if s['level'] in ('out_of_stock', 'critical')]

    return {
        'kebele': kebele,
        'hew_name': hew_name,
        'report_date': str(date.today()),
        'total_shortages': len(shortages),
        'urgent_shortages': len(urgent),
        'shortages': shortages,
        'needs_resupply': len(urgent) > 0,
    }
