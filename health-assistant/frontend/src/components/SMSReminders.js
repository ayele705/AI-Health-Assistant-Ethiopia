import React, { useState, useEffect } from 'react';
import { reminderSubscribe, reminderList, reminderUnsubscribe, smsSend } from '../api';

const L = {
  title:      { en: ' SMS Reminders', am: ' SMS ማስታወሻዎች', ti: ' SMS ዘኪሮታት', om: ' Yaadachiisa SMS', sid: ' Yaadachiisa SMS', so: ' Xusuusinta SMS', aa: ' Xusuusinta SMS', wal: ' Yaadachiisa SMS', had: ' Yaadachiisa SMS' },
  subscribe:  { en: 'Add Reminder', am: 'ማስታወሻ ጨምር', ti: 'ዘኪሮ ወስኽ', om: 'Yaadachiisa Dabali', sid: 'Yaadachiisa Dabali', so: 'Ku Dar Xusuusin', aa: 'Ku Dar Xusuusin', wal: 'Yaadachiisa Dabali', had: 'Yaadachiisa Dabali' },
  active:     { en: 'Active Reminders', am: 'ንቁ ማስታወሻዎች', ti: 'ንቡር ዘኪሮታት', om: 'Yaadachiisa Hojjataa', sid: 'Yaadachiisa Hojjataa', so: 'Xusuusinta Firfircoon', aa: 'Xusuusinta Firfircoon', wal: 'Yaadachiisa Hojjataa', had: 'Yaadachiisa Hojjataa' },
  name:       { en: 'Patient Name', am: 'የታካሚ ስም', ti: 'ስም ሕሙም', om: 'Maqaa Dhukkubsataa', sid: 'Maqaa Dhukkubsataa', so: 'Magaca Bukaanka', aa: 'Magaca Bukaanka', wal: 'Maqaa Dhukkubsataa', had: 'Maqaa Dhukkubsataa' },
  phone:      { en: 'Phone (+251...)', am: 'ስልክ (+251...)', ti: 'ስልኪ (+251...)', om: 'Bilbila (+251...)', sid: 'Bilbila (+251...)', so: 'Telefoon (+251...)', aa: 'Telefoon (+251...)', wal: 'Bilbila (+251...)', had: 'Bilbila (+251...)' },
  medication: { en: 'Medication', am: 'መድሃኒት', ti: 'መድሃኒት', om: 'Qorichaa', sid: 'Qorichaa', so: 'Daawada', aa: 'Daawada', wal: 'Qorichaa', had: 'Qorichaa' },
  time:       { en: 'Reminder Time', am: 'የማስታወሻ ጊዜ', ti: 'ጊዜ ዘኪሮ', om: 'Yeroo Yaadachiisaa', sid: 'Yeroo Yaadachiisaa', so: 'Waqtiga Xusuusinta', aa: 'Waqtiga Xusuusinta', wal: 'Yeroo Yaadachiisaa', had: 'Yeroo Yaadachiisaa' },
  language:   { en: 'Language', am: 'ቋንቋ', ti: 'ቋንቋ', om: 'Afaan', sid: 'Afaan', so: 'Luqadda', aa: 'Luqadda', wal: 'Afaan', had: 'Afaan' },
  start:      { en: 'Start Date', am: 'መጀመሪያ ቀን', ti: 'ዕለት ምጅማር', om: 'Guyyaa Jalqabaa', sid: 'Guyyaa Jalqabaa', so: 'Taariikhda Bilowga', aa: 'Taariikhda Bilowga', wal: 'Guyyaa Jalqabaa', had: 'Guyyaa Jalqabaa' },
  end:        { en: 'End Date (optional)', am: 'መጨረሻ ቀን (አማራጭ)', ti: 'ዕለት መወዳእታ', om: 'Guyyaa Xumuraa', sid: 'Guyyaa Xumuraa', so: 'Taariikhda Dhamaadka (ikhtiyaari)', aa: 'Taariikhda Dhamaadka (ikhtiyaari)', wal: 'Guyyaa Xumuraa', had: 'Guyyaa Xumuraa' },
  save:       { en: 'Subscribe', am: 'ምዝገባ', ti: 'ምምዝጋብ', om: 'Galmeessi', sid: 'Galmeessi', so: 'Diiwaanso', aa: 'Diiwaanso', wal: 'Galmeessi', had: 'Galmeessi' },
  cancel:     { en: 'Cancel', am: 'ሰርዝ', ti: 'ሰርዝ', om: 'Haquu', sid: 'Haquu', so: 'Jooji', aa: 'Jooji', wal: 'Haquu', had: 'Haquu' },
  remove:     { en: 'Remove', am: 'አስወግድ', ti: 'ኣወግድ', om: 'Kaasi', sid: 'Kaasi', so: 'Ka Saar', aa: 'Ka Saar', wal: 'Kaasi', had: 'Kaasi' },
  send_test:  { en: 'Send Test SMS', am: 'ሙከራ SMS ላክ', ti: 'ሙከራ SMS ስደድ', om: 'SMS Qormaataa Ergi', sid: 'SMS Qormaataa Ergi', so: 'Dir SMS Tijaabo', aa: 'Dir SMS Tijaabo', wal: 'SMS Qormaataa Ergi', had: 'SMS Qormaataa Ergi' },
  test_phone: { en: 'Phone for test', am: 'ሙከራ ስልክ', ti: 'ሙከራ ስልኪ', om: 'Bilbila Qormaataa', sid: 'Bilbila Qormaataa', so: 'Telefoon Tijaabada', aa: 'Telefoon Tijaabada', wal: 'Bilbila Qormaataa', had: 'Bilbila Qormaataa' },
  test_msg:   { en: 'Test message', am: 'ሙከራ መልዕክት', ti: 'ሙከራ መልእኽቲ', om: 'Ergaa Qormaataa', sid: 'Ergaa Qormaataa', so: 'Fariin Tijaabo', aa: 'Fariin Tijaabo', wal: 'Ergaa Qormaataa', had: 'Ergaa Qormaataa' },
  send:       { en: 'Send', am: 'ላክ', ti: 'ስደድ', om: 'Ergi', sid: 'Ergi', so: 'Dir', aa: 'Dir', wal: 'Ergi', had: 'Ergi' },
  morning:    { en: 'Morning (7am)', am: 'ጠዋት (7 ሰዓት)', ti: 'ንጉሆ (7 ሰዓት)', om: 'Barii (7am)', sid: 'Barii (7am)', so: 'Subaxnimo (7am)', aa: 'Subaxnimo (7am)', wal: 'Barii (7am)', had: 'Barii (7am)' },
  afternoon:  { en: 'Afternoon (1pm)', am: 'ከሰዓት (1 ሰዓት)', ti: 'ቀትሪ (1 ሰዓት)', om: 'Guyyaa (1pm)', sid: 'Guyyaa (1pm)', so: 'Galabnimo (1pm)', aa: 'Galabnimo (1pm)', wal: 'Guyyaa (1pm)', had: 'Guyyaa (1pm)' },
  evening:    { en: 'Evening (8pm)', am: 'ምሽት (8 ሰዓት)', ti: 'ምሸት (8 ሰዓት)', om: 'Galgala (8pm)', sid: 'Galgala (8pm)', so: 'Fiidnimo (8pm)', aa: 'Fiidnimo (8pm)', wal: 'Galgala (8pm)', had: 'Galgala (8pm)' },
  simulated:  { en: ' SMS simulation mode (set AT_API_KEY in .env to send real SMS)', am: ' SMS ሙከራ ሁነታ', ti: ' SMS ሙከራ ሁነታ', om: ' Haala Qormaataa SMS', sid: ' Haala Qormaataa SMS', so: ' Qaabka Tijaabada SMS', aa: ' Qaabka Tijaabada SMS', wal: ' Haala Qormaataa SMS', had: ' Haala Qormaataa SMS' },
  success:    { en: ' Subscribed!', am: ' ተመዝግቧል!', ti: ' ተመዝጊቡ!', om: ' Galmaaye!', sid: ' Galmaaye!', so: ' Waa la diiwaangeliyay!', aa: ' Waa la diiwaangeliyay!', wal: ' Galmaaye!', had: ' Galmaaye!' },
  sent_ok:    { en: ' SMS sent (simulated)', am: ' SMS ተልኳል (ሙከራ)', ti: ' SMS ተሰዲዱ', om: ' SMS Ergame', sid: ' SMS Ergame', so: ' SMS La diray (tijaabo)', aa: ' SMS La diray (tijaabo)', wal: ' SMS Ergame', had: ' SMS Ergame' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

const LANGS = [['en','English'],['am','አማርኛ'],['ti','ትግርኛ'],['om','Oromoo']];
const TIMES = ['morning','afternoon','evening'];

export default function SMSReminders({ lang = 'en' }) {
  const [tab, setTab] = useState('active');
  const [reminders, setReminders] = useState([]);
  const [form, setForm] = useState({ patient_name:'', phone:'', medication_name:'', time_of_day:'morning', language:'en', start_date: new Date().toISOString().split('T')[0], end_date:'' });
  const [testPhone, setTestPhone] = useState('');
  const [testMsg, setTestMsg] = useState('Hello from Health Assistant! This is a test message.');
  const [feedback, setFeedback] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => { loadReminders(); }, []);

  async function loadReminders() {
    try { const d = await reminderList(); setReminders(d.reminders || []); } catch {}
  }

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }));

  async function handleSubscribe(e) {
    e.preventDefault();
    setLoading(true);
    setFeedback('');
    try {
      await reminderSubscribe(form);
      setFeedback(t('success', lang));
      setForm(f => ({ ...f, patient_name:'', phone:'', medication_name:'' }));
      await loadReminders();
      setTab('active');
    } catch { setFeedback('Error. Check connection.'); }
    finally { setLoading(false); }
  }

  async function handleRemove(id) {
    await reminderUnsubscribe(id);
    await loadReminders();
  }

  async function handleTestSend(e) {
    e.preventDefault();
    setLoading(true);
    setFeedback('');
    try {
      await smsSend(testPhone, testMsg);
      setFeedback(t('sent_ok', lang));
    } catch { setFeedback('Send failed.'); }
    finally { setLoading(false); }
  }

  const inputStyle = { width:'100%', padding:'0.5rem 0.8rem', borderRadius:8, border:'1px solid #ccc', fontSize:'0.95rem', boxSizing:'border-box' };
  const labelStyle = { display:'block', fontWeight:600, marginBottom:4, color:'#333', fontSize:'0.85rem' };

  return (
    <div style={{ padding:'1rem', maxWidth:680, margin:'0 auto' }}>
      <h2 style={{ marginBottom:'0.5rem' }}>{t('title', lang)}</h2>
      <div style={{ background:'#fff3cd', borderRadius:8, padding:'0.5rem 1rem', marginBottom:'1rem', fontSize:'0.82rem', color:'#856404' }}>
        {t('simulated', lang)}
      </div>

      {/* Tabs */}
      <div style={{ display:'flex', gap:'0.5rem', marginBottom:'1.5rem' }}>
        {['active','subscribe','test'].map(tb => (
          <button key={tb} onClick={() => setTab(tb)}
            style={{ flex:1, padding:'0.5rem', borderRadius:8, border:'2px solid #1565c0', background: tab===tb ? '#1565c0':'#fff', color: tab===tb ? '#fff':'#1565c0', fontWeight:600, cursor:'pointer', textTransform:'capitalize' }}>
            {tb === 'active' ? t('active', lang) : tb === 'subscribe' ? t('subscribe', lang) : t('send_test', lang)}
          </button>
        ))}
      </div>

      {feedback && <div style={{ background:'#e8f5e9', borderRadius:8, padding:'0.6rem 1rem', marginBottom:'1rem', color:'#2e7d32', fontWeight:600 }}>{feedback}</div>}

      {/* Active reminders */}
      {tab === 'active' && (
        reminders.length === 0
          ? <p style={{ color:'#666' }}>No active reminders. Add one using the Subscribe tab.</p>
          : <div style={{ display:'flex', flexDirection:'column', gap:'0.6rem' }}>
              {reminders.map(r => (
                <div key={r.id} style={{ background:'#f5f5f5', borderRadius:10, padding:'0.8rem 1rem', display:'flex', justifyContent:'space-between', alignItems:'center', border:'1px solid #e0e0e0' }}>
                  <div>
                    <div style={{ fontWeight:700 }}>{r.patient_name}</div>
                    <div style={{ fontSize:'0.85rem', color:'#555' }}>{r.medication_name} · {r.time_of_day}</div>
                    <div style={{ fontSize:'0.78rem', color:'#888' }}>{r.phone} · {r.language}</div>
                  </div>
                  <button onClick={() => handleRemove(r.id)}
                    style={{ background:'#c62828', color:'#fff', border:'none', borderRadius:6, padding:'4px 12px', cursor:'pointer', fontWeight:600, fontSize:'0.82rem' }}>
                    {t('remove', lang)}
                  </button>
                </div>
              ))}
            </div>
      )}

      {/* Subscribe form */}
      {tab === 'subscribe' && (
        <form onSubmit={handleSubscribe} style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:'0.9rem' }}>
          <div>
            <label style={labelStyle}>{t('name', lang)} *</label>
            <input required value={form.patient_name} onChange={e => set('patient_name', e.target.value)} style={inputStyle} />
          </div>
          <div>
            <label style={labelStyle}>{t('phone', lang)} *</label>
            <input required value={form.phone} onChange={e => set('phone', e.target.value)} style={inputStyle} placeholder="+251911..." />
          </div>
          <div style={{ gridColumn:'1 / -1' }}>
            <label style={labelStyle}>{t('medication', lang)} *</label>
            <input required value={form.medication_name} onChange={e => set('medication_name', e.target.value)} style={inputStyle} placeholder="e.g. Metformin 500mg" />
          </div>
          <div>
            <label style={labelStyle}>{t('time', lang)}</label>
            <select value={form.time_of_day} onChange={e => set('time_of_day', e.target.value)} style={inputStyle}>
              {TIMES.map(tm => <option key={tm} value={tm}>{t(tm, lang)}</option>)}
            </select>
          </div>
          <div>
            <label style={labelStyle}>{t('language', lang)}</label>
            <select value={form.language} onChange={e => set('language', e.target.value)} style={inputStyle}>
              {LANGS.map(([code, name]) => <option key={code} value={code}>{name}</option>)}
            </select>
          </div>
          <div>
            <label style={labelStyle}>{t('start', lang)}</label>
            <input type="date" value={form.start_date} onChange={e => set('start_date', e.target.value)} style={inputStyle} />
          </div>
          <div>
            <label style={labelStyle}>{t('end', lang)}</label>
            <input type="date" value={form.end_date} onChange={e => set('end_date', e.target.value)} style={inputStyle} />
          </div>
          <div style={{ gridColumn:'1 / -1' }}>
            <button type="submit" disabled={loading}
              style={{ width:'100%', padding:'0.7rem', borderRadius:8, background:'#1565c0', color:'#fff', border:'none', fontWeight:700, fontSize:'1rem', cursor:'pointer' }}>
              {loading ? '…' : t('save', lang)}
            </button>
          </div>
        </form>
      )}

      {/* Test SMS */}
      {tab === 'test' && (
        <form onSubmit={handleTestSend} style={{ display:'flex', flexDirection:'column', gap:'0.9rem' }}>
          <div>
            <label style={labelStyle}>{t('test_phone', lang)}</label>
            <input required value={testPhone} onChange={e => setTestPhone(e.target.value)} style={inputStyle} placeholder="+251911..." />
          </div>
          <div>
            <label style={labelStyle}>{t('test_msg', lang)}</label>
            <textarea value={testMsg} onChange={e => setTestMsg(e.target.value)} rows={4} style={{ ...inputStyle, resize:'vertical' }} />
          </div>
          <button type="submit" disabled={loading}
            style={{ padding:'0.7rem', borderRadius:8, background:'#2e7d32', color:'#fff', border:'none', fontWeight:700, fontSize:'1rem', cursor:'pointer' }}>
            {loading ? '…' : t('send', lang)}
          </button>
        </form>
      )}
    </div>
  );
}
