// Cerminan JavaScript dari api/fpb.py.
// Dipakai untuk: tampilan (pewarnaan faktor persekutuan) dan kalkulator saat offline.
// Jika mengubah api/fpb.py, ubah juga file ini lalu jalankan tests/.

export const BATAS_MIN = 1;
export const BATAS_MAX = 1000;
export const JUMLAH_MIN = 2;
export const JUMLAH_MAX = 3;

/** Validasi 2-3 bilangan bulat 1..1000. Melempar Error berisi pesan ramah. */
export function validasi(bilangan) {
  if (!Array.isArray(bilangan) || bilangan.length < JUMLAH_MIN || bilangan.length > JUMLAH_MAX) {
    throw new Error('Masukkan 2 atau 3 bilangan, ya.');
  }
  return bilangan.map((b) => {
    let n = b;
    if (typeof n === 'string') {
      n = n.trim();
      if (!/^\d+$/.test(n)) throw new Error('Masukkan bilangan bulat positif, ya.');
      n = Number(n);
    }
    if (typeof n !== 'number' || Number.isNaN(n)) throw new Error('Masukkan bilangan bulat positif, ya.');
    if (!Number.isInteger(n)) throw new Error('Masukkan bilangan bulat, bukan desimal, ya.');
    if (n < BATAS_MIN) throw new Error('Bilangannya harus lebih dari 0, ya.');
    if (n > BATAS_MAX) throw new Error(`Bilangannya maksimal ${BATAS_MAX}, ya.`);
    return n;
  });
}

/** Pasangan perkalian yang hasilnya n. 12 -> [[1,12],[2,6],[3,4]] */
export function pasanganFaktor(n) {
  const hasil = [];
  for (let a = 1; a * a <= n; a++) {
    if (n % a === 0) hasil.push([a, n / a]);
  }
  return hasil;
}

/** Semua faktor n, terurut naik. */
export function faktor(n) {
  const kecil = [];
  const besar = [];
  for (const [a, b] of pasanganFaktor(n)) {
    kecil.push(a);
    if (a !== b) besar.push(b);
  }
  return kecil.concat(besar.reverse());
}

/** Faktor yang sama dari semua bilangan. */
export function faktorPersekutuan(...bilangan) {
  if (bilangan.length === 0) return [];
  let sama = faktor(bilangan[0]);
  for (const b of bilangan.slice(1)) {
    const fb = new Set(faktor(b));
    sama = sama.filter((x) => fb.has(x));
  }
  return sama;
}

export function fpb(...bilangan) {
  return Math.max(...faktorPersekutuan(...bilangan));
}

export function teksPasangan(n) {
  return `${n} = ` + pasanganFaktor(n).map(([a, b]) => `${a}×${b}`).join(' = ');
}

export const gabung = (angka) => angka.join(', ');

/** Langkah-langkah mencari FPB, format sama dengan langkah_fpb() di Python. */
export function langkahFPB(...bilangan) {
  const langkah = bilangan.map((b) => ({
    judul: `Faktor ${b}`,
    isi: faktor(b),
    alasan: `Karena ${teksPasangan(b)}`,
  }));
  const sama = faktorPersekutuan(...bilangan);
  langkah.push({
    judul: 'Faktor persekutuan',
    isi: sama,
    alasan: `Angka yang muncul di semua daftar faktor ${bilangan.join(' dan ')}.`,
  });
  const hasil = Math.max(...sama);
  langkah.push({
    judul: 'FPB',
    isi: [hasil],
    alasan: sama.length > 1
      ? `Dari ${gabung(sama)}, yang paling besar adalah ${hasil}.`
      : 'Faktor persekutuannya hanya 1, jadi FPB-nya 1.',
  });
  return langkah;
}

/** Sama seperti hitung() di Python: validasi -> langkah -> hasil. */
export function hitung(bilangan) {
  const bil = validasi(bilangan);
  const daftarFaktor = {};
  for (const b of bil) daftarFaktor[String(b)] = faktor(b);
  return {
    bilangan: bil,
    faktor: daftarFaktor,
    faktor_persekutuan: faktorPersekutuan(...bil),
    langkah: langkahFPB(...bil),
    fpb: fpb(...bil),
  };
}
