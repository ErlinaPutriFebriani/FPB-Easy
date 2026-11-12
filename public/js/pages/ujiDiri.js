// Uji Diri: 5 soal campuran TANPA petunjuk (GL05). Nilai & pembahasan di akhir.
import { api } from '../api.js';
import { faktorPersekutuan } from '../fpb.js';
import { simpanSkorUji } from '../storage.js';
import {
  esc, formKodeHtml, galatHtml, kepala, langkahHtml, memuat, pasangFormKode, tabelHtml,
} from '../ui.js';

export function tampil(root) {
  const wadah = document.createElement('div');
  root.appendChild(wadah);

  let soal = [];
  let jawaban = [];
  let i = 0;

  function tampilPembuka() {
    wadah.innerHTML = `
      ${kepala('Uji Diri')}
      <section class="kartu">
        <p class="angka-besar" aria-hidden="true">🎯</p>
        <h2>5 soal, tanpa petunjuk</h2>
        <p>Kerjakan sendiri seperti ujian kecil. Boleh pakai kertas coretan.
           Nilai dan pembahasan muncul setelah semua soal dijawab.</p>
      </section>
      ${formKodeHtml()}
      <div class="baris-tombol bawah">
        <button type="button" class="tombol penuh" data-aksi="mulai">Mulai</button>
      </div>`;
    pasangFormKode(wadah);
  }

  async function mulai() {
    wadah.innerHTML = kepala('Uji Diri') + memuat('Menyiapkan soal…');
    try {
      soal = await api.uji();
      jawaban = soal.map(() => '');
      i = 0;
      tampilSoal();
    } catch (err) {
      wadah.innerHTML = kepala('Uji Diri') + galatHtml(err);
    }
  }

  function tampilSoal() {
    const s = soal[i];
    const terakhir = i === soal.length - 1;
    const titik = soal.map((_, n) => `<span class="titik${n === i ? ' aktif' : ''}${jawaban[n] ? ' terisi' : ''}"></span>`).join('');
    wadah.innerHTML = `
      ${kepala('Uji Diri', { kembali: '#/uji', kanan: `${i + 1} / ${soal.length}` })}
      <section class="kotak-soal">
        <p>${esc(s.pertanyaan)}</p>
        ${tabelHtml(s.tabel)}
      </section>
      <form class="kartu baris-input" data-form="jawab">
        <label for="isian">Jawabanmu</label>
        <input id="isian" type="number" inputmode="numeric" min="1" autocomplete="off" value="${esc(jawaban[i])}">
      </form>
      <p class="umpan salah" data-pesan aria-live="polite"></p>
      <div class="indikator" aria-hidden="true">${titik}</div>
      <div class="baris-tombol bawah">
        <button type="button" class="tombol tombol-kedua" data-aksi="sebelum" ${i === 0 ? 'disabled' : ''}>Kembali</button>
        <button type="button" class="tombol" data-aksi="${terakhir ? 'selesai' : 'lanjut'}">${terakhir ? 'Selesai & lihat nilai' : 'Lanjut ▸'}</button>
      </div>`;
  }

  function simpanIsian() {
    const input = wadah.querySelector('#isian');
    if (input) jawaban[i] = input.value.trim();
  }

  async function kirimJawaban() {
    const kosong = jawaban.findIndex((j) => !/^\d+$/.test(j));
    if (kosong !== -1) {
      i = kosong;
      tampilSoal();
      wadah.querySelector('[data-pesan]').textContent = 'Soal ini belum dijawab dengan angka.';
      return;
    }
    wadah.innerHTML = kepala('Uji Diri') + memuat('Menghitung nilai…');
    try {
      const hasil = await api.nilaiUji(soal.map((s, n) => ({ soal_id: s.id, isian: Number(jawaban[n]) })));
      simpanSkorUji(hasil.skor, hasil.total);
      tampilHasil(hasil);
    } catch (err) {
      wadah.innerHTML = kepala('Uji Diri') + galatHtml(err);
      // Jawaban tidak hilang: "Coba lagi" mengirim ulang.
      wadah.querySelector('[data-aksi="coba-lagi"]')?.setAttribute('data-aksi', 'kirim-ulang');
    }
  }

  function tampilHasil(hasil) {
    const persen = hasil.skor / hasil.total;
    let pesan = 'Tidak apa-apa. Ulangi Contoh dan Latihan dulu, lalu coba lagi, ya.';
    if (persen === 1) pesan = 'Sempurna! Kamu sudah paham FPB.';
    else if (persen >= 0.75) pesan = 'Hebat! Kamu hampir sempurna.';
    else if (persen >= 0.5) pesan = 'Lumayan! Pelajari pembahasan soal yang salah, ya.';

    wadah.innerHTML = `
      ${kepala('Hasil Uji Diri')}
      <section class="kartu nilai">
        <p class="skor"><b>${hasil.skor}</b> / ${hasil.total}</p>
        <p>${pesan}</p>
      </section>
      <ol class="daftar-hasil">
        ${hasil.rincian.map((r, n) => `
          <li class="hasil-item ${r.benar ? 'benar' : 'salah'}">
            <div class="hasil-kepala">
              <span>${r.benar ? '✓' : '✗'} Soal ${n + 1}</span>
              <span class="pesan-kecil">Jawabanmu: ${esc(r.isian ?? '-')}${r.benar ? '' : ` · Benar: ${r.jawaban}`}</span>
            </div>
            <details>
              <summary>Lihat pembahasan</summary>
              <p>${esc(r.pertanyaan)}</p>
              ${tabelHtml(r.tabel)}
              <div class="daftar-langkah">
                ${r.pembahasan.map((l, k) => langkahHtml(l, k + 1, sorotDari(r.pembahasan))).join('')}
              </div>
            </details>
          </li>`).join('')}
      </ol>
      <div class="baris-tombol bawah">
        <a class="tombol tombol-kedua" href="#/">Beranda</a>
        <button type="button" class="tombol" data-aksi="ulangi">Ulangi</button>
      </div>`;
  }

  function sorotDari(langkah) {
    const bil = langkah
      .filter((l) => /^Faktor \d+$/.test(l.judul))
      .map((l) => Number(l.judul.split(' ')[1]));
    return bil.length ? faktorPersekutuan(...bil) : [];
  }

  wadah.addEventListener('submit', (e) => {
    if (e.target.dataset.form !== 'jawab') return; // form kode siswa punya handler sendiri
    e.preventDefault();
    simpanIsian();
    if (i < soal.length - 1) {
      i++;
      tampilSoal();
    } else {
      kirimJawaban();
    }
  });

  wadah.addEventListener('click', (e) => {
    const aksi = e.target.closest('[data-aksi]')?.dataset.aksi;
    if (!aksi) return;
    if (aksi === 'mulai' || aksi === 'ulangi' || aksi === 'coba-lagi') return mulai();
    if (aksi === 'kirim-ulang') return kirimJawaban();
    simpanIsian();
    if (aksi === 'lanjut') i++;
    else if (aksi === 'sebelum') i--;
    else if (aksi === 'selesai') return kirimJawaban();
    tampilSoal();
  });

  tampilPembuka();
}
