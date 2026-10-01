"""NFT marketplace sprout harden — satoshi prices, prod flag freeze (not consensus)."""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from features.nft import NFTMarketplace, resolve_price_satoshi
from runtime.amount import to_satoshi
from storage.database import Database


def test_resolve_price_refuses_dust_float():
    with pytest.raises(ValueError, match="non-integral"):
        resolve_price_satoshi(price=1.25)


def test_resolve_price_satoshi_int():
    assert resolve_price_satoshi(price_satoshi=42) == 42


def test_list_refuses_dust_float():
    tmp = tempfile.mkdtemp()
    db = Database(os.path.join(tmp, "n.db"))
    db.initialize()
    owner = "0x" + "a" * 40
    db.set_balance(owner, 100.0)
    m = NFTMarketplace(db=db)
    m.tokens.clear()
    m.mint("t1", "n", "d", "i", owner, 0.0)
    out = m.list_for_sale("t1", owner, price=3.14)
    assert out["success"] is False
    assert "price_satoshi" in out["error"] or "non-integral" in out["error"]


def test_mint_list_buy_satoshi_roundtrip():
    tmp = tempfile.mkdtemp()
    db = Database(os.path.join(tmp, "n2.db"))
    db.initialize()
    seller = "0x" + "c" * 40
    buyer = "0x" + "d" * 40
    db.set_balance(seller, 500.0)
    db.set_balance(buyer, 500.0)
    m = NFTMarketplace(db=db)
    m.tokens.clear()
    r = m.mint("t2", "n", "d", "i", seller, price_satoshi=int(to_satoshi(5)))
    assert r["success"] is True
    assert r["price_satoshi"] == int(to_satoshi(5))
    listed = m.list_for_sale("t2", seller, price_satoshi=int(to_satoshi(12)))
    assert listed["price_satoshi"] == int(to_satoshi(12))
    buy = m.buy("t2", buyer)
    assert buy["success"] is True
    assert buy["price_satoshi"] == int(to_satoshi(12))
    assert m.get_token("t2")["owner"] == buyer
    st = m.get_stats()
    assert st["consensus_wired"] is False
    assert "honesty" in st


def test_prod_mesh_feature_nft_false():
    for name in ("node.prod.mesh1.json", "node.prod.mesh2.json", "node.prod.mesh3.json"):
        data = json.loads((ROOT / "docker" / name).read_text(encoding="utf-8"))
        assert data.get("feature_nft") is False


def test_sdk_nft_read_helpers_mocked():
    from unittest import mock
    from sdk.dup_sdk import Client

    c = Client("http://127.0.0.1:19080")

    def fake_urlopen(req, timeout=None, context=None):
        class R:
            status = 200

            def read(self):
                url = req.full_url
                if url.endswith("/nft/stats"):
                    return json.dumps(
                        {"total_tokens": 1, "consensus_wired": False, "tier": "app-profile"}
                    ).encode()
                if "/nft/token/" in url:
                    return json.dumps(
                        {"token_id": "t", "price": 2.0, "price_satoshi": 2_000_000}
                    ).encode()
                if url.endswith("/nft/listings"):
                    return json.dumps([]).encode()
                return json.dumps({}).encode()

            def __enter__(self):
                return self

            def __exit__(self, *a):
                return False

        return R()

    with mock.patch("urllib.request.urlopen", fake_urlopen):
        st = c.get_nft_stats()
        assert st["total_tokens"] == 1
        tok = c.get_nft_token("t")
        assert tok["price_satoshi"] == 2_000_000
        assert c.get_nft_listings() == []
