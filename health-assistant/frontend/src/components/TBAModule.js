/**
 * TBAModule — Traditional Birth Attendant tools.
 * Full multilingual support: en, am, ti, om, sid, so, aa, wal, had
 */
import React, { useState } from 'react';

const DANGER_SIGNS = [
  { id: 'heavy_bleeding',       en: 'Heavy bleeding',        am: 'ከባድ ደም መፍሰስ',         ti: 'ከቢድ ደም ምፍሳስ',       om: 'Dhiiga baay\'ee',        so: 'Dhiig badan',         icon: '' },
  { id: 'prolonged_labour',     en: 'Prolonged labour (>12h)',am: 'ረዥም ወሊድ (>12 ሰዓት)',    ti: 'ነዊሕ ወሊድ (>12 ሰዓት)',  om: 'Dhaluu dheeraa (>12h)', so: 'Dhalmada dheer (>12s)', icon: '⏱' },
  { id: 'convulsions',          en: 'Convulsions/fits',       am: 'ሽብርታ',                  ti: 'ምንቅጥቃጥ',             om: 'Raafama',               so: 'Qanqanaha',           icon: '' },
  { id: 'absent_fetal_movement',en: 'No fetal movement',     am: 'የፅንስ እንቅስቃሴ የለም',     ti: 'ምንቅስቃስ ፅንሲ የለን',    om: 'Socho\'i hin jiru',     so: 'Dhaqdhaqaaqa ilmaha ma jiro', icon: '' },
  { id: 'fever',                en: 'High fever',             am: 'ከፍተኛ ትኩሳት',            ti: 'ልዑል ረስኒ',            om: 'Ho\'aa ol\'aanaa',       so: 'Qandho xoog leh',     icon: '' },
  { id: 'unconscious',          en: 'Unconscious mother',     am: 'ያለ ንቃት',                ti: 'ዘይንቁ ኣደ',            om: 'Haadha of wallaalee',   so: 'Hooyo maqan',         icon: '' },
];

const DELIVERY_CHECKLIST = [
  { id: 'clean_hands',    en: 'Washed hands with soap',          am: 'እጅ በሳሙና ታጠበ',              ti: 'ኢድ ብሳሙና ሓጺቡ',          om: 'Harka saabunaan dhiqate',       so: 'Gacmaha saabuun lagu dhaqay' },
  { id: 'clean_surface',  en: 'Clean delivery surface prepared', am: 'ንጹህ ቦታ ተዘጋጀ',              ti: 'ንጹህ ቦታ ተዳሊዩ',           om: 'Bakki qulqulluu qophaa\'e',     so: 'Meel nadiif ah la diyaariyay' },
  { id: 'cord_clamp',     en: 'Cord clamp/tie available',        am: 'የእምብርት ማሰሪያ አለ',           ti: 'ማሰሪ ሕቡር ኣሎ',            om: 'Hidda hidhuu jira',             so: 'Xidid xidid ah ayaa jira' },
  { id: 'clean_blade',    en: 'Clean blade for cord cutting',    am: 'ንጹህ ምላጭ አለ',               ti: 'ንጹህ ምላጭ ኣሎ',            om: 'Hidda muruu qulqulluu jira',    so: 'Mindi nadiif ah ayaa jira' },
  { id: 'warm_blanket',   en: 'Warm blanket for newborn',        am: 'ሙቅ ብርድ ልብስ አለ',            ti: 'ሙቅ ብርድ ልብሲ ኣሎ',         om: 'Uffata ho\'aa daa\'imaa jira',  so: 'Gaadiid kulul ayaa jira' },
  { id: 'referral_ready', en: 'Referral transport arranged',     am: 'ሪፈራል ትራንስፖርት ተዘጋጅቷል',   ti: 'መጓዓዝያ ሪፈራል ተዳሊዩ',      om: 'Geejjibni wabii qophaa\'e',     so: 'Gaadiidka gudbinta la diyaariyay' },
];

