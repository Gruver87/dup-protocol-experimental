# Evidence: `lrstrict1` — Long-Range lab STRICT 48h PASS

**Window:** 2026-09-26T21:23:29+02:00 → 2026-09-28T21:23:30+02:00  
**Script:** `.\scripts\start_soak_long_range_lab.ps1 -Hours 48 -Strict`  
**Host commit at start:** `edbfbcd9c14fb44c47f53eee40ea4abbd86dd965`

## Result

| Field | Value |
|-------|--------|
| `passed` | **true** |
| `strict` | **true** |
| `hard_fails` / `fail_lines` | **0** |
| `mesh_warn` / `warn_lines` / `ready_only` | **0** |
| `mesh_ok_cycles` | **2849** |
| `interval_sec` / `FullHarnessEvery` | **60** / **6** |
| tip | ~18646 → ~30096 |
| ports | 29080–29082 (`abs-lr-lab`) |

## Layers proven under STRICT

| Layer | What held |
|-------|-----------|
| Tip-safety / WS gate | Contiguous tip+1 + light ancestry advance; hard refuse below anchor |
| Long-Range roll-forward | Miner autonomous WS floor (`ABS_WS_ROLL_GAP=512`, confirm 16) |
| Gossip | tip-safe adopt (`ahead_of_tip` defer); equivocation refuse; committee verify |
| P2P mesh | under-mesh reconnect; WS push only when peer tip ≥ anchor; class rate-limit |
| Mining | mesh_min=2 + `wire_soft_fail` lab forge; reconnect ≥8s; wire-roots 3s cache |
| Health watch | HeavyProbe + FullHarnessEvery=6; fail=0 mesh_warn=0 |

## Honesty

- **Lab STRICT only** — not default [`lr48pass1`](../lr48pass1/) bar  
- **Not** BLS · **not** prod `778888` · **not** public mainnet · **not** Hybrid audit pin · **not** libp2p  
- Prod JSON stays `feature_long_range=false`  
- Staging also hard-off Long-Range  

Artifacts: `manifest.json`, `soak_result.txt`, `soak_report_*.json`, `soak_48h_*_strict.log` in this directory.
