/**
 * offlineStore.js — IndexedDB schema and AES-256 encrypted storage
 * for all rural community enhancement data stores.
 */

const DB_NAME    = 'health-assistant-db';
const DB_VERSION = 3;

// Store names
export const STORES = {
  PENDING_SYNC:       'pending_sync',
  PATIENT_RECORDS:    'patient_records',
  PATIENT_LOGS:       'patient_logs',      // chat session symptom logs
  LANGUAGE_PACKS:     'language_packs',
  AUDIO_CLIPS:        'audio_clips',
  CALENDAR_EVENTS:    'calendar_events',
  REFERRALS:          'referrals',
  EMERGENCY_CONTACTS: 'emergency_contacts',
  TRAD_REMEDIES:      'trad_remedies',
  FORM_STATE:         'form_state',
};

let _db = null;

export async function openDB() {
  if (_db) return _db;
  return new Promise((resolve, reject) => {
    const req = indexedDB.open(DB_NAME, DB_VERSION);

    req.onupgradeneeded = (event) => {
      const db = event.target.result;

      // pending_sync — offline submission queue
      if (!db.objectStoreNames.contains(STORES.PENDING_SYNC)) {
        const ps = db.createObjectStore(STORES.PENDING_SYNC, { keyPath: 'id', autoIncrement: true });
        ps.createIndex('status', 'status');
        ps.createIndex('timestamp', 'timestamp');
      }

      // patient_records — encrypted patient data
      if (!db.objectStoreNames.contains(STORES.PATIENT_RECORDS)) {
        const pr = db.createObjectStore(STORES.PATIENT_RECORDS, { keyPath: 'id' });
        pr.createIndex('type', 'type');
        pr.createIndex('kebele', 'kebele');
        pr.createIndex('created_at', 'created_at');
      }

      // language_packs
      if (!db.objectStoreNames.contains(STORES.LANGUAGE_PACKS)) {
        db.createObjectStore(STORES.LANGUAGE_PACKS, { keyPath: 'lang' });
      }

      // audio_clips
      if (!db.objectStoreNames.contains(STORES.AUDIO_CLIPS)) {
        const ac = db.createObjectStore(STORES.AUDIO_CLIPS, { keyPath: 'id' });
        ac.createIndex('lang', 'lang');
        ac.createIndex('category', 'category');
      }

      // calendar_events
      if (!db.objectStoreNames.contains(STORES.CALENDAR_EVENTS)) {
        const ce = db.createObjectStore(STORES.CALENDAR_EVENTS, { keyPath: 'id' });
        ce.createIndex('kebele', 'kebele');
        ce.createIndex('event_date', 'event_date');
      }

      // referrals
      if (!db.objectStoreNames.contains(STORES.REFERRALS)) {
        const ref = db.createObjectStore(STORES.REFERRALS, { keyPath: 'referral_id' });
        ref.createIndex('chw_identifier', 'chw_identifier');
        ref.createIndex('status', 'status');
        ref.createIndex('expected_visit_date', 'expected_visit_date');
      }

      // emergency_contacts
      if (!db.objectStoreNames.contains(STORES.EMERGENCY_CONTACTS)) {
        const ec = db.createObjectStore(STORES.EMERGENCY_CONTACTS, { keyPath: 'id', autoIncrement: true });
        ec.createIndex('user_identifier', 'user_identifier');
      }

      // trad_remedies
      if (!db.objectStoreNames.contains(STORES.TRAD_REMEDIES)) {
        const tr = db.createObjectStore(STORES.TRAD_REMEDIES, { keyPath: 'remedy_id' });
        tr.createIndex('evidence_level', 'evidence_level');
      }

      // form_state — auto-save for in-progress forms
      if (!db.objectStoreNames.contains(STORES.FORM_STATE)) {
        db.createObjectStore(STORES.FORM_STATE, { keyPath: 'form_id' });
      }

      // patient_logs — chat session symptom logs (v3)
      if (!db.objectStoreNames.contains(STORES.PATIENT_LOGS)) {
        const pl = db.createObjectStore(STORES.PATIENT_LOGS, { keyPath: 'log_id' });
        pl.createIndex('session_id',   'session_id');
        pl.createIndex('lang',         'lang');
        pl.createIndex('has_red_flags','has_red_flags');
        pl.createIndex('timestamp',    'timestamp');
        pl.createIndex('synced',       'synced');
      }
    };

    req.onsuccess = (e) => { _db = e.target.result; resolve(_db); };
    req.onerror   = (e) => reject(e.target.error);
  });
}

// ── Generic CRUD helpers ──────────────────────────────────────────────────────

export async function dbPut(storeName, record) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx  = db.transaction(storeName, 'readwrite');
    const req = tx.objectStore(storeName).put(record);
    req.onsuccess = () => resolve(req.result);
    req.onerror   = () => reject(req.error);
  });
}

export async function dbGet(storeName, key) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx  = db.transaction(storeName, 'readonly');
    const req = tx.objectStore(storeName).get(key);
    req.onsuccess = () => resolve(req.result);
    req.onerror   = () => reject(req.error);
  });
}

export async function dbGetAll(storeName) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx  = db.transaction(storeName, 'readonly');
    const req = tx.objectStore(storeName).getAll();
    req.onsuccess = () => resolve(req.result);
    req.onerror   = () => reject(req.error);
  });
}

export async function dbGetByIndex(storeName, indexName, value) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx    = db.transaction(storeName, 'readonly');
    const index = tx.objectStore(storeName).index(indexName);
    const req   = index.getAll(value);
    req.onsuccess = () => resolve(req.result);
    req.onerror   = () => reject(req.error);
  });
}

