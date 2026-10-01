#!/usr/bin/env python3
"""NFT marketplace lab — offline self-check (NOT soak / NOT prod feature_nft / NOT ERC-721).

Verifies satoshi price honesty, mint/list/buy UoW, prod mesh flag freeze.
Optional live staging :19080 stats read if port open.
"""

from __future__ import annotations

import json
import socket
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from features.nft import HONESTY, NFTMarketplace, resolve_price_satoshi
from runtime.amount import to_satoshi
from storage.database import Database


def _fail(msg: str) -> int:
    print(f"FAIL: {msg}")
    return 1


def _port_open(host: str, port: int, timeout: float = 0.4) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def _check_prod_flags() -> str | None:
    for name in ("node.prod.mesh1.json", "node.prod.mesh2.json", "node.prod.mesh3.json"):
        path = ROOT / "docker" / name
        if not path.is_file():
            return f"missing {path}"
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("feature_nft") is not False:
            return f"{name}: feature_nft must be false"
    return None


def main() -> int:
    print("nft_lab - NOT soak / NOT mainnet / NOT prod feature_nft / NOT ERC-721")
    print("honesty:", HONESTY)

    err = _check_prod_flags()
    if err:
        return _fail(err)
    print("OK: prod mesh feature_nft=false")

    try:
        resolve_price_satoshi(price=1.25)
        return _fail("expected refuse dust float price")
    except ValueError:
        pass
    assert resolve_price_satoshi(price_satoshi=1_500_000) == 1_500_000
    assert resolve_price_satoshi(price=2.0) == int(to_satoshi(2))

    with tempfile.TemporaryDirectory() as tmp:
        db = Database(str(Path(tmp) / "nft_lab.db"))
        db.initialize()
        seller = "0x" + "a" * 40
        buyer = "0x" + "b" * 40
        db.set_balance(seller, 1000.0)
        db.set_balance(buyer, 1000.0)

        m = NFTMarketplace(db=db)
        # clear genesis so mint path is clean
        m.tokens.clear()
        st = m.get_stats()
        if st.get("consensus_wired") is not False:
            return _fail("consensus_wired must be False")
        if st.get("tier") != "app-profile":
            return _fail("tier must be app-profile")

        r = m.mint("lab1", "Lab", "d", "img", seller, price=10.0)
        if not r.get("success"):
            return _fail(f"mint failed: {r}")
        if r.get("price_satoshi") != int(to_satoshi(10)):
            return _fail("mint price_satoshi mismatch")

        listed = m.list_for_sale("lab1", seller, price_satoshi=int(to_satoshi(25)))
        if not listed.get("success"):
            return _fail(f"list failed: {listed}")

        dust = m.list_for_sale("lab1", seller, price=1.25)
        if dust.get("success"):
            return _fail("dust float list must refuse")

        buy = m.buy("lab1", buyer)
        if not buy.get("success"):
            return _fail(f"buy failed: {buy}")
        if buy.get("price_satoshi") != int(to_satoshi(25)):
            return _fail("buy price_satoshi mismatch")
        tok = m.get_token("lab1")
        if not tok or tok["owner"] != buyer:
            return _fail("owner after buy mismatch")
        if tok.get("price_satoshi") is None:
            return _fail("token missing price_satoshi")

        try:
            db.close()
        except Exception:
            pass

    # optional staging read
    if _port_open("127.0.0.1", 19080):
        try:
            from sdk.dup_sdk import Client

            c = Client("http://127.0.0.1:19080")
            stats = c.get_nft_stats()
            print("OK: staging /nft/stats keys", sorted(list(stats.keys()))[:10])
        except Exception as exc:
            print(f"WARN: staging nft stats: {exc}")
    else:
        print("SKIP: staging :19080 not open")

    print("OK: nft_lab mint/list/buy satoshi honesty")
    print("RESULT: PASS nft_lab")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
