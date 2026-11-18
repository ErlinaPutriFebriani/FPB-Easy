-- FPB Easy - migrasi 002: log percakapan Pembimbing AI (RMT)
-- Jalankan SEKALI di Supabase: SQL Editor -> New query -> tempel -> Run.
-- Aman dijalankan ulang (if not exists). TIDAK menghapus atau mengubah data yang sudah ada.

create table if not exists interaksi_ai (
  id            bigserial primary key,
  perangkat_id  uuid not null,
  kode_siswa    text,
  soal_id       text not null references soal (id),
  fase          text not null check (fase in ('input', 'elaborasi', 'output', 'refleksi')),
  tahap         text not null,
  tingkat       int,                        -- 1-3 untuk tombol "Tanya Pembimbing"; null untuk tanya bebas/refleksi
  jenis         text not null check (jenis in ('petunjuk', 'tanya', 'refleksi')),
  pesan_siswa   text,                       -- pertanyaan bebas atau alasan refleksi siswa
  balasan       text not null,
  sumber        text not null check (sumber in ('ai', 'statis')),
  created_at    timestamptz not null default now()
);

create index if not exists interaksi_ai_perangkat_idx on interaksi_ai (perangkat_id);
create index if not exists interaksi_ai_soal_idx on interaksi_ai (soal_id);

-- KEAMANAN: sama seperti tabel lain, hanya backend (service key) yang bisa mengakses.
alter table interaksi_ai enable row level security;

-- ------------------------------------------------------------------
-- Contoh query analisis (jalankan terpisah bila perlu)
-- ------------------------------------------------------------------
-- Di fase RMT mana siswa paling sering minta bantuan?
-- select fase, jenis, count(*) as banyak
-- from interaksi_ai group by fase, jenis order by banyak desc;
--
-- Tahap & soal yang paling banyak memicu bantuan tingkat 3 (kesulitan berat):
-- select soal_id, tahap, count(*) as banyak
-- from interaksi_ai where tingkat = 3 group by soal_id, tahap order by banyak desc;
--
-- Alasan refleksi siswa (untuk dianalisis kualitatif):
-- select kode_siswa, soal_id, pesan_siswa, balasan, created_at
-- from interaksi_ai where jenis = 'refleksi' order by created_at;
