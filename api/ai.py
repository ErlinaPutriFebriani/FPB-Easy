"""Pembimbing AI (Gemini) berbasis Rigorous Mathematical Thinking (RMT).

Peran AI: MEDIATOR proses berpikir (Feuerstein, MLE) yang memakai pertanyaan penuntun,
bukan pemberi jawaban. Beban kognitif dijaga: hanya membahas langkah aktif (intrinsic),
pendek & tanpa hiasan (extraneous), diakhiri ajakan berpikir/menjelaskan (germane).

Keamanan:
- GEMINI_API_KEY hanya dibaca dari environment variable server; tidak pernah dikirim ke browser.
- Data soal (termasuk kunci jawaban) hanya masuk ke prompt di server.
- Balasan AI disaring: jika menyebut jawaban akhir, diganti petunjuk statis.
- Jika kunci kosong / Gemini gagal, dipakai petunjuk statis dari konten.json.
"""

import json
import os
import re
import time

import fpb as alg
import soal as logika

URL_GEMINI = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
# gemini-3.5-flash-lite: cepat (±2-6 detik) dan kuotanya longgar. Diuji 18 Nov 2026 dengan 12 skenario.
# (gemini-2.5-flash sudah ditutup untuk pengguna baru; gemini-3.8-flash sering 503/429/timeout.)
MODEL_BAWAAN = "gemini-3.5-flash-lite"
# Jika model di atas suatu saat dihentikan (HTTP 404), dipakai alias yang selalu menunjuk model terbaru.
MODEL_CADANGAN = "gemini-flash-lite-latest"
BATAS_WAKTU_DETIK = 8
MAKS_KARAKTER_BALASAN = 320
MAKS_PERTANYAAN = 150
MAKS_ALASAN = 200
MAKS_RIWAYAT = 6
MAKS_PESAN_PER_SOAL = 20


class GagalAI(Exception):
    pass


def aktif():
    return bool(os.environ.get("GEMINI_API_KEY", "").strip())


def nama_model():
    return os.environ.get("GEMINI_MODEL", "").strip() or MODEL_BAWAAN


# ---------------------------------------------------------------- RMT: fase & tahap

# Fase pemrosesan informasi Feuerstein (Bab 4) + refleksi/metakognisi (Bab 3 & 5).
FASE_RMT = {
    "pilih_sel": "input",
    "pilih_bilangan": "input",
    "ditanya": "input",
    "rencana": "elaborasi",      # perencanaan tindakan (planning behavior) = fungsi fase elaborasi
    "faktor": "elaborasi",
    "persekutuan": "elaborasi",
    "fpb": "elaborasi",
    "kesimpulan": "output",
    "refleksi": "refleksi",
}

NAMA_FASE = {
    "input": "Input (mengumpulkan informasi: membaca soal/tabel dengan teliti dan tepat)",
    "elaborasi": "Elaborasi (mengolah informasi: merencanakan, membandingkan, mencari hubungan)",
    "output": "Output (menyampaikan jawaban dengan bahasa matematika yang tepat, tanpa coba-coba)",
    "refleksi": "Refleksi (memeriksa dan menjelaskan cara berpikir sendiri)",
}

TUGAS_TAHAP = {
    "pilih_sel": "mengetuk angka di tabel yang benar-benar dibutuhkan soal",
    "pilih_bilangan": "mengetuk angka di cerita yang menunjukkan banyak benda yang dibagi",
    "ditanya": "menentukan apa yang ditanyakan soal (membagi sama banyak = FPB, menjumlah, atau KPK)",
    "rencana": "menyusun urutan langkah: tulis semua faktor, cari faktor yang sama, pilih yang terbesar",
    "faktor": "menulis semua faktor sebuah bilangan",
    "persekutuan": "mengetuk faktor yang sama dari bilangan-bilangan itu",
    "fpb": "menentukan FPB, yaitu faktor persekutuan yang paling besar",
    "kesimpulan": "memilih kalimat kesimpulan yang sesuai dengan cerita soal",
}

