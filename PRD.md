# PRD: Product Requirements Document
## FPB Easy: Aplikasi Belajar FPB Berbasis Web untuk Siswa SMP

| | |
|---|---|
| Penyusun | Erlina Putri Febriani (2225250136) |
| Versi | 1.0 (MVP) |
| Tanggal | 12 November 2026 |
| Status | Perencanaan, belum coding |
| Teknologi | Python (Flask) + JavaScript · Vercel · Supabase · PWA (bisa di-install tanpa Play Store/App Store) |

---

## 1. Latar Belakang
Wawancara dengan siswa kelas 8 (kode **S01**, 5 November 2026, durasi 25 menit) menunjukkan bahwa siswa **sudah mampu** mengerjakan soal FPB langsung, yaitu dengan mendaftar faktor tiap bilangan lalu mencari faktor yang sama. Namun siswa **mengalami kesulitan** ketika soal disajikan dalam **bentuk tabel** atau **soal cerita panjang**. Siswa bingung menentukan informasi dan angka mana yang harus dipakai.

Kesulitan ini menunjukkan **beban kognitif yang tinggi** pada tahap *memahami dan merumuskan masalah*. Tahap ini merupakan inti dari **literasi matematika**, bukan sekadar kemampuan berhitung.

## 2. Rumusan Masalah
1. Siswa kesulitan menyaring informasi penting dari tabel dan soal cerita (IL04, EL01, EL05).
2. Materi atau penjelasan yang padat dan cepat membebani memori kerja siswa (EL03, EL04).
3. Alat bantu yang ada (misalnya kalkulator) hanya memberi jawaban, tidak menunjukkan proses (DS01).

## 3. Temuan Wawancara → Kebutuhan
| Kode | Kutipan inti siswa | Kebutuhan aplikasi |
|---|---|---|
| K01, IL03 | "Sudah paham perkalian dan faktor bilangan" | Materi singkat tentang faktor sebagai *pre-training*, bukan materi panjang |
| K02 | Guru menjelaskan, memberi contoh, lalu latihan | Alur aplikasi mengikuti pola yang sudah dikenal: Materi → Contoh → Latihan |
| IL02 | "Menuliskan faktor masing-masing dulu, lalu cari angka yang sama" | Metode utama = **daftar faktor** |
| K03, IL04, EL01 | "Bingung kalau soalnya berbentuk tabel... informasi mana yang harus digunakan" | **Latihan soal tabel** dengan langkah "pilih informasi penting" |
| IL05, EL05 | "Soal cerita terlalu panjang, bingung angka mana yang dipakai" | Scaffold **Diketahui → Ditanya → Hitung → Simpulkan** |
| EL02 | "Membaca soal beberapa kali" | Soal tetap terlihat (tidak hilang) selama siswa mengerjakan |
| EL03 | "Jangan terlalu banyak tulisan dalam satu halaman" | **Satu ide per layar**, teks ringkas |
| EL04 | "Guru menjelaskan terlalu cepat" | Langkah muncul **saat siswa menekan "Lanjut"** |
| GL01, GL02 | "Lebih mudah kalau ada contoh soal... tahu dari mana angka berasal" | **Contoh bertahap** dengan alasan di setiap langkah |
| GL03 | "Melihat kembali catatan atau contoh soal" | Materi & contoh bisa dibuka ulang kapan saja |
| GL04 | "Pernah membantu teman menjelaskan" | Prompt *self-explanation*: "Jelaskan dengan katamu sendiri" |
| GL05 | "Mencoba soal lain tanpa melihat contoh" | Mode **Uji Diri** tanpa petunjuk |
| DS01 | "Ada materi, contoh, latihan... bukan cuma kalkulator" | 4 menu: Materi, Contoh, Latihan, Kalkulator bercara |
| DS02 | "Penjelasan bertahap dari awal sampai akhir" | Pembahasan langkah demi langkah |
| DS03 | "Tampilan sederhana, tombol tidak banyak, tulisan mudah dibaca, ada latihan tabel" | UI minimalis, font besar, latihan tabel |

## 4. Tujuan & Indikator Keberhasilan
| Tujuan | Indikator |
|---|---|
| Siswa memahami konsep faktor, faktor persekutuan, dan FPB | ≥ 80% jawaban benar pada latihan soal langsung |
| Siswa mampu menyaring informasi dari tabel & soal cerita | Siswa memilih sel/informasi yang relevan dengan benar pada ≥ 75% soal tabel |
| Siswa mampu mengerjakan secara mandiri | Skor Uji Diri ≥ 75% |
| Beban kognitif terasa ringan | Siswa menyatakan tampilan "mudah dipahami" saat wawancara uji coba. Opsional: angket beban kognitif sederhana (skala 1–9, Paas) |
| Aplikasi mudah dipakai | Siswa dapat membuka setiap menu tanpa bantuan dalam ≤ 1 menit |

