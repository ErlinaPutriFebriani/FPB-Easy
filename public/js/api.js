// Pemanggil API Python (Flask). Semua halaman memakai modul ini.
import { antrean, buangAntrean, kodeSiswa, perangkatId } from './storage.js';

const BATAS_WAKTU_MS = 15000;

/** Dilempar jika tidak ada koneksi (berbeda dengan galat dari server). */
export class GagalJaringan extends Error {}

async function minta(path, opsi = {}) {
  const kendali = new AbortController();
  const timer = setTimeout(() => kendali.abort(), BATAS_WAKTU_MS);
  let res;
  try {
    res = await fetch(path, {
      ...opsi,
      signal: kendali.signal,
      headers: opsi.body ? { 'Content-Type': 'application/json' } : undefined,
    });
  } catch {
    throw new GagalJaringan('Tidak ada koneksi internet. Coba lagi saat sudah tersambung, ya.');
  } finally {
    clearTimeout(timer);
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    const err = new Error(data.pesan || 'Maaf, terjadi kesalahan. Coba lagi, ya.');
    err.status = res.status;
    throw err;
  }
  return data;
}

const kirim = (path, data) => minta(path, { method: 'POST', body: JSON.stringify(data) });
const q = encodeURIComponent;

export const api = {
  materi: () => minta('/api/materi'),
  contoh: () => minta('/api/contoh'),
  soal: (level) => minta(`/api/soal?level=${q(level)}`),
  fpb: (bilangan) => minta(`/api/fpb?bil=${bilangan.map(q).join(',')}`),
  periksa: (soalId, tahap, isian) => kirim('/api/periksa', { soal_id: soalId, tahap, isian }),
  petunjuk: (soalId, ke) => minta(`/api/petunjuk?soal_id=${q(soalId)}&ke=${q(ke)}`),
  pembahasan: (soalId) => minta(`/api/pembahasan?soal_id=${q(soalId)}`),
  uji: () => minta('/api/uji'),
  // Pembimbing AI (RMT). Kunci Gemini ada di server; browser hanya mengirim konteks langkah.
  bimbing: (isi) => kirim('/api/bimbing', {
    perangkat_id: perangkatId(),
    kode_siswa: kodeSiswa() || null,
    ...isi,
  }),
  refleksi: (soalId, alasan, jawabanFpb) => kirim('/api/refleksi', {
    perangkat_id: perangkatId(),
    kode_siswa: kodeSiswa() || null,
    soal_id: soalId,
    alasan,
    jawaban_fpb: jawabanFpb,
  }),
  nilaiUji: (jawaban) => kirim('/api/uji/nilai', {
    perangkat_id: perangkatId(),
    kode_siswa: kodeSiswa() || null,
    jawaban,
  }),
};

let sedangMengirim = false;

/** Mengirim jawaban latihan yang tertunda (misalnya dibuat saat offline). */
export async function kirimAntrean() {
  if (sedangMengirim) return;
  const daftar = antrean().slice(0, 100);
  if (daftar.length === 0) return;
  sedangMengirim = true;
  try {
    await kirim('/api/hasil', {
      perangkat_id: perangkatId(),
      kode_siswa: kodeSiswa() || null,
      jawaban: daftar,
    });
    buangAntrean(daftar.length);
  } catch (err) {
    // Jika server menolak datanya (bukan masalah jaringan), buang agar antrean tidak macet.
    if (!(err instanceof GagalJaringan) && err.status === 400) buangAntrean(daftar.length);
  } finally {
    sedangMengirim = false;
  }
}
