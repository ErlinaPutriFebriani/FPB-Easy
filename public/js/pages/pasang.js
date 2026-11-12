// Panduan memasang aplikasi TANPA Play Store / App Store.
import { bisaPasangLangsung, iPhone, pasang, sudahTerpasang } from '../install.js';
import { kepala } from '../ui.js';

const PANDUAN = {
  android: {
    nama: 'Android',
    langkah: [
      ['🌐', 'Buka aplikasi ini di <b>Google Chrome</b>.'],
      ['⋮', 'Ketuk tombol <b>titik tiga (⋮)</b> di pojok kanan atas.'],
      ['📲', 'Pilih <b>"Instal aplikasi"</b> atau <b>"Tambahkan ke layar utama"</b>, lalu <b>Instal</b>.'],
    ],
  },
  iphone: {
    nama: 'iPhone',
    langkah: [
      ['🧭', 'Buka aplikasi ini di <b>Safari</b>.'],
      ['⬆️', 'Ketuk tombol <b>Bagikan</b> (kotak dengan panah ke atas) di bagian bawah layar.'],
      ['➕', 'Pilih <b>"Tambah ke Layar Utama"</b>, lalu ketuk <b>Tambah</b>.'],
    ],
  },
};

export function tampil(root, [pilihan]) {
  const wadah = document.createElement('div');
  root.appendChild(wadah);
  const platform = PANDUAN[pilihan] ? pilihan : (iPhone() ? 'iphone' : 'android');
  const lain = platform === 'iphone' ? 'android' : 'iphone';
  let langkahKe = 0;

  function gambar() {
    if (sudahTerpasang()) {
      wadah.innerHTML = `
        ${kepala('Pasang Aplikasi')}
        <section class="kartu"><p class="angka-besar" aria-hidden="true">✅</p>
          <h2>FPB Easy sudah terpasang</h2>
          <p>Buka dari ikon <b>FPB Easy</b> di layar utama HP-mu.</p></section>`;
      return;
    }
    const p = PANDUAN[platform];
    const [ikon, teks] = p.langkah[langkahKe];
    const terakhir = langkahKe === p.langkah.length - 1;
    wadah.innerHTML = `
      ${kepala(`Pasang di ${p.nama}`, { kanan: `${langkahKe + 1} / ${p.langkah.length}` })}
      <p class="pengantar">Tidak perlu Play Store atau App Store. Gratis dan tanpa daftar akun.</p>
      ${platform === 'android' && bisaPasangLangsung() ? `
        <section class="kartu">
          <h2>Cara tercepat</h2>
          <button type="button" class="tombol penuh" data-aksi="pasang">📲 Pasang sekarang</button>
        </section>
        <p class="pengantar">Atau ikuti langkah berikut:</p>` : ''}
      <section class="kartu langkah-pasang muncul" aria-live="polite">
        <p class="angka-besar" aria-hidden="true">${ikon}</p>
        <p>${teks}</p>
      </section>
      <div class="baris-tombol bawah">
        <button type="button" class="tombol tombol-kedua" data-aksi="kembali" ${langkahKe === 0 ? 'disabled' : ''}>Kembali</button>
        ${terakhir
          ? '<a class="tombol" href="#/">Selesai</a>'
          : '<button type="button" class="tombol" data-aksi="lanjut">Lanjut ▸</button>'}
      </div>
      <p class="kaki"><a href="#/pasang/${lain}">Pakai ${PANDUAN[lain].nama}? Lihat panduannya</a></p>`;
  }

  wadah.addEventListener('click', async (e) => {
    const aksi = e.target.closest('[data-aksi]')?.dataset.aksi;
    if (aksi === 'lanjut') langkahKe++;
    else if (aksi === 'kembali') langkahKe--;
    else if (aksi === 'pasang') await pasang();
    else return;
    gambar();
  });

  gambar();
  document.addEventListener('status-pasang', gambar);
  return () => document.removeEventListener('status-pasang', gambar);
}