export async function dbDelete(storeName, key) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx  = db.transaction(storeName, 'readwrite');
    const req = tx.objectStore(storeName).delete(key);
    req.onsuccess = () => resolve();
    req.onerror   = () => reject(req.error);
  });
}

// ── AES-256-GCM encryption helpers ───────────────────────────────────────────

async function deriveKey(pin) {
  const enc     = new TextEncoder();
  const keyMat  = await crypto.subtle.importKey('raw', enc.encode(pin), 'PBKDF2', false, ['deriveKey']);
  const salt    = enc.encode('health-assistant-salt-v1');
  return crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations: 100000, hash: 'SHA-256' },
    keyMat,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt', 'decrypt']
  );
}

export async function encryptRecord(data, pin) {
  if (!pin) return { encrypted: false, data };
  const key  = await deriveKey(pin);
  const iv   = crypto.getRandomValues(new Uint8Array(12));
  const enc  = new TextEncoder();
  const ct   = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, enc.encode(JSON.stringify(data)));
  return {
    encrypted: true,
    iv: Array.from(iv),
    ciphertext: Array.from(new Uint8Array(ct)),
  };
}

export async function decryptRecord(stored, pin) {
  if (!stored.encrypted) return stored.data;
  const key = await deriveKey(pin);
  const iv  = new Uint8Array(stored.iv);
  const ct  = new Uint8Array(stored.ciphertext);
  const pt  = await crypto.subtle.decrypt({ name: 'AES-GCM', iv }, key, ct);
  return JSON.parse(new TextDecoder().decode(pt));
}

// ── Patient record helpers (encrypted) ───────────────────────────────────────

export async function savePatientRecord(record, pin) {
  const payload = await encryptRecord(record, pin);
  await dbPut(STORES.PATIENT_RECORDS, {
    id: record.id || `${record.type}_${Date.now()}`,
    type: record.type,
    kebele: record.kebele || '',
    created_at: new Date().toISOString(),
    synced: false,
    payload,
  });
}

export async function loadPatientRecord(id, pin) {
  const row = await dbGet(STORES.PATIENT_RECORDS, id);
  if (!row) return null;
  return decryptRecord(row.payload, pin);
}

// ── Form auto-save ────────────────────────────────────────────────────────────

export async function saveFormState(formId, state) {
  await dbPut(STORES.FORM_STATE, {
    form_id: formId,
    state,
    saved_at: new Date().toISOString(),
  });
}

export async function loadFormState(formId) {
  const row = await dbGet(STORES.FORM_STATE, formId);
  return row ? row.state : null;
}

export async function clearFormState(formId) {
  await dbDelete(STORES.FORM_STATE, formId);
}

// ── Patient log helpers (chat session logs) ───────────────────────────────────

/**
 * Save a patient symptom log from a completed chat session.
 *
 * @param {object} log
 * @param {string} log.session_id      - Chat session ID from backend
 * @param {string} log.lang            - Language code used
 * @param {string[]} log.symptoms      - Symptoms reported by user
 * @param {string[]} log.red_flags     - Red-flag keywords detected (empty if none)
 * @param {object[]} log.conditions    - Assessed conditions from backend
 * @param {string}   log.urgency       - 'emergency' | 'visit_health_center' | 'self_care'
 * @param {string}   [log.kebele]      - Optional kebele/village identifier
 * @param {string}   [log.patient_ref] - Optional anonymous patient reference
 */
export async function savePatientLog(log) {
  const record = {
    log_id:        `log_${log.session_id || Date.now()}_${Math.random().toString(36).slice(2, 7)}`,
    session_id:    log.session_id || null,
    lang:          log.lang || 'en',
    symptoms:      log.symptoms || [],
    red_flags:     log.red_flags || [],
    has_red_flags: (log.red_flags?.length ?? 0) > 0 ? 1 : 0,  // indexed as int for IDB
    conditions:    log.conditions || [],
    urgency:       log.urgency || 'self_care',
    kebele:        log.kebele || '',
    patient_ref:   log.patient_ref || '',
    timestamp:     new Date().toISOString(),
    synced:        0,  // 0 = not synced, 1 = synced
  };
  await dbPut(STORES.PATIENT_LOGS, record);
  return record.log_id;
}

/**
 * Retrieve all patient logs, newest first.
 */
export async function getAllPatientLogs() {
  const logs = await dbGetAll(STORES.PATIENT_LOGS);
  return logs.sort((a, b) => (b.timestamp > a.timestamp ? 1 : -1));
}

/**
 * Retrieve only logs that contained red-flag symptoms.
 */
export async function getRedFlagLogs() {
  return dbGetByIndex(STORES.PATIENT_LOGS, 'has_red_flags', 1);
}

/**
 * Mark a log as synced to the backend.
 */
export async function markLogSynced(logId) {
  const db = await openDB();
  return new Promise((resolve, reject) => {
    const tx    = db.transaction(STORES.PATIENT_LOGS, 'readwrite');
    const store = tx.objectStore(STORES.PATIENT_LOGS);
    const req   = store.get(logId);
    req.onsuccess = () => {
      const record = req.result;
      if (record) {
        record.synced = 1;
        store.put(record);
      }
      resolve();
    };
    req.onerror = () => reject(req.error);
  });
}

/**
 * Delete logs older than `days` days to manage storage.
 */
export async function pruneOldLogs(days = 90) {
  const cutoff = new Date(Date.now() - days * 24 * 60 * 60 * 1000).toISOString();
  const all    = await dbGetAll(STORES.PATIENT_LOGS);
  const stale  = all.filter((l) => l.timestamp < cutoff && l.synced === 1);
  for (const log of stale) {
    await dbDelete(STORES.PATIENT_LOGS, log.log_id);
  }
  return stale.length;
}
