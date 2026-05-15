import React, { useState } from 'react';
import { searchMedications, fetchMedicationDetail } from '../api';

const L = {
  title:        { en: ' Medication Lookup', am: ' መድሃኒት ፍለጋ', ti: ' መድሃኒት ምድላይ', om: ' Qorichaa Barbaadi', sid: ' Qorichaa Barbaadi', so: ' Raadinta Daawada', aa: ' Raadinta Daawada', wal: ' Qorichaa Barbaadi', had: ' Qorichaa Barbaadi' },
  placeholder:  { en: 'Search by name or condition (e.g. paracetamol, malaria)…', am: 'በስም ወይም ሁኔታ ይፈልጉ (ለምሳሌ ፓራሲታሞል፣ ወባ)…', ti: 'ብስም ወይ ሕማም ፈልጥ…', om: 'Maqaa ykn dhukkubaatiin barbaadi…', sid: 'Maqaa ykn dhukkubaatiin barbaadi…', so: 'Ku raadi magaca ama xaaladda…', aa: 'Ku raadi magaca ama xaaladda…', wal: 'Maqaa ykn dhukkubaatiin barbaadi…', had: 'Maqaa ykn dhukkubaatiin barbaadi…' },
  search:       { en: 'Search', am: 'ፈልግ', ti: 'ፈልጥ', om: 'Barbaadi', sid: 'Barbaadi', so: 'Raadi', aa: 'Raadi', wal: 'Barbaadi', had: 'Barbaadi' },
  no_results:   { en: 'No medications found.', am: 'ምንም መድሃኒት አልተገኘም።', ti: 'ዝኾነ መድሃኒት ኣይተረኽበን።', om: 'Qorichaan hin argamne.', sid: 'Qorichaan hin argamne.', so: 'Dawo lama helin.', aa: 'Dawo lama helin.', wal: 'Qorichaan hin argamne.', had: 'Qorichaan hin argamne.' },
  dosage_adult: { en: 'Adult Dose', am: 'የጎልማሳ መጠን', ti: 'ናይ ዓቢ መጠን', om: 'Hamma Guddaa', sid: 'Hamma Guddaa', so: 'Qadarka Dadka Waaweyn', aa: 'Qadarka Dadka Waaweyn', wal: 'Hamma Guddaa', had: 'Hamma Guddaa' },
  dosage_child: { en: 'Child Dose', am: 'የህጻን መጠን', ti: 'ናይ ቆልዓ መጠን', om: 'Hamma Daa\'imaa', sid: 'Hamma Daa\'imaa', so: 'Qadarka Carruurta', aa: 'Qadarka Carruurta', wal: 'Hamma Daa\'imaa', had: 'Hamma Daa\'imaa' },
  side_effects: { en: 'Side Effects', am: 'የጎን ተጽዕኖዎች', ti: 'ናይ ጎኒ ሳዕቤናት', om: 'Miidhaa Biraa', sid: 'Miidhaa Biraa', so: 'Saameynta Dhinaca', aa: 'Saameynta Dhinaca', wal: 'Miidhaa Biraa', had: 'Miidhaa Biraa' },
  warnings:     { en: '️ Warnings', am: '️ ማስጠንቀቂያዎች', ti: '️ ምልክታት ጥንቃቐ', om: '️ Akeekkachiisa', sid: '️ Akeekkachiisa', so: '️ Digniin', aa: '️ Digniin', wal: '️ Akeekkachiisa', had: '️ Akeekkachiisa' },
  contraind:    { en: 'Do NOT use if', am: 'አይጠቀሙ ከሆነ', ti: 'ኣይትጠቐም እንተ', om: 'Hin fayyadamiin yoo', sid: 'Hin fayyadamiin yoo', so: 'HA isticmaalin haddii', aa: 'HA isticmaalin haddii', wal: 'Hin fayyadamiin yoo', had: 'Hin fayyadamiin yoo' },
  rx_required:  { en: 'Prescription required', am: 'ትዕዛዝ ያስፈልጋል', ti: 'ትዕዛዝ የድሊ', om: 'Ajaja barbaachisa', sid: 'Ajaja barbaachisa', so: 'Qorshaha dhakhtarka ayaa loo baahan yahay', aa: 'Qorshaha dhakhtarka ayaa loo baahan yahay', wal: 'Ajaja barbaachisa', had: 'Ajaja barbaachisa' },
  otc:          { en: 'Available without prescription', am: 'ያለ ትዕዛዝ ይገኛል', ti: 'ብዘይ ትዕዛዝ ይርከብ', om: 'Ajaja malee argama', sid: 'Ajaja malee argama', so: 'Qorshaha la\'aantii ayaa laga heli karaa', aa: 'Qorshaha la\'aantii ayaa laga heli karaa', wal: 'Ajaja malee argama', had: 'Ajaja malee argama' },
  who:          { en: 'WHO Essential Medicine', am: 'WHO አስፈላጊ መድሃኒት', ti: 'WHO ኣድላዪ መድሃኒት', om: 'Qorichaa WHO', sid: 'Qorichaa WHO', so: 'Daawada Muhiimka ah ee WHO', aa: 'Daawada Muhiimka ah ee WHO', wal: 'Qorichaa WHO', had: 'Qorichaa WHO' },
  back:         { en: '← Back', am: '← ተመለስ', ti: '← ተመለስ', om: '← Deebi\'i', sid: '← Deebi\'i', so: '← Dib u noqo', aa: '← Dib u noqo', wal: '← Deebi\'i', had: '← Deebi\'i' },
  offline_warn: { en: ' Offline — showing cached results', am: ' ኦፍላይን — የተቀመጡ ውጤቶች', ti: ' ኦፍላይን', om: ' Offline', sid: ' Offline', so: ' Offline — natiijadii kaydsan', aa: ' Offline — natiijadii kaydsan', wal: ' Offline', had: ' Offline' },
};

