#!/usr/bin/env python
"""
Build-time Translation Generator
=================================
Run this script once (or whenever source strings change) to pre-translate
all app strings using Google Translate and save them to:
  frontend/src/i18n/translations.json   ← consumed by React
  backend/data/translations.json        ← loaded into SQLite cache at startup

Usage:
  cd health-assistant/backend
  python scripts/generate_translations.py

  # Translate only specific languages:
  python scripts/generate_translations.py --langs am,om,ti

  # Force re-translate even if cached:
  python scripts/generate_translations.py --force

Requirements:
  GOOGLE_TRANSLATE_API_KEY must be set in .env or environment.
"""

import os
import sys
import json
import argparse
import time
from pathlib import Path

# Allow importing from backend root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / '.env')

# ── All source strings to translate ──────────────────────────────────────────
# These are the canonical English strings used throughout the app.
# Add new strings here as the app grows.

SOURCE_STRINGS = {
    # ── Navigation ────────────────────────────────────────────────────────────
    "nav": {
        "Check Symptoms": "Check Symptoms",
        "Health Tips": "Health Tips",
        "Medications": "Medications",
        "Voice Input": "Voice Input",
        "Photo Check": "Photo Check",
        "Nearest Facility": "Nearest Facility",
        "All Facilities": "All Facilities",
        "Appointment": "Appointment",
        "Growth Monitor": "Growth Monitor",
        "Vaccines": "Vaccines",
        "Pregnancy": "Pregnancy",
        "HEW Tools": "HEW Tools",
        "TBA Tools": "TBA Tools",
        "Referrals": "Referrals",
        "Calendar": "Calendar",
        "SMS Reminders": "SMS Reminders",
        "Emergency": "Emergency",
        "Dashboard": "Dashboard",
        "Accessibility": "Accessibility",
        "Core": "Core",
        "Facilities": "Facilities",
        "Community Health": "Community Health",
        "Communication": "Communication",
        "Analytics & More": "Analytics & More",
    },

    # ── App shell ─────────────────────────────────────────────────────────────
    "app": {
        "Health Assistant": "Health Assistant",
        "For Rural Ethiopian Communities": "For Rural Ethiopian Communities",
        "Toggle menu": "Toggle menu",
        "Offline": "Offline",
        "Syncing...": "Syncing...",
        "Loading...": "Loading...",
        "Save": "Save",
        "Cancel": "Cancel",
        "Submit": "Submit",
        "Back": "Back",
        "Close": "Close",
        "Yes": "Yes",
        "No": "No",
        "Error": "Error",
        "Success": "Success",
        "Please try again": "Please try again",
    },

    # ── Chat / symptom checker ────────────────────────────────────────────────
    "chat": {
        "Hello! I'm your health assistant. What is your main symptom today?": "Hello! I'm your health assistant. What is your main symptom today?",
        "How long have you had this symptom? (e.g. 1 day, 3 days)": "How long have you had this symptom? (e.g. 1 day, 3 days)",
        "Do you have any other symptoms? (e.g. fever, cough, headache — or type 'no')": "Do you have any other symptoms? (e.g. fever, cough, headache — or type 'no')",
        "What is your age?": "What is your age?",
        "Are you male or female?": "Are you male or female?",
        "Type your message...": "Type your message...",
        "Send": "Send",
        "New Chat": "New Chat",
        "Speak": "Speak",
        "Stop listening": "Stop listening",
        "Thinking...": "Thinking...",
        "I'm not sure — please contact your nearest health worker or visit your local health center.": "I'm not sure — please contact your nearest health worker or visit your local health center.",
    },

    # ── Assessment results ────────────────────────────────────────────────────
    "assessment": {
        "Based on your symptoms": "Based on your symptoms",
        "Possible conditions": "Possible conditions",
        "Recommended action": "Recommended action",
        "EMERGENCY — Go to health facility NOW": "EMERGENCY — Go to health facility NOW",
        "Visit your nearest health center": "Visit your nearest health center",
        "Self-care at home": "Self-care at home",
        "Confidence": "Confidence",
        "Home care advice": "Home care advice",
        "Warning signs — seek help if": "Warning signs — seek help if",
    },

    # ── Health tips ───────────────────────────────────────────────────────────
    "tips": {
        "Health Tips": "Health Tips",
        "All": "All",
        "Malaria": "Malaria",
        "Diarrhoea": "Diarrhoea",
        "Nutrition": "Nutrition",
        "Maternal Health": "Maternal Health",
        "Vaccination": "Vaccination",
        "Hygiene": "Hygiene",
        "Play audio": "Play audio",
        "No tips available": "No tips available",
    },

    # ── Medications ───────────────────────────────────────────────────────────
    "medications": {
        "Search medications...": "Search medications...",
        "Dosage": "Dosage",
        "Side effects": "Side effects",
        "Warnings": "Warnings",
        "Available at": "Available at",
        "No medications found": "No medications found",
        "Prescription required": "Prescription required",
        "Over the counter": "Over the counter",
    },

    # ── Facilities ────────────────────────────────────────────────────────────
    "facilities": {
        "Search facilities...": "Search facilities...",
        "Distance": "Distance",
        "Open now": "Open now",
        "Closed": "Closed",
        "Phone": "Phone",
        "Get directions": "Get directions",
        "No facilities found": "No facilities found",
        "Health Center": "Health Center",
        "Hospital": "Hospital",
        "Clinic": "Clinic",
        "Health Post": "Health Post",
        "Finding your location...": "Finding your location...",
        "Location access denied": "Location access denied",
    },

    # ── Consent ───────────────────────────────────────────────────────────────
    "consent": {
        "Privacy & Consent": "Privacy & Consent",
        "I agree to use this service": "I agree to use this service",
        "I am a caregiver": "I am a caregiver",
        "Withdraw consent": "Withdraw consent",
        "This service provides general health information only. It is not a substitute for professional medical advice.": "This service provides general health information only. It is not a substitute for professional medical advice.",
        "Your data is stored locally and never shared without your consent.": "Your data is stored locally and never shared without your consent.",
    },

    # ── Emergency ─────────────────────────────────────────────────────────────
    "emergency": {
        "EMERGENCY": "EMERGENCY",
        "Call ambulance": "Call ambulance",
        "Call health worker": "Call health worker",
        "Emergency contacts": "Emergency contacts",
        "Send alert": "Send alert",
        "Alert sent": "Alert sent",
        "Go to nearest hospital immediately": "Go to nearest hospital immediately",
    },

    # ── Growth monitor ────────────────────────────────────────────────────────
    "growth": {
        "Child Growth Monitor": "Child Growth Monitor",
        "Weight (kg)": "Weight (kg)",
        "Height (cm)": "Height (cm)",
        "Age (months)": "Age (months)",
        "Normal": "Normal",
        "Moderate malnutrition": "Moderate malnutrition",
        "Severe malnutrition": "Severe malnutrition",
        "Record measurement": "Record measurement",
        "Growth chart": "Growth chart",
    },

    # ── Pregnancy ─────────────────────────────────────────────────────────────
    "pregnancy": {
        "Pregnancy Tracker": "Pregnancy Tracker",
        "Last menstrual period": "Last menstrual period",
        "Expected due date": "Expected due date",
        "Weeks pregnant": "Weeks pregnant",
        "ANC visit": "ANC visit",
        "Next visit due": "Next visit due",
        "Danger signs": "Danger signs",
        "Register pregnancy": "Register pregnancy",
    },

    # ── Vaccination ───────────────────────────────────────────────────────────
    "vaccines": {
        "Vaccination Tracker": "Vaccination Tracker",
        "Due": "Due",
        "Overdue": "Overdue",
        "Given": "Given",
        "Mark as given": "Mark as given",
        "Next vaccine": "Next vaccine",
        "Vaccination schedule": "Vaccination schedule",
    },

    # ── IVR / USSD ────────────────────────────────────────────────────────────
    "ivr": {
        "Welcome to Health Assistant. Press 1 for English.": "Welcome to Health Assistant. Press 1 for English.",
        "Select language: 1 English, 2 Amharic, 3 Oromo, 4 Tigrinya, 5 Sidamo.": "Select language: 1 English, 2 Amharic, 3 Oromo, 4 Tigrinya, 5 Sidamo.",
        "What is your main symptom? Press 1 Fever, 2 Cough, 3 Stomach pain, 4 Other. Press 0 to repeat.": "What is your main symptom? Press 1 Fever, 2 Cough, 3 Stomach pain, 4 Other. Press 0 to repeat.",
        "EMERGENCY. Go to a health facility NOW. Call your nearest hospital.": "EMERGENCY. Go to a health facility NOW. Call your nearest hospital.",
        "Thank you. Stay safe. Goodbye.": "Thank you. Stay safe. Goodbye.",
    },
}

