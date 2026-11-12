// Latihan 3 level (langsung -> cerita -> tabel) dengan fading A -> B -> C.
// Setiap soal dikerjakan per tahap; jawaban diperiksa oleh Python (/api/periksa).
//
// Tahap yang mungkin:
//   pilih_sel      (soal tabel)  : ketuk sel tabel yang dibutuhkan      -> literasi: merumuskan
//   pilih_bilangan (soal cerita) : ketuk angka yang dibagi               -> literasi: merumuskan
//   ditanya        (cerita/tabel, fading A & B): apa yang ditanyakan?
//   faktor         (fading B)    : tulis faktor bilangan berikutnya     -> menerapkan
//   persekutuan    (fading B)    : ketuk faktor yang sama
//   fpb            (semua)       : tulis FPB
//   kesimpulan     (cerita/tabel): pilih kalimat kesimpulan              -> menafsirkan
import { api, kirimAntrean } from '../api.js';
import { faktor, faktorPersekutuan, gabung } from '../fpb.js';
import { daftarSelesai, tambahAntrean, tandaiSelesai } from '../storage.js';
import {
  bacaDaftarAngka, chips, daftarFaktorHtml, esc, formKodeHtml, galatHtml, gulirKe, kepala,
  langkahHtml, memuat, pasangFormKode, tabelHtml,
} from '../ui.js';

const LEVEL = {
  1: { nama: 'Soal langsung', awalan: 'langsung-', ikon: '🔢', ket: 'Mencari FPB dari dua bilangan.' },
  2: { nama: 'Soal cerita', awalan: 'cerita-', ikon: '📝', ket: 'Memilih angka penting dari cerita.' },
  3: { nama: 'Soal tabel', awalan: 'tabel-', ikon: '📊', ket: 'Memilih informasi dari tabel.' },
};

export function tampil(root, [levelTeks]) {
  const wadah = document.createElement('div');
  root.appendChild(wadah);
  const level = Number(levelTeks);
  if (!LEVEL[level]) {
    tampilPilihLevel(wadah);
    return;
  }
  muatLevel(wadah, level);
}

function tampilPilihLevel(wadah) {
  const selesai = daftarSelesai();
  wadah.innerHTML = `
    ${kepala('Latihan')}
    <p class="pengantar">Mulai dari Level 1. Bantuan akan berkurang sedikit demi sedikit sampai kamu bisa mandiri.</p>
    <div class="menu">
      ${Object.entries(LEVEL).map(([n, l]) => {
        const jumlah = selesai.filter((id) => id.startsWith(l.awalan)).length;
        return `
          <a class="menu-item" href="#/latihan/${n}">
            <span class="ikon" aria-hidden="true">${l.ikon}</span>
            <span>Level ${n}: ${l.nama}<small>${l.ket}</small></span>
            <span class="lencana">${Math.min(jumlah, 3)}/3</span>
          </a>`;
      }).join('')}
    </div>
    ${formKodeHtml()}`;
  pasangFormKode(wadah);
}

async function muatLevel(wadah, level) {
  wadah.innerHTML = kepala(`Level ${level}`, { kembali: '#/latihan' }) + memuat();
  let daftar;
  try {
    daftar = await api.soal(level);
  } catch (err) {
    wadah.innerHTML = kepala(`Level ${level}`, { kembali: '#/latihan' }) + galatHtml(err);
    wadah.querySelector('[data-aksi="coba-lagi"]')?.addEventListener('click', () => muatLevel(wadah, level));
    return;
  }
  const selesai = new Set(daftarSelesai());
  const awal = Math.max(0, daftar.findIndex((s) => !selesai.has(s.id)));
  new SesiSoal(wadah, level, daftar, awal).mulai();
}

class SesiSoal {
  constructor(wadah, level, daftar, indeks) {
    this.wadah = wadah;
    this.level = level;
    this.daftar = daftar;
    this.indeks = indeks;
    this.wadah.addEventListener('click', (e) => this.klik(e));
    this.wadah.addEventListener('submit', (e) => {
      e.preventDefault();
      this.periksa();
    });
  }