const t = (key, lang) => (L[key] || {})[lang] || (L[key] || {}).en || key;

export default function MedicationLookup({ lang = 'en' }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);
  const [offline, setOffline] = useState(false);

  async function handleSearch(e) {
    e.preventDefault();
    if (!query.trim()) return;
    setLoading(true);
    setSelected(null);
    try {
      const data = await searchMedications(query.trim(), lang);
      setResults(data.medications || []);
      setOffline(false);
    } catch {
      setOffline(true);
      setResults([]);
    } finally {
      setLoading(false);
    }
  }

  async function handleSelect(id) {
    setLoading(true);
    try {
      const data = await fetchMedicationDetail(id, lang);
      setSelected(data);
    } catch {
      setOffline(true);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="medication-lookup" style={{ padding: '1rem', maxWidth: 700, margin: '0 auto' }}>
      <h2 style={{ marginBottom: '1rem' }}>{t('title', lang)}</h2>

      {offline && (
        <div className="offline-banner" style={{ background: '#fff3cd', padding: '0.5rem 1rem', borderRadius: 6, marginBottom: '1rem' }}>
          {t('offline_warn', lang)}
        </div>
      )}

      <form onSubmit={handleSearch} style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.5rem' }}>
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder={t('placeholder', lang)}
          style={{ flex: 1, padding: '0.6rem 1rem', borderRadius: 8, border: '1px solid #ccc', fontSize: '1rem' }}
          aria-label={t('placeholder', lang)}
        />
        <button type="submit" disabled={loading}
          style={{ padding: '0.6rem 1.2rem', borderRadius: 8, background: '#2e7d32', color: '#fff', border: 'none', cursor: 'pointer', fontWeight: 600 }}>
          {loading ? '…' : t('search', lang)}
        </button>
      </form>

      {selected ? (
        <MedDetail med={selected} lang={lang} onBack={() => setSelected(null)} />
      ) : results !== null && (
        results.length === 0
          ? <p style={{ color: '#666' }}>{t('no_results', lang)}</p>
          : <MedList meds={results} lang={lang} onSelect={handleSelect} />
      )}
    </div>
  );
}

