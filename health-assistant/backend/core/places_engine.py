"""
Health facility search using OpenStreetMap Overpass API.
Completely free, no API key needed, real data for Ethiopia.
Falls back to knowledge base if network unavailable.
"""
import urllib.request
import urllib.parse
import json
import logging
from core.geolocation import haversine_km

logger = logging.getLogger(__name__)

OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]

# OSM amenity tags for health facilities
HEALTH_AMENITIES = ['hospital', 'clinic', 'health_post', 'doctors',
                    'pharmacy', 'nursing_home', 'dentist']

FACILITY_TYPE_MAP = {
    'hospital':     'hospital',
    'clinic':       'health_center',
    'health_post':  'health_post',
    'doctors':      'health_center',
    'pharmacy':     'pharmacy',
    'nursing_home': 'health_center',
    'dentist':      'health_center',
}


def search_nearby_facilities(lat: float, lon: float,
                              radius_m: int = 50000,
                              facility_type: str = None) -> dict:
    """
    Search for health facilities near GPS coordinates using OpenStreetMap.
    No API key required. Falls back to knowledge base if offline.
    """
    try:
        results = _overpass_search(lat, lon, radius_m)
        facilities = _parse_results(results, lat, lon, facility_type)
        if facilities:
            return {
                'facilities': facilities,
                'source': 'openstreetmap',
                'count': len(facilities),
                'note': f'Real-time data from OpenStreetMap — {len(facilities)} facilities found'
            }
        # OSM returned nothing — fall back to KB
        return _kb_fallback(lat, lon, facility_type, 'No OSM results in this area')
    except Exception as e:
        logger.warning(f"Overpass API error: {e}")
        return _kb_fallback(lat, lon, facility_type, str(e))


def _overpass_search(lat: float, lon: float, radius_m: int) -> list:
    """Query Overpass API for health amenities within radius. Tries multiple servers."""
    amenity_filter = '|'.join(HEALTH_AMENITIES)
    query = f'[out:json][timeout:15];(node["amenity"~"{amenity_filter}"](around:{radius_m},{lat},{lon});way["amenity"~"{amenity_filter}"](around:{radius_m},{lat},{lon});node["healthcare"](around:{radius_m},{lat},{lon});way["healthcare"](around:{radius_m},{lat},{lon}););out center tags;'
    data = urllib.parse.urlencode({'data': query}).encode()
    last_err = None
    for url in OVERPASS_URLS:
        try:
            req = urllib.request.Request(url, data=data,
                                          headers={'User-Agent': 'EthiopiaHealthAssistant/1.0'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read().decode()).get('elements', [])
        except Exception as e:
            last_err = e
            logger.warning(f"Overpass server {url} failed: {e}")
            continue
    raise Exception(f"All Overpass servers failed: {last_err}")


def _parse_results(elements: list, user_lat: float,
                   user_lon: float, filter_type: str = None) -> list:
    """Convert OSM elements to our facility format."""
    facilities = []
    seen = set()

    for el in elements:
        tags = el.get('tags', {})
        name = tags.get('name') or tags.get('name:en') or tags.get('name:am', '')
        if not name:
            continue

        # Get coordinates
        if el.get('type') == 'node':
            lat = el.get('lat')
            lon = el.get('lon')
        else:
            center = el.get('center', {})
            lat = center.get('lat')
            lon = center.get('lon')
        if lat is None or lon is None:
            continue

        # Deduplicate by name+coords
        key = f"{name}_{round(lat,3)}_{round(lon,3)}"
        if key in seen:
            continue
        seen.add(key)

        # Determine facility type
        amenity    = tags.get('amenity', '')
        healthcare = tags.get('healthcare', '')
        raw_type   = amenity or healthcare or 'clinic'
        ftype      = FACILITY_TYPE_MAP.get(raw_type, 'health_center')

        # Override with name hints
        name_lower = name.lower()
        if 'hospital' in name_lower or 'ሆስፒታል' in name:
            ftype = 'hospital'
        elif 'referral' in name_lower or 'specialized' in name_lower:
            ftype = 'referral_hospital'
        elif 'health post' in name_lower or 'ጤና ኬላ' in name:
            ftype = 'health_post'
        elif 'health center' in name_lower or 'ጤና ጣቢያ' in name:
            ftype = 'health_center'

        if filter_type and ftype != filter_type:
            continue

        dist = haversine_km(user_lat, user_lon, lat, lon)

        # Build services list from OSM tags
        services = _build_services(tags, ftype)

        facilities.append({
            'id':            f"osm_{el.get('type','n')}_{el.get('id','')}",
            'name':          name,
            'name_am':       tags.get('name:am', ''),
            'facility_type': ftype,
            'region':        tags.get('addr:region', tags.get('addr:city', 'Ethiopia')),
            'woreda':        tags.get('addr:district', ''),
            'phone':         tags.get('phone', tags.get('contact:phone', '')),
            'latitude':      lat,
            'longitude':     lon,
            'distance_km':   round(dist, 1),
            'services':      services,
            'hew_available': False,
            'source':        'openstreetmap',
            'opening_hours': tags.get('opening_hours', ''),
            'operator':      tags.get('operator', ''),
            'beds':          tags.get('beds', ''),
            'emergency':     tags.get('emergency', ''),
            'distance_note_en': f'{round(dist,1)} km from your location',
            'distance_note_am': f'ከእርስዎ አካባቢ {round(dist,1)} ኪሎሜትር',
        })

    facilities.sort(key=lambda x: x['distance_km'])
    return facilities


def _build_services(tags: dict, ftype: str) -> list:
    services = []
    if ftype in ('hospital', 'referral_hospital'):
        services += ['Emergency', 'OPD', 'Surgery', 'Laboratory']
    elif ftype == 'health_center':
        services += ['OPD', 'ANC', 'Immunization', 'Family planning']
    elif ftype == 'health_post':
        services += ['Immunization', 'ANC', 'ORS distribution', 'Health education']
    elif ftype == 'pharmacy':
        services += ['Pharmacy', 'Medications']
    if tags.get('emergency') == 'yes':
        if 'Emergency' not in services:
            services.insert(0, 'Emergency')
    if tags.get('healthcare:speciality'):
        services.append(tags['healthcare:speciality'].replace(';', ', '))
    return services or ['OPD']


def _kb_fallback(lat, lon, facility_type, reason):
    from core.geolocation import find_nearest_facilities
    facs = find_nearest_facilities(lat, lon, facility_type=facility_type)
    return {
        'facilities': facs,
        'source': 'knowledge_base',
        'count': len(facs),
        'note': f'Showing offline knowledge base ({reason})'
    }
