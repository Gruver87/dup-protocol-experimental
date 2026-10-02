# AI / MEV lab profile (ADR 0016 sprouts)

**Status:** experimental / analysis / dev-test — **not** industrial L1 core.  
**Mid-soak disk wave:** **CLOSED** 2026-10-03 (`6fb5640`…`18be475`) — HTTP gates + forge unhook + FeatureFlags; **not** soak PASS.  
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

- HTTP `/ai/*` and `/ai/register-validator` `enabled` only when `feature_ai_validator` ∧ loaded ∧ ¬prod_block
- HTTP `/ai-agent/*` gated the same way on `feature_ai_agents` (loaded ≠ enabled)
- `FeatureFlags.ai_validator` surfaced on `/features`
- Forge path does **not** call `ai_validator.update_performance`
- `/status` exposes `ai_agents_*` / `ai_validator_*` via sprout gate
- `ai_ops.HONESTY` + `simulation_only` triage
- SDK: `get_ai_validators` / `get_ai_proposer` / `get_ai_agent_stats` / `get_ai_mev_scan` (read-only)
- `main.py` `getattr(..., feature_ai_*, False)` fail-closed defaults

## Forbidden

- Flipping AI/MEV flags on prod `778888` mesh JSON
- Binding AI output into tip-safety / proposer forge
- Claiming soak / mainnet / firm PASS from these labs
