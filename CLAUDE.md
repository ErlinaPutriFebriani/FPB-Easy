# CLAUDE.md: Panduan Proyek "FPB Easy"

File ini berisi pedoman bagi AI (Claude) maupun pengembang saat menulis kode untuk proyek ini. **Baca file ini sebelum mulai coding.**

## 1. Ringkasan Proyek
- **Nama aplikasi:** FPB Easy
- **Pengembang:** Erlina Putri Febriani (2225250136), S1 Pendidikan Matematika, kelas 3B
- **Mata kuliah:** Algoritma dan Pemrograman. Dosen pengampu: Dr. Aan Hendrayana, S.Si., M.Pd.
- **Materi:** FPB (Faktor Persekutuan Terbesar), SMP kelas VII–VIII
- **Tujuan:** membantu siswa belajar FPB dengan **beban kognitif (cognitive load) yang terkendali**, agar kemampuan **literasi matematika** meningkat, terutama pada soal cerita dan soal berbentuk tabel.
- **Bentuk aplikasi:** aplikasi web **PWA** yang dibuka lewat browser HP/laptop dan **dapat di-install ke HP tanpa Play Store/App Store**.
- **Dasar kebutuhan:** wawancara dengan siswa S01 pada 5 November 2026. Kode temuannya adalah K, IL, EL, GL, dan DS. Lihat [PRD.md](PRD.md).

## 2. Dokumen Terkait
| File | Isi |
|---|---|
| [PRD.md](PRD.md) | Kebutuhan produk: masalah, persona, fitur, user story, kriteria penerimaan |
| [DESAIN.md](DESAIN.md) | Desain pedagogis (Cognitive Load Theory + literasi matematika), arsitektur, database, alur, wireframe, gaya visual, contoh konten |
| [RENCANA.md](RENCANA.md) | Tahapan pengerjaan, checklist, rencana uji coba |

## 3. Teknologi (Stack)
| Bagian | Teknologi | Peran |
|---|---|---|
| Frontend | **JavaScript** (vanilla, ES modules) + HTML + CSS | Tampilan, navigasi, interaksi bertahap, PWA |
| Backend | **Python 3 + Flask** | Algoritma FPB utama + API JSON. Berjalan sebagai *Vercel Python Function* |
| Database | **Supabase** (PostgreSQL) | Menyimpan materi, bank soal, jawaban siswa, dan hasil uji diri |
| Hosting | **Vercel** | Menyajikan frontend statis + API Python dengan **HTTPS otomatis** (syarat PWA) |
| PWA | `manifest.json` + `service-worker.js` | Install ke layar utama HP dan bisa dipakai offline |
| Font | Nunito (Google Fonts), cadangan `system-ui, sans-serif` | |

Arsitektur singkat:
```
HP siswa (browser / PWA terpasang)
   │  HTML+CSS+JS (statis, di-cache service worker)
   ▼
Vercel ── /        → file statis di public/
       └─ /api/*   → Python (Flask) di api/index.py
                        │  supabase-py (service role key dari Environment Variables)
                        ▼
                    Supabase (PostgreSQL)
```

## 4. Struktur Folder (rencana)
```
/
├── api/                      # PYTHON (backend, Vercel Function)
│   ├── index.py              # Flask app + semua route /api/*
│   ├── fpb.py                # ALGORITMA FPB (fungsi murni)
│   ├── soal.py               # logika memeriksa jawaban per tahap, petunjuk, pembahasan, nilai uji
│   ├── db.py                 # Supabase (supabase-py) ATAU mode lokal jika env kosong
│   └── data/konten.json      # SUMBER materi & bank soal (mode lokal + bahan seed.sql)
├── public/                   # JAVASCRIPT + HTML/CSS (frontend statis, outputDirectory Vercel)
│   ├── index.html
│   ├── manifest.json
│   ├── service-worker.js
│   ├── icons/                # icon-192, icon-512, icon-maskable-512, apple-touch-icon
│   ├── css/style.css
│   └── js/
│       ├── app.js            # router hash (#/, #/materi, #/contoh, #/latihan/1, #/kalkulator, #/uji, #/pasang)
│       ├── api.js            # fetch ke /api/* + kirim antrean jawaban
│       ├── fpb.js            # cerminan fpb.py (tampilan + kalkulator offline)
│       ├── storage.js        # perangkat_id, kode siswa, progres, antrean jawaban (localStorage)
│       ├── install.js        # beforeinstallprompt + deteksi iPhone/standalone
│       ├── ui.js             # komponen tampilan (chips, tabel, langkah, kepala halaman)
│       └── pages/            # beranda, materi, contoh, latihan, kalkulator, ujiDiri, pasang
├── supabase/
│   ├── schema.sql            # CREATE TABLE + aktifkan RLS + contoh query analisis
│   └── seed.sql              # DIBUAT OTOMATIS dari konten.json (upsert)
├── scripts/
│   ├── buat_seed_sql.py      # konten.json → supabase/seed.sql
│   └── buat_ikon.ps1         # membuat ikon PNG
├── tests/
│   ├── kasus_fpb.json        # kasus uji BERSAMA untuk Python & JavaScript
│   ├── test_fpb.py, test_soal.py, test_api.py   # pytest (selalu mode lokal)
│   ├── fpb.test.mjs          # node tests/fpb.test.mjs
│   └── fpb.test.html         # uji fpb.js di browser
├── requirements.txt          # dipasang Vercel: flask, supabase, python-dotenv
├── requirements-dev.txt      # + pytest (untuk laptop)
├── vercel.json               # outputDirectory public, rewrite /api/(.*) → /api/index
├── .env.example              # SUPABASE_URL=, SUPABASE_SERVICE_KEY=
└── .gitignore, .vercelignore
```

