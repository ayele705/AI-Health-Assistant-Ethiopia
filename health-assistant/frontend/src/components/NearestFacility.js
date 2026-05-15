import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap } from 'react-leaflet';
import L from 'leaflet';
import { fetchNearbyLive, fetchFacilities } from '../api';
import 'leaflet/dist/leaflet.css';

// Fix default marker icons (webpack issue with leaflet)
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl:       'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl:     'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Custom colored markers
const makeIcon = (color) => new L.DivIcon({
  className: '',
  html: `<div style="
    width:28px;height:28px;border-radius:50% 50% 50% 0;
    background:${color};border:3px solid #fff;
    box-shadow:0 2px 6px rgba(0,0,0,0.35);
    transform:rotate(-45deg);
  "></div>`,
  iconSize: [28, 28],
  iconAnchor: [14, 28],
  popupAnchor: [0, -30],
});

const TYPE_COLOR_MAP = {
  health_post:       '#43a047',
  health_center:     '#1e88e5',
  primary_hospital:  '#fb8c00',
  hospital:          '#e53935',
  referral_hospital: '#8e24aa',
};
const USER_ICON = new L.DivIcon({
  className: '',
  html: `<div style="
    width:18px;height:18px;border-radius:50%;
    background:#1a7a4a;border:3px solid #fff;
    box-shadow:0 0 0 4px rgba(26,122,74,0.25);
  "></div>`,
  iconSize: [18, 18],
  iconAnchor: [9, 9],
});

// Fly to new center when position changes
function MapFlyTo({ center }) {
  const map = useMap();
  useEffect(() => { if (center) map.flyTo(center, 13, { duration: 1.2 }); }, [center, map]);
  return null;
}

// ── i18n ──────────────────────────────────────────────────────────────────────
const L_TEXT = {
  title:    { en: 'Nearest Health Facilities', am: 'ቅርብ ጤና ጣቢያዎች', ti: 'ቀረባ ጥዕና ጣቢያ', om: 'Buufata Dhiyoo', sid: 'Buufata Dhiyoo' },
  gps_btn:  { en: ' Use My Location', am: ' አካባቢዬን ተጠቀም', ti: ' ቦታይ ተጠቀም', om: ' Bakka Koo Fayyadami', sid: ' Bakka Koo Fayyadami' },
  locating: { en: 'Getting location…', am: 'አካባቢ እየፈለጉ…', ti: 'ቦታ ይድለ…', om: 'Bakka argaa jira…', sid: 'Bakka argaa jira…' },
  filter:   { en: 'Type:', am: 'ዓይነት:', ti: 'ዓይነት:', om: 'Gosa:', sid: 'Gosa:' },
  all:      { en: 'All', am: 'ሁሉም', ti: 'ኩሎም', om: 'Hunda', sid: 'Hunda' },
  km_away:  { en: 'km', am: 'ኪሜ', ti: 'ኪሜ', om: 'km', sid: 'km' },
  call:     { en: 'Call', am: 'ደውሉ', ti: 'ደውል', om: 'Bilbili', sid: 'Bilbili' },
  found:    { en: 'facilities found', am: 'ጤና ጣቢያዎች ተገኝተዋል', ti: 'ጥዕና ጣቢያ ተረኺቡ', om: 'buufatni argame', sid: 'buufatni argame' },
  none:     { en: 'No facilities found. Try a larger radius.', am: 'ምንም አልተገኘም። ትልቅ ርቀት ይሞክሩ።', ti: 'ዝኾነ ኣይተረኽበን።', om: 'Hin argamne.', sid: 'Hin argamne.' },
  denied:   { en: 'Location access denied. Use region search below.', am: 'አካባቢ ፈቃድ ተከልክሏል። ከዚህ በታች ፈልጉ።', ti: 'ፍቓድ ቦታ ተኸልኪሉ።', om: 'Hayyamni dhorkaame.', sid: 'Hayyamni dhorkaame.' },
  region_fallback: { en: 'Search by region:', am: 'በክልል ፈልግ:', ti: 'ብክልል ፈልጥ:', om: 'Naannoon barbaadi:', sid: 'Naannoon barbaadi:' },
  directions: { en: 'Directions', am: 'አቅጣጫ', ti: 'ኣቅጣጫ', om: 'Karaa', sid: 'Karaa' },
  open_now:   { en: 'Open', am: 'ክፍት', ti: 'ክፉት', om: 'Banaa', sid: 'Banaa' },
  closed:     { en: 'Closed', am: 'ዝግ', ti: 'ዕጹው', om: 'Cufaa', sid: 'Cufaa' },
  hew:        { en: 'HEW', am: 'HEW', ti: 'HEW', om: 'HEW', sid: 'HEW' },
  legend:     { en: 'Legend', am: 'ምልክቶች', ti: 'ምልክታት', om: 'Mallattoo', sid: 'Mallattoo' },
};
const t = (k, lang) => (L_TEXT[k] || {})[lang] || (L_TEXT[k] || {}).en || k;

