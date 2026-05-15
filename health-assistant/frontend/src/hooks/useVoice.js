/**
 * useVoice — Web Speech API with server-side STT fallback.
 *
 * Strategy:
 *  1. If the browser supports Web Speech API (Chrome/Edge), use it directly.
 *  2. Otherwise, record audio via MediaRecorder and POST to /api/v1/stt/
 *     which transcribes it server-side (works in Firefox, Safari, WebView).
 */
import { useState, useRef, useCallback } from 'react';

const LANG_CODES = {
  en: 'en-US', am: 'am-ET', ti: 'ti-ET', om: 'om-ET',
};

// Languages natively supported by Web Speech API (browser-dependent)
const NATIVE_STT_LANGS = new Set(['en', 'en-US', 'en-GB']);

// Best MIME type the current browser supports for recording
function getBestMimeType() {
  const types = [
    'audio/webm;codecs=opus',
    'audio/webm',
    'audio/ogg;codecs=opus',
    'audio/ogg',
    'audio/mp4',
  ];
  for (const t of types) {
    if (MediaRecorder.isTypeSupported && MediaRecorder.isTypeSupported(t)) return t;
  }
  return '';
}

export default function useVoice(lang = 'en') {
  const [isListening, setIsListening]   = useState(false);
  const [transcript, setTranscript]     = useState('');
  const [error, setError]               = useState('');
  const [isProcessing, setIsProcessing] = useState(false); // server STT in-flight

  const recognitionRef  = useRef(null);
  const mediaRecRef     = useRef(null);
  const chunksRef       = useRef([]);
  const synthRef        = useRef(window.speechSynthesis);

  const nativeSpeechSupported = !!(window.SpeechRecognition || window.webkitSpeechRecognition);
  const mediaRecSupported     = !!(navigator.mediaDevices?.getUserMedia && window.MediaRecorder);
  const supported             = nativeSpeechSupported || mediaRecSupported;

  // ── Native Web Speech API path ────────────────────────────────────────────
  const startNative = useCallback(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.lang             = LANG_CODES[lang] || 'en-US';
    recognition.interimResults   = false;
    recognition.maxAlternatives  = 1;

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      if (!text.trim()) {
        setError('empty_result');
      } else {
        setTranscript(text);
        setError('');
      }
      setIsListening(false);
    };

    recognition.onerror = (event) => {
      if (event.error === 'not-allowed') {
        setError('permission_denied');
      } else if (event.error === 'no-speech') {
        setError('empty_result');
      } else {
        setError('recognition_error');
      }
      setIsListening(false);
    };

    recognition.onend = () => setIsListening(false);

    recognitionRef.current = recognition;
    recognition.start();
    setIsListening(true);
  }, [lang]);

  // ── MediaRecorder → server STT fallback path ──────────────────────────────
  const startMediaRecorder = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mimeType = getBestMimeType();
      const options  = mimeType ? { mimeType } : {};
      const recorder = new MediaRecorder(stream, options);

      chunksRef.current = [];
      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };

      recorder.onstop = async () => {
        // Stop all tracks to release the mic
        stream.getTracks().forEach(t => t.stop());
        setIsListening(false);
        setIsProcessing(true);

        const blob = new Blob(chunksRef.current, { type: mimeType || 'audio/webm' });
        const formData = new FormData();
        formData.append('audio', blob, 'recording' + (mimeType?.includes('ogg') ? '.ogg' : '.webm'));
        formData.append('lang', lang);

        try {
          const res = await fetch('/api/v1/stt/', { method: 'POST', body: formData });
          const data = await res.json();
          if (data.transcript?.trim()) {
            setTranscript(data.transcript);
            setError('');
          } else if (data.error === 'no_speech') {
            setError('empty_result');
          } else if (data.error === 'stt_unavailable') {
            setError('stt_unavailable');
          } else {
            setError('recognition_error');
          }
        } catch {
          setError('recognition_error');
        } finally {
          setIsProcessing(false);
        }
      };

      recorder.onerror = () => {
        stream.getTracks().forEach(t => t.stop());
        setIsListening(false);
        setError('recognition_error');
      };

      mediaRecRef.current = recorder;
      recorder.start();
      setIsListening(true);
      setError('');
    } catch (err) {
      if (err.name === 'NotAllowedError' || err.name === 'PermissionDeniedError') {
        setError('permission_denied');
      } else {
        setError('recognition_error');
      }
      setIsListening(false);
    }
  }, [lang]);

  // ── Public API ────────────────────────────────────────────────────────────
  const startListening = useCallback(() => {
    setError('');
    setTranscript('');
    if (nativeSpeechSupported) {
      startNative();
    } else if (mediaRecSupported) {
      startMediaRecorder();
    } else {
      setError('speech_not_supported');
    }
  }, [nativeSpeechSupported, mediaRecSupported, startNative, startMediaRecorder]);

  const stopListening = useCallback(() => {
    if (nativeSpeechSupported && recognitionRef.current) {
      recognitionRef.current.stop();
    } else if (mediaRecRef.current && mediaRecRef.current.state === 'recording') {
      mediaRecRef.current.stop(); // triggers onstop → server call
    }
    setIsListening(false);
  }, [nativeSpeechSupported]);

  const speak = useCallback((text, overrideLang) => {
    if (!synthRef.current) return;
    synthRef.current.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = LANG_CODES[overrideLang || lang] || 'en-US';
    utterance.rate = 0.9;
    synthRef.current.speak(utterance);
  }, [lang]);

  const fallbackAudio = useCallback((clipUrl) => {
    if (!clipUrl) return;
    const audio = new Audio(clipUrl);
    audio.play().catch(() => {});
  }, []);

  const isNativeSTT = NATIVE_STT_LANGS.has(lang);

  return {
    isListening,
    isProcessing,
    transcript,
    error,
    supported,
    isNativeSTT,
    startListening,
    stopListening,
    speak,
    fallbackAudio,
    clearTranscript: () => setTranscript(''),
    clearError:      () => setError(''),
  };
}
