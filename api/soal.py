"""Logika soal: menyiapkan soal untuk siswa, memeriksa jawaban per tahap,
memberi umpan balik spesifik, petunjuk, pembahasan, dan nilai Uji Diri.

Prinsip (DESAIN.md): umpan balik segera dan spesifik, petunjuk bertahap,
dan kunci jawaban tidak dikirim ke browser.
"""

import random
import re

import fpb as alg

# Kolom yang aman dikirim ke browser.
KOLOM_PUBLIK = ("id", "peran", "level", "jenis", "fading", "judul", "pertanyaan", "tabel")

PILIHAN_DITANYA = [
    {"nilai": "fpb", "teks": "Membagi benda sama banyak ke kelompok sebanyak mungkin (FPB)"},
    {"nilai": "jumlah", "teks": "Menjumlahkan semua angka"},
    {"nilai": "kpk", "teks": "Mencari waktu bertemu bersamaan (KPK)"},
]

# Tahap "rencana" (RMT: analisis tugas & perencanaan tindakan). Urutan benar = urutan list ini.
PILIHAN_RENCANA = [
    {"nilai": "faktor", "teks": "Tulis semua faktor tiap bilangan"},
    {"nilai": "sama", "teks": "Cari faktor yang sama"},
    {"nilai": "terbesar", "teks": "Pilih faktor sama yang paling besar"},
]
URUTAN_RENCANA = [p["nilai"] for p in PILIHAN_RENCANA]

PESAN_DITANYA = {
    "jumlah": "Kalau dijumlahkan, kita tidak tahu ada berapa kelompok yang isinya sama. "
              "Kata kuncinya: 'isi sama banyak' dan 'paling banyak'.",
    "kpk": "KPK dipakai untuk mencari waktu bertemu bersamaan. "
           "Di soal ini benda dibagi sama banyak, jadi pakai FPB.",
}


class InputSalah(ValueError):
    """Isian dari browser tidak sesuai format."""


# ---------------------------------------------------------------- persiapan soal

def angka_dalam_teks(teks):
    """Semua angka di soal cerita (termasuk pengecoh), urut dan tanpa duplikat."""
    hasil = []
    for a in re.findall(r"\d+", teks):
        n = int(a)
        if n not in hasil:
            hasil.append(n)
    return hasil


def untuk_siswa(soal, acak=random):
    """Versi soal yang dikirim ke browser: TANPA kunci jawaban."""
    data = {k: soal.get(k) for k in KOLOM_PUBLIK}
    data["jumlah_petunjuk"] = len(soal.get("petunjuk") or [])
    if soal["jenis"] == "langsung":
        # Pada soal langsung, bilangannya memang tertulis di soal.
        data["bilangan"] = soal["bilangan"]
    if soal["jenis"] == "cerita":
        data["angka_cerita"] = angka_dalam_teks(soal["pertanyaan"])
    if soal["jenis"] in ("cerita", "tabel"):
        data["pilihan_ditanya"] = PILIHAN_DITANYA
        rencana = list(PILIHAN_RENCANA)
        acak.shuffle(rencana)
        data["pilihan_rencana"] = rencana
    if soal.get("pilihan_kesimpulan"):
        pilihan = list(soal["pilihan_kesimpulan"])
        acak.shuffle(pilihan)
        data["pilihan_kesimpulan"] = pilihan
    return data


def contoh_lengkap(soal):
    """Contoh soal (worked example) boleh berisi semua langkah dan jawaban."""
    data = {k: soal.get(k) for k in KOLOM_PUBLIK}
    data["sel_relevan"] = soal.get("sel_relevan")
    data["bilangan"] = soal["bilangan"]
    data["langkah"] = pembahasan(soal)
    return data


# ---------------------------------------------------------------- konversi isian

def _ke_int(x):
    if isinstance(x, bool):
        raise InputSalah("Isian harus bilangan bulat.")
    if isinstance(x, int):
        return x
    if isinstance(x, float) and x.is_integer():
        return int(x)
    if isinstance(x, str) and x.strip().lstrip("-").isdigit():
        return int(x.strip())
    raise InputSalah("Isian harus bilangan bulat.")


def _ke_daftar_int(x):
    if not isinstance(x, list):
        raise InputSalah("Isian harus berupa daftar bilangan.")
    return [_ke_int(v) for v in x]


# ---------------------------------------------------------------- pemeriksaan umum

def periksa_faktor(n, daftar):
    """Memeriksa daftar faktor n yang ditulis siswa."""
    benar_semua = alg.faktor(n)
    isian = sorted(set(daftar))
    if isian == benar_semua:
        return {"benar": True, "pesan": f"Tepat! Faktor {n}: {alg.gabung(benar_semua)}."}

    for x in isian:
        if x <= 0:
            return {"benar": False, "pesan": "Faktor selalu bilangan bulat positif. Mulai dari 1, ya."}
        if x > n:
            return {"benar": False, "pesan": f"{x} lebih besar dari {n}, jadi tidak mungkin menjadi faktornya."}
        if n % x != 0:
            return {
                "benar": False,
                "pesan": f"{x} bukan faktor {n}, karena {n} : {x} masih bersisa {n % x}.",
            }

    kurang = len(set(benar_semua) - set(isian))
    return {
        "benar": False,
        "pesan": f"Angkamu sudah benar, tapi masih ada {kurang} faktor yang terlewat. "
                 f"Coba bagi {n} dengan 1, 2, 3, ... satu per satu.",
    }