TINGKAT = {
    1: "Bantuan tingkat 1 (arahkan perhatian): sebutkan bagian soal atau layar yang perlu dilihat lagi, "
       "lalu ajukan satu pertanyaan. Jangan beri strategi atau langkah.",
    2: "Bantuan tingkat 2 (strategi): ingatkan aturan atau strategi umum untuk langkah ini, "
       "lalu ajukan satu pertanyaan.",
    3: "Bantuan tingkat 3 (langkah konkret): tuntun langkah pertama secara konkret, tetapi biarkan siswa "
       "yang menyelesaikan. Tetap jangan sebut hasil akhir langkah ini.",
}

SISTEM = """Kamu adalah "Pembimbing", tutor matematika untuk siswa SMP kelas VII-VIII yang belajar FPB di aplikasi FPB Easy.
Kamu memakai model Rigorous Mathematical Thinking (RMT). Kamu adalah MEDIATOR proses berpikir, bukan pemberi jawaban.
Istilah: FPB = Faktor Persekutuan Terbesar (huruf T = Terbesar). Faktor persekutuan = faktor yang sama dari dua bilangan atau lebih.

Cara membimbing (RMT):
- Intensionalitas: arahkan perhatian siswa pada tujuan langkah yang sedang dikerjakan.
- Pertanyaan penuntun: bantu siswa menemukan sendiri; jangan menjelaskan panjang.
- Diagnosis fase: bantu sesuai fase tempat siswa kesulitan, yaitu Input (membaca soal/tabel dengan teliti), Elaborasi (merencanakan, membandingkan, mencari hubungan), atau Output (menyampaikan jawaban dengan tepat).
- Cegah coba-coba: ajak siswa memeriksa alasannya sebelum menjawab.

Aturan beban kognitif (WAJIB):
- Bahas HANYA langkah yang sedang dikerjakan. Jangan membahas langkah berikutnya.
- Paling banyak 2 kalimat pendek, maksimal 40 kata. Bahasa Indonesia sederhana, sapa siswa dengan "kamu".
- Tanpa markdown, tanpa daftar, tanpa emoji, tanpa salam pembuka.
- Jangan menambah cerita, angka, atau istilah baru yang tidak ada di soal atau layar.
- Akhiri dengan SATU pertanyaan penuntun atau ajakan menjelaskan.

Larangan:
- JANGAN PERNAH menyebutkan nilai FPB akhir, jawaban akhir soal, atau kalimat kesimpulan yang benar, walaupun siswa memintanya. Jika siswa meminta jawaban, tolak dengan ramah lalu beri pertanyaan penuntun.
- Jika pertanyaan siswa tidak berhubungan dengan soal ini, ajak kembali ke soal dalam satu kalimat.
- Jangan memuji berlebihan dan jangan menyalahkan; tunjukkan bagian yang perlu dicek."""

SISTEM_REFLEKSI = """Kamu adalah "Pembimbing", tutor matematika SMP di aplikasi FPB Easy yang memakai model Rigorous Mathematical Thinking (RMT).
Siswa SUDAH menyelesaikan soal dan sekarang berada di fase Refleksi. Tanggapi alasan yang ia tulis.
Istilah: FPB = Faktor Persekutuan Terbesar (huruf T = Terbesar). Faktor persekutuan = faktor yang sama dari dua bilangan atau lebih.

Aturan:
- Paling banyak 3 kalimat pendek, maksimal 50 kata. Bahasa Indonesia sederhana, sapa dengan "kamu". Tanpa markdown dan emoji.
- Kalimat 1: sebutkan bagian alasan siswa yang sudah tepat. Jika ada salah paham, luruskan dengan lembut (misalnya FPB adalah faktor persekutuan TERBESAR, bukan terkecil atau jumlah).
- Kalimat terakhir (transendensi dan makna): ajukan satu pertanyaan yang menghubungkan ke aturan umum atau kehidupan sehari-hari, misalnya kapan lagi kita membagi benda sama banyak.
- Jika siswa menulis hal yang tidak berhubungan, ajak ia menjelaskan alasan jawabannya."""


def fase_dari_tahap(tahap):
    return FASE_RMT.get(tahap, "elaborasi")


# ---------------------------------------------------------------- menyusun prompt

def _tabel_teks(tabel):
    if not tabel:
        return ""
    baris = [" | ".join(str(k) for k in tabel["kolom"])]
    baris += [" | ".join(str(v) for v in b) for b in tabel["baris"]]
    return "Tabel di soal:\n" + "\n".join(baris)