## 5. API (Python/Flask)
| Method & path | Fungsi |
|---|---|
| `GET /api/fpb?bil=20,28` | Hasil FPB beserta langkah-langkahnya (dihitung oleh `fpb.py`) |
| `GET /api/materi` | Daftar kartu materi, terurut |
| `GET /api/soal?level=1&jenis=tabel` | Soal latihan (tanpa kunci jawaban) |
| `GET /api/uji` | 5 soal acak campuran untuk Uji Diri |
| `POST /api/periksa` | Memeriksa jawaban/sel yang dipilih, mengembalikan `benar` + umpan balik/petunjuk |
| `POST /api/hasil` | Menyimpan jawaban/skor ke Supabase (bisa menerima beberapa sekaligus dari antrean offline) |

## 6. Aturan Coding
1. **Algoritma utama ditulis di Python** (`api/fpb.py`), berupa fungsi murni tanpa Flask/DB:
   - `faktor(n)` → list faktor n, terurut naik
   - `faktor_persekutuan(*bil)` → faktor yang sama dari semua bilangan
   - `fpb(*bil)` → nilai terbesar dari faktor persekutuan
   - `langkah_fpb(*bil)` → list langkah `{judul, isi, alasan}` untuk ditampilkan bertahap
2. `public/js/fpb.js` adalah **cerminan** fungsi yang sama (`faktor`, `faktorPersekutuan`, `fpb`, `langkahFPB`) dan hanya dipakai saat offline. Setiap perubahan di `fpb.py` **wajib** disalin ke `fpb.js`, dan keduanya diuji dengan kasus yang sama.
3. **Kunci jawaban tidak dikirim ke browser** saat latihan atau uji diri (lihat `KOLOM_PUBLIK` di `soal.py`). Pemeriksaan dilakukan di `/api/periksa`. Karena itu Latihan dan Uji Diri memerlukan internet. Materi, Contoh, dan Kalkulator tetap bisa dipakai offline.
4. **Konten ada di database**, tidak di-hardcode di JS. Sumbernya `api/data/konten.json`. Setelah mengubahnya, jalankan `python scripts/buat_seed_sql.py` dan `pytest` (test memeriksa konsistensi kunci jawaban, sel tabel, dan pilihan kesimpulan).
5. **Keamanan Supabase:** hanya backend Python yang mengakses database memakai `SUPABASE_SERVICE_KEY` dari Environment Variables. Kunci **tidak pernah** ditulis di kode JS, tidak di-commit, dan RLS tetap aktif.
6. **Validasi input:** bilangan bulat 1–1000, 2–3 bilangan. Validasi dilakukan di JS (umpan balik cepat) **dan** di Python (keamanan). Pesan ditulis ramah, misalnya "Masukkan bilangan bulat positif, ya".
7. **Bahasa UI:** Bahasa Indonesia sederhana, menyapa dengan "kamu", kalimat pendek.
8. **Aksesibilitas:** font isi ≥ 18px, tombol ≥ 44×44px, kontras ≥ 4.5:1, mobile-first (lebar 360px).
9. **Penamaan:** Python memakai `snake_case`, JavaScript memakai `camelCase`. Keduanya boleh berbahasa Indonesia.
10. Setiap fitur baru harus bisa ditelusuri ke kebutuhan di PRD.md (kode wawancara).

## 7. Prinsip Beban Kognitif (WAJIB di setiap layar)
Ringkasan dari [DESAIN.md](DESAIN.md). Periksa daftar ini sebelum menyelesaikan sebuah fitur:
- [ ] **Satu ide per layar.** Jangan menumpuk teks (EL03).
- [ ] **Maksimal 2–3 tombol aksi** per layar, ditambah tombol kembali (DS03).
- [ ] **Siswa yang mengatur tempo.** Langkah baru muncul hanya setelah siswa menekan "Lanjut". Tidak ada auto-play (EL04).
- [ ] **Setiap langkah menyertakan alasan**, yaitu "dari mana angka ini berasal" (GL02).
- [ ] **Signaling:** faktor persekutuan diberi warna penanda yang sama di semua daftar.
- [ ] **Tanpa split-attention:** soal, tabel, dan isian jawaban berada dalam satu layar yang berdekatan.
- [ ] **Tanpa dekorasi atau animasi yang tidak membantu belajar.**
- [ ] **Urutan sederhana → kompleks:** soal langsung → soal cerita → soal tabel.
- [ ] **Fading:** contoh lengkap → sebagian langkah dikosongkan → mandiri.
- [ ] **Umpan balik segera dan spesifik**, dengan petunjuk bertahap, bukan langsung memberi jawaban.
- [ ] **Loading tidak mengganggu:** saat menunggu API, tampilkan indikator kecil dan jangan kosongkan soal.