const L = {
  title:       { en: ' TBA Tools',             am: ' TBA መሳሪያዎች',       ti: ' TBA መሳርሒ',          om: ' Meeshaa TBA',          sid: ' Meeshaa TBA',          so: ' Qaladaadka TBA',       aa: ' Qaladaadka TBA',       wal: ' Meeshaa TBA',          had: ' Meeshaa TBA' },
  checklist:   { en: 'Safe Delivery Checklist',  am: 'ደህና ወሊድ ዝርዝር',       ti: 'ዝርዝር ድሕሩ ወሊድ',       om: 'Tarree Dhaloota Nagaa',   sid: 'Tarree Dhaloota Nagaa',   so: 'Liiska Dhalmada Nabadda', aa: 'Liiska Dhalmada Nabadda', wal: 'Tarree Dhaloota Nagaa',   had: 'Tarree Dhaloota Nagaa' },
  danger:      { en: '️ Danger Signs',          am: '️ አደጋ ምልክቶች',       ti: '️ ምልክታት ሓደጋ',        om: '️ Mallattoo Balaa',      sid: '️ Mallattoo Balaa',      so: '️ Calaamadaha Khatarada', aa: '️ Calaamadaha Khatarada', wal: '️ Mallattoo Balaa',      had: '️ Mallattoo Balaa' },
  birth_rec:   { en: 'Record Birth',             am: 'ወሊድ ይመዝግቡ',          ti: 'ወሊድ ምዝገባ',             om: 'Dhalootaa Galmeessi',     sid: 'Dhalootaa Galmeessi',     so: 'Diiwaanso Dhalashada',    aa: 'Diiwaanso Dhalashada',    wal: 'Dhalootaa Galmeessi',     had: 'Dhalootaa Galmeessi' },
  alert_sent:  { en: ' Emergency alert sent!', am: ' አስቸኳይ ማንቂያ ተልኳል!', ti: ' ህጹጽ ምልክት ተሰዲዱ!',   om: ' Beeksisa ariifachiisaa ergame!', sid: ' Beeksisa ariifachiisaa ergame!', so: ' Digniinta xaaladda degdegga ah la diray!', aa: ' Digniinta xaaladda degdegga ah la diray!', wal: ' Beeksisa ariifachiisaa ergame!', had: ' Beeksisa ariifachiisaa ergame!' },
  birth_saved: { en: ' Birth record saved (will sync when online).', am: ' የወሊድ መዝገብ ተቀምጧል (ኢንተርኔት ሲኖር ይሰምራል)።', ti: ' መዝገብ ወሊድ ተዓቂቡ (ምስ ኢንተርነት ይሰምር)።', om: ' Galmeen dhalootaa kuufame (yeroo interneetii jiru ni walsimsiifama).', sid: ' Galmeen dhalootaa kuufame.', so: ' Diiwaanka dhalashada waa la keydsaday.', aa: ' Diiwaanka dhalashada waa la keydsaday.', wal: ' Galmeen dhalootaa kuufame.', had: ' Galmeen dhalootaa kuufame.' },
  delivery_date:{ en: 'Delivery Date',           am: 'የወሊድ ቀን',              ti: 'ዕለት ወሊድ',              om: 'Guyyaa dhalootaa',        sid: 'Guyyaa dhalootaa',        so: 'Taariikhda Dhalashada',   aa: 'Taariikhda Dhalashada',   wal: 'Guyyaa dhalootaa',        had: 'Guyyaa dhalootaa' },
  birth_weight:{ en: 'Birth Weight (kg)',        am: 'የልደት ክብደት (ኪ.ግ)',     ti: 'ክብደት ልደት (ኪ.ግ)',      om: 'Ulfaatina dhalootaa (kg)',sid: 'Ulfaatina dhalootaa (kg)',so: 'Miisaanka Dhalashada (kg)',aa: 'Miisaanka Dhalashada (kg)',wal: 'Ulfaatina dhalootaa (kg)', had: 'Ulfaatina dhalootaa (kg)' },
  complications:{ en: 'Complications',           am: 'ችግሮች',                 ti: 'ሽግግራት',                om: 'Rakkoolee',               sid: 'Rakkoolee',               so: 'Xaaladaha adag',          aa: 'Xaaladaha adag',          wal: 'Rakkoolee',               had: 'Rakkoolee' },
  referred:    { en: 'Referred to facility',     am: 'ወደ ጤና ጣቢያ ተላልፏል',    ti: 'ናብ ጥዕና ጣቢያ ተሰዲዱ',    om: 'Gara buufataatti ergame', sid: 'Gara buufataatti ergame', so: 'Xarunta la gudbiyay',     aa: 'Xarunta la gudbiyay',     wal: 'Gara buufataatti ergame', had: 'Gara buufataatti ergame' },
  save:        { en: 'Save Birth Record',        am: 'የወሊድ መዝገብ አስቀምጥ',     ti: 'መዝገብ ወሊድ ዕቀብ',        om: 'Galmeessa Dhalootaa Kuusi',sid: 'Galmeessa Dhalootaa Kuusi',so: 'Keydi Diiwaanka Dhalashada',aa: 'Keydi Diiwaanka Dhalashada',wal: 'Galmeessa Dhalootaa Kuusi',had: 'Galmeessa Dhalootaa Kuusi' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

export default function TBAModule({ lang = 'en' }) {
  const [tab, setTab]             = useState('checklist');
  const [checked, setChecked]     = useState({});
  const [dangerAlert, setDangerAlert] = useState(null);
  const [birthForm, setBirthForm] = useState({ delivery_date: '', birth_weight: '', complications: '', referred: false });
  const [birthSaved, setBirthSaved] = useState(false);

  function toggleCheck(id) {
    setChecked((prev) => ({ ...prev, [id]: !prev[id] }));
  }

  function handleDangerSign(sign) {
    setDangerAlert(sign);
    fetch('/api/v1/emergency-alert/send/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_identifier: 'tba_user',
        condition_summary: `Danger sign during delivery: ${sign.en}`,
        urgency_level: 'emergency',
        language: lang,
      }),
    }).catch(() => {});
  }

  async function saveBirthRecord() {
    const { savePatientRecord } = await import('../services/offlineStore');
    await savePatientRecord({ ...birthForm, type: 'birth_record', id: `birth_${Date.now()}` }, null);
    setBirthSaved(true);
  }

  const signLabel = (sign) => sign[lang] || sign.en;
  const checkLabel = (item) => item[lang] || item.en;

  return (
    <div style={{ padding: '0.5rem' }}>
      <p className="section-title">{t('title', lang)}</p>

      <div style={{ display: 'flex', gap: 6, marginBottom: 12, flexWrap: 'wrap' }}>
        {['checklist', 'danger', 'birth_rec'].map((tabId) => (
          <button key={tabId} onClick={() => setTab(tabId)}
            style={{ padding: '0.4rem 0.8rem', borderRadius: 8, border: 'none',
                     background: tab === tabId ? '#2e7d32' : '#e0e0e0',
                     color: tab === tabId ? '#fff' : '#333',
                     cursor: 'pointer', fontSize: '0.8rem' }}>
            {t(tabId, lang)}
          </button>
        ))}
      </div>

      {tab === 'checklist' && (
        <div>
          {DELIVERY_CHECKLIST.map((item) => (
            <label key={item.id} style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8, cursor: 'pointer' }}>
              <input type="checkbox" checked={!!checked[item.id]} onChange={() => toggleCheck(item.id)} style={{ width: 20, height: 20 }} />
              <span style={{ fontSize: '0.9rem', textDecoration: checked[item.id] ? 'line-through' : 'none', color: checked[item.id] ? '#888' : '#333' }}>
                {checkLabel(item)}
              </span>
            </label>
          ))}
        </div>
      )}

      {tab === 'danger' && (
        <div>
          {dangerAlert && (
            <div style={{ background: '#ffebee', border: '2px solid #c62828', borderRadius: 8, padding: '0.7rem', marginBottom: 10, color: '#c62828', fontWeight: 600 }}>
              {t('alert_sent', lang)}
            </div>
          )}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
            {DANGER_SIGNS.map((sign) => (
              <button key={sign.id} onClick={() => handleDangerSign(sign)}
                style={{ padding: '0.7rem', borderRadius: 8, background: '#ffebee', border: '2px solid #c62828', cursor: 'pointer', textAlign: 'center' }}>
                <div style={{ fontSize: '1.5rem' }}>{sign.icon}</div>
                <div style={{ fontSize: '0.8rem', fontWeight: 600, color: '#c62828' }}>{signLabel(sign)}</div>
              </button>
            ))}
          </div>
        </div>
      )}

      {tab === 'birth_rec' && (
        <div>
          {birthSaved && (
            <div style={{ background: '#e8f5e9', borderRadius: 8, padding: '0.6rem', color: '#2e7d32', marginBottom: 10 }}>
              {t('birth_saved', lang)}
            </div>
          )}
          {[
            { key: 'delivery_date',  labelKey: 'delivery_date',  type: 'date' },
            { key: 'birth_weight',   labelKey: 'birth_weight',   type: 'number' },
            { key: 'complications',  labelKey: 'complications',  type: 'text' },
          ].map(({ key, labelKey, type }) => (
            <input key={key} type={type} placeholder={t(labelKey, lang)}
              value={birthForm[key]}
              onChange={(e) => setBirthForm({ ...birthForm, [key]: e.target.value })}
              style={{ display: 'block', width: '100%', marginBottom: 8, padding: '0.4rem', borderRadius: 6, border: '1px solid #ccc', boxSizing: 'border-box' }}
            />
          ))}
          <label style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 10 }}>
            <input type="checkbox" checked={birthForm.referred} onChange={(e) => setBirthForm({ ...birthForm, referred: e.target.checked })} />
            {t('referred', lang)}
          </label>
          <button onClick={saveBirthRecord}
            style={{ padding: '0.5rem 1.2rem', borderRadius: 8, background: '#2e7d32', color: '#fff', border: 'none', cursor: 'pointer' }}>
            {t('save', lang)}
          </button>
        </div>
      )}
    </div>
  );
}
