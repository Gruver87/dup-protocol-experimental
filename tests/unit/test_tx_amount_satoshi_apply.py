"""Transaction.amount_satoshi is apply money authority when present."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.blockchain import Transaction
from runtime.amount import plan_transfer_fees_sat, resolve_tx_value_satoshi, to_satoshi


def test_resolve_tx_value_prefers_amount_satoshi():
    tx = Transaction(
        "0xa",
        "0xb",
        value=99.0,
        nonce=0,
        gas=21000,
        amount_satoshi=1_000_000,
    )
    assert resolve_tx_value_satoshi(tx) == 1_000_000


def test_from_dict_binds_amount_satoshi():
    tx = Transaction.from_dict(
        {
            "from": "0xa",
            "to": "0xb",
            "value": 1.0,
            "amount_satoshi": 1_000_000,
            "nonce": 0,
            "gas": 21000,
        }
    )
    assert tx.amount_satoshi == 1_000_000
    assert tx.value == pytest.approx(1.0)


def test_from_dict_mismatch_refused():
    with pytest.raises(ValueError, match="value_satoshi_mismatch"):
        Transaction.from_dict(
            {
                "from": "0xa",
                "to": "0xb",
                "value": 2.0,
                "amount_satoshi": 1_000_000,
                "nonce": 0,
                "gas": 21000,
            }
        )


def test_plan_transfer_fees_sat_value_satoshi_override():
    plan = plan_transfer_fees_sat(21000, 0.0000001, 0.5, value=9.0, value_satoshi=500_000)
    assert plan["value_sat"] == 500_000
    assert plan["total_cost_sat"] == 500_000 + plan["fee_sat"]


def test_to_dict_emits_amount_satoshi():
    tx = Transaction("0xa", "0xb", 1.0, nonce=0, gas=21000, amount_satoshi=int(to_satoshi(1)))
    d = tx.to_dict()
    assert d["amount_satoshi"] == 1_000_000
    assert d["value_satoshi"] == 1_000_000
