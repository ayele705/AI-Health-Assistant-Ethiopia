import React, { useState } from 'react';
import { useAccessibility } from '../AccessibilityContext';

const LANG_OPTIONS = [
  { code: 'en', label: 'English' },
  { code: 'am', label: 'አማርኛ (Amharic)' },
  { code: 'om', label: 'Oromoo' },
  { code: 'ti', label: 'ትግርኛ (Tigrinya)' },
];

const A11Y_T = {
  en: { title: 'Accessibility Settings', lang: 'Language', contrast: 'High Contrast', large: 'Large Text', simple: 'Simple Mode', screen: 'Screen Reader Mode (Blind)', tts: 'Read Responses Aloud', voice: 'Voice Input (For Blind)', hearing: 'Hearing Impairment Mode', close: 'Close' },
  am: { title: 'የተደራሽነት ቅንብሮች', lang: 'ቋንቋ', contrast: 'ከፍተኛ ንፅፅር', large: 'ትልቅ ጽሑፍ', simple: 'ቀላል ሁነታ', screen: 'ስክሪን አንባቢ ሁነታ (ዕውሮች)', tts: 'ምላሾችን ጮክ ብሎ አንብብ', voice: 'የድምፅ ግቤት (ለዕውሮች)', hearing: 'ለመስማት የተሳናቸው ሁነታ', close: 'ዝጋ' },
  ti: { title: 'ቅንብሪ ተደራሽነት', lang: 'ቋንቋ', contrast: 'ልዑል ንፅፅር', large: 'ዓቢ ጽሑፍ', simple: 'ቀሊል ሁነታ', screen: 'ኣንባቢ ስክሪን (ዕዉራት)', tts: 'መልስታት ጮኽ ኢልካ ኣንብብ', voice: 'ናይ ድምጺ ምእታው (ዕዉራት)', hearing: 'ሁነታ ዘይሰምዑ', close: 'ዕጸው' },
  om: { title: 'Qindaa\'ina Argamummaa', lang: 'Afaan', contrast: "Garaagarummaa Ol'aanaa", large: 'Barreeffama Guddaa', simple: 'Haala Salphaa', screen: 'Dubbisaa Iskiriinii (Jaamaa)', tts: 'Deebii Dhageeffadhu', voice: 'Galchituu Sagalee (Jaamaa)', hearing: 'Haala Gurra Dhagahuu Dadhabuu', close: 'Cufii' },
};

export default function AccessibilityToolbar({ lang, setLang }) {
  const { prefs, toggle } = useAccessibility();
  const [open, setOpen] = useState(false);
  const t = A11Y_T[lang] || A11Y_T['en'];

  return (
    <div className="a11y-toolbar-wrapper">
      <div className="a11y-btn-container">
        <button
          className="a11y-toggle-btn"
          onClick={() => setOpen(o => !o)}
          aria-expanded={open}
          aria-label="Accessibility options"
          title="Accessibility options"
        >
        </button>
        <span className="a11y-btn-label">Accessibility</span>
      </div>

      {open && (
        <div className="a11y-panel" role="dialog" aria-label="Accessibility settings">
          <p className="a11y-panel-title">{t.title}</p>

          <label className="a11y-label" htmlFor="lang-select">{t.lang}</label>
          <select id="lang-select" className="a11y-select" value={lang} onChange={e => setLang(e.target.value)} aria-label="Select language">
            {LANG_OPTIONS.map(l => <option key={l.code} value={l.code}>{l.label}</option>)}
          </select>

          <label className="a11y-check-label">
            <input type="checkbox" checked={prefs.highContrast} onChange={() => toggle('highContrast')} aria-label="High contrast mode" />
            {t.contrast}
          </label>
          <label className="a11y-check-label">
            <input type="checkbox" checked={prefs.largeText} onChange={() => toggle('largeText')} aria-label="Large text mode" />
            {t.large}
          </label>
          <label className="a11y-check-label">
            <input type="checkbox" checked={prefs.simpleMode} onChange={() => toggle('simpleMode')} aria-label="Simple mode" />
            {t.simple}
          </label>
          <label className="a11y-check-label">
            <input type="checkbox" checked={prefs.screenReader} onChange={() => toggle('screenReader')} aria-label="Screen reader mode" />
            {t.screen}
          </label>
          <label className="a11y-check-label">
            <input type="checkbox" checked={prefs.textToSpeech} onChange={() => toggle('textToSpeech')} aria-label="Read responses aloud" />
            {t.tts}
          </label>
          <label className="a11y-check-label">
            <input type="checkbox" checked={prefs.voiceInput} onChange={() => toggle('voiceInput')} aria-label="Voice input" />
            {t.voice}
          </label>
          <label className="a11y-check-label">
            <input type="checkbox" checked={prefs.hearingMode} onChange={() => toggle('hearingMode')} aria-label="Hearing impairment mode" />
            {t.hearing}
          </label>

          <button className="a11y-close-btn" onClick={() => setOpen(false)} aria-label="Close">
            {t.close}
          </button>
        </div>
      )}
    </div>
  );
}
