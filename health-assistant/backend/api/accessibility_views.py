"""
Accessibility, consent, IVR/SMS, pilot, and partner API views.
"""
import uuid
import csv
import io
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.consent import get_consent_script, check_consent_response
from core.localization import get_safe_message, get_ivr_menu, SUPPORTED_LANGUAGES
from core.safety import apply_safety_threshold, minimize_consultation_data, is_minor, age_to_range
from core.symptom_engine import assess
from core.knowledge_base import get_all_conditions, get_facilities

from .accessibility_models import (
    ConsentLog, AccessibilitySession, AccessibilityFeedback,
    EmergencyAuditLog, CHVSupporterRegistry, PartnerRegistry,
    PilotCohort, FieldTestChecklist,
)
from .models import Consultation


# ── Consent ──────────────────────────────────────────────────────────────────

@api_view(['GET'])
def consent_script(request):
    """Return the consent script for a given language and channel."""
    language = request.query_params.get('language', 'en')
    channel = request.query_params.get('channel', 'app')
    script = get_consent_script(language)
    return Response({
        'language': language,
        'channel': channel,
        'consent_text': script['text'],
        'caregiver_prompt': script['caregiver_prompt'],
        'minor_warning': script['minor_warning'],
        'disclaimer': script['disclaimer'],
    })


@api_view(['POST'])
def consent_submit(request):
    """
    Record a consent decision.
    Body: { session_id, language, channel, response, caregiver_name?,
            caregiver_relationship?, caregiver_phone?, age? }
    """
    session_id = request.data.get('session_id') or str(uuid.uuid4())
    language = request.data.get('language', 'en')
    channel = request.data.get('channel', 'app')
    user_response = request.data.get('response', '')
    age = int(request.data.get('age', 25))

    decision = check_consent_response(user_response, language)
    script = get_consent_script(language)

    if decision == 'withdraw':
        ConsentLog.objects.create(
            session_id=session_id, language=language, channel=channel,
            given=False, withdrawn=True,
        )
        return Response({'status': 'withdrawn', 'message': script['withdraw_confirm']})

    if decision == 'caregiver':
        caregiver_name = request.data.get('caregiver_name', '')
        caregiver_rel = request.data.get('caregiver_relationship', '')
        caregiver_phone = request.data.get('caregiver_phone', '')
        ConsentLog.objects.create(
            session_id=session_id, language=language, channel=channel,
            given=True, consent_type='caregiver',
            caregiver_name=caregiver_name,
            caregiver_relationship=caregiver_rel,
            caregiver_phone=caregiver_phone,
        )
        return Response({
            'status': 'caregiver_mode',
            'session_id': session_id,
            'message': script['caregiver_prompt'],
        })

    if decision == 'agree':
        if is_minor(age):
            return Response({
                'status': 'minor_warning',
                'message': script['minor_warning'],
                'chv_lookup_url': f'/api/v1/accessibility/chv/?language={language}',
            })
        ConsentLog.objects.create(
            session_id=session_id, language=language, channel=channel, given=True,
        )
        return Response({'status': 'agreed', 'session_id': session_id})

    return Response({'status': 'unknown', 'message': script['text']})


@api_view(['DELETE'])
def consent_withdraw(request, session_id):
    """Withdraw consent and delete all session health data."""
    ConsentLog.objects.filter(session_id=session_id).update(withdrawn=True)
    Consultation.objects.filter(session_id=session_id).delete()
    AccessibilitySession.objects.filter(session_id=session_id).delete()
    return Response({'status': 'deleted', 'session_id': session_id})


# ── Accessibility Session Tracking ───────────────────────────────────────────

