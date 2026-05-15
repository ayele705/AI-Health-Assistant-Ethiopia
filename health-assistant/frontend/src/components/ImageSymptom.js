/**
 * ImageSymptom — Camera/gallery image capture + on-device classification.
 */
import React, { useState, useRef } from 'react';
import { analyseImage, compressImage, scheduleImageDelete } from '../services/imageAnalyser';

const L = {
  title:       { en: ' Photo Symptom Check', am: ' ፎቶ ምልክት ምርመራ', ti: ' ስእሊ ምልክት', om: ' Suuraa Mallattoo', sid: ' Suuraa Mallattoo', so: ' Hubinta Calaamadaha Sawirka', aa: ' Hubinta Calaamadaha Sawirka', wal: ' Suuraa Mallattoo', had: ' Suuraa Mallattoo' },
  take_photo:  { en: ' Take Photo', am: ' ፎቶ ያንሱ', ti: ' ስእሊ ውሰድ', om: ' Suuraa kaadhu', sid: ' Suuraa kaadhu', so: ' Sawir Qaado', aa: ' Sawir Qaado', wal: ' Suuraa kaadhu', had: ' Suuraa kaadhu' },
  gallery:     { en: ' Choose from Gallery', am: ' ከጋለሪ ይምረጡ', ti: ' ካብ ጋለሪ ምረጽ', om: ' Galarii keessaa filadhu', sid: ' Galarii keessaa filadhu', so: ' Ka Dooro Galariiga', aa: ' Ka Dooro Galariiga', wal: ' Galarii keessaa filadhu', had: ' Galarii keessaa filadhu' },
  analysing:   { en: 'Analysing image…', am: 'ምስሉን እየተነተነ ነው…', ti: 'ስእሊ ይምርምር ኣሎ…', om: 'Suuraa xiinxalaa…', sid: 'Suuraa xiinxalaa…', so: 'Sawirka waa la falanqeynayaa…', aa: 'Sawirka waa la falanqeynayaa…', wal: 'Suuraa xiinxalaa…', had: 'Suuraa xiinxalaa…' },
  low_conf:    { en: 'Image unclear. Please retake in better lighting or describe using voice.', am: 'ምስሉ ግልፅ አይደለም። ደህና ብርሃን ባለበት ቦታ ይሞክሩ።', ti: 'ስእሊ ብሩህ ኣይኮነን። ኣብ ጽቡቕ ብርሃን ደጊምካ ውሰድ።', om: 'Suuraan ifa miti. Ifa gaarii keessatti irra deebi\'i kaadhu.', sid: 'Suuraan ifa miti.', so: 'Sawirku ma cad. Dib u qaado meel iftiimaysa.', aa: 'Sawirku ma cad. Dib u qaado meel iftiimaysa.', wal: 'Suuraan ifa miti.', had: 'Suuraan ifa miti.' },
  consent:     { en: 'Allow uploading this image to improve analysis? (Optional)', am: 'ምስሉን ለማሻሻል ወደ ሰርቨር ይላኩ? (አማራጭ)', ti: 'ስእሊ ናብ ሰርቨር ስደድ? (ምርጫ)', om: 'Suuraa kana server erguu hayyamta? (Filannoo)', sid: 'Suuraa kana server erguu hayyamta?', so: 'Ma oggoshahay in sawirkan la soo rarayo? (Ikhtiyaari)', aa: 'Ma oggoshahay in sawirkan la soo rarayo?', wal: 'Suuraa kana server erguu hayyamta?', had: 'Suuraa kana server erguu hayyamta?' },
  result:      { en: 'Detected:', am: 'የተገኘ:', ti: 'ተረኺቡ:', om: 'Argame:', sid: 'Argame:', so: 'La ogaaday:', aa: 'La ogaaday:', wal: 'Argame:', had: 'Argame:' },
  confidence:  { en: 'Confidence:', am: 'እርግጠኝነት:', ti: 'ርግጸኝነት:', om: 'Amantaa:', sid: 'Amantaa:', so: 'Kalsoonida:', aa: 'Kalsoonida:', wal: 'Amantaa:', had: 'Amantaa:' },
  yes:         { en: 'Yes', am: 'አዎ', ti: 'እወ', om: 'Eeyyee', sid: 'Eeyyee', so: 'Haa', aa: 'Haa', wal: 'Eeyyee', had: 'Eeyyee' },
  no:          { en: 'No', am: 'አይ', ti: 'ኣይፋሉን', om: 'Lakki', sid: 'Lakki', so: 'Maya', aa: 'Maya', wal: 'Lakki', had: 'Lakki' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

const CATEGORY_LABELS = {
  wound: { en: 'Wound', am: 'ቁስል', om: 'Madaa', ti: 'ቁስሊ' },
  rash: { en: 'Rash', am: 'ሽፍታ', om: 'Qorii', ti: 'ሽፍታ' },
  skin_infection: { en: 'Skin Infection', am: 'የቆዳ ኢንፌክሽን', om: 'Dhukkuba gogaa', ti: 'ኢንፌክሽን ቆዳ' },
  eye_condition: { en: 'Eye Condition', am: 'የዓይን ሁኔታ', om: 'Dhukkuba ija', ti: 'ሕማም ዓይኒ' },
  other: { en: 'Other', am: 'ሌላ', om: 'Kan biraa', ti: 'ካልእ' },
};

export default function ImageSymptom({ lang = 'en', onResult }) {
  const [result, setResult]         = useState(null);
  const [analysing, setAnalysing]   = useState(false);
  const [preview, setPreview]       = useState(null);
  const [consentAsked, setConsentAsked] = useState(false);
  const fileRef = useRef();

  async function handleFile(file) {
    if (!file) return;
    const objUrl = URL.createObjectURL(file);
    setPreview(objUrl);
    setAnalysing(true);
    setResult(null);

    try {
      const res = await analyseImage(file);
      setResult(res);
      scheduleImageDelete(`img_${Date.now()}`);
      if (!res.low_confidence && onResult) {
        onResult(res);
      }
      if (!res.low_confidence) setConsentAsked(true);
    } finally {
      setAnalysing(false);
    }
  }

  const catLabel = (cat) => (CATEGORY_LABELS[cat] || {})[lang] || cat;

  return (
    <div style={{ padding: '0.5rem' }}>
      <p className="section-title">{t('title', lang)}</p>

      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 12 }}>
        <button
          onClick={() => { fileRef.current.setAttribute('capture', 'environment'); fileRef.current.click(); }}
          style={{ padding: '0.5rem 1rem', borderRadius: 8, background: '#2e7d32',
                   color: '#fff', border: 'none', cursor: 'pointer', fontSize: '0.9rem' }}
        >
          {t('take_photo', lang)}
        </button>
        <button
          onClick={() => { fileRef.current.removeAttribute('capture'); fileRef.current.click(); }}
          style={{ padding: '0.5rem 1rem', borderRadius: 8, background: '#1565c0',
                   color: '#fff', border: 'none', cursor: 'pointer', fontSize: '0.9rem' }}
        >
          {t('gallery', lang)}
        </button>
        <input
          ref={fileRef} type="file" accept="image/*" style={{ display: 'none' }}
          onChange={(e) => handleFile(e.target.files[0])}
        />
      </div>

      {preview && (
        <img src={preview} alt="symptom" style={{ maxWidth: 200, borderRadius: 8, marginBottom: 8 }} />
      )}

      {analysing && (
        <p style={{ color: '#555', fontSize: '0.9rem' }}>{t('analysing', lang)}</p>
      )}

      {result && !result.low_confidence && (
        <div style={{ background: '#e8f5e9', borderRadius: 8, padding: '0.7rem 1rem' }}>
          <div><strong>{t('result', lang)}</strong> {catLabel(result.category)}</div>
          <div style={{ fontSize: '0.8rem', color: '#555' }}>
            {t('confidence', lang)} {Math.round(result.confidence * 100)}%
          </div>
        </div>
      )}

      {result?.low_confidence && (
        <div style={{ background: '#fff3e0', borderRadius: 8, padding: '0.7rem 1rem',
                      color: '#e65100', fontSize: '0.9rem' }}>
          {t('low_conf', lang)}
        </div>
      )}

      {consentAsked && (
        <div style={{ marginTop: 8, fontSize: '0.8rem', color: '#555' }}>
          {t('consent', lang)}
          <button onClick={() => { setConsentAsked(false); }}
            style={{ marginLeft: 8, padding: '2px 8px', borderRadius: 4, background: '#1565c0', color: '#fff', border: 'none', cursor: 'pointer' }}>
            {t('yes', lang)}
          </button>
          <button onClick={() => setConsentAsked(false)}
            style={{ marginLeft: 4, padding: '2px 8px', borderRadius: 4, background: '#ccc', border: 'none', cursor: 'pointer' }}>
            {t('no', lang)}
          </button>
        </div>
      )}
    </div>
  );
}
