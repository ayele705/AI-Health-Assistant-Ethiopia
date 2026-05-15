import React, { useState, useEffect } from 'react';

const L = {
  offline: { en: ' Offline — using cached data', am: ' ኦፍላይን — የተቀመጡ ውሂቦች', ti: ' ኦፍላይን — ዝተቐምጠ ሓበሬታ', om: ' Offline — deetaa kuufame', sid: ' Offline — deetaa kuufame', so: ' Offline — xogta kaydsan', aa: ' Offline — xogta kaydsan', wal: ' Offline — deetaa kuufame', had: ' Offline — deetaa kuufame' },
  online:  { en: ' Back online', am: ' ኦንላይን ሆነ', ti: ' ኦንላይን ኮነ', om: ' Online deebi\'e', sid: ' Online deebi\'e', so: ' Online dib u noqday', aa: ' Online dib u noqday', wal: ' Online deebi\'e', had: ' Online deebi\'e' },
};

export default function OfflineIndicator({ lang = 'en' }) {
  const [online, setOnline] = useState(navigator.onLine);
  const [showOnline, setShowOnline] = useState(false);

  useEffect(() => {
    const goOnline = () => { setOnline(true); setShowOnline(true); setTimeout(() => setShowOnline(false), 3000); };
    const goOffline = () => { setOnline(false); setShowOnline(false); };
    window.addEventListener('online', goOnline);
    window.addEventListener('offline', goOffline);
    return () => { window.removeEventListener('online', goOnline); window.removeEventListener('offline', goOffline); };
  }, []);

  if (online && !showOnline) return null;

  const msg = online
    ? ((L.online[lang] || L.online.en))
    : ((L.offline[lang] || L.offline.en));

  return (
    <div role="status" aria-live="polite" style={{
      position: 'fixed', bottom: 16, left: '50%', transform: 'translateX(-50%)',
      background: online ? '#2e7d32' : '#e65100',
      color: '#fff', padding: '0.5rem 1.2rem', borderRadius: 20,
      fontSize: '0.85rem', fontWeight: 600, zIndex: 9999,
      boxShadow: '0 2px 8px rgba(0,0,0,0.25)',
    }}>
      {msg}
    </div>
  );
}