def periksa_persekutuan(bilangan, daftar):
    sama = alg.faktor_persekutuan(*bilangan)
    isian = sorted(set(daftar))
    if isian == sama:
        return {"benar": True, "pesan": f"Tepat! Faktor persekutuannya: {alg.gabung(sama)}."}
    for x in isian:
        if x not in sama:
            for b in bilangan:
                if x <= 0 or b % x != 0:
                    return {
                        "benar": False,
                        "pesan": f"{x} bukan faktor {b}, jadi bukan faktor persekutuan.",
                    }
    return {
        "benar": False,
        "pesan": "Masih ada faktor yang sama yang terlewat. Periksa lagi kedua daftar dengan teliti.",
    }


def periksa_fpb(bilangan, x):
    sama = alg.faktor_persekutuan(*bilangan)
    hasil = max(sama)
    daftar_bil = " dan ".join(str(b) for b in bilangan)
    if x == hasil:
        return {"benar": True, "pesan": f"Benar! FPB dari {daftar_bil} adalah {hasil}."}
    if x in sama:
        return {
            "benar": False,
            "pesan": f"{x} memang faktor persekutuan, tapi masih ada yang lebih besar. "
                     "FPB adalah yang PALING BESAR.",
        }
    terkecil = min(bilangan)
    if x > terkecil:
        return {
            "benar": False,
            "pesan": f"{x} lebih besar dari {terkecil}, jadi tidak mungkin membagi habis {terkecil}.",
        }
    return {
        "benar": False,
        "pesan": f"{x} bukan faktor persekutuan dari {daftar_bil}. Coba periksa lagi daftar faktornya.",
    }


# ---------------------------------------------------------------- pemeriksaan per tahap

def _periksa_sel(soal, isian):
    if not isinstance(isian, list):
        raise InputSalah("Isian sel harus berupa daftar [baris, kolom].")
    try:
        dipilih = {(int(s[0]), int(s[1])) for s in isian}
    except (TypeError, ValueError, IndexError):
        raise InputSalah("Isian sel harus berupa daftar [baris, kolom].")

    relevan = {tuple(s) for s in soal["sel_relevan"]}
    if not dipilih:
        return {"benar": False, "pesan": "Ketuk dulu angka di tabel yang kamu butuhkan."}
    if dipilih == relevan:
        return {
            "benar": True,
            "pesan": "Tepat! Itu angka yang dibutuhkan.",
            "bilangan": soal["bilangan"],
        }

    umpan = soal.get("umpan_balik_sel") or {}
    for (b, k) in sorted(dipilih - relevan):
        pesan = umpan.get(f"kolom:{k}") or umpan.get(f"baris:{b}")
        if pesan:
            return {"benar": False, "pesan": pesan}
    if dipilih - relevan:
        return {
            "benar": False,
            "pesan": "Ada angka yang tidak dibutuhkan. Baca lagi: benda apa yang ditanyakan, "
                     "dan kolom mana yang berisi banyaknya?",
        }
    return {"benar": False, "pesan": "Sudah benar sebagian. Masih ada angka lain yang dibutuhkan."}


def _periksa_bilangan(soal, isian):
    dipilih = sorted(set(_ke_daftar_int(isian)))
    perlu = sorted(set(soal["bilangan"]))
    if not dipilih:
        return {"benar": False, "pesan": "Ketuk dulu angka yang kamu butuhkan."}
    if dipilih == perlu:
        return {"benar": True, "pesan": "Tepat! Itu angka yang dibagi.", "bilangan": soal["bilangan"]}
    for x in dipilih:
        if x not in perlu:
            return {
                "benar": False,
                "pesan": f"Angka {x} tidak dipakai untuk membagi. Baca lagi: benda apa saja yang dibagi?",
            }
    return {"benar": False, "pesan": "Sudah benar sebagian. Masih ada angka lain yang dibutuhkan."}


def periksa_rencana(isian):
    """Urutan langkah yang dipilih siswa (RMT: perencanaan tindakan)."""
    if not isinstance(isian, list) or not all(isinstance(x, str) for x in isian):
        raise InputSalah("Isian rencana harus berupa daftar langkah.")
    if isian == URUTAN_RENCANA:
        return {"benar": True, "pesan": "Tepat! Rencanamu sudah urut. Sekarang kita jalankan rencananya."}
    if len(isian) < len(URUTAN_RENCANA):
        return {"benar": False, "pesan": "Ketuk ketiga langkah sesuai urutan yang akan kamu kerjakan."}
    if isian[0] != "faktor":
        return {
            "benar": False,
            "pesan": "Langkah pertama: kumpulkan dulu bahannya. Apa yang harus ditulis sebelum mencari yang sama?",
        }
    return {
        "benar": False,
        "pesan": "Sebelum memilih yang terbesar, kamu perlu tahu dulu faktor yang sama.",
    }


