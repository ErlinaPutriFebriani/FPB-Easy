// Penyimpanan lokal di HP (localStorage). Semua akses dibungkus try/catch
// karena localStorage bisa diblokir (mode privat, penyimpanan penuh).

const KUNCI = 'fpb-easy';
export const POLA_KODE = /^[A-Za-z0-9_-]{1,20}$/;

function baca() {
  try {
    return JSON.parse(localStorage.getItem(KUNCI)) || {};
  } catch {
    return {};
  }
}

function tulis(data) {
  try {
    localStorage.setItem(KUNCI, JSON.stringify(data));
  } catch {
    /* abaikan: aplikasi tetap jalan tanpa penyimpanan */
  }
}

function ubah(fn) {
  const data = baca();
  fn(data);
  tulis(data);
  return data;
}

function buatUUID() {
  if (window.crypto && typeof crypto.randomUUID === 'function') return crypto.randomUUID();
  // Cadangan untuk http (bukan https) di jaringan lokal.
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    return (c === 'x' ? r : (r & 0x3) | 0x8).toString(16);
  });
}

/** ID acak anonim untuk perangkat ini (tanpa nama/data pribadi). */
export function perangkatId() {
  let id = baca().perangkatId;
  if (!id) {
    id = buatUUID();
    ubah((d) => { d.perangkatId = id; });
  }
  return id;
}

export const kodeSiswa = () => baca().kodeSiswa || '';

export function setKodeSiswa(kode) {
  const bersih = (kode || '').trim().toUpperCase();
  if (bersih && !POLA_KODE.test(bersih)) return false;
  ubah((d) => { d.kodeSiswa = bersih; });
  return true;
}

// ----- progres latihan
export const daftarSelesai = () => baca().selesai || [];

export function tandaiSelesai(soalId) {
  ubah((d) => {
    d.selesai = d.selesai || [];
    if (!d.selesai.includes(soalId)) d.selesai.push(soalId);
  });
}

// ----- skor uji diri
export const skorTerbaik = () => baca().skorTerbaik || null;

export function simpanSkorUji(skor, total) {
  ubah((d) => {
    const lama = d.skorTerbaik;
    if (!lama || skor / total > lama.skor / lama.total) d.skorTerbaik = { skor, total };
  });
}

// ----- antrean jawaban yang belum terkirim ke server
export const antrean = () => baca().antrean || [];

export function tambahAntrean(baris) {
  ubah((d) => {
    d.antrean = d.antrean || [];
    d.antrean.push(baris);
    if (d.antrean.length > 300) d.antrean = d.antrean.slice(-300);
  });
}

export function buangAntrean(jumlah) {
  ubah((d) => { d.antrean = (d.antrean || []).slice(jumlah); });
}

// ----- banner pasang aplikasi
const TUJUH_HARI = 7 * 24 * 60 * 60 * 1000;
export const bannerDitunda = () => Date.now() - (baca().bannerDitunda || 0) < TUJUH_HARI;
export function tundaBanner() {
  ubah((d) => { d.bannerDitunda = Date.now(); });
}
