"""
Hybrid Translation Service
==========================
Strategy:
  1. Check in-memory cache (fastest)
  2. Check SQLite translation cache (fast, offline)
  3. Call Google Cloud Translation API (online, costs money)
  4. Fall back to hardcoded strings in localization.py (always available)

Supported languages:
  en  → English
  am  → Amharic
  om  → Oromo
  ti  → Tigrinya
"""

import os
import json
import hashlib
import sqlite3
import logging
from pathlib import Path
from typing import Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# ── Google language code mapping ──────────────────────────────────────────────
GOOGLE_LANG_MAP = {
    'en': 'en',
    'am': 'am',
    'om': 'om',
    'ti': 'ti',
}

# Cache DB path — stored alongside the backend
_CACHE_DB = Path(__file__).resolve().parent.parent / 'data' / 'translation_cache.db'
_CACHE_DB.parent.mkdir(parents=True, exist_ok=True)

# In-memory cache: (text_hash, lang) -> translated_text
_memory_cache: dict = {}


# ── Database setup ────────────────────────────────────────────────────────────

def _get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(str(_CACHE_DB))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS translations (
            text_hash   TEXT NOT NULL,
            source_lang TEXT NOT NULL DEFAULT 'en',
            target_lang TEXT NOT NULL,
            source_text TEXT NOT NULL,
            translated   TEXT NOT NULL,
            provider     TEXT NOT NULL DEFAULT 'google',
            created_at   TEXT NOT NULL,
            PRIMARY KEY (text_hash, target_lang)
        )
    """)
    conn.execute("""
        CREATE INDEX IF NOT EXISTS idx_translations_lang
        ON translations (target_lang)
    """)
    conn.commit()
    return conn


def _text_hash(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


# ── Cache read/write ──────────────────────────────────────────────────────────

def _cache_get(text: str, target_lang: str) -> Optional[str]:
    key = (_text_hash(text), target_lang)
    if key in _memory_cache:
        return _memory_cache[key]
    try:
        conn = _get_db()
        row = conn.execute(
            "SELECT translated FROM translations WHERE text_hash=? AND target_lang=?",
            key
        ).fetchone()
        conn.close()
        if row:
            _memory_cache[key] = row[0]
            return row[0]
    except Exception as e:
        logger.warning(f"Translation cache read error: {e}")
    return None


def _cache_set(text: str, target_lang: str, translated: str, provider: str = 'google') -> None:
    key = (_text_hash(text), target_lang)
    _memory_cache[key] = translated
    try:
        conn = _get_db()
        conn.execute("""
            INSERT OR REPLACE INTO translations
                (text_hash, target_lang, source_text, translated, provider, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (key[0], target_lang, text, translated, provider, datetime.utcnow().isoformat()))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.warning(f"Translation cache write error: {e}")


# ── Google Translate API call ─────────────────────────────────────────────────

def _call_google_translate(text: str, target_lang: str, source_lang: str = 'en') -> Optional[str]:
    """
    Call Google Cloud Translation API v2 (Basic).
    Requires GOOGLE_TRANSLATE_API_KEY in environment.
    """
    api_key = os.getenv('GOOGLE_TRANSLATE_API_KEY', '')
    if not api_key:
        logger.debug("GOOGLE_TRANSLATE_API_KEY not set — skipping API call")
        return None

    google_target = GOOGLE_LANG_MAP.get(target_lang, target_lang)
    google_source = GOOGLE_LANG_MAP.get(source_lang, source_lang)

    try:
        import requests
        resp = requests.post(
            'https://translation.googleapis.com/language/translate/v2',
            params={'key': api_key},
            json={
                'q': text,
                'source': google_source,
                'target': google_target,
                'format': 'text',
            },
            timeout=5,
        )
        resp.raise_for_status()
        data = resp.json()
        translated = data['data']['translations'][0]['translatedText']
        logger.info(f"Google Translate: '{text[:40]}...' → [{target_lang}]")
        return translated
    except Exception as e:
        logger.warning(f"Google Translate API error for lang={target_lang}: {e}")
        return None


# ── Public API ────────────────────────────────────────────────────────────────

