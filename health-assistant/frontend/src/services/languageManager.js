/**
 * languageManager.js — Downloads, stores, and serves Language Packs.
 * Falls back to Amharic (audio) / English (text) when pack not downloaded.
 */

import { dbPut, dbGet, STORES } from './offlineStore';

const BASE = '/api/v1';

// Supported languages with fallback chain
export const SUPPORTED_LANGUAGES = ['en', 'am', 'ti', 'om'];
export const AUDIO_FALLBACK_LANG  = 'am';
export const TEXT_FALLBACK_LANG   = 'en';

// ── Download ──────────────────────────────────────────────────────────────────

/** Fetch available language packs with sizes from the backend. */
export async function fetchAvailablePacks() {
  const res  = await fetch(`${BASE}/language-packs/`);
  const data = await res.json();
  return data.language_packs || [];
}

/**
 * Download and store a full language pack bundle.
 * @param {string} lang
 * @param {function} onProgress - called with { loaded, total } bytes
 */
export async function downloadLanguagePack(lang, onProgress) {
  const res  = await fetch(`${BASE}/language-packs/${lang}/bundle/`);
  if (!res.ok) throw new Error(`Failed to download language pack: ${lang}`);
  const data = await res.json();
  await dbPut(STORES.LANGUAGE_PACKS, {
    lang,
    version:       data.version,
    strings:       data.strings,
    audio_index:   data.audio_index,
    downloaded_at: new Date().toISOString(),
  });
  if (onProgress) onProgress({ loaded: data.size_bytes, total: data.size_bytes });
  return data;
}

/** Download audio-only bundle for a language. */
export async function downloadAudioBundle(lang) {
  const res  = await fetch(`${BASE}/language-packs/${lang}/audio/`);
  if (!res.ok) throw new Error(`Failed to download audio bundle: ${lang}`);
  return res.json();
}

// ── Retrieval ─────────────────────────────────────────────────────────────────

/** Get a stored language pack from IndexedDB. Returns null if not downloaded. */
export async function getStoredPack(lang) {
  return dbGet(STORES.LANGUAGE_PACKS, lang);
}

/** Check if a language pack is downloaded. */
export async function isPackDownloaded(lang) {
  const pack = await getStoredPack(lang);
  return !!pack;
}

/**
 * Get a UI string for the given language.
 * Falls back to English text if pack not downloaded.
 */
export async function getString(key, lang) {
  const pack = await getStoredPack(lang);
  if (pack?.strings?.[key]) return pack.strings[key];

  // Fallback to English
  const fallback = await getStoredPack(TEXT_FALLBACK_LANG);
  return fallback?.strings?.[key] || key;
}

/**
 * Get the audio clip index for a language.
 * Falls back to Amharic audio if pack not downloaded.
 */
export async function getAudioIndex(lang) {
  const pack = await getStoredPack(lang);
  if (pack?.audio_index) return pack.audio_index;

  // Fallback to Amharic audio
  const fallback = await getStoredPack(AUDIO_FALLBACK_LANG);
  return fallback?.audio_index || null;
}

/**
 * Get dialect variants for a language.
 */
export async function getDialects(lang) {
  const packs = await fetchAvailablePacks().catch(() => []);
  const pack  = packs.find((p) => p.lang === lang);
  return pack?.dialects || [];
}

// ── Language selector helpers ─────────────────────────────────────────────────

/** Get display name for a language code. */
export function getLanguageName(lang) {
  const names = {
    en: 'English', am: 'አማርኛ', ti: 'ትግርኛ', om: 'Afaan Oromoo',
  };
  return names[lang] || lang;
}

/** Get flag emoji for a language code. */
export function getLanguageFlag(lang) {
  const flags = {
    en: '', am: '', ti: '', om: '',
  };
  return flags[lang] || '';
}
