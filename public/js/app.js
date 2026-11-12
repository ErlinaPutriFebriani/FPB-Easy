// Titik masuk frontend: router hash + service worker + kirim antrean jawaban.
import './install.js';
import { kirimAntrean } from './api.js';
import * as beranda from './pages/beranda.js';
import * as materi from './pages/materi.js';
import * as contoh from './pages/contoh.js';
import * as latihan from './pages/latihan.js';
import * as kalkulator from './pages/kalkulator.js';
import * as ujiDiri from './pages/ujiDiri.js';
import * as pasang from './pages/pasang.js';

const RUTE = {
  '': beranda,
  materi,
  contoh,
  latihan,
  kalkulator,
  uji: ujiDiri,
  pasang,
};

const root = document.getElementById('app');
let bersihkan = null;

function jalankanRute() {
  const bagian = location.hash.replace(/^#\/?/, '').split('/').map(decodeURIComponent);
  const [nama = '', ...param] = bagian;
  const halaman = RUTE[nama] || beranda;

  if (typeof bersihkan === 'function') bersihkan();
  bersihkan = null;

  root.innerHTML = '';
  window.scrollTo(0, 0);
  bersihkan = halaman.tampil(root, param) || null;

  // Aksesibilitas: pindahkan fokus ke judul halaman baru.
  const judul = root.querySelector('h1');
  if (judul) {
    judul.setAttribute('tabindex', '-1');
    judul.focus({ preventScroll: true });
  }
}

window.addEventListener('hashchange', jalankanRute);
jalankanRute();

// Kirim jawaban yang tertunda saat aplikasi dibuka / internet tersambung lagi.
kirimAntrean();
window.addEventListener('online', kirimAntrean);

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js').catch(() => {
      /* tanpa service worker aplikasi tetap jalan, hanya tidak bisa offline */
    });
  });
}