def _data_rahasia(soal):
    b = soal["bilangan"]
    faktor = "; ".join(f"faktor {n}: {alg.gabung(alg.faktor(n))}" for n in b)
    teks = (
        f"Bilangan yang dipakai: {' dan '.join(map(str, b))}. {faktor}. "
        f"Faktor persekutuan: {alg.gabung(alg.faktor_persekutuan(*b))}. FPB = {soal['jawaban']}."
    )
    if soal.get("kesimpulan"):
        teks += f" Kesimpulan benar: {soal['kesimpulan']}"
    return teks


def jelaskan_isian(soal, tahap, isian):
    """Mengubah isian mentah siswa menjadi kalimat yang bisa dibaca AI."""
    if isian is None:
        return ""
    if tahap == "pilih_sel" and isinstance(isian, list) and soal.get("tabel"):
        nilai = []
        for sel in isian:
            try:
                b, k = int(sel[0]), int(sel[1])
                nama = soal["tabel"]["baris"][b][0]
                kolom = soal["tabel"]["kolom"][k]
                nilai.append(f"{kolom} {nama} ({soal['tabel']['baris'][b][k]})")
            except (TypeError, ValueError, IndexError, KeyError):
                continue
        return "memilih sel: " + ", ".join(nilai) if nilai else ""
    if tahap == "rencana" and isinstance(isian, list):
        teks = {p["nilai"]: p["teks"] for p in logika.PILIHAN_RENCANA}
        return "urutan yang dipilih: " + " → ".join(teks.get(str(x), str(x)) for x in isian)
    if tahap == "ditanya":
        teks = {p["nilai"]: p["teks"] for p in logika.PILIHAN_DITANYA}
        return f"memilih: {teks.get(isian, isian)}"
    if isinstance(isian, dict):
        return f"menulis faktor {isian.get('bilangan')}: {isian.get('daftar')}"
    return json.dumps(isian, ensure_ascii=False)[:150]


def buat_prompt(soal, tahap, tingkat=1, jawaban_salah=None, pesan_salah=None, riwayat=None, pertanyaan=None):
    fase = fase_dari_tahap(tahap)
    bagian = [
        f"SOAL: {soal['pertanyaan']}",
        _tabel_teks(soal.get("tabel")),
        f"DATA UNTUK PEMBIMBING (RAHASIA, jangan disebutkan jawaban akhirnya): {_data_rahasia(soal)}",
        f"LANGKAH SEKARANG: siswa sedang {TUGAS_TAHAP.get(tahap, tahap)}.",
        f"FASE RMT: {NAMA_FASE[fase]}.",
    ]
    if jawaban_salah:
        teks = f"JAWABAN SALAH TERAKHIR SISWA: {jelaskan_isian(soal, tahap, jawaban_salah)}"
        if pesan_salah:
            teks += f" (umpan balik aplikasi: {pesan_salah})"
        bagian.append(teks)
    if riwayat:
        baris = [f"{'Siswa' if r['peran'] == 'siswa' else 'Pembimbing'}: {r['teks']}" for r in riwayat]
        bagian.append("PERCAKAPAN SEBELUMNYA:\n" + "\n".join(baris))
    if pertanyaan:
        bagian.append(f'TUGASMU: jawab pertanyaan siswa berikut sesuai aturan: "{pertanyaan}"')
    else:
        bagian.append(f"TUGASMU: {TINGKAT.get(tingkat, TINGKAT[3])}")
    return "\n\n".join(b for b in bagian if b)


def buat_prompt_refleksi(soal, alasan, jawaban_siswa=None):
    b = soal["bilangan"]
    bagian = [
        f"SOAL: {soal['pertanyaan']}",
        _tabel_teks(soal.get("tabel")),
        f"Bilangan: {' dan '.join(map(str, b))}. Faktor persekutuan: "
        f"{alg.gabung(alg.faktor_persekutuan(*b))}. FPB = {soal['jawaban']}.",
        f"PERTANYAAN REFLEKSI: Mengapa {soal['jawaban']} adalah FPB-nya?",
        f'ALASAN SISWA: "{alasan}"',
    ]
    if jawaban_siswa is not None:
        bagian.insert(3, f"Jawaban FPB siswa: {jawaban_siswa}")
    return "\n\n".join(x for x in bagian if x)