## 5. Pengguna (Persona)
**"Sipa", siswi kelas 8 SMP**
- Belajar FPB di kelas 7 dan memiliki buku catatan berisi contoh soal.
- Paham perkalian dan cara mendaftar faktor.
- Kesulitan memahami soal tabel dan soal cerita panjang. Ia sering membaca ulang soal.
- Memakai HP Android dengan layar kecil. Kadang belajar di rumah tanpa kuota.
- Suka penjelasan yang sederhana dan bertahap, dan suka mencoba sendiri setelah melihat contoh.

Pengguna sekunder: **guru/mahasiswa** yang memakai aplikasi sebagai media pembelajaran di kelas.

## 6. Ruang Lingkup MVP (Fitur)

### F1. Beranda
- Menampilkan 5 tombol besar: **Materi, Contoh Soal, Latihan, Kalkulator FPB, Uji Diri**.
- Menampilkan progres singkat, misalnya "Latihan selesai 4/12".

### F2. Materi (kartu bertahap)
- 5–6 kartu pendek yang dibuka satu per satu:
  1. Mengingat perkalian & faktor (pre-training)
  2. Apa itu faktor? (contoh: faktor 12)
  3. Apa itu faktor persekutuan? (contoh: 16 dan 24)
  4. Apa itu FPB?
  5. Langkah mencari FPB (3 langkah)
  6. FPB dalam kehidupan sehari-hari (membagi sama banyak)
- Setiap kartu memuat **satu ide**, maksimal sekitar 40 kata, dan satu contoh visual.
- Navigasi memakai tombol **Kembali / Lanjut** dan indikator titik (●○○○).

### F3. Contoh Soal (worked example bertahap)
- Daftar 3–5 contoh: soal langsung, soal cerita, dan soal tabel.
- Langkah-langkah muncul **satu per satu** ketika siswa menekan "Lanjut".
- Setiap langkah memuat: **apa yang dilakukan** dan **mengapa** (alasan).
- Faktor persekutuan **diwarnai sama** di kedua daftar faktor.
- Di akhir contoh terdapat pertanyaan refleksi singkat, misalnya "Mengapa 8 yang dipilih, bukan 4?", dengan pilihan jawaban.

### F4. Latihan (3 level + fading)
| Level | Jenis soal | Bantuan |
|---|---|---|
| 1 | Soal langsung ("Tentukan FPB dari 20 dan 28") | Isian bertahap: faktor A → faktor B → faktor sama → FPB |
| 2 | Soal cerita | Scaffold: Diketahui → Ditanya → Hitung → Kesimpulan |
| 3 | **Soal tabel** | Langkah 1: ketuk sel tabel yang dibutuhkan. Langkah 2: hitung FPB. Langkah 3: simpulkan dalam konteks |

- **Fading** di setiap level: soal ke-1 sebagian besar langkah sudah terisi, soal ke-2 sebagian langkah kosong, soal ke-3 hanya meminta jawaban akhir.
- **Umpan balik segera:** benar ditandai hijau ✓. Jika salah, muncul petunjuk bertahap (Petunjuk 1 → 2 → 3), lalu pembahasan.
- Soal tetap terlihat di bagian atas layar (sticky) selama siswa mengerjakan.

### F5. Kalkulator FPB (bercara)
- Input 2 atau 3 bilangan bulat (1–1000).
- Output **bertahap**: daftar faktor tiap bilangan → faktor persekutuan (diwarnai) → FPB.
- Opsi "Tampilkan semua langkah" atau "Langkah demi langkah".

### F6. Uji Diri
- 5 soal acak campuran (langsung, cerita, tabel) **tanpa petunjuk**.
- Di akhir: skor, soal yang salah, dan pembahasan bertahap untuk soal tersebut.
- Skor terbaik disimpan di perangkat dan di Supabase (tabel `hasil_uji`).

### F7. Pasang Aplikasi (tanpa Play Store/App Store)
- Aplikasi berbentuk **PWA** dan dapat di-install langsung dari browser HP.
- **Android/Chrome & laptop:** tombol **"Pasang Aplikasi"** muncul di Beranda (memakai event `beforeinstallprompt`). Tombol disembunyikan jika aplikasi sudah terpasang.
- **iPhone/Safari:** halaman panduan `#/pasang` berisi 3 langkah bergambar: Bagikan → Tambah ke Layar Utama → Tambah.
- Setelah terpasang: muncul ikon "FPB Easy" di layar utama, aplikasi terbuka layar penuh, dan bisa dipakai offline untuk konten yang sudah pernah dibuka.

### F8. Penyimpanan Hasil Belajar (Supabase)
- Setiap jawaban latihan disimpan ke tabel `jawaban`: benar/salah, jumlah petunjuk, dan durasi.
- Skor Uji Diri disimpan ke tabel `hasil_uji`.
- Identitas anonim (`perangkat_id` acak). Siswa boleh mengisi **kode siswa** (misalnya S01) untuk keperluan uji coba, tanpa nama asli.
- Jawaban yang dibuat saat offline diantrikan, lalu dikirim otomatis saat online.
- Guru/peneliti melihat dan mengunduh data (CSV) dari dasbor Supabase. Data ini dipakai untuk evaluasi di tahap uji coba.

