# RENCANA.md: Tahapan Pengerjaan "FPB Easy"

Stack: **Python (Flask) + JavaScript**, hosting **Vercel**, database **Supabase**, berbentuk **PWA** (bisa di-install tanpa Play Store/App Store).
Setiap tahap diakhiri dengan pengecekan di layar HP (lebar 360px) dan checklist beban kognitif di [CLAUDE.md](CLAUDE.md#7-prinsip-beban-kognitif-wajib-di-setiap-layar).

Keterangan: [x] = kode sudah dibuat · [ ] = belum / perlu dilakukan Erlina

## Tahap 1: Kerangka Flask + Vercel + PWA
- [x] `requirements.txt`, `requirements-dev.txt`, `vercel.json`, `.gitignore`, `.vercelignore`, `.env.example`
- [x] `api/index.py`: Flask app + `GET /api/ping` (menyajikan `public/` saat dijalankan di laptop)
- [x] `public/index.html`, `css/style.css`
- [x] `public/js/app.js`: router hash + Beranda dengan 5 menu
- [x] `manifest.json`, ikon 192/512/maskable/apple, `service-worker.js`
- [ ] Repo GitHub + deploy pertama ke Vercel

**Selesai jika:** tautan Vercel dapat dibuka di HP, `/api/ping` merespons, dan Lighthouse menyatakan aplikasi "Installable".

## Tahap 2: Database Supabase
- [x] `supabase/schema.sql`: tabel `materi`, `soal`, `jawaban`, `hasil_uji` + RLS
- [x] `api/data/konten.json`: 6 kartu materi, 3 contoh, 9 soal latihan (3 level × fading A/B/C), 4 soal khusus uji
- [x] `supabase/seed.sql` (dibuat dari konten.json oleh `scripts/buat_seed_sql.py`)
- [x] `api/db.py`: Supabase jika env diisi, mode lokal jika kosong
- [ ] Buat proyek Supabase, jalankan schema.sql + seed.sql
- [ ] Isi Environment Variables di `.env` (laptop) dan di Vercel

**Selesai jika:** `GET /api/ping` mengembalikan `"mode": "supabase"`.

## Tahap 3: Algoritma FPB (Python) + Kalkulator
- [x] `api/fpb.py`: `faktor()`, `faktor_persekutuan()`, `fpb()`, `langkah_fpb()`, `validasi()`
- [x] `tests/test_fpb.py` + `tests/kasus_fpb.json` (kasus bersama Python & JS)
- [x] `GET /api/fpb` + `tests/test_api.py`
- [x] `public/js/fpb.js` (cerminan) + `tests/fpb.test.mjs` / `tests/fpb.test.html`
- [x] Halaman Kalkulator: 2–3 bilangan, langkah bertahap / semua, pewarnaan, cadangan offline
- [ ] Jalankan `pytest` dan `node tests/fpb.test.mjs`, pastikan semua lulus

## Tahap 4: Materi
- [x] Halaman Materi dari `/api/materi`: satu kartu per layar, Kembali/Lanjut, indikator titik, contoh visual
- [x] Respons di-cache service worker (bisa dibuka offline)

## Tahap 5: Contoh Soal Bertahap
- [x] Contoh langsung, cerita, tabel (`/api/contoh`)
- [x] Langkah muncul satu per satu dengan "Lanjut". Setiap langkah memuat alasan
- [x] Pertanyaan refleksi "Mengapa X dipilih sebagai FPB?"

## Tahap 6: Latihan
- [x] `POST /api/periksa` + `api/soal.py` (cek per tahap, umpan balik spesifik, sel pengecoh)
- [x] Level 1 (langsung), Level 2 (cerita: pilih angka → ditanya → hitung → kesimpulan), Level 3 (tabel: ketuk sel → ...)
- [x] Fading A (faktor sudah ada) → B (tulis faktor + ketuk faktor sama) → C (mandiri)
- [x] Petunjuk bertahap 1 → 2 → 3 → pembahasan
- [x] Soal tetap terlihat (sticky) saat mengerjakan
- [x] `POST /api/hasil` + antrean `localStorage` yang dikirim ulang saat online

## Tahap 7: Uji Diri + Progres
- [x] `GET /api/uji` (2 langsung, 1 cerita, 2 tabel, acak) + `POST /api/uji/nilai` (simpan ke `hasil_uji`)
- [x] Skor + pembahasan per soal
- [x] `storage.js`: `perangkat_id`, kode siswa opsional, progres, skor terbaik
- [x] Progres tampil di Beranda

## Tahap 8: Instalasi & Offline
- [x] `install.js` + banner "Pasang" di Beranda (Android/desktop)
- [x] Halaman `#/pasang`: panduan Android & iPhone, satu langkah per layar
- [ ] Uji instal nyata di **HP Android (Chrome)** dan **iPhone (Safari)** dari tautan Vercel
- [ ] Uji offline: buka aplikasi terpasang dalam mode pesawat (Materi, Contoh, Kalkulator)
- [ ] Periksa ikon, nama, dan warna splash screen

## Tahap 9: Uji Coba Siswa & Evaluasi
- [ ] Bagikan tautan ke siswa S01 dan, jika memungkinkan, 2–4 siswa lain. Pandu mereka memasang aplikasi dan mengisi kode siswa
- [ ] Observasi: bagian mana yang membuat siswa berhenti lama atau bingung
- [ ] Wawancara singkat setelah pemakaian (tampilan, kemudahan, soal tabel)
- [ ] Analisis data Supabase (query contoh ada di `supabase/schema.sql`): persentase benar per level, petunjuk yang dipakai, durasi, skor Uji Diri
- [ ] Opsional: angket beban kognitif (skala Paas 1–9) dan perbandingan sebelum/sesudah pada soal tabel
- [ ] Revisi aplikasi berdasarkan temuan

## Tahap 10: Dokumentasi
- [x] `README.md`: cara menjalankan, Supabase, Vercel, cara memasang di HP
- [ ] Tambahkan tautan aplikasi + tangkapan layar ke README
- [ ] Laporan akhir untuk mata kuliah
