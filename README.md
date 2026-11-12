# FPB Easy

Aplikasi web untuk belajar **FPB (Faktor Persekutuan Terbesar)** bagi siswa SMP. Aplikasi ini dirancang untuk **mengurangi beban kognitif** dan **melatih literasi matematika**, terutama pada soal cerita dan soal tabel.

- **Backend:** Python (Flask) · **Frontend:** JavaScript · **Database:** Supabase · **Hosting:** Vercel
- **Bisa dipasang di HP tanpa Play Store/App Store** (PWA)

Penyusun: Erlina Putri Febriani (2225250136), Pendidikan Matematika, mata kuliah Algoritma dan Pemrograman.

Dokumen perencanaan: [PRD.md](PRD.md) · [DESAIN.md](DESAIN.md) · [RENCANA.md](RENCANA.md) · [CLAUDE.md](CLAUDE.md)

---

## Fitur
| Menu | Isi |
|---|---|
| 📖 Materi | 6 kartu pendek, satu ide per layar |
| 💡 Contoh Soal | Pembahasan muncul satu langkah setiap kali tombol "Lanjut" ditekan, lengkap dengan alasannya |
| ✏️ Latihan | Level 1 langsung → Level 2 cerita → Level 3 tabel. Bantuan berkurang bertahap (A → B → C), dengan petunjuk bertahap dan umpan balik spesifik |
| 🧮 Kalkulator FPB | Menampilkan cara: faktor → faktor persekutuan → FPB. Tetap berfungsi offline |
| 🎯 Uji Diri | 5 soal tanpa petunjuk, lalu nilai dan pembahasan |
| 📲 Pasang Aplikasi | Tombol pasang (Android) dan panduan iPhone |

---

## A. Menjalankan di Laptop (tanpa Supabase pun bisa)

1. **Pasang Python 3.11 atau lebih baru** dari <https://www.python.org/downloads/>.
   Saat instalasi, **centang "Add python.exe to PATH"**.
2. Buka terminal di folder proyek (VS Code → Terminal → New Terminal), lalu jalankan:
   ```bash
   pip install -r requirements-dev.txt
   python api/index.py
   ```
3. Buka **http://localhost:5000** di browser.

Jika `.env` belum diisi, aplikasi berjalan dalam **mode lokal**. Materi dan soal dibaca dari `api/data/konten.json`, dan jawaban siswa hanya disimpan sementara.

**Mencoba dari HP (Wi-Fi yang sama):** cari IP laptop (`ipconfig` → IPv4, misalnya 192.168.1.5), lalu buka `http://192.168.1.5:5000` di HP. Jika tidak bisa dibuka, izinkan Python di Windows Firewall.
> Tombol "Pasang Aplikasi" baru muncul setelah aplikasi online di Vercel, karena pemasangan PWA memerlukan HTTPS.

### Menjalankan test
```bash
pytest                       # test Python: algoritma, logika soal, API
node tests/fpb.test.mjs      # test JavaScript (perlu Node.js 22+), kasusnya sama dengan test Python
```
Tanpa Node.js: jalankan `python -m http.server 8000` di folder proyek, lalu buka `http://localhost:8000/tests/fpb.test.html`.

---

## B. Menyiapkan Supabase (database)

1. Daftar di <https://supabase.com> → **New project** (pilih region Singapore).
2. Buka **SQL Editor** → New query → tempel isi [supabase/schema.sql](supabase/schema.sql) → **Run**.
3. Query baru → tempel isi [supabase/seed.sql](supabase/seed.sql) → **Run**. Langkah ini mengisi materi dan soal.
4. Buka **Project Settings → API**, lalu salin:
   - `Project URL` → `SUPABASE_URL`
   - `service_role` key (bagian *secret*) → `SUPABASE_SERVICE_KEY`
5. Salin `.env.example` menjadi `.env`, isi kedua nilai tersebut, lalu jalankan ulang `python api/index.py`. Terminal akan menampilkan `mode data: supabase`.

> ⚠️ `service_role` key bersifat **rahasia**. Jangan ditulis di kode JavaScript dan jangan diunggah ke GitHub (`.env` sudah otomatis diabaikan Git).

**Mengubah soal:** edit `api/data/konten.json`, jalankan `python scripts/buat_seed_sql.py`, lalu jalankan ulang `supabase/seed.sql` di SQL Editor. Data jawaban siswa tidak terhapus. Soal juga bisa diubah langsung di **Table Editor** Supabase.

**Melihat hasil belajar siswa:** buka Table Editor → tabel `jawaban` dan `hasil_uji` (bisa diunduh sebagai CSV). Contoh query analisis tersedia di bagian bawah `supabase/schema.sql`.

> Proyek Supabase gratis akan **dijeda jika tidak aktif ±7 hari**. Buka dasbornya secara rutin selama masa uji coba.

---

## C. Online-kan di Vercel

1. Unggah proyek ke GitHub (repo baru → upload, atau `git push`).
2. Buka <https://vercel.com> → login dengan GitHub → **Add New → Project** → pilih repo.
3. Framework Preset: **Other**. Pengaturan lain biarkan bawaan (`vercel.json` sudah mengatur semuanya).
4. Buka **Environment Variables** → tambahkan `SUPABASE_URL` dan `SUPABASE_SERVICE_KEY`.
5. Klik **Deploy**. Hasilnya berupa tautan, misalnya `https://fpb-easy.vercel.app`.
6. Periksa dengan membuka `https://<tautan>/api/ping`. Respons harus `{"ok": true, "mode": "supabase"}`.

---

## D. Memasang di HP Siswa (tanpa Play Store/App Store)

| HP | Caranya |
|---|---|
| **Android** | Buka tautan Vercel di **Chrome** → tekan tombol **Pasang** di Beranda, atau menu ⋮ → **Instal aplikasi** |
| **iPhone** | Buka tautan di **Safari** → tombol **Bagikan** (□↑) → **Tambah ke Layar Utama** → Tambah |

Ikon **FPB Easy** akan muncul di layar utama. Panduan bergambar juga tersedia di dalam aplikasi (Beranda → "Cara memasang aplikasi di HP").

**Offline:** Materi, Contoh Soal, dan Kalkulator tetap bisa dipakai tanpa internet setelah pernah dibuka sekali. Latihan dan Uji Diri memerlukan internet karena jawabannya diperiksa oleh server Python. Jawaban yang gagal terkirim akan dikirim ulang otomatis saat internet tersambung lagi.

---

## Struktur Folder
```text
api/            Python (Flask): index.py (API), fpb.py (algoritma), soal.py (pemeriksaan), db.py (Supabase)
api/data/       konten.json: materi & bank soal (sumber mode lokal & seed Supabase)
public/         JavaScript + HTML/CSS: aplikasi PWA (index.html, js/, css/, icons/, manifest, service worker)
supabase/       schema.sql & seed.sql
scripts/        buat_seed_sql.py, buat_ikon.ps1
tests/          pytest + test JavaScript (kasus uji bersama: kasus_fpb.json)
```
