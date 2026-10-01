# Audits — honest status (Experimental)

**External third-party L1 / smart-contract / penetration audit: not completed.**

**This repository is not the audit pin.** External third-party L1 audit is tracked on
[Ultimate Hybrid](https://github.com/Gruver87/dup-protocol)
tag [`v1.3.1339-tip-v2-industrial`](https://github.com/Gruver87/dup-protocol/releases/tag/v1.3.1339-tip-v2-industrial).

This sandbox ships rust-libp2p / Long-Range / EVM-depth labs. Lab PASS ≠ firm audit PDF.

| Scope | Status | Notes |
|-------|--------|-------|
| ADR 0019 hard gate (`verify_adr0019_libp2p_hard.py`) | Active | Operator-local labs — **not** an external audit |
| Experimental R&D CI (`experimental-rd.yml`) | Active | Profile F + rust-libp2p labs |
| Security workflow (`security-audit.yml`) | Active | pip-audit + cargo-audit (scoped ignores) |
| Independent external audit report | **Pending — pin** | Do not claim “audited” from this repo · kickoff: [FIRM_KICKOFF_CHECKLIST.md](FIRM_KICKOFF_CHECKLIST.md) · prep [`phase6prep1`](evidence/runs/phase6prep1/) |
| Bug bounty | **Not configured** | Disclose via [SECURITY.md](../SECURITY.md) |
| Parallel R&D after libp2p 48h PASS | **Phases 1–5 closed** | B1 [`3c801b87`](evidence/runs/3c801b87/) · B2 [`lr48pass1`](evidence/runs/lr48pass1/) + STRICT [`lrstrict1`](evidence/runs/lrstrict1/) · Phase 3 [`evm48pass1`](evidence/runs/evm48pass1/) + STRICT [`evmstrict1`](evidence/runs/evmstrict1/) · Phase 4 [`adr0021gaudit1`](evidence/runs/adr0021gaudit1/) + [`mempool48pass1`](evidence/runs/mempool48pass1/) · tip [`ind48pass1`](evidence/runs/ind48pass1/) · libp2p STRICT [`lp2pstrict1`](evidence/runs/lp2pstrict1/); next = Phase 6 org |

**Operator note (2026-09-28):** B1/B2/Phase 2d STRICT/Phase 3–5 **PASS** on disk. Prod JSON keeps
`feature_long_range=false` / `feature_oracles=false` / `feature_sharding=false` on `778888` (+ staging LR hard-off).
Not BLS · not EVM-only 48h · not public mainnet.

Related: [SECURITY.md](../SECURITY.md) · [EXPERIMENTAL_SANDBOX.md](../EXPERIMENTAL_SANDBOX.md) · [EXECUTION_ORDER.md](EXECUTION_ORDER.md) · Hybrid [AUDITS.md](https://github.com/Gruver87/dup-protocol/blob/master/docs/AUDITS.md)
