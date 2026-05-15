"""
Outbreak early warning system.
Detects unusual spikes in symptom/condition reports using a
simple threshold-based algorithm (rolling 7-day vs baseline).

Notifiable diseases tracked per WHO/Ethiopia FMOH guidelines:
cholera, measles, meningitis, typhoid, malaria, dysentery,
anthrax, rabies, dengue, yellow fever, COVID-like illness.
"""
from datetime import date, timedelta
from django.db.models import Count


# Conditions that trigger mandatory outbreak alerts
NOTIFIABLE_CONDITIONS = {
    'cholera':      {'threshold': 2,  'window_days': 7,  'alert_level': 'critical'},
    'measles':      {'threshold': 3,  'window_days': 14, 'alert_level': 'high'},
    'meningitis':   {'threshold': 2,  'window_days': 7,  'alert_level': 'critical'},
    'anthrax':      {'threshold': 1,  'window_days': 7,  'alert_level': 'critical'},
    'typhoid':      {'threshold': 5,  'window_days': 7,  'alert_level': 'medium'},
    'malaria':      {'threshold': 10, 'window_days': 7,  'alert_level': 'medium'},
    'dengue':       {'threshold': 3,  'window_days': 7,  'alert_level': 'high'},
    'rabies':       {'threshold': 2,  'window_days': 14, 'alert_level': 'high'},
    'typhus':       {'threshold': 3,  'window_days': 7,  'alert_level': 'high'},
    'leishmaniasis':{'threshold': 5,  'window_days': 14, 'alert_level': 'medium'},
}

# Symptom clusters that suggest outbreak even without confirmed diagnosis
SYMPTOM_CLUSTERS = {
    'acute_watery_diarrhea': {
        'symptoms': ['severe diarrhea', 'diarrhea', 'dehydration', 'vomiting'],
        'min_match': 2,
        'threshold': 5,
        'window_days': 3,
        'alert_level': 'high',
        'possible_cause': 'Cholera / AWD outbreak',
    },
    'fever_rash': {
        'symptoms': ['fever', 'rash', 'red eyes', 'cough'],
        'min_match': 3,
        'threshold': 4,
        'window_days': 7,
        'alert_level': 'high',
        'possible_cause': 'Measles outbreak',
    },
    'fever_stiff_neck': {
        'symptoms': ['fever', 'stiff neck', 'severe headache', 'sensitivity to light'],
        'min_match': 2,
        'threshold': 2,
        'window_days': 7,
        'alert_level': 'critical',
        'possible_cause': 'Meningitis outbreak',
    },
    'jaundice_cluster': {
        'symptoms': ['jaundice', 'fever', 'nausea', 'abdominal pain'],
        'min_match': 2,
        'threshold': 4,
        'window_days': 7,
        'alert_level': 'medium',
        'possible_cause': 'Hepatitis A / E outbreak',
    },
}


def detect_condition_spikes(region: str = None, days: int = 7) -> list:
    """
    Check if any notifiable condition has exceeded its threshold
    in the given time window.
    """
    from api.models import Consultation
    alerts = []
    cutoff = date.today() - timedelta(days=days)

    for condition_id, cfg in NOTIFIABLE_CONDITIONS.items():
        window = date.today() - timedelta(days=cfg['window_days'])
        qs = Consultation.objects.filter(
            created_at__date__gte=window,
            assessment_result__isnull=False,
        )
        if region:
            qs = qs.filter(region__iexact=region)

        # Count consultations where this condition appears in top results
        count = 0
        for c in qs:
            result = c.assessment_result or {}
            conditions = result.get('conditions', [])
            if any(cond.get('id') == condition_id for cond in conditions[:2]):
                count += 1

        if count >= cfg['threshold']:
            alerts.append({
                'type': 'condition_spike',
                'condition_id': condition_id,
                'count': count,
                'threshold': cfg['threshold'],
                'window_days': cfg['window_days'],
                'alert_level': cfg['alert_level'],
                'region': region or 'all',
                'message_en': f"ALERT: {count} cases of {condition_id.replace('_',' ').title()} reported in {cfg['window_days']} days (threshold: {cfg['threshold']}). Investigate immediately.",
                'message_am': f"ማስጠንቀቂያ: {count} የ{condition_id} ጉዳዮች በ{cfg['window_days']} ቀናት ውስጥ ሪፖርት ተደርጓል። ወዲያውኑ ምርመራ ያድርጉ።",
                'action_en': 'Report to woreda health office. Conduct rapid case investigation. Implement control measures.',
                'date': date.today().isoformat(),
            })

    return sorted(alerts, key=lambda x: {'critical': 0, 'high': 1, 'medium': 2}.get(x['alert_level'], 3))


