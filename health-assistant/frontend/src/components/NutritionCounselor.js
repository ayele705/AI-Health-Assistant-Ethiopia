/**
 * NutritionCounselor — IYCF guidance, micronutrient deficiencies, SAM/MAM protocols.
 * Full multilingual: en, am, ti, om, sid, so, aa, wal, had
 */
import React, { useState } from 'react';

const BASE = '/api/v1';

const L = {
  title:      { en: ' Nutrition Counseling', am: ' የምግብ ምክር', ti: ' ምኽሪ ምግቢ', om: ' Gorsa Nyaataa', sid: ' Gorsa Nyaataa', so: ' Talooyinka Nafaqada', aa: ' Talooyinka Nafaqada', wal: ' Gorsa Nyaataa', had: ' Gorsa Nyaataa' },
  iycf:       { en: 'Infant Feeding', am: 'የሕፃን ምግብ', ti: 'ምግቢ ሕፃን', om: 'Nyaata Daa\'imaa', sid: 'Nyaata Daa\'imaa', so: 'Quudinta Ilmaha', aa: 'Quudinta Ilmaha', wal: 'Nyaata Daa\'imaa', had: 'Nyaata Daa\'imaa' },
  micronut:   { en: 'Micronutrients', am: 'ማይክሮ ንጥረ ነገሮች', ti: 'ማይክሮ ንጥረ ነገር', om: 'Nyaata Xiqqaa', sid: 'Nyaata Xiqqaa', so: 'Nafaqada Yar', aa: 'Nafaqada Yar', wal: 'Nyaata Xiqqaa', had: 'Nyaata Xiqqaa' },
  sam_mam:    { en: 'SAM/MAM Protocol', am: 'SAM/MAM ፕሮቶኮል', ti: 'SAM/MAM ፕሮቶኮል', om: 'Sirna SAM/MAM', sid: 'Sirna SAM/MAM', so: 'Xeerka SAM/MAM', aa: 'Xeerka SAM/MAM', wal: 'Sirna SAM/MAM', had: 'Sirna SAM/MAM' },
  age_months: { en: 'Child age (months)', am: 'የልጅ ዕድሜ (ወር)', ti: 'ዕድሜ ሕፃን (ወርሒ)', om: 'Umurii daa\'imaa (ji\'a)', sid: 'Umurii daa\'imaa (ji\'a)', so: 'Da\'da ilmaha (bilood)', aa: 'Da\'da ilmaha (bilood)', wal: 'Umurii daa\'imaa (ji\'a)', had: 'Umurii daa\'imaa (ji\'a)' },
  get_guide:  { en: 'Get Guidance', am: 'ምክር ያግኙ', ti: 'ምኽሪ ርኸብ', om: 'Gorsa Argadhu', sid: 'Gorsa Argadhu', so: 'Hel Talo', aa: 'Hel Talo', wal: 'Gorsa Argadhu', had: 'Gorsa Argadhu' },
  iron:       { en: 'Iron Deficiency', am: 'የብረት ዕጦት', ti: 'ጉድለት ሓጺን', om: 'Dhabiinsa Biroo', sid: 'Dhabiinsa Biroo', so: 'Yaraanta Birta', aa: 'Yaraanta Birta', wal: 'Dhabiinsa Biroo', had: 'Dhabiinsa Biroo' },
  vita:       { en: 'Vitamin A Deficiency', am: 'ቫይታሚን ኤ ዕጦት', ti: 'ጉድለት ቫይታሚን ኤ', om: 'Dhabiinsa Vitamin A', sid: 'Dhabiinsa Vitamin A', so: 'Yaraanta Fiitamiin A', aa: 'Yaraanta Fiitamiin A', wal: 'Dhabiinsa Vitamin A', had: 'Dhabiinsa Vitamin A' },
  zinc:       { en: 'Zinc Deficiency', am: 'ዚንክ ዕጦት', ti: 'ጉድለት ዚንክ', om: 'Dhabiinsa Zinc', sid: 'Dhabiinsa Zinc', so: 'Yaraanta Zinc', aa: 'Yaraanta Zinc', wal: 'Dhabiinsa Zinc', had: 'Dhabiinsa Zinc' },
  sam:        { en: 'SAM (Severe)', am: 'SAM (ከባድ)', ti: 'SAM (ከቢድ)', om: 'SAM (Cimaa)', sid: 'SAM (Cimaa)', so: 'SAM (Xoog leh)', aa: 'SAM (Xoog leh)', wal: 'SAM (Cimaa)', had: 'SAM (Cimaa)' },
  mam:        { en: 'MAM (Moderate)', am: 'MAM (መካከለኛ)', ti: 'MAM (ማእከላይ)', om: 'MAM (Giddugaleessa)', sid: 'MAM (Giddugaleessa)', so: 'MAM (Dhexdhexaad)', aa: 'MAM (Dhexdhexaad)', wal: 'MAM (Giddugaleessa)', had: 'MAM (Giddugaleessa)' },
  loading:    { en: 'Loading…', am: 'በመጫን ላይ…', ti: 'ይጽዓን ኣሎ…', om: 'Fe\'amaa jira…', sid: 'Fe\'amaa jira…', so: 'Waa la raraya…', aa: 'Waa la raraya…', wal: 'Fe\'amaa jira…', had: 'Fe\'amaa jira…' },
  signs:      { en: 'Signs:', am: 'ምልክቶች:', ti: 'ምልክታት:', om: 'Mallattoolee:', sid: 'Mallattoolee:', so: 'Calaamadaha:', aa: 'Calaamadaha:', wal: 'Mallattoolee:', had: 'Mallattoolee:' },
  foods:      { en: 'Recommended foods:', am: 'የሚመከሩ ምግቦች:', ti: 'ዝምከሩ ምግቢ:', om: 'Nyaata Gorsamee:', sid: 'Nyaata Gorsamee:', so: 'Cuntada la talinayo:', aa: 'Cuntada la talinayo:', wal: 'Nyaata Gorsamee:', had: 'Nyaata Gorsamee:' },
  tips:       { en: 'Tips:', am: 'ምክሮች:', ti: 'ምኽሪ:', om: 'Gorsa:', sid: 'Gorsa:', so: 'Talooyinka:', aa: 'Talooyinka:', wal: 'Gorsa:', had: 'Gorsa:' },
  action:     { en: 'Action:', am: 'እርምጃ:', ti: 'ስጉምቲ:', om: 'Tarkaanfii:', sid: 'Tarkaanfii:', so: 'Tallaabada:', aa: 'Tallaabada:', wal: 'Tarkaanfii:', had: 'Tarkaanfii:' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

export default function NutritionCounselor({ lang = 'en' }) {
  const [tab, setTab]         = useState('iycf');
  const [ageMonths, setAge]   = useState('');
  const [deficiency, setDef]  = useState('iron_deficiency');
  const [samMam, setSamMam]   = useState('SAM');
  const [result, setResult]   = useState(null);
  const [loading, setLoading] = useState(false);

  async function fetchIYCF() {
    if (!ageMonths) return;
    setLoading(true);
    try {
      const res = await fetch(`${BASE}/nutrition/iycf/?age_months=${ageMonths}&language=${lang}`);
      setResult(await res.json());
    } catch { /* offline */ } finally { setLoading(false); }
  }

  async function fetchMicronutrient() {
    setLoading(true);
    try {
      const res = await fetch(`${BASE}/nutrition/micronutrients/?deficiency=${deficiency}&language=${lang}`);
      setResult(await res.json());
    } catch { /* offline */ } finally { setLoading(false); }
  }

  async function fetchTherapeutic() {
    setLoading(true);
    try {
      const res = await fetch(`${BASE}/nutrition/therapeutic/?status=${samMam}&language=${lang}`);
      setResult(await res.json());
    } catch { /* offline */ } finally { setLoading(false); }
  }

  const TABS = [
    { id: 'iycf', labelKey: 'iycf' },
    { id: 'micronut', labelKey: 'micronut' },
    { id: 'sam_mam', labelKey: 'sam_mam' },
  ];

  return (
    <div style={{ padding: '0.5rem' }}>
      <p className="section-title">{t('title', lang)}</p>

      <div style={{ display: 'flex', gap: 6, marginBottom: 12, flexWrap: 'wrap' }}>
        {TABS.map(({ id, labelKey }) => (
          <button key={id} onClick={() => { setTab(id); setResult(null); }}
            style={{ padding: '0.35rem 0.8rem', borderRadius: 8, border: 'none',
                     background: tab === id ? '#2e7d32' : '#e0e0e0',
                     color: tab === id ? '#fff' : '#333', cursor: 'pointer', fontSize: '0.8rem' }}>
            {t(labelKey, lang)}
          </button>
        ))}
      </div>

      {/* IYCF tab */}
      {tab === 'iycf' && (
        <div style={{ background: '#f5f5f5', borderRadius: 8, padding: '0.8rem', marginBottom: 12 }}>
          <label style={{ fontSize: '0.85rem', fontWeight: 600 }}>{t('age_months', lang)}</label>
          <input type="number" value={ageMonths} onChange={(e) => setAge(e.target.value)}
            placeholder="e.g. 6" min="0" max="60"
            style={{ display: 'block', width: '100%', marginTop: 4, marginBottom: 8, padding: '0.4rem', borderRadius: 6, border: '1px solid #ccc', boxSizing: 'border-box' }} />
          <button onClick={fetchIYCF} disabled={!ageMonths || loading}
            style={{ padding: '0.4rem 1.2rem', borderRadius: 8, background: '#2e7d32', color: '#fff', border: 'none', cursor: 'pointer' }}>
            {loading ? t('loading', lang) : t('get_guide', lang)}
          </button>
        </div>
      )}

      {/* Micronutrient tab */}
      {tab === 'micronut' && (
        <div style={{ background: '#f5f5f5', borderRadius: 8, padding: '0.8rem', marginBottom: 12 }}>
          <div style={{ display: 'flex', gap: 6, marginBottom: 8, flexWrap: 'wrap' }}>
            {[['iron_deficiency', 'iron'], ['vitamin_a_deficiency', 'vita'], ['zinc_deficiency', 'zinc']].map(([val, labelKey]) => (
              <button key={val} onClick={() => setDef(val)}
                style={{ padding: '0.3rem 0.7rem', borderRadius: 6, border: '2px solid',
                         borderColor: deficiency === val ? '#e65100' : '#ccc',
                         background: deficiency === val ? '#fff3e0' : '#fff',
                         cursor: 'pointer', fontSize: '0.78rem' }}>
                {t(labelKey, lang)}
              </button>
            ))}
          </div>
          <button onClick={fetchMicronutrient} disabled={loading}
            style={{ padding: '0.4rem 1.2rem', borderRadius: 8, background: '#e65100', color: '#fff', border: 'none', cursor: 'pointer' }}>
            {loading ? t('loading', lang) : t('get_guide', lang)}
          </button>
        </div>
      )}

      {/* SAM/MAM tab */}
      {tab === 'sam_mam' && (
        <div style={{ background: '#f5f5f5', borderRadius: 8, padding: '0.8rem', marginBottom: 12 }}>
          <div style={{ display: 'flex', gap: 8, marginBottom: 8 }}>
            {[['SAM', 'sam'], ['MAM', 'mam']].map(([val, labelKey]) => (
              <button key={val} onClick={() => setSamMam(val)}
                style={{ padding: '0.4rem 1rem', borderRadius: 8, border: 'none',
                         background: samMam === val ? '#c62828' : '#e0e0e0',
                         color: samMam === val ? '#fff' : '#333', cursor: 'pointer', fontWeight: 600 }}>
                {t(labelKey, lang)}
              </button>
            ))}
          </div>
          <button onClick={fetchTherapeutic} disabled={loading}
            style={{ padding: '0.4rem 1.2rem', borderRadius: 8, background: '#c62828', color: '#fff', border: 'none', cursor: 'pointer' }}>
            {loading ? t('loading', lang) : t('get_guide', lang)}
          </button>
        </div>
      )}

      {/* Result display */}
      {result && (
        <div style={{ background: '#fff', border: '1px solid #c8e6d4', borderRadius: 8, padding: '0.8rem' }}>
          {result.title && <p style={{ fontWeight: 700, color: '#2e7d32', marginBottom: 8 }}>{result.title}</p>}

          {/* IYCF guidance list */}
          {result.guidance && (
            <ul style={{ margin: 0, paddingLeft: 18, fontSize: '0.85rem' }}>
              {result.guidance.map((g, i) => <li key={i} style={{ marginBottom: 4 }}>{g}</li>)}
            </ul>
          )}

          {/* Micronutrient fields */}
          {result.signs && (
            <div style={{ marginBottom: 8 }}>
              <p style={{ fontWeight: 600, fontSize: '0.8rem', color: '#c62828', margin: '0 0 4px' }}>{t('signs', lang)}</p>
              <ul style={{ margin: 0, paddingLeft: 16, fontSize: '0.8rem' }}>
                {result.signs.map((s, i) => <li key={i}>{s}</li>)}
              </ul>
            </div>
          )}
          {result.foods && (
            <div style={{ marginBottom: 8 }}>
              <p style={{ fontWeight: 600, fontSize: '0.8rem', color: '#2e7d32', margin: '0 0 4px' }}>{t('foods', lang)}</p>
              <ul style={{ margin: 0, paddingLeft: 16, fontSize: '0.8rem' }}>
                {result.foods.map((f, i) => <li key={i}>{f}</li>)}
              </ul>
            </div>
          )}
          {result.tips && (
            <div style={{ marginBottom: 8 }}>
              <p style={{ fontWeight: 600, fontSize: '0.8rem', color: '#1565c0', margin: '0 0 4px' }}>{t('tips', lang)}</p>
              <ul style={{ margin: 0, paddingLeft: 16, fontSize: '0.8rem' }}>
                {result.tips.map((tip, i) => <li key={i}>{tip}</li>)}
              </ul>
            </div>
          )}
          {result.action && (
            <div style={{ background: '#fff3e0', borderRadius: 6, padding: '0.5rem', fontSize: '0.82rem', color: '#e65100' }}>
              <strong>{t('action', lang)}</strong> {result.action}
            </div>
          )}

          {/* SAM/MAM home care */}
          {result.home_care && (
            <div style={{ marginTop: 8 }}>
              <p style={{ fontWeight: 600, fontSize: '0.8rem', margin: '0 0 4px' }}>{t('tips', lang)}</p>
              <ul style={{ margin: 0, paddingLeft: 16, fontSize: '0.8rem' }}>
                {result.home_care.map((c, i) => <li key={i}>{c}</li>)}
              </ul>
            </div>
          )}
          {result.criteria && (
            <div style={{ background: '#fce4ec', borderRadius: 6, padding: '0.5rem', fontSize: '0.78rem', color: '#880e4f', marginTop: 8 }}>
              {result.criteria}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
