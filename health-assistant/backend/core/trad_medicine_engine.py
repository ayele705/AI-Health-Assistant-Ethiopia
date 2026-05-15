"""
Traditional Medicine Knowledge Base engine.
Loads traditional_medicine_kb.json and provides fuzzy search + interaction checking.
"""
import json
import os

_KB = None

def _load_kb():
    global _KB
    if _KB is not None:
        return _KB
    kb_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'traditional_medicine_kb.json')
    try:
        with open(kb_path, encoding='utf-8') as f:
            _KB = json.load(f).get('remedies', [])
    except FileNotFoundError:
        _KB = []
    return _KB


def search_remedies(query: str, language: str = 'en') -> list:
    """Fuzzy search remedies by local name across all languages."""
    kb    = _load_kb()
    q     = query.lower().strip()
    found = []
    for r in kb:
        names = r.get('local_names', {})
        if any(q in str(v).lower() for v in names.values()):
            found.append(_format_remedy(r, language))
    return found


def get_remedy_by_id(remedy_id: str, language: str = 'en'):
    """Get a single remedy by ID."""
    kb = _load_kb()
    for r in kb:
        if r.get('id') == remedy_id:
            return _format_remedy(r, language)
    return None


def check_interactions(remedy_names: list, medication_ids: list, language: str = 'en') -> dict:
    """Check for interactions between traditional remedies and medications."""
    kb       = _load_kb()
    warnings = []

    for name in remedy_names:
        q = name.lower().strip()
        for r in kb:
            names = r.get('local_names', {})
            if any(q in str(v).lower() for v in names.values()):
                # Check interactions
                for med_id in medication_ids:
                    if med_id.lower() in [i.lower() for i in r.get('known_interactions', [])]:
                        warnings.append({
                            'remedy': names.get(language) or names.get('en', name),
                            'medication': med_id,
                            'warning': _interaction_warning(r, language),
                            'serious': r.get('serious_adverse_effect', False),
                        })
                # Serious adverse effect warning
                if r.get('serious_adverse_effect'):
                    warnings.append({
                        'remedy': names.get(language) or names.get('en', name),
                        'medication': None,
                        'warning': _serious_warning(r, language),
                        'serious': True,
                    })

    return {
        'has_warnings': len(warnings) > 0,
        'warnings': warnings,
        'culturally_respectful_note': _respectful_note(language),
    }


def _format_remedy(r: dict, language: str) -> dict:
    lang = language if language in ('am', 'om', 'ti') else 'en'
    return {
        'id': r.get('id'),
        'local_names': r.get('local_names', {}),
        'name': r.get('local_names', {}).get(language) or r.get('local_names', {}).get('en', ''),
        'common_use': r.get(f'common_use_{lang}') or r.get('common_use_en', ''),
        'active_compounds': r.get('active_compounds', ''),
        'safety_notes': r.get(f'safety_notes_{lang}') or r.get('safety_notes_en', ''),
        'known_interactions': r.get('known_interactions', []),
        'serious_adverse_effect': r.get('serious_adverse_effect', False),
        'evidence_level': r.get('evidence_level', 'unverified'),
        'culturally_respectful_note': _respectful_note(language),
    }


def _interaction_warning(r: dict, language: str) -> str:
    msgs = {
        'en': "This traditional remedy may interact with your medication. Please consult a health worker before combining them.",
        'am': "ይህ ባህላዊ መድሃኒት ከዘመናዊ መድሃኒትዎ ጋር ሊጋጭ ይችላል። ከጤና ሠራተኛ ጋር ያማክሩ።",
        'om': "Qoricha aadaa kun qoricha kee waliin rakkoo uumuu danda'a. Ogeessa fayyaa mariisi.",
        'ti': "Qoricha aadaa kun qoricha kee waliin rakkoo uumuu danda'a. Ogeessa fayyaa mariisi.",
    }
    return msgs.get(language, msgs['en'])


def _serious_warning(r: dict, language: str) -> str:
    msgs = {
        'en': '[WARNING] This remedy has known serious adverse effects. Please consult a health worker before use.',
        'am': '[WARNING] ይህ ባህላዊ መድሃኒት ከባድ ጉዳት ሊያደርስ ይችላል። ከጤና ሠራተኛ ጋር ያማክሩ።',
        'om': '[WARNING] Qoricha kana fayyadamuun dura ogeessa fayyaa mariisi.',
        'ti': '[WARNING] Qoricha kana fayyadamuun dura ogeessa fayyaa mariisi.',
    }
    return msgs.get(language, msgs['en'])


def _respectful_note(language: str) -> str:
    msgs = {
        'en': "Traditional practices are valued in our communities. We share this information to help you stay safe alongside your cultural practices.",
        'am': "ባህላዊ ልምዶቻችን ዋጋ አላቸው። ይህ መረጃ ደህንነትዎን ለማረጋገጥ ነው።",
        'om': "Aadaan keenya gatii qaba. Odeeffannoon kun nageenya kee eeguuf.",
        'ti': "Aadaan keenya gatii qaba. Odeeffannoon kun nageenya kee eeguuf.",
    }
    return msgs.get(language, msgs['en'])
