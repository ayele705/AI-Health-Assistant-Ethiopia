import React, { useState, useRef, useEffect, useCallback } from 'react';
import { startChat, sendMessage } from '../api';
import { useAccessibility } from '../AccessibilityContext';
import TriageAlert, { detectRedFlags } from './TriageAlert';
import { savePatientLog } from '../services/offlineStore';

// ── i18n ──────────────────────────────────────────────────────────────────────
const T = {
  placeholder_en: 'Message...', placeholder_am: 'መልዕክት...', placeholder_ti: 'መልዕክቲ...', placeholder_om: 'Ergaa...', placeholder_sid: 'Ergaa...',
  conditions_en: 'Possible Conditions', conditions_am: 'ሊሆኑ የሚችሉ ሁኔታዎች', conditions_ti: 'ዝኽእሉ ሕማማት', conditions_om: "Dhukkuboota Danda'aman", conditions_sid: "Dhukkuboota Danda'aman",
  care_en: 'Self-Care Advice', care_am: 'የቤት ውስጥ እንክብካቤ ምክር', care_ti: 'ምኽሪ ናይ ቤት ክንክን', care_om: 'Gorsa Kunuunsa Mana', care_sid: 'Gorsa Kunuunsa Mana',
  restart_en: '+ New Check', restart_am: '+ አዲስ ምርመራ', restart_ti: '+ ሓድሽ ምርመራ', restart_om: "+ Sakatta'a Haaraa", restart_sid: "+ Sakatta'a Haaraa",
  no_match_en: 'No matching condition found. Please visit a health worker.',
  no_match_am: 'ተዛማጅ ሁኔታ አልተገኘም። እባክዎ የጤና ሠራተኛ ያማክሩ።',
  no_match_ti: 'ዝዛመድ ሕማም ኣይተረኽበን። ናብ ሰራሕተኛ ጥዕና ኪድ።',
  no_match_om: 'Dhukkubni wal-simatu hin argamne. Ogeessa fayyaa daawwadhu.',
  no_match_sid: 'Dhukkubni wal-simatu hin argamne. Ogeessa fayyaa daawwadhu.',
  voice_en: 'Speak', voice_am: 'ተናገር', voice_ti: 'ተዛረብ', voice_om: 'Dubbadhu', voice_sid: 'Dubbadhu', voice_so: 'Hadal', voice_aa: 'Hadal', voice_wal: 'Dubbadhu', voice_had: 'Dubbadhu',
  listening_en: 'Listening...', listening_am: 'እያዳመጠ...', listening_ti: 'ይሰምዕ ኣሎ...', listening_om: 'Dhaggeeffachaa...', listening_sid: 'Dhaggeeffachaa...', listening_so: 'Dhageysta...', listening_aa: 'Dhageysta...', listening_wal: 'Dhaggeeffachaa...', listening_had: 'Dhaggeeffachaa...',
  voice_error_en: 'Microphone access denied. Please allow microphone permission in your browser.',
  voice_error_am: 'ማይክሮፎን ፈቃድ ተከልክሏል። በ browser ውስጥ ፈቃድ ይፍቀዱ።',
  voice_error_ti: 'ፍቓድ ማይክሮፎን ተኸልኪሉ። ኣብ browser ፍቓድ ሃብ።',
  voice_error_om: 'Hayyama maaykiroofooni dhorkaame. Browser keessatti hayyama kenni.',
  voice_error_sid: 'Hayyama maaykiroofooni dhorkaame. Browser keessatti hayyama kenni.',
  voice_empty_en: 'Could not hear you. Please try again.',
  voice_empty_am: 'አልሰማዎትም። እንደገና ይሞክሩ።',
  voice_empty_ti: 'ኣይሰማዕናካን። ደጊምካ ፈትን።',
  voice_empty_om: "Sihin dhaggeenye. Irra deebi'i yaali.",
  voice_empty_sid: "Sihin dhaggeenye. Irra deebi'i yaali.",
  hearing_note_en: ' If you are deaf or hard of hearing, bring a sign language interpreter or written notes to the health facility.',
  hearing_note_am: ' መስማት የተሳናዎ ከሆነ ወደ ጤና ጣቢያ ሲሄዱ የምልክት ቋንቋ አስተርጓሚ ወይም የጽሑፍ ማስታወሻ ይዘው ይሂዱ።',
  hearing_note_ti: ' ዘይሰምዕ እንተኾይንካ ናብ ጥዕና ጣቢያ ምስ ከድካ ናይ ምልክት ቋንቋ ተርጓሚ ወይ ጽሑፍ ሒዝካ ኪድ።',
  hearing_note_om: ' Gurri si dhagahuu baate, gara buufata fayyaatti yoo deemtu hiikaa afaan mallattoo ykn barreeffama fidi.',
  hearing_note_sid: ' Gurri si dhagahuu baate, gara buufata fayyaatti yoo deemtu hiikaa afaan mallattoo ykn barreeffama fidi.',
};

