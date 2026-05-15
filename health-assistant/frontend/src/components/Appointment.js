import React, { useState, useEffect } from 'react';
import { fetchFacilities, bookAppointment } from '../api';

const T = {
  en: {
    title: 'Book an Appointment',
    name: 'Your Name',
    phone: 'Phone Number (optional)',
    facility: 'Select Health Facility',
    date: 'Preferred Date',
    reason: 'Reason for Visit',
    submit: 'Book Appointment',
    success: 'Appointment booked successfully!',
    error: 'Failed to book. Please try again.',
    required: 'Please fill all required fields.',
    new: 'New Appointment',
    select: '-- Select --',
    describe: 'Describe your symptoms...',
  },
  am: {
    title: 'ቀጠሮ ይያዙ',
    name: 'ስምዎ',
    phone: 'ስልክ ቁጥር (አማራጭ)',
    facility: 'ጤና ጣቢያ ይምረጡ',
    date: 'የሚፈልጉት ቀን',
    reason: 'የጉብኝት ምክንያት',
    submit: 'ቀጠሮ ያዝ',
    success: 'ቀጠሮ በተሳካ ሁኔታ ተይዟል!',
    error: 'አልተሳካም። እንደገና ይሞክሩ።',
    required: 'እባክዎ ሁሉንም አስፈላጊ መስኮች ይሙሉ።',
    new: 'አዲስ ቀጠሮ',
    select: '-- ይምረጡ --',
    describe: 'ምልክቶቹን ይግለጹ...',
  },
  ti: {
    title: 'ቆጸራ ሓዝ',
    name: 'ስምካ',
    phone: 'ቁጽሪ ተሌፎን (ምርጫ)',
    facility: 'ናይ ጥዕና ትካል ምረጽ',
    date: 'ዝደለኻዮ ዕለት',
    reason: 'ምኽንያት ምብጻሕ',
    submit: 'ቆጸራ ሓዝ',
    success: 'ቆጸራ ብዓወት ተሓዚዙ!',
    error: 'ኣይተሳኸዐን። ደጊምካ ፈትን።',
    required: 'በጃኻ ኩሎም ዘድልዩ ሜዳታት ምልእ።',
    new: 'ሓድሽ ቆጸራ',
    select: '-- ምረጽ --',
    describe: 'ምልክታትካ ግለጽ...',
  },
  om: {
    title: 'Beellama Qabadhu',
    name: 'Maqaa Kee',
    phone: 'Lakkoofsa Bilbilaa (dirqama miti)',
    facility: 'Dhaabbata Fayyaa Filadhu',
    date: 'Guyyaa Barbaaddu',
    reason: 'Sababaa Daawwannaa',
    submit: 'Beellama Qabadhu',
    success: 'Beellami milkaa\'inaan qabatame!',
    error: 'Hin milkoofne. Irra deebi\'i yaali.',
    required: 'Maaloo dirreewwan barbaachisoo hunda guuti.',
    new: 'Beellama Haaraa',
    select: '-- Filadhu --',
    describe: 'Mallattoolee kee ibsi...',
  },
  sid: {
    title: 'Beellama Qabadhu',
    name: 'Maqaa Kee',
    phone: 'Lakkoofsa Bilbilaa (dirqama miti)',
    facility: 'Dhaabbata Fayyaa Filadhu',
    date: 'Guyyaa Barbaaddu',
    reason: 'Sababaa Daawwannaa',
    submit: 'Beellama Qabadhu',
    success: 'Beellami milkaa\'inaan qabatame!',
    error: 'Hin milkoofne. Irra deebi\'i yaali.',
    required: 'Maaloo dirreewwan barbaachisoo hunda guuti.',
    new: 'Beellama Haaraa',
    select: '-- Filadhu --',
    describe: 'Mallattoolee kee ibsi...',
  },
  so: {
    title: 'Ballan Qabso',
    name: 'Magacaaga',
    phone: 'Lambarka Telefoonka (ikhtiyaari)',
    facility: 'Dooro Xarunta Caafimaadka',
    date: 'Taariikhda Aad Doortay',
    reason: 'Sababta Booqashada',
    submit: 'Ballan Qabso',
    success: 'Ballanta si guul leh ayaa loo qabsaday!',
    error: 'Kuma guulaysan. Dib u isku day.',
    required: 'Fadlan buuxi dhammaan goobaha loo baahan yahay.',
    new: 'Ballan Cusub',
    select: '-- Dooro --',
    describe: 'Sharax calaamadahaaga...',
  },
  aa: {
    title: 'Ballan Qabso',
    name: 'Magacaaga',
    phone: 'Lambarka Telefoonka (ikhtiyaari)',
    facility: 'Dooro Xarunta Caafimaadka',
    date: 'Taariikhda Aad Doortay',
    reason: 'Sababta Booqashada',
    submit: 'Ballan Qabso',
    success: 'Ballanta si guul leh ayaa loo qabsaday!',
    error: 'Kuma guulaysan. Dib u isku day.',
    required: 'Fadlan buuxi dhammaan goobaha loo baahan yahay.',
    new: 'Ballan Cusub',
    select: '-- Dooro --',
    describe: 'Sharax calaamadahaaga...',
  },
  wal: {
    title: 'Beellama Qabadhu',
    name: 'Maqaa Kee',
    phone: 'Lakkoofsa Bilbilaa (dirqama miti)',
    facility: 'Dhaabbata Fayyaa Filadhu',
    date: 'Guyyaa Barbaaddu',
    reason: 'Sababaa Daawwannaa',
    submit: 'Beellama Qabadhu',
    success: 'Beellami milkaa\'inaan qabatame!',
    error: 'Hin milkoofne. Irra deebi\'i yaali.',
    required: 'Maaloo dirreewwan barbaachisoo hunda guuti.',
    new: 'Beellama Haaraa',
    select: '-- Filadhu --',
    describe: 'Mallattoolee kee ibsi...',
  },
  had: {
    title: 'Beellama Qabadhu',
    name: 'Maqaa Kee',
    phone: 'Lakkoofsa Bilbilaa (dirqama miti)',
    facility: 'Dhaabbata Fayyaa Filadhu',
    date: 'Guyyaa Barbaaddu',
    reason: 'Sababaa Daawwannaa',
    submit: 'Beellama Qabadhu',
    success: 'Beellami milkaa\'inaan qabatame!',
    error: 'Hin milkoofne. Irra deebi\'i yaali.',
    required: 'Maaloo dirreewwan barbaachisoo hunda guuti.',
    new: 'Beellama Haaraa',
    select: '-- Filadhu --',
    describe: 'Mallattoolee kee ibsi...',
  },
};