function MedList({ meds, lang, onSelect }) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
      {meds.map(m => (
        <button key={m.id} onClick={() => onSelect(m.id)}
          style={{ textAlign: 'left', padding: '0.9rem 1rem', borderRadius: 10, border: '1px solid #ddd', background: '#fff', cursor: 'pointer', boxShadow: '0 1px 3px rgba(0,0,0,0.08)' }}>
          <div style={{ fontWeight: 700, fontSize: '1rem', color: '#1b5e20' }}>{m.name}</div>
          <div style={{ fontSize: '0.85rem', color: '#555', marginTop: 2 }}>{m.generic_name} · {m.category?.replace(/_/g, ' ')}</div>
          <div style={{ fontSize: '0.82rem', color: '#777', marginTop: 4 }}>{m.description?.slice(0, 100)}…</div>
          <div style={{ marginTop: 6, display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            {m.who_essential && <span style={{ background: '#e8f5e9', color: '#2e7d32', borderRadius: 4, padding: '2px 7px', fontSize: '0.75rem' }}>WHO </span>}
            {m.prescription_required
              ? <span style={{ background: '#fff3e0', color: '#e65100', borderRadius: 4, padding: '2px 7px', fontSize: '0.75rem' }}>Rx</span>
              : <span style={{ background: '#e3f2fd', color: '#1565c0', borderRadius: 4, padding: '2px 7px', fontSize: '0.75rem' }}>OTC</span>}
            {m.available_in_ethiopia && <span style={{ background: '#f3e5f5', color: '#6a1b9a', borderRadius: 4, padding: '2px 7px', fontSize: '0.75rem' }}> Ethiopia</span>}
          </div>
        </button>
      ))}
    </div>
  );
}

function MedDetail({ med, lang, onBack }) {
  const t = (key) => (L[key] || {})[lang] || (L[key] || {}).en || key;
  const Section = ({ label, text }) => text ? (
    <div style={{ marginBottom: '1rem' }}>
      <div style={{ fontWeight: 600, color: '#333', marginBottom: 4 }}>{label}</div>
      <div style={{ color: '#555', lineHeight: 1.6 }}>{text}</div>
    </div>
  ) : null;

  return (
    <div style={{ background: '#fff', borderRadius: 12, padding: '1.2rem', boxShadow: '0 2px 8px rgba(0,0,0,0.1)' }}>
      <button onClick={onBack} style={{ background: 'none', border: 'none', color: '#2e7d32', cursor: 'pointer', fontWeight: 600, marginBottom: '1rem', fontSize: '0.95rem' }}>
        {t('back')}
      </button>
      <h3 style={{ margin: '0 0 0.3rem', color: '#1b5e20' }}>{med.name}</h3>
      <div style={{ color: '#777', fontSize: '0.85rem', marginBottom: '1rem' }}>{med.generic_name} · {med.category?.replace(/_/g, ' ')}</div>
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: '1rem' }}>
        {med.who_essential && <span style={{ background: '#e8f5e9', color: '#2e7d32', borderRadius: 4, padding: '2px 8px', fontSize: '0.8rem' }}>{t('who')}</span>}
        {med.prescription_required
          ? <span style={{ background: '#fff3e0', color: '#e65100', borderRadius: 4, padding: '2px 8px', fontSize: '0.8rem' }}>{t('rx_required')}</span>
          : <span style={{ background: '#e3f2fd', color: '#1565c0', borderRadius: 4, padding: '2px 8px', fontSize: '0.8rem' }}>{t('otc')}</span>}
      </div>
      <Section label="Description" text={med.description} />
      <Section label={t('dosage_adult')} text={med.dosage_adult} />
      <Section label={t('dosage_child')} text={med.dosage_child} />
      <Section label={t('side_effects')} text={med.side_effects} />
      {med.contraindications && (
        <div style={{ marginBottom: '1rem', background: '#fff3e0', borderRadius: 8, padding: '0.7rem 1rem' }}>
          <div style={{ fontWeight: 600, color: '#e65100', marginBottom: 4 }}>{t('contraind')}</div>
          <div style={{ color: '#555' }}>{med.contraindications}</div>
        </div>
      )}
      {med.warnings && (
        <div style={{ background: '#fff8e1', borderRadius: 8, padding: '0.7rem 1rem', borderLeft: '4px solid #f9a825' }}>
          <div style={{ fontWeight: 600, color: '#f57f17', marginBottom: 4 }}>{t('warnings')}</div>
          <div style={{ color: '#555' }}>{med.warnings}</div>
        </div>
      )}
    </div>
  );
}
