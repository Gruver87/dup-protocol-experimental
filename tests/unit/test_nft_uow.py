#!/usr/bin/env python3
"""NFT mint/buy use db.atomic() UoW when available (ADR 0016 Profile C)."""
from __future__ import annotations

import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, ROOT)


def test_nft_mint_buy_report_uow_atomic():
    from features.nft import NFTMarketplace
    from storage.database import Database

    tmp = tempfile.mkdtemp()
    db = Database(os.path.join(tmp, "nft_uow.db"))
    db.initialize()
    seller = "0x" + "a" * 40
    buyer = "0x" + "b" * 40
    db.update_balance(seller, 1000.0)
    db.update_balance(buyer, 1000.0)

    nft = NFTMarketplace(db=db)
    assert nft.get_stats()["uow_atomic"] is True
    assert nft.get_stats()["tier"] == "app-profile"

    before = db.get_balance(seller)
    r = nft.mint("uow_tok", "UoW", "t", "img", seller, price=10.0)
    assert r["success"] is True
    assert r.get("uow_atomic") is True
    assert db.get_balance(seller) == before - nft.MINT_FEE

    buy = nft.buy("uow_tok", buyer)
    assert buy["success"] is True
    assert buy.get("uow_atomic") is True
    assert nft.get_token("uow_tok")["owner"] == buyer


def test_nft_mint_rolls_back_memory_on_uow_failure():
    from features.nft import NFTMarketplace

    class _BrokenAtomic:
        def atomic(self):
            raise RuntimeError("forced_uow_fail")

        def get_balance(self, _a):
            return 100.0

        def get_balance_satoshi(self, _a):
            return 100_000_000

        def balance_delta_satoshi(self, _a, _d):
            return None

        def update_balance(self, _a, _d):
            return 0.0

        def get_nft_tokens(self):
            return []

    nft = NFTMarketplace(db=_BrokenAtomic())
    # Clear genesis noise for assertion
    nft.tokens.clear()
    r = nft.mint("x", "n", "d", "i", "0xcreator", 0.0)
    assert r["success"] is False
    assert "nft_uow_failed" in r["error"]
    assert "x" not in nft.tokens


def test_nft_offer_auction_settle_under_uow():
    from features.nft import NFTMarketplace
    from storage.database import Database

    tmp = tempfile.mkdtemp()
    db = Database(os.path.join(tmp, "nft_offer_uow.db"))
    db.initialize()
    seller = "0x" + "a" * 40
    buyer = "0x" + "b" * 40
    db.update_balance(seller, 1000.0)
    db.update_balance(buyer, 1000.0)
    nft = NFTMarketplace(db=db)
    nft.tokens.clear()
    assert nft.mint("o1", "O", "d", "i", seller, price=5.0)["success"]
    oid = nft.make_offer("o1", buyer, price=5.0, hours=1)
    assert oid
    acc = nft.accept_offer(oid, seller)
    assert acc["success"] is True
    assert acc.get("uow_atomic") is True
    assert nft.get_token("o1")["owner"] == buyer

    db.update_balance(seller, 1000.0)
    db.update_balance(buyer, 1000.0)
    assert nft.mint("a1", "A", "d", "i", seller, price=5.0)["success"]
    aid = nft.create_auction(
        "a1", seller, start_price=1.0, reserve_price=1.0, hours=1
    )
    assert aid
    assert nft.place_bid(aid, buyer, amount=2.0)["success"]
    # Window must elapse before finalize (honesty guard).
    nft.auctions[aid]["ends_at"] = int(__import__("time").time()) - 1
    fin = nft.finalize_auction(aid)
    assert fin["success"] is True
    assert fin.get("uow_atomic") is True
    assert nft.get_token("a1")["owner"] == buyer
    assert nft.auctions[aid]["status"] == "finalized"
