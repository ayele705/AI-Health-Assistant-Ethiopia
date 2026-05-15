"""
Inbound SMS chat handler.
Parses incoming SMS messages and routes them to the symptom engine.
Supports simple keyword-based flow for feature phones.

Flow:
  User sends: "fever headache" → gets top condition + self-care advice
  User sends: "HELP" → gets menu
  User sends: "TIPS" → gets a random health tip
  User sends: "FACILITY" → gets nearest facility info (by region keyword)
  User sends: "CANCEL" → cancels appointment (matched by phone)
"""
import re
import random
from core.symptom_engine import assess, translate_symptoms
from core.knowledge_base import get_health_tips, get_facilities
from core.sms_engine import send_sms


HELP_MSG = {
    'en': "Health Assistant Menu:\n1. Send symptoms (e.g. 'fever cough')\n2. TIPS - health tip\n3. FACILITY - find clinic\n4. CANCEL - cancel appointment\nReply HELP anytime.",
    'am': "የጤና ረዳት ምናሌ:\n1. ምልክቶች ላኩ (ለምሳሌ 'ትኩሳት ሳል')\n2. TIPS - የጤና ምክር\n3. FACILITY - ጤና ጣቢያ\n4. CANCEL - ቀጠሮ ሰርዝ",
    'ti': "ሓጋዚ ጥዕና ምናሌ:\n1. ምልክታት ስደድ\n2. TIPS\n3. FACILITY\n4. CANCEL",
    'om': "Gargaaraa Fayyaa:\n1. Mallattoo ergi\n2. TIPS\n3. FACILITY\n4. CANCEL",
}

UNKNOWN_MSG = {
    'en': "Sorry, I didn't understand. Send HELP for the menu, or type your symptoms (e.g. 'fever headache cough').",
    'am': "ይቅርታ፣ አልገባኝም። HELP ላኩ ወይም ምልክቶቻቸውን ይጻፉ (ለምሳሌ 'ትኩሳት ሳል')።",
    'ti': "ይቅርታ፣ ኣይተረዳእኩን። HELP ስደድ ወይ ምልክታትካ ጸሓፍ።",
    'om': "Dhiifama, hin hubanne. HELP ergi ykn mallattoo kee barreessi.",
}


def detect_language(text: str) -> str:
    """Simple language detection based on character ranges."""
    amharic_chars = sum(1 for c in text if '\u1200' <= c <= '\u137f')
    if amharic_chars > 2:
        return 'am'
    return 'en'


def handle_inbound_sms(phone: str, message: str, shortcode: str = '') -> str:
    """
    Process an inbound SMS and return the reply message.
    Also sends the reply via SMS.
    """
    text = message.strip()
    lang = detect_language(text)
    text_upper = text.upper().strip()

    # HELP
    if text_upper in ('HELP', 'MENU', 'START', 'HI', 'HELLO', 'ሰላም'):
        reply = HELP_MSG.get(lang, HELP_MSG['en'])

    # TIPS
    elif text_upper == 'TIPS':
        tips = get_health_tips(language=lang)
        if tips:
            tip = random.choice(tips)
            reply = f" {tip['title']}\n{tip['content'][:200]}"
        else:
            reply = "No tips available."

    # FACILITY
    elif text_upper.startswith('FACILITY'):
        parts = text.split(None, 1)
        region = parts[1].strip() if len(parts) > 1 else ''
        facilities = get_facilities(region=region or None)[:3]
        if facilities:
            lines = [f"Nearby facilities:"]
            for f in facilities:
                lines.append(f"• {f['name']} ({f.get('facility_type','')}) {f.get('phone','')}")
            reply = '\n'.join(lines)
        else:
            reply = "No facilities found. Visit your nearest health post."

    # CANCEL appointment
    elif text_upper.startswith('CANCEL'):
        reply = _handle_cancel(phone, lang)

    # STOP / unsubscribe
    elif text_upper in ('STOP', 'UNSUBSCRIBE'):
        _handle_unsubscribe(phone)
        reply = "You have been unsubscribed from reminders. Send START to re-subscribe."

    # Symptom assessment — treat as symptom list
    else:
        reply = _handle_symptoms(text, lang)

    # Send reply
    send_sms(phone, reply)
    return reply


def _handle_symptoms(text: str, lang: str) -> str:
    """Parse symptom text and return assessment reply."""
    # Split on commas, spaces, and common separators
    raw_symptoms = re.split(r'[,،\s]+', text.strip())
    raw_symptoms = [s.strip() for s in raw_symptoms if len(s.strip()) > 2]

    if not raw_symptoms:
        return UNKNOWN_MSG.get(lang, UNKNOWN_MSG['en'])

    result = assess(raw_symptoms, age=25, sex='unknown', language=lang)
    conditions = result.get('conditions', [])

    if not conditions:
        return result.get('message', UNKNOWN_MSG.get(lang, UNKNOWN_MSG['en']))

    top = conditions[0]
    urgency = top.get('urgency', 'self_care')

    urgency_prefix = {
        'emergency':           {'en': ' EMERGENCY: ', 'am': ' አስቸኳይ: ', 'ti': ' ህጹጽ: ', 'om': ' HATATTAMA: '},
        'visit_health_center': {'en': '️ Visit health centre: ', 'am': '️ ጤና ጣቢያ ይሂዱ: ', 'ti': '️ ናብ ጥዕና ጣቢያ ኪድ: ', 'om': '️ Buufata deemi: '},
        'self_care':           {'en': 'ℹ️ ', 'am': 'ℹ️ ', 'ti': 'ℹ️ ', 'om': 'ℹ️ '},
    }
    prefix = urgency_prefix.get(urgency, urgency_prefix['self_care']).get(lang, '')

    # Keep SMS under 160 chars per segment
    name = top.get('name', '')
    care = top.get('self_care', '')[:120]
    reply = f"{prefix}{name}\n{care}"

    # Emergency alerts
    alerts = result.get('emergency_alerts', [])
    if alerts:
        reply += f"\n GO TO HOSPITAL NOW"

    return reply[:320]  # max 2 SMS segments


def _handle_cancel(phone: str, lang: str) -> str:
    """Cancel pending appointment for this phone number."""
    try:
        from api.models import Appointment
        appts = Appointment.objects.filter(patient_phone__icontains=phone[-9:], status='pending')
        if appts.exists():
            appts.update(status='cancelled')
            msgs = {'en': 'Your appointment has been cancelled.', 'am': 'ቀጠሮዎ ተሰርዟል።', 'ti': 'ቆጸራኻ ተሰሪዙ።', 'om': 'Beellamni kee haqame.'}
            return msgs.get(lang, msgs['en'])
        msgs = {'en': 'No pending appointment found for your number.', 'am': 'ቀጠሮ አልተገኘም።', 'ti': 'ቆጸራ ኣይተረኽበን።', 'om': 'Beellama hin argamne.'}
        return msgs.get(lang, msgs['en'])
    except Exception:
        return "Could not process cancellation. Please call the facility directly."


def _handle_unsubscribe(phone: str):
    """Mark phone as unsubscribed from reminders."""
    try:
        from api.models import MedicationReminder
        MedicationReminder.objects.filter(phone__icontains=phone[-9:]).update(active=False)
    except Exception:
        pass
