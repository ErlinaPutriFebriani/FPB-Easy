"""Test logika soal + pemeriksaan konsistensi bank soal di konten.json."""
import random

import pytest

import fpb as alg
import soal as logika


def cari(konten, soal_id):
    return next(s for s in konten["soal"] if s["id"] == soal_id)


# ------------------------------------------------------------ konsistensi konten

def test_id_soal_unik(konten):
    ids = [s["id"] for s in konten["soal"]]
    assert len(ids) == len(set(ids))


def test_kunci_jawaban_sesuai_fpb(konten):
    for s in konten["soal"]:
        assert s["jawaban"] == alg.fpb(*s["bilangan"]), s["id"]


def test_sel_relevan_berisi_bilangan(konten):
    for s in konten["soal"]:
        if s["jenis"] != "tabel":
            continue
        nilai = sorted(s["tabel"]["baris"][b][k] for b, k in s["sel_relevan"])
        assert nilai == sorted(s["bilangan"]), s["id"]


def test_bilangan_cerita_ada_di_teks(konten):
    for s in konten["soal"]:
        if s["jenis"] == "cerita":
            angka = logika.angka_dalam_teks(s["pertanyaan"])
            assert set(s["bilangan"]) <= set(angka), s["id"]


def test_kesimpulan_ada_di_pilihan(konten):
    for s in konten["soal"]:
        if s.get("pilihan_kesimpulan"):
            assert s["kesimpulan"] in s["pilihan_kesimpulan"], s["id"]


def test_latihan_lengkap(konten):
    latihan = [s for s in konten["soal"] if s["peran"] == "latihan"]
    for level in (1, 2, 3):
        fading = sorted(s["fading"] for s in latihan if s["level"] == level)
        assert fading == ["A", "B", "C"], level
    for s in latihan:
        assert len(s["petunjuk"]) == 3, s["id"]
        if s["jenis"] != "langsung":
            assert s.get("pilihan_kesimpulan"), s["id"]


# ------------------------------------------------------------ untuk_siswa

def test_untuk_siswa_tanpa_kunci(konten):
    for s in konten["soal"]:
        data = logika.untuk_siswa(s, random.Random(1))
        for terlarang in ("jawaban", "sel_relevan", "kesimpulan", "petunjuk", "umpan_balik_sel"):
            assert terlarang not in data, (s["id"], terlarang)
        if s["jenis"] != "langsung":
            assert "bilangan" not in data, s["id"]


def test_untuk_siswa_cerita_punya_angka_pengecoh(konten):
    data = logika.untuk_siswa(cari(konten, "cerita-b"))
    assert data["angka_cerita"] == [8, 32, 48, 3]


# ------------------------------------------------------------ periksa per tahap

def test_periksa_sel_benar(konten):
    s = cari(konten, "tabel-a")
    hasil = logika.periksa(s, "pilih_sel", [[1, 1], [0, 1]])
    assert hasil["benar"] and hasil["bilangan"] == [48, 36]


def test_periksa_sel_pengecoh_harga(konten):
    s = cari(konten, "tabel-a")
    hasil = logika.periksa(s, "pilih_sel", [[0, 1], [0, 2]])
    assert not hasil["benar"]
    assert "harga" in hasil["pesan"]


def test_periksa_sel_pengecoh_baris(konten):
    s = cari(konten, "tabel-c")
    hasil = logika.periksa(s, "pilih_sel", [[0, 1], [1, 2]])
    assert not hasil["benar"] and "7B" in hasil["pesan"]


def test_periksa_sel_kurang(konten):
    s = cari(konten, "tabel-a")
    hasil = logika.periksa(s, "pilih_sel", [[0, 1]])
    assert not hasil["benar"] and "sebagian" in hasil["pesan"]


def test_periksa_bilangan_cerita(konten):
    s = cari(konten, "cerita-b")
    assert logika.periksa(s, "pilih_bilangan", [48, 32])["benar"]
    salah = logika.periksa(s, "pilih_bilangan", [32, 3])
    assert not salah["benar"] and "3" in salah["pesan"]


