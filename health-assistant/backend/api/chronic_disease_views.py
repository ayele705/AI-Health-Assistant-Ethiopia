"""Chronic Disease Management API views."""
from datetime import date as date_type
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from core.chronic_disease_engine import (
    assess_blood_pressure, assess_blood_glucose,
    get_adherence_reminder, get_chronic_disease_checklist
)
from .models import ChronicDiseaseRecord, ChronicDiseaseReading
from .validators import (
    ValidationError, validate_request,
    sanitize_text, sanitize_optional_text,
    validate_language, validate_phone,
    validate_blood_pressure, validate_glucose,
    validate_condition, validate_date_string,
)


@api_view(['GET'])
@validate_request
def chronic_patient_list(request):
    """List chronic disease patients. Query params: condition, kebele"""
    qs = ChronicDiseaseRecord.objects.order_by('-created_at')
    if request.query_params.get('condition'):
        qs = qs.filter(condition=request.query_params['condition'])
    if request.query_params.get('kebele'):
        qs = qs.filter(kebele=request.query_params['kebele'])
    data = list(qs.values('id', 'patient_identifier', 'patient_name', 'patient_phone',
                           'condition', 'kebele', 'medication_name', 'created_at'))
    return Response({'patients': data, 'count': len(data)})


@api_view(['POST'])
@validate_request
def chronic_patient_register(request):
    """Register a chronic disease patient."""
    import uuid
    condition       = validate_condition(request.data.get('condition', ''))
    patient_name    = sanitize_optional_text(request.data.get('patient_name', ''), field='patient_name', max_length=100)
    patient_phone   = validate_phone(request.data.get('patient_phone', ''), field='patient_phone')
    kebele          = sanitize_optional_text(request.data.get('kebele', ''), field='kebele', max_length=100)
    language        = validate_language(request.data.get('language', 'en'))
    medication_name = sanitize_optional_text(request.data.get('medication_name', ''), field='medication_name', max_length=200)

    p = ChronicDiseaseRecord.objects.create(
        patient_identifier=request.data.get('patient_identifier') or str(uuid.uuid4())[:8].upper(),
        patient_name=patient_name,
        patient_phone=patient_phone,
        condition=condition,
        kebele=kebele,
        language=language,
        medication_name=medication_name,
    )
    return Response({'id': p.id, 'patient_identifier': p.patient_identifier,
                     'condition': p.condition}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def chronic_readings_list(request, patient_id):
    """List readings for a chronic disease patient."""
    try:
        patient = ChronicDiseaseRecord.objects.get(patient_identifier=patient_id)
    except ChronicDiseaseRecord.DoesNotExist:
        return Response({'error': 'Patient not found.'}, status=status.HTTP_404_NOT_FOUND)
    readings = list(patient.readings.order_by('-reading_date').values(
        'id', 'reading_type', 'reading_date', 'systolic', 'diastolic',
        'glucose_mgdl', 'fasting', 'stage_or_status', 'urgent', 'notes', 'created_at'
    ))
    return Response({'patient_name': patient.patient_name, 'condition': patient.condition,
                     'readings': readings, 'count': len(readings)})


@api_view(['POST'])
@validate_request
def chronic_reading_add(request, patient_id):
    """Add a BP or glucose reading for a chronic disease patient."""
    try:
        patient = ChronicDiseaseRecord.objects.get(patient_identifier=patient_id)
    except ChronicDiseaseRecord.DoesNotExist:
        return Response({'error': 'Patient not found.'}, status=status.HTTP_404_NOT_FOUND)

    reading_type = request.data.get('reading_type', '')
    language     = validate_language(request.data.get('language', patient.language))
    reading_date = validate_date_string(
        request.data.get('reading_date', str(date_type.today())),
        field='reading_date', allow_future=False, required=False,
    )
    notes       = sanitize_optional_text(request.data.get('notes', ''), field='notes', max_length=500)
    recorded_by = sanitize_optional_text(request.data.get('recorded_by', ''), field='recorded_by', max_length=100)

    if reading_type == 'bp':
        systolic, diastolic = validate_blood_pressure(
            request.data.get('systolic'),
            request.data.get('diastolic'),
            required=True,
        )
        assessment = assess_blood_pressure(systolic, diastolic, language)
        reading = ChronicDiseaseReading.objects.create(
            patient=patient, reading_type='bp',
            reading_date=reading_date,
            systolic=systolic, diastolic=diastolic,
            stage_or_status=assessment['stage'],
            urgent=assessment['urgent'],
            notes=notes,
            recorded_by=recorded_by,
        )
        return Response({'id': reading.id, 'assessment': assessment}, status=status.HTTP_201_CREATED)

    elif reading_type == 'glucose':
        glucose  = validate_glucose(request.data.get('glucose_mgdl'), field='glucose_mgdl', required=True)
        fasting  = bool(request.data.get('fasting', True))
        assessment = assess_blood_glucose(glucose, fasting, language)
        reading = ChronicDiseaseReading.objects.create(
            patient=patient, reading_type='glucose',
            reading_date=reading_date,
            glucose_mgdl=glucose, fasting=fasting,
            stage_or_status=assessment['status'],
            urgent=assessment['urgent'],
            notes=notes,
            recorded_by=recorded_by,
        )
        return Response({'id': reading.id, 'assessment': assessment}, status=status.HTTP_201_CREATED)

    raise ValidationError('reading_type must be bp or glucose.', field='reading_type')


@api_view(['POST'])
@validate_request
def bp_assess(request):
    """
    Assess blood pressure reading.
    Body: { systolic: int, diastolic: int, language: str }
    """
    systolic, diastolic = validate_blood_pressure(
        request.data.get('systolic'),
        request.data.get('diastolic'),
        required=True,
    )
    language = validate_language(request.data.get('language', 'en'))
    return Response(assess_blood_pressure(systolic, diastolic, language))


@api_view(['POST'])
@validate_request
def glucose_assess(request):
    """
    Assess blood glucose reading.
    Body: { glucose_mgdl: float, fasting: bool, language: str }
    """
    glucose  = validate_glucose(request.data.get('glucose_mgdl'), field='glucose_mgdl', required=True)
    fasting  = bool(request.data.get('fasting', True))
    language = validate_language(request.data.get('language', 'en'))
    return Response(assess_blood_glucose(glucose, fasting, language))


@api_view(['GET'])
@validate_request
def adherence_reminder_view(request):
    """
    Get a medication adherence reminder message.
    Query params: medication, condition, language
    """
    medication = sanitize_text(request.query_params.get('medication', ''), field='medication', max_length=200)
    condition  = sanitize_optional_text(request.query_params.get('condition', ''), field='condition', max_length=100)
    language   = validate_language(request.query_params.get('language', 'en'))
    msg = get_adherence_reminder(medication, condition, language)
    return Response({'message': msg, 'medication': medication, 'condition': condition})


@api_view(['GET'])
@validate_request
def chronic_disease_checklist_view(request):
    """
    Get self-monitoring checklist for a chronic condition.
    Query params: condition (hypertension|diabetes), language
    """
    condition = validate_condition(request.query_params.get('condition', ''))
    language  = validate_language(request.query_params.get('language', 'en'))
    return Response(get_chronic_disease_checklist(condition, language))
