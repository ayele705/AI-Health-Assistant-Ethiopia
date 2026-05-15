/**
 * TriageAlert.js
 * Displays a full-screen triage alert when "Red Flag" symptoms are detected
 * in the user's chat input. Supports all 9 project languages.
 */
import React, { useEffect, useRef } from 'react';
import './TriageAlert.css';

// ── Red Flag symptom keywords (per language) ──────────────────────────────────
// Each entry is a regex-friendly keyword list. Matching is case-insensitive.
export const RED_FLAG_KEYWORDS = {
  en: [
    'unconscious', 'not breathing', 'no pulse', 'seizure', 'convulsion',
    'severe bleeding', 'heavy bleeding', 'chest pain', 'difficulty breathing',
    'can\'t breathe', 'cannot breathe', 'stroke', 'paralysis', 'paralyzed',
    'severe headache', 'sudden headache', 'high fever', 'very high fever',
    'stiff neck', 'rash with fever', 'meningitis', 'eclampsia', 'preeclampsia',
    'severe abdominal pain', 'vomiting blood', 'blood in stool', 'bloody stool',
    'severe dehydration', 'sunken eyes', 'not urinating', 'no urine',
    'severe malnutrition', 'edema', 'swollen feet', 'swollen legs',
    'yellow eyes', 'jaundice', 'severe diarrhea', 'watery diarrhea',
    'choking', 'poisoning', 'overdose', 'snake bite', 'snakebite',
    'severe burn', 'deep wound', 'broken bone', 'fracture',
    'premature labor', 'labor before 37 weeks', 'cord prolapse',
    'baby not moving', 'fetal movement stopped',
  ],
  am: [
    'ንቃቄ ጠፋ', 'አይተነፍስም', 'ድንጋጤ', 'ከፍተኛ ደም መፍሰስ', 'የደረት ህመም',
    'መተንፈስ አልቻለም', 'ሽባ', 'ከፍተኛ ራስ ምታት', 'ከፍተኛ ትኩሳት', 'ጠንካራ አንገት',
    'ሜኒንጂቲስ', 'ኤክላምፕሲያ', 'ከፍተኛ የሆድ ህመም', 'ደም ማስታወክ', 'ደም ያለው ሰገራ',
    'ከፍተኛ ድርቀት', 'ሽንት የለም', 'ቢጫ ዓይን', 'ጃንዲስ', 'ከፍተኛ ተቅማጥ',
    'መርዝ', 'እባብ ነከሰ', 'ከፍተኛ ቃጠሎ', 'ስብራት', 'ያለጊዜ ምጥ',
    'ሕፃን አይንቀሳቀስም',
  ],
  ti: [
    'ንቃቐ ጠፊኡ', 'ኣይተነፍስን', 'ሕርቃን', 'ብዙሕ ደም', 'ቃንዛ ኣፍ ልቢ',
    'ምስትንፋስ ኣይክእልን', 'ሽምዓ', 'ብርቱዕ ቃንዛ ርእሲ', 'ልዑል ረስኒ', 'ጽኑዕ ክሳድ',
    'ሜኒንጂቲስ', 'ብርቱዕ ቃንዛ ከብዲ', 'ደም ምትፋእ', 'ደም ዘለዎ ሰገር',
    'ብርቱዕ ምድርቃ', 'ሽንቲ የለን', 'ቢጫ ዓይኒ', 'ብርቱዕ ተምሲ', 'መርዚ',
    'ተኻሲ ሓሙኽሽቲ', 'ብርቱዕ ቃጸሎ', 'ምስባር', 'ቅድሚ ግዜ ሕርሲ',
    'ህጻን ኣይንቀሳቀስን',
  ],
  om: [
    'of wallaaluu', 'hafuura hin baafatu', 'dhukkubsachuu', 'dhiigni baay\'ee', 'dhukkuba garaa laphee',
    'hafuura baafachuu hin dandeenye', 'dhukkuba mataa hamaa', 'ho\'a olaanaa', 'morma jabaataa',
    'dhukkuba garaa hamaa', 'dhiiga hanqaaquu', 'fincaan hin baafatu', 'ija keelloo',
    'garaa kaasaa hamaa', 'summii', 'bofa ciniine', 'gubaa hamaa', 'lafee cabuu',
    'daa\'ima hin sochoone',
  ],
  sid: [
    'of wallaaluu', 'hafuura hin baafatu', 'dhukkubsachuu', 'dhiigni baay\'ee', 'dhukkuba garaa laphee',
    'dhukkuba mataa hamaa', 'ho\'a olaanaa', 'morma jabaataa', 'dhukkuba garaa hamaa',
    'dhiiga hanqaaquu', 'fincaan hin baafatu', 'ija keelloo', 'garaa kaasaa hamaa',
    'summii', 'bofa ciniine', 'gubaa hamaa', 'lafee cabuu', 'daa\'ima hin sochoone',
  ],
  so: [
    'miyir la\'aanta', 'neefsiga la\'aanta', 'qaniiqa', 'dhiig badan', 'xanuunka laabta',
    'neefsiga adag', 'madax xanuun xun', 'xummad sare', 'luqunta adag',
    'xanuunka caloosha', 'dhiig matag', 'kaadi la\'aanta', 'indho huruud',
    'gudaha xanuun', 'sun', 'mas qaniinay', 'gubashada xun', 'lafta jabay',
    'ilmaha aan dhaqaaqin',
  ],
  aa: [
    'miyir la\'aanta', 'neefsiga la\'aanta', 'qaniiqa', 'dhiig badan', 'xanuunka laabta',
    'neefsiga adag', 'madax xanuun xun', 'xummad sare', 'xanuunka caloosha',
    'dhiig matag', 'kaadi la\'aanta', 'indho huruud', 'sun', 'mas qaniinay',
    'gubashada xun', 'lafta jabay', 'ilmaha aan dhaqaaqin',
  ],
  wal: [
    'of wallaaluu', 'hafuura hin baafatu', 'dhukkubsachuu', 'dhiigni baay\'ee',
    'dhukkuba mataa hamaa', 'ho\'a olaanaa', 'dhukkuba garaa hamaa',
    'fincaan hin baafatu', 'ija keelloo', 'summii', 'bofa ciniine',
    'gubaa hamaa', 'lafee cabuu', 'daa\'ima hin sochoone',
  ],
  had: [
    'of wallaaluu', 'hafuura hin baafatu', 'dhukkubsachuu', 'dhiigni baay\'ee',
    'dhukkuba mataa hamaa', 'ho\'a olaanaa', 'dhukkuba garaa hamaa',
    'fincaan hin baafatu', 'ija keelloo', 'summii', 'bofa ciniine',
    'gubaa hamaa', 'lafee cabuu', 'daa\'ima hin sochoone',
  ],
};

