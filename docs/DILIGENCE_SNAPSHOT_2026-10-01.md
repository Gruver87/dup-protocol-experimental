# Pre-fund / pre-audit diligence snapshot — 2026-10-01

**Product:** DUP Protocol (DUP Labs)  
**Kind:** operator self-check before funds / firm engagement  
**Not:** firm audit PASS · pen-test PASS · 48h soak claim · public mainnet · listed ABS

---

## Trees

| Tree | Ref | Role |
|------|-----|------|
| Experimental | `c2d24ff` (`main`) | R&D sandbox · this snapshot host |
| Industrial pin | tag `v1.3.1339-tip-v2-industrial` · SHA `0531995d41673a807b5c21ddf1beb7b5034eab07` | Firm engagement scope |

## Live Experimental mesh (operator-local)

| Check | Result |
|-------|--------|
| `probe_prod_mesh.ps1 -Quick` | **OK** · `logs/prod_mesh_probe.json` |
| Nodes | `:18180` / `:18181` / `:18182` · chain **778888** · `deployment_mode=prod` |
| Tip (probe) | **97156** · head `9e99fb32…` aligned 3/3 (later tip advanced under mining) |
| Peers | 2 each · `ready=true` |
| Bridge | **OFF** (`rust_bridge` disabled; L1 placeholder WARN expected) |
| Sprout flags | stay **false** on prod JSON (NFT/AI/LR not armed) |

## Adversarial smoke (live mesh)

| Check | Result |
|-------|--------|
| `eth_blockNumber` without RPC key | **401** |
| CORS `Origin: https://evil.example` | **PASS** — no ACAO |
| Admin mint without JWT | **401** |
| Faucet POST without auth | **401** (auth gate before faucet body) |

## STRICT 48h attempt (2026-10-01)

1. First `start_soak_evm_mesh_48h_strict.ps1 -SkipRebuild` → **blocked** by transient `harness roots mismatch` during docker recreate race.  
2. Retry path: `evm_pre_48h_harness` **PASS** · `prepare_48h_soak` **READY** · `start_soak_prod_mesh_48h_strict.ps1 -SkipPreflight` → **STARTED** PID **15476** (log `logs/soak_48h_evm_strict.log`, report `logs/soak_report_48h_evm_strict.json`).  
3. **Not yet PASS** — claim only after ~48h with a **new** `passed=true` report. Stale prior report from 2026-09-28 (`evmstrict1`) was archived to `logs/soak_report_48h_evm_strict.PRIOR_evmstrict1_2026-09-28.json` so `check_soak` cannot paint green early. Keep PC awake; no docker rebuild until done. Check: `.\scripts\check_soak.ps1`

## Pin audit pack

Exported: `Absolute_Blockchain_Ultimate_Hybrid/logs/audit_pack_20261001.zip` (pin soak reference `375d14f` — Hybrid tip-v2, not Experimental).

## Evidence already on disk (do not re-claim as new)

STRICT packs: `lp2pstrict1` · `lrstrict1` · `evmstrict1` · `mempool48pass1`  
Default tip: `ind48pass1` · Phase 6 prep: `phase6prep1`  
Face: [DILIGENCE_BRIEF](DILIGENCE_BRIEF.md) · [EVIDENCE_MATRIX](EVIDENCE_MATRIX.md)

## External audit tracker

**6/8** automated complete. Human still open:

- [ ] External penetration test scheduled  
- [ ] Third-party L1 / smart-contract security audit completed  

## Honest claim for funds / ПВТ today

Industrial private 3-node prod-profile mesh + packaged 48h evidence + fail-closed money path + Phase 6 **prep**.  
**Not** externally audited · **not** mainnet-ready · **not** a new soak from this snapshot alone.

## Next (human)

1. Sign NDA with chosen firm (template: [FIRM_NDA_OUTLINE.md](FIRM_NDA_OUTLINE.md))  
2. Send [FIRM_OUTREACH_LETTER.md](FIRM_OUTREACH_LETTER.md) + pin SHA above  
3. Schedule pen-test + L1 review ([FIRM_ENGAGEMENT_CALENDAR.md](FIRM_ENGAGEMENT_CALENDAR.md))  
4. Optional: new STRICT 48h pack only if ordered and PC stays awake 48h  

Report stamp: 2026-10-01T21:54Z (probe) · experimental tip `c2d24ff`.
