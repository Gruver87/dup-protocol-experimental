# Diligence brief — DUP Protocol / DUP Labs (honest)

**Audience:** grant officers, investors, HTP / ПВТ reviewers, technical advisors.  
**Date:** 2026-10-01 · Language: English (canonical)  
**Brand:** [BRAND.md](BRAND.md) — **DUP Labs** (org) · **DUP Protocol** (product) · Uladzimir Dabranski (D.U.P.)  
**Repos:** [`Gruver87/dup-protocol-experimental`](https://github.com/Gruver87/dup-protocol-experimental) (R&D) · [`Gruver87/dup-protocol`](https://github.com/Gruver87/dup-protocol) (industrial pin)  
**Former name:** Absolute Blockchain (same trees / evidence).  
**Showcase front door:** [SHOWCASE.md](SHOWCASE.md) · FAQ: [FAQ.md](FAQ.md) · one-pager: [ONE_PAGER.md](ONE_PAGER.md) / [ONE_PAGER_RU.md](ONE_PAGER_RU.md)

This page is the **15-minute path**. Claims below map to **on-disk evidence packs** under [`docs/evidence/runs/`](evidence/runs/). Soft marketing language is refused.

---

## One sentence

**DUP Protocol** (by **DUP Labs**) is an **industrial hybrid L1** (Python orchestration + Rust/PyO3 hot path) with a **fail-closed** private prod-profile mesh, evidence-backed 48h soaks, and an explicit split between an **audit-freeze pin** and an **R&D sandbox**.

---

## Two repositories (on purpose)

| Tree | Role | What you can claim today |
|------|------|--------------------------|
| **Industrial pin** ([`dup-protocol`](https://github.com/Gruver87/dup-protocol)) | DUP Protocol audit-freeze · tag [`v1.3.1339-tip-v2-industrial`](https://github.com/Gruver87/dup-protocol/releases/tag/v1.3.1339-tip-v2-industrial) | Tip-v2 48h soak PASS · Phase 4 binder READY for **firm** engagement · **not** public mainnet |
| **experimental** (this repo) | DUP Protocol R&D sandbox · libp2p / Long-Range / EVM depth / mempool Rust | Phases **1–5 closed** with packaged 48h evidence · Phase 6 **prep** on disk (`phase6prep1`); firm kickoff / pen-test / L1 audit PDF still **org-open** |

Hybrid stays freeze-safe. Experimental absorbs transport / Long-Range / EVM-depth risk. Do **not** conflate the two.

---

## Stage of development (honest)

| Stage | Status |
|-------|--------|
| Working local **3-node prod-profile mesh** (chain `778888`) | **Proven** — probe + multi-pack 48h soaks |
| Fail-closed money path (satoshi integers; float refuse on wire) | **Proven** — units + mesh [`ind48pass1`](evidence/runs/ind48pass1/) |
| ABS ledger persist satoshi dual-write (AUDIT Phase G) | **Code+gate** — SQLite/Rocks twins for stake/bridge/sprouts/NFT/burn/tx+receipts; Phase G PASS; **not** a new soak |
| Industrial R&D ceiling for this sandbox | **Reached** for Phases 1–5 — see [INDUSTRIAL_MAX_SCAN](INDUSTRIAL_MAX_SCAN_2026-09-20.md) |
| Public audited mainnet / listed token / BLS prod | **Not claimed** |
| External firm security audit PDF | **Pending** (Phase 6) — prep: [`FIRM_KICKOFF_CHECKLIST.md`](FIRM_KICKOFF_CHECKLIST.md) · outreach draft [`FIRM_OUTREACH_LETTER.md`](FIRM_OUTREACH_LETTER.md) · pack [`phase6prep1`](evidence/runs/phase6prep1/) · **not** firm PASS |

**Bottom line for funds / ПВТ:** ready for **technical diligence on an industrial private mesh / R&D L1**. Not ready to claim **public audited mainnet**.

---

## Evidence scorecard — Experimental (all packs on `main`)

### STRICT 48h bar (`IntervalSec=60`, `fail=0`, `mesh_warn=0`)

| Pack | Window | Tip | Cycles | Proof |
|------|--------|-----|--------|-------|
| Libp2p STRICT [`lp2pstrict1`](evidence/runs/lp2pstrict1/) | 2026-09-23→25 | ~57209→~68082 | mesh_ok=2800 | ADR 0020 Noise mesh |
| Mempool+validation STRICT [`mempool48pass1`](evidence/runs/mempool48pass1/) | 2026-09-17→19 | ~35187→~44020 | dual-report + sidecar | ADR 0021 path |
| Long-Range lab STRICT [`lrstrict1`](evidence/runs/lrstrict1/) | 2026-09-26→28 | ~18646→~30096 | mesh_ok=2849 | ADR 0017 **lab** ports |
| EVM STRICT [`evmstrict1`](evidence/runs/evmstrict1/) | 2026-09-28→30 | ~85200→~96089 | mesh_ok=2801 | post-EVM-prep mesh |

### Default / prior 48h PASS (still valid; not STRICT)

| Pack | What it proves |
|------|----------------|
| [`3c801b87`](evidence/runs/3c801b87/) | B1 — first libp2p industrial 48h PASS |
| [`0a7932c4`](evidence/runs/0a7932c4/) | TCP+TLS 48h PASS (do not relabel as libp2p) |
| [`lr48pass1`](evidence/runs/lr48pass1/) | B2 — Long-Range **lab** 48h (prod flag stays off) |
| [`evm48pass1`](evidence/runs/evm48pass1/) | Phase 3 post-EVM-prep mesh 48h |
| [`ind48pass1`](evidence/runs/ind48pass1/) | Phase 5 industrial polish + ADR 0021 wire on mesh |

### Historical FAIL (kept on purpose — honesty)

| Pack | Note |
|------|------|
| [`35104db0`](evidence/runs/35104db0/), [`87f51b3e`](evidence/runs/87f51b3e/) | libp2p 48h FAIL → healed → `3c801b87` |
| [`lr48fail1`](evidence/runs/lr48fail1/) | LR lab 48h FAIL → healed → `lr48pass1` / `lrstrict1` |

### Host / gate evidence (not soak)

| Artifact | Result |
|----------|--------|
| ADR 0021 global R&D audit [`adr0021gaudit1`](evidence/runs/adr0021gaudit1/) | **13/13** FullLaunch+Rebuild |
| Industrial waves + pytest (2026-09-21) | **542 needles** · **2734 passed** / 11 skipped |
| Hard gate ADR 0019 | **117** steps with `--rebuild` |
| CI on `main` | Experimental R&D · Tests · Security (cargo-audit) |

Full ledger: [EVIDENCE_MATRIX](EVIDENCE_MATRIX.md) · pack index: [evidence/README](evidence/README.md).

---

## What was built (technology)

```text
API / JSON-RPC / WebSocket  →  Core + Mempool  →  Consensus / P2P / Sync
                                      ↓
                              StoragePort / RocksDB
                                      ↓
                              abs_native (Rust / PyO3)
```

| Layer | Ownership |
|-------|-----------|
| Orchestration, consensus policy, secrets, metrics | **Python** |
| Crypto, state roots, RocksDB, EVM kernels, rust-libp2p | **Rust** (`abs_native`) |
| Experimental mesh transport | **libp2p Noise/Yamux** (ADR 0020) |
| Hybrid pin transport | **TCP+TLS** (unchanged) |
| Money | **satoshi integers only** — float refuse on wire |
| Long-Range (ADR 0017) | **Lab-only** until ADR complete; prod JSON `feature_long_range=false` |

ADRs: tip-safety 0001 · hybrid 0009 · profiles 0016 · Long-Range 0017 · libp2p 0019–0020 · mempool Rust 0021 · council 0022 (staging).

---

## What we do **not** claim

- Public mainnet / listed ABS / token sale  
- Completed **external** firm security audit  
- Long-Range **production** / BLS quorum  
- Full geth parity / EIP-4844 / **EVM-only** 48h  
- Bridge L1 lock/mint contracts live  
- NIST PQ signature backends (correct `NotImplemented`)  
- Relabeling Hybrid pin as this Experimental tree  

Gaps stay visible: [MAINNET_GAP_ANALYSIS](MAINNET_GAP_ANALYSIS.md).

---

## Pipeline closed (Phases 1–5)

| Phase | Track | Evidence |
|:-----:|-------|----------|
| 1 | libp2p mesh 48h | [`3c801b87`](evidence/runs/3c801b87/) + STRICT [`lp2pstrict1`](evidence/runs/lp2pstrict1/) |
| 2 | Long-Range lab | [`lr48pass1`](evidence/runs/lr48pass1/) + STRICT [`lrstrict1`](evidence/runs/lrstrict1/) |
| 3 | EVM mesh | [`evm48pass1`](evidence/runs/evm48pass1/) + STRICT [`evmstrict1`](evidence/runs/evmstrict1/) |
| 4 | Mempool → Rust | [`adr0021gaudit1`](evidence/runs/adr0021gaudit1/) + [`mempool48pass1`](evidence/runs/mempool48pass1/) |
| 5 | Industrial tip | [`ind48pass1`](evidence/runs/ind48pass1/) |
| **6** | Org / firm audit / ceremony live | **Open** |

Detail: [EXECUTION_ORDER](EXECUTION_ORDER.md) · skimmer: [AT_A_GLANCE](AT_A_GLANCE.md).

---

## How to verify (60 minutes)

1. Read this page + [FUND_READINESS](FUND_READINESS.md)  
2. Open any STRICT pack README (e.g. [`evmstrict1`](evidence/runs/evmstrict1/)) — check `passed=true`, `hard_fails=0`  
3. Skim [EVIDENCE_MATRIX](EVIDENCE_MATRIX.md) soak index  
4. Confirm GitHub Actions green on `main`  
5. Hybrid firm-audit path (separate tree): [AUDIT_ENGAGEMENT_BRIEF](https://github.com/Gruver87/dup-protocol/blob/master/docs/AUDIT_ENGAGEMENT_BRIEF.md)

Optional workstation: `.\scripts\verify_pre_soak.ps1 -SkipPrepare` with a live mesh.

---

## Author / contact

**Uladzimir Dabranski (D.U.P.)** — Dabranski · Uladzimir · Petrovich · GitHub: [Gruver87](https://github.com/Gruver87)  
**Org / product:** DUP Labs · DUP Protocol · [BRAND.md](BRAND.md)

Profile card source: [`.github/PROFILE_README.md`](../.github/PROFILE_README.md)
