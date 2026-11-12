"""Algoritma FPB (Faktor Persekutuan Terbesar).

Modul ini berisi fungsi murni (tanpa Flask / database) sehingga mudah diuji.
Metode yang dipakai sama dengan cara siswa di kelas (IL02):
  1. daftar faktor tiap bilangan,
  2. cari faktor yang sama (faktor persekutuan),
  3. ambil yang terbesar.

Cerminan JavaScript-nya ada di public/js/fpb.js (dipakai saat offline).
Jika mengubah file ini, ubah juga fpb.js dan jalankan tests/.
"""

from math import isqrt

BATAS_MIN = 1
BATAS_MAX = 1000
JUMLAH_MIN = 2
JUMLAH_MAX = 3


def validasi(bilangan):
    """Memastikan input berupa 2-3 bilangan bulat 1..1000.

    Mengembalikan list[int]. Melempar ValueError berisi pesan ramah untuk siswa.
    """
    if not isinstance(bilangan, (list, tuple)):
        raise ValueError("Masukkan 2 atau 3 bilangan, ya.")
    if not (JUMLAH_MIN <= len(bilangan) <= JUMLAH_MAX):
        raise ValueError("Masukkan 2 atau 3 bilangan, ya.")

    hasil = []
    for b in bilangan:
        if isinstance(b, bool):
            raise ValueError("Masukkan bilangan bulat positif, ya.")
        if isinstance(b, str):
            b = b.strip()
            if not b.isdigit():
                raise ValueError("Masukkan bilangan bulat positif, ya.")
            b = int(b)
        if isinstance(b, float):
            if not b.is_integer():
                raise ValueError("Masukkan bilangan bulat, bukan desimal, ya.")
            b = int(b)
        if not isinstance(b, int):
            raise ValueError("Masukkan bilangan bulat positif, ya.")
        if b < BATAS_MIN:
            raise ValueError("Bilangannya harus lebih dari 0, ya.")
        if b > BATAS_MAX:
            raise ValueError(f"Bilangannya maksimal {BATAS_MAX}, ya.")
        hasil.append(b)
    return hasil


def pasangan_faktor(n):
    """Pasangan perkalian yang hasilnya n, misal 12 -> [(1,12), (2,6), (3,4)].

    Cukup mencoba pembagi sampai akar n, karena pasangan di atas akar
    adalah kebalikan dari pasangan di bawahnya.
    """
    pasangan = []
    for a in range(1, isqrt(n) + 1):
        if n % a == 0:
            pasangan.append((a, n // a))
    return pasangan


def faktor(n):
    """Semua faktor n, terurut naik. Contoh: faktor(12) -> [1, 2, 3, 4, 6, 12]."""
    kecil = []
    besar = []
    for a, b in pasangan_faktor(n):
        kecil.append(a)
        if a != b:
            besar.append(b)
    return kecil + besar[::-1]


def faktor_persekutuan(*bilangan):
    """Faktor yang sama dari semua bilangan, terurut naik."""
    if not bilangan:
        return []
    sama = set(faktor(bilangan[0]))
    for b in bilangan[1:]:
        sama &= set(faktor(b))
    return sorted(sama)


def fpb(*bilangan):
    """FPB = faktor persekutuan yang paling besar."""
    return max(faktor_persekutuan(*bilangan))


def teks_pasangan(n):
    """'12 = 1×12 = 2×6 = 3×4' -> menjelaskan dari mana faktor berasal (GL02)."""
    bagian = [f"{a}×{b}" for a, b in pasangan_faktor(n)]
    return f"{n} = " + " = ".join(bagian)


def gabung(angka):
    """[1, 2, 4] -> '1, 2, 4'"""
    return ", ".join(str(x) for x in angka)


def langkah_fpb(*bilangan):
    """Langkah-langkah mencari FPB untuk ditampilkan bertahap.

    Setiap langkah berisi: judul (apa yang dilakukan), isi (angka-angkanya),
    dan alasan (mengapa / dari mana angka itu berasal).
    """
    langkah = []
    for b in bilangan:
        langkah.append({
            "judul": f"Faktor {b}",
            "isi": faktor(b),
            "alasan": f"Karena {teks_pasangan(b)}",
        })

    sama = faktor_persekutuan(*bilangan)
    daftar_bil = " dan ".join(str(b) for b in bilangan)
    langkah.append({
        "judul": "Faktor persekutuan",
        "isi": sama,
        "alasan": f"Angka yang muncul di semua daftar faktor {daftar_bil}.",
    })

    hasil = max(sama)
    if len(sama) > 1:
        alasan = f"Dari {gabung(sama)}, yang paling besar adalah {hasil}."
    else:
        alasan = "Faktor persekutuannya hanya 1, jadi FPB-nya 1."
    langkah.append({"judul": "FPB", "isi": [hasil], "alasan": alasan})
    return langkah


def hitung(bilangan):
    """Fungsi lengkap untuk API: validasi -> langkah -> hasil."""
    bil = validasi(bilangan)
    return {
        "bilangan": bil,
        "faktor": {str(b): faktor(b) for b in bil},
        "faktor_persekutuan": faktor_persekutuan(*bil),
        "langkah": langkah_fpb(*bil),
        "fpb": fpb(*bil),
    }
