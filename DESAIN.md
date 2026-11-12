# DESAIN.md: Desain Pedagogis & Tampilan "FPB Easy"

## 1. Landasan Teori

### 1.1 Cognitive Load Theory (Sweller)
Memori kerja manusia terbatas. Beban kognitif terdiri dari tiga jenis:

| Jenis beban | Arti | Strategi di aplikasi | Dasar wawancara |
|---|---|---|---|
| **Intrinsik** | Kesulitan bawaan materi | **Segmenting:** materi dipecah per kartu. **Pre-training:** ulang faktor & perkalian dulu. **Urutan:** langsung → cerita → tabel | IL03, IL05 |
| **Ekstrinsik** (harus *dikurangi*) | Beban dari cara penyajian yang buruk | Satu ide per layar, teks ringkas, tombol sedikit, tanpa dekorasi, soal & isian berdekatan (*split-attention*), soal tetap terlihat | EL01, EL02, EL03, DS03 |
| **Germane** (harus *diarahkan*) | Usaha membangun pemahaman | *Worked example* → *completion problem* (fading) → mandiri. *Self-explanation*. Alasan pada setiap langkah | GL01, GL02, GL04, GL05 |

Prinsip tambahan:
- **Self-pacing:** siswa sendiri yang menekan "Lanjut" (menjawab EL04).
- **Signaling:** faktor persekutuan diberi warna penanda yang sama.
- **Redundancy:** tidak mengulang informasi yang sama dalam teks dan gambar sekaligus.
- **Expertise reversal:** bantuan dikurangi saat siswa sudah mahir (fading), supaya bantuan tidak malah membebani.

### 1.2 Literasi Matematika (kerangka PISA)
Literasi matematika adalah kemampuan **merumuskan, menerapkan, dan menafsirkan** matematika dalam berbagai konteks. Kesulitan S01 ada di tahap **merumuskan**, yaitu memilih informasi dari tabel atau cerita.

| Proses PISA | Pertanyaan penuntun di aplikasi | Bentuk interaksi |
|---|---|---|
| **Merumuskan** (Formulate) | "Apa yang diketahui?" "Apa yang ditanya?" "Informasi mana yang dipakai?" | Ketuk sel tabel / pilih angka dari cerita |
| **Menerapkan** (Employ) | "Tulis faktor-faktornya." "Mana faktor yang sama?" | Isian faktor, pilih faktor persekutuan |
| **Menafsirkan** (Interpret) | "Jadi, apa artinya dalam soal?" | Pilih kalimat kesimpulan yang benar, misalnya "Paling banyak 12 kantong" |

## 2. Alur Belajar
```
Beranda
  ├─ Materi ──────► Kartu 1 ► Kartu 2 ► ... ► Kartu 6 ► [Lihat Contoh]
  ├─ Contoh Soal ─► Pilih contoh ► Langkah 1 ► Langkah 2 ► ... ► Refleksi ► [Coba Latihan]
  ├─ Latihan ─────► Level 1 (langsung) ► Level 2 (cerita) ► Level 3 (tabel)
  │                   tiap level: Soal A (dibantu penuh) ► Soal B (sebagian) ► Soal C (mandiri)
  ├─ Kalkulator ──► Input ► Langkah bertahap ► Hasil
  ├─ Uji Diri ────► 5 soal tanpa petunjuk ► Skor ► Pembahasan soal yang salah
  └─ Pasang Aplikasi (banner kecil, hanya jika belum terpasang) ► prompt instal / panduan iPhone
```
Urutan yang disarankan (namun tidak dikunci): **Materi → Contoh → Latihan → Uji Diri**. Pola ini sesuai dengan cara belajar siswa di kelas (K02).

## 3. Wireframe (layar HP 360px)

### 3.1 Beranda
```
┌──────────────────────────────┐
│  FPB Easy                     │
│  Belajar FPB pelan-pelan 🙂   │
├──────────────────────────────┤
│  ┌────────────────────────┐  │
│  │ 📖  Materi             │  │
│  └────────────────────────┘  │
│  ┌────────────────────────┐  │
│  │ 💡  Contoh Soal        │  │
│  └────────────────────────┘  │
│  ┌────────────────────────┐  │
│  │ ✏️  Latihan    4/12    │  │
│  └────────────────────────┘  │
│  ┌────────────────────────┐  │
│  │ 🧮  Kalkulator FPB     │  │
│  └────────────────────────┘  │
│  ┌────────────────────────┐  │
│  │ 🎯  Uji Diri           │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```

