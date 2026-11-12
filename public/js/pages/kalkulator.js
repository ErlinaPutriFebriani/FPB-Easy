// Kalkulator FPB yang menunjukkan CARA, bukan hanya hasil (DS01).
// Online: dihitung oleh Python (/api/fpb). Offline: dihitung oleh fpb.js di HP.
import { api, GagalJaringan } from '../api.js';
import { hitung, validasi } from '../fpb.js';
import { esc, gulirKe, kepala, langkahHtml } from '../ui.js';

export function tampil(root) {
  const wadah = document.createElement('div');
  root.appendChild(wadah);

  let jumlahInput = 2;
  let nilai = ['', '', ''];
  let hasil = null;
  let tampak = 0;
  let semuaLangkah = false;
  let catatan = '';

  function inputHtml(n) {
    return `
      <div class="baris-input">
        <label for="bil-${n}">Bilangan ${n + 1}</label>
        <input id="bil-${n}" data-bil="${n}" type="number" inputmode="numeric" min="1" max="1000"
          step="1" value="${esc(nilai[n])}" placeholder="misal ${[20, 28, 36][n]}">
      </div>`;
  }

  function gambar() {
    const langkah = hasil ? hasil.langkah : [];
    const selesai = hasil && tampak >= langkah.length;
    wadah.innerHTML = `
      ${kepala('Kalkulator FPB')}
      <form class="kartu" data-form="hitung" novalidate>
        ${Array.from({ length: jumlahInput }, (_, n) => inputHtml(n)).join('')}
        <div class="baris-tombol kecil">
          ${jumlahInput < 3
            ? '<button type="button" class="tautan" data-aksi="tambah">+ tambah bilangan</button>'
            : '<button type="button" class="tautan" data-aksi="kurang">− hapus bilangan ke-3</button>'}
        </div>
        <label class="saklar">
          <input type="checkbox" data-aksi="mode" ${semuaLangkah ? 'checked' : ''}>
          Tampilkan semua langkah sekaligus
        </label>
        <p class="umpan salah" data-pesan aria-live="polite"></p>
        <button type="submit" class="tombol penuh">Hitung</button>
      </form>
      ${hasil ? `
        <div class="daftar-langkah" aria-live="polite">
          ${langkah.slice(0, tampak).map((l, n) => langkahHtml(l, n + 1, hasil.faktor_persekutuan)).join('')}
        </div>
        ${selesai
          ? `<p class="hasil-fpb muncul">FPB dari ${hasil.bilangan.join(', ')} = <b>${hasil.fpb}</b></p>`
          : '<div class="baris-tombol bawah"><button type="button" class="tombol" data-aksi="lanjut">Langkah berikutnya ▸</button></div>'}
        ${catatan ? `<p class="pesan-kecil">${esc(catatan)}</p>` : ''}
      ` : ''}`;
  }

  async function hitungSekarang() {
    const pesan = wadah.querySelector('[data-pesan]');
    let bil;
    try {
      bil = validasi(nilai.slice(0, jumlahInput));
    } catch (err) {
      pesan.textContent = err.message;
      return;
    }
    catatan = '';
    try {
      hasil = await api.fpb(bil); // dihitung oleh Python di server
    } catch (err) {
      if (!(err instanceof GagalJaringan)) {
        pesan.textContent = err.message;
        return;
      }
      hasil = hitung(bil); // cadangan offline: dihitung di HP
      catatan = 'Sedang offline: dihitung langsung di HP-mu.';
    }
    tampak = semuaLangkah ? hasil.langkah.length : 1;
    gambar();
    gulirKe(wadah.querySelector('.daftar-langkah'));
  }

  wadah.addEventListener('input', (e) => {
    const n = e.target.dataset.bil;
    if (n !== undefined) nilai[Number(n)] = e.target.value;
  });

  wadah.addEventListener('change', (e) => {
    if (e.target.dataset.aksi === 'mode') {
      semuaLangkah = e.target.checked;
      if (hasil && semuaLangkah) tampak = hasil.langkah.length;
      gambar();
    }
  });

  wadah.addEventListener('submit', (e) => {
    e.preventDefault();
    hitungSekarang();
  });

  wadah.addEventListener('click', (e) => {
    const aksi = e.target.closest('[data-aksi]')?.dataset.aksi;
    if (aksi === 'tambah') {
      jumlahInput = 3;
      hasil = null;
      gambar();
      wadah.querySelector('#bil-2').focus();
    } else if (aksi === 'kurang') {
      jumlahInput = 2;
      nilai[2] = '';
      hasil = null;
      gambar();
    } else if (aksi === 'lanjut' && hasil) {
      tampak++;
      gambar();
      gulirKe(wadah.querySelector('.daftar-langkah .langkah:last-child'));
    }
  });

  gambar();
}
