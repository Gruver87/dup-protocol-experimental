# Fund / diligence readiness — DUP Protocol Experimental (honest)

**Audience:** grant officers, investors, HTP / ПВТ reviewers, technical advisors.  
**Date:** 2026-10-01 · Repo: [`Gruver87/dup-protocol-experimental`](https://github.com/Gruver87/dup-protocol-experimental) · branch `main`  
**Brand:** [BRAND.md](BRAND.md) — **DUP Labs** · **DUP Protocol** · Uladzimir Dabranski (D.U.P.)  
**Not:** public audited mainnet · not the industrial audit-freeze pin · not listed token.  
**Former name:** Absolute Blockchain Experimental (same codebase). GitHub: [`dup-protocol-experimental`](https://github.com/Gruver87/dup-protocol-experimental).

**Showcase front door:** [SHOWCASE.md](SHOWCASE.md)  
**15-minute brief:** [DILIGENCE_BRIEF.md](DILIGENCE_BRIEF.md)  
One-screen status: [AT_A_GLANCE.md](AT_A_GLANCE.md) · Evidence ledger: [EVIDENCE_MATRIX.md](EVIDENCE_MATRIX.md) · Gaps: [MAINNET_GAP_ANALYSIS.md](MAINNET_GAP_ANALYSIS.md) · Vision (industrial pin): [VISION](https://github.com/Gruver87/dup-protocol/blob/master/docs/VISION.md).

---

## What this is

Industrial **R&D / private-testnet** hybrid L1 — product **DUP Protocol**, org face **DUP Labs** (Python orchestration + Rust hot path). Experimental mesh default transport: **rust-libp2p Noise/Yamux (ADR 0020)**. Industrial pin remains TCP+TLS.

**Why two repos:** the Hybrid-named GitHub tree is the freeze-safe industrial pin for firm audit engagement. Experimental is where libp2p, Long-Range (lab), EVM depth, and mempool-Rust risk land — each closed phase leaves a packaged evidence directory under [`docs/evidence/runs/`](evidence/runs/).

---

## What we claim (with evidence)

| Claim | Evidence |
|-------|----------|
| libp2p industrial mesh 48h | [`3c801b87`](evidence/runs/3c801b87/) `hard_fails=0` |
| Libp2p STRICT 48h (mempool-parity bar) | [`lp2pstrict1`](evidence/runs/lp2pstrict1/) `strict=true` `warn_lines=0` tip ~57209→~68082 |
| Long-Range **lab** 48h (default) | [`lr48pass1`](evidence/runs/lr48pass1/) — prod JSON keeps `feature_long_range=false` |
| Long-Range **lab STRICT** 48h | [`lrstrict1`](evidence/runs/lrstrict1/) `strict=true` fail=0 mesh_warn=0 tip ~18646→~30096 |
| Post-EVM prep mesh 48h | [`evm48pass1`](evidence/runs/evm48pass1/) |
| EVM STRICT 48h (Phase 3b) | [`evmstrict1`](evidence/runs/evmstrict1/) `strict=true` fail=0 mesh_warn=0 tip ~85200→~96089 |
| Mempool+validation STRICT 48h | [`mempool48pass1`](evidence/runs/mempool48pass1/) |
| ADR 0021 global R&D audit | [`adr0021gaudit1`](evidence/runs/adr0021gaudit1/) 13/13 |
| Wire satoshi cutover + float-only refuse | Units + industrial waves; **mesh 48h** [`ind48pass1`](evidence/runs/ind48pass1/) |
| Host verify restore | Waves 542 needles + pytest **2734 passed** (2026-09-21) |
| Industrial polish tip 48h (`719deb4`) | [`ind48pass1`](evidence/runs/ind48pass1/) `hard_fails=0` tip ~46099→~56972 |

### STRICT scoreboard (one glance)

| Pack | fail | mesh_warn | warn_lines | tip | mesh_ok |
|------|:----:|:---------:|:----------:|-----|:-------:|
| [`lp2pstrict1`](evidence/runs/lp2pstrict1/) | 0 | 0 | 0 | ~57209→~68082 | 2800 |
| [`mempool48pass1`](evidence/runs/mempool48pass1/) | 0 | 0 | 31 soft | ~35187→~44020 | dual+sidecar |
| [`lrstrict1`](evidence/runs/lrstrict1/) | 0 | 0 | 0 | ~18646→~30096 | 2849 |
| [`evmstrict1`](evidence/runs/evmstrict1/) | 0 | 0 | 0 | ~85200→~96089 | 2801 |

Every STRICT pack: `passed=true`, `IntervalSec=60`, packaged under `docs/evidence/runs/<id>/` with README + report + log.

---

## What we do **not** claim

- Public mainnet / external firm security audit complete  
- Long-Range production / BLS  
- Full geth parity / EIP-4844 / **EVM-only** 48h  
- Bridge L1 lock/mint contracts live  
- NIST PQ signature backends (correct `NotImplemented`)  
- Hybrid pin relabel as this tree  

---

## Architecture (diligence map)

```text
API / JSON-RPC / WebSocket  →  Core + Mempool  →  Consensus / P2P / Sync
                                      ↓
                              StoragePort / Rocks
                                      ↓
                              abs_native (Rust PyO3)
```

ADRs: 0001 tip-safety · 0009 hybrid · 0016 profiles · 0017 Long-Range (lab) · 0019–0020 libp2p · 0021 mempool Rust · 0022 council (staging).

---

## Pre-audit checklist (code side)

| Item | Status |
|------|--------|
| Fail-closed money (satoshi) + wire refuse float-only | Done |
| ABS ledger persist satoshi dual-write (AUDIT Phase G) | Done — code+gate; **not** a new soak |
| Phase 5 host lab re-verify (oracle/shard/bridge OFF) | Done — [`phase5reverify2`](evidence/runs/phase5reverify2/) |
| Persist / backup fail-closed | Done |
| Industrial HIGH honesty pack | Done |
| Host pytest + waves green | Done 2026-09-21 |
| Mesh probe + pre-soak | Done 2026-09-21 → led to soak |
| Ceremony dry-run status | `ceremony_status` ready=True (≠ mainnet) |
| CI badges green (Security / Tests / Experimental R&D) | Tip `719deb4` — all four workflows green |
| Tip 48h soak after industrial polish (`719deb4`) | **PASS** [`ind48pass1`](evidence/runs/ind48pass1/) |
| Libp2p STRICT 48h (`start_soak_prod_mesh_48h_strict.ps1`) | **PASS** [`lp2pstrict1`](evidence/runs/lp2pstrict1/) |
| Long-Range STRICT 48h (`start_soak_long_range_lab.ps1 -Hours 48 -Strict`) | **PASS** [`lrstrict1`](evidence/runs/lrstrict1/) |
| EVM STRICT 48h (`start_soak_evm_mesh_48h_strict.ps1`) | **PASS** [`evmstrict1`](evidence/runs/evmstrict1/) 2026-09-28→30 — fail=0 mesh_warn=0 tip ~85200→~96089 |
| External audit / secrets rotate / validator ceremony live | Org Phase 6 |

---

## CI badges (must be green for diligence)

- Experimental R&D · Blockchain Tests · Security checks (cargo-audit)

If a badge is red: treat as **blocker for fund decks** until fixed on `main`.

---

## Recommended diligence path (60 minutes)

1. Read [DILIGENCE_BRIEF](DILIGENCE_BRIEF.md) + this page + [AT_A_GLANCE](AT_A_GLANCE.md)  
2. Skim [EVIDENCE_MATRIX](EVIDENCE_MATRIX.md) soak index — open at least one STRICT pack README  
3. Open GitHub Actions on `main` — confirm green  
4. Optional: `.\scripts\verify_pre_soak.ps1 -SkipPrepare` on a workstation with mesh  
5. Hybrid engagement brief (firm audit): [Hybrid AUDIT_ENGAGEMENT_BRIEF](https://github.com/Gruver87/dup-protocol/blob/master/docs/AUDIT_ENGAGEMENT_BRIEF.md)

**Bottom line:** ready for **technical diligence on an industrial private mesh / R&D L1**. Not ready to claim **public audited mainnet**.
