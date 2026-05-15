"""
DHIS2 integration — exports aggregated health data in DHIS2-compatible format.
Supports both direct API push (when DHIS2_URL configured) and JSON export.

DHIS2 is Ethiopia's national health information system (HMIS).
Data elements mapped to standard Ethiopia HMIS indicators.
"""
import logging
from datetime import date, timedelta
from django.conf import settings

logger = logging.getLogger(__name__)

# DHIS2 data element UIDs — mapped to Ethiopia HMIS standard codes
# These are example UIDs; replace with actual org-specific UIDs from your DHIS2 instance
DHIS2_DATA_ELEMENTS = {
    'malaria_cases':            'fbfJHSPpUQD',
    'malaria_deaths':           'cYeuwXTCPkU',
    'diarrhea_cases_under5':    'Jtf34kNZhzP',
    'pneumonia_cases_under5':   'hfdmMSPBgLG',
    'tb_new_cases':             'bX5QUIBgBhM',
    'hiv_tested':               'V37YqbqpEhV',
    'hiv_positive':             'ybzlGLjWwnK',
    'anc1_visits':              'UOlfIjgN8X6',
    'anc4_visits':              'OdiHJayrsKo',
    'skilled_delivery':         'vI2csg55S9C',
    'sam_cases':                'X8zyunlgZkI',
    'mam_cases':                'fClA2Erf6IO',
    'measles_vaccinated':       'l6byfWFUGaP',
    'dpt3_vaccinated':          'Y53DP9BQSB3',
    'fully_immunized_children': 'FTRrcoaog83',
    'maternal_deaths':          'O05mAByOgAv',
    'neonatal_deaths':          'tU7GixyHhsv',
    'outpatient_visits':        'fbfJHSPpUQD',
}


def build_dhis2_payload(period: str = None, org_unit: str = None) -> dict:
    """
    Build a DHIS2 dataValueSet payload from local data.
    period: DHIS2 period format e.g. '202401' (monthly) or '2024W01' (weekly)
    org_unit: DHIS2 organisation unit UID
    """
    if not period:
        today = date.today()
        period = f"{today.year}{today.month:02d}"  # e.g. 202401

    if not org_unit:
        org_unit = getattr(settings, 'DHIS2_ORG_UNIT', 'ImspTQPwCqd')

    from api.models import Consultation, GrowthRecord, VaccinationRecord, PregnancyRecord, ANCVisit
    from core.analytics_engine import get_date_range

    # Parse period to date range
    year = int(period[:4])
    month = int(period[4:6]) if len(period) >= 6 else date.today().month
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end = date(year, month + 1, 1) - timedelta(days=1)

    def count_condition(condition_id):
        count = 0
        for c in Consultation.objects.filter(created_at__date__gte=start, created_at__date__lte=end):
            result = c.assessment_result or {}
            if any(cond.get('id') == condition_id for cond in result.get('conditions', [])[:1]):
                count += 1
        return count

    data_values = [
        {'dataElement': DHIS2_DATA_ELEMENTS['malaria_cases'],          'value': count_condition('malaria')},
        {'dataElement': DHIS2_DATA_ELEMENTS['diarrhea_cases_under5'],  'value': count_condition('diarrhea')},
        {'dataElement': DHIS2_DATA_ELEMENTS['pneumonia_cases_under5'], 'value': count_condition('pneumonia')},
        {'dataElement': DHIS2_DATA_ELEMENTS['tb_new_cases'],           'value': count_condition('tuberculosis')},
        {'dataElement': DHIS2_DATA_ELEMENTS['hiv_tested'],             'value': count_condition('hiv_aids')},
        {'dataElement': DHIS2_DATA_ELEMENTS['sam_cases'],              'value': GrowthRecord.objects.filter(created_at__date__gte=start, created_at__date__lte=end, nutrition_status='SAM').count()},
        {'dataElement': DHIS2_DATA_ELEMENTS['mam_cases'],              'value': GrowthRecord.objects.filter(created_at__date__gte=start, created_at__date__lte=end, nutrition_status='MAM').count()},
        {'dataElement': DHIS2_DATA_ELEMENTS['anc1_visits'],            'value': ANCVisit.objects.filter(visit_date__gte=start, visit_date__lte=end, visit_number=1).count()},
        {'dataElement': DHIS2_DATA_ELEMENTS['anc4_visits'],            'value': ANCVisit.objects.filter(visit_date__gte=start, visit_date__lte=end, visit_number__gte=4).count()},
        {'dataElement': DHIS2_DATA_ELEMENTS['outpatient_visits'],      'value': Consultation.objects.filter(created_at__date__gte=start, created_at__date__lte=end).count()},
    ]

    return {
        'dataSet': getattr(settings, 'DHIS2_DATASET_UID', 'pBOMPrpg1QX'),
        'completeDate': date.today().isoformat(),
        'period': period,
        'orgUnit': org_unit,
        'dataValues': data_values,
    }


def push_to_dhis2(payload: dict) -> dict:
    """
    Push data to DHIS2 API.
    Returns result dict with status and response.
    Falls back to simulation if DHIS2_URL not configured.
    """
    dhis2_url = getattr(settings, 'DHIS2_URL', '')
    dhis2_user = getattr(settings, 'DHIS2_USERNAME', '')
    dhis2_pass = getattr(settings, 'DHIS2_PASSWORD', '')

    if not dhis2_url:
        logger.info(f"[DHIS2 SIMULATION] Would push {len(payload.get('dataValues', []))} data values for period {payload.get('period')}")
        return {
            'status': 'simulated',
            'message': 'DHIS2_URL not configured. Set DHIS2_URL, DHIS2_USERNAME, DHIS2_PASSWORD in .env to enable real push.',
            'payload_summary': {
                'period': payload.get('period'),
                'org_unit': payload.get('orgUnit'),
                'data_values_count': len(payload.get('dataValues', [])),
            }
        }

    try:
        import requests
        from requests.auth import HTTPBasicAuth
        url = f"{dhis2_url.rstrip('/')}/api/dataValueSets"
        resp = requests.post(url, json=payload, auth=HTTPBasicAuth(dhis2_user, dhis2_pass),
                             headers={'Content-Type': 'application/json'}, timeout=30)
        resp.raise_for_status()
        return {'status': 'success', 'http_status': resp.status_code, 'response': resp.json()}
    except Exception as e:
        logger.error(f"DHIS2 push failed: {e}")
        return {'status': 'error', 'error': str(e)}


def export_dhis2_json(period: str = None, org_unit: str = None) -> dict:
    """Build and return DHIS2 payload as JSON (for manual upload)."""
    payload = build_dhis2_payload(period, org_unit)
    return payload