### 3.2 Kartu Materi
```
┌──────────────────────────────┐
│ ←  Materi            3 / 6    │
├──────────────────────────────┤
│  Faktor Persekutuan           │
│                               │
│  Faktor yang SAMA dari dua    │
│  bilangan.                    │
│                               │
│  16 → 1, 2, 4, 8, 16          │
│  24 → 1, 2, 3, 4, 6, 8, 12, 24│
│       (1, 2, 4, 8 diwarnai)   │
│                               │
│  Faktor persekutuan:          │
│  1, 2, 4, 8                   │
│           ● ● ● ○ ○ ○         │
│  [ Kembali ]     [ Lanjut ]   │
└──────────────────────────────┘
```

### 3.3 Contoh Soal Bertahap
```
┌──────────────────────────────┐
│ ←  Contoh 1                   │
├──────────────────────────────┤
│ Tentukan FPB dari 18 dan 27.  │  ← soal selalu terlihat
├──────────────────────────────┤
│ Langkah 1 ✓                   │
│ Faktor 18: 1, 2, 3, 6, 9, 18  │
│ Karena 18 = 1×18 = 2×9 = 3×6  │
│                               │
│ Langkah 2 ✓                   │
│ Faktor 27: 1, 3, 9, 27        │
│ Karena 27 = 1×27 = 3×9        │
│                               │
│ (Langkah 3 belum muncul)      │
│                               │
│            [ Lanjut ▸ ]       │
└──────────────────────────────┘
```

### 3.4 Latihan Soal Tabel (Level 3)
```
┌──────────────────────────────┐
│ ←  Latihan Tabel      1 / 3   │
├──────────────────────────────┤
│ Bu Rina ingin membuat paket   │
│ alat tulis dari PENSIL dan    │
│ BUKU. Setiap paket isinya     │
│ sama. Berapa paket terbanyak? │
│ ┌─────────┬───────┬────────┐ │
│ │ Barang  │ Jumlah│ Harga  │ │
│ ├─────────┼───────┼────────┤ │
│ │ Pensil  │  48   │ 2.000  │ │
│ │ Buku    │  36   │ 5.000  │ │
│ │ Penghapus│ 60   │ 1.000  │ │
│ └─────────┴───────┴────────┘ │
│ Langkah 1: Ketuk angka yang   │
│ kamu butuhkan.                │
│                               │
│ [ Petunjuk ]    [ Periksa ]   │
└──────────────────────────────┘
```
Umpan balik jika siswa mengetuk sel yang salah:
- Mengetuk **harga** → "Soal menanyakan jumlah paket, bukan harga. Coba lihat kolom Jumlah."
- Mengetuk **penghapus** → "Penghapus tidak dimasukkan ke paket. Baca lagi barang apa saja yang disebut."

### 3.5 Kalkulator FPB
```
┌──────────────────────────────┐
│ ←  Kalkulator FPB             │
├──────────────────────────────┤
│  Bilangan 1: [ 20 ]           │
│  Bilangan 2: [ 28 ]           │
│  + tambah bilangan            │
│         [ Hitung ]            │
├──────────────────────────────┤
│ 1) Faktor 20: 1,2,4,5,10,20   │
│ 2) Faktor 28: 1,2,4,7,14,28   │
│ 3) Faktor sama: 1, 2, 4       │
│ 4) FPB = 4 (terbesar)         │
└──────────────────────────────┘
```

### 3.6 Hasil Uji Diri
```
┌──────────────────────────────┐
│  Hasil Uji Diri               │
│        4 / 5  🎉              │
│  Hebat! Kamu hampir sempurna. │
├──────────────────────────────┤
│  Soal 3 (tabel) ✗             │
│  [ Lihat pembahasan ]         │
├──────────────────────────────┤
│ [ Ulangi ]      [ Beranda ]   │
└──────────────────────────────┘
```