def periksa(soal, tahap, isian):
    """Memeriksa satu tahap pengerjaan. Mengembalikan {benar, pesan, ...}."""
    bil = soal["bilangan"]

    if tahap == "pilih_sel":
        if soal["jenis"] != "tabel":
            raise InputSalah("Tahap ini hanya untuk soal tabel.")
        return _periksa_sel(soal, isian)

    if tahap == "pilih_bilangan":
        return _periksa_bilangan(soal, isian)

    if tahap == "ditanya":
        if isian == "fpb":
            return {"benar": True, "pesan": "Tepat! Benda dibagi sama banyak sebanyak mungkin → FPB."}
        return {"benar": False, "pesan": PESAN_DITANYA.get(isian, "Coba baca lagi pertanyaannya.")}

    if tahap == "rencana":
        return periksa_rencana(isian)

    if tahap == "faktor":
        if not isinstance(isian, dict):
            raise InputSalah("Isian faktor harus {bilangan, daftar}.")
        n = _ke_int(isian.get("bilangan"))
        if n not in bil:
            raise InputSalah("Bilangan tidak ada di soal ini.")
        return periksa_faktor(n, _ke_daftar_int(isian.get("daftar")))

    if tahap == "persekutuan":
        return periksa_persekutuan(bil, _ke_daftar_int(isian))

    if tahap == "fpb":
        return periksa_fpb(bil, _ke_int(isian))

    if tahap == "kesimpulan":
        if not soal.get("kesimpulan"):
            raise InputSalah("Soal ini tidak punya tahap kesimpulan.")
        if isinstance(isian, str) and isian.strip() == soal["kesimpulan"]:
            return {"benar": True, "pesan": "Tepat! Jawabanmu sudah sesuai dengan cerita soalnya."}
        return {
            "benar": False,
            "pesan": "Belum tepat. Pilih kalimat yang memakai hasil FPB dan sesuai dengan cerita.",
        }

    raise InputSalah("Tahap tidak dikenal.")


# ---------------------------------------------------------------- petunjuk & pembahasan

def petunjuk(soal, ke):
    daftar = soal.get("petunjuk") or []
    if 1 <= ke <= len(daftar):
        return daftar[ke - 1]
    return None


def pembahasan(soal):
    """Langkah lengkap: (pahami soal) → faktor → faktor persekutuan → FPB → (kesimpulan)."""
    langkah = []
    if soal["jenis"] in ("cerita", "tabel"):
        langkah.append({"judul": "Diketahui", "isi": None, "alasan": soal.get("diketahui") or ""})
        langkah.append({"judul": "Ditanya", "isi": None, "alasan": soal.get("ditanya") or ""})
    langkah.extend(alg.langkah_fpb(*soal["bilangan"]))
    if soal.get("kesimpulan"):
        langkah.append({"judul": "Kesimpulan", "isi": None, "alasan": soal["kesimpulan"]})
    return langkah


# ---------------------------------------------------------------- uji diri

KOMPOSISI_UJI = (("langsung", 2), ("cerita", 1), ("tabel", 2))


def pilih_soal_uji(semua, acak=random):
    """5 soal campuran dari bank latihan + uji, urut dari mudah ke sulit."""
    terpilih = []
    for jenis, banyak in KOMPOSISI_UJI:
        kandidat = [s for s in semua if s["jenis"] == jenis and s["peran"] in ("latihan", "uji")]
        terpilih.extend(acak.sample(kandidat, min(banyak, len(kandidat))))
    return terpilih


def nilai_uji(daftar_jawaban, cari_soal):
    """daftar_jawaban: [{soal_id, isian}]. cari_soal: fungsi id -> soal."""
    if not isinstance(daftar_jawaban, list) or not daftar_jawaban:
        raise InputSalah("Jawaban uji kosong.")
    rincian = []
    for item in daftar_jawaban:
        soal = cari_soal(item.get("soal_id"))
        if soal is None:
            raise InputSalah("Soal tidak ditemukan.")
        try:
            isian = _ke_int(item.get("isian"))
        except InputSalah:
            isian = None
        benar = isian == soal["jawaban"]
        rincian.append({
            "soal_id": soal["id"],
            "pertanyaan": soal["pertanyaan"],
            "tabel": soal.get("tabel"),
            "isian": isian,
            "benar": benar,
            "jawaban": soal["jawaban"],
            "pembahasan": pembahasan(soal),
        })
    skor = sum(1 for r in rincian if r["benar"])
    return {"skor": skor, "total": len(rincian), "rincian": rincian}
