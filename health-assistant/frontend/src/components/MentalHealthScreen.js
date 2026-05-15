/**
 * MentalHealthScreen — PHQ-2 + GAD-2 mental health screening.
 * Culturally adapted for Ethiopian rural communities.
 * Full multilingual: en, am, ti, om, sid, so, aa, wal, had
 */
import React, { useState, useEffect } from 'react';

const BASE = '/api/v1';

const L = {
  title:       { en: ' Mental Health Check', am: ' የአዕምሮ ጤና ምርመራ', ti: ' ምርመራ ጥዕና ኣእምሮ', om: ' Sakatta\'i Fayyaa Sammuu', sid: ' Sakatta\'i Fayyaa Sammuu', so: ' Hubinta Caafimaadka Maskaxda', aa: ' Hubinta Caafimaadka Maskaxda', wal: ' Sakatta\'i Fayyaa Sammuu', had: ' Sakatta\'i Fayyaa Sammuu' },
  intro:       { en: 'These questions help identify if you may need support. Your answers are private.', am: 'እነዚህ ጥያቄዎች ድጋፍ ሊያስፈልግዎ እንደሚችል ለማወቅ ይረዳሉ። መልሶቹ ሚስጥራዊ ናቸው።', ti: 'እዚ ሕቶታት ሓገዝ ከምዘድልየካ ንምፍላጥ ይሕግዝ። መልስታትካ ሚስጢር ኢዩ።', om: 'Gaaffiileen kun gargaarsa si barbaachisu beekuuf gargaaru. Deebiin kee dhokataa dha.', sid: 'Gaaffiileen kun gargaarsa si barbaachisu beekuuf gargaaru.', so: 'Su\'aalahan waxay kaa caawiyaan in la ogaado haddaad u baahantahay taageero. Jawaabahaaagu waa sir.', aa: 'Su\'aalahan waxay kaa caawiyaan in la ogaado haddaad u baahantahay taageero.', wal: 'Gaaffiileen kun gargaarsa si barbaachisu beekuuf gargaaru.', had: 'Gaaffiileen kun gargaarsa si barbaachisu beekuuf gargaaru.' },
  phq2_title:  { en: 'Depression Screen (PHQ-2)', am: 'የድብርት ምርመራ (PHQ-2)', ti: 'ምርመራ ጓሂ (PHQ-2)', om: 'Sakatta\'i Gaddaa (PHQ-2)', sid: 'Sakatta\'i Gaddaa (PHQ-2)', so: 'Baaritaanka Murugada (PHQ-2)', aa: 'Baaritaanka Murugada (PHQ-2)', wal: 'Sakatta\'i Gaddaa (PHQ-2)', had: 'Sakatta\'i Gaddaa (PHQ-2)' },
  gad2_title:  { en: 'Anxiety Screen (GAD-2)', am: 'የጭንቀት ምርመራ (GAD-2)', ti: 'ምርመራ ሻቕሎት (GAD-2)', om: 'Sakatta\'i Yaaddoo (GAD-2)', sid: 'Sakatta\'i Yaaddoo (GAD-2)', so: 'Baaritaanka Welwelka (GAD-2)', aa: 'Baaritaanka Welwelka (GAD-2)', wal: 'Sakatta\'i Yaaddoo (GAD-2)', had: 'Sakatta\'i Yaaddoo (GAD-2)' },
  submit:      { en: 'Get Results', am: 'ውጤቶችን ያግኙ', ti: 'ውጽኢት ርኸብ', om: 'Firii Argadhu', sid: 'Firii Argadhu', so: 'Hel Natiijooyinka', aa: 'Hel Natiijooyinka', wal: 'Firii Argadhu', had: 'Firii Argadhu' },
  loading:     { en: 'Assessing…', am: 'በመገምገም ላይ…', ti: 'ይግምገም ኣሎ…', om: 'Madaallamaa jira…', sid: 'Madaallamaa jira…', so: 'Waa la qiimeynayaa…', aa: 'Waa la qiimeynayaa…', wal: 'Madaallamaa jira…', had: 'Madaallamaa jira…' },
  restart:     { en: 'Start Over', am: 'እንደገና ጀምር', ti: 'ካብ መጀመርታ ጀምር', om: 'Jalqaba irraa jalqabi', sid: 'Jalqaba irraa jalqabi', so: 'Dib u bilow', aa: 'Dib u bilow', wal: 'Jalqaba irraa jalqabi', had: 'Jalqaba irraa jalqabi' },
  crisis_help: { en: ' If you are thinking of harming yourself, please tell someone you trust and go to your nearest health center immediately.', am: ' ራስዎን ለመጉዳት ካሰቡ፣ ወዲያውኑ ለሚያምኑት ሰው ይናገሩ እና ወደ ቅርብ ጤና ጣቢያ ይሂዱ።', ti: ' ነብስኻ ንምጉዳእ ሓሳብ እንተሃልዩካ፡ ወዲኡ ንዝኣምኖ ሰብ ንገሮ ናብ ቀረባ ጥዕና ጣቢያ ኺድ።', om: ' Of miidhuuf yaada yoo qabaatte, namni amanamaa tokko itti himi, buufata fayyaa dhiyoo deemi.', sid: ' Of miidhuuf yaada yoo qabaatte, namni amanamaa tokko itti himi.', so: ' Haddaad u maleynayso in aad is dhaawacdo, fadlan qof aad aamintahay u sheeg oo xarunta caafimaadka u tag.', aa: ' Haddaad u maleynayso in aad is dhaawacdo, fadlan qof aad aamintahay u sheeg.', wal: ' Of miidhuuf yaada yoo qabaatte, namni amanamaa tokko itti himi.', had: ' Of miidhuuf yaada yoo qabaatte, namni amanamaa tokko itti himi.' },
};
const t = (k, lang) => (L[k] || {})[lang] || (L[k] || {}).en || k;

