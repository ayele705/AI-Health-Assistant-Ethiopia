import React, { useState } from 'react';
import Chat from './components/Chat';
import Tips from './components/Tips';
import Facilities from './components/Facilities';
import Dashboard from './components/Dashboard';
import Appointment from './components/Appointment';
import AccessibilityToolbar from './components/AccessibilityToolbar';
import AccessibilityDashboard from './components/AccessibilityDashboard';
import ConsentScreen from './components/ConsentScreen';
import MedicationLookup from './components/MedicationLookup';
import NearestFacility from './components/NearestFacility';
import OfflineIndicator from './components/OfflineIndicator';
import GrowthMonitor from './components/GrowthMonitor';
import VaccinationTracker from './components/VaccinationTracker';
import PregnancyTracker from './components/PregnancyTracker';
import HEWChecklist from './components/HEWChecklist';
import SMSReminders from './components/SMSReminders';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import VoiceInterface from './components/VoiceInterface';
import ImageSymptom from './components/ImageSymptom';
import EmergencyAlert from './components/EmergencyAlert';
import CommunityCalendar from './components/CommunityCalendar';
import ReferralTracker from './components/ReferralTracker';
import TBAModule from './components/TBAModule';
import MentalHealthScreen from './components/MentalHealthScreen';
import ChronicDiseaseManager from './components/ChronicDiseaseManager';
import NutritionCounselor from './components/NutritionCounselor';
import SupplyTracker from './components/SupplyTracker';
import { AccessibilityProvider, useAccessibility } from './AccessibilityContext';
import { BandwidthProvider, useBandwidth } from './context/BandwidthContext';
import { TranslationProvider, useTranslation } from './i18n/TranslationContext';
import { startConnectivityListener } from './services/syncManager';
import './App.css';

