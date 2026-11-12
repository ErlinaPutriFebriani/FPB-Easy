"""FPB Easy - backend Python (Flask).

- Di Vercel: file ini menjadi Python Function untuk semua path /api/* (lihat vercel.json).
- Di laptop: `python api/index.py` juga menyajikan frontend dari folder public/.
"""

import os
import re
import sys
from pathlib import Path

# Supaya modul di folder api/ (fpb, soal, db) bisa diimpor, baik di Vercel maupun lokal.
FOLDER_API = Path(__file__).resolve().parent
if str(FOLDER_API) not in sys.path:
    sys.path.insert(0, str(FOLDER_API))

from flask import Flask, jsonify, request, send_from_directory  # noqa: E402

import db  # noqa: E402
import fpb as alg  # noqa: E402
import soal as logika  # noqa: E402

FOLDER_PUBLIC = FOLDER_API.parent / "public"

app = Flask(__name__, static_folder=str(FOLDER_PUBLIC), static_url_path="")
app.json.ensure_ascii = False
app.json.sort_keys = False

# Catatan Vercel: proyek ini dijalankan Vercel sebagai aplikasi Flask. Setiap request yang bukan
# file statis di public/ diteruskan ke app ini DENGAN PATH ASLINYA (mis. /api/materi).
# Karena itu vercel.json TIDAK boleh berisi rewrite "/api/(.*)" -> "/api/index": rewrite itu
# mengubah semua path menjadi /api/index sehingga setiap API menjawab "tidak ditemukan".

POLA_UUID = re.compile(r"^[0-9a-fA-F-]{36}$")
POLA_KODE = re.compile(r"^[A-Za-z0-9_-]{1,20}$")
MAKS_BARIS_HASIL = 100


class PermintaanSalah(Exception):
    pass


@app.errorhandler(PermintaanSalah)
@app.errorhandler(logika.InputSalah)
def tangani_input_salah(err):
    return jsonify({"pesan": str(err)}), 400


@app.errorhandler(db.GagalDatabase)
def tangani_gagal_database(err):
    return jsonify({"pesan": str(err)}), 503


@app.errorhandler(404)
def tidak_ditemukan(_err):
    if request.path.startswith("/api/"):
        return jsonify({"pesan": "Alamat API tidak ditemukan."}), 404
    if "." in request.path.rsplit("/", 1)[-1]:
        return "File tidak ditemukan", 404
    # Router frontend memakai hash (#/...), jadi path halaman lain diarahkan ke index.html.
    # Di Vercel, public/ disajikan CDN dan tidak ikut dibundel ke function -> balas 404 biasa.
    if (FOLDER_PUBLIC / "index.html").is_file():
        return send_from_directory(FOLDER_PUBLIC, "index.html")
    return jsonify({"pesan": "Halaman tidak ditemukan."}), 404


@app.errorhandler(500)
def galat_server(_err):
    return jsonify({"pesan": "Maaf, server sedang bermasalah. Coba lagi sebentar, ya."}), 500


# ---------------------------------------------------------------- bantuan

def _json_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise PermintaanSalah("Data harus berupa JSON.")
    return data


def _ambil_soal_atau_404(soal_id):
    soal = db.ambil_soal_per_id(soal_id) if isinstance(soal_id, str) else None
    if soal is None:
        raise PermintaanSalah("Soal tidak ditemukan.")
    return soal


def _identitas(data):
    perangkat_id = data.get("perangkat_id")
    if not isinstance(perangkat_id, str) or not POLA_UUID.match(perangkat_id):
        raise PermintaanSalah("perangkat_id tidak valid.")
    kode = data.get("kode_siswa") or None
    if kode is not None and (not isinstance(kode, str) or not POLA_KODE.match(kode)):
        raise PermintaanSalah("Kode siswa hanya boleh huruf/angka, maksimal 20 karakter.")
    return perangkat_id, kode


def _int_aman(x, batas_atas):
    try:
        n = int(x)
    except (TypeError, ValueError):
        return 0
    return max(0, min(n, batas_atas))


def _int_query(nama):
    nilai = request.args.get(nama)
    if nilai is None or nilai == "":
        return None
    if not nilai.isdigit():
        raise PermintaanSalah(f"Parameter {nama} harus angka.")
    return int(nilai)


# ---------------------------------------------------------------- halaman (lokal)

@app.get("/")
def beranda():
    return send_from_directory(FOLDER_PUBLIC, "index.html")


# ---------------------------------------------------------------- API

@app.get("/api/ping")
def ping():
    """Cek cepat setelah deploy: apakah API hidup dan database tersambung."""
    return jsonify({
        "ok": True,
        "mode": "supabase" if db.mode_supabase() else "lokal",
        "database": db.cek_koneksi(),
    })


