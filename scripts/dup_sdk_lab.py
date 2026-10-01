#!/usr/bin/env python3
"""dup_sdk lab — offline self-check; optional live mesh probe.

NOT soak / NOT mainnet / NOT firm audit PASS.
"""

from __future__ import annotations

import argparse
import socket
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sdk.dup_sdk import (  # noqa: E402
    HONESTY,
    Client,
    MoneyRefuse,
    __version__,
    require_satoshi,
    to_satoshi,
)


def _port_open(host: str, port: int, timeout: float = 0.4) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def offline_self_check() -> None:
    assert __version__
    assert "not mainnet" in HONESTY
    assert to_satoshi(1) == 1_000_000
    assert require_satoshi(satoshi=42) == 42
    try:
        require_satoshi(abs_amount=1.25)
        raise AssertionError("expected MoneyRefuse for dust float")
    except MoneyRefuse:
        pass
    try:
        Client("http://127.0.0.1:9", verify_tls=False)  # type: ignore[arg-type]
        raise AssertionError("expected verify_tls refuse")
    except ValueError:
        pass
    print("OK: offline self-check", HONESTY, f"v{__version__}")


def live_probe(base_url: str) -> None:
    parsed = urlparse(base_url)
    host = parsed.hostname or "127.0.0.1"
    port = int(parsed.port or (443 if parsed.scheme == "https" else 80))
    if not _port_open(host, port):
        print(f"SKIP: live probe — {host}:{port} not open")
        return
    c = Client(base_url)
    live = c.health_live()
    print("OK: health_live", live.get("live", live.get("ok", live)))
    try:
        ready = c.health_ready()
        print("OK: health_ready", ready.get("ready", ready))
    except Exception as exc:
        print(f"WARN: health_ready: {exc}")
    try:
        st = c.status_probe()
        print("OK: status_probe keys", sorted(list(st.keys()))[:12])
    except Exception as exc:
        print(f"WARN: status_probe: {exc}")
    try:
        tip = c.get_block_number()
        print("OK: block_number", tip)
    except Exception as exc:
        print(f"WARN: block_number: {exc}")
    print("honesty: live probe is NOT a soak claim")


def main() -> int:
    ap = argparse.ArgumentParser(description="dup_sdk lab (NOT soak)")
    ap.add_argument(
        "--base-url",
        default="",
        help="optional node base URL for live probe (e.g. http://127.0.0.1:18180)",
    )
    args = ap.parse_args()
    print("dup_sdk_lab — NOT soak / NOT mainnet / NOT firm PASS")
    offline_self_check()
    if args.base_url.strip():
        live_probe(args.base_url.strip())
    else:
        # default mesh ports if listening
        for port in (18180, 18181, 18182):
            url = f"http://127.0.0.1:{port}"
            if _port_open("127.0.0.1", port):
                print(f"INFO: port {port} open — probing {url}")
                live_probe(url)
                break
        else:
            print("SKIP: no live mesh ports 18180–18182")
    print("RESULT: PASS dup_sdk_lab")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