function tl(key, lang) {
  return T[`${key}_${lang}`] || T[`${key}_am`] || T[`${key}_en`] || '';
}

const URGENCY = {
  emergency:           { en: ' Emergency',           am: ' አስቸኳይ',           ti: ' ህጹጽ',             om: ' Ariifachiisaa',          sid: ' Ariifachiisaa' },
  visit_health_center: { en: ' Visit Health Center', am: ' ጤና ጣቢያ ይሂዱ',    ti: ' ናብ ጥዕና ጣቢያ ኪድ', om: ' Giddugala Fayyaa Deemi', sid: ' Giddugala Fayyaa Deemi' },
  self_care:           { en: ' Self-Care',            am: ' ቤት ውስጥ እንክብካቤ', ti: ' ናይ ቤት ክንክን',      om: ' Kunuunsa Mana',          sid: ' Kunuunsa Mana' },
};

const L = {
  detected: { en: 'Emergency Signs Detected!', am: 'አስቸኳይ ምልክቶች ተገኝተዋል!', ti: 'ህጹጽ ምልክታት ተረኺቦም!', om: 'Mallattoolee Ariifachiisaa!', sid: 'Mallattoolee Ariifachiisaa!' },
  go_now:   { en: '️ Go to a health facility immediately!', am: '️ ወዲያውኑ ወደ ጤና ጣቢያ ይሂዱ!', ti: '️ ሕጂ ናብ ጥዕና ጣቢያ ኪድ!', om: '️ Amma buufata fayyaa deemi!', sid: '️ Amma buufata fayyaa deemi!' },
  urgent:   { en: 'URGENT — GO NOW!', am: 'አስቸኳይ — ወዲያውኑ ሂድ!', ti: 'ህጹጽ — ሕጂ ኪድ!', om: 'ARIIFACHIISAA — AMMA DEEMI!', sid: 'ARIIFACHIISAA — AMMA DEEMI!' },
  show_hw:  { en: 'Show this to health worker: ', am: 'ይህን ለጤና ሠራተኛ አሳዩ: ', ti: 'ንሰራሕተኛ ጥዕና ኣርኢ: ', om: 'Ogeessa fayyaatti agarsiisi: ', sid: 'Ogeessa fayyaatti agarsiisi: ' },
  result:   { en: 'Assessment result', am: 'የምርመራ ውጤት', ti: 'ውጽኢት ምርመራ', om: "Bu'aa Sakatta'aa", sid: "Bu'aa Sakatta'aa" },
  no_voice: { en: 'Voice input not supported in this browser', am: 'ይህ browser ድምፅ ግቤትን አይደግፍም', ti: 'እዚ browser ናይ ድምጺ ምእታው ኣይድግፍን', om: 'Browser kana keessatti galchituu sagalee hin deeggarre', sid: 'Browser kana keessatti galchituu sagalee hin deeggarre' },
};

// ── TTS ───────────────────────────────────────────────────────────────────────
const GTTS_LANG = { en: 'en', am: 'am', ti: 'ti', om: 'om' };
let _ttsAudio = null;

