"""Test endpoint Flask (mode lokal, tanpa Supabase)."""
import pytest

import db
from index import app

PERANGKAT = "123e4567-e89b-42d3-a456-426614174000"


@pytest.fixture
def klien():
    app.config["TESTING"] = True
    return app.test_client()


def test_ping(klien):
    res = klien.get("/api/ping")
    assert res.status_code == 200
    assert res.get_json() == {"ok": True, "mode": "lokal"}


def test_fpb(klien):
    data = klien.get("/api/fpb?bil=20,28").get_json()
    assert data["fpb"] == 4
    assert data["langkah"][-1]["judul"] == "FPB"


def test_fpb_tidak_valid(klien):
    res = klien.get("/api/fpb?bil=0,5")
    assert res.status_code == 400
    assert "lebih dari 0" in res.get_json()["pesan"]


def test_materi(klien):
    data = klien.get("/api/materi").get_json()
    assert len(data) == 6
    assert [m["urutan"] for m in data] == sorted(m["urutan"] for m in data)


def test_contoh_berisi_langkah(klien):
    data = klien.get("/api/contoh").get_json()
    assert {c["jenis"] for c in data} == {"langsung", "cerita", "tabel"}
    assert all(c["langkah"] for c in data)


def test_soal_per_level_tanpa_kunci(klien):
    data = klien.get("/api/soal?level=3").get_json()
    assert [s["fading"] for s in data] == ["A", "B", "C"]
    assert all("jawaban" not in s and "sel_relevan" not in s for s in data)


def test_soal_level_bukan_angka(klien):
    assert klien.get("/api/soal?level=abc").status_code == 400


def test_periksa(klien):
    res = klien.post("/api/periksa", json={"soal_id": "langsung-a", "tahap": "fpb", "isian": 9})
    assert res.get_json()["benar"] is True


def test_periksa_soal_tidak_ada(klien):
    res = klien.post("/api/periksa", json={"soal_id": "xyz", "tahap": "fpb", "isian": 9})
    assert res.status_code == 400


def test_periksa_bukan_json(klien):
    res = klien.post("/api/periksa", data="halo")
    assert res.status_code == 400


def test_petunjuk_bertahap(klien):
    p1 = klien.get("/api/petunjuk?soal_id=tabel-a&ke=1").get_json()
    p3 = klien.get("/api/petunjuk?soal_id=tabel-a&ke=3").get_json()
    assert p1["teks"] and p3["teks"] and p1["teks"] != p3["teks"]
    assert p1["jumlah"] == 3


def test_pembahasan_uji_ditolak(klien):
    assert klien.get("/api/pembahasan?soal_id=uji-tabel-1").status_code == 400
    assert klien.get("/api/pembahasan?soal_id=tabel-a").get_json()["jawaban"] == 12


def test_uji_dan_nilai(klien):
    soal = klien.get("/api/uji").get_json()
    assert len(soal) == 5
    jawaban = [{"soal_id": s["id"], "isian": 1} for s in soal]
    res = klien.post("/api/uji/nilai", json={"perangkat_id": PERANGKAT, "kode_siswa": "S01", "jawaban": jawaban})
    hasil = res.get_json()
    assert res.status_code == 200 and hasil["total"] == 5
    tersimpan = db.simpanan_lokal()["hasil_uji"]
    assert len(tersimpan) == 1 and tersimpan[0]["kode_siswa"] == "S01"


def test_hasil_disimpan(klien):
    res = klien.post("/api/hasil", json={
        "perangkat_id": PERANGKAT,
        "kode_siswa": None,
        "jawaban": [{"soal_id": "tabel-a", "jawaban": "12", "benar": True, "jumlah_salah": 0,
                     "jumlah_petunjuk": 1, "durasi_detik": 95}],
    })
    assert res.get_json() == {"tersimpan": 1}
    baris = db.simpanan_lokal()["jawaban"][0]
    assert baris["soal_id"] == "tabel-a" and baris["jumlah_petunjuk"] == 1


def test_hasil_perangkat_tidak_valid(klien):
    res = klien.post("/api/hasil", json={"perangkat_id": "bukan-uuid", "jawaban": [{"soal_id": "tabel-a"}]})
    assert res.status_code == 400


def test_hasil_kode_siswa_tidak_valid(klien):
    res = klien.post("/api/hasil", json={
        "perangkat_id": PERANGKAT, "kode_siswa": "Nama Lengkap Siswa!", "jawaban": [{"soal_id": "tabel-a"}],
    })
    assert res.status_code == 400


def test_api_tidak_dikenal(klien):
    assert klien.get("/api/tidak-ada").status_code == 404


def test_halaman_utama_dan_pwa(klien):
    assert klien.get("/").status_code == 200
    assert klien.get("/manifest.json").status_code == 200
    assert klien.get("/service-worker.js").status_code == 200
    assert klien.get("/icons/icon-512.png").status_code == 200
