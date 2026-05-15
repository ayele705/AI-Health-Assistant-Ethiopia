/**
 * TranslationContext — Hybrid Translation System
 * ================================================
 * Strategy (in order):
 *   1. Pre-built static JSON (loaded at startup, works offline)
 *   2. In-memory runtime cache (strings translated this session)
 *   3. Backend /api/v1/translate/ endpoint (calls Google Translate, caches result)
 *   4. Original English text (last resort)
 *
 * Re-render safety:
 *   - All mutable state (cache, in-flight set, batch queue) lives in refs
 *   - setRuntimeCache is only called once per unique string, after fetch resolves
 *   - flushBatch and translateAsync never appear in useCallback dep arrays
 *   - t() never triggers a state update during render
 */

import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
  useRef,
} from 'react';

const TranslationContext = createContext(null);

const FULL_SUPPORT_LANGS = new Set(['en', 'am', 'om', 'ti']);
const BATCH_DELAY_MS = 200;
const BATCH_SIZE = 50;

export function TranslationProvider({ children, initialLang = 'en' }) {
  const [lang, setLangState]         = useState(initialLang);
  const [staticStrings, setStaticStrings] = useState({});
  // runtimeCache lives in BOTH a ref (for sync reads) and state (to trigger re-render after fetch)
  const runtimeCacheRef  = useRef({});
  const [, forceUpdate]  = useState(0); // used to re-render after new translations arrive

  const loadedLangsRef   = useRef(new Set(['en']));
  const inFlightRef      = useRef(new Set());
  const pendingQueueRef  = useRef([]);
  const batchTimerRef    = useRef(null);
  const staticStringsRef = useRef({});

  // Keep ref in sync with state so flushBatch can read it without deps
  useEffect(() => {
    staticStringsRef.current = staticStrings;
  }, [staticStrings]);

  // ── Load static translations for a language ──────────────────────────────
  const loadStaticLang = useCallback(async (targetLang) => {
    if (targetLang === 'en' || loadedLangsRef.current.has(targetLang)) return;
    loadedLangsRef.current.add(targetLang); // mark immediately to prevent duplicate loads

    try {
      const module = await import(`./${targetLang}.json`).catch(() => null);
      if (module?.default) {
        setStaticStrings(prev => ({ ...prev, [targetLang]: module.default }));
        return;
      }
    } catch { /* no per-language file */ }

    try {
      const module = await import('./translations.json').catch(() => null);
      if (module?.default?.[targetLang]) {
        setStaticStrings(prev => ({ ...prev, [targetLang]: module.default[targetLang] }));
      }
    } catch { /* no combined file either */ }
  }, []); // stable — uses only refs

  useEffect(() => {
    if (lang !== 'en') loadStaticLang(lang);
  }, [lang, loadStaticLang]);

  // ── Batch API flush — reads from refs, no state deps ─────────────────────
  const flushBatch = useCallback((targetLang) => {
    const queue = pendingQueueRef.current.splice(0, BATCH_SIZE);
    if (!queue.length) return;

    const texts = queue.map(item => item.text);

    fetch('/api/v1/translate/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ texts, target_lang: targetLang, source_lang: 'en' }),
    })
      .then(r => r.ok ? r.json() : Promise.reject(r.status))
      .then(data => {
        const translations = data.translations || [];
        let hasNew = false;
        translations.forEach((translated, i) => {
          const key = `${targetLang}:${texts[i]}`;
          if (translated && translated !== texts[i] && !runtimeCacheRef.current[key]) {
            runtimeCacheRef.current[key] = translated;
            hasNew = true;
          }
          queue[i]?.resolve(translated || texts[i]);
        });
        // Only trigger one re-render for the whole batch
        if (hasNew) forceUpdate(n => n + 1);
      })
      .catch(() => {
        queue.forEach(item => item.resolve(item.text));
      })
      .finally(() => {
        // Flush remaining items if any were queued while this batch ran
        if (pendingQueueRef.current.length > 0) {
          batchTimerRef.current = setTimeout(() => flushBatch(targetLang), BATCH_DELAY_MS);
        }
      });
  }, []); // stable — uses only refs

  // ── Async translate (used by external callers) ────────────────────────────
  const translateAsync = useCallback((text, targetLang) => {
    return new Promise((resolve) => {
      if (!text || targetLang === 'en') { resolve(text); return; }

      const key = `${targetLang}:${text}`;

      // Static strings
      const staticMap = staticStringsRef.current[targetLang];
      if (staticMap?.[text]) { resolve(staticMap[text]); return; }

      // Runtime cache ref (no state read)
      if (runtimeCacheRef.current[key]) { resolve(runtimeCacheRef.current[key]); return; }

      // Queue for batch
      pendingQueueRef.current.push({ text, resolve });
      if (batchTimerRef.current) clearTimeout(batchTimerRef.current);
      batchTimerRef.current = setTimeout(() => flushBatch(targetLang), BATCH_DELAY_MS);
    });
  }, [flushBatch]); // flushBatch is stable

  // ── Synchronous t() — NEVER triggers state updates during render ──────────
  const t = useCallback((text) => {
    if (!text || lang === 'en') return text;

    // 1. Static pre-built
    const staticMap = staticStringsRef.current[lang];
    if (staticMap?.[text]) return staticMap[text];

    // 2. Runtime cache ref (sync, no state read)
    const key = `${lang}:${text}`;
    if (runtimeCacheRef.current[key]) return runtimeCacheRef.current[key];

    // 3. Queue async fetch — only once per unique string
    if (!inFlightRef.current.has(key)) {
      inFlightRef.current.add(key);
      translateAsync(text, lang).then(translated => {
        inFlightRef.current.delete(key);
        // translateAsync already wrote to runtimeCacheRef and called forceUpdate
      }).catch(() => {
        inFlightRef.current.delete(key);
      });
    }

    return text; // return original while waiting — no setState here
  }, [lang, translateAsync]);
  // Note: lang changes invalidate t() correctly; staticStrings changes are
  // handled via staticStringsRef so they don't need to be in deps.

  // ── tObj helper ───────────────────────────────────────────────────────────
  const tObj = useCallback((obj) => {
    if (lang === 'en') return obj;
    const result = {};
    for (const [key, value] of Object.entries(obj)) {
      result[key] = typeof value === 'string' ? t(value) : value;
    }
    return result;
  }, [lang, t]);

  const setLang = useCallback((newLang) => {
    setLangState(newLang);
    if (newLang !== 'en') loadStaticLang(newLang);
  }, [loadStaticLang]);

  const value = {
    lang,
    setLang,
    t,
    tObj,
    translateAsync,
    isTranslating: false, // no longer tracked as state to avoid re-renders
    loadedLangs: loadedLangsRef.current,
    hasStaticTranslations: (targetLang) => loadedLangsRef.current.has(targetLang),
    isFullySupportedLang: (targetLang) => FULL_SUPPORT_LANGS.has(targetLang),
  };

  return (
    <TranslationContext.Provider value={value}>
      {children}
    </TranslationContext.Provider>
  );
}

export function useTranslation() {
  const ctx = useContext(TranslationContext);
  if (!ctx) throw new Error('useTranslation must be used inside <TranslationProvider>');
  return ctx;
}

export default TranslationContext;
