"""
SMS engine using Africa's Talking API.
Handles outbound SMS (reminders, alerts) and inbound SMS chat parsing.
Falls back to simulation mode when SMS_ENABLED=False or no API key.
"""
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

_sms_service = None


def _get_service():
    global _sms_service
    if _sms_service is not None:
        return _sms_service
    if not settings.SMS_ENABLED or not settings.AT_API_KEY:
        return None
    try:
        import africastalking
        africastalking.initialize(settings.AT_USERNAME, settings.AT_API_KEY)
        _sms_service = africastalking.SMS
        return _sms_service
    except Exception as e:
        logger.warning(f"Africa's Talking init failed: {e}")
        return None


def send_sms(phone: str, message: str, sender_id: str = None) -> dict:
    """
    Send an SMS. Returns dict with status and message_id.
    Falls back to simulation if SMS_ENABLED=False.
    """
    phone = _normalise_phone(phone)
    if not phone:
        return {'status': 'error', 'error': 'Invalid phone number'}

    svc = _get_service()
    if svc is None:
        # Simulation mode — log and return success
        logger.info(f"[SMS SIMULATION] To: {phone} | Msg: {message[:80]}")
        return {'status': 'simulated', 'phone': phone, 'message': message}

    try:
        sender = sender_id or settings.AT_SENDER_ID or None
        kwargs = {'message': message, 'recipients': [phone]}
        if sender:
            kwargs['sender_id'] = sender
        resp = svc.send(**kwargs)
        recipients = resp.get('SMSMessageData', {}).get('Recipients', [])
        if recipients:
            r = recipients[0]
            return {'status': r.get('status', 'unknown'), 'message_id': r.get('messageId', ''), 'phone': phone}
        return {'status': 'unknown', 'response': resp}
    except Exception as e:
        logger.error(f"SMS send failed to {phone}: {e}")
        return {'status': 'error', 'error': str(e)}


def send_bulk_sms(recipients: list, message: str) -> list:
    """Send same message to multiple phone numbers."""
    return [send_sms(phone, message) for phone in recipients]


def _normalise_phone(phone: str) -> str:
    """Normalise Ethiopian phone numbers to +251 format."""
    if not phone:
        return ''
    phone = phone.strip().replace(' ', '').replace('-', '')
    if phone.startswith('0') and len(phone) == 10:
        phone = '+251' + phone[1:]
    elif phone.startswith('251') and not phone.startswith('+'):
        phone = '+' + phone
    elif not phone.startswith('+'):
        phone = '+251' + phone.lstrip('0')
    return phone


# ── Message templates ─────────────────────────────────────────────────────────

def appointment_reminder_msg(patient_name: str, facility: str,
                              appt_date: str, language: str = 'en') -> str:
    msgs = {
        'en': f"Dear {patient_name}, reminder: your appointment at {facility} is on {appt_date}. Please arrive 30 min early. - Health Assistant",
        'am': f"ውድ {patient_name}፣ ቀጠሮዎ {facility} ላይ {appt_date} ነው። 30 ደቂቃ ቀደም ብለው ይምጡ። - የጤና ረዳት",
        'ti': f"ክቡር/ት {patient_name}፣ ቆጸራኻ/ኺ {facility} ኣብ {appt_date} እዩ። - ሓጋዚ ጥዕና",
        'om': f"Kabajamaa {patient_name}, beellamni kee {facility} guyyaa {appt_date} dha. - Gargaaraa Fayyaa",
    }
    return msgs.get(language, msgs['en'])


def vaccine_reminder_msg(child_name: str, vaccine: str,
                          due_date: str, language: str = 'en') -> str:
    msgs = {
        'en': f"Reminder: {child_name}'s {vaccine} vaccine is due on {due_date}. Visit your nearest health post. - Health Assistant",
        'am': f"ማስታወሻ: {child_name} ለ{vaccine} ክትባት {due_date} ቀን ወደ ጤና ኬላ ይሂዱ። - የጤና ረዳት",
        'ti': f"ዘኪሮ: {child_name} ናይ {vaccine} ክታበት {due_date} ናብ ጥዕና ጣቢያ ኪዱ። - ሓጋዚ ጥዕና",
        'om': f"Yaadachiisa: {child_name} talaallii {vaccine} guyyaa {due_date} buufata fayyaa deemi. - Gargaaraa Fayyaa",
    }
    return msgs.get(language, msgs['en'])


def anc_reminder_msg(mother_name: str, visit_label: str,
                     due_date: str, language: str = 'en') -> str:
    msgs = {
        'en': f"Dear {mother_name}, your {visit_label} is due around {due_date}. Please visit your health centre. Danger signs: heavy bleeding, severe headache — go to hospital immediately. - Health Assistant",
        'am': f"ውድ {mother_name}፣ {visit_label} {due_date} አካባቢ ነው። ወደ ጤና ጣቢያ ይሂዱ። አደጋ ምልክቶች ካሉ ወዲያውኑ ሆስፒታል ይሂዱ። - የጤና ረዳት",
        'ti': f"ክቡርት {mother_name}፣ {visit_label} {due_date} ኣካባቢ እዩ። ናብ ጥዕና ጣቢያ ኪዲ። - ሓጋዚ ጥዕና",
        'om': f"Kabajamtuu {mother_name}, {visit_label} guyyaa {due_date} dha. Buufata fayyaa deemi. - Gargaaraa Fayyaa",
    }
    return msgs.get(language, msgs['en'])


def medication_reminder_msg(patient_name: str, medication: str,
                             time_of_day: str = 'morning', language: str = 'en') -> str:
    msgs = {
        'en': f"Reminder: {patient_name}, please take your {medication} now ({time_of_day}). Do not skip doses. - Health Assistant",
        'am': f"ማስታወሻ: {patient_name}፣ አሁን {medication} ይውሰዱ ({time_of_day})። ዶዝ አይዝለሉ። - የጤና ረዳት",
        'ti': f"ዘኪሮ: {patient_name}፣ ሕጂ {medication} ውሰድ ({time_of_day})። ዶዝ ኣይዝለፍ። - ሓጋዚ ጥዕና",
        'om': f"Yaadachiisa: {patient_name}, amma {medication} fudhu ({time_of_day}). - Gargaaraa Fayyaa",
    }
    return msgs.get(language, msgs['en'])


def danger_sign_alert_msg(name: str, sign: str, language: str = 'en') -> str:
    msgs = {
        'en': f"URGENT: {name} reported danger sign: {sign}. GO TO HOSPITAL IMMEDIATELY. Call emergency: 907. - Health Assistant",
        'am': f"አስቸኳይ: {name} አደጋ ምልክት ሪፖርት አደረጉ: {sign}። ወዲያውኑ ሆስፒታል ይሂዱ። ድንገተኛ: 907። - የጤና ረዳት",
        'ti': f"ህጹጽ: {name} ሓደጋ ምልክት ሪፖርት ጌሩ: {sign}። ሕጂ ሆስፒታል ኪድ። - ሓጋዚ ጥዕና",
        'om': f"HATATTAMA: {name} mallattoo balaa gabaase: {sign}. HOSPITAALA DEEMI. - Gargaaraa Fayyaa",
    }
    return msgs.get(language, msgs['en'])