// ── Navigation groups ─────────────────────────────────────────────────────────
const NAV_GROUPS_EN = [
  { group: { en: 'Core', am: 'ዋና', ti: 'ዋና', om: 'Ijoo' },
    items: [
      { id: 'chat',        icon: '', en: 'Check Symptoms',  am: 'ምልክቶችን ያረጋግጡ',  ti: 'ምልክታት ፈትሽ',    om: "Mallattoo Sakatta'i" },
      { id: 'tips',        icon: '', en: 'Health Tips',     am: 'የጤና ምክሮች',        ti: 'ምኽሪ ጥዕና',       om: 'Gorsa Fayyaa' },
      { id: 'meds',        icon: '', en: 'Medications',     am: 'መድሃኒቶች',          ti: 'መድሃኒታት',        om: 'Qorichaa' },
      { id: 'voice',       icon: '', en: 'Voice Input',     am: 'ድምፅ ግቤት',         ti: 'ድምፂ ምእታው',      om: 'Sagalee galchuu' },
      { id: 'image',       icon: '', en: 'Photo Check',     am: 'ፎቶ ምርመራ',         ti: 'ስእሊ ምርመራ',      om: "Suuraa Sakatta'i" },
    ],
  },
  { group: { en: 'Facilities', am: 'ጤና ጣቢያዎች', ti: 'ትካላት ጥዕና', om: 'Buufataalee' },
    items: [
      { id: 'nearest',     icon: '', en: 'Nearest Facility', am: 'ቅርብ ጤና ጣቢያ',    ti: 'ቀረባ ጥዕና ጣቢያ',  om: 'Buufata Dhiyoo' },
      { id: 'facilities',  icon: '', en: 'All Facilities',   am: 'ሁሉም ጤና ጣቢያዎች',  ti: 'ኩሎም ትካላት',      om: 'Buufataalee Hunda' },
      { id: 'appointment', icon: '', en: 'Appointment',      am: 'ቀጠሮ',             ti: 'ቆጸራ',            om: 'Beellama' },
    ],
  },
  { group: { en: 'Community Health', am: 'የማህበረሰብ ጤና', ti: 'ጥዕና ማሕበረሰብ', om: 'Fayyaa Hawaasaa' },
    items: [
      { id: 'growth',      icon: '', en: 'Growth Monitor',  am: 'ዕድገት ክትትል',      ti: 'ክትትል ዕቤት',      om: 'Hordoffii Guddina' },
      { id: 'vaccines',    icon: '', en: 'Vaccines',        am: 'ክትባቶች',           ti: 'ክታበታት',          om: 'Talaallii' },
      { id: 'pregnancy',   icon: '', en: 'Pregnancy',       am: 'እርግዝና',           ti: 'ጥንሲ',            om: 'Ulfaa' },
      { id: 'hew',         icon: '', en: 'HEW Tools',       am: 'HEW መሳሪያዎች',     ti: 'HEW መሳርሒ',       om: 'Meeshaa HEW' },
      { id: 'tba',         icon: '', en: 'TBA Tools',       am: 'TBA መሳሪያዎች',     ti: 'TBA መሳርሒ',       om: 'Meeshaa TBA' },
      { id: 'referrals',   icon: '', en: 'Referrals',       am: 'ሪፈራሎች',          ti: 'ሪፈራላት',          om: 'Wabii' },
      { id: 'calendar',    icon: '', en: 'Calendar',        am: 'ቀን መቁጠሪያ',       ti: 'ቀላንደር',          om: 'Kaaleendara' },
      { id: 'supply',      icon: '', en: 'Supply Tracker',  am: 'አቅርቦት ክትትል',     ti: 'ክትትል ቅርሲ',       om: 'Hordoffii Meeshaalee' },
    ],
  },
  { group: { en: 'Health Programs', am: 'የጤና ፕሮግራሞች', ti: 'ፕሮግራማት ጥዕና', om: 'Sagantaalee Fayyaa' },
    items: [
      { id: 'mental',      icon: '', en: 'Mental Health',   am: 'የአዕምሮ ጤና',        ti: 'ጥዕና ኣእምሮ',       om: 'Fayyaa Sammuu' },
      { id: 'chronic',     icon: '', en: 'Chronic Disease', am: 'ሥር የሰደደ ህመም',    ti: 'ሕማም ዘይፍወስ',      om: 'Dhukkuba Hin Fayyine' },
      { id: 'nutrition',   icon: '', en: 'Nutrition',       am: 'ምግብ ምክር',         ti: 'ምኽሪ ምግቢ',         om: 'Gorsa Nyaataa' },
    ],
  },
  { group: { en: 'Communication', am: 'ግንኙነት', ti: 'ርክክብ', om: 'Quunnamtii' },
    items: [
      { id: 'sms',         icon: '', en: 'SMS Reminders',   am: 'SMS ማስታወሻ',       ti: 'SMS ዘኪሮ',         om: 'SMS Yaadachiisa' },
      { id: 'emergency',   icon: '', en: 'Emergency',       am: 'አስቸኳይ',           ti: 'ህጹጽ',            om: 'Ariifachiisaa' },
    ],
  },
  { group: { en: 'Analytics & More', am: 'ትንታኔ እና ተጨማሪ', ti: 'ትንታኔ ወዘተ', om: 'Xiinxala fi Dabalata' },
    items: [
      { id: 'dashboard',   icon: '', en: 'Dashboard',       am: 'ዳሽቦርድ',           ti: 'ዳሽቦርድ',          om: 'Daashboordii' },
      { id: 'a11y',        icon: '', en: 'Accessibility',   am: 'ተደራሽነት',          ti: 'ተደራሽነት',         om: 'Argamummaa' },
    ],
  },
];

const ALL_ITEMS = NAV_GROUPS_EN.flatMap(g => g.items);

const APP_LABELS = {
  title:    { en: 'Health Assistant', am: 'የጤና ረዳት', ti: 'ሓጋዚ ጥዕና', om: 'Gargaaraa Fayyaa', sid: 'Gargaaraa Fayyaa' },
  subtitle: { en: 'For Rural Ethiopian Communities', am: 'ለኢትዮጵያ ገጠር ማህበረሰቦች', ti: 'ንገጠር ኢትዮጵያ ማሕበረሰብ', om: 'Hawaasa Baadiyyaa Itoophiyaaf', sid: 'Hawaasa Baadiyyaa Itoophiyaaf' },
};

