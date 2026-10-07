# Fund / demo operator pack — maximum prep (honest)

**Date:** 2026-10-05 · **Repo tip:** run `git rev-parse --short HEAD`  
**Brand:** DUP Labs · DUP Protocol  
**Not:** public audited mainnet · not firm pen-test PASS · not a new 48h soak claim.

This page is the **operator checklist** after diligence + money-honesty waves and the **Exp→pin honesty merge close** on the industrial pin. Use with [SHOWCASE.md](SHOWCASE.md).

---

## What is ready to show

| Layer | Status | Proof |
|-------|--------|-------|
| Industrial pin (freeze + working tip) | Show for firm scope | [`dup-protocol`](https://github.com/Gruver87/dup-protocol) tag `v1.3.1339-tip-v2-industrial` (TCP+TLS soak) · working tip ADR 0020 libp2p (pin soak **deferred**) · diligence tip `215ecf69` |
| Exp→pin honesty merge | **CLOSED** on pin | Units + `industrial_gate` on pin (not a new 48h soak). Pin: [SHOWCASE](https://github.com/Gruver87/dup-protocol/blob/master/docs/SHOWCASE.md) · [FAQ](https://github.com/Gruver87/dup-protocol/blob/master/docs/FAQ.md) · [FUND_DEMO](https://github.com/Gruver87/dup-protocol/blob/master/docs/FUND_DEMO_OPERATOR_PACK.md) |
| Experimental R&D mesh (libp2p) | Show as sandbox | Phases 1–5 CLOSED with packs under [`evidence/runs/`](evidence/runs/) |
| Fail-closed satoshi money | Code + units + midsoak honesty | Waves through CryptoWill / L2 / bridge queue / validator stake + pin merge layers |
| STRICT 48h scoreboard | Packaged (historical) | `lp2pstrict1` · `evmstrict1` · `lrstrict1` · `mempool48pass1` · `ind48pass1` — do not claim on current HEAD |
| Showcase / diligence docs | On disk | [SHOWCASE](SHOWCASE.md) · [DILIGENCE_BRIEF](DILIGENCE_BRIEF.md) · [FUND_READINESS](FUND_READINESS.md) |
| Phase 6 firm prep | Prep only | [FIRM_KICKOFF_CHECKLIST](FIRM_KICKOFF_CHECKLIST.md) · [`phase6prep1`](evidence/runs/phase6prep1/) · pin tracker **6/8** |

---

## Pre-meeting verify (operator)

```powershell
cd C:\Users\vovun\Desktop\Absolute_Blockchain_Experimental

# Honesty needles + units (no mesh restart)
.\scripts\verify_midsoak_honesty.ps1 -Quick

# Money waves from 2026-10-03
python -m pytest `
  tests/unit/test_l2_bridge_mev_satoshi_honesty.py `
  tests/unit/test_will_save_validator_satoshi.py `
  -q --tb=short

# Phase 6 engagement prep (must stay green; not firm PASS)
.\scripts\verify_audit_engagement_prep.ps1

# Optional live mesh (only if Docker mesh already up)
.\scripts\probe_prod_mesh.ps1 -Quick
```

**Pass bar for deck:** midsoak Quick PASS · engagement prep PASS · CI green on `main`.  
**Do not say:** “48h soak on this tip” unless a new pack exists for current HEAD.  
Local **5h STRICT** (`hard_fails=177`) is an honest **FAIL** and is **not** the 48h pipeline.

---

## Demo path (15–60 min)

1. Open [SHOWCASE.md](SHOWCASE.md) + [ELEVATOR_PITCH.md](ELEVATOR_PITCH.md)  
2. One STRICT pack README (recommend [`evmstrict1`](evidence/runs/evmstrict1/)) — show `passed=true`, `hard_fails=0`  
3. Live: [DEMO_RUNBOOK.md](DEMO_RUNBOOK.md) — `/status`, `/health/ready`, tip growth  
4. Honesty: `/status` shows `mev_simulation_only`, L2 `*_execution_bound`, bridge OFF  
5. Gaps: [MAINNET_GAP_ANALYSIS.md](MAINNET_GAP_ANALYSIS.md) — say them first  

Pin demo (firm narrative): pin [DEMO_RUNBOOK_PIN](https://github.com/Gruver87/dup-protocol/blob/master/docs/DEMO_RUNBOOK_PIN.md) / [SHOWCASE](https://github.com/Gruver87/dup-protocol/blob/master/docs/SHOWCASE.md) — freeze soak is **TCP+TLS**; working tip is ADR 0020 libp2p (Quick ≠ 48h). Do not sell Experimental libp2p as “audited pin.”

---

## Closed in code (money / honesty through Exp→pin merge)

- Native/EVM/StateEngine/bridge/shard/pool satoshi twins  
- Lightning/Plasma/HTTP + CryptoWill `amount_satoshi`  
- Feature `save_*` prefer inbound satoshi (mismatch refuse)  
- Validator manifest/boot/registry stake satoshi  
- MEV `simulation_only` · multisig `execution_bound=false`  
- Pool-spend sat admit · no invent gas=21000 · bridge2/fee no invent amount=100  
- WASM nonzero value refused (pseudo host) · AI trade satoshi kwargs  
- **Pin merge close (`adc8547`):** ZK range refuse · committed state_root · height-bounded eth_getLogs · tip_skew/ready honesty · oracle/Lightning/AI finite refuse · Rocks obs counts · bridge debit+burn · Phase 6 kickoff stub (`cc5dfae`)  

---

## Next soak (HEAD re-verify)

**EVM STRICT on current tip — not passed yet.** Historical [`evmstrict1`](evidence/runs/evmstrict1/) ≠ HEAD; 2026-10-03 attempt interrupted ~33.8h (**FAIL**).

Prep + start: [SOAK_HEAD_REVERIFY.md](SOAK_HEAD_REVERIFY.md)

```powershell
.\scripts\prepare_head_soak_evm_strict.ps1          # preflight only
.\scripts\start_soak_evm_mesh_48h_strict.ps1 -SkipRebuild   # 48h — operator
```

---

## Still open (do not green-paint)

| Item | Owner | Notes |
|------|-------|-------|
| External pen-test scheduled + L1 audit PDF | **Org / Phase 6** | Tracker 6/8 until firm evidence |
| Bridge L1 contracts live | Org + cutover | Keep bridge OFF on live mesh |
| Fresh 48h soak on current `main` HEAD | Operator | See [SOAK_HEAD_REVERIFY.md](SOAK_HEAD_REVERIFY.md) — EVM STRICT recommended |
| `Transaction.value: float` type erase | Later ADR | Twin is authority when present |
| Lightning in-channel float fields | MED residual | Twins on persist; deeper sat state later |
| ADR 0020 Exp libp2p vs pin TCP+TLS | Intentional | Do not sell as pin parity |
| Long-Range / BLS / listed token | Not claimed | Lab-only / off in prod JSON |
| CryptoWill / Lightning / Plasma / MEV | Feature flags default **OFF** | Demo must set `FEATURE_*` explicitly; do not imply prod inheritance L1 |

---

## Fund one-liner (approved honesty)

> Ready for **technical diligence on an industrial private mesh / R&D L1**.  
> **Not** ready to claim **public audited mainnet**.

Rough readiness: fund show **~75–85%** · working mesh **~80–90%** · firm audit **~55–65%** · public mainnet **~25–35%**.
