import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.chatbot import start_session, process_message, get_session
from core.knowledge_base import get_health_tips, get_facilities, get_all_conditions
from core.symptom_engine import assess
from core.safety import apply_safety_threshold, minimize_consultation_data, is_minor
from core.medication_engine import search_medications, get_medication_by_id
from core.geolocation import find_nearest_facilities
from .models import Consultation, Appointment
from .validators import (
    ValidationError, validate_request,
    sanitize_text, sanitize_optional_text,
    validate_language, validate_age, validate_sex,
    validate_phone, validate_date_string, validate_past_date, validate_future_date,
    validate_symptoms, validate_weight, validate_height, validate_muac,
    validate_blood_pressure, validate_glucose,
    validate_coordinates, validate_urgency,
    validate_positive_integer, require_fields,
    validate_rating, validate_age_months,
    validate_condition, validate_visit_type, validate_time_of_day,
)


@api_view(['POST'])
@validate_request
def chat_start(request):
    """Start a new symptom assessment conversation."""
    language = validate_language(request.data.get('language', 'en'))
    session_id = str(uuid.uuid4())
    response = start_session(session_id, language)
    response['session_id'] = session_id
    return Response(response, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@validate_request
def chat_message(request, session_id):
    """Send a message in an ongoing consultation session."""
    user_input = sanitize_text(request.data.get('message', ''), field='message', max_length=2000)

    result = process_message(session_id, user_input)

    # If assessment is complete, persist to DB
    if result.get('done'):
        session = get_session(session_id)
        Consultation.objects.update_or_create(
            session_id=session_id,
            defaults={
                'symptoms': result.get('collected_symptoms', []),
                'assessment_result': result,
                'urgency_level': result.get('urgency', ''),
                'age': session.get('age', 0) if session else 0,
                'sex': session.get('sex', '') if session else '',
                'language': session.get('language', 'en') if session else 'en',
            }
        )

    return Response(result)


@api_view(['POST'])
@validate_request
def quick_assess(request):
    """
    Direct symptom assessment without conversation flow.
    Body: { symptoms: [...], age: int, sex: str, language: str }
    """
    symptoms = validate_symptoms(request.data.get('symptoms', []))
    age      = validate_age(request.data.get('age', 25))
    sex      = validate_sex(request.data.get('sex', 'unknown'))
    language = validate_language(request.data.get('language', 'en'))

    result = assess(symptoms, age, sex, language)
    result = apply_safety_threshold(result, language)
    return Response(result)


@api_view(['GET'])
@validate_request
def safe_response(request):
    """
    Returns the standard safe uncertainty message in the requested language.
    Used when the assistant is not confident about a user's condition.
    Query param: language (en/am)
    """
    language = validate_language(request.query_params.get('language', 'en'))
    if language == 'am':
        message = 'እርግጠኛ አይደለሁም — እባክዎ ወደ ቅርብ ጤና ሠራተኛ ይሂዱ ወይም ወደ ጤና ጣቢያ ይደውሉ።'
    else:
        message = "I'm not sure — please contact your nearest health worker or visit your local health center."
    return Response({'message': message, 'language': language})


@api_view(['GET'])
def health_tips(request):
    """Return health education tips. Query params: category, language."""
    category = request.query_params.get('category')
    language = request.query_params.get('language', 'en')
    tips = get_health_tips(category=category, language=language)
    return Response({'tips': tips, 'count': len(tips)})


@api_view(['GET'])
def facilities(request):
    """Return health facilities. Query param: region."""
    region = request.query_params.get('region')
    data = get_facilities(region=region)
    return Response({'facilities': data, 'count': len(data)})


@api_view(['GET'])
def conditions_list(request):
    """Return all conditions in the knowledge base."""
    language = request.query_params.get('language', 'en')
    conditions = get_all_conditions()
    name_key = f'name_{language}'
    return Response({
        'conditions': [
            {
                'id': c['id'],
                'name': c.get(name_key, c.get('name_en', c['id'])),
                'category': c.get('category', ''),
                'urgency': c.get('urgency', ''),
            }
            for c in conditions
        ]
    })


@api_view(['GET'])
def consultations_list(request):
    """Return recent consultations (for HEW dashboard)."""
    qs = Consultation.objects.order_by('-created_at')[:50]
    data = [
        {
            'session_id': c.session_id,
            'symptoms': c.symptoms,
            'urgency_level': c.urgency_level,
            'created_at': c.created_at.isoformat(),
        }
        for c in qs
    ]
    return Response({'consultations': data, 'count': len(data)})


@api_view(['POST'])
@validate_request
def book_appointment(request):
    """
    Book an appointment at a health facility.
    Body: { patient_name, patient_phone, facility_id, facility_name,
            appointment_date (YYYY-MM-DD), reason, urgency_level, language }
    """
    patient_name  = sanitize_text(request.data.get('patient_name'), field='patient_name', max_length=100)
    patient_phone = validate_phone(request.data.get('patient_phone', ''), field='patient_phone')
    facility_id   = sanitize_text(request.data.get('facility_id'), field='facility_id', max_length=50)
    facility_name = sanitize_text(request.data.get('facility_name'), field='facility_name', max_length=200)
    appt_date     = validate_future_date(request.data.get('appointment_date'), field='appointment_date')
    reason        = sanitize_optional_text(request.data.get('reason', ''), field='reason', max_length=500)
    urgency       = validate_urgency(request.data.get('urgency_level', 'self_care'))
    language      = validate_language(request.data.get('language', 'en'))

    appt = Appointment.objects.create(
        patient_name=patient_name,
        patient_phone=patient_phone,
        facility_id=facility_id,
        facility_name=facility_name,
        appointment_date=appt_date,
        appointment_time=request.data.get('appointment_time') or None,
        reason=reason,
        urgency_level=urgency,
        language=language,
    )
    return Response({
        'id': appt.id,
        'patient_name': appt.patient_name,
        'facility_name': appt.facility_name,
        'appointment_date': str(appt.appointment_date),
        'status': appt.status,
        'message': 'Appointment booked successfully.' if appt.language == 'en' else 'ቀጠሮ በተሳካ ሁኔታ ተይዟል።',
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def appointments_list(request):
    """List appointments. Query param: facility_id"""
    facility_id = request.query_params.get('facility_id')
    qs = Appointment.objects.order_by('-created_at')
    if facility_id:
        qs = qs.filter(facility_id=facility_id)
    data = [
        {
            'id': a.id,
            'patient_name': a.patient_name,
            'patient_phone': a.patient_phone,
            'facility_name': a.facility_name,
            'appointment_date': str(a.appointment_date),
            'reason': a.reason,
            'urgency_level': a.urgency_level,
            'status': a.status,
            'created_at': a.created_at.isoformat(),
        }
        for a in qs[:100]
    ]
    return Response({'appointments': data, 'count': len(data)})


# ── Phase 1: Medication Lookup ────────────────────────────────────────────────

@api_view(['GET'])
@validate_request
def medication_search(request):
    """Search medications by name, generic name, or condition.
    Query params: q (required), language"""
    query    = sanitize_text(request.query_params.get('q', ''), field='q', max_length=200)
    language = validate_language(request.query_params.get('language', 'en'))
    results  = search_medications(query, language)
    return Response({'medications': results, 'count': len(results), 'query': query})


@api_view(['GET'])
@validate_request
def medication_detail(request, med_id):
    """Get full details for a single medication by ID."""
    language = validate_language(request.query_params.get('language', 'en'))
    med = get_medication_by_id(med_id, language)
    if not med:
        return Response({'error': 'Medication not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(med)


# ── Phase 1: Nearest Facility Finder ─────────────────────────────────────────

@api_view(['GET'])
@validate_request
def nearest_facilities(request):
    """Find nearest facilities to a GPS coordinate.
    Query params: lat, lon, radius_km (optional), facility_type, limit (default 50)"""
    lat, lon = validate_coordinates(
        request.query_params.get('lat', ''),
        request.query_params.get('lon', ''),
    )
    radius_km = request.query_params.get('radius_km')
    radius_km = float(radius_km) if radius_km else None
    facility_type = request.query_params.get('facility_type')
    limit = validate_positive_integer(
        request.query_params.get('limit', 50), field='limit', min_val=1, max_val=200, default=50
    )
    results = find_nearest_facilities(lat, lon, radius_km, facility_type, limit)
    return Response({'facilities': results, 'count': len(results), 'user_lat': lat, 'user_lon': lon})


# ── Phase 1: Enhanced Differential Diagnosis ─────────────────────────────────

@api_view(['POST'])
@validate_request
def differential_diagnosis(request):
    """Enhanced differential diagnosis with confidence scores and reasoning.
    Body: { symptoms: [...], age: int, sex: str, language: str }"""
    symptoms = validate_symptoms(request.data.get('symptoms', []))
    age      = validate_age(request.data.get('age', 25))
    sex      = validate_sex(request.data.get('sex', 'unknown'))
    language = validate_language(request.data.get('language', 'en'))

    result = assess(symptoms, age, sex, language)
    result = apply_safety_threshold(result, language)
    # Enrich each condition with prevention and treatment info
    from core.knowledge_base import get_condition_by_id
    for cond in result.get('conditions', []):
        full = get_condition_by_id(cond['id'])
        if full:
            lang_suffix = language if language in ('am', 'ti') else 'en'
            cond['prevention'] = full.get(f'prevention_{lang_suffix}') or full.get('prevention_en', '')
            cond['treatment'] = full.get(f'treatment_{lang_suffix}') or full.get('treatment_en', '')
            cond['icd10'] = full.get('icd10', '')
            cond['emergency_signs'] = full.get(f'emergency_signs_{lang_suffix}') or full.get('emergency_signs_en', [])
    return Response(result)


# ── Phase 2: Community Health Worker Tools ────────────────────────────────────
from datetime import date as date_type
from core.growth_engine import assess_growth, age_months_from_dob
from core.vaccine_schedule import get_vaccine_schedule
from core.pregnancy_engine import get_anc_schedule, check_bp_danger, get_danger_signs_list, calculate_edd, gestational_age_weeks
from core.hew_checklists import get_checklist, get_all_checklist_types
from .models import Child, GrowthRecord, VaccinationRecord, PregnancyRecord, ANCVisit, HEWChecklist


# ── Growth Monitoring ─────────────────────────────────────────────────────────

@api_view(['POST'])
@validate_request
def growth_assess(request):
    """Assess child nutrition status from measurements.
    Body: { weight_kg, height_cm, muac_cm, oedema, age_months, sex }"""
    data       = request.data
    weight     = validate_weight(data.get('weight_kg'))
    height     = validate_height(data.get('height_cm'))
    muac       = validate_muac(data.get('muac_cm'))
    age_months = validate_age_months(data.get('age_months', 0))
    sex        = validate_sex(data.get('sex', 'unknown'))
    oedema     = bool(data.get('oedema', False))

    result = assess_growth(
        weight_kg=weight,
        height_cm=height,
        muac_cm=muac,
        oedema=oedema,
        age_months=age_months,
        sex=sex,
    )
    return Response(result)


@api_view(['POST'])
@validate_request
def child_register(request):
    """Register a new child."""
    import uuid
    dob = validate_past_date(request.data.get('date_of_birth'), field='date_of_birth')
    name        = sanitize_optional_text(request.data.get('name', ''), field='name', max_length=100)
    sex         = validate_sex(request.data.get('sex', ''))
    mother_name = sanitize_optional_text(request.data.get('mother_name', ''), field='mother_name', max_length=100)
    kebele      = sanitize_optional_text(request.data.get('kebele', ''), field='kebele', max_length=100)
    region      = sanitize_optional_text(request.data.get('region', ''), field='region', max_length=100)
    phone       = validate_phone(request.data.get('phone', ''), field='phone')

    child = Child.objects.create(
        child_id=request.data.get('child_id') or str(uuid.uuid4())[:8].upper(),
        name=name,
        date_of_birth=dob,
        sex=sex,
        mother_name=mother_name,
        kebele=kebele,
        region=region,
        phone=phone,
    )
    return Response({'child_id': child.child_id, 'name': child.name, 'id': child.id}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@validate_request
def growth_record_add(request, child_id):
    """Add a growth measurement for a child."""
    try:
        child = Child.objects.get(child_id=child_id)
    except Child.DoesNotExist:
        return Response({'error': 'Child not found.'}, status=status.HTTP_404_NOT_FOUND)

    age_months   = age_months_from_dob(child.date_of_birth)
    weight       = validate_weight(request.data.get('weight_kg'))
    height       = validate_height(request.data.get('height_cm'))
    muac         = validate_muac(request.data.get('muac_cm'))
    oedema       = bool(request.data.get('oedema', False))
    date_measured = validate_past_date(
        request.data.get('date_measured', str(date_type.today())),
        field='date_measured',
        required=False,
    )
    recorded_by  = sanitize_optional_text(request.data.get('recorded_by', ''), field='recorded_by', max_length=100)
    notes        = sanitize_optional_text(request.data.get('notes', ''), field='notes', max_length=500)

    assessment = assess_growth(
        weight_kg=weight,
        muac_cm=muac,
        oedema=oedema,
        age_months=age_months,
        sex=child.sex,
    )

    record = GrowthRecord.objects.create(
        child=child,
        date_measured=date_measured,
        age_months=age_months,
        weight_kg=weight,
        height_cm=height,
        muac_cm=muac,
        oedema=oedema,
        nutrition_status=assessment.get('overall_status', ''),
        recorded_by=recorded_by,
        notes=notes,
    )
    return Response({'record_id': record.id, 'assessment': assessment}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def child_growth_history(request, child_id):
    """Get growth history for a child."""
    try:
        child = Child.objects.get(child_id=child_id)
    except Child.DoesNotExist:
        return Response({'error': 'Child not found.'}, status=status.HTTP_404_NOT_FOUND)
    records = child.growth_records.order_by('date_measured').values(
        'id', 'date_measured', 'age_months', 'weight_kg', 'height_cm', 'muac_cm', 'oedema', 'nutrition_status', 'notes'
    )
    return Response({'child_id': child_id, 'name': child.name, 'records': list(records)})


# ── Vaccination Tracker ───────────────────────────────────────────────────────

@api_view(['GET'])
def vaccine_schedule_view(request, child_id):
    """Get vaccine schedule and status for a child."""
    try:
        child = Child.objects.get(child_id=child_id)
    except Child.DoesNotExist:
        return Response({'error': 'Child not found.'}, status=status.HTTP_404_NOT_FOUND)
    given_ids = list(child.vaccinations.values_list('vaccine_id', flat=True))
    schedule = get_vaccine_schedule(child.date_of_birth, given_ids)
    schedule['child_name'] = child.name
    schedule['child_id'] = child_id
    return Response(schedule)


@api_view(['POST'])
@validate_request
def vaccine_record_add(request, child_id):
    """Record a vaccine given to a child."""
    try:
        child = Child.objects.get(child_id=child_id)
    except Child.DoesNotExist:
        return Response({'error': 'Child not found.'}, status=status.HTTP_404_NOT_FOUND)

    vaccine_id   = sanitize_text(request.data.get('vaccine_id', ''), field='vaccine_id', max_length=50)
    vaccine_name = sanitize_optional_text(request.data.get('vaccine_name', ''), field='vaccine_name', max_length=100)
    date_given   = validate_past_date(
        request.data.get('date_given', str(date_type.today())),
        field='date_given',
        required=False,
    )
    dose_number  = validate_positive_integer(
        request.data.get('dose_number', 1), field='dose_number', min_val=1, max_val=10, default=1
    )
    facility     = sanitize_optional_text(request.data.get('facility', ''), field='facility', max_length=200)
    given_by     = sanitize_optional_text(request.data.get('given_by', ''), field='given_by', max_length=100)

    rec = VaccinationRecord.objects.create(
        child=child,
        vaccine_id=vaccine_id,
        vaccine_name=vaccine_name,
        date_given=date_given,
        dose_number=dose_number,
        facility=facility,
        given_by=given_by,
    )
    return Response({'id': rec.id, 'vaccine_id': rec.vaccine_id, 'date_given': str(rec.date_given)}, status=status.HTTP_201_CREATED)


# ── Pregnancy Follow-up ───────────────────────────────────────────────────────

@api_view(['POST'])
@validate_request
def pregnancy_register(request):
    """Register a new pregnancy."""
    import uuid
    lmp = validate_past_date(request.data.get('lmp_date'), field='lmp_date')
    edd = calculate_edd(lmp)

    mother_name  = sanitize_optional_text(request.data.get('mother_name', ''), field='mother_name', max_length=100)
    age          = validate_age(request.data.get('age', 0), min_age=10, max_age=60, default=0)
    phone        = validate_phone(request.data.get('phone', ''), field='phone')
    kebele       = sanitize_optional_text(request.data.get('kebele', ''), field='kebele', max_length=100)
    region       = sanitize_optional_text(request.data.get('region', ''), field='region', max_length=100)
    gravida      = validate_positive_integer(request.data.get('gravida', 1), field='gravida', min_val=1, max_val=20, default=1)
    parity       = validate_positive_integer(request.data.get('parity', 0), field='parity', min_val=0, max_val=20, default=0)
    risk_factors = request.data.get('risk_factors', [])
    if not isinstance(risk_factors, list):
        raise ValidationError('risk_factors must be a list.', field='risk_factors')

    preg = PregnancyRecord.objects.create(
        record_id=request.data.get('record_id') or str(uuid.uuid4())[:8].upper(),
        mother_name=mother_name,
        age=age,
        phone=phone,
        kebele=kebele,
        region=region,
        lmp_date=lmp,
        edd=edd,
        gravida=gravida,
        parity=parity,
        risk_factors=risk_factors,
    )
    ga = gestational_age_weeks(lmp)
    return Response({'record_id': preg.record_id, 'edd': str(edd), 'gestational_age_weeks': ga}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def pregnancy_schedule(request, record_id):
    """Get ANC schedule and status for a pregnancy."""
    try:
        preg = PregnancyRecord.objects.get(record_id=record_id)
    except PregnancyRecord.DoesNotExist:
        return Response({'error': 'Pregnancy record not found.'}, status=status.HTTP_404_NOT_FOUND)
    language = request.query_params.get('language', 'en')
    completed = preg.anc_visits.count()
    schedule = get_anc_schedule(preg.lmp_date, completed)
    schedule['mother_name'] = preg.mother_name
    schedule['record_id'] = record_id
    schedule['danger_signs'] = get_danger_signs_list(language)
    return Response(schedule)


@api_view(['POST'])
@validate_request
def anc_visit_add(request, record_id):
    """Record an ANC visit."""
    try:
        preg = PregnancyRecord.objects.get(record_id=record_id)
    except PregnancyRecord.DoesNotExist:
        return Response({'error': 'Pregnancy record not found.'}, status=status.HTTP_404_NOT_FOUND)

    visit_num    = preg.anc_visits.count() + 1
    systolic, diastolic = validate_blood_pressure(
        request.data.get('bp_systolic'),
        request.data.get('bp_diastolic'),
    )
    ga           = gestational_age_weeks(preg.lmp_date)
    bp_alert     = None
    if systolic and diastolic:
        bp_alert = check_bp_danger(systolic, diastolic, ga)

    weight       = validate_weight(request.data.get('weight_kg'))
    visit_date   = validate_past_date(
        request.data.get('visit_date', str(date_type.today())),
        field='visit_date',
        required=False,
    )
    danger_signs = request.data.get('danger_signs', [])
    if not isinstance(danger_signs, list):
        raise ValidationError('danger_signs must be a list.', field='danger_signs')
    facility     = sanitize_optional_text(request.data.get('facility', ''), field='facility', max_length=200)
    notes        = sanitize_optional_text(request.data.get('notes', ''), field='notes', max_length=500)

    visit = ANCVisit.objects.create(
        pregnancy=preg,
        visit_number=visit_num,
        visit_date=visit_date,
        gestational_age_weeks=ga,
        weight_kg=weight,
        bp_systolic=systolic,
        bp_diastolic=diastolic,
        fundal_height_cm=request.data.get('fundal_height_cm'),
        fetal_heart_rate=request.data.get('fetal_heart_rate'),
        iron_folic_given=request.data.get('iron_folic_given', False),
        tt_vaccine_given=request.data.get('tt_vaccine_given', False),
        danger_signs=danger_signs,
        facility=facility,
        notes=notes,
    )
    return Response({'visit_id': visit.id, 'visit_number': visit_num, 'bp_alert': bp_alert}, status=status.HTTP_201_CREATED)


# ── HEW Checklists ────────────────────────────────────────────────────────────

@api_view(['GET'])
def hew_checklist_types(request):
    """List all available HEW checklist types."""
    return Response({'checklist_types': get_all_checklist_types()})


@api_view(['GET'])
def hew_checklist_get(request, visit_type):
    """Get a specific HEW checklist."""
    language = request.query_params.get('language', 'en')
    cl = get_checklist(visit_type, language)
    if not cl:
        return Response({'error': 'Checklist type not found.'}, status=status.HTTP_404_NOT_FOUND)
    return Response(cl)


@api_view(['POST'])
@validate_request
def hew_checklist_submit(request):
    """Submit a completed HEW checklist."""
    visit_type     = validate_visit_type(request.data.get('visit_type', ''))
    hew_name       = sanitize_optional_text(request.data.get('hew_name', ''), field='hew_name', max_length=100)
    kebele         = sanitize_optional_text(request.data.get('kebele', ''), field='kebele', max_length=100)
    household_id   = sanitize_optional_text(request.data.get('household_id', ''), field='household_id', max_length=50)
    visit_date     = validate_past_date(
        request.data.get('visit_date', str(date_type.today())),
        field='visit_date',
        required=False,
    )
    checklist_data = request.data.get('checklist_data', {})
    if not isinstance(checklist_data, dict):
        raise ValidationError('checklist_data must be an object.', field='checklist_data')
    action_taken   = sanitize_optional_text(request.data.get('action_taken', ''), field='action_taken', max_length=500)
    referral_reason = sanitize_optional_text(request.data.get('referral_reason', ''), field='referral_reason', max_length=500)

    checklist = HEWChecklist.objects.create(
        visit_type=visit_type,
        hew_name=hew_name,
        kebele=kebele,
        household_id=household_id,
        visit_date=visit_date,
        checklist_data=checklist_data,
        action_taken=action_taken,
        referral_needed=bool(request.data.get('referral_needed', False)),
        referral_reason=referral_reason,
    )
    return Response({'id': checklist.id, 'visit_type': checklist.visit_type}, status=status.HTTP_201_CREATED)


# ── Phase 3: SMS & Reminders ──────────────────────────────────────────────────
from core.sms_engine import send_sms, appointment_reminder_msg, vaccine_reminder_msg, anc_reminder_msg, medication_reminder_msg, danger_sign_alert_msg
from core.sms_chat import handle_inbound_sms
from .models import MedicationReminder, SMSLog


def _log_sms(direction, phone, message, status, message_id='', sms_type=''):
    try:
        SMSLog.objects.create(direction=direction, phone=phone, message=message[:500],
                              status=status, message_id=message_id, sms_type=sms_type)
    except Exception:
        pass


@api_view(['POST'])
@validate_request
def sms_inbound(request):
    """
    Receive inbound SMS from Africa's Talking webhook.
    AT posts: from, to, text, date, id
    """
    phone   = request.data.get('from', '') or request.POST.get('from', '')
    message = request.data.get('text', '') or request.POST.get('text', '')
    shortcode = request.data.get('to', '') or request.POST.get('to', '')

    phone   = validate_phone(phone, field='from', required=True)
    message = sanitize_text(message, field='text', max_length=500)

    _log_sms('inbound', phone, message, 'received', sms_type='chat')
    reply = handle_inbound_sms(phone, message, shortcode)
    _log_sms('outbound', phone, reply, 'sent', sms_type='chat')
    return Response({'status': 'ok', 'reply': reply})


@api_view(['POST'])
@validate_request
def sms_send(request):
    """
    Manually send an SMS.
    Body: { phone, message, sms_type }
    """
    phone    = validate_phone(request.data.get('phone', ''), field='phone', required=True)
    message  = sanitize_text(request.data.get('message', ''), field='message', max_length=500)
    sms_type = sanitize_optional_text(request.data.get('sms_type', 'manual'), field='sms_type', max_length=50, default='manual')
    result   = send_sms(phone, message)
    _log_sms('outbound', phone, message, result.get('status', 'unknown'),
             result.get('message_id', ''), sms_type)
    return Response(result)


@api_view(['POST'])
@validate_request
def reminder_subscribe(request):
    """
    Subscribe a patient to daily medication reminders.
    Body: { patient_name, phone, medication_name, condition, time_of_day, language, start_date, end_date }
    """
    patient_name    = sanitize_text(request.data.get('patient_name', ''), field='patient_name', max_length=100)
    phone           = validate_phone(request.data.get('phone', ''), field='phone', required=True)
    medication_name = sanitize_text(request.data.get('medication_name', ''), field='medication_name', max_length=200)
    condition       = sanitize_optional_text(request.data.get('condition', ''), field='condition', max_length=100)
    time_of_day     = validate_time_of_day(request.data.get('time_of_day', 'morning'))
    language        = validate_language(request.data.get('language', 'en'))
    start_date      = validate_date_string(
        request.data.get('start_date', str(date_type.today())),
        field='start_date', required=False,
    )
    end_date_raw    = request.data.get('end_date')
    end_date        = validate_date_string(end_date_raw, field='end_date', required=False, default=None) if end_date_raw else None

    reminder = MedicationReminder.objects.create(
        patient_name=patient_name,
        phone=phone,
        medication_name=medication_name,
        condition=condition,
        time_of_day=time_of_day,
        language=language,
        start_date=start_date,
        end_date=end_date,
        notes=sanitize_optional_text(request.data.get('notes', ''), field='notes', max_length=300),
    )
    # Send confirmation SMS
    msg = medication_reminder_msg(reminder.patient_name, reminder.medication_name,
                                   reminder.time_of_day, reminder.language)
    send_sms(reminder.phone, f"Subscribed to reminders. First reminder: {msg[:100]}")
    return Response({'id': reminder.id, 'patient_name': reminder.patient_name,
                     'medication_name': reminder.medication_name}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def reminder_unsubscribe(request, reminder_id):
    """Unsubscribe from a medication reminder."""
    try:
        reminder = MedicationReminder.objects.get(id=reminder_id)
        reminder.active = False
        reminder.save()
        return Response({'status': 'unsubscribed'})
    except MedicationReminder.DoesNotExist:
        return Response({'error': 'Reminder not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def reminder_list(request):
    """List medication reminders. Query param: phone"""
    phone = request.query_params.get('phone', '')
    qs = MedicationReminder.objects.filter(active=True)
    if phone:
        qs = qs.filter(phone__icontains=phone[-9:])
    data = list(qs.values('id', 'patient_name', 'phone', 'medication_name',
                           'time_of_day', 'language', 'start_date', 'end_date', 'active'))
    return Response({'reminders': data, 'count': len(data)})


@api_view(['POST'])
def send_appointment_reminder_now(request, appt_id):
    """Manually trigger appointment reminder SMS for a specific appointment."""
    try:
        appt = Appointment.objects.get(id=appt_id)
    except Appointment.DoesNotExist:
        return Response({'error': 'Appointment not found.'}, status=status.HTTP_404_NOT_FOUND)
    if not appt.patient_phone:
        return Response({'error': 'No phone number on appointment.'}, status=status.HTTP_400_BAD_REQUEST)
    msg = appointment_reminder_msg(appt.patient_name, appt.facility_name,
                                    str(appt.appointment_date), appt.language)
    result = send_sms(appt.patient_phone, msg)
    _log_sms('outbound', appt.patient_phone, msg, result.get('status', 'unknown'),
             result.get('message_id', ''), 'appointment')
    return Response(result)


@api_view(['POST'])
@validate_request
def send_danger_alert(request):
    """
    Send a danger sign alert SMS to a phone number.
    Body: { phone, name, sign, language }
    """
    phone    = validate_phone(request.data.get('phone', ''), field='phone', required=True)
    name     = sanitize_optional_text(request.data.get('name', 'Patient'), field='name', max_length=100, default='Patient')
    sign     = sanitize_text(request.data.get('sign', ''), field='sign', max_length=200)
    language = validate_language(request.data.get('language', 'en'))
    msg      = danger_sign_alert_msg(name, sign, language)
    result   = send_sms(phone, msg)
    _log_sms('outbound', phone, msg, result.get('status', 'unknown'),
             result.get('message_id', ''), 'danger_alert')
    return Response(result)


@api_view(['GET'])
def sms_log_list(request):
    """List SMS logs. Query params: phone, sms_type, direction"""
    qs = SMSLog.objects.order_by('-created_at')
    if request.query_params.get('phone'):
        qs = qs.filter(phone__icontains=request.query_params['phone'][-9:])
    if request.query_params.get('sms_type'):
        qs = qs.filter(sms_type=request.query_params['sms_type'])
    if request.query_params.get('direction'):
        qs = qs.filter(direction=request.query_params['direction'])
    data = list(qs[:100].values('id', 'direction', 'phone', 'message', 'status', 'sms_type', 'created_at'))
    return Response({'logs': data, 'count': len(data)})


# ── Phase 4: Analytics, Outbreak Detection & DHIS2 ───────────────────────────
from core.analytics_engine import full_dashboard, consultation_stats, growth_stats, vaccination_stats, pregnancy_stats, sms_stats
from core.outbreak_detector import get_all_alerts, detect_condition_spikes, get_disease_trend
from core.dhis2_reporter import build_dhis2_payload, push_to_dhis2, export_dhis2_json


@api_view(['GET'])
def analytics_dashboard(request):
    """Full analytics dashboard. Query param: days (default 30)"""
    days = int(request.query_params.get('days', 30))
    return Response(full_dashboard(days))


@api_view(['GET'])
def analytics_consultations(request):
    """Consultation stats with trends. Query param: days"""
    days = int(request.query_params.get('days', 30))
    return Response(consultation_stats(days))


@api_view(['GET'])
def analytics_growth(request):
    """Growth/nutrition stats. Query param: days"""
    days = int(request.query_params.get('days', 30))
    return Response(growth_stats(days))


@api_view(['GET'])
def analytics_vaccinations(request):
    """Vaccination coverage stats."""
    return Response(vaccination_stats())


@api_view(['GET'])
def analytics_pregnancies(request):
    """Pregnancy and ANC stats."""
    return Response(pregnancy_stats())


@api_view(['GET'])
def outbreak_alerts(request):
    """
    Run outbreak detection and return all active alerts.
    Query param: region (optional)
    """
    region = request.query_params.get('region')
    return Response(get_all_alerts(region))


@api_view(['GET'])
def disease_trend(request, condition_id):
    """
    Daily case trend for a specific condition.
    Query param: days (default 30)
    """
    days = int(request.query_params.get('days', 30))
    trend = get_disease_trend(condition_id, days)
    return Response({'condition_id': condition_id, 'days': days, 'trend': trend})


@api_view(['GET'])
def dhis2_export(request):
    """
    Export data in DHIS2 dataValueSet format (JSON).
    Query params: period (e.g. 202401), org_unit
    """
    period   = request.query_params.get('period')
    org_unit = request.query_params.get('org_unit')
    payload  = export_dhis2_json(period, org_unit)
    return Response(payload)


@api_view(['POST'])
def dhis2_push(request):
    """
    Push data to DHIS2 API.
    Body: { period, org_unit } — both optional
    """
    period   = request.data.get('period')
    org_unit = request.data.get('org_unit')
    payload  = build_dhis2_payload(period, org_unit)
    result   = push_to_dhis2(payload)
    return Response(result)


# ── Google Places: real-time nearby facility search ───────────────────────────
from core.places_engine import search_nearby_facilities

@api_view(['GET'])
@validate_request
def nearby_facilities_live(request):
    """
    Search for health facilities near GPS coordinates using Google Places API.
    Falls back to knowledge base if API key not set.
    Query params: lat, lon, radius_m (default 50000), facility_type
    """
    lat, lon = validate_coordinates(
        request.query_params.get('lat', ''),
        request.query_params.get('lon', ''),
    )
    radius_m      = validate_positive_integer(
        request.query_params.get('radius_m', 50000),
        field='radius_m', min_val=100, max_val=200000, default=50000,
    )
    facility_type = request.query_params.get('facility_type', '')
    result = search_nearby_facilities(lat, lon, radius_m, facility_type or None)
    return Response(result)


# ── TTS Proxy ─────────────────────────────────────────────────────────────────
import urllib.request
import urllib.parse
from django.http import HttpResponse as DjangoHttpResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_GET
def tts_proxy(request):
    """
    TTS proxy — uses ElevenLabs for realistic human voice.
    Falls back to Google Translate TTS if ElevenLabs key is not set.
    Usage: GET /api/v1/tts/?lang=am&text=ሰላም
    """
    text = request.GET.get('text', '').strip()
    lang = request.GET.get('lang', 'en').strip()

    if not text:
        return DjangoHttpResponse('text is required', status=400)

    text = text[:500]  # ElevenLabs supports longer text than Google TTS

    # ── Try ElevenLabs first ──────────────────────────────────────────────────
    elevenlabs_key   = os.environ.get('ELEVENLABS_API_KEY', '').strip()
    elevenlabs_voice = os.environ.get('ELEVENLABS_VOICE_ID', '21m00Tcm4TlvDq8ikWAM').strip()

    if elevenlabs_key:
        try:
            import json as _json
            el_url = f'https://api.elevenlabs.io/v1/text-to-speech/{elevenlabs_voice}'
            payload = _json.dumps({
                'text': text,
                'model_id': 'eleven_multilingual_v2',  # supports Amharic + other Ethiopian langs
                'voice_settings': {
                    'stability': 0.5,
                    'similarity_boost': 0.75,
                    'style': 0.0,
                    'use_speaker_boost': True,
                },
            }).encode('utf-8')

            req = urllib.request.Request(
                el_url,
                data=payload,
                headers={
                    'xi-api-key': elevenlabs_key,
                    'Content-Type': 'application/json',
                    'Accept': 'audio/mpeg',
                },
                method='POST',
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                audio_data = resp.read()

            response = DjangoHttpResponse(audio_data, content_type='audio/mpeg')
            response['Cache-Control'] = 'public, max-age=86400'
            response['Access-Control-Allow-Origin'] = '*'
            response['X-TTS-Provider'] = 'elevenlabs'
            return response

        except Exception as e:
            # Log and fall through to Google TTS fallback
            import logging
            logging.getLogger(__name__).warning(f'ElevenLabs TTS failed: {e}')

    # ── Fallback: Google Translate TTS ───────────────────────────────────────
    GTTS_SUPPORTED = {'en', 'am', 'ti', 'om', 'so'}
    gtts_lang = lang if lang in GTTS_SUPPORTED else 'am'
    text_short = text[:200]  # Google TTS limit

    url = (
        'https://translate.google.com/translate_tts'
        f'?ie=UTF-8&tl={gtts_lang}&q={urllib.parse.quote(text_short)}&client=tw-ob'
    )

    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0',
            'Referer': 'https://translate.google.com/',
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            audio_data = resp.read()

        response = DjangoHttpResponse(audio_data, content_type='audio/mpeg')
        response['Cache-Control'] = 'public, max-age=86400'
        response['Access-Control-Allow-Origin'] = '*'
        response['X-TTS-Provider'] = 'google'
        return response

    except Exception as e:
        return DjangoHttpResponse(f'TTS error: {e}', status=502)


# ── STT Proxy ─────────────────────────────────────────────────────────────────
import io
import tempfile
import os

@csrf_exempt
def stt_proxy(request):
    """
    Server-side speech-to-text fallback for browsers that don't support
    the Web Speech API (Firefox, Safari, older Android WebView).

    Accepts a POST with an audio file (WebM/OGG/WAV) and returns a transcript.
    Uses Google's free STT via the SpeechRecognition library — no API key needed.

    Usage: POST /api/v1/stt/
      Form field: audio (file), lang (e.g. 'en', 'am')
    Response: { transcript: "...", lang: "en" }
    """
    if request.method != 'POST':
        return DjangoHttpResponse('POST required', status=405)

    audio_file = request.FILES.get('audio')
    lang = request.POST.get('lang', 'en').strip()

    if not audio_file:
        return DjangoHttpResponse('audio file required', status=400)

    # Map app language codes to BCP-47 for Google STT
    LANG_MAP = {
        'en': 'en-US', 'am': 'am-ET', 'ti': 'ti-ET', 'om': 'om-ET',
    }
    bcp47 = LANG_MAP.get(lang, 'en-US')

    try:
        import speech_recognition as sr

        recognizer = sr.Recognizer()

        # Write uploaded audio to a temp file so SpeechRecognition can read it
        suffix = '.webm'
        content_type = audio_file.content_type or ''
        if 'wav' in content_type:
            suffix = '.wav'
        elif 'ogg' in content_type:
            suffix = '.ogg'
        elif 'mp4' in content_type or 'aac' in content_type:
            suffix = '.mp4'

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            for chunk in audio_file.chunks():
                tmp.write(chunk)
            tmp_path = tmp.name

        try:
            with sr.AudioFile(tmp_path) as source:
                audio_data = recognizer.record(source)
            transcript = recognizer.recognize_google(audio_data, language=bcp47)
            return DjangoHttpResponse(
                __import__('json').dumps({'transcript': transcript, 'lang': lang}),
                content_type='application/json',
                status=200,
            )
        except sr.UnknownValueError:
            return DjangoHttpResponse(
                __import__('json').dumps({'transcript': '', 'error': 'no_speech', 'lang': lang}),
                content_type='application/json',
                status=200,
            )
        except sr.RequestError as e:
            return DjangoHttpResponse(
                __import__('json').dumps({'transcript': '', 'error': 'stt_unavailable', 'detail': str(e), 'lang': lang}),
                content_type='application/json',
                status=502,
            )
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    except ImportError:
        return DjangoHttpResponse(
            __import__('json').dumps({'transcript': '', 'error': 'stt_not_installed'}),
            content_type='application/json',
            status=501,
        )
    except Exception as e:
        return DjangoHttpResponse(
            __import__('json').dumps({'transcript': '', 'error': 'server_error', 'detail': str(e)}),
            content_type='application/json',
            status=500,
        )
