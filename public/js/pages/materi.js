// Materi: kartu pendek, satu ide per layar (segmenting), siswa mengatur tempo.
import { api } from '../api.js';
import { faktorPersekutuan, fpb, teksPasangan } from '../fpb.js';
import { chips, daftarFaktorHtml, esc, galatHtml, kepala, memuat } from '../ui.js';

function contohHtml(contoh) {
  if (!contoh) return '';
  const bil = contoh.bilangan || [];
  switch (contoh.jenis) {
    case 'pasangan':
      return `<p class="angka-besar">${esc(teksPasangan(bil[0]))}</p>`;
    case 'faktor':
      return daftarFaktorHtml(bil, { warnai: false });
    case 'persekutuan':
      return `${daftarFaktorHtml(bil)}
        <div class="baris-faktor"><span class="label-faktor">Faktor persekutuan</span>
        ${chips(faktorPersekutuan(...bil), faktorPersekutuan(...bil))}</div>`;
    case 'fpb':
    case 'langkah':
      return `${daftarFaktorHtml(bil)}
        <p class="hasil-fpb">FPB dari ${bil.join(' dan ')} = <b>${fpb(...bil)}</b></p>`;
    case 'teks':
      return `<p class="contoh-teks">${esc(contoh.teks)}</p>`;
    default:
      return '';
  }
}

export function tampil(root) {
  const wadah = document.createElement('div');
  root.appendChild(wadah);
  let daftar = [];
  let i = 0;

  function gambar() {
    const kartu = daftar[i];
    const terakhir = i === daftar.length - 1;
    const titik = daftar
      .map((_, n) => `<span class="titik${n === i ? ' aktif' : ''}"></span>`)
      .join('');
    wadah.innerHTML = `
      ${kepala('Materi', { kanan: `${i + 1} / ${daftar.length}` })}
      <article class="kartu kartu-materi muncul" aria-live="polite">
        <h2>${esc(kartu.judul)}</h2>
        <p class="isi-materi">${esc(kartu.isi)}</p>
        <div class="contoh-visual">${contohHtml(kartu.contoh)}</div>
      </article>
      <div class="indikator" aria-hidden="true">${titik}</div>
      <div class="baris-tombol bawah">
        <button type="button" class="tombol tombol-kedua" data-aksi="kembali" ${i === 0 ? 'disabled' : ''}>Kembali</button>
        ${terakhir
          ? '<a class="tombol" href="#/contoh">Lihat Contoh Soal ▸</a>'
          : '<button type="button" class="tombol" data-aksi="lanjut">Lanjut ▸</button>'}
      </div>`;
  }

  wadah.addEventListener('click', (e) => {
    const aksi = e.target.closest('[data-aksi]')?.dataset.aksi;
    if (aksi === 'lanjut' && i < daftar.length - 1) i++;
    else if (aksi === 'kembali' && i > 0) i--;
    else if (aksi === 'coba-lagi') return muat();
    else return;
    gambar();
    window.scrollTo(0, 0);
  });

  async function muat() {
    wadah.innerHTML = kepala('Materi') + memuat();
    try {
      daftar = await api.materi();
      gambar();
    } catch (err) {
      wadah.innerHTML = kepala('Materi') + galatHtml(err);
    }
  }

  muat();
}
