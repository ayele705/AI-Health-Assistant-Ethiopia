import React, { useState, useEffect } from 'react';
import { fetchConsultations } from '../api';

const T = {
  en: {
    title: 'HEW Community Dashboard',
    total: 'Total Consultations',
    emergency: 'Emergency Cases',
    hc: 'HC Referrals',
    selfcare: 'Self-Care Cases',
    recent: 'Recent Consultations',
    none: 'No consultations yet.',
    loading: 'Loading...',
    urgency: {
      emergency: 'Emergency',
      visit_health_center: 'Visit HC',
      self_care: 'Self-Care',
    },
  },
  am: {
    title: 'የጤና ሠራተኛ ዳሽቦርድ',
    total: 'ጠቅላላ ምክክሮች',
    emergency: 'አስቸኳይ ጉዳዮች',
    hc: 'ጤና ጣቢያ ጉዳዮች',
    selfcare: 'ቤት ውስጥ እንክብካቤ',
    recent: 'የቅርብ ጊዜ ምክክሮች',
    none: 'ምክክሮች የሉም።',
    loading: 'በመጫን ላይ...',
    urgency: {
      emergency: 'አስቸኳይ',
      visit_health_center: 'ጤና ጣቢያ',
      self_care: 'ቤት ውስጥ',
    },
  },
  ti: {
    title: 'ዳሽቦርድ ናይ ሰራሕተኛ ጥዕና',
    total: 'ጠቕላላ ምኽሪ',
    emergency: 'ህጹጽ ጉዳያት',
    hc: 'ናብ ጥዕና ጣቢያ',
    selfcare: 'ናይ ቤት ክንክን',
    recent: 'ቀረባ ምኽሪ',
    none: 'ምኽሪ የለን።',
    loading: 'ይጽዓን ኣሎ...',
    urgency: {
      emergency: 'ህጹጽ',
      visit_health_center: 'ጥዕና ጣቢያ',
      self_care: 'ናይ ቤት',
    },
  },
  om: {
    title: 'Daashboordii HEW',
    total: 'Mariiwwan Waliigalaa',
    emergency: 'Dhimmoota Ariifachiisaa',
    hc: 'Giddugala Fayyaa',
    selfcare: 'Kunuunsa Mana',
    recent: 'Mariiwwan Dhiyoo',
    none: 'Mariiwwan hin jiran.',
    loading: "Fe'amaa jira...",
    urgency: {
      emergency: 'Ariifachiisaa',
      visit_health_center: 'Giddugala Fayyaa',
      self_care: 'Mana',
    },
  },
  sid: {
    title: 'Daashboordii HEW',
    total: 'Mariiwwan Waliigalaa',
    emergency: 'Dhimmoota Ariifachiisaa',
    hc: 'Giddugala Fayyaa',
    selfcare: 'Kunuunsa Mana',
    recent: 'Mariiwwan Dhiyoo',
    none: 'Mariiwwan hin jiran.',
    loading: "Fe'amaa jira...",
    urgency: {
      emergency: 'Ariifachiisaa',
      visit_health_center: 'Giddugala Fayyaa',
      self_care: 'Mana',
    },
  },
  so: {
    title: 'Xoghaynta Bulshada HEW',
    total: 'Wadarta La-talinta',
    emergency: 'Kiisaska Degdegga',
    hc: 'Gudbinta Xarunta Caafimaadka',
    selfcare: 'Daryeelka Guriga',
    recent: 'La-talinta Dhowaan',
    none: 'Wali la-talin ma jirto.',
    loading: 'Waa la raraya...',
    urgency: {
      emergency: 'Degdeg',
      visit_health_center: 'Tag Xarunta',
      self_care: 'Guriga',
    },
  },
  aa: {
    title: 'Xoghaynta Bulshada HEW',
    total: 'Wadarta La-talinta',
    emergency: 'Kiisaska Degdegga',
    hc: 'Gudbinta Xarunta Caafimaadka',
    selfcare: 'Daryeelka Guriga',
    recent: 'La-talinta Dhowaan',
    none: 'Wali la-talin ma jirto.',
    loading: 'Waa la raraya...',
    urgency: {
      emergency: 'Degdeg',
      visit_health_center: 'Tag Xarunta',
      self_care: 'Guriga',
    },
  },
  wal: {
    title: 'Daashboordii HEW',
    total: 'Mariiwwan Waliigalaa',
    emergency: 'Dhimmoota Ariifachiisaa',
    hc: 'Giddugala Fayyaa',
    selfcare: 'Kunuunsa Mana',
    recent: 'Mariiwwan Dhiyoo',
    none: 'Mariiwwan hin jiran.',
    loading: "Fe'amaa jira...",
    urgency: {
      emergency: 'Ariifachiisaa',
      visit_health_center: 'Giddugala Fayyaa',
      self_care: 'Mana',
    },
  },
  had: {
    title: 'Daashboordii HEW',
    total: 'Mariiwwan Waliigalaa',
    emergency: 'Dhimmoota Ariifachiisaa',
    hc: 'Giddugala Fayyaa',
    selfcare: 'Kunuunsa Mana',
    recent: 'Mariiwwan Dhiyoo',
    none: 'Mariiwwan hin jiran.',
    loading: "Fe'amaa jira...",
    urgency: {
      emergency: 'Ariifachiisaa',
      visit_health_center: 'Giddugala Fayyaa',
      self_care: 'Mana',
    },
  },
};

export default function Dashboard({ lang }) {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const t = T[lang] || T['en'];

  useEffect(() => {
    fetchConsultations()
      .then(d => setData(d.consultations || []))
      .finally(() => setLoading(false));
  }, []);

  const counts = data.reduce((acc, c) => {
    acc[c.urgency_level] = (acc[c.urgency_level] || 0) + 1;
    return acc;
  }, {});

  const urgencyLabel = (u) => t.urgency[u] || u;

  return (
    <div>
      <p className="section-title">{t.title}</p>

      {loading && <p className="loading">{t.loading}</p>}

      {!loading && (
        <>
          <div className="stat-grid">
            <div className="stat-card">
              <div className="stat-number">{data.length}</div>
              <div className="stat-label">{t.total}</div>
            </div>
            <div className="stat-card" style={{ background: '#fde8e8' }}>
              <div className="stat-number" style={{ color: '#c0392b' }}>{counts['emergency'] || 0}</div>
              <div className="stat-label">{t.emergency}</div>
            </div>
            <div className="stat-card" style={{ background: '#fef3e2' }}>
              <div className="stat-number" style={{ color: '#e67e22' }}>{counts['visit_health_center'] || 0}</div>
              <div className="stat-label">{t.hc}</div>
            </div>
            <div className="stat-card">
              <div className="stat-number">{counts['self_care'] || 0}</div>
              <div className="stat-label">{t.selfcare}</div>
            </div>
          </div>

          <p className="section-title">{t.recent}</p>
          <div style={{ background: '#fff', border: '1px solid #c8e6d4', borderRadius: 12 }}>
            {data.length === 0 && (
              <p className="loading">{t.none}</p>
            )}
            {data.map((c, i) => (
              <div key={i} className="consult-row">
                <strong>{urgencyLabel(c.urgency_level)}</strong>
                {' — '}
                {c.symptoms?.join(', ') || '—'}
                <span style={{ float: 'right', color: '#aaa', fontSize: '0.75rem' }}>
                  {new Date(c.created_at).toLocaleDateString()}
                </span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
