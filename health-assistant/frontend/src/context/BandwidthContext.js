/**
 * BandwidthContext — Low Bandwidth Mode toggle + session data usage tracking.
 */
import React, { createContext, useContext, useState, useEffect, useRef } from 'react';

const BandwidthContext = createContext({
  lowBandwidth: false,
  setLowBandwidth: () => {},
  sessionDataUsage: 0,
  addDataUsage: () => {},
});

export function BandwidthProvider({ children }) {
  const [lowBandwidth, setLowBandwidthState] = useState(
    () => localStorage.getItem('ha_low_bandwidth') === 'true'
  );
  const [sessionDataUsage, setSessionDataUsage] = useState(0);
  const [showSuggestion, setShowSuggestion]     = useState(false);
  const usageRef = useRef(0);

  // Persist preference
  function setLowBandwidth(val) {
    setLowBandwidthState(val);
    localStorage.setItem('ha_low_bandwidth', String(val));
  }

  // Track data usage
  function addDataUsage(bytes) {
    usageRef.current += bytes;
    setSessionDataUsage(usageRef.current);
  }

  // Auto-suggest Low Bandwidth Mode when connection is slow
  useEffect(() => {
    const conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    if (!conn) return;

    function checkSpeed() {
      const downlink = conn.downlink; // Mbps
      if (downlink && downlink < 0.05 && !lowBandwidth) { // < 50 kbps
        setShowSuggestion(true);
      }
    }

    checkSpeed();
    conn.addEventListener('change', checkSpeed);
    return () => conn.removeEventListener('change', checkSpeed);
  }, [lowBandwidth]);

  return (
    <BandwidthContext.Provider value={{ lowBandwidth, setLowBandwidth, sessionDataUsage, addDataUsage }}>
      {showSuggestion && !lowBandwidth && (
        <div style={{
          position: 'fixed', bottom: 60, left: 0, right: 0, zIndex: 1000,
          background: '#fff3e0', borderTop: '2px solid #e65100',
          padding: '0.6rem 1rem', display: 'flex', justifyContent: 'space-between',
          alignItems: 'center', fontSize: '0.85rem',
        }}>
          <span> Slow connection detected. Enable Low Bandwidth Mode?</span>
          <div style={{ display: 'flex', gap: 8 }}>
            <button onClick={() => { setLowBandwidth(true); setShowSuggestion(false); }}
              style={{ padding: '0.3rem 0.8rem', borderRadius: 6, background: '#e65100',
                       color: '#fff', border: 'none', cursor: 'pointer' }}>
              Enable
            </button>
            <button onClick={() => setShowSuggestion(false)}
              style={{ padding: '0.3rem 0.8rem', borderRadius: 6, background: '#ccc',
                       border: 'none', cursor: 'pointer' }}>
              Dismiss
            </button>
          </div>
        </div>
      )}
      {children}
    </BandwidthContext.Provider>
  );
}

export function useBandwidth() {
  return useContext(BandwidthContext);
}

export default BandwidthContext;
