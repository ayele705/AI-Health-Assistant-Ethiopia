"""
USSD/IVR webhook views for Africa's Talking integration.
"""
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.ussd_engine import process_ussd
from core.sms_engine import send_sms
from .models import USSDSessionLog


@api_view(['POST'])
def ussd_webhook(request):
    """Africa's Talking USSD webhook handler."""
    session_id   = request.data.get('sessionId', '') or request.POST.get('sessionId', '')
    phone        = request.data.get('phoneNumber', '') or request.POST.get('phoneNumber', '')
    text         = request.data.get('text', '') or request.POST.get('text', '')
    service_code = request.data.get('serviceCode', '') or request.POST.get('serviceCode', '')

    result = process_ussd(session_id, phone, text, service_code)

    # Persist/update session log (anonymised)
    _upsert_session_log(result, service_code)

    # Send SMS if requested
    if result.get('sms_sent') and result.get('sms_phone') and result.get('sms_body'):
        send_sms(result['sms_phone'], result['sms_body'])

    # Africa's Talking expects plain text response
    return HttpResponse(result['response'], content_type='text/plain')


@api_view(['POST'])
def ivr_webhook(request):
    """Africa's Talking IVR webhook — returns TwiML-style XML."""
    session_id = request.data.get('sessionId', '') or request.POST.get('sessionId', '')
    phone      = request.data.get('callerNumber', '') or request.POST.get('callerNumber', '')
    dtmf       = request.data.get('dtmfDigits', '') or request.POST.get('dtmfDigits', '')

    result = process_ussd(session_id, phone, dtmf)
    text   = result['response'].replace('CON ', '').replace('END ', '')

    # Build TwiML-style XML
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say voice="woman" playBeep="false">{text}</Say>
  {'<GetDigits timeout="30" finishOnKey="#" callbackUrl="/api/v1/ivr/" />' if not result.get('completed') else ''}
</Response>"""

    # Send SMS on emergency
    if result.get('urgency') == 'emergency' and phone:
        send_sms(phone, text[:160])

    return HttpResponse(xml, content_type='application/xml')


@api_view(['GET'])
def ussd_session_list(request):
    """Admin: list anonymised USSD session logs."""
    sessions = USSDSessionLog.objects.order_by('-created_at')[:100]
    data = list(sessions.values(
        'session_hash', 'service_code', 'language_selected',
        'symptom_selected', 'urgency_result', 'sms_sent', 'completed', 'created_at'
    ))
    return Response({'sessions': data, 'count': len(data)})


# ── Helpers ───────────────────────────────────────────────────────────────────

def _upsert_session_log(result, service_code):
    try:
        USSDSessionLog.objects.update_or_create(
            session_hash=result['session_hash'],
            defaults={
                'service_code':      service_code,
                'language_selected': result.get('lang', ''),
                'symptom_selected':  result.get('symptom', ''),
                'urgency_result':    result.get('urgency', ''),
                'sms_sent':          result.get('sms_sent', False),
                'completed':         result.get('completed', False),
            }
        )
    except Exception:
        pass
