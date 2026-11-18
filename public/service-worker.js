// Service worker FPB Easy: membuat aplikasi bisa di-install dan dibuka offline.
// Naikkan VERSI setiap kali daftar FILE_STATIS berubah.
const VERSI = 'fpb-easy-v2';

const FILE_STATIS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/css/style.css',
  '/js/app.js',
  '/js/api.js',
  '/js/fpb.js',
  '/js/install.js',
  '/js/storage.js',
  '/js/ui.js',
  '/js/pages/beranda.js',
  '/js/pages/materi.js',
  '/js/pages/contoh.js',
  '/js/pages/latihan.js',
  '/js/pages/kalkulator.js',
  '/js/pages/ujiDiri.js',
  '/js/pages/pasang.js',
  '/icons/icon-192.png',
  '/icons/icon-512.png',
  '/icons/apple-touch-icon.png',
];

// Respons API yang boleh disimpan untuk dipakai saat offline.
const API_BOLEH_CACHE = ['/api/materi', '/api/contoh', '/api/soal', '/api/fpb'];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(VERSI).then((cache) => cache.addAll(FILE_STATIS)));
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys()
      .then((kunci) => Promise.all(kunci.filter((k) => k !== VERSI).map((k) => caches.delete(k))))
      .then(() => self.clients.claim()),
  );
});

/** Network first: coba internet dulu, kalau gagal pakai salinan terakhir. */
async function jaringanDulu(request) {
  const cache = await caches.open(VERSI);
  try {
    const res = await fetch(request);
    if (res.ok) cache.put(request, res.clone());
    return res;
  } catch (err) {
    const simpanan = await cache.match(request);
    if (simpanan) return simpanan;
    throw err;
  }
}

/** Stale-while-revalidate: tampilkan salinan cepat, perbarui diam-diam di belakang. */
async function salinanDulu(request) {
  const cache = await caches.open(VERSI);
  const simpanan = await cache.match(request, { ignoreSearch: true });
  const ambilBaru = fetch(request)
    .then((res) => {
      if (res.ok || res.type === 'opaque') cache.put(request, res.clone());
      return res;
    })
    .catch(() => null);
  if (simpanan) return simpanan;
  const baru = await ambilBaru;
  if (baru) return baru;
  if (request.mode === 'navigate') return cache.match('/index.html');
  return Response.error();
}

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return; // POST (periksa, hasil) selalu langsung ke server

  const url = new URL(request.url);
  const asalSama = url.origin === self.location.origin;

  if (asalSama && url.pathname.startsWith('/api/')) {
    if (API_BOLEH_CACHE.includes(url.pathname)) event.respondWith(jaringanDulu(request));
    return; // API lain (uji, petunjuk, pembahasan) tidak di-cache
  }

  if (request.mode === 'navigate') {
    event.respondWith(fetch(request).catch(() => caches.match('/index.html')));
    return;
  }

  const fontGoogle = url.hostname === 'fonts.googleapis.com' || url.hostname === 'fonts.gstatic.com';
  if (asalSama || fontGoogle) event.respondWith(salinanDulu(request));
});