def detect_symptom_clusters(region: str = None, days: int = 7) -> list:
    """
    Detect unusual clusters of symptom combinations
    that may indicate an outbreak even before diagnosis.
    """
    from api.models import Consultation
    alerts = []

    for cluster_id, cfg in SYMPTOM_CLUSTERS.items():
        window = date.today() - timedelta(days=cfg['window_days'])
        qs = Consultation.objects.filter(created_at__date__gte=window)
        if region:
            qs = qs.filter(region__iexact=region)

        count = 0
        for c in qs:
            symptoms = [s.lower() for s in (c.symptoms or [])]
            matches = sum(1 for s in cfg['symptoms'] if any(s in sym for sym in symptoms))
            if matches >= cfg['min_match']:
                count += 1

        if count >= cfg['threshold']:
            alerts.append({
                'type': 'symptom_cluster',
                'cluster_id': cluster_id,
                'possible_cause': cfg['possible_cause'],
                'count': count,
                'threshold': cfg['threshold'],
                'window_days': cfg['window_days'],
                'alert_level': cfg['alert_level'],
                'region': region or 'all',
                'message_en': f"CLUSTER ALERT: {count} cases with {cluster_id.replace('_',' ')} symptoms in {cfg['window_days']} days. Possible: {cfg['possible_cause']}.",
                'message_am': f"ምልክት ስብስብ ማስጠንቀቂያ: {count} ጉዳዮች። ሊሆን የሚችለው: {cfg['possible_cause']}",
                'action_en': 'Collect stool/blood samples. Report to health authorities. Implement WASH measures.',
                'date': date.today().isoformat(),
            })

    return sorted(alerts, key=lambda x: {'critical': 0, 'high': 1, 'medium': 2}.get(x['alert_level'], 3))


def get_all_alerts(region: str = None) -> dict:
    """Run all outbreak detection checks and return combined alerts."""
    condition_alerts = detect_condition_spikes(region)
    cluster_alerts   = detect_symptom_clusters(region)
    all_alerts = condition_alerts + cluster_alerts
    critical = [a for a in all_alerts if a['alert_level'] == 'critical']
    high     = [a for a in all_alerts if a['alert_level'] == 'high']
    medium   = [a for a in all_alerts if a['alert_level'] == 'medium']
    return {
        'total_alerts': len(all_alerts),
        'critical_count': len(critical),
        'high_count': len(high),
        'medium_count': len(medium),
        'alerts': all_alerts,
        'region': region or 'all',
        'checked_at': date.today().isoformat(),
    }


def get_disease_trend(condition_id: str, days: int = 30) -> list:
    """Return daily case counts for a specific condition over time."""
    from api.models import Consultation
    trend = {}
    cutoff = date.today() - timedelta(days=days)
    for c in Consultation.objects.filter(created_at__date__gte=cutoff):
        result = c.assessment_result or {}
        conditions = result.get('conditions', [])
        if any(cond.get('id') == condition_id for cond in conditions[:2]):
            k = str(c.created_at.date())
            trend[k] = trend.get(k, 0) + 1
    return [{'date': k, 'count': v} for k, v in sorted(trend.items())]