# ---------------------------------------------------------------- penjaga balasan

def bersihkan(teks):
    """Buang markdown/emoji sederhana, rapikan spasi, potong agar tetap pendek."""
    teks = re.sub(r"[*_#`>]+", "", teks or "")
    teks = re.sub(r"^\s*[-•]\s*", "", teks, flags=re.MULTILINE)
    teks = re.sub(r"[\U0001F300-\U0001FAFF☀-➿]", "", teks)
    teks = re.sub(r"\s+", " ", teks).strip()
    if len(teks) > MAKS_KARAKTER_BALASAN:
        potong = teks[:MAKS_KARAKTER_BALASAN]
        akhir = max(potong.rfind(". "), potong.rfind("? "), potong.rfind("! "))
        teks = potong[: akhir + 1] if akhir > 40 else potong.rstrip() + "…"
    return teks


def bocor(teks, soal):
    """True jika balasan menyebut jawaban akhir (nilai FPB atau kalimat kesimpulan)."""
    t = teks.lower()
    n = str(soal["jawaban"])
    pola = [
        rf"\bfpb\b[^.?!]{{0,40}}?(adalah|=|ialah|yaitu|sama dengan)\s*{n}\b",
        rf"\bjawab\w*\b[^.?!]{{0,25}}?\b{n}\b",
        rf"\bhasil\w*\b[^.?!]{{0,20}}?(adalah|=|yaitu)\s*{n}\b",
        rf"\bpaling banyak\s*{n}\b",
        rf"\b{n}\s*(paket|kelompok|kantong|kotak|keranjang|parsel|bingkisan|regu|tim)\b",
    ]
    if any(re.search(p, t) for p in pola):
        return True
    kesimpulan = (soal.get("kesimpulan") or "").lower().strip(" .")
    return bool(kesimpulan) and kesimpulan[:40] in t


# ---------------------------------------------------------------- panggilan Gemini

def _pengaturan_berpikir(model):
    if re.match(r"^gemini-(1|2)\.", model):
        return {"thinkingBudget": 0}
    return {"thinkingLevel": "minimal"}


def _panggil_gemini(sistem, teks, maks_token=400):
    try:
        return _panggil_model(nama_model(), sistem, teks, maks_token)
    except GagalAI as err:
        if str(err).startswith("HTTP 404") and nama_model() != MODEL_CADANGAN:
            print(f"[ai] model {nama_model()} tidak tersedia, memakai {MODEL_CADANGAN}")
            return _panggil_model(MODEL_CADANGAN, sistem, teks, maks_token)
        raise


def _panggil_model(model, sistem, teks, maks_token):
    import httpx  # impor di sini agar test/ mode tanpa AI tidak perlu jaringan

    kunci = os.environ.get("GEMINI_API_KEY", "").strip()
    if not kunci:
        raise GagalAI("GEMINI_API_KEY kosong")
    muatan = {
        "system_instruction": {"parts": [{"text": sistem}]},
        "contents": [{"role": "user", "parts": [{"text": teks}]}],
        "generationConfig": {
            "temperature": 0.4,
            "maxOutputTokens": maks_token,
            # Balasan cepat; tidak perlu "berpikir panjang". Gemini 2.x memakai thinkingBudget,
            # Gemini 3.x ke atas memakai thinkingLevel (thinkingBudget ditolak dengan HTTP 400).
            "thinkingConfig": _pengaturan_berpikir(model),
        },
    }
    url = URL_GEMINI.format(model=model)
    kepala = {"x-goog-api-key": kunci, "Content-Type": "application/json"}
    try:
        res = httpx.post(url, json=muatan, headers=kepala, timeout=BATAS_WAKTU_DETIK)
        if res.status_code == 400:
            # Model tertentu tidak mendukung thinkingConfig -> ulangi sekali tanpa itu.
            muatan["generationConfig"].pop("thinkingConfig")
            res = httpx.post(url, json=muatan, headers=kepala, timeout=BATAS_WAKTU_DETIK)
    except httpx.HTTPError as err:
        raise GagalAI(f"jaringan: {type(err).__name__}") from err
    if res.status_code != 200:
        raise GagalAI(f"HTTP {res.status_code}: {res.text[:200]}")
    try:
        data = res.json()
        bagian = data["candidates"][0]["content"]["parts"]
        teks_balasan = "".join(p.get("text", "") for p in bagian if not p.get("thought"))
    except (ValueError, KeyError, IndexError, TypeError) as err:
        raise GagalAI("format balasan tidak dikenal") from err
    if not teks_balasan.strip():
        raise GagalAI("balasan kosong")
    return teks_balasan