const TYPE_LABELS = {
  health_post:       { en: 'Health Post',       am: 'ጤና ኬላ'       },
  health_center:     { en: 'Health Center',     am: 'ጤና ጣቢያ'      },
  primary_hospital:  { en: 'Primary Hospital',  am: 'ዋና ሆስፒታል'    },
  hospital:          { en: 'Hospital',          am: 'ሆስፒታል'       },
  referral_hospital: { en: 'Referral Hospital', am: 'ሪፈራል ሆስፒታል' },
};

const REGIONS = ['Addis Ababa','Oromia','Amhara','Tigray','SNNPR','Somali','Afar','Dire Dawa','Harari','Gambella','Benishangul-Gumuz','Sidama','South West Ethiopia'];

// Default center: Ethiopia
const ETHIOPIA_CENTER = [9.145, 40.489];

export default function NearestFacility({ lang = 'en' }) {
  const [facilities, setFacilities] = useState([]);
  const [loading, setLoading]       = useState(false);
  const [error, setError]           = useState('');
  const [filterType, setFilterType] = useState('');
  const [userPos, setUserPos]       = useState(null);
  const [mapCenter, setMapCenter]   = useState(ETHIOPIA_CENTER);
  const [region, setRegion]         = useState('Amhara');
  const [showRegion, setShowRegion] = useState(false);
  const [selected, setSelected]     = useState(null);
  const [source, setSource]         = useState('');

  const sel = { padding: '6px 10px', borderRadius: 8, border: '1.5px solid #c8e6d4', fontSize: '0.88rem', background: '#fff' };

  async function doSearch(lat, lon) {
    setLoading(true); setError('');
    try {
      const data = await fetchNearbyLive(lat, lon, 50000, filterType);
      const facs = data.facilities || [];
      setFacilities(facs);
      setSource(data.source || 'knowledge_base');
      if (facs.length === 0) setError(t('none', lang));
    } catch {
      setError('Network error — make sure the backend is running.');
    } finally { setLoading(false); }
  }

  function handleGPS() {
    setError(''); setFacilities([]); setShowRegion(false); setSelected(null);
    if (!navigator.geolocation) { setError('Geolocation not supported.'); setShowRegion(true); return; }
    setLoading(true);
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        const { latitude: lat, longitude: lon } = pos.coords;
        setUserPos({ lat, lon });
        setMapCenter([lat, lon]);
        doSearch(lat, lon);
      },
      (err) => {
        setLoading(false);
        setError(err.code === 1 ? t('denied', lang) : `GPS error: ${err.message}`);
        setShowRegion(true);
      },
      { enableHighAccuracy: true, timeout: 15000, maximumAge: 60000 }
    );
  }

  async function handleRegionSearch() {
    setLoading(true); setError(''); setFacilities([]); setSelected(null);
    try {
      const data = await fetchFacilities(region);
      let facs = data.facilities || [];
      if (filterType) facs = facs.filter(f => f.facility_type === filterType);
      setFacilities(facs);
      setSource('knowledge_base');
      // Center map on first facility with coords
      const first = facs.find(f => f.latitude && f.longitude);
      if (first) setMapCenter([first.latitude, first.longitude]);
      if (facs.length === 0) setError(t('none', lang));
    } catch {
      setError('Network error.');
    } finally { setLoading(false); }
  }

  const displayed = filterType ? facilities.filter(f => f.facility_type === filterType) : facilities;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 130px)', gap: 0 }}>

      {/* ── Top controls ── */}
      <div style={{ padding: '10px 14px', background: '#fff', borderBottom: '1px solid #e0e0e0', display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center' }}>
        <h2 style={{ margin: 0, fontSize: '1rem', fontWeight: 700, color: '#1a7a4a', flex: 1 }}>
           {t('title', lang)}
        </h2>

        <select value={filterType} onChange={e => setFilterType(e.target.value)} style={sel}>
          <option value="">{t('all', lang)}</option>
          {Object.entries(TYPE_LABELS).map(([k, v]) => (
            <option key={k} value={k}>{v[lang] || v.en}</option>
          ))}
        </select>

        <button onClick={handleGPS} disabled={loading} style={{
          padding: '7px 16px', borderRadius: 20, background: '#1a7a4a', color: '#fff',
          border: 'none', fontWeight: 700, cursor: 'pointer', fontSize: '0.88rem',
          opacity: loading ? 0.7 : 1,
        }}>
          {loading ? t('locating', lang) : t('gps_btn', lang)}
        </button>
      </div>

      {/* ── Error / region fallback ── */}
      {error && (
        <div style={{ background: '#ffebee', color: '#c62828', padding: '8px 14px', fontSize: '0.88rem' }}>
          {error}
        </div>
      )}
      {showRegion && (
        <div style={{ background: '#e3f2fd', padding: '8px 14px', display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
          <span style={{ fontSize: '0.85rem', color: '#1565c0', fontWeight: 600 }}>{t('region_fallback', lang)}</span>
          <select value={region} onChange={e => setRegion(e.target.value)} style={{ ...sel, minWidth: 150 }}>
            {REGIONS.map(r => <option key={r} value={r}>{r}</option>)}
          </select>
          <button onClick={handleRegionSearch} disabled={loading} style={{
            padding: '6px 14px', borderRadius: 16, background: '#1565c0', color: '#fff',
            border: 'none', fontWeight: 700, cursor: 'pointer', fontSize: '0.85rem',
          }}>
            {loading ? '…' : ''}
          </button>
        </div>
      )}

      {/* ── Map + sidebar ── */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>

        {/* Map */}
        <div style={{ flex: 1, position: 'relative' }}>
          <MapContainer
            center={mapCenter}
            zoom={6}
            style={{ height: '100%', width: '100%' }}
            zoomControl={true}
          >
            <TileLayer
              attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            <MapFlyTo center={mapCenter} />

            {/* User location */}
            {userPos && (
              <>
                <Marker position={[userPos.lat, userPos.lon]} icon={USER_ICON}>
                  <Popup> Your location</Popup>
                </Marker>
                <Circle
                  center={[userPos.lat, userPos.lon]}
                  radius={50000}
                  pathOptions={{ color: '#1a7a4a', fillColor: '#1a7a4a', fillOpacity: 0.05, weight: 1.5, dashArray: '6' }}
                />
              </>
            )}

            {/* Facility markers */}
            {displayed.map((f, i) => {
              if (!f.latitude || !f.longitude) return null;
              const color = TYPE_COLOR_MAP[f.facility_type] || '#607d8b';
              const icon  = makeIcon(color);
              return (
                <Marker
                  key={f.id || i}
                  position={[f.latitude, f.longitude]}
                  icon={icon}
                  eventHandlers={{ click: () => setSelected(f) }}
                >
                  <Popup>
                    <div style={{ minWidth: 180 }}>
                      <div style={{ fontWeight: 700, color: '#1b5e20', marginBottom: 4 }}>{f.name}</div>
                      <div style={{ fontSize: '0.8rem', color: '#555' }}>
                        {TYPE_LABELS[f.facility_type]?.[lang] || f.facility_type}
                      </div>
                      {f.distance_km && (
                        <div style={{ fontSize: '0.8rem', color: '#2e7d32', fontWeight: 600, marginTop: 4 }}>
                           {f.distance_km} {t('km_away', lang)}
                        </div>
                      )}
                      {f.phone && (
                        <a href={`tel:${f.phone}`} style={{ display: 'block', marginTop: 6, color: '#1565c0', fontSize: '0.82rem', fontWeight: 600 }}>
                           {f.phone}
                        </a>
                      )}
                      {f.latitude && f.longitude && (
                        <a
                          href={`https://www.openstreetmap.org/directions?from=${userPos?.lat || ''},${userPos?.lon || ''}&to=${f.latitude},${f.longitude}`}
                          target="_blank" rel="noopener noreferrer"
                          style={{ display: 'block', marginTop: 4, color: '#1565c0', fontSize: '0.82rem' }}
                        >
                          ️ {t('directions', lang)}
                        </a>
                      )}
                    </div>
                  </Popup>
                </Marker>
              );
            })}
          </MapContainer>

          {/* Legend */}
          <div style={{
            position: 'absolute', bottom: 24, left: 10, zIndex: 1000,
            background: 'rgba(255,255,255,0.95)', borderRadius: 10, padding: '8px 12px',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)', fontSize: '0.75rem',
          }}>
            <div style={{ fontWeight: 700, marginBottom: 5, color: '#333' }}>{t('legend', lang)}</div>
            {Object.entries(TYPE_COLOR_MAP).map(([type, color]) => (
              <div key={type} style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 3 }}>
                <div style={{ width: 12, height: 12, borderRadius: '50%', background: color, flexShrink: 0 }} />
                <span style={{ color: '#444' }}>{TYPE_LABELS[type]?.[lang] || TYPE_LABELS[type]?.en}</span>
              </div>
            ))}
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginTop: 3 }}>
              <div style={{ width: 12, height: 12, borderRadius: '50%', background: '#1a7a4a', flexShrink: 0 }} />
              <span style={{ color: '#444' }}>You</span>
            </div>
          </div>

          {/* Result count badge */}
          {displayed.length > 0 && (
            <div style={{
              position: 'absolute', top: 10, left: '50%', transform: 'translateX(-50%)',
              zIndex: 1000, background: '#1a7a4a', color: '#fff',
              borderRadius: 20, padding: '4px 14px', fontSize: '0.82rem', fontWeight: 700,
              boxShadow: '0 2px 6px rgba(0,0,0,0.2)',
            }}>
              {displayed.length} {t('found', lang)}
              {source === 'google' && ' ·  Live'}
            </div>
          )}
        </div>

        {/* ── Sidebar list ── */}
        <div style={{
          width: 280, overflowY: 'auto', background: '#f7f8fa',
          borderLeft: '1px solid #e0e0e0', flexShrink: 0,
        }}>
          {displayed.length === 0 && !loading && (
            <div style={{ padding: 20, color: '#888', fontSize: '0.88rem', textAlign: 'center' }}>
              {error || 'Click "Use My Location" to find nearby facilities'}
            </div>
          )}
          {displayed.map((f, i) => {
            const color = TYPE_COLOR_MAP[f.facility_type] || '#607d8b';
            const isSelected = selected?.id === f.id;
            return (
              <div
                key={f.id || i}
                onClick={() => {
                  setSelected(f);
                  if (f.latitude && f.longitude) setMapCenter([f.latitude, f.longitude]);
                }}
                style={{
                  padding: '10px 12px',
                  borderBottom: '1px solid #e8e8e8',
                  cursor: 'pointer',
                  background: isSelected ? '#e8f5ee' : '#fff',
                  borderLeft: `4px solid ${isSelected ? '#1a7a4a' : color}`,
                  transition: 'background 0.15s',
                }}
              >
                <div style={{ fontWeight: 700, fontSize: '0.88rem', color: '#1b5e20' }}>{f.name}</div>
                <div style={{ fontSize: '0.75rem', color: '#666', marginTop: 2 }}>
                  {TYPE_LABELS[f.facility_type]?.[lang] || f.facility_type}
                  {f.distance_km && <span style={{ color: '#2e7d32', fontWeight: 600 }}> · {f.distance_km} {t('km_away', lang)}</span>}
                </div>
                <div style={{ display: 'flex', gap: 5, marginTop: 5, flexWrap: 'wrap' }}>
                  {f.open_now === true  && <span style={{ background: '#e8f5e9', color: '#2e7d32', borderRadius: 4, padding: '1px 6px', fontSize: '0.7rem', fontWeight: 600 }}>🟢 {t('open_now', lang)}</span>}
                  {f.open_now === false && <span style={{ background: '#ffebee', color: '#c62828', borderRadius: 4, padding: '1px 6px', fontSize: '0.7rem', fontWeight: 600 }}> {t('closed', lang)}</span>}
                  {f.hew_available     && <span style={{ background: '#e8f5e9', color: '#2e7d32', borderRadius: 4, padding: '1px 6px', fontSize: '0.7rem', fontWeight: 600 }}>{t('hew', lang)}</span>}
                  {f.rating            && <span style={{ background: '#fff8e1', color: '#f57f17', borderRadius: 4, padding: '1px 6px', fontSize: '0.7rem', fontWeight: 600 }}>⭐ {f.rating}</span>}
                </div>
                {f.phone && (
                  <a href={`tel:${f.phone}`} onClick={e => e.stopPropagation()}
                    style={{ display: 'inline-block', marginTop: 5, color: '#1565c0', fontSize: '0.78rem', fontWeight: 600, textDecoration: 'none' }}>
                     {t('call', lang)} {f.phone}
                  </a>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
