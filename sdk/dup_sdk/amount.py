"""Satoshi helpers for the thin SDK (self-contained; matches runtime.amount).

1 ABS = 1_000_000 satoshi. Float ABS is display-only; money APIs prefer int satoshi.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation, ROUND_DOWN
from typing import Any, Optional, Union

from .errors import MoneyRefuse

ABS_DECIMALS = 6
SATOSHI_MULTIPLIER = 10**ABS_DECIMALS
WEI_PER_ABS = 10**18
WEI_PER_SATOSHI = WEI_PER_ABS // SATOSHI_MULTIPLIER

NumberLike = Union[int, float, str, Decimal]


def to_satoshi(amount_abs: NumberLike) -> int:
    """Convert ABS amount to integer satoshi (floor toward zero)."""
    if isinstance(amount_abs, bool):
        raise MoneyRefuse("bool is not a valid amount")
    try:
        d = Decimal(str(amount_abs))
    except (InvalidOperation, ValueError, TypeError) as exc:
        raise MoneyRefuse(f"invalid amount: {amount_abs!r}") from exc
    scaled = (d * Decimal(SATOSHI_MULTIPLIER)).quantize(
        Decimal("1"), rounding=ROUND_DOWN
    )
    return int(scaled)


def from_satoshi_float(satoshi: int) -> float:
    """Display ABS float derived from satoshi (not a money source of truth)."""
    return float(Decimal(int(satoshi)) / Decimal(SATOSHI_MULTIPLIER))


def require_satoshi(
    *,
    satoshi: Optional[Any] = None,
    abs_amount: Optional[Any] = None,
    field: str = "amount",
) -> int:
    """Prefer explicit satoshi; refuse float-only money without satoshi twin.

    If ``satoshi`` is provided it wins (must be int-like, not float).
    If only ``abs_amount`` is provided and it is a non-integral float → refuse.
    Whole ABS int / whole float (1.0) may be converted via ``to_satoshi``.
    """
    if satoshi is not None:
        if isinstance(satoshi, bool):
            raise MoneyRefuse(f"{field}_satoshi: bool refused")
        if isinstance(satoshi, float):
            raise MoneyRefuse(f"{field}_satoshi must be int, got float")
        try:
            return max(0, int(satoshi))
        except (TypeError, ValueError) as exc:
            raise MoneyRefuse(f"invalid {field}_satoshi: {satoshi!r}") from exc

    if abs_amount is None:
        raise MoneyRefuse(f"{field}_satoshi required (float-only money refused)")

    if isinstance(abs_amount, bool):
        raise MoneyRefuse(f"{field}: bool refused")
    if isinstance(abs_amount, float):
        if not abs_amount.is_integer():
            raise MoneyRefuse(
                f"{field}: non-integral float refused without {field}_satoshi"
            )
        return to_satoshi(int(abs_amount))
    return to_satoshi(abs_amount)


def wei_hex_to_satoshi(wei_hex: str) -> int:
    """Convert eth_getBalance wei hex to satoshi integer."""
    raw = (wei_hex or "0x0").strip().lower()
    if not raw.startswith("0x"):
        raw = "0x" + raw
    wei = int(raw, 16)
    return wei // WEI_PER_SATOSHI