export default function Appointment({ lang }) {
  const [facilities, setFacilities] = useState([]);
  const [form, setForm] = useState({
    patient_name: '',
    patient_phone: '',
    facility_id: '',
    facility_name: '',
    appointment_date: '',
    reason: '',
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const t = T[lang] || T['en'];

  useEffect(() => {
    fetchFacilities().then(d => setFacilities(d.facilities || []));
  }, []);

  const today = new Date().toISOString().split('T')[0];

  const handleFacilityChange = (e) => {
    const selected = facilities.find(f => f.id === e.target.value);
    setForm(prev => ({
      ...prev,
      facility_id: e.target.value,
      facility_name: selected ? selected.name : '',
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.patient_name || !form.facility_id || !form.appointment_date) {
      setError(t.required);
      return;
    }
    setError('');
    setLoading(true);
    try {
      const data = await bookAppointment({ ...form, language: lang });
      if (data.id) {
        setResult(data);
        setForm({ patient_name: '', patient_phone: '', facility_id: '', facility_name: '', appointment_date: '', reason: '' });
      } else {
        setError(t.error);
      }
    } catch {
      setError(t.error);
    }
    setLoading(false);
  };

  return (
    <div>
      <p className="section-title">{t.title}</p>

      {result && (
        <div className="assessment-card" style={{ background: '#e8f5e9', marginBottom: 16 }}>
          <p style={{ color: '#2e7d32', fontWeight: 600 }}> {t.success}</p>
          <p>{result.facility_name} — {result.appointment_date}</p>
          <button className="filter-btn active" onClick={() => setResult(null)} style={{ marginTop: 8 }}>
            {t.new}
          </button>
        </div>
      )}

      {!result && (
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
          <div>
            <label className="form-label">{t.name} *</label>
            <input
              className="chat-input"
              style={{ width: '100%' }}
              value={form.patient_name}
              onChange={e => setForm(p => ({ ...p, patient_name: e.target.value }))}
              placeholder={t.name}
            />
          </div>

          <div>
            <label className="form-label">{t.phone}</label>
            <input
              className="chat-input"
              style={{ width: '100%' }}
              value={form.patient_phone}
              onChange={e => setForm(p => ({ ...p, patient_phone: e.target.value }))}
              placeholder="+251..."
            />
          </div>

          <div>
            <label className="form-label">{t.facility} *</label>
            <select
              className="chat-input"
              style={{ width: '100%' }}
              value={form.facility_id}
              onChange={handleFacilityChange}
            >
              <option value="">{t.select}</option>
              {facilities.map(f => (
                <option key={f.id} value={f.id}>{f.name} ({f.region})</option>
              ))}
            </select>
          </div>

          <div>
            <label className="form-label">{t.date} *</label>
            <input
              type="date"
              className="chat-input"
              style={{ width: '100%' }}
              min={today}
              value={form.appointment_date}
              onChange={e => setForm(p => ({ ...p, appointment_date: e.target.value }))}
            />
          </div>

          <div>
            <label className="form-label">{t.reason}</label>
            <textarea
              className="chat-input"
              style={{ width: '100%', minHeight: 70, resize: 'vertical' }}
              value={form.reason}
              onChange={e => setForm(p => ({ ...p, reason: e.target.value }))}
              placeholder={t.describe}
            />
          </div>

          {error && <p style={{ color: '#c0392b', fontSize: '0.85rem' }}>{error}</p>}

          <button className="start-btn" type="submit" disabled={loading}>
            {loading ? '...' : t.submit}
          </button>
        </form>
      )}
    </div>
  );
}