  get soal() {
    return this.daftar[this.indeks];
  }

  mulai() {
    const s = this.soal;
    this.st = {
      tahap: [],
      posisi: 0,
      bilangan: s.bilangan || null,
      pilihan: new Set(), // sel / angka / opsi yang sedang dipilih
      selDipakai: new Set(),
      riwayat: [],
      pesan: '',
      benarPesan: false,
      petunjuk: [],
      salah: 0,
      jawabanFpb: null,
      pembahasan: null,
      selesai: false,
      sibuk: false,
      mulai: Date.now(),
    };
    if (s.jenis === 'tabel') this.st.tahap.push({ t: 'pilih_sel' });
    if (s.jenis === 'cerita') this.st.tahap.push({ t: 'pilih_bilangan' });
    if (s.jenis !== 'langsung' && s.fading !== 'C') this.st.tahap.push({ t: 'ditanya' });
    if (s.jenis === 'langsung') this.tambahTahapHitung();
    this.gambar();
  }

  tambahTahapHitung() {
    const s = this.soal;
    const b = this.st.bilangan;
    if (s.fading === 'B') {
      b.slice(1).forEach((n) => this.st.tahap.push({ t: 'faktor', n }));
      this.st.tahap.push({ t: 'persekutuan' });
    }
    this.st.tahap.push({ t: 'fpb' });
    if (s.pilihan_kesimpulan) this.st.tahap.push({ t: 'kesimpulan' });
  }

  get tahap() {
    return this.st.tahap[this.st.posisi];
  }

  // ------------------------------------------------------------ tampilan

  gambar() {
    const s = this.soal;
    const st = this.st;
    const tabelDiSoal = s.tabel && !(this.tahap && this.tahap.t === 'pilih_sel');
    this.wadah.innerHTML = `
      ${kepala(`Level ${this.level}: ${LEVEL[this.level].nama}`, {
        kembali: '#/latihan',
        kanan: `${this.indeks + 1} / ${this.daftar.length}`,
      })}
      <section class="kotak-soal lengket" aria-label="Soal">
        <p>${esc(s.pertanyaan)}</p>
        ${tabelDiSoal ? tabelHtml(s.tabel, { sorot: st.selDipakai }) : ''}
      </section>
      ${st.riwayat.length ? `<ul class="riwayat">${st.riwayat.map((r) => `<li>✓ ${esc(r)}</li>`).join('')}</ul>` : ''}
      ${st.selesai ? this.htmlSelesai() : this.htmlTahap()}`;
  }