## 4. Pola Interaksi

### 4.1 Fading di setiap level latihan
| Soal | Langkah yang sudah terisi | Yang dikerjakan siswa |
|---|---|---|
| A | Faktor A, faktor B, faktor persekutuan | Memilih FPB |
| B | Faktor A | Faktor B, faktor persekutuan, FPB |
| C | (tidak ada) | Jawaban akhir saja (dengan langkah opsional) |

### 4.2 Umpan balik & petunjuk bertahap
1. Jawaban salah → pesan singkat yang spesifik, misalnya "Hampir! Coba periksa lagi apakah 6 adalah faktor 28."
2. Petunjuk 1 → pengingat konsep ("Faktor adalah bilangan yang membagi habis").
3. Petunjuk 2 → langkah separuh jalan ("Faktor 28: 1, 2, 4, __, 14, 28").
4. Petunjuk 3 → pembahasan lengkap bertahap.
- Gunakan bahasa yang menyemangati dan tidak menghakimi. Hindari kata "Salah!" yang besar dan berwarna merah menyala.

### 4.3 Scaffold soal cerita
```
Diketahui : [pilih angka dari cerita]
Ditanya   : [pilih: FPB / KPK / jumlah biasa]
Hitung    : faktor... → faktor sama... → FPB = ...
Kesimpulan: [pilih kalimat yang sesuai konteks]
```
Angka penting dalam cerita **tidak** disorot otomatis di level awal. Siswa yang mengetuknya, supaya latihan memilih informasi tetap terjadi. Sorotan otomatis baru muncul sebagai Petunjuk 1.

## 5. Sistem Visual
| Elemen | Nilai |
|---|---|
| Warna utama | Biru tenang `#2F6FDB` |
| Latar | Putih `#FFFFFF` / abu sangat muda `#F6F8FB` |
| Teks | Abu gelap `#1F2937` |
| **Penanda faktor persekutuan** | Oranye `#F59E0B` (latar lembut `#FEF3C7`) |
| Benar | Hijau `#16A34A` |
| Perlu diperbaiki | Merah lembut `#DC2626` (hanya di garis tepi/ikon) |
| Font | Nunito. Judul 24px, isi 18–20px, angka 22px tebal |
| Jarak | Kelipatan 8px. Padding kartu 16–24px |
| Tombol | Tinggi ≥ 48px, sudut membulat 12px, maksimal 2–3 per layar |
| Ikon | Emoji/ikon sederhana, hanya di menu Beranda |
| Animasi | Hanya transisi halus (≤ 200ms) saat langkah baru muncul |
| Mode gelap | Opsional (setelah MVP) |

## 6. Contoh Konten (isi awal tabel `soal` di Supabase, lewat `supabase/seed.sql`)

### Soal langsung (diambil dari catatan siswa & latihan wawancara)
| Soal | Faktor | Faktor persekutuan | FPB |
|---|---|---|---|
| 16 dan 24 | 16: 1,2,4,8,16 · 24: 1,2,3,4,6,8,12,24 | 1,2,4,8 | **8** |
| 18 dan 27 | 18: 1,2,3,6,9,18 · 27: 1,3,9,27 | 1,3,9 | **9** |
| 20 dan 28 | 20: 1,2,4,5,10,20 · 28: 1,2,4,7,14,28 | 1,2,4 | **4** |

### Soal cerita
> Ibu memiliki 24 apel dan 36 jeruk. Buah-buahan itu akan dimasukkan ke dalam kantong. Setiap kantong berisi apel dan jeruk dengan jumlah yang sama banyak. Berapa kantong paling banyak yang bisa dibuat?

Jawaban: FPB(24, 36) = **12 kantong**. Setiap kantong berisi 2 apel dan 3 jeruk.

### Soal tabel
| Barang | Jumlah | Harga satuan |
|---|---|---|
| Pensil | 48 | Rp2.000 |
| Buku | 36 | Rp5.000 |
| Penghapus | 60 | Rp1.000 |

> Bu Rina membuat paket berisi **pensil dan buku** dengan isi tiap paket sama. Berapa paket terbanyak?