/**
 * Checks input text for red-flag symptoms.
 * Returns array of matched keywords, or empty array if none.
 */
export function detectRedFlags(text, lang = 'en') {
  if (!text) return [];
  const lower = text.toLowerCase();
  // Always check English keywords too (users may mix languages)
  const keywords = [
    ...(RED_FLAG_KEYWORDS[lang] || []),
    ...(lang !== 'en' ? RED_FLAG_KEYWORDS.en : []),
  ];
  return keywords.filter((kw) => lower.includes(kw.toLowerCase()));
}

// ── i18n strings ──────────────────────────────────────────────────────────────
const LABELS = {
  title: {
    en: ' RED FLAG SYMPTOMS DETECTED',
    am: ' አደገኛ ምልክቶች ተገኝተዋል',
    ti: ' ሓደገኛ ምልክታት ተረኺቦም',
    om: ' MALLATTOOLEE HAMAA ARGAMAN',
    sid: ' MALLATTOOLEE HAMAA ARGAMAN',
    so: ' CALAAMADAHA KHATAR AH OO LA HELAY',
    aa: ' CALAAMADAHA KHATAR AH OO LA HELAY',
    wal: ' MALLATTOOLEE HAMAA ARGAMAN',
    had: ' MALLATTOOLEE HAMAA ARGAMAN',
  },
  subtitle: {
    en: 'This may be a medical emergency. Act immediately.',
    am: 'ይህ አስቸኳይ የህክምና ሁኔታ ሊሆን ይችላል። ወዲያውኑ እርምጃ ይውሰዱ።',
    ti: 'እዚ ህጹጽ ሕክምናዊ ኩነታት ክኸውን ይኽእል። ሕጂ ስጉምቲ ውሰድ።',
    om: 'Kun yeroo ariifachiisaa fayyaa ta\'uu danda\'a. Amma tarkaanfii fudhaa.',
    sid: 'Kun yeroo ariifachiisaa fayyaa ta\'uu danda\'a. Amma tarkaanfii fudhaa.',
    so: 'Tani waxay noqon kartaa xaalad caafimaad degdeg ah. Hadda tallaabo.',
    aa: 'Tani waxay noqon kartaa xaalad caafimaad degdeg ah. Hadda tallaabo.',
    wal: 'Kun yeroo ariifachiisaa fayyaa ta\'uu danda\'a. Amma tarkaanfii fudhaa.',
    had: 'Kun yeroo ariifachiisaa fayyaa ta\'uu danda\'a. Amma tarkaanfii fudhaa.',
  },
  detected_symptoms: {
    en: 'Detected symptoms:',
    am: 'የተገኙ ምልክቶች:',
    ti: 'ዝተረኽቡ ምልክታት:',
    om: 'Mallattoolee argaman:',
    sid: 'Mallattoolee argaman:',
    so: 'Calaamadaha la helay:',
    aa: 'Calaamadaha la helay:',
    wal: 'Mallattoolee argaman:',
    had: 'Mallattoolee argaman:',
  },
  call_emergency: {
    en: ' Call Emergency: 907',
    am: ' አስቸኳይ ደውሉ: 907',
    ti: ' ህጹጽ ደውል: 907',
    om: ' Ariifachiisaa Bilbili: 907',
    sid: ' Ariifachiisaa Bilbili: 907',
    so: ' Degdeg Wac: 907',
    aa: ' Degdeg Wac: 907',
    wal: ' Ariifachiisaa Bilbili: 907',
    had: ' Ariifachiisaa Bilbili: 907',
  },
  go_facility: {
    en: ' Go to nearest health facility NOW',
    am: ' ወዲያውኑ ወደ ቅርብ ጤና ጣቢያ ሂዱ',
    ti: ' ሕጂ ናብ ቀረባ ጥዕና ጣቢያ ኪድ',
    om: ' AMMA buufata fayyaa dhiyoo deemi',
    sid: ' AMMA buufata fayyaa dhiyoo deemi',
    so: ' HADDA xarunta caafimaadka ugu dhow aad',
    aa: ' HADDA xarunta caafimaadka ugu dhow aad',
    wal: ' AMMA buufata fayyaa dhiyoo deemi',
    had: ' AMMA buufata fayyaa dhiyoo deemi',
  },
  continue: {
    en: 'Continue with assessment',
    am: 'ምርመራ ቀጥሉ',
    ti: 'ምርመራ ቀጽሉ',
    om: "Sakatta'aa itti fufi",
    sid: "Sakatta'aa itti fufi",
    so: 'Qiimaynta sii wad',
    aa: 'Qiimaynta sii wad',
    wal: "Sakatta'aa itti fufi",
    had: "Sakatta'aa itti fufi",
  },
  dismiss: {
    en: 'Dismiss',
    am: 'ዝጋ',
    ti: 'ዕጸዎ',
    om: 'Cufii',
    sid: 'Cufii',
    so: 'Xidh',
    aa: 'Xidh',
    wal: 'Cufii',
    had: 'Cufii',
  },
};