@app.get("/api/fpb")
def api_fpb():
    """Contoh: /api/fpb?bil=20,28 -> langkah + hasil FPB."""
    teks = request.args.get("bil", "")
    bagian = [b for b in teks.split(",") if b.strip() != ""]
    try:
        return jsonify(alg.hitung(bagian))
    except ValueError as err:
        return jsonify({"pesan": str(err)}), 400


@app.get("/api/materi")
def api_materi():
    return jsonify(db.ambil_materi())


@app.get("/api/contoh")
def api_contoh():
    return jsonify([logika.contoh_lengkap(s) for s in db.ambil_soal(peran="contoh")])


@app.get("/api/soal")
def api_soal():
    level = _int_query("level")
    jenis = request.args.get("jenis") or None
    daftar = db.ambil_soal(peran="latihan", level=level, jenis=jenis)
    return jsonify([logika.untuk_siswa(s) for s in daftar])


@app.post("/api/periksa")
def api_periksa():
    data = _json_body()
    soal = _ambil_soal_atau_404(data.get("soal_id"))
    tahap = data.get("tahap")
    if not isinstance(tahap, str):
        raise PermintaanSalah("Tahap harus diisi.")
    return jsonify(logika.periksa(soal, tahap, data.get("isian")))


@app.get("/api/petunjuk")
def api_petunjuk():
    soal = _ambil_soal_atau_404(request.args.get("soal_id"))
    ke = _int_query("ke") or 1
    teks = logika.petunjuk(soal, ke)
    return jsonify({"ke": ke, "teks": teks, "jumlah": len(soal.get("petunjuk") or [])})


@app.get("/api/pembahasan")
def api_pembahasan():
    soal = _ambil_soal_atau_404(request.args.get("soal_id"))
    if soal["peran"] == "uji":
        raise PermintaanSalah("Pembahasan uji diri muncul setelah semua soal dijawab.")
    return jsonify({
        "langkah": logika.pembahasan(soal),
        "jawaban": soal["jawaban"],
        "kesimpulan": soal.get("kesimpulan"),
    })


@app.get("/api/uji")
def api_uji():
    terpilih = logika.pilih_soal_uji(db.ambil_semua_soal())
    return jsonify([logika.untuk_siswa(s) for s in terpilih])


@app.post("/api/uji/nilai")
def api_uji_nilai():
    data = _json_body()
    perangkat_id, kode = _identitas(data)
    hasil = logika.nilai_uji(data.get("jawaban"), db.ambil_soal_per_id)
    db.simpan_hasil_uji({
        "perangkat_id": perangkat_id,
        "kode_siswa": kode,
        "skor": hasil["skor"],
        "total": hasil["total"],
        "rincian": [
            {"soal_id": r["soal_id"], "isian": r["isian"], "benar": r["benar"]}
            for r in hasil["rincian"]
        ],
    })
    return jsonify(hasil)


@app.post("/api/hasil")
def api_hasil():
    """Menyimpan jawaban latihan (bisa beberapa sekaligus dari antrean offline)."""
    data = _json_body()
    perangkat_id, kode = _identitas(data)
    daftar = data.get("jawaban")
    if not isinstance(daftar, list) or not daftar:
        raise PermintaanSalah("Daftar jawaban kosong.")
    if len(daftar) > MAKS_BARIS_HASIL:
        raise PermintaanSalah("Terlalu banyak jawaban sekaligus.")

    baris = []
    for item in daftar:
        if not isinstance(item, dict):
            raise PermintaanSalah("Format jawaban salah.")
        soal = _ambil_soal_atau_404(item.get("soal_id"))
        baris.append({
            "perangkat_id": perangkat_id,
            "kode_siswa": kode,
            "soal_id": soal["id"],
            "jawaban": str(item.get("jawaban", ""))[:200],
            "benar": bool(item.get("benar")),
            "jumlah_salah": _int_aman(item.get("jumlah_salah"), 100),
            "jumlah_petunjuk": _int_aman(item.get("jumlah_petunjuk"), 10),
            "durasi_detik": _int_aman(item.get("durasi_detik"), 3600),
        })
    tersimpan = db.simpan_jawaban(baris)
    return jsonify({"tersimpan": tersimpan})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    mode = "supabase" if db.mode_supabase() else "lokal"
    print(f"FPB Easy berjalan di http://localhost:{port}  (mode data: {mode})")
    print("Untuk dibuka dari HP di Wi-Fi yang sama: http://<IP-laptop>:" + str(port))
    # host 0.0.0.0 agar bisa diakses dari HP; debug dimatikan supaya debugger tidak terbuka di jaringan.
    app.run(host="0.0.0.0", port=port, debug=False)