Jawaban: FPB(48, 36) = **12 paket**. Setiap paket berisi 4 pensil dan 3 buku. Kolom harga dan baris penghapus sengaja menjadi **pengecoh**, untuk melatih kemampuan menyaring informasi (IL04).

### Format satu baris tabel `soal` di Supabase
```json
{
  "id": "tabel-01",
  "level": 3,
  "jenis": "tabel",
  "fading": "A",
  "pertanyaan": "Bu Rina membuat paket berisi pensil dan buku...",
  "tabel": {
    "kolom": ["Barang", "Jumlah", "Harga"],
    "baris": [["Pensil", 48, 2000], ["Buku", 36, 5000], ["Penghapus", 60, 1000]]
  },
  "sel_relevan": [[0, 1], [1, 1]],
  "umpan_balik_sel": {
    "2": "Soal menanyakan jumlah paket, bukan harga. Coba lihat kolom Jumlah.",
    "baris:2": "Penghapus tidak dimasukkan ke paket. Baca lagi barang apa saja yang disebut."
  },
  "bilangan": [48, 36],
  "jawaban": 12,
  "kesimpulan": "Paling banyak 12 paket, tiap paket 4 pensil dan 3 buku.",
  "petunjuk": ["Barang apa saja yang masuk paket?", "Lihat kolom Jumlah untuk pensil dan buku.", "Cari FPB dari 48 dan 36."]
}
```
Saat dikirim ke browser lewat `GET /api/soal`, kolom `jawaban`, `sel_relevan`, `kesimpulan`, dan `petunjuk` **tidak disertakan**. Pemeriksaan dilakukan oleh Python di `POST /api/periksa`.

## 7. Arsitektur Teknis

### 7.1 Gambaran umum
```
┌──────────────────────┐        HTTPS        ┌──────────────────────────────┐
│ HP siswa             │ ──────────────────► │ VERCEL                       │
│ Browser / PWA        │                     │  /        → public/ (JS,HTML)│
│  - JavaScript (UI)   │ ◄────────────────── │  /api/*   → Python (Flask)   │
│  - service worker    │      JSON           │             api/index.py     │
│  - localStorage      │                     └──────────────┬───────────────┘
└──────────────────────┘                                    │ supabase-py
                                                            ▼ (service role key)
                                             ┌──────────────────────────────┐
                                             │ SUPABASE (PostgreSQL)        │
                                             │ materi · soal · jawaban ·    │
                                             │ hasil_uji   (RLS aktif)      │
                                             └──────────────────────────────┘
```
Pembagian peran bahasa:
- **Python:** algoritma FPB (`fpb.py`), pemeriksaan jawaban & pemilihan petunjuk (`soal.py`), serta akses database (`db.py`).
- **JavaScript:** semua tampilan dan interaksi, PWA (service worker, instalasi), penyimpanan lokal, dan cadangan kalkulator offline (`fpb.js`).

### 7.2 Contoh respons `GET /api/fpb?bil=20,28`
```json
{
  "bilangan": [20, 28],
  "langkah": [
    {"judul": "Faktor 20", "isi": [1, 2, 4, 5, 10, 20], "alasan": "20 = 1×20 = 2×10 = 4×5"},
    {"judul": "Faktor 28", "isi": [1, 2, 4, 7, 14, 28], "alasan": "28 = 1×28 = 2×14 = 4×7"},
    {"judul": "Faktor persekutuan", "isi": [1, 2, 4], "alasan": "Angka yang ada di kedua daftar"},
    {"judul": "FPB", "isi": [4], "alasan": "4 adalah faktor persekutuan yang paling besar"}
  ],
  "fpb": 4
}
```

### 7.3 Contoh `POST /api/periksa`
Permintaan: `{"soal_id": "tabel-01", "tahap": "pilih_sel", "sel": [[0,1],[0,2]]}`
Respons: `{"benar": false, "pesan": "Soal menanyakan jumlah paket, bukan harga. Coba lihat kolom Jumlah."}`