function t(key, lang) {
  return LABELS[key]?.[lang] || LABELS[key]?.en || '';
}

// ── Component ─────────────────────────────────────────────────────────────────
export default function TriageAlert({ flags, lang = 'en', onContinue, onDismiss }) {
  const dialogRef = useRef(null);
  const firstBtnRef = useRef(null);

  // Trap focus inside the modal for accessibility
  useEffect(() => {
    if (!flags?.length) return;
    firstBtnRef.current?.focus();

    function handleKeyDown(e) {
      if (e.key === 'Escape') onDismiss?.();
    }
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [flags, onDismiss]);

  if (!flags?.length) return null;

  return (
    <div
      className="triage-overlay"
      role="alertdialog"
      aria-modal="true"
      aria-labelledby="triage-title"
      aria-describedby="triage-desc"
    >
      {/* Pulsing red border animation */}
      <div className="triage-modal" ref={dialogRef}>
        {/* Header */}
        <div className="triage-header">
          <span className="triage-pulse-dot" aria-hidden="true" />
          <h2 id="triage-title" className="triage-title">
            {t('title', lang)}
          </h2>
        </div>

        {/* Subtitle */}
        <p id="triage-desc" className="triage-subtitle">
          {t('subtitle', lang)}
        </p>

        {/* Detected symptoms list */}
        <div className="triage-flags">
          <p className="triage-flags-label">{t('detected_symptoms', lang)}</p>
          <ul className="triage-flags-list" aria-label="Red flag symptoms">
            {flags.map((flag, i) => (
              <li key={i} className="triage-flag-item">
                ️ {flag}
              </li>
            ))}
          </ul>
        </div>

        {/* Action buttons */}
        <div className="triage-actions">
          <a
            href="tel:907"
            className="triage-btn triage-btn--emergency"
            ref={firstBtnRef}
            aria-label="Call emergency number 907"
          >
            {t('call_emergency', lang)}
          </a>

          <div className="triage-btn triage-btn--facility" role="note">
            {t('go_facility', lang)}
          </div>

          <div className="triage-secondary-actions">
            <button
              className="triage-btn triage-btn--continue"
              onClick={onContinue}
              aria-label="Continue with symptom assessment"
            >
              {t('continue', lang)}
            </button>
            <button
              className="triage-btn triage-btn--dismiss"
              onClick={onDismiss}
              aria-label="Dismiss alert"
            >
              {t('dismiss', lang)}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
