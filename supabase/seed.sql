begin;
-- FPB Easy: isi awal materi & soal.
-- DIBUAT OTOMATIS oleh scripts/buat_seed_sql.py dari api/data/konten.json. Jangan edit manual.
-- Jalankan di Supabase SQL Editor setelah schema.sql. Aman dijalankan berulang (upsert).

create temp table _konten on commit drop as select $konten$
{
  "materi": [
    {
      "id": 1,
      "urutan": 1,
      "judul": "Ingat lagi: perkalian",
      "isi": "Faktor selalu berhubungan dengan perkalian. Kalau 3 × 4 = 12, maka 3 dan 4 adalah faktor dari 12.",
      "contoh": { "jenis": "pasangan", "bilangan": [12] }
    },
    {
      "id": 2,
      "urutan": 2,
      "judul": "Apa itu faktor?",
      "isi": "Faktor adalah bilangan yang membagi habis sebuah bilangan, tanpa sisa. Cari dengan membagi mulai dari 1, 2, 3, dan seterusnya.",
      "contoh": { "jenis": "faktor", "bilangan": [12] }
    },
    {
      "id": 3,
      "urutan": 3,
      "judul": "Faktor persekutuan",
      "isi": "Faktor persekutuan adalah faktor yang SAMA dari dua bilangan atau lebih. Angka yang sama diberi warna oranye.",
      "contoh": { "jenis": "persekutuan", "bilangan": [16, 24] }
    },
    {
      "id": 4,
      "urutan": 4,
      "judul": "Apa itu FPB?",
      "isi": "FPB adalah Faktor Persekutuan Terbesar, yaitu faktor persekutuan yang paling besar.",
      "contoh": { "jenis": "fpb", "bilangan": [16, 24] }
    },
    {
      "id": 5,
      "urutan": 5,
      "judul": "3 langkah mencari FPB",
      "isi": "1) Tulis faktor tiap bilangan. 2) Cari faktor yang sama. 3) Pilih yang paling besar.",
      "contoh": { "jenis": "langkah", "bilangan": [18, 27] }
    },
    {
      "id": 6,
      "urutan": 6,
      "judul": "FPB dalam kehidupan",
      "isi": "FPB dipakai saat membagi beberapa jenis benda ke kelompok yang isinya sama banyak, dan ingin kelompoknya sebanyak mungkin.",
      "contoh": { "jenis": "teks", "teks": "24 apel dan 36 jeruk → paling banyak 12 kantong, tiap kantong 2 apel dan 3 jeruk." }
    }
  ],
  "soal": [
    {
      "id": "contoh-langsung",
      "peran": "contoh",
      "level": 1,
      "jenis": "langsung",
      "fading": "A",
      "judul": "Contoh 1: Soal langsung",
      "pertanyaan": "Tentukan FPB dari 16 dan 24.",
      "diketahui": "Bilangan 16 dan 24.",
      "ditanya": "FPB dari 16 dan 24.",
      "tabel": null,
      "sel_relevan": null,
      "umpan_balik_sel": null,
      "bilangan": [16, 24],
      "jawaban": 8,
      "kesimpulan": "Jadi, FPB dari 16 dan 24 adalah 8.",
      "pilihan_kesimpulan": null,
      "petunjuk": []
    },
    {
      "id": "contoh-cerita",
      "peran": "contoh",
      "level": 2,
      "jenis": "cerita",
      "fading": "A",
      "judul": "Contoh 2: Soal cerita",
      "pertanyaan": "Ibu memiliki 24 apel dan 36 jeruk. Buah itu dimasukkan ke dalam kantong. Isi setiap kantong sama banyak. Berapa kantong paling banyak yang bisa dibuat?",
      "diketahui": "Ada 24 apel dan 36 jeruk.",
      "ditanya": "Banyak kantong paling banyak dengan isi sama → ini soal FPB.",
      "tabel": null,
      "sel_relevan": null,
      "umpan_balik_sel": null,
      "bilangan": [24, 36],
      "jawaban": 12,
      "kesimpulan": "Jadi, paling banyak 12 kantong. Tiap kantong berisi 2 apel (24 : 12) dan 3 jeruk (36 : 12).",
      "pilihan_kesimpulan": null,
      "petunjuk": []
    },
    {
      "id": "contoh-tabel",
      "peran": "contoh",
      "level": 3,
      "jenis": "tabel",
      "fading": "A",
      "judul": "Contoh 3: Soal tabel",
      "pertanyaan": "Bu Ani membuat kotak hampers berisi bolu dan donat. Isi setiap kotak sama banyak. Berapa kotak paling banyak yang bisa dibuat?",
      "diketahui": "Dari tabel: bolu 24 buah dan donat 30 buah. Kolom harga dan baris roti tidak dipakai.",
      "ditanya": "Banyak kotak paling banyak dengan isi sama → ini soal FPB.",
      "tabel": {
        "kolom": ["Kue", "Jumlah", "Harga"],
        "baris": [["Bolu", 24, "Rp5.000"], ["Donat", 30, "Rp3.000"], ["Roti", 20, "Rp4.000"]]
      },
      "sel_relevan": [[0, 1], [1, 1]],
      "umpan_balik_sel": null,
      "bilangan": [24, 30],
      "jawaban": 6,
      "kesimpulan": "Jadi, paling banyak 6 kotak. Tiap kotak berisi 4 bolu (24 : 6) dan 5 donat (30 : 6).",
      "pilihan_kesimpulan": null,
      "petunjuk": []
    },

    {
      "id": "langsung-a",
      "peran": "latihan",
      "level": 1,
      "jenis": "langsung",
      "fading": "A",
      "pertanyaan": "Tentukan FPB dari 18 dan 27.",
      "diketahui": "Bilangan 18 dan 27.",
      "ditanya": "FPB dari 18 dan 27.",
      "tabel": null,
      "sel_relevan": null,
      "umpan_balik_sel": null,
      "bilangan": [18, 27],
      "jawaban": 9,
      "kesimpulan": null,
      "pilihan_kesimpulan": null,
      "petunjuk": [
        "FPB adalah faktor persekutuan yang PALING BESAR.",
        "Faktor persekutuan 18 dan 27 adalah 1, 3, dan 9.",
        "Dari 1, 3, 9, yang paling besar adalah 9."
      ]
    },
    {
      "id": "langsung-b",
      "peran": "latihan",
      "level": 1,
      "jenis": "langsung",
      "fading": "B",
      "pertanyaan": "Tentukan FPB dari 20 dan 28.",
      "diketahui": "Bilangan 20 dan 28.",
      "ditanya": "FPB dari 20 dan 28.",
      "tabel": null,
      "sel_relevan": null,
      "umpan_balik_sel": null,
      "bilangan": [20, 28],
      "jawaban": 4,
      "kesimpulan": null,
      "pilihan_kesimpulan": null,
      "petunjuk": [
        "Faktor adalah bilangan yang membagi habis. Coba bagi 28 dengan 1, 2, 3, ... satu per satu.",
        "Faktor 28: 1, 2, 4, __, 14, 28. Angka berapa yang hilang? (ingat 4 × 7 = 28)",
        "Faktor sama dari 20 dan 28 adalah 1, 2, 4. Yang terbesar 4."
      ]
    },
    {
      "id": "langsung-c",
      "peran": "latihan",
      "level": 1,
      "jenis": "langsung",
      "fading": "C",
      "pertanyaan": "Tentukan FPB dari 24 dan 32.",
      "diketahui": "Bilangan 24 dan 32.",
      "ditanya": "FPB dari 24 dan 32.",
      "tabel": null,
      "sel_relevan": null,
      "umpan_balik_sel": null,
      "bilangan": [24, 32],
      "jawaban": 8,
      "kesimpulan": null,
      "pilihan_kesimpulan": null,
      "petunjuk": [
        "Tulis dulu faktor 24, lalu faktor 32.",
        "Faktor 24: 1, 2, 3, 4, 6, 8, 12, 24. Faktor 32: 1, 2, 4, 8, 16, 32.",
        "Faktor yang sama: 1, 2, 4, 8. Yang terbesar 8."
      ]
    },

    {
      "id": "cerita-a",
      "peran": "latihan",
      "level": 2,
      "jenis": "cerita",
      "fading": "A",
      "pertanyaan": "Pak Budi punya 30 kelereng merah dan 45 kelereng biru. Semua kelereng dimasukkan ke kantong. Isi setiap kantong sama banyak. Berapa kantong paling banyak yang bisa dibuat?",
      "diketahui": "30 kelereng merah dan 45 kelereng biru.",
      "ditanya": "Banyak kantong paling banyak dengan isi sama.",
      "tabel": null,
      "sel_relevan": null,
      "umpan_balik_sel": null,
      "bilangan": [30, 45],
      "jawaban": 15,
      "kesimpulan": "Paling banyak 15 kantong, tiap kantong berisi 2 kelereng merah dan 3 kelereng biru.",
      "pilihan_kesimpulan": [
        "Paling banyak 15 kantong, tiap kantong berisi 2 kelereng merah dan 3 kelereng biru.",
        "Paling banyak 75 kantong, karena 30 + 45 = 75.",
        "Paling banyak 5 kantong, tiap kantong berisi 6 kelereng merah dan 9 kelereng biru."
      ],
      "petunjuk": [
        "Angka apa saja yang menunjukkan banyak benda yang dibagi?",
        "Bendanya kelereng merah dan kelereng biru. Cari FPB dari 30 dan 45.",
        "Faktor persekutuan 30 dan 45: 1, 3, 5, 15. FPB = 15."
      ]
    },
    {
      "id": "cerita-b",
      "peran": "latihan",
      "level": 2,
      "jenis": "cerita",
      "fading": "B",
      "pertanyaan": "Kelas 8A mengumpulkan 32 buku tulis dan 48 pensil untuk disumbangkan. Ada 3 guru yang membantu mengemas. Semua barang dibagi ke paket yang isinya sama. Berapa paket paling banyak yang bisa dibuat?",
      "diketahui": "32 buku tulis dan 48 pensil. (Angka 8 dan 3 tidak dipakai.)",
      "ditanya": "Banyak paket paling banyak dengan isi sama.",
      "tabel": null,
      "sel_relevan": null,
      "umpan_balik_sel": null,
      "bilangan": [32, 48],
      "jawaban": 16,
      "kesimpulan": "Paling banyak 16 paket, tiap paket berisi 2 buku tulis dan 3 pensil.",
      "pilihan_kesimpulan": [
        "Paling banyak 3 paket, karena ada 3 guru.",
        "Paling banyak 16 paket, tiap paket berisi 2 buku tulis dan 3 pensil.",
        "Paling banyak 8 paket, tiap paket berisi 4 buku tulis dan 6 pensil."
      ],
      "petunjuk": [
        "Barang apa saja yang dibagi ke paket? Angka kelas dan banyak guru tidak dibagi.",
        "Faktor 48: 1, 2, 3, 4, 6, 8, 12, __, 24, 48. (ingat 3 × 16 = 48)",
        "Faktor persekutuan 32 dan 48: 1, 2, 4, 8, 16. FPB = 16."
      ]
    },
    {
      "id": "cerita-c",
      "peran": "latihan",
      "level": 2,
      "jenis": "cerita",
      "fading": "C",
      "pertanyaan": "Regu pramuka punya 42 tali dan 56 tongkat. Kegiatan berlangsung 2 hari. Semua tali dan tongkat dibagi rata ke beberapa kelompok dengan isi yang sama. Berapa kelompok paling banyak?",
      "diketahui": "42 tali dan 56 tongkat. (Angka 2 hari tidak dipakai.)",
      "ditanya": "Banyak kelompok paling banyak dengan isi sama.",
      "tabel": null,
      "sel_relevan": null,
      "umpan_balik_sel": null,
      "bilangan": [42, 56],
      "jawaban": 14,
      "kesimpulan": "Paling banyak 14 kelompok, tiap kelompok mendapat 3 tali dan 4 tongkat.",
      "pilihan_kesimpulan": [
        "Paling banyak 7 kelompok, tiap kelompok mendapat 6 tali dan 8 tongkat.",
        "Paling banyak 98 kelompok, karena 42 + 56 = 98.",
        "Paling banyak 14 kelompok, tiap kelompok mendapat 3 tali dan 4 tongkat."
      ],
      "petunjuk": [
        "Benda yang dibagi adalah tali dan tongkat. Lama kegiatan tidak dibagi.",
        "Cari FPB dari 42 dan 56.",
        "Faktor persekutuan 42 dan 56: 1, 2, 7, 14. FPB = 14."
      ]
    },

    {
      "id": "tabel-a",
      "peran": "latihan",
      "level": 3,
      "jenis": "tabel",
      "fading": "A",
      "pertanyaan": "Bu Rina ingin membuat paket berisi PENSIL dan BUKU. Isi setiap paket sama banyak. Berapa paket paling banyak yang bisa dibuat?",
      "diketahui": "Pensil 48 dan buku 36.",
      "ditanya": "Banyak paket paling banyak dengan isi sama.",
      "tabel": {
        "kolom": ["Barang", "Jumlah", "Harga"],
        "baris": [["Pensil", 48, "Rp2.000"], ["Buku", 36, "Rp5.000"], ["Penghapus", 60, "Rp1.000"]]
      },
      "sel_relevan": [[0, 1], [1, 1]],
      "umpan_balik_sel": {
        "kolom:0": "Nama barang bukan angka yang dihitung. Pilih angka jumlahnya.",
        "kolom:2": "Soal menanyakan banyak paket, bukan harga. Coba lihat kolom Jumlah.",
        "baris:2": "Penghapus tidak dimasukkan ke paket. Baca lagi barang apa saja yang disebut."
      },
      "bilangan": [48, 36],
      "jawaban": 12,
      "kesimpulan": "Paling banyak 12 paket, tiap paket berisi 4 pensil dan 3 buku.",
      "pilihan_kesimpulan": [
        "Paling banyak 12 paket, tiap paket berisi 4 pensil dan 3 buku.",
        "Paling banyak 84 paket, karena 48 + 36 = 84.",
        "Paling banyak 6 paket, tiap paket berisi 8 pensil dan 6 buku."
      ],
      "petunjuk": [
        "Barang apa saja yang masuk paket? Cari barisnya di tabel.",
        "Lihat kolom Jumlah untuk pensil dan buku saja.",
        "Cari FPB dari 48 dan 36. Faktor persekutuannya 1, 2, 3, 4, 6, 12."
      ]
    },
    {
      "id": "tabel-b",
      "peran": "latihan",
      "level": 3,
      "jenis": "tabel",
      "fading": "B",
      "pertanyaan": "Hasil panen kebun sekolah ada di tabel. MANGGA dan JERUK akan dimasukkan ke keranjang. Banyak buah di setiap keranjang sama. Berapa keranjang paling banyak yang dibutuhkan?",
      "diketahui": "Mangga 54 buah dan jeruk 72 buah.",
      "ditanya": "Banyak keranjang paling banyak dengan isi sama.",
      "tabel": {
        "kolom": ["Buah", "Banyak (buah)", "Berat (kg)"],
        "baris": [["Mangga", 54, 18], ["Jeruk", 72, 12], ["Apel", 40, 8]]
      },
      "sel_relevan": [[0, 1], [1, 1]],
      "umpan_balik_sel": {
        "kolom:0": "Nama buah bukan angka yang dihitung. Pilih banyak buahnya.",
        "kolom:2": "Yang dibagi adalah banyak buah, bukan beratnya. Coba lihat kolom Banyak (buah).",
        "baris:2": "Apel tidak dimasukkan ke keranjang. Soal hanya menyebut mangga dan jeruk."
      },
      "bilangan": [54, 72],
      "jawaban": 18,
      "kesimpulan": "Paling banyak 18 keranjang, tiap keranjang berisi 3 mangga dan 4 jeruk.",
      "pilihan_kesimpulan": [
        "Paling banyak 6 keranjang, karena berat mangga 18 kg dan jeruk 12 kg.",
        "Paling banyak 18 keranjang, tiap keranjang berisi 3 mangga dan 4 jeruk.",
        "Paling banyak 9 keranjang, tiap keranjang berisi 6 mangga dan 8 jeruk."
      ],
      "petunjuk": [
        "Soal menanyakan banyak buah, jadi pakai kolom Banyak (buah), bukan Berat.",
        "Faktor 72: 1, 2, 3, 4, 6, 8, 9, 12, __, 24, 36, 72. (ingat 4 × 18 = 72)",
        "Faktor persekutuan 54 dan 72: 1, 2, 3, 6, 9, 18. FPB = 18."
      ]
    },
    {
      "id": "tabel-c",
      "peran": "latihan",
      "level": 3,
      "jenis": "tabel",
      "fading": "C",
      "pertanyaan": "Siswa PUTRA dan PUTRI kelas 7A dibagi menjadi beberapa kelompok. Setiap kelompok punya banyak putra yang sama dan banyak putri yang sama. Berapa kelompok paling banyak?",
      "diketahui": "Kelas 7A: putra 18 dan putri 24.",
      "ditanya": "Banyak kelompok paling banyak.",
      "tabel": {
        "kolom": ["Kelas", "Putra", "Putri"],
        "baris": [["7A", 18, 24], ["7B", 20, 16], ["8A", 15, 21]]
      },
      "sel_relevan": [[0, 1], [0, 2]],
      "umpan_balik_sel": {
        "kolom:0": "Nama kelas bukan angka yang dihitung. Pilih banyak siswanya.",
        "baris:1": "Itu data kelas 7B. Soal hanya menanyakan kelas 7A.",
        "baris:2": "Itu data kelas 8A. Soal hanya menanyakan kelas 7A."
      },
      "bilangan": [18, 24],
      "jawaban": 6,
      "kesimpulan": "Paling banyak 6 kelompok, tiap kelompok berisi 3 putra dan 4 putri.",
      "pilihan_kesimpulan": [
        "Paling banyak 6 kelompok, tiap kelompok berisi 3 putra dan 4 putri.",
        "Paling banyak 42 kelompok, karena 18 + 24 = 42.",
        "Paling banyak 3 kelompok, tiap kelompok berisi 6 putra dan 8 putri."
      ],
      "petunjuk": [
        "Cari baris kelas 7A saja, lalu lihat kolom Putra dan Putri.",
        "Cari FPB dari 18 dan 24.",
        "Faktor persekutuan 18 dan 24: 1, 2, 3, 6. FPB = 6."
      ]
    },

    {
      "id": "uji-langsung-1",
      "peran": "uji",
      "level": 1,
      "jenis": "langsung",
      "fading": "C",
      "pertanyaan": "Tentukan FPB dari 36 dan 48.",
      "diketahui": "Bilangan 36 dan 48.",
      "ditanya": "FPB dari 36 dan 48.",
      "tabel": null,
      "sel_relevan": null,
      "umpan_balik_sel": null,
      "bilangan": [36, 48],
      "jawaban": 12,
      "kesimpulan": null,
      "pilihan_kesimpulan": null,
      "petunjuk": []
    },
    {
      "id": "uji-langsung-2",
      "peran": "uji",
      "level": 1,
      "jenis": "langsung",
      "fading": "C",
      "pertanyaan": "Tentukan FPB dari 45 dan 60.",
      "diketahui": "Bilangan 45 dan 60.",
      "ditanya": "FPB dari 45 dan 60.",
      "tabel": null,
      "sel_relevan": null,
      "umpan_balik_sel": null,
      "bilangan": [45, 60],
      "jawaban": 15,
      "kesimpulan": null,
      "pilihan_kesimpulan": null,
      "petunjuk": []
    },
    {
      "id": "uji-cerita-1",
      "peran": "uji",
      "level": 2,
      "jenis": "cerita",
      "fading": "C",
      "pertanyaan": "Ani punya 27 stiker bintang dan 45 stiker hati. Ani berumur 13 tahun. Semua stiker dibagikan ke teman-temannya. Setiap teman mendapat stiker dengan jumlah yang sama. Paling banyak berapa teman yang bisa mendapat stiker?",
      "diketahui": "27 stiker bintang dan 45 stiker hati. (Umur Ani tidak dipakai.)",
      "ditanya": "Banyak teman paling banyak.",
      "tabel": null,
      "sel_relevan": null,
      "umpan_balik_sel": null,
      "bilangan": [27, 45],
      "jawaban": 9,
      "kesimpulan": "Paling banyak 9 teman, tiap teman mendapat 3 stiker bintang dan 5 stiker hati.",
      "pilihan_kesimpulan": null,
      "petunjuk": []
    },
    {
      "id": "uji-tabel-1",
      "peran": "uji",
      "level": 3,
      "jenis": "tabel",
      "fading": "C",
      "pertanyaan": "KOMIK dan NOVEL di perpustakaan akan dimasukkan ke dalam kardus. Isi setiap kardus sama. Berapa kardus paling banyak yang dibutuhkan?",
      "diketahui": "Komik 60 dan novel 84.",
      "ditanya": "Banyak kardus paling banyak.",
      "tabel": {
        "kolom": ["Jenis buku", "Jumlah", "Rak"],
        "baris": [["Komik", 60, 3], ["Novel", 84, 4], ["Kamus", 30, 2]]
      },
      "sel_relevan": [[0, 1], [1, 1]],
      "umpan_balik_sel": null,
      "bilangan": [60, 84],
      "jawaban": 12,
      "kesimpulan": "Paling banyak 12 kardus, tiap kardus berisi 5 komik dan 7 novel.",
      "pilihan_kesimpulan": null,
      "petunjuk": []
    }
  ]
}

