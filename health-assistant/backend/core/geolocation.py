"""
Geolocation utilities — Haversine distance and nearest facility finder.
"""
import math
from .knowledge_base import get_facilities


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return distance in km between two lat/lon points."""
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def find_nearest_facilities(user_lat: float, user_lon: float,
                             radius_km: float = None,
                             facility_type: str = None,
                             limit: int = 50) -> list:
    """Return ALL facilities sorted by distance from user. No radius cutoff by default."""
    results = []
    for f in get_facilities():
        lat = f.get('latitude')
        lon = f.get('longitude')
        if lat is None or lon is None:
            continue
        if facility_type and f.get('facility_type') != facility_type:
            continue
        dist = haversine_km(user_lat, user_lon, lat, lon)
        if radius_km is not None and dist > radius_km:
            continue
        results.append({**f, 'distance_km': round(dist, 1)})
    results.sort(key=lambda x: x['distance_km'])
    return results[:limit]
