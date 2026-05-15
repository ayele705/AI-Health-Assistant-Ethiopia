import React, { useState } from 'react';
import { fetchVaccineSchedule, addVaccineRecord, registerChild } from '../api';

const L = {
  title:      { en: ' Vaccination Tracker', am: ' የክትባት ክትትል', ti: ' ክታበት ምክትታል', om: ' Talaallii Hordofuu', sid: ' Talaallii Hordofuu', so: ' Raadraaca Tallaalka', aa: ' Raadraaca Tallaalka', wal: ' Talaallii Hordofuu', had: ' Talaallii Hordofuu' },
  child_id:   { en: 'Enter Child ID', am: 'የህጻኑ መለያ ያስገቡ', ti: 'ናይ ቆልዓ መለለዪ ኣእቱ', om: "ID Daa'imaa galchi", sid: "ID Daa'imaa galchi", so: 'Geli ID Ilmaha', aa: 'Geli ID Ilmaha', wal: "ID Daa'imaa galchi", had: "ID Daa'imaa galchi" },
  load:       { en: 'Load Schedule', am: 'ሰሌዳ ጫን', ti: 'መደብ ጸዓን', om: "Karoora Fe'i", sid: "Karoora Fe'i", so: 'Soo Geli Jadwalka', aa: 'Soo Geli Jadwalka', wal: "Karoora Fe'i", had: "Karoora Fe'i" },
  register:   { en: '+ Register New Child', am: '+ አዲስ ህጻን ይመዝግቡ', ti: '+ ሓዲሽ ቆልዓ ምዝገባ', om: "+ Daa'ima Haaraa Galmeessi", sid: "+ Daa'ima Haaraa Galmeessi", so: '+ Diiwaanso Ilmo Cusub', aa: '+ Diiwaanso Ilmo Cusub', wal: "+ Daa'ima Haaraa Galmeessi", had: "+ Daa'ima Haaraa Galmeessi" },
  name:       { en: 'Child name', am: 'የህጻኑ ስም', ti: 'ስም ቆልዓ', om: "Maqaa daa'imaa", sid: "Maqaa daa'imaa", so: 'Magaca ilmaha', aa: 'Magaca ilmaha', wal: "Maqaa daa'imaa", had: "Maqaa daa'imaa" },
  dob:        { en: 'Date of birth', am: 'የልደት ቀን', ti: 'ዕለት ምደት', om: 'Guyyaa dhalootaa', sid: 'Guyyaa dhalootaa', so: 'Taariikhda dhalashada', aa: 'Taariikhda dhalashada', wal: 'Guyyaa dhalootaa', had: 'Guyyaa dhalootaa' },
  sex:        { en: 'Sex', am: 'ጾታ', ti: 'ጾታ', om: 'Saala', sid: 'Saala', so: 'Jinsiga', aa: 'Jinsiga', wal: 'Saala', had: 'Saala' },
  male:       { en: 'Male', am: 'ወንድ', ti: 'ተባዕታይ', om: 'Dhiira', sid: 'Dhiira', so: 'Lab', aa: 'Lab', wal: 'Dhiira', had: 'Dhiira' },
  female:     { en: 'Female', am: 'ሴት', ti: 'ኣንስታይ', om: 'Dhalaa', sid: 'Dhalaa', so: 'Dheddig', aa: 'Dheddig', wal: 'Dhalaa', had: 'Dhalaa' },
  save:       { en: 'Register', am: 'ይመዝግቡ', ti: 'ምዝገባ', om: 'Galmeessi', sid: 'Galmeessi', so: 'Diiwaanso', aa: 'Diiwaanso', wal: 'Galmeessi', had: 'Galmeessi' },
  cancel:     { en: 'Cancel', am: 'ሰርዝ', ti: 'ሰርዝ', om: 'Haqi', sid: 'Haqi', so: 'Jooji', aa: 'Jooji', wal: 'Haqi', had: 'Haqi' },
  registered: { en: ' Child registered! ID:', am: ' ህጻን ተመዝግቧል! መለያ:', ti: ' ቆልዓ ተመዝጊቡ! ID:', om: " Daa'imni galmaaye! ID:", sid: " Daa'imni galmaaye! ID:", so: ' Ilmaha waa la diiwaangeliyay! ID:', aa: ' Ilmaha waa la diiwaangeliyay! ID:', wal: " Daa'imni galmaaye! ID:", had: " Daa'imni galmaaye! ID:" },
  given:      { en: ' Given', am: ' ተሰጥቷል', ti: ' ተዋሂቡ', om: ' Kenname', sid: ' Kenname', so: ' La siiyay', aa: ' La siiyay', wal: ' Kenname', had: ' Kenname' },
  overdue:    { en: ' Overdue', am: ' ዘግይቷል', ti: ' ዘግዩ', om: ' Yeroo Darbee', sid: ' Yeroo Darbee', so: ' Waqtigii dhaafay', aa: ' Waqtigii dhaafay', wal: ' Yeroo Darbee', had: ' Yeroo Darbee' },
  due_soon:   { en: '🟡 Due Soon', am: '🟡 ቅርብ ጊዜ', ti: '🟡 ቀሚጢ', om: '🟡 Dhiyoo', sid: '🟡 Dhiyoo', so: '🟡 Waqtigiisu dhow yahay', aa: '🟡 Waqtigiisu dhow yahay', wal: '🟡 Dhiyoo', had: '🟡 Dhiyoo' },
  upcoming:   { en: ' Upcoming', am: ' መጪ', ti: ' ዝመጽእ', om: ' Dhufaa', sid: ' Dhufaa', so: ' Soo socda', aa: ' Soo socda', wal: ' Dhufaa', had: ' Dhufaa' },
  mark_given: { en: 'Mark as Given', am: 'ተሰጥቷል ምልክት', ti: 'ተዋሂቡ ምልክት', om: 'Kenname Godhi', sid: 'Kenname Godhi', so: 'Ku Calaamadee La Siiyay', aa: 'Ku Calaamadee La Siiyay', wal: 'Kenname Godhi', had: 'Kenname Godhi' },
  completion: { en: 'Completion', am: 'ማጠናቀቂያ', ti: 'ምውዳእ', om: 'Xumura', sid: 'Xumura', so: 'Dhammaystirka', aa: 'Dhammaystirka', wal: 'Xumura', had: 'Xumura' },
  alert:      { en: '️ Overdue vaccines', am: '️ ዘግይተዋል', ti: '️ ዘግዮም', om: '️ Talaallii Yeroo Darbee', sid: '️ Talaallii Yeroo Darbee', so: '️ Tallaalka waqtigiisii dhaafay', aa: '️ Tallaalka waqtigiisii dhaafay', wal: '️ Talaallii Yeroo Darbee', had: '️ Talaallii Yeroo Darbee' },
  days:       { en: 'days', am: 'ቀናት', ti: 'መዓልቲ', om: 'guyyaa', sid: 'guyyaa', so: 'maalmood', aa: 'maalmood', wal: 'guyyaa', had: 'guyyaa' },
  hint:       { en: 'No child ID yet? Register a new child below.', am: 'የህጻኑ መለያ የለዎትም? ከታች አዲስ ህጻን ይመዝግቡ።', ti: 'ID ቆልዓ የብልካን? ኣብ ታሕቲ ሓዲሽ ቆልዓ ምዝገባ።', om: "ID daa'imaa hin qabduu? Daa'ima haaraa galmaa'i.", sid: "ID daa'imaa hin qabduu? Daa'ima haaraa galmaa'i.", so: 'ID ilmo ma lihid? Diiwaanso ilmo cusub hoose.', aa: 'ID ilmo ma lihid? Diiwaanso ilmo cusub hoose.', wal: "ID daa'imaa hin qabduu? Daa'ima haaraa galmaa'i.", had: "ID daa'imaa hin qabduu? Daa'ima haaraa galmaa'i." },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

const STATUS_COLOR  = { given: '#e8f5e9', overdue: '#ffebee', due_soon: '#fff8e1', upcoming: '#f5f5f5' };
const STATUS_BORDER = { given: '#2e7d32', overdue: '#c62828', due_soon: '#f9a825', upcoming: '#bbb' };

export default function VaccinationTracker({ lang = 'en' }) {
  const [childId, setChildId]   = useState('');
  const [schedule, setSchedule] = useState(null);
  const [loading, setLoading]   = useState(false);
  const [marking, setMarking]   = useState(null);
  const [showReg, setShowReg]   = useState(false);
  const [regForm, setRegForm]   = useState({ name: '', date_of_birth: '', sex: 'male' });
  const [regMsg, setRegMsg]     = useState('');
  const [saving, setSaving]     = useState(false);

  async function loadSchedule() {
    if (!childId.trim()) return;
    setLoading(true);
    try {
      const data = await fetchVaccineSchedule(childId.trim().toUpperCase());
      setSchedule(data);
    } finally {
      setLoading(false);
    }
  }

  async function markGiven(vaccine) {
    setMarking(vaccine.id);
    try {
      await addVaccineRecord(childId.trim().toUpperCase(), {
        vaccine_id: vaccine.id,
        vaccine_name: vaccine.name,
        date_given: new Date().toISOString().split('T')[0],
      });
      await loadSchedule();
    } finally {
      setMarking(null);
    }
  }

  async function handleRegister() {
    if (!regForm.name || !regForm.date_of_birth) return;
    setSaving(true);
    try {
      const data = await registerChild(regForm);
      if (data.child_id) {
        setRegMsg(`${t('registered', lang)} ${data.child_id}`);
        setChildId(data.child_id);
        setShowReg(false);
        setRegForm({ name: '', date_of_birth: '', sex: 'male' });
        const sched = await fetchVaccineSchedule(data.child_id);
        setSchedule(sched);
      }
    } finally {
      setSaving(false);
    }
  }

  return (
    <div style={{ padding: '1rem', maxWidth: 680, margin: '0 auto' }}>
      <h2 style={{ marginBottom: '1rem' }}>{t('title', lang)}</h2>

      {/* Search bar */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '0.5rem' }}>
        <input
          value={childId}
          onChange={e => setChildId(e.target.value.toUpperCase())}
          placeholder={t('child_id', lang)}
          onKeyDown={e => e.key === 'Enter' && loadSchedule()}
          style={{ flex: 1, padding: '0.6rem 1rem', borderRadius: 8, border: '1px solid #ccc', fontSize: '1rem' }}
        />
        <button
          onClick={loadSchedule}
          disabled={loading}
          style={{ padding: '0.6rem 1.2rem', borderRadius: 8, background: '#1565c0', color: '#fff', border: 'none', fontWeight: 600, cursor: 'pointer' }}>
          {loading ? '…' : t('load', lang)}
        </button>
      </div>

      {/* Hint + register toggle */}
      <p style={{ fontSize: '0.8rem', color: '#888', marginBottom: 8 }}>{t('hint', lang)}</p>
      <button
        onClick={() => setShowReg(!showReg)}
        style={{ marginBottom: 12, padding: '0.4rem 1rem', borderRadius: 8, background: '#2e7d32', color: '#fff', border: 'none', cursor: 'pointer', fontSize: '0.85rem' }}>
        {t('register', lang)}
      </button>

      {/* Registration form */}
      {showReg && (
        <div style={{ background: '#e8f5e9', borderRadius: 10, padding: '1rem', marginBottom: 16 }}>
          <input
            placeholder={t('name', lang)}
            value={regForm.name}
            onChange={e => setRegForm({ ...regForm, name: e.target.value })}
            style={{ display: 'block', width: '100%', marginBottom: 8, padding: '0.5rem', borderRadius: 6, border: '1px solid #ccc', boxSizing: 'border-box' }}
          />
          <input
            type="date"
            value={regForm.date_of_birth}
            onChange={e => setRegForm({ ...regForm, date_of_birth: e.target.value })}
            style={{ display: 'block', width: '100%', marginBottom: 8, padding: '0.5rem', borderRadius: 6, border: '1px solid #ccc', boxSizing: 'border-box' }}
          />
          <select
            value={regForm.sex}
            onChange={e => setRegForm({ ...regForm, sex: e.target.value })}
            style={{ display: 'block', width: '100%', marginBottom: 12, padding: '0.5rem', borderRadius: 6, border: '1px solid #ccc', boxSizing: 'border-box' }}>
            <option value="male">{t('male', lang)}</option>
            <option value="female">{t('female', lang)}</option>
          </select>
          <div style={{ display: 'flex', gap: 8 }}>
            <button
              onClick={handleRegister}
              disabled={saving}
              style={{ padding: '0.5rem 1.2rem', borderRadius: 8, background: '#1565c0', color: '#fff', border: 'none', cursor: 'pointer', fontWeight: 600 }}>
              {saving ? '…' : t('save', lang)}
            </button>
            <button
              onClick={() => setShowReg(false)}
              style={{ padding: '0.5rem 1rem', borderRadius: 8, background: '#ccc', border: 'none', cursor: 'pointer' }}>
              {t('cancel', lang)}
            </button>
          </div>
        </div>
      )}

      {/* Success message */}
      {regMsg && (
        <div style={{ background: '#e8f5e9', borderRadius: 8, padding: '0.6rem 1rem', marginBottom: 12, color: '#2e7d32', fontWeight: 600 }}>
          {regMsg}
        </div>
      )}

      {schedule?.error && <div style={{ color: '#c62828' }}>{schedule.error}</div>}

      {schedule && !schedule.error && (
        <>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', background: '#e3f2fd', borderRadius: 10, padding: '0.75rem 1rem' }}>
            <div>
              <div style={{ fontWeight: 700, fontSize: '1.05rem' }}>{schedule.child_name}</div>
              <div style={{ fontSize: '0.85rem', color: '#555' }}>{schedule.given_count} / {schedule.total_vaccines} vaccines</div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#1565c0' }}>{schedule.completion_percent}%</div>
              <div style={{ fontSize: '0.75rem', color: '#777' }}>{t('completion', lang)}</div>
            </div>
          </div>

          {schedule.alert && (
            <div style={{ background: '#ffebee', borderRadius: 8, padding: '0.6rem 1rem', marginBottom: '1rem', color: '#c62828', fontWeight: 600 }}>
              {t('alert', lang)}: {schedule.overdue?.join(', ')}
            </div>
          )}

          {schedule.due_soon?.length > 0 && (
            <div style={{ background: '#fff8e1', borderRadius: 8, padding: '0.6rem 1rem', marginBottom: '1rem', color: '#f57f17' }}>
              🟡 {t('due_soon', lang)}: {schedule.due_soon.map(d => `${d.name} (${d.days_until} ${t('days', lang)})`).join(', ')}
            </div>
          )}

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
            {schedule.schedule?.map(v => (
              <div key={v.id} style={{ background: STATUS_COLOR[v.status], borderRadius: 8, padding: '0.7rem 1rem', borderLeft: `4px solid ${STATUS_BORDER[v.status]}`, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <div style={{ fontWeight: 600 }}>{v.name}</div>
                  <div style={{ fontSize: '0.8rem', color: '#666', marginTop: 2 }}>{v.description_en?.slice(0, 80)}</div>
                  <div style={{ fontSize: '0.78rem', color: '#888', marginTop: 2 }}>Due: {v.due_date}</div>
                </div>
                <div style={{ minWidth: 100, textAlign: 'right' }}>
                  {v.status === 'given' && (
                    <span style={{ color: '#2e7d32', fontWeight: 700 }}>{t('given', lang)}</span>
                  )}
                  {(v.status === 'overdue' || v.status === 'due_soon') && (
                    <button
                      onClick={() => markGiven(v)}
                      disabled={marking === v.id}
                      style={{ background: v.status === 'overdue' ? '#c62828' : '#f9a825', color: '#fff', border: 'none', borderRadius: 6, padding: '4px 10px', cursor: 'pointer', fontSize: '0.8rem', fontWeight: 600 }}>
                      {marking === v.id ? '…' : t('mark_given', lang)}
                    </button>
                  )}
                  {v.status === 'upcoming' && (
                    <span style={{ color: '#999', fontSize: '0.8rem' }}>{v.days_until > 0 ? `${v.days_until}d` : ''}</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
