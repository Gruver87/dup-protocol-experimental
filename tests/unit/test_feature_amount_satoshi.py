"""Feature sprout money persist dual-writes *_satoshi columns."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.amount import to_satoshi
from storage.database import Database


def _db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    db = Database(path)
    db.initialize()
    return db, path


def test_plasma_deposit_and_exit_amount_satoshi():
    db, path = _db()
    try:
        db.save_plasma_deposit(
            {
                "id": "d1",
                "from": "0xfrom",
                "amount": 12.5,
                "main_tx_hash": "0x1",
                "created_at": 1,
                "status": "confirmed",
            }
        )
        deps = db.get_plasma_deposits()
        assert deps[0]["amount_satoshi"] == int(to_satoshi(12.5))
        db.save_plasma_exit(
            {
                "id": "e1",
                "deposit_id": "d1",
                "user": "0xuser",
                "amount": 12.5,
                "created_at": 2,
                "status": "pending",
            }
        )
        exits = db.get_plasma_exits()
        assert exits[0]["amount_satoshi"] == int(to_satoshi(12.5))
    finally:
        db.close()
        os.remove(path)


def test_lightning_channel_and_payment_satoshi():
    db, path = _db()
    try:
        db.save_lightning_channel(
            {
                "channel_id": "c1",
                "node1": "n1",
                "node2": "n2",
                "capacity": 10.0,
                "balance1": 6.0,
                "balance2": 4.0,
                "status": "open",
                "fee_rate": 0.00001,
                "created_at": 1,
            }
        )
        ch = db.get_lightning_channels()[0]
        assert ch["capacity_satoshi"] == int(to_satoshi(10.0))
        assert ch["balance1_satoshi"] == int(to_satoshi(6.0))
        assert ch["balance2_satoshi"] == int(to_satoshi(4.0))
        db.save_lightning_payment(
            {
                "payment_id": "p1",
                "channel_id": "c1",
                "from_node": "n1",
                "to_node": "n2",
                "amount": 1.25,
                "fee": 0.01,
                "status": "completed",
                "payment_hash": "h",
                "timestamp": 2,
            }
        )
        pay = db.get_lightning_payments()[0]
        assert pay["amount_satoshi"] == int(to_satoshi(1.25))
        assert pay["fee_satoshi"] == int(to_satoshi(0.01))
    finally:
        db.close()
        os.remove(path)


def test_crypto_will_amount_satoshi():
    db, path = _db()
    try:
        db.save_crypto_will(
            {
                "will_id": "w1",
                "owner": "0xo",
                "heir": "0xh",
                "amount": 100.0,
                "assets": {},
                "execution_time": 9,
                "created_at": 1,
                "status": "pending",
                "witnesses": [],
            }
        )
        wills = db.get_crypto_wills()
        assert wills[0]["amount_satoshi"] == int(to_satoshi(100.0))
    finally:
        db.close()
        os.remove(path)


def test_source_needles_feature_amount_satoshi():
    src = (ROOT / "storage" / "database.py").read_text(encoding="utf-8")
    assert "_backfill_feature_amount_satoshi" in src
    assert '("plasma_deposits", "amount_satoshi"' in src
    assert '("lightning_channels", "capacity_satoshi"' in src
    assert '("crypto_wills", "amount_satoshi"' in src
