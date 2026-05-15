"""Referral Tracker API views."""
import uuid
from datetime import date, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Referral
from core.sms_engine import send_sms
from .validators import (
    ValidationError, validate_request,
    sanitize_text, sanitize_optional_text,
    validate_phone, validate_date_string, validate_future_date,
)


@api_view(['GET'])
@validate_request
def referral_list(request):
    chw = sanitize_optional_text(request.query_params.get('chw', ''), field='chw', max_length=100)
    qs  = Referral.objects.order_by('expected_visit_date')
    if chw:
        qs = qs.filter(chw_identifier=chw)
    data = list(qs.values(
        'referral_id', 'patient_name', 'patient_phone', 'chw_identifier',
        'destination_facility', 'reason', 'referral_date', 'expected_visit_date',
        'status', 'outcome_notes', 'sms_reminder_sent', 'created_at'
    ))
    return Response({'referrals': data, 'count': len(data)})


@api_view(['POST'])
@validate_request
def referral_create(request):
    patient_identifier   = sanitize_text(request.data.get('patient_identifier', ''), field='patient_identifier', max_length=100)
    chw_identifier       = sanitize_text(request.data.get('chw_identifier', ''), field='chw_identifier', max_length=100)
    destination_facility = sanitize_text(request.data.get('destination_facility', ''), field='destination_facility', max_length=200)
    reason               = sanitize_text(request.data.get('reason', ''), field='reason', max_length=500)
    referral_date        = validate_date_string(request.data.get('referral_date'), field='referral_date', allow_future=False)
    expected_visit_date  = validate_future_date(request.data.get('expected_visit_date'), field='expected_visit_date')
    patient_name         = sanitize_optional_text(request.data.get('patient_name', ''), field='patient_name', max_length=100)
    patient_phone        = validate_phone(request.data.get('patient_phone', ''), field='patient_phone')

    ref_id = request.data.get('referral_id') or str(uuid.uuid4())[:8].upper()
    # Ensure unique
    while Referral.objects.filter(referral_id=ref_id).exists():
        ref_id = str(uuid.uuid4())[:8].upper()

    r = Referral.objects.create(
        referral_id=ref_id,
        patient_identifier=patient_identifier,
        patient_name=patient_name,
        patient_phone=patient_phone,
        chw_identifier=chw_identifier,
        destination_facility=destination_facility,
        reason=reason,
        referral_date=referral_date,
        expected_visit_date=expected_visit_date,
    )
    return Response({'referral_id': r.referral_id, 'status': r.status},
                    status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@validate_request
def referral_outcome(request, referral_id):
    try:
        r = Referral.objects.get(referral_id=referral_id)
    except Referral.DoesNotExist:
        return Response({'error': 'Referral not found.'}, status=status.HTTP_404_NOT_FOUND)

    from django.utils import timezone
    valid_statuses = {'open', 'attended', 'not_attended', 'admitted', 'discharged'}
    new_status = request.data.get('status', r.status)
    if new_status not in valid_statuses:
        raise ValidationError(
            f'status must be one of: {", ".join(sorted(valid_statuses))}.',
            field='status',
        )
    r.status = new_status
    r.outcome_notes = sanitize_optional_text(request.data.get('outcome_notes', ''), field='outcome_notes', max_length=500)
    r.outcome_recorded_at = timezone.now()
    r.save()
    return Response({'referral_id': r.referral_id, 'status': r.status})


@api_view(['GET'])
@validate_request
def referral_report(request):
    chw   = sanitize_optional_text(request.query_params.get('chw', ''), field='chw', max_length=100)
    month = request.query_params.get('month', '')  # YYYY-MM

    qs = Referral.objects.all()
    if chw:
        qs = qs.filter(chw_identifier=chw)
    if month:
        try:
            year, mon = month.split('-')
            qs = qs.filter(referral_date__year=int(year), referral_date__month=int(mon))
        except ValueError:
            raise ValidationError('month must be in YYYY-MM format (e.g. 2024-06).', field='month')

    total    = qs.count()
    attended = qs.filter(status='attended').count()
    rate     = round(attended / total * 100, 1) if total else 0

    from django.db.models import Count
    top_reasons = (qs.values('reason').annotate(count=Count('id'))
                     .order_by('-count')[:5])

    return Response({
        'chw': chw, 'month': month,
        'total_referrals': total,
        'attended': attended,
        'attendance_rate_pct': rate,
        'top_reasons': list(top_reasons),
    })
