"""DUP Protocol thin operator SDK (experimental).

Honesty
-------
- R&D / operator client for ``dup-protocol-experimental`` nodes.
- **Not** public audited mainnet, **not** the industrial pin SDK,
  **not** a wallet key manager, **not** full geth parity.
- Money APIs prefer integer satoshi; float-only money inputs are refused.
- TLS certificate verification is **on** by default (no disable helper).
"""

from __future__ import annotations

from .__version__ import __version__
from .amount import (
    ABS_DECIMALS,
    SATOSHI_MULTIPLIER,
    WEI_PER_SATOSHI,
    from_satoshi_float,
    require_satoshi,
    to_satoshi,
)
from .client import Client
from .errors import DupSdkError, HttpError, MoneyRefuse, RpcError

HONESTY = (
    "dup_sdk v0: experimental operator client — "
    "not mainnet / not industrial pin / not wallet custody"
)

__all__ = [
    "__version__",
    "ABS_DECIMALS",
    "SATOSHI_MULTIPLIER",
    "WEI_PER_SATOSHI",
    "HONESTY",
    "Client",
    "DupSdkError",
    "HttpError",
    "MoneyRefuse",
    "RpcError",
    "from_satoshi_float",
    "require_satoshi",
    "to_satoshi",
]
