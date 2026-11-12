// Komponen tampilan kecil yang dipakai berulang.
import { faktor, faktorPersekutuan } from './fpb.js';
import { kodeSiswa, POLA_KODE, setKodeSiswa } from './storage.js';

/** Mencegah teks dari server dianggap HTML. */
export function esc(teks) {
  return String(teks ?? '')
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

/** Kepala halaman: tombol kembali + judul + info kecil di kanan. */
export function kepala(judul, { kembali = '#/', kanan = '' } = {}) {
  return `
    <header class="kepala">
      <a class="tombol-kembali" href="${kembali}" aria-label="Kembali">←</a>
      <h1 tabindex="-1">${esc(judul)}</h1>
      <span class="kepala-kanan">${esc(kanan)}</span>
    </header>`;
}

/** Deretan angka (chip). Angka di `sorot` diberi warna penanda faktor persekutuan. */
export function chips(angka, sorot = []) {
  const set = new Set(sorot);
  return `<div class="chips">${angka
    .map((x) => `<span class="chip${set.has(x) ? ' sama' : ''}">${x}</span>`)
    .join('')}</div>`;
}

/** Daftar faktor beberapa bilangan dengan faktor persekutuan diwarnai (signaling). */
export function daftarFaktorHtml(bilangan, { warnai = true } = {}) {
  const sama = warnai ? faktorPersekutuan(...bilangan) : [];
  return bilangan
    .map((b) => `
      <div class="baris-faktor">
        <span class="label-faktor">Faktor ${b}</span>
        ${chips(faktor(b), sama)}
      </div>`)
    .join('');
}

/** Satu langkah pembahasan: judul, angka (opsional), dan alasan. */
export function langkahHtml(langkah, nomor, sorot = []) {
  const isi = Array.isArray(langkah.isi) && langkah.isi.length
    ? chips(langkah.isi, langkah.judul === 'FPB' ? langkah.isi : sorot)
    : '';
  return `
    <div class="langkah muncul">
      <div class="langkah-judul"><span class="nomor">${nomor}</span>${esc(langkah.judul)}</div>
      ${isi}
      <p class="alasan">${esc(langkah.alasan)}</p>
    </div>`;
}

/**
 * Tabel soal. opsi.ketuk = true -> sel bisa diketuk (tombol).
 * opsi.pilih / opsi.sorot = Set berisi "baris,kolom".
 */
export function tabelHtml(tabel, { ketuk = false, pilih = new Set(), sorot = new Set() } = {}) {
  if (!tabel) return '';
  const kepalaTabel = tabel.kolom.map((k) => `<th scope="col">${esc(k)}</th>`).join('');
  const isi = tabel.baris
    .map((baris, b) => `<tr>${baris
      .map((sel, k) => {
        const kunci = `${b},${k}`;
        const kelas = [pilih.has(kunci) ? 'dipilih' : '', sorot.has(kunci) ? 'disorot' : '']
          .join(' ').trim();
        if (ketuk) {
          return `<td class="${kelas}"><button type="button" class="sel" data-sel="${kunci}"
            aria-pressed="${pilih.has(kunci)}">${esc(sel)}</button></td>`;
        }
        return `<td class="${kelas}">${esc(sel)}</td>`;
      })
      .join('')}</tr>`)
    .join('');
  return `<div class="tabel-bungkus"><table class="tabel-soal">
    <thead><tr>${kepalaTabel}</tr></thead><tbody>${isi}</tbody></table></div>`;
}

export const memuat = (teks = 'Sebentar, ya…') =>
  `<div class="memuat" role="status"><span class="putar" aria-hidden="true"></span>${esc(teks)}</div>`;

export function galatHtml(err, { cobaLagi = true } = {}) {
  return `
    <div class="kotak-galat" role="alert">
      <p>${esc(err.message || err)}</p>
      ${cobaLagi ? '<button type="button" class="tombol tombol-kedua" data-aksi="coba-lagi">Coba lagi</button>' : ''}
    </div>`;
}

/** Form kecil untuk kode siswa (opsional, untuk uji coba penelitian). */
export function formKodeHtml() {
  return `
    <details class="kode-siswa">
      <summary>Kode siswa (boleh dikosongkan)${kodeSiswa() ? `: <b>${esc(kodeSiswa())}</b>` : ''}</summary>
      <form data-form="kode">
        <label for="input-kode">Isi kode dari gurumu, misalnya S01. Jangan isi nama.</label>
        <div class="baris-input">
          <input id="input-kode" name="kode" maxlength="20" autocomplete="off" value="${esc(kodeSiswa())}">
          <button class="tombol tombol-kedua" type="submit">Simpan</button>
        </div>
        <p class="pesan-kecil" data-pesan-kode></p>
      </form>
    </details>`;
}

export function pasangFormKode(root) {
  const form = root.querySelector('[data-form="kode"]');
  if (!form) return;
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const nilai = form.kode.value.trim();
    const pesan = form.querySelector('[data-pesan-kode]');
    if (nilai && !POLA_KODE.test(nilai)) {
      pesan.textContent = 'Hanya huruf dan angka, tanpa spasi.';
      return;
    }
    setKodeSiswa(nilai);
    pesan.textContent = nilai ? 'Tersimpan.' : 'Kode dikosongkan.';
  });
}

/** Mengacak urutan array (salinan). */
export function acak(arr) {
  const a = [...arr];
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [a[i], a[j]] = [a[j], a[i]];
  }
  return a;
}

/** Ubah "1, 2, 4" atau "1 2 4" menjadi [1, 2, 4]. null jika ada isian yang bukan bilangan bulat. */
export function bacaDaftarAngka(teks) {
  const bagian = teks.split(/[\s,;.]+/).filter(Boolean);
  if (!bagian.length || bagian.some((b) => !/^\d+$/.test(b))) return null;
  return bagian.map(Number);
}

export function gulirKe(el) {
  if (!el) return;
  const kurangiGerak = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  el.scrollIntoView({ behavior: kurangiGerak ? 'auto' : 'smooth', block: 'nearest' });
}
