import React, { createContext, useContext, useState, useEffect } from 'react';

const AccessibilityContext = createContext(null);

const STORAGE_KEY = 'ha_a11y_prefs';

const DEFAULTS = {
  highContrast: false,
  largeText: false,
  simpleMode: false,
  screenReader: false,
  voiceInput: false,
  textToSpeech: false,
  hearingMode: false,
  lang: 'en',
};

export function AccessibilityProvider({ children }) {
  const [prefs, setPrefs] = useState(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        // Always reset screenReader to false on load — prevents stale state causing visual bugs
        return { ...DEFAULTS, ...parsed, screenReader: false };
      }
      return DEFAULTS;
    } catch {
      return DEFAULTS;
    }
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(prefs));
    const root = document.documentElement;
    root.classList.toggle('high-contrast', prefs.highContrast);
    root.classList.toggle('large-text', prefs.largeText);
    root.classList.toggle('simple-mode', prefs.simpleMode);
    root.classList.toggle('screen-reader-mode', prefs.screenReader);
    root.classList.toggle('hearing-mode', prefs.hearingMode);
    // Font size for large text
    root.style.fontSize = prefs.largeText ? '120%' : '';
  }, [prefs]);

  const update = (key, value) => setPrefs(p => ({ ...p, [key]: value }));
  const toggle = (key) => setPrefs(p => ({ ...p, [key]: !p[key] }));

  return (
    <AccessibilityContext.Provider value={{ prefs, update, toggle }}>
      {children}
    </AccessibilityContext.Provider>
  );
}

export function useAccessibility() {
  return useContext(AccessibilityContext);
}
