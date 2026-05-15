"""
Emergency Alert Engine.
Sends SMS to all registered emergency contacts when urgency == 'emergency'.
"""
from core.sms_engine import send_sms
from core.geolocation import find_nearest_facilities


def send_emergency_alerts(user_id: str, condition_summary: str,
                           urgency_level: str, location_text: str,
                           language: str = 'en') -> dict:
    """
    Send emergency SMS to all registered contacts for a user.
    Returns summary of results.
    """
    from api.models import EmergencyContact, EmergencyAlertLog

    contacts = list(EmergencyContact.objects.filter(user_identifier=user_id))
    if not contacts:
        return {
            'status': 'no_contacts',
            'message': 'No emergency contacts registered.',
            'contacts_notified': [],
        }

    # Find nearest facility
    nearest_facility = ''
    try:
        facilities = find_nearest_facilities(0, 0)  # fallback — no GPS coords here
        if facilities:
            f = facilities[0]
            nearest_facility = f"{f['name']} — {f.get('phone', '907')}"
    except Exception:
        nearest_facility = 'Call 907 for emergency'

    # Build SMS message
    msg = _build_alert_sms(condition_summary, location_text, nearest_facility, language)

    # Send to all contacts
    notified = []
    for contact in contacts:
        try:
            result = send_sms(contact.phone, msg)
            notified.append({
                'phone': contact.phone,
                'name': contact.name,
                'status': result.get('status', 'sent'),
            })
        except Exception as e:
            notified.append({'phone': contact.phone, 'name': contact.name, 'status': 'failed'})

    # Log the alert
    try:
        EmergencyAlertLog.objects.create(
            user_identifier=user_id,
            condition_summary=condition_summary,
            urgency_level=urgency_level,
            contacts_notified=[c['phone'] for c in notified],
            location_text=location_text,
            nearest_facility=nearest_facility,
            cancelled=False,
        )
    except Exception:
        pass

    return {
        'status': 'sent',
        'contacts_notified': notified,
        'nearest_facility': nearest_facility,
        'message': msg[:160],
    }


def _build_alert_sms(condition: str, location: str, facility: str, language: str) -> str:
    templates = {
        'en':  f"HEALTH EMERGENCY: {condition}. Location: {location or 'unknown'}. Nearest facility: {facility}. Please help immediately.",
        'am':  f"የጤና አደጋ: {condition}. አካባቢ: {location or 'ያልታወቀ'}. ቅርብ ጤና ጣቢያ: {facility}. እባክዎ ወዲያውኑ ይርዱ።",
        'om':  f"Balaa fayyaa: {condition}. Bakka: {location or 'hin beekamne'}. Buufata dhiyoo: {facility}. Maaloo gargaari.",
        'ti':  f"ህጹጽ ጥዕና: {condition}. ቦታ: {location or 'ዘይፍለጥ'}. ቀረባ ጥዕና ጣቢያ: {facility}. በጃኻ ሓግዞ።",
    }
    return templates.get(language, templates['en'])[:160]
