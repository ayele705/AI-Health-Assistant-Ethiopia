"""
Medication lookup engine.
Searches the medications section of the knowledge base.
"""
from .knowledge_base import load_kb


def get_all_medications() -> list:
    return load_kb().get('medications', [])


def search_medications(query: str, language: str = 'en') -> list:
    query_lower = query.lower().strip()
    results = []
    for med in get_all_medications():
        name_en = med.get('name_en', '').lower()
        name_am = med.get('name_am', '').lower()
        generic = med.get('generic_name', '').lower()
        aliases = [a.lower() for a in med.get('aliases', [])]
        condition_ids = [c.lower() for c in med.get('used_for_conditions', [])]
        if (query_lower in name_en or query_lower in name_am
                or query_lower in generic
                or any(query_lower in a for a in aliases)
                or any(query_lower in c for c in condition_ids)):
            results.append(_localize(med, language))
    return results


def get_medication_by_id(med_id: str, language: str = 'en') -> dict | None:
    for med in get_all_medications():
        if med.get('id') == med_id:
            return _localize(med, language)
    return None


def _localize(med: dict, language: str) -> dict:
    def f(field):
        return (med.get(f'{field}_{language}')
                or med.get(f'{field}_am')
                or med.get(f'{field}_en', ''))
    return {
        'id': med.get('id'),
        'name': f('name'),
        'generic_name': med.get('generic_name', ''),
        'category': med.get('category', ''),
        'description': f('description'),
        'dosage_adult': f('dosage_adult'),
        'dosage_child': f('dosage_child'),
        'side_effects': f('side_effects'),
        'contraindications': f('contraindications'),
        'warnings': f('warnings'),
        'used_for_conditions': med.get('used_for_conditions', []),
        'available_in_ethiopia': med.get('available_in_ethiopia', True),
        'who_essential': med.get('who_essential', False),
        'prescription_required': med.get('prescription_required', True),
        'aliases': med.get('aliases', []),
    }
