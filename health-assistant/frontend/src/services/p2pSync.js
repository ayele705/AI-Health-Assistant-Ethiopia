/**
 * p2pSync.js — WebRTC peer-to-peer data sync between two devices.
 * AES-256 encrypted. No data sent to external servers.
 */

import { dbGetAll, dbPut, STORES } from './offlineStore';

// ── Pairing code helpers ──────────────────────────────────────────────────────

export function generatePairingCode() {
  return Math.floor(100000 + Math.random() * 900000).toString();
}

// ── P2P Sync session ──────────────────────────────────────────────────────────

export class P2PSyncSession {
  constructor(onStatus) {
    this.onStatus    = onStatus || (() => {});
    this.pc          = null;
    this.dc          = null;
    this.pairingCode = null;
    this.retries     = 0;
    this.MAX_RETRIES = 3;
  }

  /** Initiator: create offer and display pairing code. */
  async initiate() {
    this.pairingCode = generatePairingCode();
    this.pc = new RTCPeerConnection({ iceServers: [] }); // LAN only — no STUN needed
    this.dc = this.pc.createDataChannel('ha-sync', { ordered: true });

    this._setupDataChannel(this.dc);

    const offer = await this.pc.createOffer();
    await this.pc.setLocalDescription(offer);

    this.onStatus({ type: 'PAIRING_CODE', code: this.pairingCode });
    return { offer: this.pc.localDescription, pairingCode: this.pairingCode };
  }

  /** Receiver: accept offer with pairing code verification. */
  async accept(offer, pairingCode) {
    if (pairingCode !== this.pairingCode) {
      this.retries++;
      if (this.retries >= this.MAX_RETRIES) {
        this.onStatus({ type: 'ERROR', message: 'Too many failed pairing attempts.' });
        return false;
      }
      this.onStatus({ type: 'PAIRING_FAILED', retriesLeft: this.MAX_RETRIES - this.retries });
      return false;
    }

    this.pc = new RTCPeerConnection({ iceServers: [] });
    this.pc.ondatachannel = (event) => {
      this.dc = event.channel;
      this._setupDataChannel(this.dc);
    };

    await this.pc.setRemoteDescription(offer);
    const answer = await this.pc.createAnswer();
    await this.pc.setLocalDescription(answer);

    this.onStatus({ type: 'CONNECTED' });
    return { answer: this.pc.localDescription };
  }

  /** Send pending records, KB updates, and language packs to peer. */
  async syncData() {
    if (!this.dc || this.dc.readyState !== 'open') {
      this.onStatus({ type: 'ERROR', message: 'Data channel not open.' });
      return;
    }

    this.onStatus({ type: 'SYNCING' });

    const pending  = await dbGetAll(STORES.PENDING_SYNC);
    const remedies = await dbGetAll(STORES.TRAD_REMEDIES);
    const packs    = await dbGetAll(STORES.LANGUAGE_PACKS);

    const payload = {
      pending_sync:  pending,
      trad_remedies: remedies,
      language_packs: packs.map((p) => ({ lang: p.lang, version: p.version })), // metadata only
    };

    const encrypted = await _encrypt(JSON.stringify(payload));
    this.dc.send(JSON.stringify({ type: 'SYNC_DATA', data: encrypted }));
  }

  _setupDataChannel(dc) {
    dc.onopen = () => this.onStatus({ type: 'CHANNEL_OPEN' });
    dc.onclose = () => this.onStatus({ type: 'CHANNEL_CLOSED' });

    dc.onmessage = async (event) => {
      try {
        const msg = JSON.parse(event.data);
        if (msg.type === 'SYNC_DATA') {
          const decrypted = await _decrypt(msg.data);
          const payload   = JSON.parse(decrypted);
          await _mergePayload(payload, this.onStatus);
        }
      } catch (e) {
        this.onStatus({ type: 'ERROR', message: `Decryption failed: ${e.message}` });
        this.dc?.close();
      }
    };
  }

  close() {
    this.dc?.close();
    this.pc?.close();
  }
}

// ── Encryption (AES-256-GCM with a session key) ───────────────────────────────

const SESSION_KEY_MATERIAL = 'ha-p2p-session-key-v1';

async function _getSessionKey() {
  const enc = new TextEncoder();
  const km  = await crypto.subtle.importKey('raw', enc.encode(SESSION_KEY_MATERIAL), 'PBKDF2', false, ['deriveKey']);
  const salt = enc.encode('ha-p2p-salt');
  return crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations: 10000, hash: 'SHA-256' },
    km,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt', 'decrypt']
  );
}

async function _encrypt(text) {
  const key = await _getSessionKey();
  const iv  = crypto.getRandomValues(new Uint8Array(12));
  const enc = new TextEncoder();
  const ct  = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, enc.encode(text));
  return JSON.stringify({ iv: Array.from(iv), ct: Array.from(new Uint8Array(ct)) });
}

async function _decrypt(json) {
  const { iv, ct } = JSON.parse(json);
  const key = await _getSessionKey();
  const pt  = await crypto.subtle.decrypt(
    { name: 'AES-GCM', iv: new Uint8Array(iv) },
    key,
    new Uint8Array(ct)
  );
  return new TextDecoder().decode(pt);
}

// ── Merge received payload ────────────────────────────────────────────────────

async function _mergePayload(payload, onStatus) {
  let transferred = 0, skipped = 0;

  for (const record of (payload.pending_sync || [])) {
    try {
      await dbPut(STORES.PENDING_SYNC, record);
      transferred++;
    } catch { skipped++; }
  }

  for (const remedy of (payload.trad_remedies || [])) {
    try {
      await dbPut(STORES.TRAD_REMEDIES, remedy);
      transferred++;
    } catch { skipped++; }
  }

  onStatus({ type: 'SYNC_COMPLETE', transferred, skipped });
}
