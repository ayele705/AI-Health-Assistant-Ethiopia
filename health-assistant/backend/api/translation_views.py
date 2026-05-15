"""
Translation API Views
=====================
Runtime translation endpoints for the hybrid translation system.

Endpoints:
  POST /api/v1/translate/              — translate one or more strings on-demand
  GET  /api/v1/translate/cache/        — cache statistics
  POST /api/v1/translate/cache/clear/  — clear cache (admin use)
  GET  /api/v1/translate/languages/    — list supported languages
"""

import os
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.translation_service import (
    translate,
    translate_batch,
    get_cache_stats,
    clear_cache,
    GOOGLE_LANG_MAP,
)

logger = logging.getLogger(__name__)

# Supported languages: en, am, om, ti only
LANGUAGE_INFO = {
    'en': {'name': 'English',  'native': 'English',     'flag': '', 'google_support': 'full'},
    'am': {'name': 'Amharic',  'native': 'አማርኛ',        'flag': '', 'google_support': 'full'},
    'om': {'name': 'Oromo',    'native': 'Afaan Oromoo', 'flag': '', 'google_support': 'full'},
    'ti': {'name': 'Tigrinya', 'native': 'ትግርኛ',        'flag': '', 'google_support': 'full'},
}


@api_view(['POST'])
def translate_text(request):
    """
    Translate one or more strings to a target language.

    Request body:
      {
        "text": "Hello",           // single string
        "texts": ["Hello", "..."], // OR list of strings
        "target_lang": "am",
        "source_lang": "en"        // optional, defaults to "en"
      }
    """
    data = request.data
    target_lang = data.get('target_lang', 'en')
    source_lang = data.get('source_lang', 'en')

    if target_lang not in LANGUAGE_INFO:
        return Response(
            {'error': f'Unsupported language: {target_lang}. Supported: {list(LANGUAGE_INFO.keys())}'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Single string
    if 'text' in data:
        text = data['text']
        if not isinstance(text, str):
            return Response({'error': '"text" must be a string'}, status=status.HTTP_400_BAD_REQUEST)
        result = translate(text, target_lang, source_lang)
        return Response({
            'translated': result,
            'target_lang': target_lang,
            'source_lang': source_lang,
            'api_available': bool(os.getenv('GOOGLE_TRANSLATE_API_KEY')),
        })

    # Batch strings
    if 'texts' in data:
        texts = data['texts']
        if not isinstance(texts, list):
            return Response({'error': '"texts" must be a list'}, status=status.HTTP_400_BAD_REQUEST)
        if len(texts) > 200:
            return Response({'error': 'Maximum 200 strings per request'}, status=status.HTTP_400_BAD_REQUEST)
        results = translate_batch(texts, target_lang, source_lang)
        return Response({
            'translations': results,
            'count': len(results),
            'target_lang': target_lang,
            'source_lang': source_lang,
            'api_available': bool(os.getenv('GOOGLE_TRANSLATE_API_KEY')),
        })

    return Response(
        {'error': 'Provide either "text" (string) or "texts" (list)'},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['GET'])
def translation_cache_stats(request):
    """Return translation cache statistics."""
    stats = get_cache_stats()
    stats['api_configured'] = bool(os.getenv('GOOGLE_TRANSLATE_API_KEY'))
    return Response(stats)


@api_view(['POST'])
def translation_cache_clear(request):
    """
    Clear translation cache.
    Optional body: { "lang": "am" } to clear only one language.
    """
    lang = request.data.get('lang')
    deleted = clear_cache(lang)
    return Response({
        'deleted': deleted,
        'lang': lang or 'all',
        'message': f'Cleared {deleted} cached translations',
    })


@api_view(['GET'])
def supported_translation_languages(request):
    """List all supported languages."""
    api_configured = bool(os.getenv('GOOGLE_TRANSLATE_API_KEY'))
    langs = [
        {
            'code': code,
            'name': info['name'],
            'native_name': info['native'],
            'flag': info['flag'],
            'google_support': info['google_support'],
            'google_code': GOOGLE_LANG_MAP.get(code, code),
            'translation_available': api_configured or code == 'en',
        }
        for code, info in LANGUAGE_INFO.items()
    ]
    return Response({
        'languages': langs,
        'count': len(langs),
        'api_configured': api_configured,
    })
