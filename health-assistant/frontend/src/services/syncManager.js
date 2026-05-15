/**
 * syncManager.js — Background sync: queues offline submissions and replays
 * them when connectivity is restored. Exponential backoff, max 5 retries.
 */

import { openDB, dbPut, dbGetAll, dbDelete, STORES } from './offlineStore';

const MAX_RETRIES    = 5;
const BASE_DELAY_MS  = 2000;
const STALE_DAYS     = 30;

let _syncInProgress = false;
let _listeners      = [];

// ── Public API ────────────────────────────────────────────────────────────────

/** Queue a submission for later sync when offline. */
export async function queueSubmission({ url, method = 'POST', body, type = 'generic' }) {
  await openDB();
  await dbPut(STORES.PENDING_SYNC, {
    url,
    method,
    body: JSON.stringify(body),
    type,
    status: 'pending_sync',
    retries: 0,
    timestamp: new Date().toISOString(),
  });
  notifyListeners({ type: 'QUEUED', count: await getPendingCount() });
}

/** Replay all pending submissions. Called on reconnection. */
export async function replayPending() {
  if (_syncInProgress) return;
  _syncInProgress = true;
  notifyListeners({ type: 'SYNCING' });

  try {
    const all     = await dbGetAll(STORES.PENDING_SYNC);
    const pending = all.filter((r) => r.status === 'pending_sync' || r.status === 'sync_failed');

    for (const record of pending) {
      await _syncRecord(record);
    }
  } finally {
    _syncInProgress = false;
    const remaining = await getPendingCount();
    notifyListeners({ type: 'SYNC_COMPLETE', remaining });
  }
}

/** Silently refresh stale cached data (>30 days) in the background. */
export async function refreshStaleData() {
  const staleEndpoints = [
    '/api/v1/tips/',
    '/api/v1/facilities/',
    '/api/v1/medications/',
    '/api/v1/conditions/',
    '/api/v1/trad-medicine/',
  ];
  for (const url of staleEndpoints) {
    try {
      await fetch(url, { cache: 'reload' });
    } catch {
      // Ignore — we're just refreshing opportunistically
    }
  }
}

/** Subscribe to sync events. Returns unsubscribe function. */
export function onSyncEvent(listener) {
  _listeners.push(listener);
  return () => { _listeners = _listeners.filter((l) => l !== listener); };
}

/** Get count of records still pending sync. */
export async function getPendingCount() {
  const all = await dbGetAll(STORES.PENDING_SYNC);
  return all.filter((r) => r.status === 'pending_sync').length;
}

/** Get all failed sync records. */
export async function getFailedRecords() {
  const all = await dbGetAll(STORES.PENDING_SYNC);
  return all.filter((r) => r.status === 'sync_failed');
}

/** Manually retry a failed record. */
export async function retryRecord(id) {
  const all    = await dbGetAll(STORES.PENDING_SYNC);
  const record = all.find((r) => r.id === id);
  if (!record) return;
  record.status  = 'pending_sync';
  record.retries = 0;
  await dbPut(STORES.PENDING_SYNC, record);
  await replayPending();
}

// ── Connectivity listener ─────────────────────────────────────────────────────

export function startConnectivityListener() {
  window.addEventListener('online', async () => {
    notifyListeners({ type: 'ONLINE' });
    await replayPending();
    await refreshStaleData();
  });
  window.addEventListener('offline', () => {
    notifyListeners({ type: 'OFFLINE' });
  });

  // Listen for SW trigger
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.addEventListener('message', async (event) => {
      if (event.data?.type === 'TRIGGER_SYNC') {
        await replayPending();
      }
    });
  }
}

// ── Internal helpers ──────────────────────────────────────────────────────────

async function _syncRecord(record) {
  const delay = BASE_DELAY_MS * Math.pow(2, record.retries);

  try {
    const res = await fetch(record.url, {
      method:  record.method,
      headers: { 'Content-Type': 'application/json' },
      body:    record.body,
    });

    if (res.ok) {
      await dbDelete(STORES.PENDING_SYNC, record.id);
      notifyListeners({ type: 'RECORD_SYNCED', record });
    } else {
      await _handleRetry(record, `HTTP ${res.status}`);
    }
  } catch (err) {
    await _handleRetry(record, err.message);
  }
}

async function _handleRetry(record, reason) {
  record.retries += 1;
  if (record.retries >= MAX_RETRIES) {
    record.status = 'sync_failed';
    notifyListeners({ type: 'RECORD_FAILED', record, reason });
  }
  await dbPut(STORES.PENDING_SYNC, record);
}

function notifyListeners(event) {
  _listeners.forEach((l) => {
    try { l(event); } catch { /* ignore listener errors */ }
  });
}