const SCORE_LABELS = {
  en: ['Not at all', 'Several days', 'More than half the days', 'Nearly every day'],
  am: ['ጭራሽ አይደለም', 'ጥቂት ቀናት', 'ከግማሽ ቀናት በላይ', 'ሁሉም ቀናት ማለት ይቻላል'],
  om: ['Gonkumaa miti', 'Guyyoota muraasa', 'Guyyoota walakkaa ol', 'Guyyaa hunda'],
  ti: ['ፈጺሙ ኣይኮነን', 'ሒደት መዓልታት', 'ካብ ፍርቂ ንላዕሊ', 'ኩሉ ቀን ማለት'],
};

function ScoreSelector({ question, value, onChange, lang }) {
  const labels = SCORE_LABELS[lang] || SCORE_LABELS.en;
  return (
    <div style={{ marginBottom: 16 }}>
      <p style={{ fontSize: '0.9rem', fontWeight: 600, marginBottom: 8, color: '#333' }}>{question}</p>
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
        {[0, 1, 2, 3].map((score) => (
          <button key={score} onClick={() => onChange(score)}
            style={{
              padding: '6px 12px', borderRadius: 8, border: '2px solid',
              borderColor: value === score ? '#1565c0' : '#ccc',
              background: value === score ? '#1565c0' : '#fff',
              color: value === score ? '#fff' : '#333',
              cursor: 'pointer', fontSize: '0.78rem', transition: 'all 0.15s',
            }}>
            <div style={{ fontWeight: 700 }}>{score}</div>
            <div style={{ fontSize: '0.65rem' }}>{labels[score]}</div>
          </button>
        ))}
      </div>
    </div>
  );
}

