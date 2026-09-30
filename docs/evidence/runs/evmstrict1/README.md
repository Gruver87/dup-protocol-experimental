# Evidence: `evmstrict1` — EVM STRICT 48h PASS (post-EVM prep mesh)

**Window:** 2026-09-28T22:55:26+02:00 → 2026-09-30T22:55:27+02:00  
**Script:** `.\scripts\start_soak_evm_mesh_48h_strict.ps1`  
**Host commit at start:** `0c369045af492a8010e89b03998e9de843e3edf6`  
**Image:** `sha256:0861666a4b2ec59bb0a3edb11b47eb004908b97385140922f48f3d46b4eaaaf3`

## Result

| Field | Value |
|-------|--------|
| `passed` | **true** |
| `strict` | **true** |
| `hard_fails` / `fail_lines` | **0** |
| `mesh_warn` / `warn_lines` / `ready_only` | **0** |
| `mesh_ok_cycles` | **2801** |
| `interval_sec` / `FullHarnessEvery` | **60** / **6** |
| `TipStagnantFailAfterSec` | **3600** |
| tip | ~85200 → ~96089 |
| ports | 18180–18182 (Experimental prod `778888`) |

## Layers proven under STRICT

| Layer | What held |
|-------|-----------|
| EVM prep path | `evm_pre_48h_harness` + `prepare_48h_soak` before start |
| Prod mesh / libp2p | ADR 0020 Noise; peers=2 aligned; tip growth |
| Tip stagnation | TipStagnant=3600 armed; tip advanced full window |
| Health watch | FullHarnessEvery=6; fail=0 mesh_warn=0 warn_lines=0 |
| Soft residuals | No under_mesh / ready_flap WARN lines scored |

## Honesty

- **STRICT mesh after EVM prep** — distinct from default [`evm48pass1`](../evm48pass1/)  
- **Not** EVM-only 48h · **not** full geth · **not** EIP-4844  
- **Not** Long-Range · **not** BLS · **not** public mainnet · **not** Hybrid audit pin  
- Prod JSON stays `feature_long_range=false`

Artifacts: `manifest.json`, `soak_result.txt`, `soak_report_48h_evm_strict.json`, `soak_48h_evm_strict.log` in this directory.
