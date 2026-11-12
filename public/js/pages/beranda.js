// Beranda: 5 menu besar + banner "Pasang Aplikasi" (hanya bila belum terpasang).
import { bisaPasangLangsung, iPhone, pasang, sudahTerpasang } from '../install.js';
import { bannerDitunda, daftarSelesai, skorTerbaik, tundaBanner } from '../storage.js';

const TOTAL_LATIHAN = 9;

export function tampil(root) {
  const selesai = daftarSelesai().filter((id) => !id.startsWith('uji')).length;
  const skor = skorTerbaik();

  root.innerHTML = `
    <header class="judul-app">
      <h1>FPB Easy</h1>
      <p>Belajar FPB pelan-pelan, langkah demi langkah 🙂</p>
    </header>

    <div data-banner></div>

    <nav class="menu" aria-label="Menu utama">
      <a class="menu-item" href="#/materi"><span class="ikon" aria-hidden="true">📖</span>Materi</a>
      <a class="menu-item" href="#/contoh"><span class="ikon" aria-hidden="true">💡</span>Contoh Soal</a>
      <a class="menu-item" href="#/latihan"><span class="ikon" aria-hidden="true">✏️</span>Latihan
        <span class="lencana">${Math.min(selesai, TOTAL_LATIHAN)}/${TOTAL_LATIHAN}</span></a>
      <a class="menu-item" href="#/kalkulator"><span class="ikon" aria-hidden="true">🧮</span>Kalkulator FPB</a>
      <a class="menu-item" href="#/uji"><span class="ikon" aria-hidden="true">🎯</span>Uji Diri
        ${skor ? `<span class="lencana">${skor.skor}/${skor.total}</span>` : ''}</a>
    </nav>

    <footer class="kaki">
      ${sudahTerpasang() ? '' : '<a href="#/pasang">Cara memasang aplikasi di HP</a>'}
    </footer>`;

  const tempat = root.querySelector('[data-banner]');

  function gambarBanner() {
    if (sudahTerpasang() || bannerDitunda()) {
      tempat.innerHTML = '';
      return;
    }
    if (bisaPasangLangsung()) {
      tempat.innerHTML = `
        <div class="banner">
          <p><span aria-hidden="true">📲</span> Pasang FPB Easy di HP-mu supaya mudah dibuka.</p>
          <div class="baris-tombol">
            <button type="button" class="tombol" data-aksi="pasang">Pasang</button>
            <button type="button" class="tombol tombol-kedua" data-aksi="nanti">Nanti</button>
          </div>
        </div>`;
    } else if (iPhone()) {
      tempat.innerHTML = `
        <div class="banner">
          <p><span aria-hidden="true">📲</span> Pasang FPB Easy di iPhone-mu.</p>
          <div class="baris-tombol">
            <a class="tombol" href="#/pasang">Caranya</a>
            <button type="button" class="tombol tombol-kedua" data-aksi="nanti">Nanti</button>
          </div>
        </div>`;
    } else {
      tempat.innerHTML = '';
    }
  }

  tempat.addEventListener('click', async (e) => {
    const aksi = e.target.closest('[data-aksi]')?.dataset.aksi;
    if (aksi === 'pasang') await pasang();
    if (aksi === 'nanti') tundaBanner();
    gambarBanner();
  });

  gambarBanner();
  document.addEventListener('status-pasang', gambarBanner);
  return () => document.removeEventListener('status-pasang', gambarBanner);
}
