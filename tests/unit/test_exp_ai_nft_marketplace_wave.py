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


def test_soft_escrow_offer_and_cancel_auction():
    from features.nft import NFTMarketplace
    from runtime.amount import to_satoshi
    from storage.database import Database

    tmp = tempfile.mkdtemp()
    db = Database(f"{tmp}/nft_escrow.db")
    db.initialize()
    seller = "0x" + "a" * 40
    buyer = "0x" + "b" * 40
    db.set_balance(seller, 1000.0)
    db.set_balance(buyer, 1000.0)
    m = NFTMarketplace(db=db)
    m.tokens.clear()
    assert m.mint("e1", "E", "d", "i", seller, price=5.0)["success"]
    bal0 = db.get_balance(buyer)
    oid = m.make_offer("e1", buyer, price_satoshi=int(to_satoshi(5)), hours=1)
    assert oid
    assert int(m.offers[oid]["held_satoshi"]) == int(to_satoshi(5))
    assert abs(db.get_balance(buyer) - (bal0 - 5.0)) < 1e-9
    assert m.cancel_offer(oid, buyer)["success"] is True
    assert abs(db.get_balance(buyer) - bal0) < 1e-9

    assert m.mint("e2", "E2", "d", "i", seller, price=5.0)["success"]
    aid = m.create_auction(
        "e2",
        seller,
        start_price_satoshi=int(to_satoshi(1)),
        reserve_price_satoshi=int(to_satoshi(1)),
        hours=1,
    )
    assert aid
    assert m.place_bid(aid, buyer, amount_satoshi=int(to_satoshi(4)))["success"]
    bal1 = db.get_balance(buyer)
    out = m.cancel_auction(aid, seller)
    assert out["success"] is True
    assert int(out["refunded_satoshi"]) == int(to_satoshi(4))
    assert abs(db.get_balance(buyer) - (bal1 + 4.0)) < 1e-9
    st = m.get_stats()
    assert st["offers_escrow"] is True
    assert st["auction_escrow"] is True


def test_main_no_ai_validator_forge_hook():
    src = (ROOT / "main.py").read_text(encoding="utf-8")
    assert "ai_validator.update_performance" not in src


def test_ai_http_source_honesty_needles():
    src = (ROOT / "api" / "http.py").read_text(encoding="utf-8")
    chunk = src.split('path == "/ai/validators"')[1].split("elif path == \"/ai/proposer\"")[0]
    assert "feature_ai_validator" in chunk or "_ai_sprout_enabled" in chunk
    assert "honesty" in chunk
    assert "_ai_sprout_enabled" in src
    assert "_nft_sprout_enabled" in src
    assert "_nft_disabled_payload" in src
    assert 'feature_attr="feature_ai_agents"' in src
    assert "/ai-agent/stats" in src
    agent_chunk = src.split('path == "/ai-agent/create"')[1].split("elif path == \"/ai-agent/predict\"")[0]
    assert "feature_ai_agents" in agent_chunk
    reg = src.split('path == "/ai/register-validator"')[1].split("elif path ==")[0]
    assert "_ai_sprout_enabled" in reg
    assert "feature_ai_validator" in reg
    offer = src.split('path == "/nft/offer"')[1].split("elif path ==")[0]
    assert '"offers_escrow": False' not in offer
    assert "held_satoshi" in offer
    assert "nft_enabled" in src
    assert "ai_validator_enabled" in src


def test_main_ai_nft_feature_defaults_fail_closed():
    src = (ROOT / "main.py").read_text(encoding="utf-8")
    assert 'getattr(config, "feature_nft", False)' in src
    assert 'getattr(config, "feature_ai_agents", False)' in src
    assert 'getattr(config, "feature_ai_validator", False)' in src
    assert 'getattr(config, "feature_nft", True)' not in src
    assert 'getattr(config, "feature_ai_agents", True)' not in src
    assert 'getattr(config, "feature_ai_validator", True)' not in src


def test_sdk_ai_read_helpers_exist():
    src = (ROOT / "sdk" / "dup_sdk" / "client.py").read_text(encoding="utf-8")
    assert "def get_ai_agent_stats" in src
    assert "def get_ai_mev_scan" in src
    assert "/ai-agent/stats" in src
    assert "/ai/mev-scan" in src


def test_feature_flags_includes_ai_validator():
    from features import FeatureFlags

    flags = FeatureFlags()
    assert flags.ai_validator is False
    assert flags.ai_agents is False
    cfg = MagicMock()
    cfg.feature_ai_validator = True
    cfg.feature_ai_agents = False
    for attr in (
        "evm_enabled",
        "bridge_enabled",
        "feature_nft",
        "feature_zk",
        "feature_sharding",
        "feature_oracles",
        "feature_wasm",
        "feature_plasma",
        "feature_lightning",
        "feature_pq",
        "feature_mev",
    ):
        setattr(cfg, attr, False)
    cfg.evm_enabled = True
    out = FeatureFlags.from_config(cfg)
    assert out.ai_validator is True
    assert out.ai_agents is False


def test_sdk_no_invent_price_satoshi():
    src = (ROOT / "sdk" / "dup_sdk" / "client.py").read_text(encoding="utf-8")
    chunk = src.split("def get_nft_token")[1].split("def get_nft_by_owner")[0]
    assert "to_satoshi(out[\"price\"])" not in chunk
    assert "never invent price_satoshi" in chunk


def test_ai_ops_honesty_constant():
    from features import ai_ops

    assert "not consensus" in ai_ops.HONESTY.lower()
