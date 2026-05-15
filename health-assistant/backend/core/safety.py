"""
Safety & Ethics Module.
- Clinical safety threshold enforcement
- Data minimization helpers
- Disclaimer injection
- Age-range bucketing (no exact age stored)
"""

CONFIDENCE_THRESHOLD = 0.15  # below this → safe-uncertainty response

DISCLAIMERS = {
    'en': '[NOTE] This is not a clinical diagnosis. Always consult a qualified health worker for medical decisions.',
    'am': '[NOTE] ይህ ክሊኒካዊ ምርመራ አይደለም። ሁልጊዜ ለህክምና ውሳኔ ብቁ የጤና ሠራተኛ ያማክሩ።',
    'om': '[NOTE] Kun dhukkuba adda baasuu miti. Ogeessa fayyaa mariisi.',
    'ti': '[NOTE] እዚ ክሊኒካዊ ምርመራ ኣይኮነን። ሓኪም ወይ ሰራሕተኛ ጥዕና ተወከስ።',
}


def get_disclaimer(language: str) -> str:
    return DISCLAIMERS.get(language, DISCLAIMERS['en'])


def age_to_range(age: int) -> str:
    """Convert exact age to anonymized range for storage."""
    if age < 5:
        return 'under_5'
    if age < 18:
        return '5_17'
    if age < 60:
        return '18_59'
    return '60_plus'


def is_minor(age: int) -> bool:
    return age < 18


def apply_safety_threshold(result: dict, language: str) -> dict:
    """
    If top condition score is below threshold, replace with safe-uncertainty response.
    Injects disclaimer into all results.
    """
    from core.localization import get_safe_message

    conditions = result.get('conditions', [])
    top_score = conditions[0]['score'] if conditions else 0.0

    if top_score < CONFIDENCE_THRESHOLD and not result.get('emergency_alerts'):
        result['conditions'] = []
        result['message'] = get_safe_message(language)
        result['urgency'] = 'self_care'
        result['low_confidence'] = True

    result['disclaimer'] = get_disclaimer(language)
    return result


def minimize_consultation_data(data: dict, is_minor_user: bool = False) -> dict:
    """
    Apply data minimization before DB storage.
    Converts exact age to range; removes PII for minors.
    """
    safe = {
        'symptoms': data.get('symptoms', []),
        'age_range': age_to_range(data.get('age', 25)),
        'sex': data.get('sex', 'unknown'),
        'language': data.get('language', 'en'),
        'channel': data.get('channel', 'app'),
        'urgency_level': data.get('urgency_level', ''),
        'assessment_result': data.get('assessment_result'),
    }
    if is_minor_user:
        # Extra minimization for minors — no demographic beyond range+sex
        safe.pop('sex', None)
    return safe
