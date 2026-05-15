const BASE = '/api/v1';

async function safeJson(res) {
  const text = await res.text();
  try {
    return JSON.parse(text);
  } catch {
    console.error('Non-JSON response:', res.status, text.slice(0, 200));
    return {};
  }
}

export async function startChat(language = 'en') {
  const res = await fetch(`${BASE}/chat/start/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ language }),
  });
  return safeJson(res);
}

export async function sendMessage(sessionId, message, language = 'en') {
  const res = await fetch(`${BASE}/chat/${sessionId}/message/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, language }),
  });
  return safeJson(res);
}

export async function fetchTips(language = 'en', category = '') {
  const params = new URLSearchParams({ language });
  if (category) params.append('category', category);
  const res = await fetch(`${BASE}/tips/?${params}`);
  return safeJson(res);
}

export async function fetchFacilities(region = '') {
  const params = region ? new URLSearchParams({ region }) : '';
  const res = await fetch(`${BASE}/facilities/${params ? '?' + params : ''}`);
  return safeJson(res);
}

export async function bookAppointment(data) {
  const res = await fetch(`${BASE}/appointments/book/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return safeJson(res);
}

export async function fetchAppointments(facilityId = '') {
  const params = facilityId ? `?facility_id=${facilityId}` : '';
  const res = await fetch(`${BASE}/appointments/${params}`);
  return safeJson(res);
}

export async function fetchConsultations() {
  const res = await fetch(`${BASE}/consultations/`);
  return safeJson(res);
}

export async function fetchSafeResponse(language = 'en') {
  const res = await fetch(`${BASE}/safe-response/?language=${language}`);
  return safeJson(res);
}

export async function quickAssess(symptoms, age = 25, sex = 'unknown', language = 'en') {
  const res = await fetch(`${BASE}/assess/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ symptoms, age, sex, language }),
  });
  return safeJson(res);
}

// ── Phase 1: Medication Lookup ────────────────────────────────────────────────
export async function searchMedications(query, language = 'en') {
  const res = await fetch(`${BASE}/medications/?q=${encodeURIComponent(query)}&language=${language}`);
  return safeJson(res);
}

export async function fetchMedicationDetail(medId, language = 'en') {
  const res = await fetch(`${BASE}/medications/${medId}/?language=${language}`);
  return safeJson(res);
}

// ── Phase 1: Nearest Facility Finder ─────────────────────────────────────────
export async function fetchNearestFacilities(lat, lon, radiusKm = null, facilityType = '', limit = 50) {
  const params = new URLSearchParams({ lat, lon, limit });
  if (radiusKm) params.append('radius_km', radiusKm);
  if (facilityType) params.append('facility_type', facilityType);
  const res = await fetch(`${BASE}/facilities/nearest/?${params}`);
  return safeJson(res);
}

