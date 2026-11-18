import json
import sys
from pathlib import Path

import pytest

AKAR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AKAR / "api"))


@pytest.fixture(autouse=True)
def mode_lokal(monkeypatch):
    """Semua test memakai data lokal (api/data/konten.json), tidak pernah menyentuh Supabase."""
    monkeypatch.delenv("SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_SERVICE_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)  # test TIDAK PERNAH memanggil Gemini sungguhan
    monkeypatch.delenv("GEMINI_MODEL", raising=False)
    import ai
    import db

    db.hapus_cache()
    ai._hitungan.clear()
    for daftar in db.simpanan_lokal().values():
        daftar.clear()
    yield


@pytest.fixture(scope="session")
def kasus():
    with open(AKAR / "tests" / "kasus_fpb.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def konten():
    with open(AKAR / "api" / "data" / "konten.json", encoding="utf-8") as f:
        return json.load(f)
