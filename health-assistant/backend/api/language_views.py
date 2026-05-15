"""
Language Pack Manager API views.
Serves downloadable language bundles for 8 Ethiopian languages.
"""
import os
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# Language pack metadata — sizes are approximate (bytes)
LANGUAGE_PACKS = {
    'en':  {'name': 'English',   'flag': '', 'size_bytes': 45000,  'audio_size_bytes': 1200000},
    'am':  {'name': 'Amharic',   'flag': '', 'size_bytes': 52000,  'audio_size_bytes': 1400000},
    'ti':  {'name': 'Tigrinya',  'flag': '', 'size_bytes': 50000,  'audio_size_bytes': 1350000},
    'om':  {'name': 'Oromo',     'flag': '', 'size_bytes': 51000,  'audio_size_bytes': 1380000},
    'sid': {'name': 'Sidama',    'flag': '', 'size_bytes': 48000,  'audio_size_bytes': 1250000},
    'so':  {'name': 'Somali',    'flag': '', 'size_bytes': 49000,  'audio_size_bytes': 1300000},
    'aa':  {'name': 'Afar',      'flag': '', 'size_bytes': 46000,  'audio_size_bytes': 1200000},
    'wal': {'name': 'Wolaytta',  'flag': '', 'size_bytes': 47000,  'audio_size_bytes': 1220000},
    'had': {'name': 'Hadiyya',   'flag': '', 'size_bytes': 46500,  'audio_size_bytes': 1210000},
}

DIALECT_VARIANTS = {
    'om': ['om-borana', 'om-harar'],
    'so': ['so-ogaden'],
}


@api_view(['GET'])
def language_pack_list(request):
    """List all available language packs with sizes."""
    packs = []
    for lang, meta in LANGUAGE_PACKS.items():
        packs.append({
            'lang': lang,
            'name': meta['name'],
            'flag': meta['flag'],
            'size_bytes': meta['size_bytes'],
            'audio_size_bytes': meta['audio_size_bytes'],
            'total_size_bytes': meta['size_bytes'] + meta['audio_size_bytes'],
            'dialects': DIALECT_VARIANTS.get(lang, []),
        })
    return Response({'language_packs': packs, 'count': len(packs)})


@api_view(['GET'])
def language_pack_bundle(request, lang):
    """Download the full language pack bundle (strings + audio index)."""
    if lang not in LANGUAGE_PACKS:
        return Response({'error': f'Language pack "{lang}" not found.'}, status=status.HTTP_404_NOT_FOUND)

    # In production this would serve a pre-built bundle file.
    # Here we return the metadata + placeholder strings structure.
    bundle = _build_bundle(lang)
    return Response(bundle)


@api_view(['GET'])
def language_pack_audio(request, lang):
    """Download the audio-only bundle index for a language."""
    if lang not in LANGUAGE_PACKS:
        return Response({'error': f'Language pack "{lang}" not found.'}, status=status.HTTP_404_NOT_FOUND)

    audio_index = _build_audio_index(lang)
    return Response(audio_index)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _build_bundle(lang):
    meta = LANGUAGE_PACKS[lang]
    return {
        'lang': lang,
        'name': meta['name'],
        'version': '1.0',
        'size_bytes': meta['size_bytes'],
        'strings': _get_strings(lang),
        'audio_index': _build_audio_index(lang),
        'dialects': DIALECT_VARIANTS.get(lang, []),
    }


def _build_audio_index(lang):
    categories = ['malaria', 'diarrhoea', 'maternal', 'nutrition', 'vaccination', 'hygiene']
    clips = []
    for i, cat in enumerate(categories, 1):
        for j in range(1, 4):  # 3 clips per category
            clips.append({
                'id': f'{lang}_{cat}_{j:02d}',
                'category': cat,
                'file': f'audio/{lang}/{cat}_{j:02d}.mp3',
                'duration_s': 30 + (i * 5),
                'size_bytes': 32000 * (30 + i * 5) // 8,  # ~32kbps estimate
            })
    return {
        'lang': lang,
        'version': '1.0',
        'clip_count': len(clips),
        'clips': clips,
    }


def _get_strings(lang):
    """Return UI strings for the given language (fallback to English)."""
    base = {
        'app_title': 'Health Assistant',
        'check_symptoms': 'Check Symptoms',
        'health_tips': 'Health Tips',
        'medications': 'Medications',
        'nearest_facility': 'Nearest Facility',
        'emergency': 'EMERGENCY',
        'visit_health_center': 'Visit Health Center',
        'self_care': 'Self Care',
        'offline': 'Offline',
        'syncing': 'Syncing...',
        'loading': 'Loading...',
        'safe_message': "I'm not sure — please contact your nearest health worker.",
    }
    translations = {
        'am': {
            'app_title': 'የጤና ረዳት',
            'check_symptoms': 'ምልክቶችን ያረጋግጡ',
            'health_tips': 'የጤና ምክሮች',
            'medications': 'መድሃኒቶች',
            'nearest_facility': 'ቅርብ ጤና ጣቢያ',
            'emergency': 'አስቸኳይ',
            'visit_health_center': 'ጤና ጣቢያ ይሂዱ',
            'self_care': 'ቤት ውስጥ እንክብካቤ',
            'offline': 'ከኢንተርኔት ውጭ',
            'syncing': 'በማስተባበር ላይ...',
            'loading': 'በመጫን ላይ...',
            'safe_message': 'እርግጠኛ አይደለሁም — ወደ ቅርብ ጤና ሠራተኛ ይሂዱ።',
        },
        'om': {
            'app_title': 'Gargaaraa Fayyaa',
            'check_symptoms': "Mallattoo Sakatta'i",
            'health_tips': 'Gorsa Fayyaa',
            'medications': 'Qorichaa',
            'nearest_facility': 'Buufata Fagoo Hin Taane',
            'emergency': 'Ariifachiisaa',
            'visit_health_center': 'Giddugala Fayyaa Deemi',
            'self_care': 'Kunuunsa Mana',
            'offline': 'Sarara Ala',
            'syncing': 'Walsimsiisaa...',
            'loading': "Fe'amaa jira...",
            'safe_message': 'Hin beeku — ogeessa fayyaa dhiyoo kee quunnamii.',
        },
        'ti': {
            'app_title': 'ሓጋዚ ጥዕና',
            'check_symptoms': 'ምልክታት ፈትሽ',
            'health_tips': 'ምኽሪ ጥዕና',
            'medications': 'መድሃኒታት',
            'nearest_facility': 'ቀረባ ጥዕና ጣቢያ',
            'emergency': 'ህጹጽ',
            'visit_health_center': 'ናብ ጥዕና ጣቢያ ኺድ',
            'self_care': 'ናይ ቤት ክንክን',
            'offline': 'ካብ ኢንተርነት ወጻኢ',
            'syncing': 'ይሰማማዕ ኣሎ...',
            'loading': 'ይጽዓን ኣሎ...',
            'safe_message': 'ርግጸኛ ኣይኮንኩን — ናብ ቀረባ ሰራሕተኛ ጥዕና ኺድ።',
        },
    }
    strings = dict(base)
    strings.update(translations.get(lang, {}))
    return strings
