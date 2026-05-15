import React, { useState, useEffect } from 'react';
import { fetchFacilities } from '../api';

const REGIONS = ['', 'Oromia', 'Amhara', 'SNNPR', 'Tigray', 'Somali', 'Dire Dawa'];
const FACILITY_TYPES = ['', 'health_post', 'health_center', 'primary_hospital', 'hospital', 'referral_hospital'];

const T = {
  en: {
    title: 'Health Facilities',
    referral_chain: ' Follow the referral chain: Health Post → Health Center → Primary Hospital → Referral Hospital',
    filter_region: 'Filter by Region:',
    filter_type: 'Filter by Type:',
    all: 'All',
    hew: 'HEW Available',
    no_facilities: 'No facilities found.',
    loading: 'Loading...',
    types: {
      health_post: 'Health Post',
      health_center: 'Health Center',
      primary_hospital: 'Primary Hospital',
      hospital: 'Hospital',
      referral_hospital: 'Referral Hospital',
    },
  },
  am: {
    title: 'የጤና ተቋማት',
    referral_chain: ' ጤና ኬላ → ጤና ጣቢያ → ዋና ሆስፒታል → ሪፈራል ሆስፒታል የሚለው ቅደም ተከተል ይከተሉ',
    filter_region: 'በክልል ፈልግ:',
    filter_type: 'በዓይነት ፈልግ:',
    all: 'ሁሉም',
    hew: 'HEW አለ',
    no_facilities: 'ተቋማት አልተገኙም።',
    loading: 'በመጫን ላይ...',
    types: {
      health_post: 'የጤና ኬላ',
      health_center: 'ጤና ጣቢያ',
      primary_hospital: 'ዋና ሆስፒታል',
      hospital: 'ሆስፒታል',
      referral_hospital: 'ሪፈራል ሆስፒታል',
    },
  },
  ti: {
    title: 'ናይ ጥዕና ትካላት',
    referral_chain: ' ናይ ሪፈራል ሰንሰለት ተኸተል: ናይ ጥዕና ኬላ → ናይ ጥዕና ጣቢያ → ቀዳማይ ሆስፒታል → ሪፈራል ሆስፒታል',
    filter_region: 'ብክልል ፈልጥ:',
    filter_type: 'ብዓይነት ፈልጥ:',
    all: 'ኩሎም',
    hew: 'HEW ኣሎ',
    no_facilities: 'ትካላት ኣይተረኽቡን።',
    loading: 'ይጽዓን ኣሎ...',
    types: {
      health_post: 'ናይ ጥዕና ኬላ',
      health_center: 'ናይ ጥዕና ጣቢያ',
      primary_hospital: 'ቀዳማይ ሆስፒታል',
      hospital: 'ሆስፒታል',
      referral_hospital: 'ሪፈራል ሆስፒታል',
    },
  },
  om: {
    title: 'Dhaabbilee Fayyaa',
    referral_chain: ' Hanga dhaabbata fayyaa: Buufata Fayyaa → Giddugala Fayyaa → Hospitaala Duraa → Hospitaala Wabii',
    filter_region: 'Naannoon Barbaadi:',
    filter_type: 'Gosa Barbaadi:',
    all: 'Hunda',
    hew: 'HEW Jira',
    no_facilities: 'Dhaabbilee hin argamne.',
    loading: 'Fe\'amaa jira...',
    types: {
      health_post: 'Buufata Fayyaa',
      health_center: 'Giddugala Fayyaa',
      primary_hospital: 'Hospitaala Duraa',
      hospital: 'Hospitaala',
      referral_hospital: 'Hospitaala Wabii',
    },
  },
  sid: {
    title: 'Dhaabbilee Fayyaa',
    referral_chain: ' Hanga dhaabbata fayyaa: Buufata → Giddugala → Hospitaala',
    filter_region: 'Naannoon Barbaadi:',
    filter_type: 'Gosa Barbaadi:',
    all: 'Hunda',
    hew: 'HEW Jira',
    no_facilities: 'Dhaabbilee hin argamne.',
    loading: 'Fe\'amaa jira...',
    types: {
      health_post: 'Buufata Fayyaa',
      health_center: 'Giddugala Fayyaa',
      primary_hospital: 'Hospitaala Duraa',
      hospital: 'Hospitaala',
      referral_hospital: 'Hospitaala Wabii',
    },
  },
};

// distance_note fallback: ti -> am -> en
function getDistanceNote(facility, lang) {
  return facility[`distance_note_${lang}`]
    || facility.distance_note_am
    || facility.distance_note_en
    || '';
}

export default function Facilities({ lang }) {
  const [facilities, setFacilities] = useState([]);
  const [region, setRegion] = useState('');
  const [facilityType, setFacilityType] = useState('');
  const [loading, setLoading] = useState(true);
  const t = T[lang] || T['en'];

  useEffect(() => {
    setLoading(true);
    fetchFacilities(region)
      .then(d => {
        let list = d.facilities || [];
        if (facilityType) list = list.filter(f => f.facility_type === facilityType);
        setFacilities(list);
      })
      .finally(() => setLoading(false));
  }, [region, facilityType]);

  const typeLabel = (type) => t.types[type] || type;

  return (
    <div>
      <p className="section-title">{t.title}</p>

      <p style={{ fontSize: '0.8rem', color: '#555', marginBottom: 8 }}>{t.referral_chain}</p>

      <p style={{ fontSize: '0.8rem', marginBottom: 4, fontWeight: 600 }}>{t.filter_region}</p>
      <div className="filter-row" role="group" aria-label={t.filter_region}>
        {REGIONS.map(r => (
          <button key={r || 'all'} className={`filter-btn ${region === r ? 'active' : ''}`} onClick={() => setRegion(r)}>
            {r || t.all}
          </button>
        ))}
      </div>

      <p style={{ fontSize: '0.8rem', marginBottom: 4, fontWeight: 600 }}>{t.filter_type}</p>
      <div className="filter-row" role="group" aria-label={t.filter_type}>
        {FACILITY_TYPES.map(type => (
          <button key={type || 'all'} className={`filter-btn ${facilityType === type ? 'active' : ''}`} onClick={() => setFacilityType(type)}>
            {type ? typeLabel(type) : t.all}
          </button>
        ))}
      </div>

      {loading && <p className="loading">{t.loading}</p>}

      {!loading && facilities.map(f => (
        <div key={f.id} className="facility-card">
          <p className="facility-name">{f.name}</p>
          <span className="facility-type">{typeLabel(f.facility_type)}</span>
          {f.hew_available && (
            <span className="facility-type" style={{ background: '#e8f5e9', color: '#2e7d32', marginLeft: 6 }}>
              ‍️ {t.hew}
            </span>
          )}
          <p className="facility-info"> {f.region}{f.woreda ? `, ${f.woreda}` : ''}</p>
          {f.distance_note_en && (
            <p className="facility-info" style={{ fontStyle: 'italic', color: '#555' }}>
              ℹ️ {getDistanceNote(f, lang)}
            </p>
          )}
          {f.services && (
            <p className="facility-info"> {f.services.join(' · ')}</p>
          )}
          {f.phone && (
            <p className="facility-info">
               <a href={`tel:${f.phone}`} className="facility-phone">{f.phone}</a>
            </p>
          )}
        </div>
      ))}

      {!loading && facilities.length === 0 && (
        <p className="loading">{t.no_facilities}</p>
      )}
    </div>
  );
}
