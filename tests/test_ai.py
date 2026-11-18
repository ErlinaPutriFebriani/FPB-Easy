"""Test Pembimbing AI (RMT). Gemini TIDAK pernah dipanggil sungguhan: httpx.post di-mock."""
import pytest

import ai


def cari(konten, soal_id):
    return next(s for s in konten["soal"] if s["id"] == soal_id)


class ResPalsu:
    def __init__(self, teks, status=200):
        self.status_code = status
        self._teks = teks
        self.text = "" if status == 200 else teks

    def json(self):
        return {"candidates": [{"content": {"parts": [{"text": self._teks}]}}]}


@pytest.fixture
def gemini(monkeypatch):
    """Aktifkan AI dengan kunci palsu. Mengembalikan muatan yang terkirim + balasan yang bisa diatur."""
    import httpx

    terkirim = []
    balasan = {"teks": "Lihat lagi baris faktor 28. Angka mana yang juga ada di faktor 20?", "status": 200}

    def post(url, json=None, headers=None, timeout=None):
        terkirim.append({"url": url, "json": json, "headers": headers})
        return ResPalsu(balasan["teks"], balasan["status"])

    monkeypatch.setenv("GEMINI_API_KEY", "kunci-palsu")
    monkeypatch.setattr(httpx, "post", post)
    return {"terkirim": terkirim, "balasan": balasan}


def test_fase_rmt():
    assert ai.fase_dari_tahap("pilih_sel") == "input"
    assert ai.fase_dari_tahap("ditanya") == "input"
    assert ai.fase_dari_tahap("rencana") == "elaborasi"
    assert ai.fase_dari_tahap("fpb") == "elaborasi"
    assert ai.fase_dari_tahap("kesimpulan") == "output"
    assert set(ai.TUGAS_TAHAP) <= set(ai.FASE_RMT)


def test_prompt_memuat_tahap_fase_tingkat_dan_jawaban_salah(konten):
    s = cari(konten, "tabel-a")
    p = ai.buat_prompt(s, "pilih_sel", 2, jawaban_salah=[[0, 2]], pesan_salah="Bukan harga.")
    assert "mengetuk angka di tabel" in p
    assert "Input" in p
    assert "tingkat 2" in p
    assert "Harga Pensil (Rp2.000)" in p          # sel yang salah dijelaskan dengan kata-kata
    assert "Pensil | 48 | Rp2.000" in p           # tabel ikut dikirim sebagai teks
    p3 = ai.buat_prompt(s, "fpb", 3)
    assert "tingkat 3" in p3 and "Elaborasi" in p3


def test_prompt_pertanyaan_bebas_dan_riwayat(konten):
    s = cari(konten, "langsung-b")
    p = ai.buat_prompt(s, "fpb", 1, riwayat=[{"peran": "siswa", "teks": "bingung"}], pertanyaan="faktor itu apa?")
    assert "jawab pertanyaan siswa berikut" in p and "faktor itu apa?" in p
    assert "Siswa: bingung" in p


def test_sistem_melarang_jawaban_akhir_dan_mengatur_beban_kognitif():
    assert "JANGAN PERNAH menyebutkan nilai FPB akhir" in ai.SISTEM
    assert "HANYA langkah yang sedang dikerjakan" in ai.SISTEM      # intrinsic load
    assert "Paling banyak 2 kalimat" in ai.SISTEM                   # extraneous load
    assert "SATU pertanyaan penuntun" in ai.SISTEM                  # germane load


@pytest.mark.parametrize("teks", [
    "FPB dari 20 dan 28 adalah 4.",
    "Jadi FPB-nya = 4, ya.",
    "Jawabannya 4.",
    "Hasilnya adalah 4.",
])
def test_bocor_terdeteksi(konten, teks):
    assert ai.bocor(teks, cari(konten, "langsung-b"))


def test_bocor_kesimpulan_dan_paket(konten):
    s = cari(konten, "tabel-a")
    assert ai.bocor("Paling banyak 12 paket, tiap paket berisi 4 pensil dan 3 buku.", s)
    assert ai.bocor("Bisa dibuat 12 paket.", s)


def test_tidak_bocor_untuk_bimbingan_wajar(konten):
    s = cari(konten, "langsung-b")
    assert not ai.bocor("Lihat lagi faktor 20: 1, 2, 4, 5, 10, 20. Angka mana yang ada juga di faktor 28?", s)


def test_bersihkan_markdown_emoji_dan_panjang():
    assert ai.bersihkan("**Coba** lihat\n- baris `28` \U0001F60A") == "Coba lihat baris 28"
    panjang = "Kalimat pertama cukup panjang untuk diuji. " * 20
    hasil = ai.bersihkan(panjang)
    assert len(hasil) <= ai.MAKS_KARAKTER_BALASAN and hasil.endswith(".")


def test_tanpa_kunci_pakai_petunjuk_statis(konten):
    s = cari(konten, "tabel-a")
    h = ai.bimbing(s, "pilih_sel", 2)
    assert h["sumber"] == "statis" and h["teks"] == s["petunjuk"][1] and h["fase"] == "input"
    h2 = ai.bimbing(s, "fpb", 1, pertanyaan="halo")
    assert h2["sumber"] == "statis" and "belum aktif" in h2["teks"]


