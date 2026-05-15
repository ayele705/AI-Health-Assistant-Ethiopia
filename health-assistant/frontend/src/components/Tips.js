import React, { useState, useEffect } from 'react';
import { fetchTips } from '../api';

const CATEGORIES = ['all', 'hygiene', 'disease_prevention', 'maternal_health', 'child_health', 'nutrition'];

const T = {
  en: {
    title: 'Health Education Tips',
    none: 'No tips found.',
    loading: 'Loading...',
    cats: { all: 'All', hygiene: 'Hygiene', disease_prevention: 'Prevention', maternal_health: 'Maternal', child_health: 'Child Health', nutrition: 'Nutrition' },
  },
  am: {
    title: 'የጤና ምክሮች',
    none: 'ምክሮች አልተገኙም።',
    loading: 'በመጫን ላይ...',
    cats: { all: 'ሁሉም', hygiene: 'ንጽህና', disease_prevention: 'ህመም መከላከል', maternal_health: 'የእናቶች ጤና', child_health: 'የህጻናት ጤና', nutrition: 'አመጋገብ' },
  },
  ti: {
    title: 'ምኽሪ ጥዕና',
    none: 'ምኽሪ ኣይተረኽበን።',
    loading: 'ይጽዓን ኣሎ...',
    cats: { all: 'ኩሎም', hygiene: 'ጽሬት', disease_prevention: 'ምክልኻል ሕማም', maternal_health: 'ጥዕና ኣደ', child_health: 'ጥዕና ቆልዓ', nutrition: 'ምግቢ' },
  },
  om: {
    title: 'Gorsa Fayyaa',
    none: 'Gorsi hin argamne.',
    loading: "Fe'amaa jira...",
    cats: { all: 'Hunda', hygiene: 'Qulqullina', disease_prevention: 'Ittisa Dhukkubaa', maternal_health: 'Fayyaa Haadha', child_health: "Fayyaa Daa'imaa", nutrition: 'Nyaata' },
  },
  sid: {
    title: 'Gorsa Fayyaa',
    none: 'Gorsi hin argamne.',
    loading: "Fe'amaa jira...",
    cats: { all: 'Hunda', hygiene: 'Qulqullina', disease_prevention: 'Ittisa Dhukkubaa', maternal_health: 'Fayyaa Haadha', child_health: "Fayyaa Daa'imaa", nutrition: 'Nyaata' },
  },
  so: {
    title: 'Talooyinka Caafimaadka',
    none: 'Talo lama helin.',
    loading: 'Waa la raraya...',
    cats: { all: 'Dhammaan', hygiene: 'Nadiifnimada', disease_prevention: 'Kahorinta Cudurka', maternal_health: 'Caafimaadka Hooyadda', child_health: 'Caafimaadka Carruurta', nutrition: 'Nafaqada' },
  },
  aa: {
    title: 'Talooyinka Caafimaadka',
    none: 'Talo lama helin.',
    loading: 'Waa la raraya...',
    cats: { all: 'Dhammaan', hygiene: 'Nadiifnimada', disease_prevention: 'Kahorinta Cudurka', maternal_health: 'Caafimaadka Hooyadda', child_health: 'Caafimaadka Carruurta', nutrition: 'Nafaqada' },
  },
  wal: {
    title: 'Gorsa Fayyaa',
    none: 'Gorsi hin argamne.',
    loading: "Fe'amaa jira...",
    cats: { all: 'Hunda', hygiene: 'Qulqullina', disease_prevention: 'Ittisa Dhukkubaa', maternal_health: 'Fayyaa Haadha', child_health: "Fayyaa Daa'imaa", nutrition: 'Nyaata' },
  },
  had: {
    title: 'Gorsa Fayyaa',
    none: 'Gorsi hin argamne.',
    loading: "Fe'amaa jira...",
    cats: { all: 'Hunda', hygiene: 'Qulqullina', disease_prevention: 'Ittisa Dhukkubaa', maternal_health: 'Fayyaa Haadha', child_health: "Fayyaa Daa'imaa", nutrition: 'Nyaata' },
  },
};

export default function Tips({ lang }) {
  const [tips, setTips] = useState([]);
  const [category, setCategory] = useState('all');
  const [loading, setLoading] = useState(true);
  const t = T[lang] || T['en'];

  useEffect(() => {
    setLoading(true);
    fetchTips(lang, category === 'all' ? '' : category)
      .then(d => setTips(d.tips || []))
      .finally(() => setLoading(false));
  }, [lang, category]);

  const catLabel = (c) => t.cats[c] || c;

  return (
    <div>
      <p className="section-title">{t.title}</p>
      <div className="filter-row" role="group" aria-label={t.title}>
        {CATEGORIES.map(c => (
          <button key={c} className={`filter-btn ${category === c ? 'active' : ''}`} onClick={() => setCategory(c)}>
            {catLabel(c)}
          </button>
        ))}
      </div>
      {loading && <p className="loading">{t.loading}</p>}
      {!loading && tips.map(tip => (
        <div key={tip.id} className="tip-card">
          <span className="category-badge">{catLabel(tip.category)}</span>
          <p className="tip-title">{tip.title}</p>
          <p className="tip-content">{tip.content}</p>
        </div>
      ))}
      {!loading && tips.length === 0 && <p className="loading">{t.none}</p>}
    </div>
  );
}
