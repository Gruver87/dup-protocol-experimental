# AI / MEV lab profile (ADR 0016 sprouts)

**Status:** experimental / analysis / dev-test — **not** industrial L1 core.  
**Prod mesh:** `feature_ai_agents=false`, `feature_ai_validator=false`, `feature_mev=false`.

## What this is

| Module | Role | Consensus-wired? |
|--------|------|------------------|
| `features/ai_manager.py` | Agent registry + optional `ModelPort` | **No** |
| `features/ai_ports.py` | Fail-closed model binding | **No** |
| `features/ai_validator.py` | Heuristic validator sim | **No** |
| `features/mev_analyzer.py` | Mempool fee heuristics | **No** |
| `scripts/ai_ops_anomaly.py` | Off-node ready/status triage | **No** |

## Operator checks

```powershell
python scripts/ai_lab.py
python scripts/ai_ops_anomaly.py --offline-only
pytest tests/unit/test_ai_sprout_harden.py tests/unit/test_wave43_ai_agents.py tests/unit/test_exp_ai_nft_marketplace_wave.py -q
```

## Honesty (2026-10-03)

- HTTP `/ai/*` `enabled` only when `feature_ai_validator` and not prod-blocked
- Forge path does **not** call `ai_validator.update_performance`
- `/status` exposes `ai_agents_loaded` (loaded ≠ enabled)
- `ai_ops.HONESTY` + `simulation_only` triage
- SDK: `get_ai_validators` / `get_ai_proposer` (read-only)

## Forbidden

- Flipping AI/MEV flags on prod `778888` mesh JSON
- Binding AI output into tip-safety / proposer forge
- Claiming soak / mainnet / firm PASS from these labs
