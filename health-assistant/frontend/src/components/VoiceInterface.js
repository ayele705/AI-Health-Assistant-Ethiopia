/**
 * VoiceInterface — Microphone button + transcript display + TTS readback.
 *
 * Uses useVoice which automatically falls back to server-side STT
 * (MediaRecorder → POST /api/v1/stt/) when the Web Speech API is unavailable
 * (Firefox, Safari, older Android WebView).
 */
import React, { useEffect } from 'react';
import useVoice from '../hooks/useVoice';

const L = {
  tap_to_speak:   { en: ' Tap to Speak',    am: ' ለመናገር ይጫኑ',       om: ' Dubbachuuf tuqi',                ti: ' ንምዝራብ ጠውቕ' },
  listening:      { en: ' Listening…',       am: ' እያዳመጠ ነው…',        om: ' Dhaggeeffachaa…',               ti: ' ይሰምዕ ኣሎ…' },
  processing:     { en: '⏳ Processing…',       am: '⏳ እየሰራ ነው…',          om: '⏳ Hojjechaa…',                    ti: '⏳ ይሰርሕ ኣሎ…' },
  not_supported:  { en: 'Voice input is not available. Your browser does not support audio recording.', am: 'ድምፅ ግቤት አይቻልም። ብሮውዘርዎ ድምፅ ቀረጻን አይደግፍም።', om: 'Sagalee galchuu hin danda\'amu. Browser keessan sagalee galmeessuu hin deeggaru.', ti: 'ድምፂ ምእታው ኣይካኣልን። ብሮውዘርካ ናይ ድምፂ ቀረጻ ኣይድግፍን።' },
  permission:     { en: 'Microphone access denied. Please allow microphone permission in your browser settings.', am: 'ማይክሮፎን ፈቃድ ተከልክሏል። በ browser ቅንብሮች ፈቃድ ይፍቀዱ።', om: 'Hayyama maaykiroofooni dhorkaame. Qindaa\'ina browser keessatti hayyama kenni.', ti: 'ፍቓድ ማይክሮፎን ተኸልኪሉ። ኣብ ቅንብር browser ፍቓድ ሃብ።' },
  empty:          { en: 'Could not hear you. Please try again.',                                                  am: 'አልሰማዎትም። እንደገና ይሞክሩ።',                                                                                om: "Sihin dhaggeenye. Irra deebi'i yaali.",                                         ti: 'ኣይሰማዕናካን። ደጊምካ ፈትን።' },
  stt_unavail:    { en: 'Speech recognition service unavailable. Check your internet connection.',                am: 'የድምፅ ማወቂያ አገልግሎት አይገኝም። የኢንተርኔት ግንኙነትዎን ያረጋግጡ።',                                                  om: 'Tajaajilli beekamtii sagalee hin argamu. Walqunnamtii interneetii kee mirkaneessi.', ti: 'ኣገልግሎት ፍልጠት ድምፂ ኣይርከብን። ናይ ኢንተርነት ምትእስሳርካ ኣረጋግጽ.' },
  send_sms:       { en: 'Send result as SMS?',                                                                    am: 'ውጤቱን SMS ይላኩ?',                                                                                          om: 'Firii SMS erguu?',                                                              ti: 'ውጽኢት SMS ስደድ?' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

export default function VoiceInterface({ lang = 'en', onTranscript, response, onSendSMS }) {
  const voice = useVoice(lang);

  // Read response aloud when it changes
  useEffect(() => {
    if (response) voice.speak(response, lang);
  }, [response]); // eslint-disable-line

  // When transcript is ready, read it back then pass to parent
  useEffect(() => {
    if (voice.transcript) {
      voice.speak(voice.transcript, lang);
      if (onTranscript) onTranscript(voice.transcript);
    }
  }, [voice.transcript]); // eslint-disable-line

  if (!voice.supported) {
    const isHttp = window.location.protocol === 'http:';
    return (
      <div style={{ padding: '1rem' }}>
        <p className="section-title"> {t('tap_to_speak', lang).replace(' ', '')}</p>
        {isHttp ? (
          <div style={{ background: '#fff3e0', borderRadius: 10, padding: '1rem', color: '#e65100' }}>
            <p style={{ fontWeight: 700, marginBottom: 8 }}>️ HTTPS required for voice input</p>
            <p style={{ fontSize: '0.9rem', marginBottom: 12 }}>
              Stop the frontend terminal (Ctrl+C) and restart with:
            </p>
            <div style={{ background: '#1a1a1a', color: '#00ff88', borderRadius: 8, padding: '0.8rem', fontFamily: 'monospace', fontSize: '0.85rem', marginBottom: 8 }}>
              <div>cd health-assistant/frontend</div>
              <div style={{ marginTop: 4 }}>npm run start:https</div>
            </div>
            <p style={{ fontSize: '0.8rem', color: '#888' }}>
              Then open <strong>https://localhost:3000</strong>, click <em>Advanced → Accept the Risk</em> on the certificate warning, and voice will work.
            </p>
          </div>
        ) : (
          <div style={{ color: '#888', fontSize: '0.85rem', padding: '0.5rem', textAlign: 'center' }}>
            {t('not_supported', lang)}
          </div>
        )}
      </div>
    );
  }

  const busy    = voice.isListening || voice.isProcessing;
  const btnBg   = voice.isListening ? '#c62828' : voice.isProcessing ? '#e65100' : '#2e7d32';
  const btnShadow = busy ? `0 0 0 6px ${voice.isListening ? 'rgba(198,40,40,0.3)' : 'rgba(230,81,0,0.3)'}` : 'none';
  const label   = voice.isProcessing ? t('processing', lang)
                : voice.isListening  ? t('listening', lang)
                : t('tap_to_speak', lang);

  function handleMicClick() {
    if (voice.isProcessing) return; // wait for server response
    if (voice.isListening) {
      voice.stopListening();
    } else {
      voice.clearError();
      voice.startListening();
    }
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8 }}>
      {/* Mic button */}
      <button
        onClick={handleMicClick}
        disabled={voice.isProcessing}
        aria-label={label}
        style={{
          width: 64, height: 64, borderRadius: '50%',
          background: btnBg,
          color: '#fff', border: 'none', fontSize: '1.8rem',
          cursor: voice.isProcessing ? 'wait' : 'pointer',
          boxShadow: btnShadow,
          transition: 'all 0.2s',
          opacity: voice.isProcessing ? 0.8 : 1,
        }}
      >
        {voice.isProcessing ? '⏳' : voice.isListening ? '⏹' : ''}
      </button>

      <span style={{ fontSize: '0.8rem', color: voice.isListening ? '#c62828' : voice.isProcessing ? '#e65100' : '#555' }}>
        {label}
      </span>

      {/* Transcript display */}
      {voice.transcript && (
        <div style={{ background: '#e8f5e9', borderRadius: 8, padding: '0.5rem 1rem',
                      fontSize: '0.9rem', maxWidth: 300, textAlign: 'center' }}>
          "{voice.transcript}"
        </div>
      )}

      {/* Error messages */}
      {voice.error === 'permission_denied' && (
        <div style={{ color: '#c62828', fontSize: '0.8rem', textAlign: 'center', maxWidth: 280 }}>
          {t('permission', lang)}
        </div>
      )}
      {(voice.error === 'empty_result' || voice.error === 'recognition_error') && (
        <div style={{ color: '#e65100', fontSize: '0.8rem', textAlign: 'center', maxWidth: 280 }}>
          {t('empty', lang)}
        </div>
      )}
      {voice.error === 'stt_unavailable' && (
        <div style={{ color: '#e65100', fontSize: '0.8rem', textAlign: 'center', maxWidth: 280 }}>
          {t('stt_unavail', lang)}
        </div>
      )}

      {/* SMS offer after assessment */}
      {response && onSendSMS && (
        <button
          onClick={onSendSMS}
          style={{ marginTop: 8, padding: '0.4rem 1rem', borderRadius: 8,
                   background: '#1565c0', color: '#fff', border: 'none',
                   fontSize: '0.85rem', cursor: 'pointer' }}
        >
           {t('send_sms', lang)}
        </button>
      )}
    </div>
  );
}
