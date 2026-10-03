#!/usr/bin/env python3
"""DUP Protocol — unified verify for pin + Experimental (one operator entry).

Runs the key working surfaces of both trees without merging repos and without
starting a 48h soak or rebuilding Docker (unless you pass --rebuild-libp2p).

Modes (from Experimental root):
  quick    — pin quick + Exp industrial_gate + midsoak units + AI/NFT labs + showcase needles
  standard — pin standard + Exp RD units/labs + ADR 0019 hard + gate + midsoak
  full     — pin industrial + everything in standard
  max      — full + Exp verify_full_blockchain --hard (live mesh :18180–18182 required)

Usage:
  python scripts/verify_dup_suite.py --mode quick
  python scripts/verify_dup_suite.py --mode standard
  python scripts/verify_dup_suite.py --mode full
  python scripts/verify_dup_suite.py --mode max
  .\\scripts\\verify_dup_suite.ps1 -Mode Standard

Env:
  ABS_HYBRID_ROOT / DUP_PIN_ROOT — path to Absolute_Blockchain_Ultimate_Hybrid (dup-protocol)

Honesty:
  PASS != public mainnet / firm audit PDF / soak PASS invented without pack.
  Exp libp2p PASS != pin TCP+TLS cutover.
  Live mesh probe/hard does NOT restart soak containers.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

EXPERIMENTAL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PIN = EXPERIMENTAL_ROOT.parent / "Absolute_Blockchain_Ultimate_Hybrid"

SHOWCASE_NEEDLES = (
    "docs/SHOWCASE.md",
    "docs/FAQ.md",
    "docs/ONE_PAGER.md",
    "docs/ONE_PAGER_RU.md",
    "docs/ELEVATOR_PITCH.md",
    "docs/DILIGENCE_BRIEF.md",
    "docs/FUND_READINESS.md",
)

MIDSOAK_PYTEST = [
    "tests/unit/test_exp_ai_nft_marketplace_wave.py",
    "tests/unit/test_nft_ports.py",
    "tests/unit/test_exp_no_invent_gas_21000.py",
    "tests/unit/test_exp_rest_amount_honesty.py",
    "tests/unit/test_exp_wallet_tx_gas_required.py",
]


def _safe_print(text: str) -> None:
    enc = getattr(sys.stdout, "encoding", None) or "utf-8"
    sys.stdout.buffer.write((text + "\n").encode(enc, errors="replace"))
    sys.stdout.flush()


def _banner(text: str) -> None:
    _safe_print("")
    _safe_print("=" * 72)
    _safe_print(f" {text}")
    _safe_print("=" * 72)


def _run_stage(
    *,
    name: str,
    cwd: Path,
    cmd: list[str],
    keep_going: bool,
    steps: list[dict],
) -> bool:
    _safe_print("")
    _safe_print(f">>> [{name}]")
    _safe_print(f"    cwd: {cwd}")
    _safe_print(f"    $ {' '.join(cmd)}")
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(cmd, cwd=str(cwd))
        rc = int(proc.returncode)
    except OSError as exc:
        rc = 127
        _safe_print(f"FAIL: spawn error: {exc}")
    elapsed = round(time.perf_counter() - t0, 1)
    ok = rc == 0
    steps.append(
        {
            "name": name,
            "cwd": str(cwd),
            "cmd": cmd,
            "ok": ok,
            "exit": rc,
            "elapsed_sec": elapsed,
        }
    )
    status = "PASS" if ok else "FAIL"
    _safe_print(f"[{status}] {name}  ({elapsed}s, exit={rc})")
    if not ok and not keep_going:
        raise SystemExit(f"STAGE FAIL: {name} (exit {rc})")
    return ok


def _resolve_pin(path: str | None) -> Path:
    raw = (
        path
        or os.environ.get("DUP_PIN_ROOT")
        or os.environ.get("ABS_HYBRID_ROOT")
        or str(DEFAULT_PIN)
    ).strip()
    root = Path(raw).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"FAIL: pin/Hybrid root not found: {root}")
    marker = root / "scripts" / "verify_project.py"
    if not marker.is_file():
        raise SystemExit(f"FAIL: not a pin repo (missing {marker})")
    return root


def _check_showcase(experimental: Path, steps: list[dict], keep_going: bool) -> bool:
    _safe_print("")
    _safe_print(">>> [experimental:showcase_docs]")
    missing = [rel for rel in SHOWCASE_NEEDLES if not (experimental / rel).is_file()]
    ok = not missing
    steps.append(
        {
            "name": "experimental:showcase_docs",
            "cwd": str(experimental),
            "cmd": ["exists"] + list(SHOWCASE_NEEDLES),
            "ok": ok,
            "exit": 0 if ok else 1,
            "elapsed_sec": 0.0,
            "missing": missing,
        }
    )
    if ok:
        _safe_print("[PASS] experimental:showcase_docs")
    else:
        _safe_print(f"[FAIL] missing: {', '.join(missing)}")
        if not keep_going:
            raise SystemExit("STAGE FAIL: experimental:showcase_docs")
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--mode",
        choices=("quick", "standard", "full", "max"),
        default="standard",
        help="quick|standard|full|max (see module docstring)",
    )
    ap.add_argument(
        "--hybrid-root",
        "--pin-root",
        dest="pin_root",
        default=None,
        help="Path to pin (Absolute_Blockchain_Ultimate_Hybrid / dup-protocol)",
    )
    ap.add_argument(
        "--experimental-root",
        default=None,
        help="Path to Experimental (default: this repo)",
    )
    ap.add_argument("--min-soak-hours", type=float, default=48.0)
    ap.add_argument("--skip-pin", "--skip-hybrid", dest="skip_pin", action="store_true")
    ap.add_argument("--skip-experimental-rd", action="store_true")
    ap.add_argument("--skip-libp2p", action="store_true")
    ap.add_argument("--skip-midsoak", action="store_true")
    ap.add_argument("--skip-labs", action="store_true", help="skip ai_lab/nft_lab")
    ap.add_argument("--skip-gate", action="store_true", help="skip Exp industrial_gate")
    ap.add_argument("--rebuild-libp2p", action="store_true")
    ap.add_argument(
        "--with-mesh-probe",
        action="store_true",
        help="also run probe_prod_mesh -Quick (no docker rebuild)",
    )
    ap.add_argument("--keep-going", action="store_true")
    ap.add_argument("-q", "--quiet", action="store_true")
    args = ap.parse_args()

    experimental = (
        Path(args.experimental_root).resolve()
        if args.experimental_root
        else EXPERIMENTAL_ROOT
    )
    if not (experimental / "scripts" / "industrial_gate.py").is_file():
        raise SystemExit(f"FAIL: Experimental root incomplete: {experimental}")

    pin = None if args.skip_pin else _resolve_pin(args.pin_root)
    py = sys.executable
    started = time.time()
    steps: list[dict] = []
    report: dict = {
        "script": "verify_dup_suite.py",
        "brand": "DUP Labs / DUP Protocol",
        "mode": args.mode,
        "pin_root": str(pin) if pin else None,
        "experimental_root": str(experimental),
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "steps": steps,
        "ok": False,
        "honesty": [
            "Two repos, one operator view — not a git merge",
            "PASS is not public mainnet / firm audit PDF",
            "Pin default transport remains TCP+TLS",
            "Experimental libp2p PASS does not authorize pin cutover",
            "This suite does NOT start 48h soak or claim soak PASS",
            "max mode requires live mesh :18180-18182 (probe only; no container recreate)",
        ],
    }

    _banner(f"DUP VERIFY SUITE  mode={args.mode}")
    _safe_print(f"Pin:          {pin or '(skipped)'}")
    _safe_print(f"Experimental: {experimental}")
    _safe_print(f"Python:       {py}")
    _safe_print("Honesty: green != mainnet / != soak PASS / != merged tree")

    all_ok = True
    try:
        # --- Pin ---
        if pin is not None:
            pin_mode = {
                "quick": "quick",
                "standard": "standard",
                "full": "industrial",
                "max": "industrial",
            }[args.mode]
            cmd = [py, "scripts/verify_project.py", "--mode", pin_mode]
            if pin_mode == "industrial":
                cmd += ["--min-soak-hours", str(args.min_soak_hours)]
            ok = _run_stage(
                name=f"pin:verify_project:{pin_mode}",
                cwd=pin,
                cmd=cmd,
                keep_going=args.keep_going,
                steps=steps,
            )
            all_ok = all_ok and ok

        # --- Showcase docs (Exp) ---
        ok = _check_showcase(experimental, steps, args.keep_going)
        all_ok = all_ok and ok

        # --- Exp industrial_gate ---
        if not args.skip_gate:
            ok = _run_stage(
                name="experimental:industrial_gate",
                cwd=experimental,
                cmd=[py, "scripts/industrial_gate.py"],
                keep_going=args.keep_going,
                steps=steps,
            )
            all_ok = all_ok and ok

        # --- Mid-soak honesty units ---
        if not args.skip_midsoak:
            ok = _run_stage(
                name="experimental:midsoak_pytest",
                cwd=experimental,
                cmd=[py, "-m", "pytest", *MIDSOAK_PYTEST, "-q", "--tb=line"],
                keep_going=args.keep_going,
                steps=steps,
            )
            all_ok = all_ok and ok

        # --- AI / NFT labs ---
        if not args.skip_labs:
            for lab in ("scripts/ai_lab.py", "scripts/nft_lab.py"):
                ok = _run_stage(
                    name=f"experimental:{Path(lab).stem}",
                    cwd=experimental,
                    cmd=[py, lab],
                    keep_going=args.keep_going,
                    steps=steps,
                )
                all_ok = all_ok and ok

        # --- Experimental RD (Profile F) ---
        if not args.skip_experimental_rd and args.mode in (
            "standard",
            "full",
            "max",
        ):
            rd_cmd = [py, "scripts/verify_experimental_rd.py"]
            if args.quiet:
                rd_cmd.append("-q")
            ok = _run_stage(
                name="experimental:verify_experimental_rd",
                cwd=experimental,
                cmd=rd_cmd,
                keep_going=args.keep_going,
                steps=steps,
            )
            all_ok = all_ok and ok

        # --- ADR 0019 hard ---
        run_libp2p = (not args.skip_libp2p) and (args.mode in ("standard", "full", "max"))
        if args.mode == "quick" and not args.skip_libp2p:
            _safe_print("")
            _safe_print("NOTE: mode=quick skips ADR 0019 hard (use standard|full|max)")
        if run_libp2p:
            hard_cmd = [py, "scripts/verify_adr0019_libp2p_hard.py"]
            if args.rebuild_libp2p:
                hard_cmd.append("--rebuild")
            if args.keep_going:
                hard_cmd.append("--keep-going")
            if args.quiet:
                hard_cmd.append("-q")
            ok = _run_stage(
                name="experimental:adr0019_libp2p_hard",
                cwd=experimental,
                cmd=hard_cmd,
                keep_going=args.keep_going,
                steps=steps,
            )
            all_ok = all_ok and ok

        # --- Optional mesh probe (no docker recreate) ---
        if args.with_mesh_probe or args.mode == "max":
            probe = experimental / "scripts" / "probe_prod_mesh.ps1"
            if probe.is_file():
                ok = _run_stage(
                    name="experimental:probe_prod_mesh_quick",
                    cwd=experimental,
                    cmd=[
                        "powershell",
                        "-NoProfile",
                        "-ExecutionPolicy",
                        "Bypass",
                        "-File",
                        str(probe),
                        "-Quick",
                    ],
                    keep_going=args.keep_going,
                    steps=steps,
                )
                all_ok = all_ok and ok

        # --- Max: full hard blockchain verify ---
        if args.mode == "max":
            ok = _run_stage(
                name="experimental:verify_full_blockchain_hard",
                cwd=experimental,
                cmd=[py, "scripts/verify_full_blockchain.py", "--hard"],
                keep_going=args.keep_going,
                steps=steps,
            )
            all_ok = all_ok and ok

        report["ok"] = all_ok
        if not all_ok:
            raise SystemExit("DUP SUITE FAIL: one or more stages failed (--keep-going)")
    except SystemExit as exc:
        report["error"] = str(exc)
        if not args.keep_going:
            all_ok = False
            report["ok"] = False
        _safe_print(f"\nFAIL: {exc}")

    report["ended_utc"] = datetime.now(timezone.utc).isoformat()
    report["elapsed_sec"] = round(time.time() - started, 1)
    report["ok"] = bool(report.get("ok")) and all_ok

    out_dir = experimental / "data"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "verify_dup_suite.json"
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    # Compatibility alias for older operator docs
    (out_dir / "verify_absolute_unified.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    _banner(
        ("PASS" if report["ok"] else "FAIL")
        + f" — DUP suite mode={args.mode} — {report['elapsed_sec']}s"
    )
    _safe_print(
        "Stages: "
        + ", ".join(f"{s['name']}={'OK' if s['ok'] else 'FAIL'}" for s in steps)
    )
    _safe_print(f"Report: {out_path}")
    _safe_print("Honesty:")
    for line in report["honesty"]:
        _safe_print(f"  - {line}")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
