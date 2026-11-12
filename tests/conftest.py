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
    import db

    db.hapus_cache()
    db.simpanan_lokal()["jawaban"].clear()
    db.simpanan_lokal()["hasil_uji"].clear()
    yield


@pytest.fixture(scope="session")
def kasus():
    with open(AKAR / "tests" / "kasus_fpb.json", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def konten():
    with open(AKAR / "api" / "data" / "konten.json", encoding="utf-8") as f:
        return json.load(f)