// ── Phase 1: Enhanced Differential Diagnosis ─────────────────────────────────
export async function differentialDiagnosis(symptoms, age = 25, sex = 'unknown', language = 'en') {
  const res = await fetch(`${BASE}/differential/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ symptoms, age, sex, language }),
  });
  return safeJson(res);
}

// ── Phase 1: Offline cache helpers ───────────────────────────────────────────
const CACHE_KEY = 'ha_offline_cache';
const CACHE_TTL = 24 * 60 * 60 * 1000; // 24 hours

export function saveOfflineCache(key, data) {
  try {
    const cache = JSON.parse(localStorage.getItem(CACHE_KEY) || '{}');
    cache[key] = { data, ts: Date.now() };
    localStorage.setItem(CACHE_KEY, JSON.stringify(cache));
  } catch (_) {}
}

export function loadOfflineCache(key) {
  try {
    const cache = JSON.parse(localStorage.getItem(CACHE_KEY) || '{}');
    const entry = cache[key];
    if (entry && Date.now() - entry.ts < CACHE_TTL) return entry.data;
  } catch (_) {}
  return null;
}

export async function fetchTipsCached(language = 'en', category = '') {
  const key = `tips_${language}_${category}`;
  if (!navigator.onLine) return loadOfflineCache(key) || { tips: [] };
  const data = await fetchTips(language, category);
  saveOfflineCache(key, data);
  return data;
}

export async function fetchFacilitiesCached(region = '') {
  const key = `facilities_${region}`;
  if (!navigator.onLine) return loadOfflineCache(key) || { facilities: [] };
  const data = await fetchFacilities(region);
  saveOfflineCache(key, data);
  return data;
}

// ── Phase 2: Growth Monitoring ────────────────────────────────────────────────
export async function assessGrowth(data) {
  const res = await fetch(`${BASE}/growth/assess/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
  return safeJson(res);
}
export async function registerChild(data) {
  const res = await fetch(`${BASE}/children/register/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
  return safeJson(res);
}
export async function addGrowthRecord(childId, data) {
  const res = await fetch(`${BASE}/children/${childId}/growth/add/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
  return safeJson(res);
}
export async function fetchGrowthHistory(childId) {
  const res = await fetch(`${BASE}/children/${childId}/growth/`);
  return safeJson(res);
}

// ── Phase 2: Vaccination Tracker ─────────────────────────────────────────────
export async function fetchVaccineSchedule(childId) {
  const res = await fetch(`${BASE}/children/${childId}/vaccines/`);
  return safeJson(res);
}
export async function addVaccineRecord(childId, data) {
  const res = await fetch(`${BASE}/children/${childId}/vaccines/add/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
  return safeJson(res);
}

// ── Phase 2: Pregnancy Follow-up ─────────────────────────────────────────────
export async function registerPregnancy(data) {
  const res = await fetch(`${BASE}/pregnancy/register/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
  return safeJson(res);
}
export async function fetchPregnancySchedule(recordId, language = 'en') {
  const res = await fetch(`${BASE}/pregnancy/${recordId}/schedule/?language=${language}`);
  return safeJson(res);
}
export async function addANCVisit(recordId, data) {
  const res = await fetch(`${BASE}/pregnancy/${recordId}/anc/add/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
  return safeJson(res);
}

// ── Phase 2: HEW Checklists ───────────────────────────────────────────────────
export async function fetchChecklistTypes() {
  const res = await fetch(`${BASE}/hew/checklists/`);
  return safeJson(res);
}
export async function fetchChecklist(visitType, language = 'en') {
  const res = await fetch(`${BASE}/hew/checklists/${visitType}/?language=${language}`);
  return safeJson(res);
}
export async function submitChecklist(data) {
  const res = await fetch(`${BASE}/hew/checklists/submit/`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
  return safeJson(res);
}

// ── Phase 3: SMS & Reminders ──────────────────────────────────────────────────
export async function reminderSubscribe(data) {
  const res = await fetch(`${BASE}/reminders/subscribe/`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(data) });
  return safeJson(res);
}
export async function reminderList(phone = '') {
  const params = phone ? `?phone=${encodeURIComponent(phone)}` : '';
  const res = await fetch(`${BASE}/reminders/${params}`);
  return safeJson(res);
}
export async function reminderUnsubscribe(id) {
  const res = await fetch(`${BASE}/reminders/${id}/unsubscribe/`, { method:'DELETE' });
  return safeJson(res);
}
export async function smsSend(phone, message, smsType = 'manual') {
  const res = await fetch(`${BASE}/sms/send/`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ phone, message, sms_type: smsType }) });
  return safeJson(res);
}
export async function fetchSmsLogs(params = {}) {
  const q = new URLSearchParams(params);
  const res = await fetch(`${BASE}/sms/logs/?${q}`);
  return safeJson(res);
}
export async function sendAppointmentReminder(apptId) {
  const res = await fetch(`${BASE}/appointments/${apptId}/remind/`, { method:'POST' });
  return safeJson(res);
}
export async function sendDangerAlert(phone, name, sign, language = 'en') {
  const res = await fetch(`${BASE}/sms/danger-alert/`, { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ phone, name, sign, language }) });
  return safeJson(res);
}

// ── Phase 4: Analytics, Outbreak & DHIS2 ─────────────────────────────────────
export async function fetchAnalytics(days = 30) {
  const res = await fetch(`${BASE}/analytics/?days=${days}`);
  return safeJson(res);
}
export async function fetchOutbreakAlerts(region = '') {
  const params = region ? `?region=${encodeURIComponent(region)}` : '';
  const res = await fetch(`${BASE}/outbreak/alerts/${params}`);
  return safeJson(res);
}
export async function fetchDiseaseTrend(conditionId, days = 30) {
  const res = await fetch(`${BASE}/outbreak/trend/${conditionId}/?days=${days}`);
  return safeJson(res);
}
export async function fetchDHIS2Export(period = '', orgUnit = '') {
  const params = new URLSearchParams();
  if (period) params.append('period', period);
  if (orgUnit) params.append('org_unit', orgUnit);
  const res = await fetch(`${BASE}/dhis2/export/?${params}`);
  return safeJson(res);
}
export async function pushToDHIS2(period = '', orgUnit = '') {
  const res = await fetch(`${BASE}/dhis2/push/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ period, org_unit: orgUnit }),
  });
  return safeJson(res);
}

// ── Google Places live facility search ───────────────────────────────────────
export async function fetchNearbyLive(lat, lon, radiusM = 50000, facilityType = '') {
  const params = new URLSearchParams({ lat, lon, radius_m: radiusM });
  if (facilityType) params.append('facility_type', facilityType);
  const res = await fetch(`${BASE}/facilities/live/?${params}`);
  return safeJson(res);
}
