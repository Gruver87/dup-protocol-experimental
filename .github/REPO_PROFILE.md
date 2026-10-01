# GitHub repository profile — Gruver87/dup-protocol-experimental

**Display brand:** DUP Labs · DUP Protocol (Experimental). See [docs/BRAND.md](../docs/BRAND.md).  
GitHub repo URL stays `experimental` (no rename this change).

Apply with:

```powershell
gh repo edit Gruver87/dup-protocol-experimental --description "DUP Protocol (DUP Labs) — industrial R&D L1. Phases 1–5 closed: lp2pstrict1 + lrstrict1 + evmstrict1 + mempool48pass1 + ind48pass1. Diligence: docs/DILIGENCE_BRIEF.md. Formerly Absolute Blockchain Experimental. Not the audit pin / not mainnet."
gh repo edit Gruver87/dup-protocol-experimental --homepage "https://github.com/Gruver87/dup-protocol-experimental/blob/main/docs/DILIGENCE_BRIEF.md"
gh repo edit Gruver87/dup-protocol-experimental --enable-wiki=false
@(
    "absolute-blockchain","blockchain","blockchain-node","layer1","python","rust","pyo3",
    "p2p","libp2p","evm","experimental","research","devnet","cryptography","web3",
    "json-rpc","rest-api","rocksdb","hybrid-blockchain","noise-protocol"
) | ForEach-Object { gh repo edit Gruver87/dup-protocol-experimental --add-topic $_ }
```

Or paste into **Settings → General → About**.

| Field | Value |
|-------|-------|
| **Description** | DUP Protocol (DUP Labs) — industrial R&D L1. Phases 1–5 closed: lp2pstrict1 + lrstrict1 + evmstrict1 + mempool48pass1 + ind48pass1. Diligence: docs/DILIGENCE_BRIEF.md. Formerly Absolute Blockchain Experimental. Not the audit pin / not mainnet. |
| **Website** | https://github.com/Gruver87/dup-protocol-experimental/blob/main/docs/DILIGENCE_BRIEF.md |
| **Social preview** | Upload evergreen `docs/assets/repo-banner.svg` (export PNG 1280×640) in **Settings → General · Social preview** |
| **Brand** | [docs/BRAND.md](../docs/BRAND.md) |
| **Skimmer card** | [docs/AT_A_GLANCE.md](../docs/AT_A_GLANCE.md) |
| **Diligence brief (funds / ПВТ)** | [docs/DILIGENCE_BRIEF.md](../docs/DILIGENCE_BRIEF.md) |
| **Fund / diligence** | [docs/FUND_READINESS.md](../docs/FUND_READINESS.md) |
| **Execution order** | [docs/EXECUTION_ORDER.md](../docs/EXECUTION_ORDER.md) |
| **Cite** | [CITATION.cff](../CITATION.cff) |
| **Issue chooser** | Bug · Feature · Ops/verify · private vulnerability report · industrial pin (other repo) |

## Topics

```
absolute-blockchain
blockchain
blockchain-node
layer1
python
rust
pyo3
p2p
libp2p
evm
experimental
research
devnet
cryptography
web3
json-rpc
rest-api
rocksdb
hybrid-blockchain
noise-protocol
```

> Cap = 20 topics. Keep `experimental` / `libp2p` / `research` / historical `absolute-blockchain` so search still finds the tree. Product brand is **DUP Protocol**.

## Branches

| Branch | Role |
|--------|------|
| **`main`** | **Default** — R&D landing |
| `rd/*` | Slice work before merge |

## Current release

| Field | Value |
|-------|-------|
| **Tag** | `rd-1.0.0` — first R&D GitHub Release; `main` through Slice DB phase 105 |
| **ADR stack** | Industrial pin 0001–0016 inherited · **0017–0021** Experimental |
| **Hard gate** | 117 steps with `--rebuild` |
| **Closed** | B1 [`3c801b87`](../docs/evidence/runs/3c801b87/) · B2 [`lr48pass1`](../docs/evidence/runs/lr48pass1/) + STRICT [`lrstrict1`](../docs/evidence/runs/lrstrict1/) · Phase 3 [`evm48pass1`](../docs/evidence/runs/evm48pass1/) + STRICT [`evmstrict1`](../docs/evidence/runs/evmstrict1/) · Phase 4 [`adr0021gaudit1`](../docs/evidence/runs/adr0021gaudit1/) + STRICT [`mempool48pass1`](../docs/evidence/runs/mempool48pass1/) · Phase 5 industrial tip [`ind48pass1`](../docs/evidence/runs/ind48pass1/) · libp2p STRICT [`lp2pstrict1`](../docs/evidence/runs/lp2pstrict1/) |
| **Open / next** | Phase 6 org kickoff (prep on disk [`phase6prep1`](../docs/evidence/runs/phase6prep1/)) — [FIRM_KICKOFF_CHECKLIST](../docs/FIRM_KICKOFF_CHECKLIST.md) · [DILIGENCE_BRIEF](../docs/DILIGENCE_BRIEF.md) · [FUND_READINESS](../docs/FUND_READINESS.md) · operator SDK [`sdk/`](../sdk/) · [AUDIT_FULL_SCAN_2026-10-01](../docs/AUDIT_FULL_SCAN_2026-10-01.md) |
| **Notes** | [CHANGELOG](../CHANGELOG.md) · [RELEASING](../docs/RELEASING.md) · [AT_A_GLANCE](../docs/AT_A_GLANCE.md) |
| **Industrial sibling** | [`dup-protocol`](https://github.com/Gruver87/dup-protocol) — **DUP Protocol industrial pin** · **not** this freeze |
| **Self-check** | `.\scripts\verify_global_rd_audit.ps1` · `.\scripts\verify_pre_soak.ps1` · `.\scripts\verify_audit_engagement_prep.ps1` · `python scripts/verify_experimental_rd.py` · `python scripts/dup_sdk_lab.py` |
| **CI** | `experimental-rd.yml`, `test.yml`, `security-audit.yml` |
| **Community health** | **100%** (GitHub community profile) |

### Not yet proven (do not claim in About)

- External security audit
- Long-Range **prod** `feature_long_range` / BLS / mainnet Long-Range
- EVM-only 48h / full geth / EIP-4844
- Public VPS testnet / launched mainnet / listed token
- GPG-signed release tags (annotated tags in use when signing key absent)
- Thin SDK / NFT / AI labs as production or pin SDK

## Honest positioning (release / About)

- **Is:** DUP Protocol R&D (DUP Labs); rust-libp2p industrial mesh **48h PASS** + STRICT [`lp2pstrict1`](../docs/evidence/runs/lp2pstrict1/); Long-Range **lab** 48h PASS + STRICT [`lrstrict1`](../docs/evidence/runs/lrstrict1/); Phase 3 post-EVM mesh **48h PASS** + EVM STRICT [`evmstrict1`](../docs/evidence/runs/evmstrict1/); mempool+validation STRICT **48h PASS**; industrial polish tip **48h PASS** (`ind48pass1`); Phase 6 **prep** + thin SDK + AI/NFT labs + critical-path audit scan; [DILIGENCE_BRIEF](../docs/DILIGENCE_BRIEF.md)
- **Is not:** industrial audit pin; live public mainnet; Long-Range production / BLS; EVM-only 48h; firm audit PDF
- **Banner:** evergreen `docs/assets/repo-banner.svg`
- **Profile README source:** [PROFILE_README.md](PROFILE_README.md) → publish as `Gruver87/Gruver87`
- **Surface date:** 2026-10-01 (SDK · AI/NFT · Phase 6 prep · audit scan face sync)
