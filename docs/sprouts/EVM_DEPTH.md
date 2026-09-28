# EVM depth (Profile A — industrial L1)

EVM is **core**, not a FEATURE_* sprout. It already runs on prod mesh through
the single `ChainApplyQueue` / mempool / state-root path.

## Rules (ADR 0016)

1. Grow opcodes / gas / CREATE2+salt **inside** existing apply only.
2. Do **not** enable MiniVM or WASM on the same tip as EVM.
3. Evidence: `scripts/prod_evm_smoke.py` + matching state-root across mesh RPC.
4. Prod requires `evm_create2_eip1014` + `evm_require_deploy_salt`.

## Evidence

- Mesh smoke: `python scripts/prod_evm_smoke.py` (mempool path on :18546–:18548)
- Pre-STRICT / pre-48h: `python scripts/evm_pre_48h_harness.py` (labs + gate + probe + smoke)
- STRICT starter (soak **only if ordered**): `.\scripts\start_soak_evm_mesh_48h_strict.ps1`
- Profile freeze: `tests/unit/test_sprout_profiles.py`
- Industrial gate requires CREATE2 + deploy salt on prod mesh JSON
- Honesty snapshot: `GET /evm/status` ↔ [EVM_COMPAT_MATRIX.md](EVM_COMPAT_MATRIX.md) (`supported_absolute` / `partial` / `not_claimed`)

## Compatibility gaps

Honest matrix (Shanghai/Cancun subset): [EVM_COMPAT_MATRIX.md](EVM_COMPAT_MATRIX.md).

## Explicit non-goals

- Full Ethereum client parity
- Parallel VM domains on `778888`