function AppInner() {
  const [tab, setTab]               = useState('chat');
  const [lang, setLangState]        = useState('en');
  const [consentGiven, setConsentGiven] = useState(false);
  const [caregiverMode, setCaregiverMode] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // ── Backend health check — prevents vibration when server is offline ──────
  const [backendStatus, setBackendStatus] = useState('checking'); // 'checking' | 'online' | 'offline'

  const { prefs } = useAccessibility();
  const { lowBandwidth } = useBandwidth();
  const { t, setLang: setTranslationLang } = useTranslation();

  const setLang = (newLang) => {
    setLangState(newLang);
    setTranslationLang(newLang);
  };

  // Re-run health check when user clicks Retry (status goes back to 'checking')
  React.useEffect(() => {
    if (backendStatus !== 'checking') return;
    let cancelled = false;
    const timer = setTimeout(() => {
      fetch('/api/v1/tips/?language=en', { signal: AbortSignal.timeout ? AbortSignal.timeout(4000) : undefined })
        .then(r => { if (!cancelled) setBackendStatus(r.ok ? 'online' : 'offline'); })
        .catch(() => { if (!cancelled) setBackendStatus('offline'); });
    }, 500);
    return () => { cancelled = true; clearTimeout(timer); };
  }, [backendStatus]);

  React.useEffect(() => { startConnectivityListener(); }, []);

  const appTitle    = APP_LABELS.title[lang]    || APP_LABELS.title['en'];
  const appSubtitle = APP_LABELS.subtitle[lang] || APP_LABELS.subtitle['en'];
  const activeItem  = ALL_ITEMS.find(i => i.id === tab);

  // ── Show stable screens while backend is not ready ────────────────────────
  if (backendStatus === 'checking') {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center',
                    justifyContent: 'center', minHeight: '100vh', background: '#f0f7f4' }}>
        <span style={{ fontSize: '3rem' }}>🌿</span>
        <p style={{ marginTop: 16, fontSize: '1.1rem', color: '#1a7a4a', fontWeight: 600 }}>
          Health Assistant
        </p>
        <p style={{ color: '#888', fontSize: '0.9rem', marginTop: 8 }}>Starting up…</p>
        <div style={{ marginTop: 20, width: 40, height: 4, borderRadius: 2,
                      background: '#c8e6d4', overflow: 'hidden' }}>
          <div style={{ height: '100%', background: '#1a7a4a', borderRadius: 2,
                        animation: 'slide 1.2s ease-in-out infinite',
                        width: '60%' }} />
        </div>
        <style>{`@keyframes slide { 0%{transform:translateX(-100%)} 100%{transform:translateX(200%)} }`}</style>
      </div>
    );
  }

  if (backendStatus === 'offline') {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center',
                    justifyContent: 'center', minHeight: '100vh', background: '#f0f7f4',
                    padding: '2rem', textAlign: 'center' }}>
        <span style={{ fontSize: '3rem' }}>🌿</span>
        <p style={{ marginTop: 16, fontSize: '1.2rem', color: '#1a7a4a', fontWeight: 700 }}>
          Health Assistant
        </p>
        <div style={{ marginTop: 20, background: '#fff', borderRadius: 12, padding: '1.5rem',
                      maxWidth: 380, boxShadow: '0 2px 12px rgba(0,0,0,0.08)',
                      border: '1px solid #c8e6d4' }}>
          <p style={{ fontSize: '1.5rem', marginBottom: 8 }}>⚠️</p>
          <p style={{ fontWeight: 700, color: '#333', marginBottom: 8 }}>
            Server not running
          </p>
          <p style={{ fontSize: '0.88rem', color: '#555', lineHeight: 1.6, marginBottom: 16 }}>
            The backend server needs to be started. Open a new terminal and run:
          </p>
          <div style={{ background: '#1a2e1a', borderRadius: 8, padding: '0.8rem 1rem',
                        textAlign: 'left', marginBottom: 16 }}>
            <code style={{ color: '#7ec8a0', fontSize: '0.82rem', whiteSpace: 'pre-wrap', wordBreak: 'break-all' }}>
              {`cd health-assistant/backend\npython manage.py runserver`}
            </code>
          </div>
          <p style={{ fontSize: '0.8rem', color: '#888', marginBottom: 16 }}>
            Then come back here and click Retry.
          </p>
          <button
            onClick={() => { setBackendStatus('checking'); }}
            style={{ padding: '0.6rem 2rem', borderRadius: 8, background: '#1a7a4a',
                     color: '#fff', border: 'none', cursor: 'pointer',
                     fontWeight: 700, fontSize: '0.95rem' }}>
             Retry
          </button>
        </div>
      </div>
    );
  }

  function navigate(id) {
    setTab(id);
    setSidebarOpen(false); // close menu on mobile after selection
  }

  if (tab === 'chat' && !consentGiven) {
    return (
      <div className="app-shell">
        <header className="app-header">
          <div className="header-title">
            <span className="logo">🌿</span>
            <div><h1>{appTitle}</h1><p>{appSubtitle}</p></div>
          </div>
          <AccessibilityToolbar lang={lang} setLang={setLang} />
        </header>
        <div className="app-body">
          <main className="app-main">
            <ConsentScreen lang={lang}
              onAgree={() => setConsentGiven(true)}
              onCaregiver={() => { setCaregiverMode(true); setConsentGiven(true); }}
              onWithdraw={() => setTab('tips')} />
          </main>
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell">
      {/* Header */}
      <header className="app-header">
        <div className="header-left">
          <button className="hamburger-btn" onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Toggle menu" aria-expanded={sidebarOpen}>
            {sidebarOpen ? 'Close' : 'Menu'}
          </button>
          <div className="header-title">
            <span className="logo">🌿</span>
            <div><h1>{appTitle}</h1><p className="subtitle-hide">{appSubtitle}</p></div>
          </div>
        </div>
        <div className="header-right">
          <span className="current-tab-label">{activeItem?.icon} {activeItem ? (activeItem[lang] || activeItem.en) : ''}</span>
          <AccessibilityToolbar lang={lang} setLang={setLang} />
        </div>
      </header>

      <div className="app-body">
        {/* Sidebar overlay on mobile */}
        {sidebarOpen && (
          <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />
        )}

        {/* Sidebar */}
        <nav className={`sidebar ${sidebarOpen ? 'sidebar-open' : ''}`} aria-label="Main navigation">
          {NAV_GROUPS_EN.map((group, gi) => (
            <div key={gi} className="nav-group">
              <div className="nav-group-label">
                {group.group[lang] || group.group['en']}
              </div>
              {group.items.map(item => (
                <button key={item.id}
                  className={`nav-item ${tab === item.id ? 'active' : ''}`}
                  onClick={() => navigate(item.id)}
                  aria-current={tab === item.id ? 'page' : undefined}>
                  {item.icon && <span className="nav-icon">{item.icon}</span>}
                  <span className="nav-label">{item[lang] || item.en}</span>
                </button>
              ))}
            </div>
          ))}
        </nav>

        {/* Main content */}
        <main className="app-main" id="main-content">
          {tab === 'chat'        && <Chat lang={lang} caregiverMode={caregiverMode} />}
          {tab === 'tips'        && <Tips lang={lang} />}
          {tab === 'meds'        && <MedicationLookup lang={lang} />}
          {tab === 'nearest'     && <NearestFacility lang={lang} />}
          {tab === 'facilities'  && <Facilities lang={lang} />}
          {tab === 'appointment' && <Appointment lang={lang} />}
          {tab === 'growth'      && <GrowthMonitor lang={lang} />}
          {tab === 'vaccines'    && <VaccinationTracker lang={lang} />}
          {tab === 'pregnancy'   && <PregnancyTracker lang={lang} />}
          {tab === 'hew'         && <HEWChecklist lang={lang} />}
          {tab === 'sms'         && <SMSReminders lang={lang} />}
          {tab === 'dashboard'   && <AnalyticsDashboard lang={lang} />}
          {tab === 'a11y'        && <AccessibilityDashboard lang={lang} />}
          {tab === 'voice'       && <VoiceInterface lang={lang} />}
          {tab === 'image'       && <ImageSymptom lang={lang} />}
          {tab === 'emergency'   && <EmergencyAlert lang={lang} />}
          {tab === 'calendar'    && <CommunityCalendar lang={lang} />}
          {tab === 'referrals'   && <ReferralTracker lang={lang} />}
          {tab === 'tba'         && <TBAModule lang={lang} />}
          {tab === 'mental'      && <MentalHealthScreen lang={lang} />}
          {tab === 'chronic'     && <ChronicDiseaseManager lang={lang} />}
          {tab === 'nutrition'   && <NutritionCounselor lang={lang} />}
          {tab === 'supply'      && <SupplyTracker lang={lang} />}
        </main>
      </div>

      <OfflineIndicator lang={lang} />
    </div>
  );
}

export default function App() {
  return (
    <AccessibilityProvider>
      <BandwidthProvider>
        <TranslationProvider>
          <AppInner />
        </TranslationProvider>
      </BandwidthProvider>
    </AccessibilityProvider>
  );
}
