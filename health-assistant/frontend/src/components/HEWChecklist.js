import React, { useState, useEffect } from 'react';
import { fetchChecklistTypes, fetchChecklist, submitChecklist } from '../api';

const L = {
  title:      { en: ' HEW Checklists', am: ' HEW ዝርዝሮች', ti: ' HEW ዝርዝራት', om: ' Tarree HEW', sid: ' Tarree HEW', so: ' Liiska HEW', aa: ' Liiska HEW', wal: ' Tarree HEW', had: ' Tarree HEW' },
  select:     { en: 'Select visit type:', am: 'የጉብኝት ዓይነት ይምረጡ:', ti: 'ዓይነት ምብጻሕ ምረጽ:', om: 'Gosa Daawwannaa Filadhu:', sid: 'Gosa Daawwannaa Filadhu:', so: 'Dooro nooca booqashada:', aa: 'Dooro nooca booqashada:', wal: 'Gosa Daawwannaa Filadhu:', had: 'Gosa Daawwannaa Filadhu:' },
  hew_name:   { en: 'HEW Name', am: 'HEW ስም', ti: 'ስም HEW', om: 'Maqaa HEW', sid: 'Maqaa HEW', so: 'Magaca HEW', aa: 'Magaca HEW', wal: 'Maqaa HEW', had: 'Maqaa HEW' },
  kebele:     { en: 'Kebele', am: 'ቀበሌ', ti: 'ቀበሌ', om: 'Ganda', sid: 'Ganda', so: 'Kebele', aa: 'Kebele', wal: 'Ganda', had: 'Ganda' },
  household:  { en: 'Household ID', am: 'የቤተሰብ መለያ', ti: 'ናይ ቤተሰብ መለለዪ', om: 'ID Mana', sid: 'ID Mana', so: 'ID Guriga', aa: 'ID Guriga', wal: 'ID Mana', had: 'ID Mana' },
  yes:        { en: 'Yes', am: 'አዎ', ti: 'እወ', om: 'Eeyyee', sid: 'Eeyyee', so: 'Haa', aa: 'Haa', wal: 'Eeyyee', had: 'Eeyyee' },
  no:         { en: 'No', am: 'አይደለም', ti: 'ኣይፋል', om: 'Lakki', sid: 'Lakki', so: 'Maya', aa: 'Maya', wal: 'Lakki', had: 'Lakki' },
  na:         { en: 'N/A', am: 'አይሰራም', ti: 'ኣይምልከትን', om: 'Hin Ilaaltu', sid: 'Hin Ilaaltu', so: 'Kuma khuseyso', aa: 'Kuma khuseyso', wal: 'Hin Ilaaltu', had: 'Hin Ilaaltu' },
  action:     { en: 'Action taken / Notes', am: 'የተወሰደ እርምጃ / ማስታወሻ', ti: 'ዝተወሰደ ስጉምቲ', om: 'Tarkaanfii Fudhataame', sid: 'Tarkaanfii Fudhataame', so: 'Tallaabada la qaaday / Xusuusin', aa: 'Tallaabada la qaaday / Xusuusin', wal: 'Tarkaanfii Fudhataame', had: 'Tarkaanfii Fudhataame' },
  referral:   { en: 'Referral needed?', am: 'ሪፈራል ያስፈልጋል?', ti: 'ሪፈራል የድሊ?', om: 'Ergiinsa Barbaachisaa?', sid: 'Ergiinsa Barbaachisaa?', so: 'Gudbinta ma loo baahan yahay?', aa: 'Gudbinta ma loo baahan yahay?', wal: 'Ergiinsa Barbaachisaa?', had: 'Ergiinsa Barbaachisaa?' },
  ref_reason: { en: 'Referral reason', am: 'የሪፈራል ምክንያት', ti: 'ምኽንያት ሪፈራል', om: 'Sababaa Ergiinsaa', sid: 'Sababaa Ergiinsaa', so: 'Sababta gudbinta', aa: 'Sababta gudbinta', wal: 'Sababaa Ergiinsaa', had: 'Sababaa Ergiinsaa' },
  submit:     { en: 'Submit Checklist', am: 'ዝርዝር አስገባ', ti: 'ዝርዝር ኣእቱ', om: 'Tarree Galchi', sid: 'Tarree Galchi', so: 'Gudbi Liiska', aa: 'Gudbi Liiska', wal: 'Tarree Galchi', had: 'Tarree Galchi' },
  submitted:  { en: ' Checklist submitted successfully!', am: ' ዝርዝር ተልኳል!', ti: ' ዝርዝር ተሰዲዱ!', om: ' Tarreen Galame!', sid: ' Tarreen Galame!', so: ' Liiska si guul leh ayaa loo gudbiyay!', aa: ' Liiska si guul leh ayaa loo gudbiyay!', wal: ' Tarreen Galame!', had: ' Tarreen Galame!' },
  critical:   { en: '️ Critical', am: '️ አስፈላጊ', ti: '️ ኣገዳሲ', om: '️ Barbaachisaa', sid: '️ Barbaachisaa', so: '️ Muhiim', aa: '️ Muhiim', wal: '️ Barbaachisaa', had: '️ Barbaachisaa' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

export default function HEWChecklist({ lang = 'en' }) {
  const [types, setTypes] = useState([]);
  const [selectedType, setSelectedType] = useState('');
  const [checklist, setChecklist] = useState(null);
  const [answers, setAnswers] = useState({});
  const [meta, setMeta] = useState({ hew_name: '', kebele: '', household_id: '', action_taken: '', referral_needed: false, referral_reason: '' });
  const [submitted, setSubmitted] = useState(false);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchChecklistTypes().then(d => setTypes(d.checklist_types || []));
  }, []);

  async function loadChecklist(type) {
    setSelectedType(type);
    setAnswers({});
    setSubmitted(false);
    const data = await fetchChecklist(type, lang);
    setChecklist(data);
  }

  function setAnswer(id, val) {
    setAnswers(a => ({ ...a, [id]: val }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    try {
      await submitChecklist({
        visit_type: selectedType,
        hew_name: meta.hew_name,
        kebele: meta.kebele,
        household_id: meta.household_id,
        visit_date: new Date().toISOString().split('T')[0],
        checklist_data: answers,
        action_taken: meta.action_taken,
        referral_needed: meta.referral_needed,
        referral_reason: meta.referral_reason,
      });
      setSubmitted(true);
    } finally {
      setLoading(false);
    }
  }

  const inputStyle = { width: '100%', padding: '0.5rem 0.8rem', borderRadius: 8, border: '1px solid #ccc', fontSize: '0.95rem', boxSizing: 'border-box' };
  const setMeta_ = (k, v) => setMeta(m => ({ ...m, [k]: v }));

  return (
    <div style={{ padding: '1rem', maxWidth: 680, margin: '0 auto' }}>
      <h2 style={{ marginBottom: '1rem' }}>{t('title', lang)}</h2>

      <div style={{ marginBottom: '1.5rem' }}>
        <label style={{ fontWeight: 600, display: 'block', marginBottom: 6 }}>{t('select', lang)}</label>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
          {types.map(tp => (
            <button key={tp.id} onClick={() => loadChecklist(tp.id)}
              style={{ padding: '0.5rem 1rem', borderRadius: 8, border: '2px solid #2e7d32', background: selectedType === tp.id ? '#2e7d32' : '#fff', color: selectedType === tp.id ? '#fff' : '#2e7d32', fontWeight: 600, cursor: 'pointer' }}>
              {tp[`title_${lang}`] || tp.title_en}
            </button>
          ))}
        </div>
      </div>

      {checklist && (
        <form onSubmit={handleSubmit}>
          <div style={{ background: '#f5f5f5', borderRadius: 10, padding: '1rem', marginBottom: '1rem', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
            {[['hew_name', 'HEW Name'], ['kebele', 'Kebele'], ['household_id', 'Household ID']].map(([k, lbl]) => (
              <div key={k}>
                <label style={{ fontWeight: 600, fontSize: '0.85rem', display: 'block', marginBottom: 3 }}>{t(k, lang) || lbl}</label>
                <input value={meta[k]} onChange={e => setMeta_(k, e.target.value)} style={inputStyle} />
              </div>
            ))}
          </div>

          <h3 style={{ marginBottom: '0.75rem', color: '#1b5e20' }}>{checklist.title}</h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', marginBottom: '1rem' }}>
            {checklist.items?.map(item => (
              <div key={item.id} style={{ background: '#fff', borderRadius: 8, padding: '0.75rem 1rem', border: `1px solid ${item.critical ? '#ffcdd2' : '#e0e0e0'}`, borderLeft: `4px solid ${item.critical ? '#c62828' : '#bbb'}` }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '1rem' }}>
                  <div style={{ flex: 1 }}>
                    {item.critical && <span style={{ fontSize: '0.72rem', background: '#ffebee', color: '#c62828', borderRadius: 4, padding: '1px 6px', marginRight: 6, fontWeight: 700 }}>{t('critical', lang)}</span>}
                    <span style={{ fontSize: '0.95rem' }}>{item.question}</span>
                  </div>
                  <div style={{ display: 'flex', gap: '0.4rem', flexShrink: 0 }}>
                    {['yes', 'no', 'na'].map(opt => (
                      <button key={opt} type="button" onClick={() => setAnswer(item.id, opt)}
                        style={{ padding: '4px 10px', borderRadius: 6, border: '1px solid #ccc', background: answers[item.id] === opt ? (opt === 'yes' ? '#2e7d32' : opt === 'no' ? '#c62828' : '#757575') : '#f5f5f5', color: answers[item.id] === opt ? '#fff' : '#333', fontWeight: 600, cursor: 'pointer', fontSize: '0.8rem' }}>
                        {t(opt, lang)}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div style={{ marginBottom: '0.75rem' }}>
            <label style={{ fontWeight: 600, display: 'block', marginBottom: 4 }}>{t('action', lang)}</label>
            <textarea value={meta.action_taken} onChange={e => setMeta_('action_taken', e.target.value)} rows={3} style={{ ...inputStyle, resize: 'vertical' }} />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
            <input type="checkbox" id="referral" checked={meta.referral_needed} onChange={e => setMeta_('referral_needed', e.target.checked)} style={{ width: 18, height: 18 }} />
            <label htmlFor="referral" style={{ fontWeight: 600, color: '#c62828' }}>{t('referral', lang)}</label>
          </div>

          {meta.referral_needed && (
            <div style={{ marginBottom: '0.75rem' }}>
              <label style={{ fontWeight: 600, display: 'block', marginBottom: 4 }}>{t('ref_reason', lang)}</label>
              <input value={meta.referral_reason} onChange={e => setMeta_('referral_reason', e.target.value)} style={inputStyle} />
            </div>
          )}

          {submitted
            ? <div style={{ background: '#e8f5e9', borderRadius: 8, padding: '0.75rem', color: '#2e7d32', fontWeight: 700, textAlign: 'center' }}>{t('submitted', lang)}</div>
            : <button type="submit" disabled={loading} style={{ width: '100%', padding: '0.7rem', borderRadius: 8, background: '#2e7d32', color: '#fff', border: 'none', fontWeight: 700, fontSize: '1rem', cursor: 'pointer' }}>
                {loading ? '…' : t('submit', lang)}
              </button>
          }
        </form>
      )}
    </div>
  );
}
