import React, { useState, useEffect } from 'react';
import { fetchAnalytics, fetchOutbreakAlerts, fetchDHIS2Export } from '../api';

const L = {
  title:        { en: ' Analytics Dashboard', am: ' ትንታኔ ዳሽቦርድ', ti: ' ትንታኔ ዳሽቦርድ', om: ' Daashboordii Xiinxalaa', sid: ' Daashboordii Xiinxalaa' },
  period:       { en: 'Period (days)', am: 'ጊዜ (ቀናት)', ti: 'ጊዜ (መዓልቲ)', om: 'Yeroo (guyyaa)', sid: 'Yeroo (guyyaa)' },
  refresh:      { en: 'Refresh', am: 'አድስ', ti: 'ሓድስ', om: 'Haaromsi', sid: 'Haaromsi' },
  consultations:{ en: 'Consultations', am: 'ምክክሮች', ti: 'ምኽሪ', om: 'Mariiwwan', sid: 'Mariiwwan' },
  emergency:    { en: 'Emergency', am: 'አስቸኳይ', ti: 'ህጹጽ', om: 'Hatattama', sid: 'Hatattama' },
  health_center:{ en: 'Visit Clinic', am: 'ጤና ጣቢያ', ti: 'ጥዕና ጣቢያ', om: 'Buufata', sid: 'Buufata' },
  self_care:    { en: 'Self Care', am: 'ራስ ህክምና', ti: 'ናይ ርእሰ ክንክን', om: 'Of-kunuunsa', sid: 'Of-kunuunsa' },
  sam:          { en: 'SAM Cases', am: 'SAM ጉዳዮች', ti: 'SAM ጉዳያት', om: 'Dhimmoota SAM', sid: 'Dhimmoota SAM' },
  mam:          { en: 'MAM Cases', am: 'MAM ጉዳዮች', ti: 'MAM ጉዳያት', om: 'Dhimmoota MAM', sid: 'Dhimmoota MAM' },
  coverage:     { en: 'Vaccine Coverage', am: 'የክትባት ሽፋን', ti: 'ሽፋን ክታበት', om: 'Haguuggii Talaallii', sid: 'Haguuggii Talaallii' },
  anc4:         { en: 'ANC 4+ Rate', am: 'ANC 4+ ምጣኔ', ti: 'ANC 4+ ሬሾ', om: 'Hamma ANC 4+', sid: 'Hamma ANC 4+' },
  top_symptoms: { en: 'Top Symptoms', am: 'ዋና ምልክቶች', ti: 'ዋና ምልክታት', om: "Mallattoo Ol'aanaa", sid: "Mallattoo Ol'aanaa" },
  outbreak:     { en: ' Outbreak Alerts', am: ' ወረርሽኝ ማስጠንቀቂያ', ti: ' ናይ ወረርሽኝ ምልክታት', om: ' Akeekkachiisa Dhukkuba', sid: ' Akeekkachiisa Dhukkuba' },
  no_alerts:    { en: ' No outbreak alerts', am: ' ምንም ማስጠንቀቂያ የለም', ti: ' ዝኾነ ምልክት የለን', om: ' Akeekkachiisa Hin Jiru', sid: ' Akeekkachiisa Hin Jiru' },
  dhis2:        { en: ' DHIS2 Export', am: ' DHIS2 ወደ ውጭ ላክ', ti: ' DHIS2 ምስዳድ', om: ' DHIS2 Erguu', sid: ' DHIS2 Erguu' },
  export:       { en: 'Export JSON', am: 'JSON ላክ', ti: 'JSON ስደድ', om: 'JSON Ergi', sid: 'JSON Ergi' },
  push:         { en: 'Push to DHIS2', am: 'ወደ DHIS2 ላክ', ti: 'ናብ DHIS2 ስደድ', om: 'DHIS2 Ergi', sid: 'DHIS2 Ergi' },
  loading:      { en: 'Loading…', am: 'እየጫነ…', ti: 'ይጸዓን…', om: "Fe'aa jira…", sid: "Fe'aa jira…" },
  active_preg:  { en: 'Active Pregnancies', am: 'ንቁ እርግዝናዎች', ti: 'ንቡር ጥንስታት', om: 'Ulfaa Hojjataa', sid: 'Ulfaa Hojjataa' },
  sms_sent:     { en: 'SMS Sent', am: 'SMS ተልኳል', ti: 'SMS ተሰዲዱ', om: 'SMS Ergame', sid: 'SMS Ergame' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

const ALERT_COLOR = { critical: '#c62828', high: '#e65100', medium: '#f57f17' };
const ALERT_BG    = { critical: '#ffebee', high: '#fff3e0', medium: '#fff8e1' };

export default function AnalyticsDashboard({ lang = 'en' }) {
  const [data, setData]       = useState(null);
  const [alerts, setAlerts]   = useState(null);
  const [days, setDays]       = useState(30);
  const [loading, setLoading] = useState(false);
  const [tab, setTab]         = useState('overview');
  const [dhis2Result, setDhis2Result] = useState(null);

  useEffect(() => { load(); }, [days]);

  async function load() {
    setLoading(true);
    try {
      const [dash, outbreak] = await Promise.all([
        fetchAnalytics(days),
        fetchOutbreakAlerts(),
      ]);
      setData(dash);
      setAlerts(outbreak);
    } finally {
      setLoading(false);
    }
  }

  async function handleDHIS2Export() {
    const payload = await fetchDHIS2Export();
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' });
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement('a');
    a.href = url;
    a.download = `dhis2_export_${new Date().toISOString().split('T')[0]}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  const tabs = ['overview', 'symptoms', 'outbreak', 'dhis2'];

  return (
    <div style={{ padding: '1rem', maxWidth: 800, margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
        <h2 style={{ margin: 0 }}>{t('title', lang)}</h2>
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <select value={days} onChange={e => setDays(Number(e.target.value))}
            style={{ padding: '0.4rem 0.6rem', borderRadius: 6, border: '1px solid #ccc' }}>
            {[7, 14, 30, 60, 90].map(d => <option key={d} value={d}>{d}d</option>)}
          </select>
          <button onClick={load} disabled={loading}
            style={{ padding: '0.4rem 0.9rem', borderRadius: 6, background: '#1565c0', color: '#fff', border: 'none', cursor: 'pointer', fontWeight: 600 }}>
            {loading ? '…' : t('refresh', lang)}
          </button>
        </div>
      </div>

      {/* Outbreak banner */}
      {alerts?.critical_count > 0 && (
        <div style={{ background: '#ffebee', border: '2px solid #c62828', borderRadius: 10, padding: '0.75rem 1rem', marginBottom: '1rem', color: '#c62828', fontWeight: 700 }}>
           {alerts.critical_count} CRITICAL outbreak alert{alerts.critical_count > 1 ? 's' : ''} — check Outbreak tab
        </div>
      )}

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '0.4rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
        {tabs.map(tb => (
          <button key={tb} onClick={() => setTab(tb)}
            style={{ padding: '0.4rem 0.9rem', borderRadius: 8, border: '2px solid #1565c0', background: tab === tb ? '#1565c0' : '#fff', color: tab === tb ? '#fff' : '#1565c0', fontWeight: 600, cursor: 'pointer', textTransform: 'capitalize' }}>
            {tb === 'dhis2' ? 'DHIS2' : tb.charAt(0).toUpperCase() + tb.slice(1)}
          </button>
        ))}
      </div>

      {loading && !data && <div style={{ color: '#666', textAlign: 'center', padding: '2rem' }}>{t('loading', lang)}</div>}

      {/* Overview tab */}
      {tab === 'overview' && data && (
        <div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(150px, 1fr))', gap: '0.75rem', marginBottom: '1.5rem' }}>
            <KPI label={t('consultations', lang)} value={data.consultations?.total} color="#1565c0" />
            <KPI label={t('emergency', lang)}     value={data.consultations?.emergency_count} color="#c62828" />
            <KPI label={t('health_center', lang)} value={data.consultations?.health_center_count} color="#e65100" />
            <KPI label={t('self_care', lang)}     value={data.consultations?.self_care_count} color="#2e7d32" />
            <KPI label={t('sam', lang)}           value={data.growth?.sam_count} color="#c62828" sub={`${data.growth?.sam_percent}%`} />
            <KPI label={t('mam', lang)}           value={data.growth?.mam_count} color="#f57f17" sub={`${data.growth?.mam_percent}%`} />
            <KPI label={t('coverage', lang)}      value={`${data.vaccinations?.coverage_percent}%`} color="#1565c0" sub={`${data.vaccinations?.fully_vaccinated}/${data.vaccinations?.total_children}`} />
            <KPI label={t('anc4', lang)}          value={`${data.pregnancies?.anc4_plus_percent}%`} color="#6a1b9a" sub={`${data.pregnancies?.anc4_plus_count} women`} />
            <KPI label={t('active_preg', lang)}   value={data.pregnancies?.active_pregnancies} color="#6a1b9a" />
            <KPI label={t('sms_sent', lang)}      value={data.sms?.total_sent} color="#00695c" />
          </div>

          {/* Daily trend bar chart (simple CSS) */}
          {data.consultations?.daily_trend?.length > 0 && (
            <div style={{ background: '#f5f5f5', borderRadius: 10, padding: '1rem', marginBottom: '1rem' }}>
              <div style={{ fontWeight: 700, marginBottom: '0.75rem', color: '#333' }}>Daily Consultations (last {days} days)</div>
              <MiniBarChart data={data.consultations.daily_trend} />
            </div>
          )}

          {/* Language breakdown */}
          {data.consultations?.by_language && (
            <div style={{ background: '#f5f5f5', borderRadius: 10, padding: '1rem' }}>
              <div style={{ fontWeight: 700, marginBottom: '0.5rem' }}>By Language</div>
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
                {Object.entries(data.consultations.by_language).map(([lang_, count]) => (
                  <span key={lang_} style={{ background: '#e3f2fd', color: '#1565c0', borderRadius: 6, padding: '3px 10px', fontSize: '0.85rem', fontWeight: 600 }}>
                    {lang_.toUpperCase()}: {count}
                  </span>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Top symptoms tab */}
      {tab === 'symptoms' && data && (
        <div>
          <div style={{ fontWeight: 700, marginBottom: '0.75rem' }}>{t('top_symptoms', lang)}</div>
          {data.consultations?.top_symptoms?.map((s, i) => {
            const max = data.consultations.top_symptoms[0]?.count || 1;
            const pct = Math.round(s.count / max * 100);
            return (
              <div key={s.symptom} style={{ marginBottom: '0.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 2 }}>
                  <span style={{ fontWeight: i < 3 ? 700 : 400 }}>{s.symptom}</span>
                  <span style={{ color: '#666', fontSize: '0.85rem' }}>{s.count}</span>
                </div>
                <div style={{ background: '#e0e0e0', borderRadius: 4, height: 8 }}>
                  <div style={{ background: i === 0 ? '#c62828' : i < 3 ? '#e65100' : '#1565c0', width: `${pct}%`, height: '100%', borderRadius: 4, transition: 'width 0.3s' }} />
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Outbreak tab */}
      {tab === 'outbreak' && alerts && (
        <div>
          {alerts.total_alerts === 0
            ? <div style={{ background: '#e8f5e9', borderRadius: 10, padding: '1.5rem', textAlign: 'center', color: '#2e7d32', fontWeight: 700 }}>{t('no_alerts', lang)}</div>
            : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {alerts.alerts?.map((a, i) => (
                  <div key={i} style={{ background: ALERT_BG[a.alert_level] || '#fff', borderRadius: 10, padding: '1rem', borderLeft: `5px solid ${ALERT_COLOR[a.alert_level] || '#333'}` }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <div style={{ fontWeight: 800, color: ALERT_COLOR[a.alert_level], textTransform: 'uppercase', fontSize: '0.8rem' }}>{a.alert_level} · {a.type?.replace('_', ' ')}</div>
                      <div style={{ fontSize: '0.78rem', color: '#888' }}>{a.date}</div>
                    </div>
                    <div style={{ fontWeight: 700, marginTop: 4 }}>{a.message_en}</div>
                    {a.message_am && lang === 'am' && <div style={{ color: '#555', marginTop: 4 }}>{a.message_am}</div>}
                    <div style={{ marginTop: 6, fontSize: '0.82rem', color: '#555', background: 'rgba(0,0,0,0.04)', borderRadius: 6, padding: '4px 8px' }}>
                       {a.action_en}
                    </div>
                    <div style={{ marginTop: 4, fontSize: '0.78rem', color: '#888' }}>Region: {a.region} · Cases: {a.count} (threshold: {a.threshold})</div>
                  </div>
                ))}
              </div>
            )
          }
        </div>
      )}

      {/* DHIS2 tab */}
      {tab === 'dhis2' && (
        <div>
          <div style={{ background: '#e3f2fd', borderRadius: 10, padding: '1rem', marginBottom: '1rem' }}>
            <div style={{ fontWeight: 700, marginBottom: '0.5rem' }}>DHIS2 — Ethiopia National HMIS</div>
            <div style={{ fontSize: '0.85rem', color: '#555', lineHeight: 1.6 }}>
              Export aggregated health data in DHIS2 dataValueSet format for upload to the national health information system.
              Set DHIS2_URL, DHIS2_USERNAME, DHIS2_PASSWORD in .env to enable direct push.
            </div>
          </div>
          <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
            <button onClick={handleDHIS2Export}
              style={{ padding: '0.6rem 1.2rem', borderRadius: 8, background: '#1565c0', color: '#fff', border: 'none', fontWeight: 600, cursor: 'pointer' }}>
              {t('export', lang)}
            </button>
            <button onClick={async () => { const r = await fetch('/api/v1/dhis2/push/', {method:'POST', headers:{'Content-Type':'application/json'}, body:'{}'}); setDhis2Result(await r.json()); }}
              style={{ padding: '0.6rem 1.2rem', borderRadius: 8, background: '#2e7d32', color: '#fff', border: 'none', fontWeight: 600, cursor: 'pointer' }}>
              {t('push', lang)}
            </button>
          </div>
          {dhis2Result && (
            <div style={{ marginTop: '1rem', background: '#f5f5f5', borderRadius: 8, padding: '0.75rem', fontFamily: 'monospace', fontSize: '0.82rem', whiteSpace: 'pre-wrap' }}>
              {JSON.stringify(dhis2Result, null, 2)}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

function KPI({ label, value, color, sub }) {
  return (
    <div style={{ background: '#fff', borderRadius: 10, padding: '0.75rem', textAlign: 'center', boxShadow: '0 1px 4px rgba(0,0,0,0.08)', border: `2px solid ${color}20` }}>
      <div style={{ fontSize: '1.6rem', fontWeight: 800, color }}>{value ?? '—'}</div>
      {sub && <div style={{ fontSize: '0.75rem', color: '#888' }}>{sub}</div>}
      <div style={{ fontSize: '0.75rem', color: '#666', marginTop: 2 }}>{label}</div>
    </div>
  );
}

function MiniBarChart({ data }) {
  const max = Math.max(...data.map(d => d.count), 1);
  return (
    <div style={{ display: 'flex', alignItems: 'flex-end', gap: 2, height: 60, overflowX: 'auto' }}>
      {data.map((d, i) => (
        <div key={i} title={`${d.date}: ${d.count}`}
          style={{ flex: '0 0 auto', width: Math.max(8, 300 / data.length), background: '#1565c0', borderRadius: '2px 2px 0 0', height: `${Math.round(d.count / max * 100)}%`, minHeight: 2, opacity: 0.8 }} />
      ))}
    </div>
  );
}
