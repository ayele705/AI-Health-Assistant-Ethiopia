/**
 * FeedbackWidget — Inline star rating + comment for any feature.
 * Designed to be embedded at the bottom of any component.
 * Full multilingual: en, am, ti, om, sid, so, aa, wal, had
 */
import React, { useState } from 'react';

const BASE = '/api/v1';

const L = {
  prompt:   { en: 'Was this helpful?', am: 'ይህ ጠቃሚ ነበር?', ti: 'እዚ ሓጋዚ ነይሩ?', om: 'Kun gargaaraa ture?', sid: 'Kun gargaaraa ture?', so: 'Ma faa\'iido buu lahaa?', aa: 'Ma faa\'iido buu lahaa?', wal: 'Kun gargaaraa ture?', had: 'Kun gargaaraa ture?' },
  comment:  { en: 'Any comments? (optional)', am: 'አስተያየት? (አማራጭ)', ti: 'ርእይቶ? (ምርጫ)', om: 'Yaada? (dirqama miti)', sid: 'Yaada? (dirqama miti)', so: 'Faallo? (ikhtiyaari)', aa: 'Faallo? (ikhtiyaari)', wal: 'Yaada? (dirqama miti)', had: 'Yaada? (dirqama miti)' },
  submit:   { en: 'Send', am: 'ላክ', ti: 'ስደድ', om: 'Ergi', sid: 'Ergi', so: 'Dir', aa: 'Dir', wal: 'Ergi', had: 'Ergi' },
  thanks:   { en: ' Thank you for your feedback!', am: ' አስተያየትዎ ስለሰጡ እናመሰግናለን!', ti: ' ርእይቶኻ ስለሃብካ ነመስግን!', om: ' Yaada keetiif galatoomi!', sid: ' Yaada keetiif galatoomi!', so: ' Mahadsanid faalladaada!', aa: ' Mahadsanid faalladaada!', wal: ' Yaada keetiif galatoomi!', had: ' Yaada keetiif galatoomi!' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

export default function FeedbackWidget({ lang = 'en', featureUsed = '', sessionId = '' }) {
  const [rating, setRating]   = useState(0);
  const [hover, setHover]     = useState(0);
  const [comment, setComment] = useState('');
  const [submitted, setSubmitted] = useState(false);

  async function submit() {
    if (!rating) return;
    try {
      await fetch(`${BASE}/feedback/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId || `anon_${Date.now()}`,
          rating,
          helpful: rating >= 3,
          comment,
          language: lang,
          feature_used: featureUsed,
        }),
      });
    } catch { /* offline — best effort */ }
    setSubmitted(true);
  }

  if (submitted) {
    return (
      <div style={{ marginTop: 12, padding: '0.5rem', background: '#e8f5e9', borderRadius: 8, fontSize: '0.82rem', color: '#2e7d32', textAlign: 'center' }}>
        {t('thanks', lang)}
      </div>
    );
  }

  return (
    <div style={{ marginTop: 14, padding: '0.6rem', background: '#f9f9f9', borderRadius: 8, borderTop: '1px solid #e0e0e0' }}>
      <p style={{ fontSize: '0.82rem', color: '#555', marginBottom: 6 }}>{t('prompt', lang)}</p>
      <div style={{ display: 'flex', gap: 4, marginBottom: 8 }}>
        {[1, 2, 3, 4, 5].map((star) => (
          <button key={star}
            onClick={() => setRating(star)}
            onMouseEnter={() => setHover(star)}
            onMouseLeave={() => setHover(0)}
            style={{
              fontSize: '1.4rem', background: 'none', border: 'none', cursor: 'pointer',
              color: star <= (hover || rating) ? '#f9a825' : '#ccc',
              padding: '0 2px', lineHeight: 1,
            }}
            aria-label={`${star} star`}>
            
          </button>
        ))}
      </div>
      {rating > 0 && (
        <>
          <textarea placeholder={t('comment', lang)} value={comment}
            onChange={(e) => setComment(e.target.value)}
            rows={2}
            style={{ display: 'block', width: '100%', padding: '0.4rem', borderRadius: 6, border: '1px solid #ccc', fontSize: '0.8rem', boxSizing: 'border-box', marginBottom: 6, resize: 'none' }} />
          <button onClick={submit}
            style={{ padding: '0.3rem 1rem', borderRadius: 6, background: '#1565c0', color: '#fff', border: 'none', cursor: 'pointer', fontSize: '0.82rem' }}>
            {t('submit', lang)}
          </button>
        </>
      )}
    </div>
  );
}
