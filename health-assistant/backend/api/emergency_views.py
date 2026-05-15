"""Emergency Contact and Alert API views."""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import EmergencyContact, EmergencyAlertLog
from core.emergency_engine import send_emergency_alerts
from .validators import (
    ValidationError, validate_request,
    sanitize_text, sanitize_optional_text,
    validate_phone, validate_language, validate_urgency,
)


@api_view(['GET'])
@validate_request
def contact_list(request):
    user_id = sanitize_optional_text(request.query_params.get('user_identifier', ''), field='user_identifier', max_length=100)
    qs = EmergencyContact.objects.filter(user_identifier=user_id)
    data = list(qs.values('id', 'name', 'phone', 'relationship', 'created_at'))
    return Response({'contacts': data, 'count': len(data)})


@api_view(['POST'])
@validate_request
def contact_create(request):
    user_id = sanitize_text(request.data.get('user_identifier', ''), field='user_identifier', max_length=100)
    name    = sanitize_text(request.data.get('name', ''), field='name', max_length=100)
    phone   = validate_phone(request.data.get('phone', ''), field='phone', required=True)
    relationship = sanitize_optional_text(request.data.get('relationship', ''), field='relationship', max_length=50)

    # Enforce max 5 contacts
    existing = EmergencyContact.objects.filter(user_identifier=user_id).count()
    if existing >= 5:
        return Response({'error': 'Maximum 5 emergency contacts allowed.'},
                        status=status.HTTP_400_BAD_REQUEST)

    c = EmergencyContact.objects.create(
        user_identifier=user_id,
        name=name,
        phone=phone,
        relationship=relationship,
    )
    return Response({'id': c.id, 'name': c.name, 'phone': c.phone},
                    status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def contact_delete(request, contact_id):
    try:
        c = EmergencyContact.objects.get(id=contact_id)
        c.delete()
        return Response({'status': 'deleted'})
    except EmergencyContact.DoesNotExist:
        return Response({'error': 'Contact not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@validate_request
def send_alert(request):
    user_id   = sanitize_text(request.data.get('user_identifier', ''), field='user_identifier', max_length=100)
    condition = sanitize_text(request.data.get('condition_summary', ''), field='condition_summary', max_length=500)
    urgency   = validate_urgency(request.data.get('urgency_level', 'emergency'))
    location  = sanitize_optional_text(request.data.get('location_text', ''), field='location_text', max_length=200)
    language  = validate_language(request.data.get('language', 'en'))

    result = send_emergency_alerts(user_id, condition, urgency, location, language)
    return Response(result)
