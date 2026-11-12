// Contoh soal (worked example): langkah muncul satu per satu saat siswa menekan "Lanjut".
// Setiap langkah berisi alasan "dari mana angka ini berasal" (GL02, EL04).
import { api } from '../api.js';
import { faktorPersekutuan, fpb } from '../fpb.js';
import { acak, esc, galatHtml, gulirKe, kepala, langkahHtml, memuat, tabelHtml } from '../ui.js';

const NAMA_JENIS = { langsung: 'Soal langsung', cerita: 'Soal cerita', tabel: 'Soal tabel' };

let cacheContoh = null;

async function ambilContoh() {
  if (!cacheContoh) cacheContoh = await api.contoh();
  return cacheContoh;
}

export function tampil(root, [id]) {
  const wadah = document.createElement('div');
  root.appendChild(wadah);

  async function muat() {
    wadah.innerHTML = kepala('Contoh Soal') + memuat();
    try {
      const daftar = await ambilContoh();
      const soal = id ? daftar.find((s) => s.id === id) : null;
      if (soal) tampilDetail(soal);
      else tampilDaftar(daftar);
    } catch (err) {
      wadah.innerHTML = kepala('Contoh Soal') + galatHtml(err);
    }
  }

  function tampilDaftar(daftar) {
    wadah.innerHTML = `
      ${kepala('Contoh Soal')}
      <p class="pengantar">Pilih contoh. Bahasannya muncul satu langkah setiap kamu menekan <b>Lanjut</b>.</p>
      <div class="menu">
        ${daftar.map((s) => `
          <a class="menu-item" href="#/contoh/${encodeURIComponent(s.id)}">
            <span class="ikon" aria-hidden="true">${s.jenis === 'tabel' ? '📊' : s.jenis === 'cerita' ? '📝' : '🔢'}</span>
            <span>${esc(s.judul || NAMA_JENIS[s.jenis])}</span>
          </a>`).join('')}
      </div>`;
  }

  function tampilDetail(soal) {
    const sama = faktorPersekutuan(...soal.bilangan);
    const hasil = fpb(...soal.bilangan);
    const sorotSel = new Set((soal.sel_relevan || []).map(([b, k]) => `${b},${k}`));
    let tampak = 1;

    function gambar() {
      const selesai = tampak >= soal.langkah.length;
      // Sel tabel yang dipakai baru disorot setelah langkah "Diketahui" muncul.
      const sorot = tampak >= 1 ? sorotSel : new Set();
      wadah.innerHTML = `
        ${kepala(soal.judul || 'Contoh', { kembali: '#/contoh', kanan: `${Math.min(tampak, soal.langkah.length)} / ${soal.langkah.length}` })}
        <section class="kotak-soal">
          <p>${esc(soal.pertanyaan)}</p>
          ${tabelHtml(soal.tabel, { sorot })}
        </section>
        <div class="daftar-langkah">
          ${soal.langkah.slice(0, tampak).map((l, n) => langkahHtml(l, n + 1, sama)).join('')}
        </div>
        <div data-refleksi></div>
        <div class="baris-tombol bawah" data-tombol>
          ${selesai ? '' : '<button type="button" class="tombol" data-aksi="lanjut">Lanjut ▸</button>'}
        </div>`;
      if (selesai) tampilRefleksi();
    }

    function tampilRefleksi() {
      const tempat = wadah.querySelector('[data-refleksi]');
      const pilihan = acak([
        { teks: `Karena ${hasil} paling besar di antara faktor persekutuan`, benar: true },
        { teks: `Karena ${hasil} paling kecil di antara faktor persekutuan`, benar: false },
        { teks: `Karena ${hasil} muncul paling sering`, benar: false },
      ]);
      tempat.innerHTML = `
        <section class="kartu refleksi muncul">
          <h2>Coba pikirkan</h2>
          <p>Mengapa <b>${hasil}</b> yang dipilih sebagai FPB, bukan ${sama.length > 1 ? sama[sama.length - 2] : 'angka lain'}?</p>
          <div class="pilihan">
            ${pilihan.map((p, n) => `<button type="button" class="tombol-pilihan" data-pilih="${n}">${esc(p.teks)}</button>`).join('')}
          </div>
          <p class="umpan" data-umpan aria-live="polite"></p>
        </section>`;
      tempat.querySelectorAll('[data-pilih]').forEach((btn) => {
        btn.addEventListener('click', () => {
          const p = pilihan[Number(btn.dataset.pilih)];
          const umpan = tempat.querySelector('[data-umpan]');
          tempat.querySelectorAll('[data-pilih]').forEach((b) => b.classList.remove('dipilih'));
          btn.classList.add('dipilih');
          umpan.className = `umpan ${p.benar ? 'benar' : 'salah'}`;
          umpan.textContent = p.benar
            ? 'Tepat! FPB adalah faktor persekutuan yang TERBESAR.'
            : 'Belum tepat. Ingat, huruf T pada FPB artinya "Terbesar".';
          if (p.benar) {
            wadah.querySelector('[data-tombol]').innerHTML = `
              <a class="tombol tombol-kedua" href="#/contoh">Contoh lain</a>
              <a class="tombol" href="#/latihan/${soal.level}">Coba Latihan ▸</a>`;
          }
        });
      });
      gulirKe(tempat);
    }

    wadah.addEventListener('click', (e) => {
      if (e.target.closest('[data-aksi="lanjut"]')) {
        tampak++;
        gambar();
        gulirKe(wadah.querySelector('.daftar-langkah .langkah:last-child'));
      }
    });

    gambar();
  }

  wadah.addEventListener('click', (e) => {
    if (e.target.closest('[data-aksi="coba-lagi"]')) muat();
  });

  muat();
}