function speak(text, lang) {
  if (!text) return;
  if (_ttsAudio) { _ttsAudio.pause(); _ttsAudio = null; }
  if (window.speechSynthesis) window.speechSynthesis.cancel();
  const code  = GTTS_LANG[lang] || 'am';
  const chunk = text.slice(0, 200);
  const audio = new Audio(`/api/v1/tts/?lang=${code}&text=${encodeURIComponent(chunk)}`);
  audio.volume = 1.0;
  _ttsAudio = audio;
  audio.play().catch(() => {
    if (window.speechSynthesis) {
      const utt = new SpeechSynthesisUtterance(text);
      utt.lang = 'en-US'; utt.rate = 0.9;
      window.speechSynthesis.speak(utt);
    }
  });
}

// ── Quick replies per step ────────────────────────────────────────────────────
const QUICK_REPLIES = {
  2: {
    en:  ['Fever', 'Cough', 'Headache', 'Vomiting', 'Diarrhea', 'No other symptoms'],
    am:  ['ትኩሳት', 'ሳል', 'ራስ ምታት', 'ማስታወክ', 'ተቅማጥ', 'ሌሎች የሉም'],
    ti:  ['ረስኒ', 'ሳዕዓል', 'ቃንዛ ርእሲ', 'ምትፋእ', 'ተምሲ', 'ካልእ ኣይፋል'],
    om:  ["Ho'a", 'Qufaa', 'Dhukkuba mataa', 'Hanqaaquu', 'Garaa kaasaa', 'Lakki'],
    sid: ["Ho'a", 'Qufaa', 'Dhukkuba mataa', 'Hanqaaquu', 'Garaa kaasaa', 'Lakki'],
  },
  4: {
    en:  ['Male', 'Female'],
    am:  ['ወንድ', 'ሴት'],
    ti:  ['ተባዕታይ', 'ኣንስታይ'],
    om:  ['Dhiira', 'Dhalaa'],
    sid: ['Dhiira', 'Dhalaa'],
  },
};

