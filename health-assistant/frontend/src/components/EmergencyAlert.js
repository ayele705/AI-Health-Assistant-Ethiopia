/**
 * EmergencyAlert — Register emergency contacts + trigger alert with countdown.
 */
import React, { useState, useEffect, useRef } from 'react';

const BASE = '/api/v1';
const L = {
  title:       { en: ' Emergency Contacts', am: ' አስቸኳይ ዕውቂያዎች', ti: ' ህጹጽ ርክብ', om: ' Quunnamtii Ariifachiisaa', sid: ' Quunnamtii Ariifachiisaa', so: ' Xiriiriyayaasha Xaaladda Degdegga', aa: ' Xiriiriyayaasha Xaaladda Degdegga', wal: ' Quunnamtii Ariifachiisaa', had: ' Quunnamtii Ariifachiisaa' },
  add:         { en: '+ Add Contact', am: '+ ዕውቂያ ጨምር', ti: '+ ርክብ ወሰኽ', om: '+ Quunnamtii Dabaluu', sid: '+ Quunnamtii Dabaluu', so: '+ Ku Dar Xiriiriye', aa: '+ Ku Dar Xiriiriye', wal: '+ Quunnamtii Dabaluu', had: '+ Quunnamtii Dabaluu' },
  no_contacts: { en: '️ No emergency contacts registered. Add contacts to enable automatic alerts.', am: '️ ምንም አስቸኳይ ዕውቂያ የለም።', ti: '️ ህጹጽ ርክብ ኣይተመዝገበን።', om: '️ Quunnamtii ariifachiisaa hin galmoofne.', sid: '️ Quunnamtii ariifachiisaa hin galmoofne.', so: '️ Xiriiriye xaaladda degdegga ah ma jiro.', aa: '️ Xiriiriye xaaladda degdegga ah ma jiro.', wal: '️ Quunnamtii ariifachiisaa hin galmoofne.', had: '️ Quunnamtii ariifachiisaa hin galmoofne.' },
  send_alert:  { en: ' Send Emergency Alert', am: ' አስቸኳይ ማንቂያ ላክ', ti: ' ህጹጽ ምልክት ስደድ', om: ' Beeksisa Ariifachiisaa Ergi', sid: ' Beeksisa Ariifachiisaa Ergi', so: ' Dir Digniinta Xaaladda Degdegga', aa: ' Dir Digniinta Xaaladda Degdegga', wal: ' Beeksisa Ariifachiisaa Ergi', had: ' Beeksisa Ariifachiisaa Ergi' },
  cancel:      { en: 'Cancel', am: 'ሰርዝ', ti: 'ሰርዝ', om: 'Haqi', sid: 'Haqi', so: 'Jooji', aa: 'Jooji', wal: 'Haqi', had: 'Haqi' },
  sending:     { en: 'Sending in', am: 'በ', ti: 'ይስደድ', om: 'Ergamaa', sid: 'Ergamaa', so: 'Diraya', aa: 'Diraya', wal: 'Ergamaa', had: 'Ergamaa' },
  seconds:     { en: 'seconds…', am: 'ሰከንድ…', ti: 'ሰከንድ…', om: 'sekondii…', sid: 'sekondii…', so: 'ilbiriqsi…', aa: 'ilbiriqsi…', wal: 'sekondii…', had: 'sekondii…' },
  name:        { en: 'Name', am: 'ስም', ti: 'ስም', om: 'Maqaa', sid: 'Maqaa', so: 'Magac', aa: 'Magac', wal: 'Maqaa', had: 'Maqaa' },
  phone:       { en: 'Phone', am: 'ስልክ', ti: 'ስልኪ', om: 'Bilbila', sid: 'Bilbila', so: 'Telefoon', aa: 'Telefoon', wal: 'Bilbila', had: 'Bilbila' },
  relation:    { en: 'Relationship', am: 'ዝምድና', ti: 'ዝምድና', om: 'Hidhata', sid: 'Hidhata', so: 'Xiriirka', aa: 'Xiriirka', wal: 'Hidhata', had: 'Hidhata' },
  save:        { en: 'Save', am: 'አስቀምጥ', ti: 'ዕቀብ', om: 'Kuusi', sid: 'Kuusi', so: 'Keydi', aa: 'Keydi', wal: 'Kuusi', had: 'Kuusi' },
  alert_sent:  { en: ' Alert sent to', am: ' ማንቂያ ተልኳል ለ', ti: ' ምልክት ተሰዲዱ ናብ', om: ' Beeksisni ergame', sid: ' Beeksisni ergame', so: ' Digniinta la diray', aa: ' Digniinta la diray', wal: ' Beeksisni ergame', had: ' Beeksisni ergame' },
  contacts:    { en: 'contact(s).', am: 'ዕውቂያ(ዎች)።', ti: 'ርክብ(ታት)።', om: 'quunnamtii.', sid: 'quunnamtii.', so: 'xiriiriye(yaal).', aa: 'xiriiriye(yaal).', wal: 'quunnamtii.', had: 'quunnamtii.' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

export default function EmergencyAlert({ lang = 'en', userId = 'default_user',
                                          urgency, conditionSummary, location }) {
  const [contacts, setContacts]     = useState([]);
  const [showAdd, setShowAdd]       = useState(false);
  const [form, setForm]             = useState({ name: '', phone: '', relationship: '' });
  const [countdown, setCountdown]   = useState(null);
  const [alertSent, setAlertSent]   = useState(false);
  const timerRef           = useRef(null);
  const autoTriggeredRef   = useRef(false); // ensure auto-trigger fires only once

  useEffect(() => {
    fetchContacts();
  }, [userId]); // eslint-disable-line

  // Auto-trigger countdown when urgency is emergency — only once
  useEffect(() => {
    if (urgency === 'emergency' && contacts.length > 0 && !alertSent && !autoTriggeredRef.current) {
      autoTriggeredRef.current = true;
      startCountdown();
    }
  }, [urgency, contacts]); // eslint-disable-line

  async function fetchContacts() {
    try {
      const res  = await fetch(`${BASE}/emergency-contacts/?user_identifier=${userId}`);
      const data = await res.json();
      setContacts(data.contacts || []);
    } catch { /* offline */ }
  }

  async function addContact() {
    if (!form.name || !form.phone) return;
    try {
      await fetch(`${BASE}/emergency-contacts/create/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, user_identifier: userId }),
      });
      setForm({ name: '', phone: '', relationship: '' });
      setShowAdd(false);
      fetchContacts();
    } catch { /* queue offline */ }
  }

  async function deleteContact(id) {
    await fetch(`${BASE}/emergency-contacts/${id}/`, { method: 'DELETE' });
    fetchContacts();
  }

  function startCountdown() {
    setCountdown(10);
    timerRef.current = setInterval(() => {
      setCountdown((c) => {
        if (c <= 1) {
          clearInterval(timerRef.current);
          sendAlert();
          return null;
        }
        return c - 1;
      });
    }, 1000);
  }

  function cancelCountdown() {
    clearInterval(timerRef.current);
    setCountdown(null);
  }

  async function sendAlert() {
    setAlertSent(true);
    try {
      await fetch(`${BASE}/emergency-alert/send/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_identifier: userId,
          condition_summary: conditionSummary || 'Emergency',
          urgency_level: 'emergency',
          location_text: location || '',
          language: lang,
        }),
      });
    } catch { /* queued offline */ }
  }

  return (
    <div style={{ padding: '0.5rem' }}>
      <p className="section-title">{t('title', lang)}</p>

      {contacts.length === 0 && (
        <div style={{ background: '#fff3e0', borderRadius: 8, padding: '0.7rem 1rem',
                      color: '#e65100', fontSize: '0.85rem', marginBottom: 10 }}>
          {t('no_contacts', lang)}
        </div>
      )}

      {/* Countdown overlay */}
      {countdown !== null && (
        <div style={{ background: '#ffebee', border: '2px solid #c62828', borderRadius: 10,
                      padding: '1rem', textAlign: 'center', marginBottom: 12 }}>
          <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#c62828' }}>
             {t('sending', lang)} {countdown} {t('seconds', lang)}
          </div>
          <button onClick={cancelCountdown}
            style={{ marginTop: 8, padding: '0.4rem 1.2rem', borderRadius: 8,
                     background: '#555', color: '#fff', border: 'none', cursor: 'pointer' }}>
            {t('cancel', lang)}
          </button>
        </div>
      )}

      {alertSent && (
        <div style={{ background: '#e8f5e9', borderRadius: 8, padding: '0.7rem',
                      color: '#2e7d32', fontWeight: 600, marginBottom: 10 }}>
          {t('alert_sent', lang)} {contacts.length} {t('contacts', lang)}
        </div>
      )}

      {/* Contact list */}
      {contacts.map((c) => (
        <div key={c.id} style={{ display: 'flex', justifyContent: 'space-between',
                                  alignItems: 'center', background: '#f5f5f5',
                                  borderRadius: 8, padding: '0.5rem 0.8rem', marginBottom: 6 }}>
          <div>
            <strong>{c.name}</strong>
            <span style={{ color: '#555', fontSize: '0.8rem', marginLeft: 8 }}>{c.phone}</span>
            {c.relationship && <span style={{ color: '#888', fontSize: '0.75rem', marginLeft: 6 }}>({c.relationship})</span>}
          </div>
          <button onClick={() => deleteContact(c.id)}
            style={{ background: 'none', border: 'none', color: '#c62828', cursor: 'pointer', fontSize: '1rem' }}>
            
          </button>
        </div>
      ))}

      {/* Add contact form */}
      {showAdd ? (
        <div style={{ background: '#e3f2fd', borderRadius: 8, padding: '0.8rem', marginTop: 8 }}>
          {['name', 'phone', 'relation'].map((field) => (
            <input key={field}
              placeholder={t(field, lang)}
              value={form[field === 'relation' ? 'relationship' : field]}
              onChange={(e) => setForm({ ...form, [field === 'relation' ? 'relationship' : field]: e.target.value })}
              style={{ display: 'block', width: '100%', marginBottom: 6, padding: '0.4rem',
                       borderRadius: 6, border: '1px solid #ccc', boxSizing: 'border-box' }}
            />
          ))}
          <button onClick={addContact}
            style={{ padding: '0.4rem 1rem', borderRadius: 8, background: '#2e7d32',
                     color: '#fff', border: 'none', cursor: 'pointer', marginRight: 8 }}>
            {t('save', lang)}
          </button>
          <button onClick={() => setShowAdd(false)}
            style={{ padding: '0.4rem 1rem', borderRadius: 8, background: '#ccc',
                     border: 'none', cursor: 'pointer' }}>
            {t('cancel', lang)}
          </button>
        </div>
      ) : (
        contacts.length < 5 && (
          <button onClick={() => setShowAdd(true)}
            style={{ marginTop: 8, padding: '0.4rem 1rem', borderRadius: 8,
                     background: '#1565c0', color: '#fff', border: 'none', cursor: 'pointer' }}>
            {t('add', lang)}
          </button>
        )
      )}

      {/* Manual alert trigger */}
      {contacts.length > 0 && !countdown && !alertSent && (
        <button onClick={startCountdown}
          style={{ display: 'block', marginTop: 12, width: '100%', padding: '0.6rem',
                   borderRadius: 8, background: '#c62828', color: '#fff',
                   border: 'none', fontWeight: 700, cursor: 'pointer', fontSize: '1rem' }}>
          {t('send_alert', lang)}
        </button>
      )}
    </div>
  );
}
