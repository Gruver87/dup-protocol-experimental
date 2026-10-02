"""Exp mid-soak: AI honesty + NFT settlement/offer/auction guards."""

from __future__ import annotations

import tempfile
import time
from pathlib import Path
from unittest.mock import MagicMock

import pytest

ROOT = Path(__file__).resolve().parents[2]


def test_nft_settle_raises_on_royalty_fail_rolls_back_balances():
    from features.nft import NFTMarketplace
    from storage.database import Database

    tmp = tempfile.mkdtemp()
    db = Database(f"{tmp}/nft_royalty.db")
    db.initialize()
    seller = "0x" + "a" * 40
    buyer = "0x" + "b" * 40
    creator = "0x" + "c" * 40
    db.set_balance(seller, 1000.0)
    db.set_balance(buyer, 1000.0)
    db.set_balance(creator, 1.0)

    m = NFTMarketplace(db=db)
    m.tokens.clear()
    assert m.mint("t1", "n", "d", "i", creator, price=10.0)["success"]
    # Transfer to seller without sale settle
    m.tokens["t1"].owner = seller
    m.tokens["t1"].for_sale = True
    m.tokens["t1"].price = 10.0
    from runtime.amount import to_satoshi

    m.tokens["t1"].price_satoshi = int(to_satoshi(10))

    # Break royalty credit mid-settle after buyer debit would have applied —
    # apply_store_delta raises via monkeypatch on creator credit.
    real_apply = __import__("runtime.amount", fromlist=["apply_store_delta_satoshi"]).apply_store_delta_satoshi
    calls = {"n": 0}

    def _flaky(store, addr, delta, **kw):
        calls["n"] += 1
        # 1=buyer debit, 2=seller credit, 3=royalty → fail royalty
        if calls["n"] >= 3 and addr == creator:
            return False
        return real_apply(store, addr, delta, **kw)

    import runtime.amount as amt

    monkey = pytest.MonkeyPatch()
    monkey.setattr(amt, "apply_store_delta_satoshi", _flaky)
    try:
        bal_b0 = db.get_balance(buyer)
        bal_s0 = db.get_balance(seller)
        out = m.buy("t1", buyer)
        assert out.get("success") is False
        assert "nft_settle_failed" in str(out.get("error", "")) or "nft_uow" in str(
            out.get("error", "")
        )
        # Atomic rollback — balances unchanged
        assert db.get_balance(buyer) == bal_b0
        assert db.get_balance(seller) == bal_s0
        assert m.get_token("t1")["owner"] == seller
    finally:
        monkey.undo()


def test_offer_expired_refuse_and_cancel():
    from features.nft import NFTMarketplace
    from storage.database import Database

    tmp = tempfile.mkdtemp()
    db = Database(f"{tmp}/nft_offer.db")
    db.initialize()
    seller = "0x" + "a" * 40
    buyer = "0x" + "b" * 40
    db.set_balance(seller, 1000.0)
    db.set_balance(buyer, 1000.0)
    m = NFTMarketplace(db=db)
    m.tokens.clear()
    assert m.mint("o1", "O", "d", "i", seller, price=5.0)["success"]
    oid = m.make_offer("o1", buyer, price=5.0, hours=1)
    assert oid
    m.offers[oid]["expires_at"] = int(time.time()) - 5
    bad = m.accept_offer(oid, seller)
    assert bad["success"] is False
    assert "expired" in bad["error"].lower()

    oid2 = m.make_offer("o1", buyer, price=5.0, hours=1)
    assert m.cancel_offer(oid2, buyer)["success"] is True
    assert m.accept_offer(oid2, seller)["success"] is False


def test_finalize_auction_before_ends_at_refused():
    from features.nft import NFTMarketplace
    from storage.database import Database

    tmp = tempfile.mkdtemp()
    db = Database(f"{tmp}/nft_auc.db")
    db.initialize()
    seller = "0x" + "a" * 40
    buyer = "0x" + "b" * 40
    db.set_balance(seller, 1000.0)
    db.set_balance(buyer, 1000.0)
    m = NFTMarketplace(db=db)
    m.tokens.clear()
    assert m.mint("a1", "A", "d", "i", seller, price=5.0)["success"]
    aid = m.create_auction("a1", seller, start_price=1.0, reserve_price=1.0, hours=1)
    assert aid
    assert m.place_bid(aid, buyer, amount=2.0)["success"]
    early = m.finalize_auction(aid)
    assert early["success"] is False
    assert "ends_at" in early["error"] or "still active" in early["error"].lower()


def test_nft_stats_enabled_follows_balance_backend():
    from features.nft import NFTMarketplace

    m = NFTMarketplace(db=None)
    st = m.get_stats()
    assert st["enabled"] is False
    assert st["offers_escrow"] is False
    assert st["auction_escrow"] is False


def test_main_no_ai_validator_forge_hook():
    src = (ROOT / "main.py").read_text(encoding="utf-8")
    assert "ai_validator.update_performance" not in src


def test_ai_http_source_honesty_needles():
    src = (ROOT / "api" / "http.py").read_text(encoding="utf-8")
    chunk = src.split('path == "/ai/validators"')[1].split("elif path == \"/ai/proposer\"")[0]
    assert "feature_ai_validator" in chunk
    assert "honesty" in chunk


def test_sdk_no_invent_price_satoshi():
    src = (ROOT / "sdk" / "dup_sdk" / "client.py").read_text(encoding="utf-8")
    chunk = src.split("def get_nft_token")[1].split("def get_nft_by_owner")[0]
    assert "to_satoshi(out[\"price\"])" not in chunk
    assert "never invent price_satoshi" in chunk


def test_ai_ops_honesty_constant():
    from features import ai_ops

    assert "not consensus" in ai_ops.HONESTY.lower()
