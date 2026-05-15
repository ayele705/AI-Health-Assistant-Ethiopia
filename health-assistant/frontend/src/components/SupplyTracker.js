/**
 * SupplyTracker — HEW stock reporting and shortage alerts.
 * Full multilingual: en, am, ti, om, sid, so, aa, wal, had
 */
import React, { useState, useEffect } from 'react';

const BASE = '/api/v1';

const L = {
  title:      { en: ' Supply Tracker', am: ' አቅርቦት መከታተያ', ti: ' ክትትል ቅርሲ', om: ' Hordoffii Meeshaalee', sid: ' Hordoffii Meeshaalee', so: ' Raadraaca Sahayda', aa: ' Raadraaca Sahayda', wal: ' Hordoffii Meeshaalee', had: ' Hordoffii Meeshaalee' },
  kebele:     { en: 'Kebele / Health Post', am: 'ቀበሌ / ጤና ጣቢያ', ti: 'ቀበሌ / ጥዕና ጣቢያ', om: 'Ganda / Buufata Fayyaa', sid: 'Ganda / Buufata Fayyaa', so: 'Xaafada / Xarunta Caafimaadka', aa: 'Xaafada / Xarunta Caafimaadka', wal: 'Ganda / Buufata Fayyaa', had: 'Ganda / Buufata Fayyaa' },
  hew_name:   { en: 'HEW Name', am: 'HEW ስም', ti: 'ስም HEW', om: 'Maqaa HEW', sid: 'Maqaa HEW', so: 'Magaca HEW', aa: 'Magaca HEW', wal: 'Maqaa HEW', had: 'Maqaa HEW' },
  qty:        { en: 'Qty', am: 'መጠን', ti: 'መጠን', om: 'Baay\'ina', sid: 'Baay\'ina', so: 'Tirada', aa: 'Tirada', wal: 'Baay\'ina', had: 'Baay\'ina' },
  weekly:     { en: 'Weekly use', am: 'ሳምንታዊ አጠቃቀም', ti: 'ሳምንታዊ ጥቕሚ', om: 'Torban keessatti', sid: 'Torban keessatti', so: 'Isticmaalka toddobaadlaha', aa: 'Isticmaalka toddobaadlaha', wal: 'Torban keessatti', had: 'Torban keessatti' },
  submit:     { en: 'Submit Report', am: 'ሪፖርት ያስገቡ', ti: 'ሪፖርት ኣቕርብ', om: 'Gabaasa Galchi', sid: 'Gabaasa Galchi', so: 'Gudbi Warbixinta', aa: 'Gudbi Warbixinta', wal: 'Gabaasa Galchi', had: 'Gabaasa Galchi' },
  loading:    { en: 'Submitting…', am: 'በማስገባት ላይ…', ti: 'ይቐርብ ኣሎ…', om: 'Galchaa jira…', sid: 'Galchaa jira…', so: 'Waa la gudbinayaa…', aa: 'Waa la gudbinayaa…', wal: 'Galchaa jira…', had: 'Galchaa jira…' },
  no_shortage:{ en: ' All supplies are adequate.', am: ' ሁሉም አቅርቦቶች በቂ ናቸው።', ti: ' ኩሎም ቅርሲ ኣኻሊ ኢዩ።', om: ' Meeshaaleen hundi gahaa dha.', sid: ' Meeshaaleen hundi gahaa dha.', so: ' Dhammaan sahayda waa ku filan tahay.', aa: ' Dhammaan sahayda waa ku filan tahay.', wal: ' Meeshaaleen hundi gahaa dha.', had: ' Meeshaaleen hundi gahaa dha.' },
  shortages:  { en: 'Shortages detected:', am: 'ጉድለቶች ተገኝተዋል:', ti: 'ጉድለታት ተረኺቡ:', om: 'Dhabiinsi argame:', sid: 'Dhabiinsi argame:', so: 'Yarida la ogaaday:', aa: 'Yarida la ogaaday:', wal: 'Dhabiinsi argame:', had: 'Dhabiinsi argame:' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

const LEVEL_COLORS = {
  out_of_stock: '#c62828', critical: '#e65100', low: '#f57f17', adequate: '#2e7d32',
};
const LEVEL_BG = {
  out_of_stock: '#ffebee', critical: '#fbe9e7', low: '#fff9c4', adequate: '#e8f5e9',
};

export default function SupplyTracker({ lang = 'en' }) {
  const [supplies, setSupplies] = useState([]);
  const [kebele, setKebele]     = useState('');
  const [hewName, setHewName]   = useState('');
  const [quantities, setQty]    = useState({});
  const [weekly, setWeekly]     = useState({});
  const [result, setResult]     = useState(null);
  const [loading, setLoading]   = useState(false);

  useEffect(() => {
    fetch(`${BASE}/supply/list/?language=${lang}`)
      .then((r) => r.json())
      .then((d) => setSupplies(d.supplies || []))
      .catch(() => {});
  }, [lang]);

  async function submitReport() {
    if (!kebele) return;
    setLoading(true);
    const reports = supplies.map((s) => ({
      supply_id: s.id,
      quantity: parseInt(quantities[s.id] || 0),
      weekly_consumption: parseInt(weekly[s.id] || 1),
    }));
    try {
      const res = await fetch(`${BASE}/supply/report/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ kebele, hew_name: hewName, language: lang, reports }),
      });
      setResult(await res.json());
    } catch { /* offline */ } finally { setLoading(false); }
  }

  const CATEGORIES = [...new Set(supplies.map((s) => s.category))];

  return (
    <div style={{ padding: '0.5rem' }}>
      <p className="section-title">{t('title', lang)}</p>

      <div style={{ display: 'flex', gap: 8, marginBottom: 10 }}>
        <input placeholder={t('kebele', lang)} value={kebele} onChange={(e) => setKebele(e.target.value)}
          style={{ flex: 2, padding: '0.4rem', borderRadius: 6, border: '1px solid #ccc' }} />
        <input placeholder={t('hew_name', lang)} value={hewName} onChange={(e) => setHewName(e.target.value)}
          style={{ flex: 2, padding: '0.4rem', borderRadius: 6, border: '1px solid #ccc' }} />
      </div>

      {CATEGORIES.map((cat) => (
        <div key={cat} style={{ marginBottom: 12 }}>
          <p style={{ fontWeight: 700, fontSize: '0.8rem', color: '#555', textTransform: 'uppercase', marginBottom: 4 }}>{cat}</p>
          {supplies.filter((s) => s.category === cat).map((s) => (
            <div key={s.id} style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6, background: '#f5f5f5', borderRadius: 6, padding: '0.4rem 0.6rem' }}>
              <span style={{ flex: 3, fontSize: '0.82rem' }}>{s.name}</span>
              <input type="number" placeholder={t('qty', lang)} min="0"
                value={quantities[s.id] || ''}
                onChange={(e) => setQty({ ...quantities, [s.id]: e.target.value })}
                style={{ flex: 1, padding: '0.3rem', borderRadius: 4, border: '1px solid #ccc', fontSize: '0.8rem' }} />
              <input type="number" placeholder={t('weekly', lang)} min="0"
                value={weekly[s.id] || ''}
                onChange={(e) => setWeekly({ ...weekly, [s.id]: e.target.value })}
                style={{ flex: 1, padding: '0.3rem', borderRadius: 4, border: '1px solid #ccc', fontSize: '0.8rem' }} />
            </div>
          ))}
        </div>
      ))}

      <button onClick={submitReport} disabled={!kebele || loading}
        style={{ padding: '0.5rem 1.5rem', borderRadius: 8, background: '#1565c0', color: '#fff', border: 'none', cursor: 'pointer', fontWeight: 700 }}>
        {loading ? t('loading', lang) : t('submit', lang)}
      </button>

      {result && (
        <div style={{ marginTop: 14 }}>
          {result.shortages.length === 0 ? (
            <div style={{ background: '#e8f5e9', borderRadius: 8, padding: '0.7rem', color: '#2e7d32', fontWeight: 600 }}>
              {t('no_shortage', lang)}
            </div>
          ) : (
            <div>
              <p style={{ fontWeight: 700, color: '#c62828', marginBottom: 6 }}>
                ️ {t('shortages', lang)} {result.shortages.length}
              </p>
              {result.shortages.map((s, i) => (
                <div key={i} style={{ background: LEVEL_BG[s.level], borderRadius: 6, padding: '0.5rem 0.8rem', marginBottom: 6, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>{s.name}</span>
                  <span style={{ fontSize: '0.75rem', color: LEVEL_COLORS[s.level], fontWeight: 700 }}>{s.level_label}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
