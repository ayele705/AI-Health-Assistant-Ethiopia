/* Service Worker — Rural Community Enhancements
 * Offline-first: caches core assets + API responses, queues offline submissions
 */

const CACHE_NAME = 'health-assistant-v1';
const API_CACHE  = 'ha-api-v1';
const OFFLINE_PAGE = '/offline.html';

// Core assets to pre-cache on install
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/offline.html',
  '/static/js/main.chunk.js',
  '/static/js/bundle.js',
  '/static/css/main.chunk.css',
  '/manifest.json',
];

// API paths to cache with network-first strategy
const API_CACHE_PATHS = [
  '/api/v1/tips/',
  '/api/v1/facilities/',
  '/api/v1/medications/',
  '/api/v1/conditions/',
  '/api/v1/hew/checklists/',
  '/api/v1/language-packs/',
  '/api/v1/calendar/',
  '/api/v1/referrals/',
  '/api/v1/trad-medicine/',
];

// ── Install: pre-cache core assets ───────────────────────────────────────────
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_URLS).catch((err) => {
        console.warn('[SW] Pre-cache partial failure:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// ── Activate: clean old caches ────────────────────────────────────────────────
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((k) => k !== CACHE_NAME && k !== API_CACHE)
          .map((k) => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

// ── Fetch: serve from cache when offline ─────────────────────────────────────
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET and cross-origin requests
  if (request.method !== 'GET' || url.origin !== self.location.origin) return;

  // API requests: network-first, fall back to cache
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirstApi(request));
    return;
  }

  // Static assets: cache-first
  event.respondWith(cacheFirst(request));
});

async function networkFirstApi(request) {
  const url = new URL(request.url);
  try {
    const response = await fetch(request.clone());
    if (response.ok) {
      // Cache if it's a cacheable API path
      const shouldCache = API_CACHE_PATHS.some((p) => url.pathname.startsWith(p));
      if (shouldCache) {
        const cache = await caches.open(API_CACHE);
        cache.put(request, response.clone());
      }
    }
    return response;
  } catch {
    // Offline — try cache
    const cached = await caches.match(request);
    if (cached) return cached;
    // Return empty JSON so the app doesn't crash
    return new Response(JSON.stringify({ offline: true, error: 'No cached data available' }), {
      headers: { 'Content-Type': 'application/json' },
      status: 503,
    });
  }
}

async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch {
    const offlinePage = await caches.match(OFFLINE_PAGE);
    return offlinePage || new Response('Offline', { status: 503 });
  }
}

// ── Background Sync: replay pending submissions ───────────────────────────────
self.addEventListener('sync', (event) => {
  if (event.tag === 'pending-sync') {
    event.waitUntil(replayPendingSync());
  }
});

async function replayPendingSync() {
  // Notify all clients to trigger sync via syncManager
  const clients = await self.clients.matchAll();
  clients.forEach((client) => client.postMessage({ type: 'TRIGGER_SYNC' }));
}

// ── Push notifications (future use) ──────────────────────────────────────────
self.addEventListener('push', (event) => {
  if (!event.data) return;
  const data = event.data.json();
  event.waitUntil(
    self.registration.showNotification(data.title || 'Health Assistant', {
      body: data.body || '',
      icon: '/logo192.png',
      badge: '/logo192.png',
      tag: data.tag || 'ha-notification',
    })
  );
});
