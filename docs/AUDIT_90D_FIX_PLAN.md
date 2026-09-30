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

## Phase B — Trust UX ✅ in progress / landed this wave

| Step | Action | Status |
|------|--------|--------|
| B1 | Explorer: disable key-paste sign; DEMO badges PQ/ZK; console link | Done |
| B2 | Admin JWT mint requires `ABS_ALLOW_DEV_ADMIN_JWT=1` | Done |
| B3 | Banner uses `jwt_enforce_admin` honesty | Done |

**Next:** Phase C (satoshi ports) — surgical, additive.

---

## Phase C — Money surface (structural, surgical)

| Step | Action | Break risk |
|------|--------|------------|
| C1 | Additive `*_satoshi` on `StoragePort` / adapters; keep float getters as display wrappers | Medium — needs broad unit pass |
| C2 | Quarantine `cross_shard_coordinator` float debit (refuse if sharding armed) | Low (flag OFF) |
| C3 | Bridge envelope satoshi types while `bridge_enabled=false` | Low |
| C4 | Validator stake register: satoshi-only on non-prod path too | Low–medium |

Mesh probe after C1–C4; soak only if operator orders.

---

## Phase D — Harden (still no feature unlock)

| Step | Action |
|------|--------|
| D1 | EVM native writeback: refuse Python fallback under `require_native` / prod |
| D2 | Deprecate parallel Casper/Beacon construction (unified only) |
| D3 | Rename legacy `network/p2p/` + `network/sync/fast_sync` → `legacy_test_*` |
| D4 | CREATE2 host salt honesty in matrix (EIP-1014 claim downgrade or fix) |
| D5 | `/health/ready`: if `p2p is None` in prod → not ready |
| D6 | Kill `print()` on consensus/sync hot paths |

---

## Phase E — Org / show (parallel, non-code)

| Step | Action |
|------|--------|
| E1 | Demo runbook (3-node + console + STRICT pack) |
| E2 | Ceremony dry-run pack |
| E3 | Investor / ПВТ deck from DILIGENCE_BRIEF |
| E4 | Optional one tip soak before meetings |

---

## Phase F — Optional later (breaking / big)

| Step | Action |
|------|--------|
| F1 | ADR: Absolute-VM forever **or** Yellow Paper + revm migration |
| F2 | Real ZK circuits or strip module from explorer entirely |
| F3 | External firm audit engagement |

---

## Done definition per phase

- Unit tests green for touched surfaces  
- No prod mesh JSON flag flips  
- Docs honesty matches code  
- No claim of soak unless pack exists  

**Current focus:** Phase A → then B.