## 7. User Story & Kriteria Penerimaan
| ID | User story | Kriteria penerimaan |
|---|---|---|
| US1 | Sebagai siswa, aku ingin membaca materi sedikit demi sedikit supaya tidak bingung | Satu kartu per layar. Ada tombol Kembali/Lanjut. Tidak ada kartu > 60 kata |
| US2 | Sebagai siswa, aku ingin melihat contoh soal dibahas satu per satu supaya tahu asal setiap angka | Langkah muncul hanya setelah tombol ditekan. Setiap langkah punya kalimat "karena..." |
| US3 | Sebagai siswa, aku ingin berlatih soal tabel supaya tidak bingung memilih informasi | Siswa bisa mengetuk sel tabel. Pilihan yang salah diberi umpan balik khusus, misalnya "Kolom harga tidak ditanyakan" |
| US4 | Sebagai siswa, aku ingin bantuan yang berkurang perlahan supaya akhirnya bisa mandiri | Setiap level punya 3 tahap fading |
| US5 | Sebagai siswa, aku ingin kalkulator yang menunjukkan caranya | Kalkulator menampilkan daftar faktor, faktor persekutuan, dan FPB, bukan angka FPB saja |
| US6 | Sebagai siswa, aku ingin menguji diri tanpa contoh | Uji Diri tidak menampilkan petunjuk sebelum semua soal dijawab |
| US7 | Sebagai siswa, aku ingin belajar lewat HP walau tanpa internet | Setelah dibuka sekali, Materi, Contoh Soal, dan Kalkulator tetap berjalan dalam mode pesawat. Latihan dan Uji Diri menampilkan pesan ramah bahwa internet diperlukan (jawaban diperiksa server). Jawaban yang gagal terkirim akan dikirim ulang saat online |
| US8 | Sebagai siswa, aku ingin progresku tersimpan | Progres tetap ada setelah aplikasi ditutup dan dibuka lagi (`localStorage`) dan tercatat di Supabase |
| US9 | Sebagai siswa, aku ingin memasang aplikasi di HP tanpa lewat Play Store/App Store | Dari tautan Vercel, aplikasi bisa di-install di Android (tombol "Pasang Aplikasi") dan iPhone (panduan "Tambah ke Layar Utama"). Ikon muncul di layar utama dan aplikasi terbuka tanpa bilah alamat |
| US10 | Sebagai guru/peneliti, aku ingin melihat hasil belajar siswa | Data jawaban dan skor bisa dilihat dan diunduh dari dasbor Supabase tanpa memuat data pribadi |

## 8. Kebutuhan Non-Fungsional
- **Teknologi:** backend **Python (Flask)**, frontend **JavaScript**, database **Supabase**, hosting **Vercel**.
- **Akses & instalasi:** dibuka lewat browser HP/laptop dengan HTTPS. Dapat **di-install sebagai PWA tanpa Play Store/App Store** di Android (Chrome) dan iPhone (Safari).
- **Perangkat:** layar mulai 360px. Diuji di Chrome Android, Safari iPhone, dan Chrome/Edge desktop.
- **Kinerja:** ukuran frontend < 1 MB, halaman pertama tampil < 2 detik di jaringan 3G. Respons API < 1 detik setelah *warm*.
- **Offline:** service worker men-cache file statis, materi, dan soal. Kalkulator memakai cadangan `fpb.js`.
- **Keamanan:** kunci Supabase hanya ada di server (Environment Variables Vercel), RLS aktif, dan kunci jawaban tidak dikirim ke browser saat latihan.
- **Privasi:** tidak meminta nama, email, atau login. Data di Supabase bersifat anonim (`perangkat_id` acak + kode siswa opsional).
- **Aksesibilitas:** font ≥ 18px, kontras cukup, tombol ≥ 44px.
- **Bahasa:** Bahasa Indonesia baku tetapi santai.

## 9. Di Luar Ruang Lingkup MVP (pengembangan lanjutan)
- Materi KPK dan hubungan FPB–KPK
- Metode faktorisasi prima / pohon faktor (bisa jadi materi pengayaan)
- Login, akun siswa, dasbor guru, leaderboard
- Mode suara (text-to-speech)

## 10. Asumsi & Risiko
| Risiko | Mitigasi |
|---|---|
| Data kebutuhan hanya berasal dari 1 siswa | Uji coba ke beberapa siswa lain di tahap 7 (RENCANA.md) |
| Siswa menebak jawaban tanpa berpikir | Petunjuk bertahap. Pembahasan baru muncul setelah 2–3 percobaan |
| Soal tabel terlalu sulit | Mulai dari tabel kecil (2 kolom relevan + 1 kolom pengecoh) |
| iPhone tidak menampilkan tombol instal otomatis | Halaman panduan `#/pasang` bergambar. Demonstrasikan langsung saat uji coba |
| *Cold start* Vercel (API pertama lambat ±1–3 detik) | Tampilkan indikator memuat. Materi & soal di-cache service worker |
| Proyek Supabase gratis dijeda jika tidak aktif ±7 hari | Buka dasbor secara rutin selama uji coba. Aplikasi tetap bisa memakai data yang di-cache |
| Kunci Supabase bocor | Kunci hanya di Environment Variables, `.env` di `.gitignore`, RLS aktif |