## 8. Instalasi di Smartphone tanpa Play Store/App Store
Aplikasi ini adalah **PWA**. Siswa cukup membuka tautan Vercel (misalnya `https://fpb-easy.vercel.app`) lalu memasangnya dari browser:

| Perangkat | Cara memasang |
|---|---|
| **Android (Chrome)** | Tekan tombol **"Pasang Aplikasi"** di dalam aplikasi, atau menu ⋮ → **"Instal aplikasi" / "Tambahkan ke layar utama"** |
| **iPhone (Safari)** | Tombol **Bagikan** (□↑) → **"Tambah ke Layar Utama"** → Tambah. iOS tidak menampilkan tombol instal otomatis, jadi aplikasi menampilkan panduan bergambar di halaman `#/pasang` |
| **Laptop (Chrome/Edge)** | Ikon instal (⊕) di bilah alamat |

Setelah terpasang, aplikasi muncul sebagai ikon di layar utama dan terbuka layar penuh, tanpa bilah alamat browser.

**Syarat teknis PWA (wajib dipenuhi):**
- Disajikan lewat **HTTPS**. Vercel otomatis menyediakannya, dan `localhost` juga dianggap aman saat pengembangan.
- `manifest.json` berisi `name`, `short_name`, `start_url: "/"`, `display: "standalone"`, `theme_color`, `background_color`, serta ikon 192px & 512px (termasuk ikon `maskable`).
- `service-worker.js` disajikan dari **root** (`/service-worker.js`) agar scope-nya mencakup seluruh aplikasi. Isinya menangani `fetch` dan men-cache file statis + `/api/materi` & `/api/soal`.
- iPhone: tambahkan `<link rel="apple-touch-icon">` dan `<meta name="apple-mobile-web-app-capable" content="yes">`.

## 9. Database Supabase
Tabel (detail kolom di [DESAIN.md](DESAIN.md#8-rancangan-database-supabase)):
- `materi`: kartu materi
- `soal`: bank soal (langsung, cerita, tabel), dapat diedit dari dasbor Supabase
- `jawaban`: setiap jawaban latihan (anonim, memakai `perangkat_id`)
- `hasil_uji`: skor Uji Diri

Privasi: **tidak ada nama, email, atau login.** `perangkat_id` adalah UUID acak yang dibuat di `localStorage`. `kode_siswa` (misalnya S01) bersifat opsional, hanya untuk uji coba penelitian.

Catatan paket gratis Supabase: proyek akan **dijeda jika tidak aktif ±7 hari**. Buka dasbor atau aplikasi secara rutin selama masa uji coba.

## 10. Cara Menjalankan
Panduan lengkap untuk pemula ada di [README.md](README.md).

**Menjalankan secara lokal:**
- `pip install -r requirements-dev.txt` lalu `python api/index.py` → buka `http://localhost:5000`. Flask menyajikan `public/` sekaligus API.
- Tanpa `.env`, aplikasi berjalan dalam **mode lokal** (data dari `api/data/konten.json`, jawaban disimpan di memori). Dengan `.env` berisi kunci Supabase, aplikasi memakai Supabase.
- Uji di HP pada Wi-Fi yang sama: `http://<IP-laptop>:5000`. Instalasi PWA penuh baru bisa dicoba setelah deploy karena butuh HTTPS.
- Alternatif yang paling mirip produksi: `vercel dev` (perlu Node.js + `npm i -g vercel`).

**Pengujian:**
- `pytest`: menguji `fpb.py`, `soal.py`, konsistensi `konten.json`, dan semua endpoint API.
- `node tests/fpb.test.mjs` (atau buka `tests/fpb.test.html` lewat server): menguji `fpb.js` dengan kasus yang sama.
- Chrome DevTools → Lighthouse / tab Application → Manifest harus "Installable".
- Setelah mengubah file di `public/`, naikkan `VERSI` di `service-worker.js` jika daftar file berubah.

**Deploy ke Vercel:**
1. Push proyek ke GitHub.
2. Buka [vercel.com](https://vercel.com) → Add New Project → pilih repo.
3. Isi Environment Variables `SUPABASE_URL` dan `SUPABASE_SERVICE_KEY`.
4. Deploy. Tautan `https://<nama>.vercel.app` siap dibagikan ke siswa.

## 11. Istilah
- **FPB** = Faktor Persekutuan Terbesar
- **Faktor persekutuan** = faktor yang sama dari dua bilangan atau lebih
- **PWA** = Progressive Web App, situs web yang bisa di-install seperti aplikasi
- **Worked example** = contoh soal yang dibahas lengkap langkah demi langkah
- **Fading** = bantuan dikurangi sedikit demi sedikit
- **Scaffold** = bantuan berupa langkah atau pertanyaan penuntun
- **RLS** = Row Level Security, aturan keamanan baris di Supabase