def translate(
    text: str,
    target_lang: str,
    source_lang: str = 'en',
    fallback: Optional[str] = None,
) -> str:
    """
    Translate text to target_lang using the hybrid strategy:
      1. Memory cache
      2. SQLite cache
      3. Google Translate API (if key configured)
      4. fallback string (if provided)
      5. Original text (last resort)
    """
    if not text or not text.strip():
        return text

    if target_lang == source_lang or target_lang == 'en':
        return text

    # 1 & 2 — caches
    cached = _cache_get(text, target_lang)
    if cached:
        return cached

    if result:
        _cache_set(text, target_lang, result)
        return result

    # 4 — caller-provided fallback
    if fallback:
        return fallback

    # 5 — return original
    return text


def translate_batch(
    texts: list[str],
    target_lang: str,
    source_lang: str = 'en',
) -> list[str]:
    """
    Translate a list of strings. Uses cache for already-translated items,
    batches uncached items into a single Google API call.
    """
    if target_lang == source_lang or target_lang == 'en':
        return texts

    results = [None] * len(texts)
    uncached_indices = []
    uncached_texts = []

    for i, text in enumerate(texts):
        cached = _cache_get(text, target_lang)
        if cached:
            results[i] = cached
        else:
            uncached_indices.append(i)
            uncached_texts.append(text)

    if not uncached_texts:
        return results

    api_key = os.getenv('GOOGLE_TRANSLATE_API_KEY', '')
    if not api_key:
        for i, idx in enumerate(uncached_indices):
            results[idx] = texts[idx]
        return results

    google_target = GOOGLE_LANG_MAP.get(target_lang, target_lang)
    google_source = GOOGLE_LANG_MAP.get(source_lang, source_lang)

    try:
        import requests
        resp = requests.post(
            'https://translation.googleapis.com/language/translate/v2',
            params={'key': api_key},
            json={
                'q': uncached_texts,
                'source': google_source,
                'target': google_target,
                'format': 'text',
            },
            timeout=10,
        )
        resp.raise_for_status()
        translations = resp.json()['data']['translations']

        for i, (idx, translated_obj) in enumerate(zip(uncached_indices, translations)):
            translated = translated_obj['translatedText']
            results[idx] = translated
            _cache_set(texts[idx], target_lang, translated)

    except Exception as e:
        logger.warning(f"Google Translate batch error for lang={target_lang}: {e}")
        for idx in uncached_indices:
            results[idx] = texts[idx]

    return results


def get_cache_stats() -> dict:
    """Return stats about the translation cache."""
    try:
        conn = _get_db()
        total = conn.execute("SELECT COUNT(*) FROM translations").fetchone()[0]
        by_lang = conn.execute(
            "SELECT target_lang, COUNT(*) FROM translations GROUP BY target_lang"
        ).fetchall()
        by_provider = conn.execute(
            "SELECT provider, COUNT(*) FROM translations GROUP BY provider"
        ).fetchall()
        conn.close()
        return {
            'total_cached': total,
            'by_language': dict(by_lang),
            'by_provider': dict(by_provider),
            'memory_cache_size': len(_memory_cache),
        }
    except Exception as e:
        return {'error': str(e)}


def clear_cache(target_lang: Optional[str] = None) -> int:
    """Clear translation cache. Returns number of rows deleted."""
    global _memory_cache
    try:
        conn = _get_db()
        if target_lang:
            cursor = conn.execute(
                "DELETE FROM translations WHERE target_lang=?", (target_lang,)
            )
            _memory_cache = {k: v for k, v in _memory_cache.items() if k[1] != target_lang}
        else:
            cursor = conn.execute("DELETE FROM translations")
            _memory_cache = {}
        conn.commit()
        deleted = cursor.rowcount
        conn.close()
        return deleted
    except Exception as e:
        logger.error(f"Cache clear error: {e}")
        return 0


def load_static_translations(json_path: str) -> int:
    """
    Bulk-load pre-built translations from a JSON file into the cache.
    JSON format: { "lang": { "source_text": "translated_text", ... }, ... }
    Returns number of entries loaded.
    """
    count = 0
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for lang, strings in data.items():
            for source, translated in strings.items():
                if source and translated and source != translated:
                    _cache_set(source, lang, translated, provider='static')
                    count += 1
        logger.info(f"Loaded {count} static translations from {json_path}")
    except Exception as e:
        logger.error(f"Failed to load static translations: {e}")
    return count
