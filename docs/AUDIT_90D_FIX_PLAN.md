# Audit → 90-day fix plan (safe order)

**Repo:** `dup-protocol-experimental`  
**Rule:** nothing that breaks tip-v2 / mempool wire satoshi / tip-safety / prod mesh JSON / evidence packs.  
**Soak:** new 48h soaks stay on the shelf unless a hot-path money/P2P/consensus change requires re-proof.  
**Source audits (2026-10-01):** deep scan consensus/storage + network/api/web/EVM (chat session).

---

## Safety ladder (always)

```text
1. Honesty / docs / labels          ← no consensus break
2. Quarantine / UI / refuse APIs    ← fail-closed, tests update
3. Additive satoshi ports           ← float display only at REST
4. Behavior harden under flags      ← require_native refuse, etc.
5. Breaking remap / revm            ← ONLY with migration ADR + lab
```

**Forbidden in this window:** Great Merge, bridge ON, prod Long-Range, silent opcode remap to Yellow Paper without ADR, rewrite Rocks/GHOST/native kernels.

---

## Phase A — Honesty first ✅ DONE (2026-10-01)

| Step | Action | Status |
|------|--------|--------|
| A1 | Disclose Absolute opcode map ≠ Yellow Paper | Done — matrix + `/evm/status` `opcode_map_honesty` |
| A2 | ZK range hash theater → `NotImplementedError` | Done |
| A3 | Units + industrial_gate needles | Done |

---

## Phase B — Trust UX ✅ DONE (2026-10-01)

| Step | Action | Status |
|------|--------|--------|
| B1 | Explorer: disable key-paste sign; DEMO badges PQ/ZK; console link | Done |
| B2 | Admin JWT mint requires `ABS_ALLOW_DEV_ADMIN_JWT=1` | Done |
| B3 | Banner uses `jwt_enforce_admin` honesty | Done |

---

## Phase C — Money surface ✅ DONE (2026-10-01)

| Step | Action | Status |
|------|--------|--------|
| C2 | Cross-shard migration: `balance_satoshi` wire; refuse float-only credit | Done |
| C3 | `InboundEnvelope.amount_satoshi` + mismatch refuse | Done |
| C4 | P2P `validator_register` requires `stake_satoshi` | Done |
| C1 | Broader StoragePort float display wrappers | Done (2026-10-01) — QueryFacade + REST/RPC prefer `get_balance_satoshi`; display ABS from sat |

---

## Phase D — Harden ✅ DONE (2026-10-01)

| Step | Action | Status |
|------|--------|--------|
| D1 | EVM native writeback: refuse Python fallback under `require_native` / prod | Done |
| D2 | `consensus_mode=auto` → unified; parallel lab-only; prod/staging coerce | Done |
| D3 | Legacy `network/p2p/*` + sync managers → `legacy_test_*` (+ shims) | Done — [LEGACY_NETWORK_QUARANTINE.md](LEGACY_NETWORK_QUARANTINE.md) |
| D4 | CREATE2 host salt honesty in matrix / `evm_runtime` | Done — partial Absolute honesty |
| D5 | `/health/ready`: `p2p is None` in prod → not ready | Done |
| D6 | `print()` → logging on consensus/sync hot paths | Done |

---

## Phase E — Org / show ✅ DONE (2026-10-01)

| Step | Action | Status |
|------|--------|--------|
| E1 | Demo runbook (3-node + console + STRICT pack) | Done — [DEMO_RUNBOOK.md](DEMO_RUNBOOK.md) |
| E2 | Ceremony dry-run pack | Done — [CEREMONY_DRY_RUN.md](CEREMONY_DRY_RUN.md) |
| E3 | Investor / ПВТ deck from DILIGENCE_BRIEF | Done — [INVESTOR_DECK_SKELETON.md](INVESTOR_DECK_SKELETON.md) |
| E4 | Optional one tip soak before meetings | Shelf — operator-ordered only |

---

## Phase F — Optional later

| Step | Action | Status |
|------|--------|--------|
| F1 | ADR: Absolute-VM forever **or** Yellow Paper + revm | Done decision — **Absolute-VM kept** ([ADR 0023](adr/0023-absolute-vm-opcode-map.md)); YP+revm remains future optional |
| F2 | Real ZK circuits or strip module from explorer entirely | Done strip — explorer ZK generate UI removed; honesty panel only |
| F3 | External firm audit engagement | Checklist shipped — [EXTERNAL_AUDIT_ENGAGEMENT.md](EXTERNAL_AUDIT_ENGAGEMENT.md); firm kickoff is org |

---

## Done definition per phase

- Unit tests green for touched surfaces  
- No prod mesh JSON flag flips  
- Docs honesty matches code  
- No claim of soak unless pack exists  

**Current focus:** Residual float writes on EVM/cross-shard/faucet prefer `apply_store_delta_satoshi` / `balance_delta_satoshi`. Remaining without soak: firm audit kickoff (org) · **E4 soak** (operator) · feature-sprout float fallbacks (NFT/plasma/lightning when satoshi method absent).

---

## Operator self-check (per phase)

```powershell
.\scripts\verify_audit_phase.ps1 -Phase A
.\scripts\verify_audit_phase.ps1 -Phase B
.\scripts\verify_audit_phase.ps1 -Phase C
.\scripts\verify_audit_phase.ps1 -Phase D
.\scripts\verify_audit_phase.ps1 -Phase E
.\scripts\verify_audit_phase.ps1 -Phase F
.\scripts\verify_audit_phase.ps1 -Phase All          # + industrial_gate
.\scripts\verify_audit_phase.ps1 -Phase E -MeshProbe # optional live probe (NOT soak)
```

`-SkipGate` skips `industrial_gate.py`. Unit/needle checks only — **not** a 48h soak claim.
