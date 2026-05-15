"""
Analytics engine — aggregates consultation, growth, vaccination,
and pregnancy data into dashboard KPIs and trend data.
"""
from datetime import date, timedelta
from django.db.models import Count, Q
from django.utils import timezone


def get_date_range(days: int = 30):
    end = date.today()
    start = end - timedelta(days=days)
    return start, end


def consultation_stats(days: int = 30) -> dict:
    from api.models import Consultation
    start, end = get_date_range(days)
    qs = Consultation.objects.filter(created_at__date__gte=start)
    total = qs.count()
    by_urgency = dict(qs.values_list('urgency_level').annotate(n=Count('id')).values_list('urgency_level', 'n'))
    by_language = dict(qs.values_list('language').annotate(n=Count('id')).values_list('language', 'n'))
    by_region   = dict(qs.exclude(region='').values_list('region').annotate(n=Count('id')).values_list('region', 'n'))

    # Top symptoms across all consultations
    symptom_counts = {}
    for c in qs.values_list('symptoms', flat=True):
        for s in (c or []):
            symptom_counts[s] = symptom_counts.get(s, 0) + 1
    top_symptoms = sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    # Daily trend
    daily = {}
    for c in qs.values_list('created_at__date', flat=True):
        k = str(c)
        daily[k] = daily.get(k, 0) + 1
    daily_trend = [{'date': k, 'count': v} for k, v in sorted(daily.items())]

    return {
        'total': total,
        'period_days': days,
        'by_urgency': by_urgency,
        'by_language': by_language,
        'by_region': by_region,
        'top_symptoms': [{'symptom': s, 'count': c} for s, c in top_symptoms],
        'daily_trend': daily_trend,
        'emergency_count': by_urgency.get('emergency', 0),
        'self_care_count': by_urgency.get('self_care', 0),
        'health_center_count': by_urgency.get('visit_health_center', 0),
    }


def growth_stats(days: int = 30) -> dict:
    from api.models import GrowthRecord
    start, _ = get_date_range(days)
    qs = GrowthRecord.objects.filter(created_at__date__gte=start)
    total = qs.count()
    by_status = dict(qs.values_list('nutrition_status').annotate(n=Count('id')).values_list('nutrition_status', 'n'))
    sam_count = by_status.get('SAM', 0)
    mam_count = by_status.get('MAM', 0)
    normal_count = by_status.get('normal', 0)
    sam_pct = round(sam_count / total * 100, 1) if total else 0
    mam_pct = round(mam_count / total * 100, 1) if total else 0
    return {
        'total_measurements': total,
        'sam_count': sam_count,
        'mam_count': mam_count,
        'normal_count': normal_count,
        'sam_percent': sam_pct,
        'mam_percent': mam_pct,
        'acute_malnutrition_percent': round((sam_count + mam_count) / total * 100, 1) if total else 0,
    }


def vaccination_stats() -> dict:
    from api.models import Child, VaccinationRecord
    from core.vaccine_schedule import get_vaccine_schedule
    total_children = Child.objects.count()
    fully_vaccinated = 0
    overdue_any = 0
    for child in Child.objects.all():
        given_ids = list(child.vaccinations.values_list('vaccine_id', flat=True))
        sched = get_vaccine_schedule(child.date_of_birth, given_ids)
        if sched['completion_percent'] == 100:
            fully_vaccinated += 1
        if sched['alert']:
            overdue_any += 1
    return {
        'total_children': total_children,
        'fully_vaccinated': fully_vaccinated,
        'overdue_any_vaccine': overdue_any,
        'coverage_percent': round(fully_vaccinated / total_children * 100, 1) if total_children else 0,
    }


def pregnancy_stats() -> dict:
    from api.models import PregnancyRecord, ANCVisit
    active = PregnancyRecord.objects.filter(status='active').count()
    total  = PregnancyRecord.objects.count()
    anc4_plus = 0
    for preg in PregnancyRecord.objects.filter(status__in=['active', 'delivered']):
        if preg.anc_visits.count() >= 4:
            anc4_plus += 1
    return {
        'active_pregnancies': active,
        'total_pregnancies': total,
        'anc4_plus_count': anc4_plus,
        'anc4_plus_percent': round(anc4_plus / total * 100, 1) if total else 0,
    }


def appointment_stats(days: int = 30) -> dict:
    from api.models import Appointment
    start, _ = get_date_range(days)
    qs = Appointment.objects.filter(created_at__date__gte=start)
    by_status = dict(qs.values_list('status').annotate(n=Count('id')).values_list('status', 'n'))
    return {
        'total': qs.count(),
        'pending': by_status.get('pending', 0),
        'confirmed': by_status.get('confirmed', 0),
        'cancelled': by_status.get('cancelled', 0),
    }


def sms_stats(days: int = 30) -> dict:
    from api.models import SMSLog
    start, _ = get_date_range(days)
    qs = SMSLog.objects.filter(created_at__date__gte=start)
    by_type = dict(qs.values_list('sms_type').annotate(n=Count('id')).values_list('sms_type', 'n'))
    by_status = dict(qs.values_list('status').annotate(n=Count('id')).values_list('status', 'n'))
    return {
        'total_sent': qs.filter(direction='outbound').count(),
        'total_received': qs.filter(direction='inbound').count(),
        'by_type': by_type,
        'by_status': by_status,
    }


def full_dashboard(days: int = 30) -> dict:
    """Aggregate all stats for the main dashboard."""
    return {
        'period_days': days,
        'generated_at': date.today().isoformat(),
        'consultations': consultation_stats(days),
        'growth': growth_stats(days),
        'vaccinations': vaccination_stats(),
        'pregnancies': pregnancy_stats(),
        'appointments': appointment_stats(days),
        'sms': sms_stats(days),
    }