@api_view(['POST'])
def accessibility_session_start(request):
    """
    Register accessibility modes for a session.
    Body: { session_id?, channel, language, simple_mode, high_contrast,
            large_text, screen_reader, voice_input, caregiver_mode, disability_category }
    """
    session_id = request.data.get('session_id') or str(uuid.uuid4())
    AccessibilitySession.objects.update_or_create(
        session_id=session_id,
        defaults={
            'channel': request.data.get('channel', 'app'),
            'language': request.data.get('language', 'en'),
            'simple_mode': request.data.get('simple_mode', False),
            'high_contrast': request.data.get('high_contrast', False),
            'large_text': request.data.get('large_text', False),
            'screen_reader': request.data.get('screen_reader', False),
            'voice_input': request.data.get('voice_input', False),
            'caregiver_mode': request.data.get('caregiver_mode', False),
            'disability_category': request.data.get('disability_category', ''),
        }
    )
    return Response({'session_id': session_id}, status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
def accessibility_session_complete(request, session_id):
    """Mark a session as completed with duration."""
    duration = int(request.data.get('duration_seconds', 0))
    AccessibilitySession.objects.filter(session_id=session_id).update(
        completed=True, duration_seconds=duration
    )
    return Response({'status': 'completed'})


# ── Feedback ─────────────────────────────────────────────────────────────────

@api_view(['POST'])
def submit_feedback(request):
    """
    Submit accessibility feedback survey.
    Body: { session_id, channel, language, disability_category,
            score_q1, score_q2, score_q3, comment? }
    """
    session_id = request.data.get('session_id', str(uuid.uuid4()))
    scores = [
        int(request.data.get('score_q1', 3)),
        int(request.data.get('score_q2', 3)),
        int(request.data.get('score_q3', 3)),
    ]
    avg = sum(scores) / 3
    fb = AccessibilityFeedback.objects.create(
        session_id=session_id,
        channel=request.data.get('channel', 'app'),
        language=request.data.get('language', 'en'),
        disability_category=request.data.get('disability_category', ''),
        score_q1=scores[0],
        score_q2=scores[1],
        score_q3=scores[2],
        comment=request.data.get('comment', ''),
        flagged=(avg < 3.0),
    )
    return Response({'id': fb.id, 'average_score': fb.average_score, 'flagged': fb.flagged},
                    status=status.HTTP_201_CREATED)


# ── IVR / SMS Channel ─────────────────────────────────────────────────────────

@api_view(['POST'])
def ivr_inbound(request):
    """
    Simulate IVR inbound call handler.
    Body: { caller_number (hashed), language?, step?, input?, session_id? }
    Returns TTS prompt text and next step.
    """
    language = request.data.get('language', 'en')
    step = request.data.get('step', 'lang_select')
    user_input = request.data.get('input', '')
    session_id = request.data.get('session_id') or str(uuid.uuid4())
    menu = get_ivr_menu(language)

    # Language selection step
    if step == 'lang_select':
        lang_map = {'1': 'en', '2': 'am', '3': 'om', '4': 'ti', '5': 'sid'}
        if user_input in lang_map:
            language = lang_map[user_input]
            menu = get_ivr_menu(language)
        return Response({
            'session_id': session_id,
            'language': language,
            'tts': menu['symptom_prompt'],
            'next_step': 'symptom',
        })

    if step == 'symptom':
        symptom_map = {'1': 'fever', '2': 'cough', '3': 'stomach pain', '4': user_input or 'other'}
        symptom = symptom_map.get(user_input, user_input or 'other')
        return Response({
            'session_id': session_id,
            'language': language,
            'collected': {'symptom': symptom},
            'tts': menu['duration_prompt'],
            'next_step': 'duration',
        })

    if step == 'assess':
        # Final step: run assessment
        symptoms = request.data.get('symptoms', [])
        age = int(request.data.get('age', 25))
        sex = request.data.get('sex', 'unknown')
        result = assess(symptoms, age, sex, language)
        result = apply_safety_threshold(result, language)

        if result.get('urgency') == 'emergency':
            facilities_data = get_facilities()
            nearest_phone = facilities_data[0]['phone'] if facilities_data else 'your local hospital'
            tts = f"{menu['emergency']} {nearest_phone}"
            EmergencyAuditLog.objects.create(
                session_id=session_id, channel='ivr',
                urgency_level='emergency', language=language,
            )
        else:
            msg = result.get('message', '')
            top = result['conditions'][0] if result.get('conditions') else {}
            care = top.get('self_care', '')
            tts = f"{menu['result_intro']} {msg} {care} {menu['sms_offer']}"

        return Response({
            'session_id': session_id,
            'language': language,
            'tts': tts,
            'result': result,
            'next_step': 'goodbye',
        })

    return Response({'session_id': session_id, 'tts': menu['goodbye'], 'next_step': 'end'})


@api_view(['POST'])
def sms_inbound(request):
    """
    Handle inbound SMS keyword assessment.
    Body: { from_number (hashed), message, language? }
    Returns SMS reply text (≤160 chars per segment).
    """
    message = request.data.get('message', '').strip().lower()
    language = request.data.get('language', 'en')
    session_id = str(uuid.uuid4())

    # Parse symptom keywords
    keyword_map = {
        'fever': 'fever', 'ትኩሳት': 'fever', 'ho\'a': 'fever', 'ረስኒ': 'fever',
        'cough': 'cough', 'ሳል': 'cough', 'qufaa': 'cough', 'ሳዕዓል': 'cough',
        'diarrhea': 'diarrhea', 'ተቅማጥ': 'diarrhea',
        'headache': 'headache', 'ራስ ምታት': 'headache',
        'vomiting': 'vomiting', 'ማስታወክ': 'vomiting',
        'pain': 'stomach pain', 'ህመም': 'stomach pain',
    }

    matched_symptom = None
    for kw, symptom in keyword_map.items():
        if kw in message:
            matched_symptom = symptom
            break

    if not matched_symptom:
        safe_msg = get_safe_message(language)
        return Response({'reply': safe_msg[:160], 'session_id': session_id})

    result = assess([matched_symptom], 25, 'unknown', language)
    result = apply_safety_threshold(result, language)

    if result.get('urgency') == 'emergency':
        facilities_data = get_facilities()
        phone = facilities_data[0]['phone'] if facilities_data else ''
        reply = f"EMERGENCY: Go to health center NOW. {phone}"
        EmergencyAuditLog.objects.create(
            session_id=session_id, channel='sms',
            urgency_level='emergency', language=language,
        )
    else:
        top = result['conditions'][0] if result.get('conditions') else {}
        name = top.get('name', '')
        care = top.get('self_care', '')[:80]
        reply = f"{name}: {care}"

    return Response({'reply': reply[:160], 'session_id': session_id, 'result': result})


# ── CHV Registry ──────────────────────────────────────────────────────────────

@api_view(['GET'])
def chv_lookup(request):
    """Find nearest certified CHV supporters. Query: region, language."""
    region = request.query_params.get('region', '')
    language = request.query_params.get('language', '')
    qs = CHVSupporterRegistry.objects.filter(certified=True)
    if region:
        qs = qs.filter(region__icontains=region)
    if language:
        qs = qs.filter(language=language)
    data = [
        {
            'id': c.id, 'name': c.name, 'region': c.region,
            'woreda': c.woreda, 'phone': c.phone,
            'disability_specialties': c.disability_specialties,
        }
        for c in qs[:10]
    ]
    return Response({'supporters': data, 'count': len(data)})


@api_view(['POST'])
def chv_register(request):
    """Register a new CHV supporter."""
    required = ['name', 'region', 'phone']
    for f in required:
        if not request.data.get(f):
            return Response({'error': f'{f} is required.'}, status=400)
    chv = CHVSupporterRegistry.objects.create(
        name=request.data['name'],
        region=request.data['region'],
        woreda=request.data.get('woreda', ''),
        phone=request.data['phone'],
        language=request.data.get('language', 'am'),
        disability_specialties=request.data.get('disability_specialties', []),
    )
    return Response({'id': chv.id, 'name': chv.name, 'certified': chv.certified},
                    status=status.HTTP_201_CREATED)


# ── Partner Registry ──────────────────────────────────────────────────────────

@api_view(['GET'])
def partner_list(request):
    partners = PartnerRegistry.objects.filter(status='active')
    return Response({
        'partners': [
            {'id': p.id, 'name': p.name, 'type': p.partner_type,
             'territory': p.territory, 'status': p.status}
            for p in partners
        ]
    })


@api_view(['POST'])
def partner_register(request):
    required = ['name', 'partner_type', 'contact_person']
    for f in required:
        if not request.data.get(f):
            return Response({'error': f'{f} is required.'}, status=400)
    api_key = str(uuid.uuid4()).replace('-', '')[:32]
    p = PartnerRegistry.objects.create(
        name=request.data['name'],
        partner_type=request.data['partner_type'],
        contact_person=request.data['contact_person'],
        contact_email=request.data.get('contact_email', ''),
        contact_phone=request.data.get('contact_phone', ''),
        territory=request.data.get('territory', ''),
        api_key=api_key,
    )
    return Response({'id': p.id, 'name': p.name, 'api_key': api_key},
                    status=status.HTTP_201_CREATED)


# ── Pilot & Field Testing ─────────────────────────────────────────────────────

@api_view(['GET', 'POST'])
def pilot_cohorts(request):
    if request.method == 'POST':
        cohort = PilotCohort.objects.create(
            name=request.data.get('name', 'Cohort'),
            region=request.data.get('region', ''),
            facility_id=request.data.get('facility_id', ''),
            chv_group=request.data.get('chv_group', ''),
            target_sample_size=int(request.data.get('target_sample_size', 100)),
            evaluator_email=request.data.get('evaluator_email', ''),
        )
        return Response({'id': cohort.id, 'name': cohort.name}, status=status.HTTP_201_CREATED)
    cohorts = PilotCohort.objects.filter(active=True)
    return Response({'cohorts': [{'id': c.id, 'name': c.name, 'target': c.target_sample_size} for c in cohorts]})


@api_view(['POST'])
def field_checklist_submit(request):
    """CHV submits field-testing checklist after an assisted session."""
    checklist = FieldTestChecklist.objects.create(
        session_id=request.data.get('session_id', str(uuid.uuid4())),
        chv_name=request.data.get('chv_name', ''),
        device_compatible=request.data.get('device_compatible', True),
        network_condition=request.data.get('network_condition', 'good'),
        user_comprehension=request.data.get('user_comprehension', 'good'),
        adverse_event=request.data.get('adverse_event', False),
        adverse_event_notes=request.data.get('adverse_event_notes', ''),
        notes=request.data.get('notes', ''),
    )
    return Response({'id': checklist.id}, status=status.HTTP_201_CREATED)


# ── Accessibility Dashboard KPIs ──────────────────────────────────────────────

@api_view(['GET'])
def accessibility_kpis(request):
    """Return aggregated accessibility KPIs for the dashboard."""
    sessions = AccessibilitySession.objects.all()
    total = sessions.count()
    completed = sessions.filter(completed=True).count()

    mode_counts = {
        'simple_mode': sessions.filter(simple_mode=True).count(),
        'high_contrast': sessions.filter(high_contrast=True).count(),
        'large_text': sessions.filter(large_text=True).count(),
        'screen_reader': sessions.filter(screen_reader=True).count(),
        'voice_input': sessions.filter(voice_input=True).count(),
        'caregiver_mode': sessions.filter(caregiver_mode=True).count(),
        'ivr': sessions.filter(channel='ivr').count(),
        'sms': sessions.filter(channel='sms').count(),
        'ussd': sessions.filter(channel='ussd').count(),
    }

    feedback = AccessibilityFeedback.objects.all()
    avg_score = 0.0
    if feedback.exists():
        total_score = sum(f.average_score for f in feedback)
        avg_score = round(total_score / feedback.count(), 2)

    flagged_count = feedback.filter(flagged=True).count()
    emergency_count = EmergencyAuditLog.objects.count()
    partner_count = PartnerRegistry.objects.filter(status='active').count()

    return Response({
        'total_sessions': total,
        'completed_sessions': completed,
        'completion_rate': round(completed / total * 100, 1) if total else 0,
        'mode_counts': mode_counts,
        'average_feedback_score': avg_score,
        'flagged_feedback_count': flagged_count,
        'emergency_escalations': emergency_count,
        'active_partners': partner_count,
    })


@api_view(['GET'])
def accessibility_kpis_csv(request):
    """Export KPI data as CSV."""
    from django.http import HttpResponse
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['metric', 'value'])

    sessions = AccessibilitySession.objects.all()
    total = sessions.count()
    completed = sessions.filter(completed=True).count()
    writer.writerow(['total_sessions', total])
    writer.writerow(['completed_sessions', completed])
    writer.writerow(['completion_rate_pct', round(completed / total * 100, 1) if total else 0])

    for mode in ['simple_mode', 'high_contrast', 'large_text', 'screen_reader', 'voice_input', 'caregiver_mode']:
        count = sessions.filter(**{mode: True}).count()
        writer.writerow([f'sessions_{mode}', count])

    for ch in ['ivr', 'sms', 'ussd', 'app']:
        writer.writerow([f'sessions_channel_{ch}', sessions.filter(channel=ch).count()])

    feedback = AccessibilityFeedback.objects.all()
    if feedback.exists():
        avg = round(sum(f.average_score for f in feedback) / feedback.count(), 2)
        writer.writerow(['average_feedback_score', avg])

    writer.writerow(['emergency_escalations', EmergencyAuditLog.objects.count()])
    writer.writerow(['active_partners', PartnerRegistry.objects.filter(status='active').count()])

    response = HttpResponse(output.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="accessibility_kpis.csv"'
    return response


# ── Localization helpers ──────────────────────────────────────────────────────

@api_view(['GET'])
def ivr_menu_text(request):
    """Return IVR menu prompts for a language."""
    language = request.query_params.get('language', 'en')
    return Response({'language': language, 'menu': get_ivr_menu(language)})


@api_view(['GET'])
def supported_languages(request):
    return Response({'languages': SUPPORTED_LANGUAGES})