def test_periksa_ditanya(konten):
    s = cari(konten, "cerita-a")
    assert logika.periksa(s, "ditanya", "fpb")["benar"]
    assert not logika.periksa(s, "ditanya", "jumlah")["benar"]


def test_periksa_faktor_spesifik(konten):
    s = cari(konten, "langsung-b")  # 20 dan 28
    assert logika.periksa(s, "faktor", {"bilangan": 28, "daftar": [1, 2, 4, 7, 14, 28]})["benar"]
    salah = logika.periksa(s, "faktor", {"bilangan": 28, "daftar": [1, 2, 3, 4]})
    assert "3 bukan faktor 28" in salah["pesan"]
    kurang = logika.periksa(s, "faktor", {"bilangan": 28, "daftar": [1, 2, 4, 28]})
    assert "terlewat" in kurang["pesan"]


def test_periksa_faktor_bilangan_asing_ditolak(konten):
    s = cari(konten, "langsung-b")
    with pytest.raises(logika.InputSalah):
        logika.periksa(s, "faktor", {"bilangan": 99, "daftar": [1]})


def test_periksa_persekutuan(konten):
    s = cari(konten, "langsung-b")
    assert logika.periksa(s, "persekutuan", [4, 2, 1])["benar"]
    salah = logika.periksa(s, "persekutuan", [1, 2, 5])
    assert "5 bukan faktor 28" in salah["pesan"]


def test_periksa_fpb_umpan_balik(konten):
    s = cari(konten, "langsung-a")  # 18 dan 27, FPB 9
    assert logika.periksa(s, "fpb", 9)["benar"]
    assert "lebih besar" in logika.periksa(s, "fpb", 3)["pesan"]  # faktor persekutuan tapi bukan terbesar
    assert "tidak mungkin" in logika.periksa(s, "fpb", 54)["pesan"]
    assert "bukan faktor persekutuan" in logika.periksa(s, "fpb", 6)["pesan"]


def test_periksa_kesimpulan(konten):
    s = cari(konten, "tabel-a")
    assert logika.periksa(s, "kesimpulan", s["kesimpulan"])["benar"]
    assert not logika.periksa(s, "kesimpulan", s["pilihan_kesimpulan"][1])["benar"]


def test_periksa_tahap_asing(konten):
    with pytest.raises(logika.InputSalah):
        logika.periksa(cari(konten, "langsung-a"), "hapus", None)


def test_periksa_isian_bukan_angka(konten):
    with pytest.raises(logika.InputSalah):
        logika.periksa(cari(konten, "langsung-a"), "fpb", "sembilan")


# ------------------------------------------------------------ pembahasan & uji

def test_pembahasan_tabel_lengkap(konten):
    langkah = logika.pembahasan(cari(konten, "tabel-a"))
    judul = [l["judul"] for l in langkah]
    assert judul[0] == "Diketahui" and judul[1] == "Ditanya" and judul[-1] == "Kesimpulan"
    assert "FPB" in judul


def test_pilih_soal_uji_komposisi(konten):
    terpilih = logika.pilih_soal_uji(konten["soal"], random.Random(7))
    assert len(terpilih) == 5
    assert [s["jenis"] for s in terpilih].count("tabel") == 2
    assert all(s["peran"] in ("latihan", "uji") for s in terpilih)


def test_nilai_uji(konten):
    def cari_soal(i):
        return next((s for s in konten["soal"] if s["id"] == i), None)

    hasil = logika.nilai_uji(
        [{"soal_id": "uji-langsung-1", "isian": 12}, {"soal_id": "uji-tabel-1", "isian": "7"}],
        cari_soal,
    )
    assert hasil["skor"] == 1 and hasil["total"] == 2
    assert hasil["rincian"][1]["jawaban"] == 12