# ---------------------------------------------------------------- batas pemakaian (kasar, per instance)

_hitungan = {}


def melewati_batas(perangkat_id, soal_id):
    """Batas kasar per instance server: MAKS_PESAN_PER_SOAL pesan per perangkat per soal per jam."""
    sekarang = time.time()
    kunci = (perangkat_id, soal_id)
    awal, jumlah = _hitungan.get(kunci, (sekarang, 0))
    if sekarang - awal > 3600:
        awal, jumlah = sekarang, 0
    jumlah += 1
    _hitungan[kunci] = (awal, jumlah)
    if len(_hitungan) > 5000:  # cegah memori membengkak
        _hitungan.clear()
    return jumlah > MAKS_PESAN_PER_SOAL


# ---------------------------------------------------------------- fungsi utama

def _petunjuk_statis(soal, tingkat):
    teks = logika.petunjuk(soal, max(1, min(tingkat, 3)))
    return teks or "Baca lagi soalnya pelan-pelan. Bagian mana yang membuatmu ragu?"


def bimbing(soal, tahap, tingkat=1, jawaban_salah=None, pesan_salah=None, riwayat=None, pertanyaan=None):
    """Mengembalikan {teks, sumber: 'ai'|'statis', fase, catatan}."""
    fase = fase_dari_tahap(tahap)
    if pertanyaan and not aktif():
        return {
            "teks": "Pembimbing AI belum aktif. Tekan tombol Tanya Pembimbing untuk petunjuk, ya.",
            "sumber": "statis", "fase": fase, "catatan": "ai-nonaktif",
        }
    if not aktif():
        return {"teks": _petunjuk_statis(soal, tingkat), "sumber": "statis", "fase": fase, "catatan": "ai-nonaktif"}
    prompt = buat_prompt(soal, tahap, tingkat, jawaban_salah, pesan_salah, riwayat, pertanyaan)
    try:
        teks = bersihkan(_panggil_gemini(SISTEM, prompt))
    except GagalAI as err:
        print(f"[ai] Gemini gagal: {err}")  # muncul di log Vercel
        return {"teks": _petunjuk_statis(soal, tingkat), "sumber": "statis", "fase": fase, "catatan": "gagal"}
    if not teks or bocor(teks, soal):
        cadangan = (
            "Jawaban akhirnya kamu yang temukan, ya. Lihat lagi langkah yang sedang kamu kerjakan: apa yang perlu dicek?"
            if pertanyaan else _petunjuk_statis(soal, tingkat)
        )
        return {"teks": cadangan, "sumber": "statis", "fase": fase, "catatan": "disaring"}
    return {"teks": teks, "sumber": "ai", "fase": fase, "catatan": None}


def tanggapi_refleksi(soal, alasan, jawaban_siswa=None):
    statis = (
        f"Terima kasih sudah menjelaskan! Ingat, FPB adalah faktor persekutuan yang PALING BESAR, "
        f"jadi {soal['jawaban']} dipilih karena tidak ada faktor sama yang lebih besar. "
        "Kapan lagi kamu perlu membagi benda sama banyak?"
    )
    if not aktif():
        return {"teks": statis, "sumber": "statis", "fase": "refleksi", "catatan": "ai-nonaktif"}
    try:
        teks = bersihkan(_panggil_gemini(SISTEM_REFLEKSI, buat_prompt_refleksi(soal, alasan, jawaban_siswa)))
    except GagalAI as err:
        print(f"[ai] Gemini gagal (refleksi): {err}")
        return {"teks": statis, "sumber": "statis", "fase": "refleksi", "catatan": "gagal"}
    return {"teks": teks or statis, "sumber": "ai" if teks else "statis", "fase": "refleksi", "catatan": None}
