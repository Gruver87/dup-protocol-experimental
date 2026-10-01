"""Unit tests for sdk.dup_sdk (mocked HTTP; no mesh / no soak)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest import mock

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sdk.dup_sdk import Client, HONESTY, MoneyRefuse, HttpError, RpcError, require_satoshi
from sdk.dup_sdk.amount import to_satoshi, wei_hex_to_satoshi, WEI_PER_SATOSHI


def test_honesty_banner():
    assert "not mainnet" in HONESTY


def test_verify_tls_false_refused():
    with pytest.raises(ValueError, match="verify_tls"):
        Client("http://127.0.0.1:18180", verify_tls=False)  # type: ignore[arg-type]


def test_require_satoshi_prefers_int():
    assert require_satoshi(satoshi=1_500_000) == 1_500_000


def test_require_satoshi_refuses_float_satoshi():
    with pytest.raises(MoneyRefuse):
        require_satoshi(satoshi=1.5)


def test_require_satoshi_refuses_dust_float_abs():
    with pytest.raises(MoneyRefuse):
        require_satoshi(abs_amount=1.25)


def test_require_satoshi_whole_abs_int():
    assert require_satoshi(abs_amount=2) == int(to_satoshi(2))


def test_wei_hex_to_satoshi():
    sat = 7
    wei_hex = hex(sat * WEI_PER_SATOSHI)
    assert wei_hex_to_satoshi(wei_hex) == sat


class _FakeResp:
    def __init__(self, payload, status=200):
        self._payload = payload
        self.status = status

    def read(self):
        if isinstance(self._payload, (bytes, bytearray)):
            return bytes(self._payload)
        return json.dumps(self._payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def test_status_and_health_mocked():
    c = Client("http://127.0.0.1:18180")
    calls = []

    def fake_urlopen(req, timeout=None, context=None):
        url = req.full_url
        calls.append(url)
        if "/health/live" in url:
            return _FakeResp({"ok": True, "live": True})
        if "/health/ready" in url:
            return _FakeResp({"ready": True})
        if "probe=1" in url:
            return _FakeResp({"probe": True, "height": 3})
        if url.rstrip("/").endswith("/status") or "/status?" in url:
            return _FakeResp({"height": 3})
        raise AssertionError(url)

    with mock.patch("urllib.request.urlopen", fake_urlopen):
        assert c.health_live()["live"] is True
        assert c.health_ready()["ready"] is True
        assert c.status()["height"] == 3
        assert c.status_probe()["probe"] is True


def test_get_balance_satoshi_rest():
    c = Client("http://127.0.0.1:18180")

    def fake_urlopen(req, timeout=None, context=None):
        return _FakeResp(
            {"address": "0xabc", "balance": 1.5, "balance_satoshi": 1_500_000}
        )

    with mock.patch("urllib.request.urlopen", fake_urlopen):
        assert c.get_balance_satoshi("0xabc") == 1_500_000
        bal = c.get_balance("0xabc")
        assert bal["balance_satoshi"] == 1_500_000


def test_get_balance_satoshi_rpc_fallback():
    c = Client("http://127.0.0.1:18180")
    sat = 42
    wei = hex(sat * WEI_PER_SATOSHI)

    def fake_urlopen(req, timeout=None, context=None):
        body = req.data.decode("utf-8") if req.data else ""
        if req.get_method() == "GET":
            import urllib.error

            raise urllib.error.HTTPError(
                req.full_url, 404, "missing", hdrs=None, fp=None
            )
        assert "eth_getBalance" in body
        return _FakeResp({"jsonrpc": "2.0", "id": 1, "result": wei})

    with mock.patch("urllib.request.urlopen", fake_urlopen):
        assert c.get_balance_satoshi("0xabc") == sat


def test_get_block_number():
    c = Client("http://127.0.0.1:18180")

    def fake_urlopen(req, timeout=None, context=None):
        return _FakeResp({"jsonrpc": "2.0", "id": 1, "result": "0x10"})

    with mock.patch("urllib.request.urlopen", fake_urlopen):
        assert c.get_block_number() == 16


def test_rpc_error_raises():
    c = Client("http://127.0.0.1:18180")

    def fake_urlopen(req, timeout=None, context=None):
        return _FakeResp(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "error": {"code": -32000, "message": "boom"},
            }
        )

    with mock.patch("urllib.request.urlopen", fake_urlopen):
        with pytest.raises(RpcError, match="boom"):
            c.rpc("eth_blockNumber")


def test_submit_signed_tx_refuses_dust_float():
    c = Client("http://127.0.0.1:18180")
    with pytest.raises(MoneyRefuse):
        c.submit_signed_tx({"from": "0xa", "to": "0xb", "amount": 1.25, "fee": 0.01})


def test_submit_signed_tx_raw():
    c = Client("http://127.0.0.1:18180")

    def fake_urlopen(req, timeout=None, context=None):
        return _FakeResp({"jsonrpc": "2.0", "id": 1, "result": "0xdead"})

    with mock.patch("urllib.request.urlopen", fake_urlopen):
        out = c.submit_signed_tx(raw_tx_hex="dead")
        assert out["tx_hash"] == "0xdead"


def test_submit_signed_tx_body_satoshi():
    c = Client("http://127.0.0.1:18180")
    seen = {}

    def fake_urlopen(req, timeout=None, context=None):
        seen["body"] = json.loads(req.data.decode("utf-8"))
        return _FakeResp({"tx_hash": "0xabc", "status": "pending", "trace_url": "/tx/trace/0xabc"})

    with mock.patch("urllib.request.urlopen", fake_urlopen):
        out = c.submit_signed_tx(
            {
                "from": "0xa",
                "to": "0xb",
                "amount_satoshi": 1_000_000,
                "fee_satoshi": 1000,
                "signature": "s",
                "public_key": "p",
            }
        )
        assert out["tx_hash"] == "0xabc"
        assert seen["body"]["amount_satoshi"] == 1_000_000
        assert seen["body"]["fee_satoshi"] == 1000


def test_get_tx_receipt_rest():
    c = Client("http://127.0.0.1:18180")

    def fake_urlopen(req, timeout=None, context=None):
        return _FakeResp(
            {
                "tx_hash": "0x1",
                "block_height": 9,
                "status": 1,
                "value_satoshi": 100,
                "fee_satoshi": 1,
                "burned_satoshi": 0,
            }
        )

    with mock.patch("urllib.request.urlopen", fake_urlopen):
        rcpt = c.get_tx_receipt("0x1")
        assert rcpt["value_satoshi"] == 100
        assert rcpt["block_height"] == 9


def test_http_error_surface():
    c = Client("http://127.0.0.1:18180")

    def fake_urlopen(req, timeout=None, context=None):
        import urllib.error
        from io import BytesIO

        raise urllib.error.HTTPError(
            req.full_url,
            503,
            "down",
            hdrs=None,
            fp=BytesIO(b'{"error":"down"}'),
        )

    with mock.patch("urllib.request.urlopen", fake_urlopen):
        with pytest.raises(HttpError) as ei:
            c.health_live()
        assert ei.value.status == 503

def test_bearer_and_api_key_headers():
    c = Client(
        "http://127.0.0.1:18180",
        api_key="rpc-key-abc",
        bearer_token="jwt-or-key-xyz",
    )
    assert c.auth_configured() is True
    seen = {}

    def fake_urlopen(req, timeout=None, context=None):
        seen["Authorization"] = req.get_header("Authorization")
        seen["X-API-Key"] = req.headers.get("X-api-key") or req.headers.get("X-API-Key")
        return _FakeResp({"jsonrpc": "2.0", "id": 1, "result": "0x2a"})

    with mock.patch("urllib.request.urlopen", fake_urlopen):
        assert c.get_block_number() == 42
    assert seen["Authorization"] == "Bearer jwt-or-key-xyz"
    assert seen["X-API-Key"] == "rpc-key-abc"


def test_placeholder_bearer_refused():
    with pytest.raises(ValueError, match="placeholder"):
        Client("http://127.0.0.1:18180", bearer_token="changeme")


def test_from_env_loads_auth(monkeypatch):
    monkeypatch.setenv("DUP_SDK_BASE_URL", "http://127.0.0.1:18180")
    monkeypatch.setenv("DUP_SDK_API_KEY", "k1")
    monkeypatch.setenv("DUP_SDK_BEARER", "b1")
    c = Client.from_env()
    assert c.api_key == "k1"
    assert c.bearer_token == "b1"
    assert c.auth_configured() is True


def test_from_env_rpc_api_keys_first(monkeypatch):
    monkeypatch.setenv("DUP_SDK_BASE_URL", "http://127.0.0.1:18180")
    monkeypatch.delenv("DUP_SDK_API_KEY", raising=False)
    monkeypatch.delenv("DUP_SDK_BEARER", raising=False)
    monkeypatch.delenv("DUP_SDK_JWT", raising=False)
    monkeypatch.delenv("ABS_ADMIN_JWT", raising=False)
    monkeypatch.setenv("RPC_API_KEYS", "first-key,second-key")
    c = Client.from_env()
    assert c.api_key == "first-key"
