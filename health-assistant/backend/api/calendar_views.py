"""Community Calendar API views."""
from datetime import date, timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CalendarEvent, PersonalReminder
from core.sms_engine import send_sms


@api_view(['GET'])
def calendar_list(request):
    kebele = request.query_params.get('kebele', '')
    days   = int(request.query_params.get('days', 90))
    lang   = request.query_params.get('language', 'en')
    end    = date.today() + timedelta(days=days)

    qs = CalendarEvent.objects.filter(event_date__gte=date.today(), event_date__lte=end)
    if kebele:
        qs = qs.filter(kebele=kebele)
    qs = qs.order_by('event_date')

    title_key = f'title_{lang}' if lang in ('am', 'ti', 'om') else 'title_en'
    events = []
    for e in qs:
        events.append({
            'id': e.id, 'kebele': e.kebele, 'event_type': e.event_type,
            'event_date': str(e.event_date),
            'title': getattr(e, title_key, '') or e.title_en,
            'created_by': e.created_by,
        })
    return Response({'events': events, 'count': len(events)})


@api_view(['POST'])
def calendar_create(request):
    e = CalendarEvent.objects.create(
        kebele=request.data.get('kebele', ''),
        event_type=request.data.get('event_type', 'other'),
        event_date=request.data.get('event_date'),
        title_en=request.data.get('title_en', ''),
        title_am=request.data.get('title_am', ''),
        title_ti=request.data.get('title_ti', ''),
        title_om=request.data.get('title_om', ''),
        created_by=request.data.get('created_by', ''),
    )
    return Response({'id': e.id, 'event_type': e.event_type, 'event_date': str(e.event_date)},
                    status=status.HTTP_201_CREATED)


@api_view(['PUT'])
def calendar_update(request, event_id):
    try:
        e = CalendarEvent.objects.get(id=event_id)
    except CalendarEvent.DoesNotExist:
        return Response({'error': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)
    for field in ('event_type', 'event_date', 'title_en', 'title_am', 'title_ti', 'title_om'):
        if field in request.data:
            setattr(e, field, request.data[field])
    e.save()
    return Response({'id': e.id, 'updated': True})


@api_view(['POST'])
def calendar_remind(request, event_id):
    try:
        e = CalendarEvent.objects.get(id=event_id)
    except CalendarEvent.DoesNotExist:
        return Response({'error': 'Event not found.'}, status=status.HTTP_404_NOT_FOUND)

    from datetime import datetime
    remind_at = datetime.combine(e.event_date, datetime.min.time()) - timedelta(hours=24)
    r = PersonalReminder.objects.create(
        user_identifier=request.data.get('user_identifier', ''),
        calendar_event=e,
        phone=request.data.get('phone', ''),
        channel=request.data.get('channel', 'sms'),
        remind_at=remind_at,
    )
    return Response({'reminder_id': r.id, 'remind_at': r.remind_at.isoformat()},
                    status=status.HTTP_201_CREATED)
