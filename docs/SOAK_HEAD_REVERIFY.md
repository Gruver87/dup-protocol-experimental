# Soak re-verify on current HEAD — operator prep (2026-10-03)

**Tip to claim:** `git rev-parse --short HEAD` (prep written at `7fb9a54`)  
**Goal:** one **STRICT 48h** pack so fund decks can say “soak on this tip”, not only historical packs.  
**Not:** mainnet · not pin TCP+TLS · not firm PASS · not Long-Range prod.

---

## EVM soak — honest status

| Run | Result |
|-----|--------|
| Historical STRICT PASS [`evmstrict1`](evidence/runs/evmstrict1/) | **PASS** — tip `0c36904` (2026-09-28→30). **Not** current HEAD. |
| Attempt 2026-10-03 | **FAIL / interrupted** ~33.8h — host `full_audit`/`pytest`/`Max` starved `/health/ready`. Evidence: `logs/soak_48h_evm_strict_fail_summary.json`. **Not** 48h PASS. |
| Fresh PASS on money/honesty tip (`7fb9a54`+) | **Not run yet** |

So: **новый EVM soak мы не прошли.** Старый `evmstrict1` остаётся историческим PASS.

---

## Preflight status (2026-10-03)

| Step | Result |
|------|--------|
| midsoak honesty Quick | PASS |
| industrial_gate (stake needle → `resolve_amount_satoshi`) | PASS (3 org warnings) |
| `prepare_head_soak_evm_strict.ps1 -SkipRebuild` | **PASS** — mesh READY, EVM harness OK |
| 48h STRICT started | **No** |

Commit soak-prep files before tip claim (dirty tree was warned at preflight). Then start 48h.

---

## Which soak to run now (one is enough)

**Recommended:** EVM STRICT path — covers prod mesh + EVM harness after satoshi/EVM money waves.

```powershell
cd C:\Users\vovun\Desktop\Absolute_Blockchain_Experimental

# 1) Prep wrapper (honesty + stop monitors + PreflightOnly) — already PASS once
.\scripts\prepare_head_soak_evm_strict.ps1 -SkipRebuild

# 2) Start 48h (only after prep PASS). Do NOT run Max/full_audit/pytest on this host while ALIVE.
.\scripts\start_soak_evm_mesh_48h_strict.ps1 -SkipRebuild
```

Alternative (mesh-only STRICT, no EVM harness):

```powershell
.\scripts\start_soak_prod_mesh_48h_strict.ps1
```

Pass bar: `passed=true`, `hard_fails=0`, `mesh_warn=0`, IntervalSec=60. Then package under `docs/evidence/runs/<id>/`.

---

## Host rules (why last EVM run failed)

1. While soak monitor is ALIVE — **no** `verify_dup_suite -Max`, **no** `full_audit`, heavy pytest on mesh ports.  
2. Guard: `python scripts/soak_guard.py` (blocks live-mesh hammering).  
3. If interrupted: `.\scripts\stop_soak_monitors.ps1 -Force` → soft restart mesh `-KeepVolumes` → **new** 48h (do not claim partial hours).

---

## After PASS

1. Copy report/log into `docs/evidence/runs/<newid>/` + README (`passed=true`, tip range, git SHA).  
2. Link from `EVIDENCE_MATRIX.md` / `FUND_DEMO_OPERATOR_PACK.md`.  
3. Only then say: “STRICT 48h on tip `<sha>`”.

Historical packs (`evmstrict1`, `ind48pass1`, …) stay valid as prior evidence — do not delete.