  htmlTahap() {
    const s = this.soal;
    const st = this.st;
    const t = this.tahap;
    const nomor = st.posisi + 1;
    let isi = '';

    if (t.t === 'pilih_sel') {
      isi = `
        <h2>Langkah ${nomor}: Ketuk angka di tabel yang kamu butuhkan</h2>
        ${tabelHtml(s.tabel, { ketuk: true, pilih: st.pilihan })}`;
    } else if (t.t === 'pilih_bilangan') {
      isi = `
        <h2>Langkah ${nomor}: Ketuk angka yang menunjukkan banyak benda yang dibagi</h2>
        <div class="chips">${s.angka_cerita.map((a) => `
          <button type="button" class="chip chip-tombol${st.pilihan.has(String(a)) ? ' dipilih' : ''}"
            data-pilih="${a}" aria-pressed="${st.pilihan.has(String(a))}">${a}</button>`).join('')}
        </div>`;
    } else if (t.t === 'ditanya') {
      isi = `
        <h2>Langkah ${nomor}: Apa yang ditanyakan soal ini?</h2>
        <div class="pilihan">${s.pilihan_ditanya.map((p) => `
          <button type="button" class="tombol-pilihan${st.pilihan.has(p.nilai) ? ' dipilih' : ''}"
            data-pilih="${p.nilai}" data-tunggal="1">${esc(p.teks)}</button>`).join('')}
        </div>`;
    } else if (t.t === 'faktor') {
      const b0 = st.bilangan[0];
      isi = `
        <h2>Langkah ${nomor}: Tulis semua faktor ${t.n}</h2>
        <p class="pesan-kecil">Faktor ${b0} sudah dibantu:</p>
        ${daftarFaktorHtml([b0], { warnai: false })}
        <form class="baris-input" data-form="isian">
          <label for="isian" class="sr-only">Faktor ${t.n}</label>
          <input id="isian" name="isian" inputmode="numeric" autocomplete="off"
            placeholder="contoh: 1, 2, 3" value="${esc(st.ketikan || '')}">
        </form>
        <p class="pesan-kecil">Pisahkan dengan koma. Mulai dari 1.</p>`;
    } else if (t.t === 'persekutuan') {
      const [b0, ...lain] = st.bilangan;
      isi = `
        <h2>Langkah ${nomor}: Ketuk faktor ${b0} yang juga ada di faktor ${lain.join(' dan ')}</h2>
        ${daftarFaktorHtml(lain, { warnai: false })}
        <div class="baris-faktor"><span class="label-faktor">Faktor ${b0}</span>
          <div class="chips">${faktor(b0).map((a) => `
            <button type="button" class="chip chip-tombol${st.pilihan.has(String(a)) ? ' dipilih' : ''}"
              data-pilih="${a}" aria-pressed="${st.pilihan.has(String(a))}">${a}</button>`).join('')}
          </div>
        </div>`;
    } else if (t.t === 'fpb') {
      const b = st.bilangan;
      const sama = faktorPersekutuan(...b);
      let bantuan = '';
      if (s.fading === 'A' || s.fading === 'B') {
        bantuan = `${daftarFaktorHtml(b)}
          <div class="baris-faktor"><span class="label-faktor">Faktor persekutuan</span>${chips(sama, sama)}</div>`;
      } else {
        bantuan = '<p class="pesan-kecil">Kerjakan sendiri. Boleh pakai kertas coretan.</p>';
      }
      isi = `
        <h2>Langkah ${nomor}: Berapa FPB dari ${b.join(' dan ')}?</h2>
        ${bantuan}
        <form class="baris-input" data-form="isian">
          <label for="isian">FPB =</label>
          <input id="isian" name="isian" type="number" inputmode="numeric" min="1" autocomplete="off"
            value="${esc(st.ketikan || '')}">
        </form>`;
    } else if (t.t === 'kesimpulan') {
      isi = `
        <h2>Langkah ${nomor}: Pilih kesimpulan yang tepat</h2>
        <div class="pilihan">${s.pilihan_kesimpulan.map((p, n) => `
          <button type="button" class="tombol-pilihan${st.pilihan.has(String(n)) ? ' dipilih' : ''}"
            data-pilih="${n}" data-tunggal="1">${esc(p)}</button>`).join('')}
        </div>`;
    }

    const sisaPetunjuk = s.jumlah_petunjuk - st.petunjuk.length;
    return `
      <section class="kartu kerja muncul">${isi}</section>
      ${st.pesan ? `<p class="umpan ${st.benarPesan ? 'benar' : 'salah'}" role="status">${esc(st.pesan)}</p>` : ''}
      ${st.petunjuk.length ? `<div class="kotak-petunjuk">${st.petunjuk.map((p, n) => `<p><b>Petunjuk ${n + 1}:</b> ${esc(p)}</p>`).join('')}</div>` : ''}
      <div class="baris-tombol bawah">
        ${s.jumlah_petunjuk
          ? (sisaPetunjuk > 0
            ? `<button type="button" class="tombol tombol-kedua" data-aksi="petunjuk">Petunjuk (${st.petunjuk.length + 1}/${s.jumlah_petunjuk})</button>`
            : '<button type="button" class="tombol tombol-kedua" data-aksi="pembahasan">Lihat pembahasan</button>')
          : ''}
        <button type="button" class="tombol" data-aksi="periksa" ${st.sibuk ? 'disabled' : ''}>Periksa</button>
      </div>`;
  }