# Flatten all source strings into a single list for translation
def _flatten(source: dict) -> list[str]:
    strings = []
    for section in source.values():
        strings.extend(section.keys())
    return list(dict.fromkeys(strings))  # deduplicate, preserve order


# ── Target languages ──────────────────────────────────────────────────────────
ALL_LANGS = ['am', 'om', 'ti', 'sid', 'so', 'aa', 'wal', 'had']

LANG_NAMES = {
    'am':  'Amharic',
    'om':  'Oromo',
    'ti':  'Tigrinya',
    'sid': 'Sidama',
    'so':  'Somali',
    'aa':  'Afar',
    'wal': 'Wolaytta',
    'had': 'Hadiyya',
}


def translate_all(langs: list[str], force: bool = False) -> dict:
    """Translate all source strings to all target languages."""
    # Import here so Django settings are loaded first
    from core.translation_service import translate_batch, _cache_get

    all_strings = _flatten(SOURCE_STRINGS)
    result = {}

    for lang in langs:
        print(f"\n[{LANG_NAMES.get(lang, lang)}] Translating {len(all_strings)} strings...")
        translated_map = {}

        # Split into cached and uncached
        to_translate = []
        for s in all_strings:
            if not force:
                cached = _cache_get(s, lang)
                if cached:
                    translated_map[s] = cached
                    continue
            to_translate.append(s)

        cached_count = len(all_strings) - len(to_translate)
        print(f"   {cached_count} from cache, {len(to_translate)} need API call")

        if to_translate:
            # Batch in chunks of 100 (Google API limit)
            chunk_size = 100
            for i in range(0, len(to_translate), chunk_size):
                chunk = to_translate[i:i + chunk_size]
                translations = translate_batch(chunk, lang)
                for src, tgt in zip(chunk, translations):
                    translated_map[src] = tgt
                if len(to_translate) > chunk_size:
                    time.sleep(0.2)  # be polite to the API

        result[lang] = translated_map
        print(f"   Done — {len(translated_map)} strings translated")

    return result


