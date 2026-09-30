"""Console wallet helpers + probe rpc_port honesty."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def test_abs_to_wei_hex_in_wallets_js():
    js = (ROOT / "web" / "console" / "assets" / "wallets.js").read_text(encoding="utf-8")
    assert "function absToWeiHex" in js
    assert "eth_sendTransaction" in js
    assert "wallet_addEthereumChain" in js
    assert "wallet_switchEthereumChain" in js
    assert "private_key" not in js.lower() or "never" in js.lower()


def test_console_has_council_and_theme():
    html = (ROOT / "web" / "console" / "index.html").read_text(encoding="utf-8")
    assert 'data-view="council"' in html
    assert 'data-view="evm"' in html
    assert 'data-view="features"' in html
    assert 'data-view="evidence"' in html
    assert "DUP PROTOCOL" in html or "DUP Protocol" in html
    assert "theme.js" in html
    assert "eth-rpc" in html
    css = (ROOT / "web" / "console" / "assets" / "console.css").read_text(encoding="utf-8")
    assert '[data-theme="light"]' in css
    app = (ROOT / "web" / "console" / "assets" / "app.js").read_text(encoding="utf-8")
    assert "renderCouncil" in app
    assert "renderEvm" in app
    assert "renderFeatures" in app
    assert "renderEvidence" in app
    assert "/evm/status" in app
    assert "/features" in app
    assert "/p2p/peer-score" in app
    assert "/p2p/reconnect" in app
    assert "/council/stats" in app
    assert "778889" in app
    assert "778888" in app


def test_console_api_has_post_json():
    api = (ROOT / "web" / "console" / "assets" / "api.js").read_text(encoding="utf-8")
    assert "postJson" in api
    assert "eth_sendTransaction" not in api  # wallets only


def test_probe_payload_includes_rpc_ports():
    import ast

    http = (ROOT / "api" / "http.py").read_text(encoding="utf-8")
    assert '"rpc_port"' in http
    # Narrow: probe builder must expose rpc_port for console JSON-RPC derive.
    idx = http.find("def _build_status_probe_payload")
    assert idx > 0
    chunk = http[idx : idx + 6500]
    assert "rpc_port" in chunk
    assert "mesh_min_peers" in chunk
    assert "coin_symbol" in chunk