  htmlSelesai() {
    const st = this.st;
    const adaBerikutnya = this.indeks < this.daftar.length - 1;
    let pujian;
    if (st.pembahasan) pujian = 'Pelajari pembahasannya, lalu coba soal berikutnya, ya.';
    else if (st.salah === 0) pujian = 'Hebat, semua langkah benar tanpa salah!';
    else pujian = 'Kamu berhasil setelah mencoba lagi. Itu bagus!';

    return `
      ${st.pesan ? `<p class="umpan ${st.benarPesan ? 'benar' : 'salah'}" role="status">${esc(st.pesan)}</p>` : ''}
      ${st.pembahasan ? `
        <section class="daftar-langkah">
          <h2>Pembahasan</h2>
          ${st.pembahasan.map((l, n) => langkahHtml(l, n + 1, faktorPersekutuan(...st.bilangan))).join('')}
        </section>` : ''}
      <section class="kartu selesai muncul">
        <p class="angka-besar" aria-hidden="true">${st.pembahasan ? '📘' : '🎉'}</p>
        <h2>Soal selesai!</h2>
        <p>${pujian}</p>
      </section>
      <div class="baris-tombol bawah">
        ${adaBerikutnya
          ? '<button type="button" class="tombol" data-aksi="berikutnya">Soal berikutnya ▸</button>'
          : `<a class="tombol tombol-kedua" href="#/latihan">Daftar level</a>
             ${this.level < 3
              ? `<a class="tombol" href="#/latihan/${this.level + 1}">Level ${this.level + 1} ▸</a>`
              : '<a class="tombol" href="#/uji">Coba Uji Diri ▸</a>'}`}
      </div>`;
  }

  // ------------------------------------------------------------ interaksi

  klik(e) {
    const sel = e.target.closest('[data-sel]');
    if (sel) {
      this.togglePilihan(sel.dataset.sel, false);
      return;
    }
    const pilih = e.target.closest('[data-pilih]');
    if (pilih) {
      this.togglePilihan(pilih.dataset.pilih, pilih.dataset.tunggal === '1');
      return;
    }
    const aksi = e.target.closest('[data-aksi]')?.dataset.aksi;
    if (aksi === 'periksa') this.periksa();
    else if (aksi === 'petunjuk') this.ambilPetunjuk();
    else if (aksi === 'pembahasan') this.ambilPembahasan();
    else if (aksi === 'berikutnya') {
      this.indeks++;
      this.mulai();
      window.scrollTo(0, 0);
    }
  }

  simpanKetikan() {
    const input = this.wadah.querySelector('#isian');
    if (input) this.st.ketikan = input.value;
  }

  togglePilihan(nilai, tunggal) {
    const p = this.st.pilihan;
    if (tunggal) {
      p.clear();
      p.add(nilai);
    } else if (p.has(nilai)) p.delete(nilai);
    else p.add(nilai);
    this.st.pesan = '';
    this.gambar();
  }

  isianTahap() {
    const t = this.tahap;
    const p = [...this.st.pilihan];
    const teks = (this.wadah.querySelector('#isian')?.value || '').trim();
    switch (t.t) {
      case 'pilih_sel':
        return p.length
          ? { isian: p.map((k) => k.split(',').map(Number)) }
          : { kosong: 'Ketuk dulu angka di tabel yang kamu butuhkan, ya.' };
      case 'pilih_bilangan':
      case 'persekutuan':
        return p.length ? { isian: p.map(Number) } : { kosong: 'Ketuk dulu angkanya, ya.' };
      case 'ditanya':
        return p.length ? { isian: p[0] } : { kosong: 'Pilih salah satu jawaban dulu, ya.' };
      case 'kesimpulan':
        return p.length
          ? { isian: this.soal.pilihan_kesimpulan[Number(p[0])] }
          : { kosong: 'Pilih salah satu kalimat dulu, ya.' };
      case 'faktor': {
        const daftar = bacaDaftarAngka(teks);
        if (!daftar) return { kosong: 'Tulis faktor-faktornya dengan angka, dipisah koma. Contoh: 1, 2, 3' };
        return { isian: { bilangan: t.n, daftar } };
      }
      case 'fpb':
        if (!/^\d+$/.test(teks)) return { kosong: 'Tulis jawabanmu dengan angka, ya.' };
        return { isian: Number(teks) };
      default:
        return { kosong: 'Tahap tidak dikenal.' };
    }
  }

