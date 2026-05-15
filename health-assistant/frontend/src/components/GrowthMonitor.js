import React, { useState } from 'react';
import { assessGrowth } from '../api';

const L = {
  title:       { en: ' Growth Monitor', am: ' የዕድገት ክትትል', ti: ' ዕቤት ምክትታል', om: ' Guddina Hordofuu', sid: ' Guddina Hordofuu', so: ' Kormeerka Kobaca', aa: ' Kormeerka Kobaca', wal: ' Guddina Hordofuu', had: ' Guddina Hordofuu' },
  age_months:  { en: 'Age (months)', am: 'ዕድሜ (ወር)', ti: 'ዕድሜ (ወርሒ)', om: 'Umurii (ji\'a)', sid: 'Umurii (ji\'a)', so: 'Da\'da (bilood)', aa: 'Da\'da (bilood)', wal: 'Umurii (ji\'a)', had: 'Umurii (ji\'a)' },
  sex:         { en: 'Sex', am: 'ጾታ', ti: 'ጾታ', om: 'Saala', sid: 'Saala', so: 'Jinsiga', aa: 'Jinsiga', wal: 'Saala', had: 'Saala' },
  male:        { en: 'Male', am: 'ወንድ', ti: 'ወዲ', om: 'Dhiira', sid: 'Dhiira', so: 'Lab', aa: 'Lab', wal: 'Dhiira', had: 'Dhiira' },
  female:      { en: 'Female', am: 'ሴት', ti: 'ጓል', om: 'Dhalaa', sid: 'Dhalaa', so: 'Dheddig', aa: 'Dheddig', wal: 'Dhalaa', had: 'Dhalaa' },
  weight:      { en: 'Weight (kg)', am: 'ክብደት (ኪሎ)', ti: 'ክብደት (ኪሎ)', om: 'Ulfaatina (kg)', sid: 'Ulfaatina (kg)', so: 'Miisaanka (kg)', aa: 'Miisaanka (kg)', wal: 'Ulfaatina (kg)', had: 'Ulfaatina (kg)' },
  height:      { en: 'Height (cm)', am: 'ቁመት (ሴሜ)', ti: 'ቁመት (ሴሜ)', om: 'Dheerina (cm)', sid: 'Dheerina (cm)', so: 'Dhererka (cm)', aa: 'Dhererka (cm)', wal: 'Dheerina (cm)', had: 'Dheerina (cm)' },
  muac:        { en: 'MUAC (cm)', am: 'MUAC (ሴሜ)', ti: 'MUAC (ሴሜ)', om: 'MUAC (cm)', sid: 'MUAC (cm)', so: 'MUAC (cm)', aa: 'MUAC (cm)', wal: 'MUAC (cm)', had: 'MUAC (cm)' },
  muac_help:   { en: 'Mid-upper arm circumference — measure left arm midpoint', am: 'የግራ ክንድ መካከለኛ ዙሪያ', ti: 'ናይ ጸጋም ቅልጽም ማእከላዊ ዙሪያ', om: 'Giddugaleessa harka bitaa', sid: 'Giddugaleessa harka bitaa', so: 'Wareegga dhexe ee gacanta bidix', aa: 'Wareegga dhexe ee gacanta bidix', wal: 'Giddugaleessa harka bitaa', had: 'Giddugaleessa harka bitaa' },
  oedema:      { en: 'Bilateral pitting oedema?', am: 'የሁለቱም እግሮች እብጠት?', ti: 'ናይ ክልቲኡ እግሪ ሕበጥ?', om: 'Dhiita lama?', sid: 'Dhiita lama?', so: 'Barar labada cagood?', aa: 'Barar labada cagood?', wal: 'Dhiita lama?', had: 'Dhiita lama?' },
  assess:      { en: 'Assess', am: 'ምዘና', ti: 'ምዘና', om: 'Madaali', sid: 'Madaali', so: 'Qiimee', aa: 'Qiimee', wal: 'Madaali', had: 'Madaali' },
  result:      { en: 'Result', am: 'ውጤት', ti: 'ውጽኢት', om: 'Bu\'aa', sid: 'Bu\'aa', so: 'Natiijada', aa: 'Natiijada', wal: 'Bu\'aa', had: 'Bu\'aa' },
  recommend:   { en: 'Recommendation', am: 'ምክር', ti: 'ምኽሪ', om: 'Gorsa', sid: 'Gorsa', so: 'Talada', aa: 'Talada', wal: 'Gorsa', had: 'Gorsa' },
  sam_badge:   { en: 'SAM — REFER NOW', am: 'SAM — ወዲያውኑ ሪፈር', ti: 'SAM — ሕጂ ሪፈር', om: 'SAM — AMMA ERGI', sid: 'SAM — AMMA ERGI', so: 'SAM — HADDA U DIR', aa: 'SAM — HADDA U DIR', wal: 'SAM — AMMA ERGI', had: 'SAM — AMMA ERGI' },
  mam_badge:   { en: 'MAM — Needs Support', am: 'MAM — ድጋፍ ያስፈልጋል', ti: 'MAM — ሓገዝ የድሊ', om: 'MAM — Gargaarsa Barbaachisa', sid: 'MAM — Gargaarsa Barbaachisa', so: 'MAM — Taageero Ayaa Loo Baahan Yahay', aa: 'MAM — Taageero Ayaa Loo Baahan Yahay', wal: 'MAM — Gargaarsa Barbaachisa', had: 'MAM — Gargaarsa Barbaachisa' },
  normal_badge:{ en: 'Normal', am: 'መደበኛ', ti: 'ንቡር', om: 'Idilee', sid: 'Idilee', so: 'Caadi', aa: 'Caadi', wal: 'Idilee', had: 'Idilee' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

const STATUS_STYLE = {
  SAM:    { background: '#ffebee', border: '2px solid #c62828', color: '#c62828' },
  MAM:    { background: '#fff8e1', border: '2px solid #f9a825', color: '#f57f17' },
  normal: { background: '#e8f5e9', border: '2px solid #2e7d32', color: '#2e7d32' },
};

export default function GrowthMonitor({ lang = 'en' }) {
  const [form, setForm] = useState({ age_months: '', sex: 'male', weight_kg: '', height_cm: '', muac_cm: '', oedema: false });
  const [result, setResult] = useState(null);

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  async function handleSubmit(e) {
    e.preventDefault();
    const payload = {
      age_months: parseFloat(form.age_months) || 0,
      sex: form.sex,
      oedema: form.oedema,
      ...(form.weight_kg ? { weight_kg: parseFloat(form.weight_kg) } : {}),
      ...(form.height_cm ? { height_cm: parseFloat(form.height_cm) } : {}),
      ...(form.muac_cm   ? { muac_cm:   parseFloat(form.muac_cm)   } : {}),
    };
    const data = await assessGrowth(payload);
    setResult(data);
  }

  const inputStyle = { width: '100%', padding: '0.5rem 0.8rem', borderRadius: 8, border: '1px solid #ccc', fontSize: '1rem', boxSizing: 'border-box' };
  const labelStyle = { display: 'block', fontWeight: 600, marginBottom: 4, color: '#333', fontSize: '0.9rem' };

  return (
    <div style={{ padding: '1rem', maxWidth: 600, margin: '0 auto' }}>
      <h2 style={{ marginBottom: '1rem' }}>{t('title', lang)}</h2>
      <form onSubmit={handleSubmit} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
        <div>
          <label style={labelStyle}>{t('age_months', lang)} *</label>
          <input type="number" min="0" max="60" step="0.5" required value={form.age_months} onChange={e => set('age_months', e.target.value)} style={inputStyle} />
        </div>
        <div>
          <label style={labelStyle}>{t('sex', lang)}</label>
          <select value={form.sex} onChange={e => set('sex', e.target.value)} style={inputStyle}>
            <option value="male">{t('male', lang)}</option>
            <option value="female">{t('female', lang)}</option>
          </select>
        </div>
        <div>
          <label style={labelStyle}>{t('weight', lang)}</label>
          <input type="number" min="0" step="0.1" value={form.weight_kg} onChange={e => set('weight_kg', e.target.value)} style={inputStyle} placeholder="e.g. 7.5" />
        </div>
        <div>
          <label style={labelStyle}>{t('height', lang)}</label>
          <input type="number" min="0" step="0.1" value={form.height_cm} onChange={e => set('height_cm', e.target.value)} style={inputStyle} placeholder="e.g. 68" />
        </div>
        <div style={{ gridColumn: '1 / -1' }}>
          <label style={labelStyle}>{t('muac', lang)}</label>
          <input type="number" min="0" step="0.1" value={form.muac_cm} onChange={e => set('muac_cm', e.target.value)} style={inputStyle} placeholder="e.g. 12.5" />
          <div style={{ fontSize: '0.78rem', color: '#777', marginTop: 3 }}>{t('muac_help', lang)}</div>
        </div>
        <div style={{ gridColumn: '1 / -1', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <input type="checkbox" id="oedema" checked={form.oedema} onChange={e => set('oedema', e.target.checked)} style={{ width: 18, height: 18 }} />
          <label htmlFor="oedema" style={{ fontWeight: 600, color: '#c62828' }}>{t('oedema', lang)}</label>
        </div>
        <div style={{ gridColumn: '1 / -1' }}>
          <button type="submit" style={{ width: '100%', padding: '0.7rem', borderRadius: 8, background: '#2e7d32', color: '#fff', border: 'none', fontWeight: 700, fontSize: '1rem', cursor: 'pointer' }}>
            {t('assess', lang)}
          </button>
        </div>
      </form>

      {result && (
        <div style={{ marginTop: '1.5rem' }}>
          <div style={{ ...STATUS_STYLE[result.overall_status] || STATUS_STYLE.normal, borderRadius: 10, padding: '1rem', marginBottom: '1rem', textAlign: 'center' }}>
            <div style={{ fontSize: '1.4rem', fontWeight: 800 }}>
              {result.overall_status === 'SAM' ? t('sam_badge', lang) : result.overall_status === 'MAM' ? t('mam_badge', lang) : t('normal_badge', lang)}
            </div>
          </div>
          {result.assessments?.map((a, i) => (
            <div key={i} style={{ background: '#f5f5f5', borderRadius: 8, padding: '0.75rem', marginBottom: '0.5rem', borderLeft: `4px solid ${a.color === 'red' ? '#c62828' : a.color === 'yellow' ? '#f9a825' : '#2e7d32'}` }}>
              <div style={{ fontWeight: 600, textTransform: 'uppercase', fontSize: '0.75rem', color: '#666' }}>{a.type?.replace(/_/g, ' ')}</div>
              <div style={{ marginTop: 4 }}>{a[`message_${lang}`] || a.message_en}</div>
            </div>
          ))}
          {result.oedema_alert && (
            <div style={{ background: '#ffebee', borderRadius: 8, padding: '0.75rem', marginBottom: '0.5rem', borderLeft: '4px solid #c62828' }}>
              {result.oedema_alert[`message_${lang}`] || result.oedema_alert.message_en}
            </div>
          )}
          <div style={{ background: '#e8f5e9', borderRadius: 8, padding: '0.75rem', borderLeft: '4px solid #2e7d32' }}>
            <div style={{ fontWeight: 600, marginBottom: 4 }}>{t('recommend', lang)}</div>
            <div>{result[`recommendation_${lang}`] || result.recommendation_en}</div>
          </div>
        </div>
      )}
    </div>
  );
}
