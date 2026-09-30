# At a glance — DUP Protocol Experimental (DUP Labs)

One-screen card. Brand: [BRAND](BRAND.md) · Full detail: [README](../README.md) · sandbox rules: [EXPERIMENTAL_SANDBOX](../EXPERIMENTAL_SANDBOX.md).

## What this is

R&D sandbox for **DUP Protocol** (DUP Labs): rust-libp2p (ADR 0019), Long-Range (ADR 0017), EVM depth. Hybrid Python + Rust L1 **fork** of the industrial pin. Former name: Absolute Blockchain Experimental.

## What it is not

The audit-freeze pin · public audited mainnet · listed token · industrial `v1.3.*-industrial` tags (repo: [`dup-protocol`](https://github.com/Gruver87/dup-protocol)).

## Status

| | |
|---|---|
| Repo | [`Gruver87/dup-protocol-experimental`](https://github.com/Gruver87/dup-protocol-experimental) · default **`main`** |
| R&D tag | **`rd-1.0.0`** (prerelease snapshot) |
| ADR 0019 | Slices **A–DB** · phase **105** |
| Hard gate | **117** steps with `--rebuild` (operator-local, 2026-08-15) |
| Default transport | **libp2p (ADR 0020)** on Experimental prod mesh JSON — Hybrid pin stays TCP+TLS |
| Industrial pin | [Hybrid `v1.3.1339-tip-v2-industrial`](https://github.com/Gruver87/dup-protocol/releases/tag/v1.3.1339-tip-v2-industrial) |
| 48h soaks here | TCP+TLS **PASS** (`0a7932c4`) · **libp2p** [`3c801b87`](evidence/runs/3c801b87/) · **libp2p STRICT** [`lp2pstrict1`](evidence/runs/lp2pstrict1/) · **LR lab** [`lr48pass1`](evidence/runs/lr48pass1/) · **LR STRICT** [`lrstrict1`](evidence/runs/lrstrict1/) · **Phase 3 post-EVM** [`evm48pass1`](evidence/runs/evm48pass1/) · **EVM STRICT** [`evmstrict1`](evidence/runs/evmstrict1/) · **mempool+validation STRICT** [`mempool48pass1`](evidence/runs/mempool48pass1/) · **industrial polish tip** [`ind48pass1`](evidence/runs/ind48pass1/). Not BLS / not mainnet / not EVM-only. |
| Self-check | `.\scripts\verify_global_rd_audit.ps1` (FullLaunch/Live) · `.\scripts\verify_pre_soak.ps1` · `.\scripts\start_pre48h_maxload_2h.ps1` (2h STRICT max-load pre-48h) · `.\scripts\start_mempool_validation_soak.ps1` (mempool+validation STRICT; operator-ordered) · `.\scripts\verify_adr0021_wire_satoshi.ps1` (wire fee/amount satoshi cutover) · `.\scripts\verify_persist_fail_closed.ps1` (hot persist PersistError) · `.\scripts\verify_native_f64_hygiene.ps1` (amount/writeback typed refuse) · `.\scripts\verify_industrial_high_honesty.ps1` (HIGH #18/#19–20/#22/#24) · `.\scripts\verify_wave_e.ps1` · `.\scripts\verify_wave_f.ps1` · `.\scripts\verify_wave_g.ps1` · `.\scripts\verify_wave_h.ps1` · `.\scripts\verify_wave_i.ps1` · `.\scripts\verify_wave_j.ps1` · `.\scripts\verify_wave_k.ps1` · `.\scripts\verify_wave_l.ps1` · `.\scripts\verify_wave_m.ps1` · `.\scripts\verify_wave_n.ps1` · `.\scripts\verify_wave_o.ps1` · `.\scripts\verify_wave_p.ps1` · `.\scripts\verify_wave_q.ps1` · `.\scripts\verify_wave_r.ps1` · `.\scripts\verify_evm_depth_lab.ps1` · `.\scripts\verify_long_range_lab.ps1` · `.\scripts\verify_council_lab.ps1` · `.\scripts\verify_hard_all.ps1` · `python scripts/verify_experimental_rd.py` |
| Web UI | **Ops Console** `/` (`web/console/`) · legacy explorer `/explorer` · Grafana `deploy/grafana/dashboard.json` |
| Open UI | `.\scripts\open_ops_console.ps1` (solo + **one** main tab `/`) · `-AllTabs` for multi-tab tour · reopen `.\scripts\open_ops_console.ps1 -OpenOnly` |

## Pipeline (columns)

| 1 libp2p 48h | 2a LR solo 2h | 2b LR mesh 2h | 2c LR lab 48h | 2d LR STRICT | 3 EVM mesh | 3b EVM STRICT | 4 Mempool Rust |
|:------------:|:-------------:|:-------------:|:-------------:|:------------:|:----------:|:-------------:|:--------------:|
| **PASS** [`3c801b87`](evidence/runs/3c801b87/) | **PASS** [`lr2h9f3a`](evidence/runs/lr2h9f3a/) | **PASS** [`lr2hmesh`](evidence/runs/lr2hmesh/) | **PASS** [`lr48pass1`](evidence/runs/lr48pass1/) | **PASS** [`lrstrict1`](evidence/runs/lrstrict1/) | **PASS** [`evm48pass1`](evidence/runs/evm48pass1/) | **PASS** [`evmstrict1`](evidence/runs/evmstrict1/) | **PASS** [`mempool48pass1`](evidence/runs/mempool48pass1/) + audit [`adr0021gaudit1`](evidence/runs/adr0021gaudit1/) |

Full map: [ARCHITECTURE § R&D execution chain](ARCHITECTURE.md#rd-execution-chain) · [EXECUTION_ORDER](EXECUTION_ORDER.md).

## Proven vs not (honest)

| Proven (lab / Experimental mesh) | Not claimed |
|--------------|-------------|
| rust-libp2p swarm A–DB + **libp2p 48h PASS** (`3c801b87`) | Long-Range **production** / firm audit PDF |
| Experimental 48h TCP+TLS (`0a7932c4`) + libp2p (`3c801b87`) | Public mainnet / Hybrid pin relabel |
| Advertised unique cap 20; circuit out of crate book | Public IPFS DHT / Noise = mTLS |
| AutoNAT/UPnP confirm admit-canonical-or-omit | Tip proof / public mainnet |
| Identify observed confirm charges canonical key | Firm audit PDF |
| Add/remove/expire match canonical charge key | NTFS replace = POSIX inode-atomic |
| Long-Range WS lab + mesh 2h [`lr2hmesh`](evidence/runs/lr2hmesh/) + **lab 48h** [`lr48pass1`](evidence/runs/lr48pass1/) + **STRICT 48h** [`lrstrict1`](evidence/runs/lrstrict1/) | Long-Range **prod arm** / BLS / `feature_long_range` on `778888` |
| Phase 3 post-EVM-prep mesh 48h [`evm48pass1`](evidence/runs/evm48pass1/) + `evm_pre_48h_harness.py` | Full geth parity / EIP-4844 / **EVM-only** 48h claim |
| EVM STRICT 48h Phase 3b **PASS** [`evmstrict1`](evidence/runs/evmstrict1/) (IntervalSec=60, fail=0 mesh_warn=0, tip ~85200→~96089) | EVM-only 48h / geth / EIP-4844 / BLS / mainnet |
| EVM depth lab (waves 8–11 + RPC honesty; `GET /evm/status`) | Oracles/sharding on prod mesh 778888 |
| Oracle quorum + shard 2/3 labs (`oracle_lab`, `cross_shard_lab`; prod flags off) | Council 48h soak / on-chain signed gov / mainnet treasury |
| Gruver87 council ADR 0022 (Profile C `:19080`, 87 genesis mint) | Merging Dependabot major bumps |
| Fail-closed identity/persist ACL labs (Windows) | |

## Where R&D lives

| Path | Role |
|------|------|
| `native/abs_native/src/libp2p_swarm.rs` | ADR 0019 swarm (feature `libp2p`) |
| `scripts/libp2p_rust_*_lab.py` | Slice labs |
| `scripts/verify_adr0019_libp2p_hard.py` | Hard gate |
| `scripts/evm_pre_48h_harness.py` | Phase 3 pre-soak (labs+gate+probe+smoke; no soak start) |
| `scripts/verify_evm_depth_lab.ps1` | EVM depth operator pack ([`evmlab1`](evidence/runs/evmlab1/); host default, `-WithMesh` optional) |
| `docs/adr/0019-rust-libp2p-industrial.md` | Slice ledger |
| `docs/sprouts/` | Profile F / Long-Range / EVM matrix |
| `docs/sprouts/GOVERNANCE_COUNCIL_PROFILE.md` | Profile C council NFT (778889) |

## Next click

- **Funds / investors / ПВТ** → [DILIGENCE_BRIEF.md](DILIGENCE_BRIEF.md) (15 min) · [FUND_READINESS.md](FUND_READINESS.md)
- **Next click** → [EXECUTION_ORDER.md](EXECUTION_ORDER.md) — Phases 1–5 closed; next Phase 6 org · **safe code polish order:** [AUDIT_90D_FIX_PLAN.md](AUDIT_90D_FIX_PLAN.md)
- Hybrid pin (do not break): [`dup-protocol`](https://github.com/Gruver87/dup-protocol)
- Contribute: [CONTRIBUTING](../CONTRIBUTING.md)
- GitHub About: [REPO_PROFILE](../.github/REPO_PROFILE.md)
