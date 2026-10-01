# Full critical-path audit scan — 2026-10-01

**Repo:** `dup-protocol-experimental` (local Desktop: `Absolute_Blockchain_Experimental`)  
**Scope:** Automated pattern scan across critical packages + surgical fail-closed fixes.  
**Not claimed:** 48h soak, STRICT pack, public mainnet, Great Merge, bridge ON, prod Long-Range.

## Method

1. Pattern scan: TLS `verify=False`, float money fallback, hardcoded secrets, prod `feature_*=true`, CORS `*`, `except→pass/True` on critical packages.
2. Call-site review: `apply_store_delta_satoshi` (all production money paths already pass `allow_float_fallback=False`).
3. Existing gates: `scripts/verify_industrial_high_honesty.ps1` → **PASS**; `scripts/industrial_gate.py` → **OK** (warnings: external audit pending, bridge example ON, abs_bridge_bin missing while bridge OFF).
4. Unit evidence for this change (not L1 mesh acceptance):  
   `tests/unit/test_apply_store_delta_satoshi.py`, `test_cors_receipt_ready_honesty.py`, `test_nft_marketplace_harden.py` → **20 passed**.

Re-run scan: `python scripts/audit_critical_paths.py`

## Findings triage

| Severity | Finding | Action |
|----------|---------|--------|
| P0 (fixed) | `apply_store_delta_satoshi` defaulted to float fallback `True` | Default now **`False`** (fail-closed); opt-in only for legacy fakes |
| P0 (fixed) | NFT auctions / offer settle used float as money authority | Satoshi twins on create/bid/finalize; settle prefers `price_satoshi` |
| P1 (fixed) | CORS resolver could emit `*` if mis-listed even under prod | Prod path returns empty ACAO (defense in depth; config.validate already refuses `*`) |
| Benign | `verify=False` hit in comments only (`network/p2p_tls.py`) | No change |
| Benign | `except→pass` cleanup / optional native probe | No change (not paint-green on tip/money) |
| Benign | `except→return True` in sync genesis-need / stall detect | Fail-closed toward catch-up / stall, not ready-green |
| Residual (org) | External firm audit / NDA / Phase 6 human kickoff | Not code — see `docs/EXTERNAL_AUDIT_ENGAGEMENT.md` |
| Residual (R&D) | Long-Range / NFT `feature_*=false` on 778888; Experimental mesh may keep `feature_libp2p=true` (ADR 0020) | Intentional — do not flip Long-Range/NFT on pin |
| Residual | Mesh probe / industrial gate for core/P2P changes | **Not run this pass** (no tip/P2P/native edits) |

## What was *not* done (on purpose)

- No Big-bang rewrite of consensus / tip-safety / mempool / Rocks / PyO3.
- No prod feature flag flips (`feature_nft`, `feature_long_range`, bridge ON).
- No “improve absolutely every folder” drive-by — that would break industrial order.
- No soak claim.

## Honesty label

`industrial_audit_scan_2026-10-01` — surgical fail-closed harden only; unit + honesty gate evidence; **not** mesh L1 acceptance for this delta.
