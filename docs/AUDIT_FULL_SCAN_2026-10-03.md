# Full diligence audit scan — 2026-10-03

**Repo:** [`dup-protocol-experimental`](https://github.com/Gruver87/dup-protocol-experimental) (local: `Absolute_Blockchain_Experimental`)  
**Tip at scan:** `9944c55`  
**Audience:** fund / corporate technical diligence (pre firm audit)  
**Not claimed:** public mainnet · firm pen-test PASS · L1/EVM vendor PDF · new 48h soak from this scan

---

## Method (Big-4 style ladder)

1. **Scope freeze** — industrial private mesh / R&D L1; pin vs Experimental split respected.
2. **Evidence first** — gates, probes, packaged soaks; no green from pytest alone on tip/P2P.
3. **Critical-path pattern scan** — `scripts/audit_critical_paths.py` + money/TLS/CORS/feature flags.
4. **90-day audit phases A–H** — `.\scripts\verify_audit_phase.ps1 -Phase All -SkipGate`.
5. **Live mesh** — `verify_prod_mesh_probe` + `check_mesh_catchup` on `:18180–:18182`.
6. **Org blockers** — `external_audit` evaluate (human items stay pending).
7. **Surgical fix only** — no Great Merge, no prod Long-Range, no bridge ON.

---

## Live results (this pass)

| Gate / probe | Result |
|--------------|--------|
| `check_secrets.py` | OK |
| `prod_gate.py` | OK |
| `industrial_gate.py` | OK (3 warnings: 2 human audit + bridge.example ON) |
| `monolith_gate.py --bridge-cutover` | OK (warnings: audit + bridge cutover placeholders) |
| `mainnet_readiness.py --no-strict-audit` | OK (2 human audit warnings) |
| `audit_critical_paths.py` | No new CRITICAL; known `feature_libp2p=true` on Experimental prod mesh (ADR 0020); float fallback only behind explicit opt-in |
| Audit 90d phases A–H (`-SkipGate`) | **PASS** |
| Live mesh probe deep | **OK** tip ~105214 peers=2/2/2 |
| Mesh catch-up / wire | **PASS** ready_200 + consist + wire |
| CI on `main` @ `9944c55` | Blockchain Tests · Experimental R&D · Security · Docker — **success** |
| Ceremony status (operator disk) | `ready=True` pin match — **≠** public mainnet |
| Packaged 48h Experimental soak | On disk PASS (`soak_report_48h_experimental.json`); **not** re-run this scan |
| 5h STRICT local report | Honest **FAIL** (`hard_fails=177`) — do not relabel |

---

## Findings triage

| Sev | Finding | Action |
|-----|---------|--------|
| P1 (fixed) | `pre_mainnet_audit.py` painted all 8 external checklist rows `[ ]` even when live evaluate / tracker had 6/8 PASS — diligence under-claim / confusion for fund decks | Now uses `runtime.external_audit.evaluate`; report JSON includes `external_audit` summary; prints `[x]`/`[ ]` + notes |
| P1 (fixed) | `Wallet.export` / plaintext `import_wallet` allowed bare calls (ops footgun — critical-path scan HIGH) | Require `allow_plaintext=True` or password keystore; ceremony/mesh/dev callers explicit |
| P1 (fixed) | `execution/mempool` + `secure_mempool` float-only add (legacy layer HIGH) | `resolve_wire_amount_sat`; prod/staging (`DEPLOYMENT_MODE`) refuse float-only; bind `amount_satoshi` |
| P1 (fixed) | `bridge/adapter` credit from float when satoshi absent | Coerce always binds satoshi twin; confirm refuses if still missing |
| P2 (fixed) | `FileSecretAdapter(allow_prod=…)` latent bypass | Knob removed — prod always refused (ADR 0015) |
| P0 (fixed) | `storage/types.SATOSHI_PER_COIN=1e8` (Bitcoin scale) while protocol is **1e6** — float→satoshi mis-scale on `AccountRecord.from_mapping` | Alias `SATOSHI_MULTIPLIER`; convert via `to_satoshi` |
| P1 (fixed) | `crypto.signing.create_signed_transaction` invented gas 21000/1 | Require explicit `gas_limit` / `gas_price` |
| P1 (fixed) | BFT round SM swallowed lockdown failure after slash | Re-raise — fail-closed |
| P2 (fixed) | Prod example/k8s JSON omitted explicit `feature_libp2p` / `feature_long_range` / `feature_nft` | Set `false` (pin/TCP examples; Experimental mesh JSON unchanged ADR 0020) |
| P2 (docs) | `FUND_READINESS.md` CI tip still said `719deb4` while `main` moved | Clarified: current CI tip `9944c55`; soak pack tip stays `719deb4` |
| P1 (fixed) | `Transaction.value: float` apply authority residual | `amount_satoshi` twin on Transaction; `resolve_tx_value_satoshi` + `plan_transfer_fees_sat(value_satoshi=…)`; from_dict mismatch refuse. Display float retained (Wave C dual-write) |
| P1 (fixed) | Mining/P2P/HTTP dropped `amount_satoshi` on Mempool→Transaction | Bound on `main` forge, mempool validate, P2P ingest, `/tx/send`+deploy/call; `get_sorted_transactions` emits satoshi |
| Residual MED | Full type erase of `Transaction.value: float` | Later ADR — satoshi twin is authority when present |
| Residual HIGH (known) | Experimental mesh `feature_libp2p=true` + `p2p_tls_enabled=false` | ADR 0020 Noise; pin stays TCP+TLS — do not sell as pin parity |
| Residual org **P0 for mainnet** | Pen-test scheduled + third-party L1/EVM audit PDF | **Not code** — Phase 6 firm kickoff |
| Residual org | Bridge L1 contracts / cutover env placeholders | Keep bridge OFF on live mesh |
| Residual intentional | `feature_long_range=false` on prod | ADR 0017 lab-only |
| Residual R&D | Absolute-VM ≠ Yellow Paper; EVM subset | Disclosed in matrix / ADR 0023 |
| Benign | `/market/fx` uses float for FX display amounts | Not ledger money |

Critical-path search (no CRITICAL green-paint): [Critical-path security scan](556bf27c-14b0-46dc-a1de-2a2064fab99a).

---

## What was *not* done (on purpose)

- No tip-safety / consensus / mempool / Rocks / PyO3 rewrite.
- No prod feature flag flips (NFT / Long-Range / bridge ON).
- No invented “100% mainnet ready” label.
- No new 48h soak started (operator-ordered only).
- No Big-bang “fix every folder” — that would break industrial order.

---

## Fund / corporate readiness (honest)

| Question | Answer |
|----------|--------|
| Ready for technical diligence on industrial private mesh? | **Yes** — gates green, mesh live, evidence packs on disk, CI green |
| Ready to claim public audited mainnet? | **No** — 2 human firm items open |
| Ready for firm engagement kickoff? | **Prep yes** — Phase H / `phase6prep1` / outreach docs; NDA + schedule still org |

---

## Re-run

```powershell
python scripts/audit_critical_paths.py
python scripts/pre_mainnet_audit.py
.\scripts\verify_audit_phase.ps1 -Phase All
python scripts/verify_prod_mesh_probe.py
python scripts/check_mesh_catchup.py
```

**Honesty label:** `industrial_diligence_scan_2026-10-03` — static + live mesh + surgical diligence fix; **not** firm audit PASS · **not** soak from this delta.