export default function MentalHealthScreen({ lang = 'en' }) {
  const [questions, setQuestions] = useState(null);
  const [phq2, setPhq2]           = useState([null, null]);
  const [gad2, setGad2]           = useState([null, null]);
  const [result, setResult]       = useState(null);
  const [loading, setLoading]     = useState(false);

  useEffect(() => {
    fetch(`${BASE}/mental-health/questions/?language=${lang}`)
      .then((r) => r.json())
      .then(setQuestions)
      .catch(() => {});
  }, [lang]);

  const allAnswered = phq2.every((v) => v !== null) && gad2.every((v) => v !== null);

  async function submit() {
    setLoading(true);
    try {
      const res = await fetch(`${BASE}/mental-health/screen/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phq2_scores: phq2, gad2_scores: gad2, language: lang }),
      });
      const data = await res.json();
      setResult(data);
    } catch { /* offline */ } finally { setLoading(false); }
  }

  function reset() {
    setPhq2([null, null]);
    setGad2([null, null]);
    setResult(null);
  }

  const urgencyColor = (level) => level === 'positive' ? '#c62828' : '#2e7d32';
  const urgencyBg    = (level) => level === 'positive' ? '#ffebee' : '#e8f5e9';

  return (
    <div style={{ padding: '0.5rem' }}>
      <p className="section-title">{t('title', lang)}</p>

      {!result && (
        <div style={{ background: '#e3f2fd', borderRadius: 8, padding: '0.7rem', marginBottom: 12, fontSize: '0.85rem', color: '#1565c0' }}>
          {t('intro', lang)}
        </div>
      )}

      {/* Crisis help always visible */}
      <div style={{ background: '#fff3e0', borderRadius: 8, padding: '0.6rem', marginBottom: 12, fontSize: '0.8rem', color: '#e65100' }}>
        {t('crisis_help', lang)}
      </div>

      {!result && questions && (
        <>
          <p style={{ fontWeight: 700, color: '#1565c0', marginBottom: 8 }}>{t('phq2_title', lang)}</p>
          {questions.phq2_questions.map((q, i) => (
            <ScoreSelector key={`phq2_${i}`} question={q} value={phq2[i]}
              onChange={(v) => { const s = [...phq2]; s[i] = v; setPhq2(s); }} lang={lang} />
          ))}

          <p style={{ fontWeight: 700, color: '#6a1b9a', marginBottom: 8, marginTop: 16 }}>{t('gad2_title', lang)}</p>
          {questions.gad2_questions.map((q, i) => (
            <ScoreSelector key={`gad2_${i}`} question={q} value={gad2[i]}
              onChange={(v) => { const s = [...gad2]; s[i] = v; setGad2(s); }} lang={lang} />
          ))}

          <button onClick={submit} disabled={!allAnswered || loading}
            style={{
              marginTop: 12, padding: '0.6rem 1.5rem', borderRadius: 8,
              background: allAnswered ? '#1565c0' : '#ccc',
              color: '#fff', border: 'none', cursor: allAnswered ? 'pointer' : 'not-allowed',
              fontWeight: 700, fontSize: '0.95rem',
            }}>
            {loading ? t('loading', lang) : t('submit', lang)}
          </button>
        </>
      )}

      {result && (
        <div>
          {/* PHQ-2 result */}
          <div style={{ background: urgencyBg(result.phq2.level), borderRadius: 8, padding: '0.8rem', marginBottom: 10 }}>
            <div style={{ fontWeight: 700, color: urgencyColor(result.phq2.level), marginBottom: 4 }}>
              {t('phq2_title', lang)} — Score: {result.phq2.score}/6
            </div>
            <p style={{ fontSize: '0.85rem', margin: 0 }}>{result.phq2.message}</p>
          </div>

          {/* GAD-2 result */}
          <div style={{ background: urgencyBg(result.gad2.level), borderRadius: 8, padding: '0.8rem', marginBottom: 10 }}>
            <div style={{ fontWeight: 700, color: urgencyColor(result.gad2.level), marginBottom: 4 }}>
              {t('gad2_title', lang)} — Score: {result.gad2.score}/6
            </div>
            <p style={{ fontSize: '0.85rem', margin: 0 }}>{result.gad2.message}</p>
          </div>

          {/* Cultural note */}
          <div style={{ background: '#f3e5f5', borderRadius: 8, padding: '0.7rem', marginBottom: 10, fontSize: '0.82rem', color: '#6a1b9a' }}>
             {result.cultural_note}
          </div>

          <button onClick={reset}
            style={{ padding: '0.4rem 1rem', borderRadius: 8, background: '#555', color: '#fff', border: 'none', cursor: 'pointer' }}>
            {t('restart', lang)}
          </button>
        </div>
      )}
    </div>
  );
}
