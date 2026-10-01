"""TypedDict shapes for dup_sdk responses (documentation / typing only)."""

from __future__ import annotations

from typing import Any, Dict, Optional, TypedDict


class BalanceInfo(TypedDict, total=False):
    address: str
    balance_satoshi: int
    balance: float
    symbol: str


class TxSubmitResult(TypedDict, total=False):
    tx_hash: str
    status: str
    trace_url: str


class ReceiptInfo(TypedDict, total=False):
    tx_hash: str
    block_height: int
    status: int
    value_satoshi: int
    fee_satoshi: int
    burned_satoshi: int
    value: float
    fee: float
    burned: float


JsonDict = Dict[str, Any]
OptionalStr = Optional[str]
