"""Akses data: Supabase (jika dikonfigurasi) atau mode lokal (api/data/konten.json).

Kunci Supabase HANYA dibaca dari environment variable di server
(SUPABASE_URL, SUPABASE_SERVICE_KEY). Kunci tidak pernah dikirim ke browser.
"""

import json
import os
import time
from pathlib import Path

try:  # python-dotenv hanya untuk pengembangan lokal
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
except ImportError:
    pass

FILE_KONTEN = Path(__file__).resolve().parent / "data" / "konten.json"
CACHE_DETIK = 60

_klien = None
_cache = {}
# Mode lokal: jawaban disimpan di memori saja (hilang saat server restart).
_simpanan_lokal = {"jawaban": [], "hasil_uji": [], "interaksi_ai": []}


class GagalDatabase(Exception):
    """Supabase tidak bisa dihubungi (mis. env salah, proyek dijeda, atau jaringan lambat)."""

    def __init__(self, pesan="Data belum bisa diambil. Coba lagi sebentar, ya."):
        super().__init__(pesan)


def mode_supabase():
    return bool(os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_SERVICE_KEY"))


def _supabase():
    """Klien dibuat sekali per instance serverless lalu dipakai ulang selama instance masih hangat.
    supabase-py memakai HTTPS (REST), jadi tidak ada koneksi Postgres yang perlu di-pool."""
    global _klien
    if _klien is None:
        from supabase import create_client  # impor di sini agar mode lokal tidak butuh paket supabase

        _klien = create_client(os.environ["SUPABASE_URL"].strip(), os.environ["SUPABASE_SERVICE_KEY"].strip())
    return _klien


def _jalankan(buat_query):
    """Menjalankan query Supabase. Jika gagal, klien di-reset dan dilempar GagalDatabase."""
    global _klien
    try:
        return buat_query(_supabase()).execute()
    except Exception as err:  # noqa: BLE001 - semua galat jaringan/kunci dijadikan satu pesan ramah
        _klien = None
        print(f"[db] Supabase gagal: {type(err).__name__}: {err}")  # muncul di log Vercel
        raise GagalDatabase() from err


def cek_koneksi():
    """Untuk /api/ping: 'lokal', 'terhubung', atau 'gagal'."""
    if not mode_supabase():
        return "lokal"
    try:
        _jalankan(lambda k: k.table("materi").select("id").limit(1))
        return "terhubung"
    except GagalDatabase:
        return "gagal"


def _konten_lokal():
    with open(FILE_KONTEN, encoding="utf-8") as f:
        return json.load(f)


def _dengan_cache(kunci, ambil):
    """Simpan hasil baca selama CACHE_DETIK supaya tidak bolak-balik ke database."""
    sekarang = time.time()
    if kunci in _cache and sekarang - _cache[kunci][0] < CACHE_DETIK:
        return _cache[kunci][1]
    data = ambil()
    _cache[kunci] = (sekarang, data)
    return data


def hapus_cache():
    _cache.clear()


def ambil_materi():
    def ambil():
        if mode_supabase():
            return _jalankan(lambda k: k.table("materi").select("*").order("urutan")).data
        return sorted(_konten_lokal()["materi"], key=lambda m: m["urutan"])

    return _dengan_cache("materi", ambil)


def ambil_semua_soal():
    def ambil():
        if mode_supabase():
            return _jalankan(lambda k: k.table("soal").select("*").eq("aktif", True).order("id")).data
        return _konten_lokal()["soal"]

    return _dengan_cache("soal", ambil)


def ambil_soal(peran=None, level=None, jenis=None):
    hasil = ambil_semua_soal()
    if peran is not None:
        hasil = [s for s in hasil if s["peran"] == peran]
    if level is not None:
        hasil = [s for s in hasil if s["level"] == level]
    if jenis is not None:
        hasil = [s for s in hasil if s["jenis"] == jenis]
    urutan_fading = {"A": 0, "B": 1, "C": 2}
    return sorted(hasil, key=lambda s: (s["level"], urutan_fading.get(s["fading"], 9), s["id"]))


def ambil_soal_per_id(soal_id):
    for s in ambil_semua_soal():
        if s["id"] == soal_id:
            return s
    return None


def simpan_jawaban(baris):
    """baris: list of dict sesuai kolom tabel `jawaban`."""
    if not baris:
        return 0
    if mode_supabase():
        _jalankan(lambda k: k.table("jawaban").insert(baris))
    else:
        _simpanan_lokal["jawaban"].extend(baris)
    return len(baris)


def simpan_hasil_uji(baris):
    if mode_supabase():
        _jalankan(lambda k: k.table("hasil_uji").insert(baris))
    else:
        _simpanan_lokal["hasil_uji"].append(baris)


def simpan_interaksi_ai(baris):
    """Log percakapan Pembimbing AI (untuk penelitian). Kegagalan TIDAK boleh mengganggu siswa."""
    if mode_supabase():
        try:
            _jalankan(lambda k: k.table("interaksi_ai").insert(baris))
        except GagalDatabase:
            pass  # mis. migrasi_002 belum dijalankan; balasan ke siswa tetap dikirim
    else:
        _simpanan_lokal["interaksi_ai"].append(baris)


def simpanan_lokal():
    """Untuk pengujian mode lokal."""
    return _simpanan_lokal