  async periksa() {
    if (this.st.sibuk || this.st.selesai) return;
    this.simpanKetikan();
    const { isian, kosong } = this.isianTahap();
    if (kosong) {
      this.st.pesan = kosong;
      this.st.benarPesan = false;
      this.gambar();
      return;
    }
    this.st.sibuk = true;
    let hasil;
    try {
      hasil = await api.periksa(this.soal.id, this.tahap.t, isian);
    } catch (err) {
      this.st.sibuk = false;
      this.st.pesan = err.message;
      this.st.benarPesan = false;
      this.gambar();
      return;
    }
    this.st.sibuk = false;
    this.st.pesan = hasil.pesan;
    this.st.benarPesan = hasil.benar;

    if (!hasil.benar) {
      this.st.salah++;
      this.gambar();
      this.wadah.querySelector('.umpan')?.focus?.();
      return;
    }
    this.lanjutTahap(isian, hasil);
  }

  lanjutTahap(isian, hasil) {
    const st = this.st;
    const t = this.tahap;
    if (t.t === 'pilih_sel' || t.t === 'pilih_bilangan') {
      st.bilangan = hasil.bilangan;
      if (t.t === 'pilih_sel') st.selDipakai = new Set(st.pilihan);
      st.riwayat.push(`Angka yang dipakai: ${st.bilangan.join(' dan ')}`);
      this.tambahTahapHitung();
    } else if (t.t === 'ditanya') {
      st.riwayat.push('Yang ditanya: FPB');
    } else if (t.t === 'faktor') {
      st.riwayat.push(`Faktor ${t.n}: ${gabung(faktor(t.n))}`);
    } else if (t.t === 'persekutuan') {
      st.riwayat.push(`Faktor persekutuan: ${gabung(faktorPersekutuan(...st.bilangan))}`);
    } else if (t.t === 'fpb') {
      st.jawabanFpb = isian;
      st.riwayat.push(`FPB = ${isian}`);
    } else if (t.t === 'kesimpulan') {
      st.riwayat.push('Kesimpulan sudah tepat');
    }
    st.posisi++;
    st.pilihan = new Set();
    st.ketikan = '';
    if (st.posisi >= st.tahap.length) this.selesaikan();
    this.gambar();
    gulirKe(this.wadah.querySelector('.kerja, .selesai'));
  }

  async ambilPetunjuk() {
    this.simpanKetikan();
    try {
      const res = await api.petunjuk(this.soal.id, this.st.petunjuk.length + 1);
      if (res.teks) this.st.petunjuk.push(res.teks);
    } catch (err) {
      this.st.pesan = err.message;
      this.st.benarPesan = false;
    }
    this.gambar();
    gulirKe(this.wadah.querySelector('.kotak-petunjuk'));
  }

  async ambilPembahasan() {
    try {
      const res = await api.pembahasan(this.soal.id);
      this.st.pembahasan = res.langkah;
      if (!this.st.bilangan) {
        // Ambil bilangan dari langkah "Faktor X" pembahasan (untuk pewarnaan).
        this.st.bilangan = res.langkah
          .filter((l) => /^Faktor \d+$/.test(l.judul))
          .map((l) => Number(l.judul.split(' ')[1]));
      }
      this.st.pesan = '';
      this.selesaikan();
    } catch (err) {
      this.st.pesan = err.message;
      this.st.benarPesan = false;
    }
    this.gambar();
  }

  selesaikan() {
    const st = this.st;
    if (st.selesai) return;
    st.selesai = true;
    tandaiSelesai(this.soal.id);
    tambahAntrean({
      soal_id: this.soal.id,
      jawaban: st.jawabanFpb === null ? '' : String(st.jawabanFpb),
      benar: st.salah === 0 && !st.pembahasan,
      jumlah_salah: st.salah,
      jumlah_petunjuk: st.petunjuk.length,
      durasi_detik: Math.round((Date.now() - st.mulai) / 1000),
    });
    kirimAntrean();
  }
}
