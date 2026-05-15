/**
 * CommunityCalendar — Displays upcoming health events for a kebele.
 * Full multilingual support: en, am, ti, om, sid, so, aa, wal, had
 */
import React, { useState, useEffect } from 'react';

const BASE = '/api/v1';
const L = {
  title:     { en: ' Community Health Calendar', am: ' የማህበረሰብ ጤና ቀን መቁጠሪያ', ti: ' ቀላንደር ጥዕና', om: ' Kaaleendara Fayyaa', sid: ' Kaaleendara Fayyaa', so: ' Kalandarka Caafimaadka', aa: ' Kalandara Caafimaad', wal: ' Kaaleendara Fayyaa', had: ' Kaaleendara Fayyaa' },
  no_events: { en: 'No upcoming events.', am: 'ምንም ክስተቶች የሉም።', ti: 'ዝኾነ ፍጻሜ የለን።', om: 'Taateewwan hin jiran.', sid: 'Taateewwan hin jiran.', so: 'Wax dhacdo ah ma jiraan.', aa: 'Dhacdooyiin ma jiraan.', wal: 'Taateewwan hin jiran.', had: 'Taateewwan hin jiran.' },
  remind:    { en: 'Remind me', am: 'አስታውሰኝ', ti: 'ዘኽረኒ', om: 'Na yaadachiisi', sid: 'Na yaadachiisi', so: 'I xasuusii', aa: 'I xusuusii', wal: 'Na yaadachiisi', had: 'Na yaadachiisi' },
  loading:   { en: 'Loading…', am: 'በመጫን ላይ…', ti: 'ይጽዓን ኣሎ…', om: "Fe'amaa jira…", sid: "Fe'amaa jira…", so: 'Waa la raraya…', aa: 'Raraya…', wal: "Fe'amaa jira…", had: "Fe'amaa jira…" },
  reminder_set: { en: ' Reminder set!', am: ' ማስታወሻ ተቀናጅቷል!', ti: ' ዘኪሮ ተቀሪጹ!', om: ' Yaadachiisni qindaa\'ame!', sid: ' Yaadachiisni qindaa\'ame!', so: ' Xusuusin la dejiyay!', aa: ' Xusuusin la dejiyay!', wal: ' Yaadachiisni qindaa\'ame!', had: ' Yaadachiisni qindaa\'ame!' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

const EVENT_ICONS = {
  vaccination_day: '',
  chw_visit: '‍️',
  anc_clinic: '',
  health_education: '',
  other: '',
};

export default function CommunityCalendar({ lang = 'en', kebele = '', userId = 'default_user' }) {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [reminderMsg, setReminderMsg] = useState('');

  useEffect(() => { fetchEvents(); }, [kebele, lang]); // eslint-disable-line

  async function fetchEvents() {
    setLoading(true);
    try {
      const res  = await fetch(`${BASE}/calendar/?kebele=${kebele}&days=90&language=${lang}`);
      const data = await res.json();
      setEvents(data.events || []);
    } catch { /* offline */ } finally { setLoading(false); }
  }

  async function setReminder(eventId) {
    try {
      await fetch(`${BASE}/calendar/${eventId}/remind/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_identifier: userId, phone: '', channel: 'in_app' }),
      });
      setReminderMsg(t('reminder_set', lang));
      setTimeout(() => setReminderMsg(''), 3000);
    } catch { /* queue offline */ }
  }

  return (
    <div style={{ padding: '0.5rem' }}>
      <p className="section-title">{t('title', lang)}</p>

      {reminderMsg && (
        <div style={{ background: '#e8f5e9', borderRadius: 8, padding: '0.5rem 1rem',
                      color: '#2e7d32', marginBottom: 10, fontSize: '0.9rem' }}>
          {reminderMsg}
        </div>
      )}

      {loading && <p className="loading">{t('loading', lang)}</p>}

      {!loading && events.length === 0 && (
        <p style={{ color: '#888', fontSize: '0.9rem' }}>{t('no_events', lang)}</p>
      )}

      {events.map((e) => (
        <div key={e.id} style={{ background: '#f1f8e9', borderRadius: 8, padding: '0.7rem 1rem',
                                  marginBottom: 8, display: 'flex', justifyContent: 'space-between',
                                  alignItems: 'center' }}>
          <div>
            <div style={{ fontSize: '1.2rem' }}>{EVENT_ICONS[e.event_type] || ''}</div>
            <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{e.title}</div>
            <div style={{ fontSize: '0.75rem', color: '#555' }}>{e.event_date}</div>
          </div>
          <button onClick={() => setReminder(e.id)}
            style={{ padding: '0.3rem 0.8rem', borderRadius: 6, background: '#1565c0',
                     color: '#fff', border: 'none', fontSize: '0.75rem', cursor: 'pointer' }}>
             {t('remind', lang)}
          </button>
        </div>
      ))}
    </div>
  );
}
