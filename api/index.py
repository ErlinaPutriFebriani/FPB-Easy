"""FPB Easy - backend Python (Flask).

- Di Vercel: file ini menjadi Python Function untuk semua path /api/* (lihat vercel.json).
- Di laptop: `python api/index.py` juga menyajikan frontend dari folder public/.
"""

import json
import os
import re
import sys
from pathlib import Path

# Supaya modul di folder api/ (fpb, soal, db) bisa diimpor, baik di Vercel maupun lokal.
FOLDER_API = Path(__file__).resolve().parent
if str(FOLDER_API) not in sys.path:
    sys.path.insert(0, str(FOLDER_API))

from flask import Flask, jsonify, request, send_from_directory  # noqa: E402

import ai  # noqa: E402
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
        "ai": "aktif" if ai.aktif() else "nonaktif",
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


# ---------------------------------------------------------------- Pembimbing AI (RMT)

def _soal_untuk_ai(soal_id):
    soal = _ambil_soal_atau_404(soal_id)
    if soal["peran"] == "uji":
        raise PermintaanSalah("Uji Diri dikerjakan mandiri, tanpa Pembimbing.")
    return soal


def _teks_pendek(data, nama, batas, wajib=False):
    nilai = data.get(nama)
    if nilai is None or (isinstance(nilai, str) and not nilai.strip()):
        if wajib:
            raise PermintaanSalah("Tulis dulu pesanmu, ya.")
        return None
    if not isinstance(nilai, str):
        raise PermintaanSalah(f"{nama} harus berupa teks.")
    nilai = nilai.strip()
    if len(nilai) > batas:
        raise PermintaanSalah(f"Pesanmu terlalu panjang. Maksimal {batas} huruf, ya.")
    return nilai


def _riwayat(data):
    daftar = data.get("riwayat") or []
    if not isinstance(daftar, list):
        raise PermintaanSalah("Riwayat harus berupa daftar.")
    hasil = []
    for r in daftar[-ai.MAKS_RIWAYAT:]:
        if isinstance(r, dict) and r.get("peran") in ("siswa", "pembimbing") and isinstance(r.get("teks"), str):
            hasil.append({"peran": r["peran"], "teks": r["teks"][:ai.MAKS_KARAKTER_BALASAN]})
    return hasil


def _catat_interaksi(perangkat_id, kode, soal, tahap, tingkat, jenis, pesan_siswa, hasil):
    db.simpan_interaksi_ai({
        "perangkat_id": perangkat_id,
        "kode_siswa": kode,
        "soal_id": soal["id"],
        "fase": hasil["fase"],
        "tahap": tahap,
        "tingkat": tingkat,
        "jenis": jenis,
        "pesan_siswa": pesan_siswa,
        "balasan": hasil["teks"],
        "sumber": hasil["sumber"],
    })


@app.post("/api/bimbing")
def api_bimbing():
    """Bantuan bertahap / jawaban pertanyaan siswa dari Pembimbing (tanpa jawaban akhir)."""
    data = _json_body()
    perangkat_id, kode = _identitas(data)
    soal = _soal_untuk_ai(data.get("soal_id"))
    tahap = data.get("tahap")
    if tahap not in ai.TUGAS_TAHAP:
        raise PermintaanSalah("Tahap tidak dikenal.")
    pertanyaan = _teks_pendek(data, "pertanyaan", ai.MAKS_PERTANYAAN)
    tingkat = max(1, min(_int_aman(data.get("tingkat"), 3), 3))
    jawaban_salah = data.get("jawaban_salah")
    if len(json.dumps(jawaban_salah, ensure_ascii=False)) > 400:
        jawaban_salah = None
    pesan_salah = _teks_pendek(data, "pesan_salah", 300) if isinstance(data.get("pesan_salah"), str) else None

    if ai.melewati_batas(perangkat_id, soal["id"]):
        hasil = {
            "teks": "Kamu sudah banyak bertanya di soal ini. Coba kerjakan dulu, atau buka pembahasannya, ya.",
            "sumber": "statis", "fase": ai.fase_dari_tahap(tahap), "catatan": "batas",
        }
    else:
        hasil = ai.bimbing(soal, tahap, tingkat, jawaban_salah, pesan_salah, _riwayat(data), pertanyaan)
    _catat_interaksi(perangkat_id, kode, soal, tahap, None if pertanyaan else tingkat,
                     "tanya" if pertanyaan else "petunjuk", pertanyaan, hasil)
    return jsonify({"teks": hasil["teks"], "sumber": hasil["sumber"], "fase": hasil["fase"],
                    "ai_aktif": ai.aktif()})


@app.post("/api/refleksi")
def api_refleksi():
    """Fase Refleksi RMT: siswa menjelaskan alasannya, Pembimbing menanggapi (makna & transendensi)."""
    data = _json_body()
    perangkat_id, kode = _identitas(data)
    soal = _soal_untuk_ai(data.get("soal_id"))
    alasan = _teks_pendek(data, "alasan", ai.MAKS_ALASAN, wajib=True)
    jawaban_siswa = data.get("jawaban_fpb")
    jawaban_siswa = jawaban_siswa if isinstance(jawaban_siswa, int) and not isinstance(jawaban_siswa, bool) else None
    if ai.melewati_batas(perangkat_id, soal["id"]):
        hasil = {"teks": "Terima kasih sudah menjelaskan, ya!", "sumber": "statis", "fase": "refleksi", "catatan": "batas"}
    else:
        hasil = ai.tanggapi_refleksi(soal, alasan, jawaban_siswa)
    _catat_interaksi(perangkat_id, kode, soal, "refleksi", None, "refleksi", alasan, hasil)
    return jsonify({"teks": hasil["teks"], "sumber": hasil["sumber"], "fase": "refleksi"})


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
