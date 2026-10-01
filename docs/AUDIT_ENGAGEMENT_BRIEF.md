# Audit engagement brief — DUP Protocol (firm one-pager)

**Org:** DUP Labs · **Product:** DUP Protocol  
**Author:** Uladzimir Dabranski (D.U.P.)  
**Primary audit pin:** https://github.com/Gruver87/dup-protocol  
**Pin tag:** `v1.3.1339-tip-v2-industrial`  
**Pin commit:** `git rev-list -n 1 v1.3.1339-tip-v2-industrial`  
**R&D sandbox (optional appendix):** https://github.com/Gruver87/dup-protocol-experimental  
**Date (prep refresh):** 2026-10-01  
**Owner:** Gruver87

**Honesty:** This brief is for **firm kickoff**. It is **not** an audit report and **not** a soak claim. Prefer the **pin** for scope; Experimental packs are R&D evidence — label them as such.

Formerly: Absolute Blockchain Ultimate Hybrid (historical alias in sealed packs).

---

## What we are asking you to review

Prod-profile chain **`778888`** (3-node Docker mesh, tip encoding v2 `b_satoshi`, RocksDB, native crypto required, bridge **OFF**).

Full scope: [AUDIT_SCOPE.md](AUDIT_SCOPE.md) · threat model: [THREAT_MODEL.md](THREAT_MODEL.md) · status: [AUDITS.md](AUDITS.md) · letter: [EXTERNAL_AUDIT_ENGAGEMENT.md](EXTERNAL_AUDIT_ENGAGEMENT.md) · human checklist: [FIRM_KICKOFF_CHECKLIST.md](FIRM_KICKOFF_CHECKLIST.md).

### In scope (summary)

1. Consensus tip path (import, tip-safety enforce, Path A catch-up, fork reconcile)  
2. State / money (satoshi storage + tip v2 apply / fees / gas / reward; ABS ledger persist dual-write)  
3. P2P mesh honesty (pin: TCP+TLS; Experimental default: libp2p Noise — label transport per tree)  
4. API / RPC (JWT admin, API keys, mempool-only contract deploy in prod)  
5. RocksDB prod path + DR rehearsal scripts  
6. `abs_native` hot-path crypto (`ABS_REQUIRE_NATIVE_CRYPTO`)  
7. Ops gates + packaged evidence under `docs/evidence/runs/`

### Explicitly out of scope

| Item | Why |
|------|-----|
| Bridge ON / L1 lock-mint | Disabled until separate cutover |
| Sharding / L2 / ZK / PQ / Lightning / Plasma / WASM / AI forge | R&D; FEATURE_* off on prod |
| Full Ethereum client compatibility | EVM subset only |
| Tip proof / Long-Range on prod JSON | Not claimed (`feature_long_range=false`) |
| Public mainnet ops / listing / legal | Organizational |
| `finality_quorum_live=true` marketing | Quorum not live-proven |

---

## Evidence pack (start here)

| Artifact | Path / note |
|----------|-------------|
| Industrial freeze | pin tag `v1.3.1339-tip-v2-industrial` |
| Tip-v2 **48h soak PASS** (Hybrid/pin tree) | `docs/evidence/runs/375d14f/` (or pin equivalent) |
| Phase 4 binder READY | `docs/evidence/runs/phase4-691329c/` |
| Experimental R&D packs (optional, label R&D) | `ind48pass1`, `lp2pstrict1`, `evmstrict1`, `mempool48pass1`, `lrstrict1` |
| Phase 6 prep refresh | [`evidence/runs/phase6prep1/`](evidence/runs/phase6prep1/) |
| Ledger | [EVIDENCE_MATRIX.md](EVIDENCE_MATRIX.md) |

---

## Reproduce locally (Windows) — **pin** preferred

```powershell
git clone https://github.com/Gruver87/dup-protocol.git
cd dup-protocol
git fetch --tags
git checkout v1.3.1339-tip-v2-industrial
pip install -r requirements.txt
.\scripts\build_native.ps1   # if wheel missing
python scripts/industrial_gate.py --min-soak-hours 48
python scripts/prod_gate.py
python scripts/bridge_off_audit_gate.py
.\scripts\export_audit_pack.ps1
```

Optional live mesh: `.\scripts\docker_prod_3node.ps1 -KeepVolumes` then `.\scripts\probe_prod_mesh.ps1 -Quick`.

Experimental appendix (not a substitute for pin scope):

```powershell
git clone https://github.com/Gruver87/dup-protocol-experimental.git
cd dup-protocol-experimental
.\scripts\verify_audit_engagement_prep.ps1
```

---

## Deliverables we need from you

1. Written report with severity ratings  
2. Reproduction notes against **the pin tag**  
3. Explicit statement that tip-v2 + satoshi apply path were in the reviewed build  
4. PDF under agreed path → `audits/<firm>/report.pdf` (pin repo preferred)

---

## What we will **not** claim until your report lands

- “Audited” / “mainnet-ready” / listed ABS  
- Closing tracker items *External penetration test* and *Third-party L1/SC audit*  
- Public testnet DNS/TLS go-live as security proof  

Tracker (Experimental tree): `python scripts/external_audit_tracker.py --list` — **6/8** automated; **2** firm-owned open.

---

## Contact

GitHub: [@Gruver87](https://github.com/Gruver87) · Security: [SECURITY.md](../SECURITY.md)
