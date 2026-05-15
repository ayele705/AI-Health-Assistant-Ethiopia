"""
Loads and queries the disease knowledge base from JSON.
"""
import json
from pathlib import Path
from django.conf import settings


_kb = None  # cached knowledge base


def load_kb() -> dict:
    global _kb
    if _kb is None:
        path = Path(settings.KNOWLEDGE_BASE_PATH)
        with open(path, 'r', encoding='utf-8') as f:
            _kb = json.load(f)
    return _kb


def get_all_conditions() -> list:
    return load_kb().get('conditions', [])


def get_condition_by_id(condition_id: str) -> dict | None:
    for c in get_all_conditions():
        if c['id'] == condition_id:
            return c
    return None


def get_health_tips(category: str = None, language: str = 'en') -> list:
    tips = load_kb().get('health_tips', [])
    if category:
        tips = [t for t in tips if t.get('category') == category]

    # Fallback chain: requested lang -> am -> en
    def get_field(tip, field):
        return (tip.get(f'{field}_{language}')
                or tip.get(f'{field}_am')
                or tip.get(f'{field}_en', ''))

    return [
        {
            'id': t['id'],
            'title': get_field(t, 'title'),
            'content': get_field(t, 'content'),
            'category': t['category'],
        }
        for t in tips
    ]


def get_facilities(region: str = None) -> list:
    facilities = load_kb().get('facilities', [])
    if region:
        facilities = [f for f in facilities if f.get('region', '').lower() == region.lower()]
    return facilities
