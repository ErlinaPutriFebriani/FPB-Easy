import pytest

import fpb as alg


def test_faktor(kasus):
    for k in kasus["faktor"]:
        assert alg.faktor(k["n"]) == k["faktor"], k


def test_fpb_dan_persekutuan(kasus):
    for k in kasus["fpb"]:
        assert alg.fpb(*k["bilangan"]) == k["fpb"], k
        assert alg.faktor_persekutuan(*k["bilangan"]) == k["persekutuan"], k


def test_fpb_cocok_dengan_math_gcd():
    from math import gcd

    for a in range(1, 121):
        for b in range(1, 121, 7):
            assert alg.fpb(a, b) == gcd(a, b)


def test_pasangan_faktor():
    assert alg.pasangan_faktor(12) == [(1, 12), (2, 6), (3, 4)]
    assert alg.teks_pasangan(16) == "16 = 1×16 = 2×8 = 4×4"


def test_langkah_fpb_lengkap():
    langkah = alg.langkah_fpb(20, 28)
    assert [l["judul"] for l in langkah] == ["Faktor 20", "Faktor 28", "Faktor persekutuan", "FPB"]
    assert langkah[0]["isi"] == [1, 2, 4, 5, 10, 20]
    assert langkah[2]["isi"] == [1, 2, 4]
    assert langkah[3]["isi"] == [4]
    # setiap langkah punya alasan (GL02)
    assert all(l["alasan"] for l in langkah)


def test_langkah_fpb_relatif_prima():
    langkah = alg.langkah_fpb(7, 13)
    assert "hanya 1" in langkah[-1]["alasan"]


def test_validasi_menerima_string_angka():
    assert alg.validasi(["20", " 28 "]) == [20, 28]
    assert alg.validasi([20.0, 28]) == [20, 28]


def test_validasi_menolak(kasus):
    for salah in kasus["tidak_valid"]:
        with pytest.raises(ValueError):
            alg.validasi(salah)


def test_validasi_menolak_bool():
    with pytest.raises(ValueError):
        alg.validasi([True, 4])


def test_hitung():
    hasil = alg.hitung(["18", "27"])
    assert hasil["fpb"] == 9
    assert hasil["faktor"] == {"18": [1, 2, 3, 6, 9, 18], "27": [1, 3, 9, 27]}
    assert hasil["faktor_persekutuan"] == [1, 3, 9]
