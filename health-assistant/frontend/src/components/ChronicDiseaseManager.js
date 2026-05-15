/**
 * ChronicDiseaseManager — BP and glucose tracking with adherence reminders.
 * Full multilingual: en, am, ti, om, sid, so, aa, wal, had
 */
import React, { useState, useEffect } from 'react';

const BASE = '/api/v1';

const L = {
  title:      { en: ' Chronic Disease', am: ' ሥር የሰደደ ህመም', ti: ' ሕማም ዘይፍወስ', om: ' Dhukkuba Hin Fayyine', sid: ' Dhukkuba Hin Fayyine', so: ' Cudurka Joogtada ah', aa: ' Cudurka Joogtada ah', wal: ' Dhukkuba Hin Fayyine', had: ' Dhukkuba Hin Fayyine' },
  htn:        { en: 'Hypertension', am: 'ከፍተኛ ደም ግፊት', ti: 'ልዑል ጸቕጢ ደም', om: 'Dhiibbaa Dhiigaa Ol Ka\'e', sid: 'Dhiibbaa Dhiigaa Ol Ka\'e', so: 'Cadaadiska Dhiigga', aa: 'Cadaadiska Dhiigga', wal: 'Dhiibbaa Dhiigaa Ol Ka\'e', had: 'Dhiibbaa Dhiigaa Ol Ka\'e' },
  dm:         { en: 'Diabetes', am: 'የስኳር ህመም', ti: 'ሕማም ሽኮር', om: 'Dhukkuba Sukkaara', sid: 'Dhukkuba Sukkaara', so: 'Cudurka Sonkorta', aa: 'Cudurka Sonkorta', wal: 'Dhukkuba Sukkaara', had: 'Dhukkuba Sukkaara' },
  bp_check:   { en: 'Check Blood Pressure', am: 'ደም ግፊት ይለኩ', ti: 'ጸቕጢ ደም ዕቀን', om: 'Dhiibbaa Dhiigaa Sakatta\'i', sid: 'Dhiibbaa Dhiigaa Sakatta\'i', so: 'Hubi Cadaadiska Dhiigga', aa: 'Hubi Cadaadiska Dhiigga', wal: 'Dhiibbaa Dhiigaa Sakatta\'i', had: 'Dhiibbaa Dhiigaa Sakatta\'i' },
  glucose_check: { en: 'Check Blood Sugar', am: 'ደም ስኳር ይለኩ', ti: 'ሽኮር ደም ዕቀን', om: 'Sukkaara Dhiigaa Sakatta\'i', sid: 'Sukkaara Dhiigaa Sakatta\'i', so: 'Hubi Sonkorta Dhiigga', aa: 'Hubi Sonkorta Dhiigga', wal: 'Sukkaara Dhiigaa Sakatta\'i', had: 'Sukkaara Dhiigaa Sakatta\'i' },
  systolic:   { en: 'Systolic (upper)', am: 'ሲስቶሊክ (ላይኛ)', ti: 'ሲስቶሊክ (ላዕሊ)', om: 'Ol (systolic)', sid: 'Ol (systolic)', so: 'Sare (systolic)', aa: 'Sare (systolic)', wal: 'Ol (systolic)', had: 'Ol (systolic)' },
  diastolic:  { en: 'Diastolic (lower)', am: 'ዲያስቶሊክ (ታችኛ)', ti: 'ዲያስቶሊክ (ታሕቲ)', om: 'Gadi (diastolic)', sid: 'Gadi (diastolic)', so: 'Hoose (diastolic)', aa: 'Hoose (diastolic)', wal: 'Gadi (diastolic)', had: 'Gadi (diastolic)' },
  glucose:    { en: 'Blood Sugar (mg/dL)', am: 'ደም ስኳር (mg/dL)', ti: 'ሽኮር ደም (mg/dL)', om: 'Sukkaara Dhiigaa (mg/dL)', sid: 'Sukkaara Dhiigaa (mg/dL)', so: 'Sonkorta Dhiigga (mg/dL)', aa: 'Sonkorta Dhiigga (mg/dL)', wal: 'Sukkaara Dhiigaa (mg/dL)', had: 'Sukkaara Dhiigaa (mg/dL)' },
  fasting:    { en: 'Fasting reading', am: 'ጾም ምርመራ', ti: 'ጾም ምርመራ', om: 'Nyaata malee', sid: 'Nyaata malee', so: 'Qado la\'aanta', aa: 'Qado la\'aanta', wal: 'Nyaata malee', had: 'Nyaata malee' },
  check:      { en: 'Check', am: 'ፈትሽ', ti: 'ፈትሽ', om: 'Sakatta\'i', sid: 'Sakatta\'i', so: 'Hubi', aa: 'Hubi', wal: 'Sakatta\'i', had: 'Sakatta\'i' },
  checklist:  { en: 'Self-Care Checklist', am: 'ራስ-እንክብካቤ ዝርዝር', ti: 'ዝርዝር ናይ ባዕልኻ ክንክን', om: 'Tarree Kunuunsa Ofii', sid: 'Tarree Kunuunsa Ofii', so: 'Liiska Daryeelka Nafta', aa: 'Liiska Daryeelka Nafta', wal: 'Tarree Kunuunsa Ofii', had: 'Tarree Kunuunsa Ofii' },
  loading:    { en: 'Checking…', am: 'በመፈተሽ ላይ…', ti: 'ይፈትሽ ኣሎ…', om: 'Sakattaa\'amaa jira…', sid: 'Sakattaa\'amaa jira…', so: 'Waa la hubinayaa…', aa: 'Waa la hubinayaa…', wal: 'Sakattaa\'amaa jira…', had: 'Sakattaa\'amaa jira…' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

const STAGE_COLORS = {
  normal: '#e8f5e9', elevated: '#fff9c4', stage1: '#fff3e0',
  stage2: '#fbe9e7', crisis: '#ffebee',
  hypoglycemia: '#ffebee', hyperglycemia: '#fbe9e7',
};
const STAGE_TEXT = {
  normal: '#2e7d32', elevated: '#f57f17', stage1: '#e65100',
  stage2: '#bf360c', crisis: '#c62828',
  hypoglycemia: '#c62828', hyperglycemia: '#bf360c',
};

export default function ChronicDiseaseManager({ lang = 'en' }) {
  const [tab, setTab]         = useState('htn');
  const [systolic, setSys]    = useState('');
  const [diastolic, setDia]   = useState('');
  const [glucose, setGlucose] = useState('');
  const [fasting, setFasting] = useState(true);
  const [result, setResult]   = useState(null);
  const [checklist, setChecklist] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const condition = tab === 'htn' ? 'hypertension' : 'diabetes';
    fetch(`${BASE}/chronic/checklist/?condition=${condition}&language=${lang}`)
      .then((r) => r.json())
      .then(setChecklist)
      .catch(() => {});
    setResult(null);
  }, [tab, lang]);

  async function checkBP() {
    if (!systolic || !diastolic) return;
    setLoading(true);
    try {
      const res = await fetch(`${BASE}/chronic/bp/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ systolic: parseInt(systolic), diastolic: parseInt(diastolic), language: lang }),
      });
      setResult(await res.json());
    } catch { /* offline */ } finally { setLoading(false); }
  }

  async function checkGlucose() {
    if (!glucose) return;
    setLoading(true);
    try {
      const res = await fetch(`${BASE}/chronic/glucose/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ glucose_mgdl: parseFloat(glucose), fasting, language: lang }),
      });
      setResult(await res.json());
    } catch { /* offline */ } finally { setLoading(false); }
  }

  const resultColor = result ? (STAGE_TEXT[result.stage || result.status] || '#333') : '#333';
  const resultBg    = result ? (STAGE_COLORS[result.stage || result.status] || '#f5f5f5') : '#f5f5f5';

  return (
    <div style={{ padding: '0.5rem' }}>
      <p className="section-title">{t('title', lang)}</p>

      {/* Tab selector */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 14 }}>
        {[['htn', 'htn'], ['dm', 'dm']].map(([id, labelKey]) => (
          <button key={id} onClick={() => setTab(id)}
            style={{ padding: '0.4rem 1rem', borderRadius: 8, border: 'none',
                     background: tab === id ? '#1565c0' : '#e0e0e0',
                     color: tab === id ? '#fff' : '#333', cursor: 'pointer', fontWeight: 600 }}>
            {t(labelKey, lang)}
          </button>
        ))}
      </div>

      {/* BP checker */}
      {tab === 'htn' && (
        <div style={{ background: '#f5f5f5', borderRadius: 8, padding: '0.8rem', marginBottom: 12 }}>
          <p style={{ fontWeight: 600, marginBottom: 8 }}>{t('bp_check', lang)}</p>
          <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
            <div style={{ flex: 1 }}>
              <label style={{ fontSize: '0.75rem', color: '#555' }}>{t('systolic', lang)}</label>
              <input type="number" value={systolic} onChange={(e) => setSys(e.target.value)}
                placeholder="120" min="60" max="250"
                style={{ display: 'block', width: '100%', padding: '0.4rem', borderRadius: 6, border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
            <div style={{ flex: 1 }}>
              <label style={{ fontSize: '0.75rem', color: '#555' }}>{t('diastolic', lang)}</label>
              <input type="number" value={diastolic} onChange={(e) => setDia(e.target.value)}
                placeholder="80" min="40" max="150"
                style={{ display: 'block', width: '100%', padding: '0.4rem', borderRadius: 6, border: '1px solid #ccc', boxSizing: 'border-box' }} />
            </div>
          </div>
          <button onClick={checkBP} disabled={!systolic || !diastolic || loading}
            style={{ padding: '0.4rem 1.2rem', borderRadius: 8, background: '#1565c0', color: '#fff', border: 'none', cursor: 'pointer' }}>
            {loading ? t('loading', lang) : t('check', lang)}
          </button>
        </div>
      )}

      {/* Glucose checker */}
      {tab === 'dm' && (
        <div style={{ background: '#f5f5f5', borderRadius: 8, padding: '0.8rem', marginBottom: 12 }}>
          <p style={{ fontWeight: 600, marginBottom: 8 }}>{t('glucose_check', lang)}</p>
          <input type="number" value={glucose} onChange={(e) => setGlucose(e.target.value)}
            placeholder="mg/dL" min="20" max="600"
            style={{ display: 'block', width: '100%', marginBottom: 8, padding: '0.4rem', borderRadius: 6, border: '1px solid #ccc', boxSizing: 'border-box' }} />
          <label style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8, fontSize: '0.85rem' }}>
            <input type="checkbox" checked={fasting} onChange={(e) => setFasting(e.target.checked)} />
            {t('fasting', lang)}
          </label>
          <button onClick={checkGlucose} disabled={!glucose || loading}
            style={{ padding: '0.4rem 1.2rem', borderRadius: 8, background: '#6a1b9a', color: '#fff', border: 'none', cursor: 'pointer' }}>
            {loading ? t('loading', lang) : t('check', lang)}
          </button>
        </div>
      )}

      {/* Result */}
      {result && (
        <div style={{ background: resultBg, borderRadius: 8, padding: '0.8rem', marginBottom: 12 }}>
          <div style={{ fontWeight: 700, color: resultColor, marginBottom: 6 }}>
            {result.urgent && ' '}{result.stage || result.status}
          </div>
          <p style={{ fontSize: '0.85rem', margin: '0 0 8px' }}>{result.message}</p>
          {result.danger_signs && (
            <div>
              <p style={{ fontSize: '0.75rem', fontWeight: 600, color: '#c62828', margin: '4px 0 2px' }}>️ Danger signs:</p>
              <ul style={{ margin: 0, paddingLeft: 16, fontSize: '0.75rem', color: '#555' }}>
                {result.danger_signs.slice(0, 4).map((s, i) => <li key={i}>{s}</li>)}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Self-care checklist */}
      {checklist && checklist.items && (
        <div>
          <p style={{ fontWeight: 600, marginBottom: 6 }}>{t('checklist', lang)}</p>
          <div style={{ background: '#fff', border: '1px solid #c8e6d4', borderRadius: 8, padding: '0.6rem' }}>
            {checklist.items.map((item, i) => (
              <div key={i} style={{ display: 'flex', alignItems: 'flex-start', gap: 8, marginBottom: 6, fontSize: '0.82rem' }}>
                <span style={{ color: '#2e7d32', flexShrink: 0 }}></span>
                <span>{item}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