// ── Component ─────────────────────────────────────────────────────────────────
export default function Chat({ lang }) {
  const { prefs } = useAccessibility();

  // All chat state in one object — batched updates = one render per transition
  const [chat, setChat] = useState({
    messages:  [],
    sessionId: null,
    loading:   true,   // true on mount so we show spinner, not blank flash
    done:      false,
    step:      0,
  });
  const [input, setInput]           = useState('');
  const [listening, setListening]   = useState(false);
  const [voiceError, setVoiceError] = useState('');

  const bottomRef      = useRef(null);
  const inputRef       = useRef(null);
  const recognitionRef = useRef(null);
  const startedRef     = useRef(false);
  const prevLangRef    = useRef(lang);

  // ── Triage alert state ────────────────────────────────────────────────────
  const [triageFlags, setTriageFlags]             = useState([]);
  const [pendingTriageText, setPendingTriageText] = useState(null);
  const symptomListRef = useRef([]);

  // ── handleStart — single setState call, no flash ─────────────────────────
  const handleStart = useCallback(async (overrideLang) => {
    const useLang = overrideLang || lang;

    // One update: reset everything + show spinner
    setChat({ messages: [], sessionId: null, loading: true, done: false, step: 0 });
    setInput('');
    setTriageFlags([]);
    setPendingTriageText(null);
    symptomListRef.current = [];

    try {
      const data = await startChat(useLang);
      // One update: session ready + first message
      setChat({
        messages:  [{ text: data.message || '...', from: 'bot', extra: null }],
        sessionId: data.session_id || null,
        loading:   false,
        done:      false,
        step:      0,
      });
      if (prefs.textToSpeech && data.message) speak(data.message, useLang);
    } catch {
      // One update: show offline message
      setChat({
        messages:  [{ text: 'Could not connect to server. Check your connection and try again.', from: 'bot', extra: null }],
        sessionId: null,
        loading:   false,
        done:      false,
        step:      0,
      });
    }
    setTimeout(() => inputRef.current?.focus(), 100);
  }, [lang, prefs.textToSpeech]); // eslint-disable-line

  // Auto-scroll
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chat.messages, chat.loading]);

  // Auto-start on first mount
  useEffect(() => {
    if (startedRef.current) return;
    startedRef.current = true;
    handleStart();
  }, []); // eslint-disable-line

  // Restart when language changes
  useEffect(() => {
    if (prevLangRef.current === lang) return;
    prevLangRef.current = lang;
    handleStart(lang);
  }, [lang]); // eslint-disable-line

  // Destructure for convenience
  const { messages, sessionId, loading, done, step } = chat;

  // ── handleSend ────────────────────────────────────────────────────────────
  const handleSend = useCallback(async (textOverride) => {
    const text = (textOverride !== undefined ? textOverride : input).trim();
    if (!text || !sessionId || loading) return;

    const flags = detectRedFlags(text, lang);
    if (flags.length > 0) {
      setTriageFlags(flags);
      setPendingTriageText(text);
      return;
    }

    symptomListRef.current = [...symptomListRef.current, text];

    // One update: add user message + spinner
    setChat(prev => ({ ...prev, loading: true, messages: [...prev.messages, { text, from: 'user', extra: null }] }));
    setInput('');

    try {
      const data = await sendMessage(sessionId, text, lang);
      if (data.done) {
        setChat(prev => ({ ...prev, loading: false, done: true, messages: [...prev.messages, { text: '', from: 'bot', extra: data }] }));
        if (prefs.textToSpeech && data.message) speak(data.message, lang);
        try {
          await savePatientLog({ session_id: sessionId, lang, symptoms: symptomListRef.current, red_flags: [], conditions: data.conditions || [], urgency: data.urgency || 'self_care' });
        } catch (e) { console.warn('[PatientLog]', e); }
      } else {
        setChat(prev => ({ ...prev, loading: false, step: data.step ?? prev.step + 1, messages: [...prev.messages, { text: data.message, from: 'bot', extra: null }] }));
        if (prefs.textToSpeech && data.message) speak(data.message, lang);
      }
    } catch {
      setChat(prev => ({ ...prev, loading: false, messages: [...prev.messages, { text: 'Error communicating with server.', from: 'bot', extra: null }] }));
    }
    setTimeout(() => inputRef.current?.focus(), 100);
  }, [input, sessionId, loading, lang, prefs.textToSpeech]); // eslint-disable-line

  // ── Triage alert handlers ─────────────────────────────────────────────────
  const handleTriageContinue = useCallback(async () => {
    const text  = pendingTriageText;
    const flags = triageFlags;
    setTriageFlags([]);
    setPendingTriageText(null);
    if (!text || !sessionId) return;

    try {
      await savePatientLog({ session_id: sessionId, lang, symptoms: [...symptomListRef.current, text], red_flags: flags, conditions: [], urgency: 'emergency' });
    } catch (e) { console.warn('[PatientLog]', e); }

    symptomListRef.current = [...symptomListRef.current, text];
    setChat(prev => ({ ...prev, loading: true, messages: [...prev.messages, { text, from: 'user', extra: null }] }));
    setInput('');

    try {
      const data = await sendMessage(sessionId, text, lang);
      if (data.done) {
        setChat(prev => ({ ...prev, loading: false, done: true, messages: [...prev.messages, { text: '', from: 'bot', extra: data }] }));
        if (prefs.textToSpeech && data.message) speak(data.message, lang);
      } else {
        setChat(prev => ({ ...prev, loading: false, step: data.step ?? prev.step + 1, messages: [...prev.messages, { text: data.message, from: 'bot', extra: null }] }));
        if (prefs.textToSpeech && data.message) speak(data.message, lang);
      }
    } catch {
      setChat(prev => ({ ...prev, loading: false, messages: [...prev.messages, { text: 'Error communicating with server.', from: 'bot', extra: null }] }));
    }
    setTimeout(() => inputRef.current?.focus(), 100);
  }, [pendingTriageText, triageFlags, sessionId, lang, prefs.textToSpeech]); // eslint-disable-line

  const handleTriageDismiss = useCallback(() => {
    setTriageFlags([]);
    setPendingTriageText(null);
    setTimeout(() => inputRef.current?.focus(), 100);
  }, []);

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
  };

  // ── Voice helpers ─────────────────────────────────────────────────────────
  const nativeSRSupported = !!(window.SpeechRecognition || window.webkitSpeechRecognition);
  const mediaRecSupported = !!(navigator.mediaDevices?.getUserMedia && window.MediaRecorder);

  const LANG_MAP = {
    en: 'en-US', am: 'am-ET', ti: 'ti-ET', om: 'om-ET',
    sid: 'sid-ET', so: 'so-SO', aa: 'aa-ET', wal: 'wal-ET', had: 'had-ET',
  };

  // Server-side STT via MediaRecorder fallback
  const startMediaRecorder = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const types = ['audio/webm;codecs=opus','audio/webm','audio/ogg;codecs=opus','audio/ogg','audio/mp4'];
      const mimeType = types.find(t => MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(t)) || '';
      const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : {});
      const chunks = [];

      recorder.ondataavailable = (e) => { if (e.data.size > 0) chunks.push(e.data); };
      recorder.onstop = async () => {
        stream.getTracks().forEach(t => t.stop());
        setListening(false);
        const blob = new Blob(chunks, { type: mimeType || 'audio/webm' });
        const form = new FormData();
        form.append('audio', blob, mimeType?.includes('ogg') ? 'rec.ogg' : 'rec.webm');
        form.append('lang', lang);
        try {
          const res  = await fetch('/api/v1/stt/', { method: 'POST', body: form });
          const data = await res.json();
          if (data.transcript?.trim()) {
            setInput(data.transcript);
            setVoiceError('');
          } else if (data.error === 'no_speech') {
            setVoiceError(tl('voice_empty', lang));
          } else {
            setVoiceError(tl('voice_empty', lang));
          }
        } catch {
          setVoiceError(tl('voice_empty', lang));
        }
      };
      recorder.onerror = () => { stream.getTracks().forEach(t => t.stop()); setListening(false); setVoiceError(tl('voice_empty', lang)); };

      recognitionRef.current = { stop: () => recorder.state === 'recording' && recorder.stop(), _isMediaRec: true };
      recorder.start();
      setListening(true);
      setVoiceError('');
    } catch (err) {
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        setVoiceError(tl('voice_error', lang));
      } else {
        setVoiceError(tl('voice_empty', lang));
      }
      setListening(false);
    }
  };

  const handleVoice = () => {
    if (listening) { recognitionRef.current?.stop(); setListening(false); return; }
    setVoiceError('');

    if (nativeSRSupported) {
      // Native Web Speech API (Chrome/Edge)
      const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
      const rec = new SR();
      rec.lang = LANG_MAP[lang] || 'en-US';
      rec.interimResults = false;
      rec.onresult = (e) => {
        const text = e.results[0][0].transcript;
        if (text.trim()) { setInput(text); setVoiceError(''); }
        else { setVoiceError(tl('voice_empty', lang)); }
        setListening(false);
      };
      rec.onerror = (e) => {
        setVoiceError(e.error === 'not-allowed' ? tl('voice_error', lang) : tl('voice_empty', lang));
        setListening(false);
      };
      rec.onend = () => setListening(false);
      recognitionRef.current = rec;
      rec.start(); setListening(true);
    } else if (mediaRecSupported) {
      // Server-side STT fallback (Firefox, Safari, WebView)
      startMediaRecorder();
    } else {
      setVoiceError(L.no_voice[lang] || L.no_voice.en);
    }
  };

  const quickReplies = QUICK_REPLIES[step]?.[lang] || QUICK_REPLIES[step]?.en || [];

  // ── Render ────────────────────────────────────────────────────────────────
  return (
    <div className="chat-container">
      {/* Triage Alert — rendered outside the chat flow, above everything */}
      <TriageAlert
        flags={triageFlags}
        lang={lang}
        onContinue={handleTriageContinue}
        onDismiss={handleTriageDismiss}
      />

      {prefs.hearingMode && (
        <div className="hearing-notice"> {tl('hearing_note', lang)}</div>
      )}

      <div className="messages" role="log" aria-live="polite">
        {messages.map((m, i) => (
          <div key={i} className={`msg ${m.from}`}>
            {m.extra ? (
              <AssessmentCard data={m.extra} lang={lang} prefs={prefs} />
            ) : (
              <div className="msg-inner">
                <span className="msg-text">{m.text}</span>
                {m.from === 'bot' && m.text && (
                  <button className="tts-btn" onClick={() => speak(m.text, lang)} title="Read aloud" aria-label="Read aloud"></button>
                )}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="msg bot">
            <div className="typing-indicator"><span /><span /><span /></div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {!loading && !done && sessionId && quickReplies.length > 0 && (
        <div className="quick-replies">
          {quickReplies.map((r, i) => (
            <button key={i} className="quick-reply-btn" onClick={() => handleSend(r)}>{r}</button>
          ))}
        </div>
      )}

      <div className="chat-input-row">
        {done && (
          <button className="new-chat-btn" onClick={() => handleStart()}>{tl('restart', lang)}</button>
        )}
        {voiceError && (
          <div className="voice-error" role="alert" aria-live="assertive">
            ️ {voiceError}
            <button className="voice-error-close" onClick={() => setVoiceError('')} aria-label="Dismiss"></button>
          </div>
        )}
        <input
          ref={inputRef}
          className="chat-input"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKey}
          placeholder={tl('placeholder', lang)}
          disabled={loading || !sessionId}
          aria-label="Message input"
        />
        {prefs.voiceInput && (
          <button
            className={`icon-btn ${listening ? 'listening' : ''}`}
            onClick={handleVoice}
            title={listening ? tl('listening', lang) : tl('voice', lang)}
            aria-label={listening ? tl('listening', lang) : tl('voice', lang)}
          >
            {listening ? 'Stop' : 'Mic'}
          </button>
        )}
        <button
          className="icon-btn send"
          onClick={() => handleSend()}
          disabled={loading || !input.trim()}
          aria-label="Send"
        >
          Send
        </button>
      </div>
    </div>
  );
}

// ── Assessment Card ───────────────────────────────────────────────────────────
function AssessmentCard({ data, lang, prefs }) {
  const hasConditions = data.conditions?.length > 0;
  const hasEmergency  = data.emergency_alerts?.length > 0;
  const urgencyLabel  = (URGENCY[data.urgency] || URGENCY.self_care)[lang]
                     || (URGENCY[data.urgency] || URGENCY.self_care).en;

  return (
    <div role="region" aria-label={L.result[lang] || L.result.en}>
      {hasEmergency && (
        <div className="emergency-card" role="alert" aria-live="assertive">
          <p className="emergency-title"> {L.detected[lang] || L.detected.en}</p>
          {data.emergency_alerts.map((alert, i) => (
            <div key={i} className="emergency-item">
              <strong>{alert.condition}:</strong> {alert.signs.join(', ')}
            </div>
          ))}
          <p className="emergency-go">{L.go_now[lang] || L.go_now.en}</p>
          {prefs?.hearingMode && (
            <div className="emergency-visual"> {L.urgent[lang] || L.urgent.en}</div>
          )}
        </div>
      )}

      {!hasConditions ? (
        <p>{tl('no_match', lang)}</p>
      ) : (
        <div className="assessment-card">
          {data.message && <p className="assessment-msg">{data.message}</p>}
          <span className={`urgency-badge ${data.urgency || 'self_care'}`}>{urgencyLabel}</span>

          {prefs?.hearingMode && data.urgency !== 'self_care' && (
            <div className="show-hw-note">
              ️ {(L.show_hw[lang] || L.show_hw.en) + (data.conditions[0]?.name || '')}
            </div>
          )}

          <p className="section-title" style={{ marginTop: 12 }}>{tl('conditions', lang)}</p>
          {data.conditions.map((c, i) => (
            <div key={i} className="condition-item">
              <div className="condition-name">
                {c.name}
                {c.score != null && <span className="confidence"> ({Math.round(c.score * 100)}%)</span>}
                <button
                  className="tts-btn"
                  onClick={() => speak(`${c.name}. ${c.description}. ${c.self_care}`, lang)}
                  aria-label={`Read ${c.name} aloud`}
                ></button>
              </div>
              <div className="condition-desc">{c.description}</div>
              {c.self_care && (
                <div className="condition-care"> {tl('care', lang)}: {c.self_care}</div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
