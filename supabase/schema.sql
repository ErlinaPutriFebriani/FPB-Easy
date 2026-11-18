-- FPB Easy: skema database Supabase
-- Jalankan SEKALI di Supabase: SQL Editor -> New query -> tempel -> Run.
-- Setelah itu jalankan supabase/seed.sql untuk mengisi materi & soal.

create table if not exists materi (
  id      serial primary key,
  urutan  int  not null,
  judul   text not null,
  isi     text not null,
  contoh  jsonb
);

create table if not exists soal (
  id                  text primary key,
  peran               text not null check (peran in ('contoh', 'latihan', 'uji')),
  level               int  not null check (level between 1 and 3),
  jenis               text not null check (jenis in ('langsung', 'cerita', 'tabel')),
  fading              text not null check (fading in ('A', 'B', 'C')),
  judul               text,
  pertanyaan          text not null,
  diketahui           text,
  ditanya             text,
  tabel               jsonb,
  sel_relevan         jsonb,
  umpan_balik_sel     jsonb,
  bilangan            int[] not null,
  jawaban             int  not null,
  kesimpulan          text,
  pilihan_kesimpulan  jsonb,
  petunjuk            jsonb not null default '[]'::jsonb,
  aktif               boolean not null default true
);

-- Satu baris untuk setiap soal latihan yang diselesaikan siswa (anonim).
create table if not exists jawaban (
  id               bigserial primary key,
  perangkat_id     uuid not null,
  kode_siswa       text,
  soal_id          text not null references soal (id),
  jawaban          text,
  benar            boolean not null,          -- benar tanpa salah sama sekali (mandiri)
  jumlah_salah     int not null default 0,
  jumlah_petunjuk  int not null default 0,
  durasi_detik     int not null default 0,
  created_at       timestamptz not null default now()
);

-- Satu baris untuk setiap Uji Diri.
create table if not exists hasil_uji (
  id            bigserial primary key,
  perangkat_id  uuid not null,
  kode_siswa    text,
  skor          int not null,
  total         int not null,
  rincian       jsonb,
  created_at    timestamptz not null default now()
);

create index if not exists jawaban_perangkat_idx on jawaban (perangkat_id);
create index if not exists jawaban_soal_idx on jawaban (soal_id);
create index if not exists hasil_uji_perangkat_idx on hasil_uji (perangkat_id);

-- KEAMANAN: RLS aktif tanpa policy -> browser (role anon) tidak bisa membaca/menulis apa pun.
-- Hanya backend Python yang memakai service role key yang dapat mengakses tabel.
alter table materi    enable row level security;
alter table soal      enable row level security;
alter table jawaban   enable row level security;
alter table hasil_uji enable row level security;

-- Tabel interaksi_ai (log Pembimbing AI) ada di supabase/migrasi_002_interaksi_ai.sql.
-- Untuk proyek Supabase BARU: jalankan schema.sql, seed.sql, lalu migrasi_002_interaksi_ai.sql.

-- ------------------------------------------------------------------
-- Contoh query analisis untuk penelitian (jalankan terpisah bila perlu)
-- ------------------------------------------------------------------
-- Persentase benar (mandiri) per level & jenis soal:
-- select s.level, s.jenis, count(*) as banyak,
--        round(avg(j.benar::int) * 100) as persen_benar_mandiri,
--        round(avg(j.jumlah_petunjuk), 1) as rata_petunjuk,
--        round(avg(j.durasi_detik)) as rata_detik
-- from jawaban j join soal s on s.id = j.soal_id
-- group by s.level, s.jenis order by s.level;
--
-- Skor uji diri per kode siswa:
-- select kode_siswa, skor, total, created_at from hasil_uji order by created_at desc;