$konten$::jsonb as j;

insert into materi (id, urutan, judul, isi, contoh)
select r.id, r.urutan, r.judul, r.isi, r.contoh
from _konten, jsonb_populate_recordset(null::materi, _konten.j -> 'materi') as r
on conflict (id) do update set
  urutan = excluded.urutan, judul = excluded.judul, isi = excluded.isi, contoh = excluded.contoh;

select setval(pg_get_serial_sequence('materi', 'id'), (select max(id) from materi));

insert into soal (id, peran, level, jenis, fading, judul, pertanyaan, diketahui, ditanya, tabel,
                  sel_relevan, umpan_balik_sel, bilangan, jawaban, kesimpulan, pilihan_kesimpulan,
                  petunjuk, aktif)
select r.id, r.peran, r.level, r.jenis, r.fading, r.judul, r.pertanyaan, r.diketahui, r.ditanya, r.tabel,
       r.sel_relevan, r.umpan_balik_sel, r.bilangan, r.jawaban, r.kesimpulan, r.pilihan_kesimpulan,
       coalesce(r.petunjuk, '[]'::jsonb), coalesce(r.aktif, true)
from _konten, jsonb_populate_recordset(null::soal, _konten.j -> 'soal') as r
on conflict (id) do update set
  peran = excluded.peran, level = excluded.level, jenis = excluded.jenis, fading = excluded.fading,
  judul = excluded.judul, pertanyaan = excluded.pertanyaan, diketahui = excluded.diketahui,
  ditanya = excluded.ditanya, tabel = excluded.tabel, sel_relevan = excluded.sel_relevan,
  umpan_balik_sel = excluded.umpan_balik_sel, bilangan = excluded.bilangan, jawaban = excluded.jawaban,
  kesimpulan = excluded.kesimpulan, pilihan_kesimpulan = excluded.pilihan_kesimpulan,
  petunjuk = excluded.petunjuk, aktif = excluded.aktif;

commit;
