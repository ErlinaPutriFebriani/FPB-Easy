"""Membuat supabase/seed.sql dari api/data/konten.json.

Jalankan setiap kali konten.json diubah:
    python scripts/buat_seed_sql.py
Lalu jalankan isi supabase/seed.sql di Supabase SQL Editor.
Seed memakai upsert, jadi aman dijalankan berulang (data jawaban siswa tidak terhapus).
"""

import json
from pathlib import Path

AKAR = Path(__file__).resolve().parent.parent
SUMBER = AKAR / "api" / "data" / "konten.json"
TUJUAN = AKAR / "supabase" / "seed.sql"

KEPALA = """-- FPB Easy: isi awal materi & soal.
-- DIBUAT OTOMATIS oleh scripts/buat_seed_sql.py dari api/data/konten.json. Jangan edit manual.
-- Jalankan di Supabase SQL Editor setelah schema.sql. Aman dijalankan berulang (upsert).

create temp table _konten on commit drop as select $konten$
"""

EKOR = """
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
"""


def main():
    teks = SUMBER.read_text(encoding="utf-8")
    json.loads(teks)  # pastikan JSON valid sebelum dibuat SQL-nya
    if "$konten$" in teks:
        raise SystemExit("konten.json tidak boleh berisi teks $konten$")
    TUJUAN.write_text("begin;\n" + KEPALA + teks.strip() + EKOR + "\ncommit;\n", encoding="utf-8")
    print(f"Berhasil menulis {TUJUAN.relative_to(AKAR)}")


if __name__ == "__main__":
    main()
