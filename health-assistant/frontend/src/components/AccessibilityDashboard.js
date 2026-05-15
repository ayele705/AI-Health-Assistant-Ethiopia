import React, { useState, useEffect } from 'react';

const BASE = '/api/v1';

const T = {
  en: {
    title: 'Accessibility Dashboard',
    total: 'Total Sessions',
    completed: 'Completed',
    rate: 'Completion Rate',
    modes: 'Accessibility Modes Used',
    feedback: 'Avg Feedback Score',
    flagged: 'Flagged Feedback',
    emergency: 'Emergency Escalations',
    partners: 'Active Partners',
    export: 'Export CSV',
    loading: 'Loading...',
    no_data: 'No data.',
  },
  am: {
    title: 'የተደራሽነት ዳሽቦርድ',
    total: 'ጠቅላላ ክፍለ ጊዜዎች',
    completed: 'የተጠናቀቁ',
    rate: 'የማጠናቀቅ መጠን',
    modes: 'ጥቅም ላይ የዋሉ ሁነታዎች',
    feedback: 'አማካይ የግብረ-መልስ ነጥብ',
    flagged: 'የተምልክቱ ግብረ-መልሶች',
    emergency: 'አስቸኳይ ጉዳዮች',
    partners: 'ንቁ አጋሮች',
    export: 'CSV ወደ ውጭ ላክ',
    loading: 'በመጫን ላይ...',
    no_data: 'ምንም ውሂብ የለም።',
  },
  ti: {
    title: 'ዳሽቦርድ ናይ ተደራሽነት',
    total: 'ጠቕላላ ክፍለ-ጊዜ',
    completed: 'ዝተወድኡ',
    rate: 'ናይ ምውዳእ ሬሾ',
    modes: 'ዝተጠቕሙ ሁነታታት',
    feedback: 'ማእከላይ ነጥቢ ርእይቶ',
    flagged: 'ዝተምልከቱ ርእይቶታት',
    emergency: 'ህጹጽ ጉዳያት',
    partners: 'ንቡር ሽርክቲ',
    export: 'CSV ኣውጽእ',
    loading: 'ይጽዓን ኣሎ...',
    no_data: 'ምንም ሓበሬታ የለን።',
  },
  om: {
    title: 'Daashboordii Argamummaa',
    total: 'Waliigala Seeshiniiwwan',
    completed: 'Xumuramanii',
    rate: 'Hanga Xumuruu',
    modes: 'Haalota Fayyadamame',
    feedback: 'Qabxii Deebii Gad-fageenyaa',
    flagged: 'Deebii Mallattaa\'ame',
    emergency: 'Dhimmoota Ariifachiisaa',
    partners: 'Hirmaattoota Hojii Irra',
    export: 'CSV Baasi',
    loading: "Fe'amaa jira...",
    no_data: 'Odeeffannoo hin jiru.',
  },
  sid: {
    title: 'Daashboordii Argamummaa',
    total: 'Waliigala Seeshiniiwwan',
    completed: 'Xumuramanii',
    rate: 'Hanga Xumuruu',
    modes: 'Haalota Fayyadamame',
    feedback: 'Qabxii Deebii',
    flagged: 'Deebii Mallattaa\'ame',
    emergency: 'Dhimmoota Ariifachiisaa',
    partners: 'Hirmaattoota',
    export: 'CSV Baasi',
    loading: "Fe'amaa jira...",
    no_data: 'Odeeffannoo hin jiru.',
  },
  so: {
    title: 'Xoghaynta Helitaanka',
    total: 'Wadarta Xilalka',
    completed: 'La Dhammeeyay',
    rate: 'Heerka Dhammaystirka',
    modes: 'Qaababka La Isticmaalay',
    feedback: 'Dhibcaha Jawaabta Celinta',
    flagged: 'Jawaabta Calaamadaysan',
    emergency: 'Kiisaska Degdegga',
    partners: 'Wadaagayaasha Firfircoon',
    export: 'Dhoofin CSV',
    loading: 'Waa la raraya...',
    no_data: 'Xog ma jirto.',
  },
  aa: {
    title: 'Xoghaynta Helitaanka',
    total: 'Wadarta Xilalka',
    completed: 'La Dhammeeyay',
    rate: 'Heerka Dhammaystirka',
    modes: 'Qaababka La Isticmaalay',
    feedback: 'Dhibcaha Jawaabta Celinta',
    flagged: 'Jawaabta Calaamadaysan',
    emergency: 'Kiisaska Degdegga',
    partners: 'Wadaagayaasha Firfircoon',
    export: 'Dhoofin CSV',
    loading: 'Waa la raraya...',
    no_data: 'Xog ma jirto.',
  },
  wal: {
    title: 'Daashboordii Argamummaa',
    total: 'Waliigala Seeshiniiwwan',
    completed: 'Xumuramanii',
    rate: 'Hanga Xumuruu',
    modes: 'Haalota Fayyadamame',
    feedback: 'Qabxii Deebii',
    flagged: 'Deebii Mallattaa\'ame',
    emergency: 'Dhimmoota Ariifachiisaa',
    partners: 'Hirmaattoota',
    export: 'CSV Baasi',
    loading: "Fe'amaa jira...",
    no_data: 'Odeeffannoo hin jiru.',
  },
  had: {
    title: 'Daashboordii Argamummaa',
    total: 'Waliigala Seeshiniiwwan',
    completed: 'Xumuramanii',
    rate: 'Hanga Xumuruu',
    modes: 'Haalota Fayyadamame',
    feedback: 'Qabxii Deebii',
    flagged: 'Deebii Mallattaa\'ame',
    emergency: 'Dhimmoota Ariifachiisaa',
    partners: 'Hirmaattoota',
    export: 'CSV Baasi',
    loading: "Fe'amaa jira...",
    no_data: 'Odeeffannoo hin jiru.',
  },
};

