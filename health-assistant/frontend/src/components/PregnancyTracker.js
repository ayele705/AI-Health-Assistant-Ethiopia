import React, { useState } from 'react';
import { registerPregnancy, fetchPregnancySchedule } from '../api';

const L = {
  title:      { en: ' Pregnancy Follow-up', am: ' የእርግዝና ክትትል', ti: ' ናይ ጥንሲ ምክትታል', om: ' Ulfaa Hordofuu', sid: ' Ulfaa Hordofuu', so: ' Raadraaca Uurka', aa: ' Raadraaca Uurka', wal: ' Ulfaa Hordofuu', had: ' Ulfaa Hordofuu' },
  register:   { en: 'Register New Pregnancy', am: 'አዲስ እርግዝና ምዝገባ', ti: 'ሓድሽ ጥንሲ ምምዝጋብ', om: 'Ulfaa Haaraa Galmeessi', sid: 'Ulfaa Haaraa Galmeessi', so: 'Diiwaanso Uur Cusub', aa: 'Diiwaanso Uur Cusub', wal: 'Ulfaa Haaraa Galmeessi', had: 'Ulfaa Haaraa Galmeessi' },
  lookup:     { en: 'Look Up Existing', am: 'ያለ ፈልግ', ti: 'ዘሎ ፈልጥ', om: 'Jiru Barbaadi', sid: 'Jiru Barbaadi', so: 'Raadi Kan Jira', aa: 'Raadi Kan Jira', wal: 'Jiru Barbaadi', had: 'Jiru Barbaadi' },
  mother:     { en: "Mother's Name", am: 'የእናቲቱ ስም', ti: 'ስም ኣደ', om: 'Maqaa Haadha', sid: 'Maqaa Haadha', so: 'Magaca Hooyadda', aa: 'Magaca Hooyadda', wal: 'Maqaa Haadha', had: 'Maqaa Haadha' },
  lmp:        { en: 'Last Menstrual Period (LMP)', am: 'የመጨረሻ ወር አበባ', ti: 'ናይ መጨረሻ ወርሓዊ ደም', om: 'Yeroo Dhiigni Dhufe', sid: 'Yeroo Dhiigni Dhufe', so: 'Xilliga Caadada Ugu Dambeeyay', aa: 'Xilliga Caadada Ugu Dambeeyay', wal: 'Yeroo Dhiigni Dhufe', had: 'Yeroo Dhiigni Dhufe' },
  record_id:  { en: 'Record ID', am: 'መዝገብ መለያ', ti: 'ናይ መዝገብ መለለዪ', om: 'ID Galmeessa', sid: 'ID Galmeessa', so: 'ID Diiwaanka', aa: 'ID Diiwaanka', wal: 'ID Galmeessa', had: 'ID Galmeessa' },
  ga_weeks:   { en: 'Gestational Age', am: 'የእርግዝና ዕድሜ', ti: 'ዕድሜ ጥንሲ', om: 'Umurii Ulfaa', sid: 'Umurii Ulfaa', so: 'Jirka Uurka', aa: 'Jirka Uurka', wal: 'Umurii Ulfaa', had: 'Umurii Ulfaa' },
  edd:        { en: 'Expected Due Date', am: 'የሚጠበቀው ቀን', ti: 'ዝጽበ ዕለት', om: 'Guyyaa Eegamu', sid: 'Guyyaa Eegamu', so: 'Taariikhda La Filayo', aa: 'Taariikhda La Filayo', wal: 'Guyyaa Eegamu', had: 'Guyyaa Eegamu' },
  weeks:      { en: 'weeks', am: 'ሳምንት', ti: 'ሰሙናት', om: 'torban', sid: 'torban', so: 'toddobaad', aa: 'toddobaad', wal: 'torban', had: 'torban' },
  weeks_left: { en: 'weeks remaining', am: 'ሳምንት ቀርቷል', ti: 'ሰሙናት ተሪፉ', om: 'torban hafe', sid: 'torban hafe', so: 'toddobaad haray', aa: 'toddobaad haray', wal: 'torban hafe', had: 'torban hafe' },
  anc_done:   { en: 'ANC visits completed', am: 'ANC ጉብኝቶች ተጠናቅቋል', ti: 'ANC ምብጻሓት ተዛዚሙ', om: 'Daawwannaa ANC xumuraman', sid: 'Daawwannaa ANC xumuraman', so: 'Booqashooyinka ANC ee la dhammeeyay', aa: 'Booqashooyinka ANC ee la dhammeeyay', wal: 'Daawwannaa ANC xumuraman', had: 'Daawwannaa ANC xumuraman' },
  danger:     { en: ' Danger Signs — Go to Hospital Immediately', am: ' አደጋ ምልክቶች — ወዲያውኑ ሆስፒታል', ti: ' ሓደጋ ምልክታት — ሕጂ ሆስፒታል', om: ' Mallattoo Balaa — Hospitaala Deemi', sid: ' Mallattoo Balaa — Hospitaala Deemi', so: ' Calaamadaha Khatarada — Isbitaalka Aad u Tag', aa: ' Calaamadaha Khatarada — Isbitaalka Aad u Tag', wal: ' Mallattoo Balaa — Hospitaala Deemi', had: ' Mallattoo Balaa — Hospitaala Deemi' },
  next_visit: { en: 'Next ANC Visit', am: 'ቀጣይ ANC ጉብኝት', ti: 'ዝቕጽል ANC ምብጻሕ', om: 'Daawwannaa ANC Itti Aanaa', sid: 'Daawwannaa ANC Itti Aanaa', so: 'Booqashada ANC ee Xigta', aa: 'Booqashada ANC ee Xigta', wal: 'Daawwannaa ANC Itti Aanaa', had: 'Daawwannaa ANC Itti Aanaa' },
  trimester:  { en: 'Trimester', am: 'ሶስት ወር', ti: 'ሶስት ወርሒ', om: 'Sadarkaa Ulfaa', sid: 'Sadarkaa Ulfaa', so: 'Sadexdii Bilood', aa: 'Sadexdii Bilood', wal: 'Sadarkaa Ulfaa', had: 'Sadarkaa Ulfaa' },
  submit:     { en: 'Register', am: 'ምዝገባ', ti: 'ምምዝጋብ', om: 'Galmeessi', sid: 'Galmeessi', so: 'Diiwaanso', aa: 'Diiwaanso', wal: 'Galmeessi', had: 'Galmeessi' },
  load:       { en: 'Load', am: 'ጫን', ti: 'ጸዓን', om: "Fe'i", sid: "Fe'i", so: 'Soo Geli', aa: 'Soo Geli', wal: "Fe'i", had: "Fe'i" },
  age:        { en: 'Age', am: 'ዕድሜ', ti: 'ዕድሜ', om: 'Umurii', sid: 'Umurii', so: 'Da\'da', aa: 'Da\'da', wal: 'Umurii', had: 'Umurii' },
  phone:      { en: 'Phone', am: 'ስልክ', ti: 'ስልኪ', om: 'Bilbila', sid: 'Bilbila', so: 'Telefoon', aa: 'Telefoon', wal: 'Bilbila', had: 'Bilbila' },
  kebele:     { en: 'Kebele', am: 'ቀበሌ', ti: 'ቀበሌ', om: 'Ganda', sid: 'Ganda', so: 'Kebele', aa: 'Kebele', wal: 'Ganda', had: 'Ganda' },
  registered: { en: ' Registered! ID:', am: ' ተመዝግቧል! መለያ:', ti: ' ተመዝጊቡ! ID:', om: ' Galmaaye! ID:', sid: ' Galmaaye! ID:', so: ' Waa la diiwaangeliyay! ID:', aa: ' Waa la diiwaangeliyay! ID:', wal: ' Galmaaye! ID:', had: ' Galmaaye! ID:' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

const URGENCY_COLOR = { emergency: '#c62828', urgent: '#e65100', visit_soon: '#f57f17' };

export default function PregnancyTracker({ lang = 'en' }) {
  const [mode, setMode] = useState('lookup');
  const [recordId, setRecordId] = useState('');
  const [schedule, setSchedule] = useState(null);
  const [loading, setLoading] = useState(false);
  const [form, setForm] = useState({ mother_name: '', lmp_date: '', age: '', phone: '', kebele: '' });
  const [registered, setRegistered] = useState(null);

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  async function handleRegister(e) {
    e.preventDefault();
    setLoading(true);
    try {
      const data = await registerPregnancy({ ...form, age: parseInt(form.age) || 0 });
      setRegistered(data);
      if (data.record_id) {
        setRecordId(data.record_id);
        const sched = await fetchPregnancySchedule(data.record_id, lang);
        setSchedule(sched);
        setMode('lookup');
      }
    } finally {
      setLoading(false);
    }
  }

  async function handleLoad() {
    if (!recordId.trim()) return;
    setLoading(true);
    try {
      const data = await fetchPregnancySchedule(recordId.trim().toUpperCase(), lang);
      setSchedule(data);
    } finally {
      setLoading(false);
    }
  }

  const inputStyle = { width: '100%', padding: '0.5rem 0.8rem', borderRadius: 8, border: '1px solid #ccc', fontSize: '1rem', boxSizing: 'border-box' };
  const labelStyle = { display: 'block', fontWeight: 600, marginBottom: 4, color: '#333', fontSize: '0.9rem' };

  return (
    <div style={{ padding: '1rem', maxWidth: 680, margin: '0 auto' }}>
      <h2 style={{ marginBottom: '1rem' }}>{t('title', lang)}</h2>

      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
        {['lookup', 'register'].map(m => (
          <button key={m} onClick={() => setMode(m)}
            style={{ flex: 1, padding: '0.5rem', borderRadius: 8, border: '2px solid #1565c0', background: mode === m ? '#1565c0' : '#fff', color: mode === m ? '#fff' : '#1565c0', fontWeight: 600, cursor: 'pointer' }}>
            {m === 'lookup' ? t('lookup', lang) : t('register', lang)}
          </button>
        ))}
      </div>

      {mode === 'lookup' && (
        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
          <input value={recordId} onChange={e => setRecordId(e.target.value.toUpperCase())}
            placeholder={t('record_id', lang)} onKeyDown={e => e.key === 'Enter' && handleLoad()}
            style={{ flex: 1, padding: '0.6rem 1rem', borderRadius: 8, border: '1px solid #ccc', fontSize: '1rem' }} />
          <button onClick={handleLoad} disabled={loading}
            style={{ padding: '0.6rem 1.2rem', borderRadius: 8, background: '#1565c0', color: '#fff', border: 'none', fontWeight: 600, cursor: 'pointer' }}>
            {loading ? '…' : t('load', lang)}
          </button>
        </div>
      )}

      {mode === 'register' && (
        <form onSubmit={handleRegister} style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1.5rem' }}>
          <div style={{ gridColumn: '1 / -1' }}>
            <label style={labelStyle}>{t('mother', lang)} *</label>
            <input required value={form.mother_name} onChange={e => set('mother_name', e.target.value)} style={inputStyle} />
          </div>
          <div>
            <label style={labelStyle}>{t('lmp', lang)} *</label>
            <input type="date" required value={form.lmp_date} onChange={e => set('lmp_date', e.target.value)} style={inputStyle} />
          </div>
          <div>
            <label style={labelStyle}>{t('age', lang)}</label>
            <input type="number" value={form.age} onChange={e => set('age', e.target.value)} style={inputStyle} placeholder="e.g. 24" />
          </div>
          <div>
            <label style={labelStyle}>{t('phone', lang)}</label>
            <input value={form.phone} onChange={e => set('phone', e.target.value)} style={inputStyle} placeholder="+251..." />
          </div>
          <div>
            <label style={labelStyle}>{t('kebele', lang)}</label>
            <input value={form.kebele} onChange={e => set('kebele', e.target.value)} style={inputStyle} />
          </div>
          <div style={{ gridColumn: '1 / -1' }}>
            <button type="submit" disabled={loading}
              style={{ width: '100%', padding: '0.7rem', borderRadius: 8, background: '#1565c0', color: '#fff', border: 'none', fontWeight: 700, fontSize: '1rem', cursor: 'pointer' }}>
              {loading ? '…' : t('submit', lang)}
            </button>
          </div>
        </form>
      )}

      {registered && <div style={{ background: '#e8f5e9', borderRadius: 8, padding: '0.75rem', marginBottom: '1rem', color: '#2e7d32', fontWeight: 600 }}>
        {t('registered', lang)} {registered.record_id} · EDD: {registered.edd} · GA: {registered.gestational_age_weeks}w
      </div>}

      {schedule && !schedule.error && (
        <div>
          <div style={{ background: '#e3f2fd', borderRadius: 10, padding: '1rem', marginBottom: '1rem' }}>
            <div style={{ fontWeight: 700, fontSize: '1.05rem' }}>{schedule.mother_name}</div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '0.5rem', marginTop: '0.75rem' }}>
              <Stat label={t('ga_weeks', lang)} value={`${schedule.gestational_age_weeks}w`} />
              <Stat label={t('trimester', lang)} value={schedule.trimester} />
              <Stat label={t('weeks_left', lang)} value={`${schedule.weeks_remaining}w`} />
              <Stat label={t('edd', lang)} value={schedule.edd} />
              <Stat label={t('anc_done', lang)} value={`${schedule.completed_visits}/${schedule.total_visits}`} />
            </div>
          </div>

          {schedule.next_visit && (
            <div style={{ background: '#fff8e1', borderRadius: 8, padding: '0.75rem', marginBottom: '1rem', borderLeft: '4px solid #f9a825' }}>
              <div style={{ fontWeight: 600 }}>{t('next_visit', lang)}: {schedule.next_visit.label_en}</div>
              <div style={{ fontSize: '0.85rem', color: '#666', marginTop: 4 }}>Due: {schedule.next_visit.due_date}</div>
              <div style={{ fontSize: '0.82rem', color: '#555', marginTop: 4 }}>{schedule.next_visit.key_actions_en?.join(' · ')}</div>
            </div>
          )}

          <details style={{ marginBottom: '1rem' }}>
            <summary style={{ fontWeight: 700, cursor: 'pointer', color: '#c62828', padding: '0.5rem 0' }}>{t('danger', lang)}</summary>
            <div style={{ marginTop: '0.5rem', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
              {schedule.danger_signs?.map(d => (
                <div key={d.id} style={{ display: 'flex', justifyContent: 'space-between', background: '#fff', borderRadius: 6, padding: '0.4rem 0.75rem', border: '1px solid #eee' }}>
                  <span>{d.sign}</span>
                  <span style={{ fontWeight: 700, color: URGENCY_COLOR[d.urgency] || '#333', fontSize: '0.8rem' }}>{d.urgency.replace('_', ' ').toUpperCase()}</span>
                </div>
              ))}
            </div>
          </details>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
            {schedule.schedule?.map(v => (
              <div key={v.visit_number} style={{ background: v.status === 'done' ? '#e8f5e9' : v.status === 'overdue' ? '#ffebee' : '#f5f5f5', borderRadius: 8, padding: '0.6rem 1rem', borderLeft: `4px solid ${v.status === 'done' ? '#2e7d32' : v.status === 'overdue' ? '#c62828' : '#bbb'}` }}>
                <div style={{ fontWeight: 600 }}>{v.label_en}</div>
                <div style={{ fontSize: '0.8rem', color: '#666' }}>Due: {v.due_date} · {v.status}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div style={{ background: '#fff', borderRadius: 8, padding: '0.5rem 0.75rem', textAlign: 'center' }}>
      <div style={{ fontSize: '1.1rem', fontWeight: 800, color: '#1565c0' }}>{value}</div>
      <div style={{ fontSize: '0.72rem', color: '#777' }}>{label}</div>
    </div>
  );
}