def test_dengan_gemini(konten, gemini):
    s = cari(konten, "langsung-b")
    h = ai.bimbing(s, "fpb", 1, jawaban_salah=2)
    assert h == {"teks": gemini["balasan"]["teks"], "sumber": "ai", "fase": "elaborasi", "catatan": None}
    kirim = gemini["terkirim"][0]
    assert kirim["headers"]["x-goog-api-key"] == "kunci-palsu"
    assert ":generateContent" in kirim["url"]
    assert "JANGAN PERNAH" in kirim["json"]["system_instruction"]["parts"][0]["text"]
    assert "JAWABAN SALAH TERAKHIR SISWA: 2" in kirim["json"]["contents"][0]["parts"][0]["text"]


def test_pengaturan_berpikir_per_versi_model(konten, gemini, monkeypatch):
    s = cari(konten, "langsung-b")
    ai.bimbing(s, "fpb", 1)
    assert gemini["terkirim"][-1]["json"]["generationConfig"]["thinkingConfig"] == {"thinkingLevel": "minimal"}
    monkeypatch.setenv("GEMINI_MODEL", "gemini-2.5-flash")
    ai.bimbing(s, "fpb", 1)
    assert gemini["terkirim"][-1]["json"]["generationConfig"]["thinkingConfig"] == {"thinkingBudget": 0}


def test_400_diulang_tanpa_thinking(konten, monkeypatch):
    import httpx

    terkirim = []

    def post(url, json=None, headers=None, timeout=None):
        terkirim.append(json["generationConfig"].copy())
        return ResPalsu("Coba lihat lagi faktornya. Mana yang paling besar?", 400 if len(terkirim) == 1 else 200)

    monkeypatch.setenv("GEMINI_API_KEY", "kunci-palsu")
    monkeypatch.setattr(httpx, "post", post)
    h = ai.bimbing(cari(konten, "langsung-b"), "fpb", 1)
    assert h["sumber"] == "ai"
    assert "thinkingConfig" in terkirim[0] and "thinkingConfig" not in terkirim[1]


def test_model_dihentikan_404_pakai_model_cadangan(konten, monkeypatch):
    import httpx

    url_dipakai = []

    def post(url, json=None, headers=None, timeout=None):
        url_dipakai.append(url)
        if ai.MODEL_CADANGAN in url:
            return ResPalsu("Coba lihat lagi faktornya. Mana yang paling besar?")
        return ResPalsu("model is no longer available", 404)

    monkeypatch.setenv("GEMINI_API_KEY", "kunci-palsu")
    monkeypatch.setattr(httpx, "post", post)
    h = ai.bimbing(cari(konten, "langsung-b"), "fpb", 1)
    assert h["sumber"] == "ai"
    assert ai.MODEL_BAWAAN in url_dipakai[0] and ai.MODEL_CADANGAN in url_dipakai[-1]


def test_gemini_bocor_diganti_statis(konten, gemini):
    s = cari(konten, "langsung-b")
    gemini["balasan"]["teks"] = "Gampang, FPB-nya adalah 4."
    h = ai.bimbing(s, "fpb", 2)
    assert h["sumber"] == "statis" and h["catatan"] == "disaring" and h["teks"] == s["petunjuk"][1]
    h2 = ai.bimbing(s, "fpb", 1, pertanyaan="jawabannya berapa?")
    assert h2["sumber"] == "statis" and "kamu yang temukan" in h2["teks"]


def test_gemini_error_pakai_statis(konten, gemini):
    s = cari(konten, "langsung-b")
    gemini["balasan"]["status"] = 500
    h = ai.bimbing(s, "fpb", 3)
    assert h["sumber"] == "statis" and h["catatan"] == "gagal" and h["teks"] == s["petunjuk"][2]


def test_refleksi(konten, gemini):
    s = cari(konten, "langsung-b")
    gemini["balasan"]["teks"] = "Tepat, 4 paling besar. Kapan lagi kamu membagi benda sama banyak?"
    h = ai.tanggapi_refleksi(s, "karena paling besar", 4)
    assert h["sumber"] == "ai" and h["fase"] == "refleksi"
    assert "ALASAN SISWA" in gemini["terkirim"][0]["json"]["contents"][0]["parts"][0]["text"]


def test_petunjuk_statis_tidak_menyebut_jawaban_akhir(konten):
    """Petunjuk statis adalah cadangan AI, jadi juga tidak boleh langsung memberi jawaban akhir."""
    import re

    for s in konten["soal"]:
        for p in s.get("petunjuk") or []:
            assert not ai.bocor(p, s), (s["id"], p)
            assert not re.search(r"(FPB\s*=|terbesar(nya)?\s+(adalah\s+)?\d)", p, re.IGNORECASE), (s["id"], p)


def test_batas_pesan_per_soal():
    for _ in range(ai.MAKS_PESAN_PER_SOAL):
        assert not ai.melewati_batas("p1", "s1")
    assert ai.melewati_batas("p1", "s1")
    assert not ai.melewati_batas("p2", "s1")
