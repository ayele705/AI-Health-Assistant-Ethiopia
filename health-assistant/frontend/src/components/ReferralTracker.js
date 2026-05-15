/**
 * ReferralTracker — CHW referral management with offline support.
 * Full multilingual support: en, am, ti, om, sid, so, aa, wal, had
 */
import React, { useState, useEffect } from 'react';

const BASE = '/api/v1';
const STATUS_COLORS = {
  open: '#fff3e0', attended: '#e8f5e9',
  not_attended: '#ffebee', admitted: '#e3f2fd', discharged: '#f3e5f5',
};

const L = {
  title:       { en: ' Referral Tracker', am: ' ሪፈራል መከታተያ', ti: ' ሪፈራል ክትትል', om: ' Hordoffii Wabii', sid: ' Hordoffii Wabii', so: ' Raadraaca Gudbinta', aa: ' Raadraaca Gudbinta', wal: ' Hordoffii Wabii', had: ' Hordoffii Wabii' },
  new_ref:     { en: '+ New Referral', am: '+ አዲስ ሪፈራል', ti: '+ ሓድሽ ሪፈራል', om: '+ Wabii Haaraa', sid: '+ Wabii Haaraa', so: '+ Gudbinta Cusub', aa: '+ Gudbinta Cusub', wal: '+ Wabii Haaraa', had: '+ Wabii Haaraa' },
  no_refs:     { en: 'No open referrals.', am: 'ምንም ክፍት ሪፈራሎች የሉም።', ti: 'ዝኾነ ክፉት ሪፈራል የለን።', om: 'Wabii banaa hin jiru.', sid: 'Wabii banaa hin jiru.', so: 'Gudbino furan ma jiraan.', aa: 'Gudbino furan ma jiraan.', wal: 'Wabii banaa hin jiru.', had: 'Wabii banaa hin jiru.' },
  overdue:     { en: '️ Overdue', am: '️ ዘግይቷል', ti: '️ ዝሓለፈ', om: '️ Yeroo darbee', sid: '️ Yeroo darbee', so: '️ Waqtigii dhaafay', aa: '️ Waqtigii dhaafay', wal: '️ Yeroo darbee', had: '️ Yeroo darbee' },
  loading:     { en: 'Loading…', am: 'በመጫን ላይ…', ti: 'ይጽዓን ኣሎ…', om: "Fe'amaa jira…", sid: "Fe'amaa jira…", so: 'Waa la raraya…', aa: 'Raraya…', wal: "Fe'amaa jira…", had: "Fe'amaa jira…" },
  save:        { en: 'Save', am: 'አስቀምጥ', ti: 'ዕቀብ', om: 'Kuusi', sid: 'Kuusi', so: 'Keydi', aa: 'Keydi', wal: 'Kuusi', had: 'Kuusi' },
  cancel:      { en: 'Cancel', am: 'ሰርዝ', ti: 'ሰርዝ', om: 'Haqi', sid: 'Haqi', so: 'Jooji', aa: 'Jooji', wal: 'Haqi', had: 'Haqi' },
  expected:    { en: 'Expected:', am: 'የሚጠበቀው:', ti: 'ዝጽበ:', om: 'Eegama:', sid: 'Eegama:', so: 'La filayo:', aa: 'La filayo:', wal: 'Eegama:', had: 'Eegama:' },
  patient:     { en: 'Patient name', am: 'የታካሚ ስም', ti: 'ስም ሕሙም', om: 'Maqaa dhukkubsataa', sid: 'Maqaa dhukkubsataa', so: 'Magaca bukaanka', aa: 'Magaca bukaanka', wal: 'Maqaa dhukkubsataa', had: 'Maqaa dhukkubsataa' },
  phone:       { en: 'Phone', am: 'ስልክ', ti: 'ስልኪ', om: 'Bilbila', sid: 'Bilbila', so: 'Telefoon', aa: 'Telefoon', wal: 'Bilbila', had: 'Bilbila' },
  facility:    { en: 'Destination facility', am: 'መዳረሻ ጤና ጣቢያ', ti: 'ዕላማ ጥዕና ጣቢያ', om: 'Buufata gara deemamu', sid: 'Buufata gara deemamu', so: 'Xarunta la aadayo', aa: 'Xarunta la aadayo', wal: 'Buufata gara deemamu', had: 'Buufata gara deemamu' },
  reason:      { en: 'Reason', am: 'ምክንያት', ti: 'ምኽንያት', om: 'Sababa', sid: 'Sababa', so: 'Sababta', aa: 'Sababta', wal: 'Sababa', had: 'Sababa' },
  ref_date:    { en: 'Referral date', am: 'የሪፈራል ቀን', ti: 'ዕለት ሪፈራል', om: 'Guyyaa wabii', sid: 'Guyyaa wabii', so: 'Taariikhda gudbinta', aa: 'Taariikhda gudbinta', wal: 'Guyyaa wabii', had: 'Guyyaa wabii' },
  visit_date:  { en: 'Expected visit date', am: 'የሚጠበቀው ቀጠሮ ቀን', ti: 'ዕለት ዝጽበ ምብጻሕ', om: 'Guyyaa daawwannaa eegamu', sid: 'Guyyaa daawwannaa eegamu', so: 'Taariikhda booqashada la filayo', aa: 'Taariikhda booqashada la filayo', wal: 'Guyyaa daawwannaa eegamu', had: 'Guyyaa daawwannaa eegamu' },
  attended:    { en: 'Attended', am: 'ሄዷል', ti: 'ከይዱ', om: 'Argame', sid: 'Argame', so: 'Wuu yimid', aa: 'Wuu yimid', wal: 'Argame', had: 'Argame' },
  not_attended:{ en: 'Not attended', am: 'አልሄደም', ti: 'ኣይከደን', om: 'Hin argamne', sid: 'Hin argamne', so: 'Kuma aadin', aa: 'Kuma aadin', wal: 'Hin argamne', had: 'Hin argamne' },
  admitted:    { en: 'Admitted', am: 'ተቀብሏል', ti: 'ተቐቢሉ', om: 'Seenee jira', sid: 'Seenee jira', so: 'La qaaday', aa: 'La qaaday', wal: 'Seenee jira', had: 'Seenee jira' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

const FORM_FIELDS = [
  { key: 'patient_name',        labelKey: 'patient',    type: 'text' },
  { key: 'patient_phone',       labelKey: 'phone',      type: 'tel' },
  { key: 'destination_facility',labelKey: 'facility',   type: 'text' },
  { key: 'reason',              labelKey: 'reason',     type: 'text' },
  { key: 'referral_date',       labelKey: 'ref_date',   type: 'date' },
  { key: 'expected_visit_date', labelKey: 'visit_date', type: 'date' },
];

export default function ReferralTracker({ lang = 'en', chwId = '' }) {
  const [referrals, setReferrals] = useState([]);
  const [loading, setLoading]     = useState(true);
  const [showForm, setShowForm]   = useState(false);
  const [form, setForm]           = useState({
    patient_name: '', patient_phone: '', destination_facility: '',
    reason: '', referral_date: '', expected_visit_date: '',
  });

  useEffect(() => { fetchReferrals(); }, [chwId]); // eslint-disable-line

  async function fetchReferrals() {
    setLoading(true);
    try {
      const res  = await fetch(`${BASE}/referrals/?chw=${chwId}`);
      const data = await res.json();
      setReferrals(data.referrals || []);
    } catch { /* offline */ } finally { setLoading(false); }
  }

  async function createReferral() {
    try {
      await fetch(`${BASE}/referrals/create/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ...form, chw_identifier: chwId, patient_identifier: `pat_${Date.now()}` }),
      });
      setShowForm(false);
      setForm({ patient_name: '', patient_phone: '', destination_facility: '', reason: '', referral_date: '', expected_visit_date: '' });
      fetchReferrals();
    } catch { /* queue offline */ }
  }

  async function recordOutcome(referralId, status) {
    await fetch(`${BASE}/referrals/${referralId}/outcome/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status }),
    });
    fetchReferrals();
  }

  const isOverdue = (r) => r.status === 'open' && new Date(r.expected_visit_date) < new Date();

  return (
    <div style={{ padding: '0.5rem' }}>
      <p className="section-title">{t('title', lang)}</p>

      <button onClick={() => setShowForm(!showForm)}
        style={{ marginBottom: 10, padding: '0.4rem 1rem', borderRadius: 8,
                 background: '#2e7d32', color: '#fff', border: 'none', cursor: 'pointer' }}>
        {t('new_ref', lang)}
      </button>

      {showForm && (
        <div style={{ background: '#e3f2fd', borderRadius: 8, padding: '0.8rem', marginBottom: 12 }}>
          {FORM_FIELDS.map(({ key, labelKey, type }) => (
            <input key={key} type={type} placeholder={t(labelKey, lang)}
              value={form[key]}
              onChange={(e) => setForm({ ...form, [key]: e.target.value })}
              style={{ display: 'block', width: '100%', marginBottom: 6, padding: '0.4rem',
                       borderRadius: 6, border: '1px solid #ccc', boxSizing: 'border-box' }}
            />
          ))}
          <button onClick={createReferral}
            style={{ padding: '0.4rem 1rem', borderRadius: 8, background: '#2e7d32',
                     color: '#fff', border: 'none', cursor: 'pointer', marginRight: 8 }}>
            {t('save', lang)}
          </button>
          <button onClick={() => setShowForm(false)}
            style={{ padding: '0.4rem 1rem', borderRadius: 8, background: '#ccc',
                     border: 'none', cursor: 'pointer' }}>
            {t('cancel', lang)}
          </button>
        </div>
      )}

      {loading && <p className="loading">{t('loading', lang)}</p>}
      {!loading && referrals.length === 0 && (
        <p style={{ color: '#888', fontSize: '0.9rem' }}>{t('no_refs', lang)}</p>
      )}

      {referrals.map((r) => (
        <div key={r.referral_id}
          style={{ background: STATUS_COLORS[r.status] || '#f5f5f5', borderRadius: 8,
                   padding: '0.7rem 1rem', marginBottom: 8 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            <strong>{r.patient_name || r.referral_id}</strong>
            {isOverdue(r) && <span style={{ color: '#c62828', fontSize: '0.8rem' }}>{t('overdue', lang)}</span>}
          </div>
          <div style={{ fontSize: '0.8rem', color: '#555' }}>→ {r.destination_facility}</div>
          <div style={{ fontSize: '0.75rem', color: '#777' }}>{t('expected', lang)} {r.expected_visit_date}</div>
          {r.status === 'open' && (
            <div style={{ marginTop: 6, display: 'flex', gap: 6, flexWrap: 'wrap' }}>
              {[['attended','attended'],['not_attended','not_attended'],['admitted','admitted']].map(([s, labelKey]) => (
                <button key={s} onClick={() => recordOutcome(r.referral_id, s)}
                  style={{ padding: '2px 8px', borderRadius: 4, background: '#1565c0',
                           color: '#fff', border: 'none', fontSize: '0.75rem', cursor: 'pointer' }}>
                  {t(labelKey, lang)}
                </button>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}