## 8. Rancangan Database Supabase
| Tabel | Kolom | Keterangan |
|---|---|---|
| `materi` | `id` serial PK, `urutan` int, `judul` text, `isi` text, `contoh` jsonb | 6 kartu materi |
| `soal` | `id` text PK, `level` int (1–3), `jenis` text (langsung/cerita/tabel), `fading` text (A/B/C), `pertanyaan` text, `tabel` jsonb null, `sel_relevan` jsonb null, `umpan_balik_sel` jsonb null, `bilangan` int[], `jawaban` int, `kesimpulan` text, `petunjuk` jsonb, `aktif` bool | Bank soal latihan & contoh, bisa diedit di dasbor |
| `jawaban` | `id` bigserial PK, `perangkat_id` uuid, `kode_siswa` text null, `soal_id` text FK→soal, `jawaban` text, `benar` bool (selesai tanpa salah & tanpa pembahasan), `jumlah_salah` int, `jumlah_petunjuk` int, `durasi_detik` int, `created_at` timestamptz default now() | Satu baris per soal latihan yang diselesaikan |
| `hasil_uji` | `id` bigserial PK, `perangkat_id` uuid, `kode_siswa` text null, `skor` int, `total` int, `rincian` jsonb, `created_at` timestamptz default now() | Satu baris per Uji Diri |

**Keamanan:** `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` di semua tabel, tanpa policy untuk role `anon`/`authenticated`. Hanya backend Python yang memakai *service role key*, sehingga browser tidak bisa membaca kunci jawaban atau data siswa lain.

**Analisis untuk penelitian** (dijalankan di SQL Editor Supabase), contohnya persentase benar per level:
```sql
select s.level, s.jenis, round(avg(j.benar::int)*100) as persen_benar, avg(j.jumlah_petunjuk) as rata_petunjuk
from jawaban j join soal s on s.id = j.soal_id
group by s.level, s.jenis order by s.level;
```

## 9. Instalasi Tanpa Play Store/App Store (PWA)

### 9.1 Banner pasang di Beranda (Android/laptop)
```
┌──────────────────────────────┐
│  FPB Easy                     │
├──────────────────────────────┤
│ 📲 Pasang FPB Easy di HP-mu   │
│    biar mudah dibuka.         │
│   [ Pasang ]   [ Nanti ]      │
├──────────────────────────────┤
│  📖  Materi                   │
│  ...                          │
```
- Muncul hanya jika browser memicu `beforeinstallprompt` dan aplikasi belum terpasang.
- Jika siswa menekan "Nanti", banner disembunyikan selama 7 hari (disimpan di `localStorage`), agar tidak menambah beban ekstrinsik.

### 9.2 Panduan iPhone (`#/pasang`)
```
┌──────────────────────────────┐
│ ←  Pasang di iPhone           │
├──────────────────────────────┤
│ 1. Buka di Safari             │
│ 2. Ketuk tombol Bagikan  □↑   │
│ 3. Pilih "Tambah ke Layar     │
│    Utama", lalu "Tambah"      │
│                               │
│  [gambar ikon FPB Easy        │
│   di layar utama]             │
│                               │
│          [ Mengerti ]         │
└──────────────────────────────┘
```
Ditampilkan satu langkah per layar (sesuai prinsip segmenting), lengkap dengan gambar.

### 9.3 Isi `manifest.json` (rancangan)
```json
{
  "name": "FPB Easy - Belajar FPB",
  "short_name": "FPB Easy",
  "start_url": "/",
  "scope": "/",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#FFFFFF",
  "theme_color": "#2F6FDB",
  "lang": "id",
  "icons": [
    {"src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png"},
    {"src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png"},
    {"src": "/icons/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}
  ]
}
```

### 9.4 Strategi cache service worker
| Jenis permintaan | Strategi |
|---|---|
| File statis (HTML, CSS, JS, ikon, font) | *Cache first*, diperbarui saat versi cache berubah |
| `/api/materi`, `/api/contoh`, `/api/soal` | *Network first*, jika gagal memakai cache terakhir |
| `/api/fpb` | *Network first*, jika offline frontend memakai `fpb.js` |
| `/api/uji`, `/api/petunjuk`, `/api/pembahasan` | Tidak di-cache (soal acak / bantuan bertahap) |
| `/api/periksa`, `/api/hasil` (POST) | Tidak di-cache. Pemeriksaan butuh internet. Data hasil masuk antrean `localStorage` dan dikirim ulang saat online |
