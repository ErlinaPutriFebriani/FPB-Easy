// Pemasangan aplikasi (PWA) tanpa Play Store / App Store.
// - Android & laptop (Chrome/Edge): browser memicu event `beforeinstallprompt`,
//   kita simpan lalu tampilkan saat siswa menekan tombol "Pasang".
// - iPhone (Safari): tidak ada event tersebut, jadi kita tampilkan panduan
//   "Bagikan -> Tambah ke Layar Utama" di halaman #/pasang.

let promptTertunda = null;

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  promptTertunda = e;
  document.dispatchEvent(new CustomEvent('status-pasang'));
});

window.addEventListener('appinstalled', () => {
  promptTertunda = null;
  document.dispatchEvent(new CustomEvent('status-pasang'));
});

export function sudahTerpasang() {
  return window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true;
}

export function iPhone() {
  const ua = navigator.userAgent;
  return /iphone|ipad|ipod/i.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
}

export const bisaPasangLangsung = () => promptTertunda !== null;

/** Menampilkan dialog pasang bawaan browser. true jika siswa menyetujui. */
export async function pasang() {
  if (!promptTertunda) return false;
  const e = promptTertunda;
  promptTertunda = null;
  e.prompt();
  const { outcome } = await e.userChoice;
  document.dispatchEvent(new CustomEvent('status-pasang'));
  return outcome === 'accepted';
}