const MODE_LABELS = {
  simple_mode:    { en: 'Simple Mode',    am: 'ቀላል ሁነታ',    ti: 'ቀሊል ሁነታ',     om: 'Haala Salphaa',          sid: 'Haala Salphaa',          so: 'Qaabka Fudud',         aa: 'Qaabka Fudud',         wal: 'Haala Salphaa',          had: 'Haala Salphaa' },
  high_contrast:  { en: 'High Contrast',  am: 'ከፍተኛ ንፅፅር',  ti: 'ልዑል ንፅፅር',     om: "Garaagarummaa Ol'aanaa", sid: "Garaagarummaa Ol'aanaa", so: 'Kala-duwanaanshaha Sare', aa: 'Kala-duwanaanshaha Sare', wal: "Garaagarummaa Ol'aanaa", had: "Garaagarummaa Ol'aanaa" },
  large_text:     { en: 'Large Text',     am: 'ትልቅ ጽሑፍ',    ti: 'ዓቢ ጽሑፍ',       om: 'Barreeffama Guddaa',     sid: 'Barreeffama Guddaa',     so: 'Qoraalka Weyn',        aa: 'Qoraalka Weyn',        wal: 'Barreeffama Guddaa',     had: 'Barreeffama Guddaa' },
  screen_reader:  { en: 'Screen Reader',  am: 'ስክሪን አንባቢ',   ti: 'ኣንባቢ ስክሪን',    om: 'Dubbisaa Iskiriinii',    sid: 'Dubbisaa Iskiriinii',    so: 'Akhristaha Shaashadda', aa: 'Akhristaha Shaashadda', wal: 'Dubbisaa Iskiriinii',    had: 'Dubbisaa Iskiriinii' },
  voice_input:    { en: 'Voice Input',    am: 'የድምፅ ግቤት',    ti: 'ናይ ድምጺ ምእታው', om: 'Galchituu Sagalee',      sid: 'Galchituu Sagalee',      so: 'Gelinta Codka',        aa: 'Gelinta Codka',        wal: 'Galchituu Sagalee',      had: 'Galchituu Sagalee' },
  caregiver_mode: { en: 'Caregiver Mode', am: 'ተንከባካቢ ሁነታ',  ti: 'ሁነታ ተኸናኻኒ',   om: 'Haala Kunuunsituu',      sid: 'Haala Kunuunsituu',      so: 'Qaabka Daryeelaha',    aa: 'Qaabka Daryeelaha',    wal: 'Haala Kunuunsituu',      had: 'Haala Kunuunsituu' },
  ivr:            { en: 'IVR Channel',    am: 'IVR ቻናል',      ti: 'IVR ቻናል',       om: 'Chaanaalii IVR',         sid: 'Chaanaalii IVR',         so: 'Kanaalka IVR',         aa: 'Kanaalka IVR',         wal: 'Chaanaalii IVR',         had: 'Chaanaalii IVR' },
  sms:            { en: 'SMS Channel',    am: 'SMS ቻናል',      ti: 'SMS ቻናል',       om: 'Chaanaalii SMS',         sid: 'Chaanaalii SMS',         so: 'Kanaalka SMS',         aa: 'Kanaalka SMS',         wal: 'Chaanaalii SMS',         had: 'Chaanaalii SMS' },
  ussd:           { en: 'USSD Channel',   am: 'USSD ቻናል',     ti: 'USSD ቻናል',      om: 'Chaanaalii USSD',        sid: 'Chaanaalii USSD',        so: 'Kanaalka USSD',        aa: 'Kanaalka USSD',        wal: 'Chaanaalii USSD',        had: 'Chaanaalii USSD' },
};

