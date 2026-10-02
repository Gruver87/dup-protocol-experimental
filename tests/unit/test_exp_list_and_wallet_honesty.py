"""Experimental: list endpoints 503 on failure; /wallet/create no hash-demo address."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_wallet_create_no_invented_address():
    src = (ROOT / "api" / "http.py").read_text(encoding="utf-8")
    chunk = src.split('path == "/wallet/create"')[1].split("elif path")[0]
    assert "ecdsa not available" not in chunk
    assert "wallet create unavailable" in chunk
    assert "sha256_hex(str(_t.time())" not in chunk


def test_list_exception_paths_use_503():
    src = (ROOT / "api" / "http.py").read_text(encoding="utf-8")
    for needle in (
        "consensus stats failed",
        "smart_accounts list failed",
        "multisig list failed",
    ):
        assert needle in src