def save_outputs(translations: dict, force: bool = False) -> None:
    """Save translations to both frontend and backend output files."""
    backend_root = Path(__file__).resolve().parent.parent
    project_root = backend_root.parent

    # Backend JSON (loaded into SQLite cache at startup)
    backend_out = backend_root / 'data' / 'translations.json'
    existing = {}
    if backend_out.exists() and not force:
        with open(backend_out, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    existing.update(translations)
    with open(backend_out, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    print(f"\n Backend translations saved → {backend_out}")

    # Frontend JSON (imported by React TranslationContext)
    frontend_i18n = project_root / 'frontend' / 'src' / 'i18n'
    frontend_i18n.mkdir(parents=True, exist_ok=True)
    frontend_out = frontend_i18n / 'translations.json'
    with open(frontend_out, 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)
    print(f" Frontend translations saved → {frontend_out}")

    # Also write per-language files for lazy loading
    for lang, strings in existing.items():
        lang_file = frontend_i18n / f'{lang}.json'
        with open(lang_file, 'w', encoding='utf-8') as f:
            json.dump(strings, f, ensure_ascii=False, indent=2)
    print(f" Per-language files written to {frontend_i18n}/")


def main():
    parser = argparse.ArgumentParser(description='Generate translations for Health Assistant')
    parser.add_argument('--langs', default=','.join(ALL_LANGS),
                        help='Comma-separated language codes (default: all)')
    parser.add_argument('--force', action='store_true',
                        help='Re-translate even if cached')
    parser.add_argument('--stats', action='store_true',
                        help='Show cache stats and exit')
    args = parser.parse_args()

    if args.stats:
        from core.translation_service import get_cache_stats
        stats = get_cache_stats()
        print(json.dumps(stats, indent=2))
        return

    api_key = os.getenv('GOOGLE_TRANSLATE_API_KEY', '')
    if not api_key:
        print("️  WARNING: GOOGLE_TRANSLATE_API_KEY not set.")
        print("   Translations will use cache only. Set the key in .env to enable API calls.")
        print("   Get a key at: https://console.cloud.google.com → APIs → Cloud Translation API\n")

    langs = [l.strip() for l in args.langs.split(',') if l.strip()]
    invalid = [l for l in langs if l not in ALL_LANGS + ['en']]
    if invalid:
        print(f"Unknown language codes: {invalid}")
        print(f"Valid codes: {ALL_LANGS}")
        sys.exit(1)

    langs = [l for l in langs if l != 'en']  # skip English source

    print(f"Translating to: {', '.join(LANG_NAMES.get(l, l) for l in langs)}")
    print(f"Total source strings: {len(_flatten(SOURCE_STRINGS))}")

    translations = translate_all(langs, force=args.force)
    save_outputs(translations, force=args.force)

    print("\n Translation generation complete!")
    print("   Run this script again whenever you add new strings.")


if __name__ == '__main__':
    main()