function getModeLabel(mode, lang) {
  return (MODE_LABELS[mode] || {})[lang]
    || (MODE_LABELS[mode] || {})['en']
    || mode;
}

export default function AccessibilityDashboard({ lang }) {
  const [kpis, setKpis] = useState(null);
  const [loading, setLoading] = useState(true);
  const t = T[lang] || T['en'];

  useEffect(() => {
    fetch(`${BASE}/accessibility/kpis/`)
      .then(r => r.json())
      .then(setKpis)
      .catch(() => setKpis(null))
      .finally(() => setLoading(false));
  }, []);

  const handleExport = () => {
    window.open(`${BASE}/accessibility/kpis/export/`, '_blank');
  };

  if (loading) return <p className="loading">{t.loading}</p>;
  if (!kpis) return <p className="loading">{t.no_data}</p>;

  return (
    <div>
      <p className="section-title">{t.title}</p>

      <div className="stat-grid">
        <div className="stat-card">
          <div className="stat-number">{kpis.total_sessions}</div>
          <div className="stat-label">{t.total}</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{kpis.completed_sessions}</div>
          <div className="stat-label">{t.completed}</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{kpis.completion_rate}%</div>
          <div className="stat-label">{t.rate}</div>
        </div>
        <div className="stat-card" style={{ background: '#fde8e8' }}>
          <div className="stat-number" style={{ color: '#c0392b' }}>{kpis.emergency_escalations}</div>
          <div className="stat-label">{t.emergency}</div>
        </div>
        <div className="stat-card" style={{ background: '#fef3e2' }}>
          <div className="stat-number" style={{ color: '#e67e22' }}>{kpis.average_feedback_score}</div>
          <div className="stat-label">{t.feedback}</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{kpis.active_partners}</div>
          <div className="stat-label">{t.partners}</div>
        </div>
      </div>

      <p className="section-title">{t.modes}</p>
      <div style={{ background: '#fff', border: '1px solid #c8e6d4', borderRadius: 12, padding: 12 }}>
        {Object.entries(kpis.mode_counts || {}).map(([mode, count]) => (
          <div key={mode} className="consult-row" style={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>{getModeLabel(mode, lang)}</span>
            <strong>{count}</strong>
          </div>
        ))}
      </div>

      <button className="start-btn" onClick={handleExport} style={{ marginTop: 16 }} aria-label={t.export}>
         {t.export}
      </button>
    </div>
  );
}
