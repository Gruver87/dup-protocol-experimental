# NFT marketplace lab profile (ADR 0016 Profile C / app-profile)

**Status:** sprout — **not** industrial L1 core on `778888`.  
**Prod mesh:** `feature_nft=false` (enforced by industrial_gate).

## What this is

| Surface | Role |
|---------|------|
| `features/nft.py` | Mint / list / buy / offer / auction + satoshi prices |
| Staging Profile C | chain `778889` / `:19080` (council + NFT) |
| `scripts/nft_lab.py` | Offline honesty lab |
| `sdk.dup_sdk.Client` | Read helpers: `get_nft_stats` / `get_nft_token` / listings |

## Operator

```powershell
python scripts/nft_lab.py
python -m pytest tests/unit/test_nft_marketplace_harden.py tests/unit/test_nft_uow.py -q
# optional staging:
docker compose -p abs-staging-app -f docker-compose.staging.app.yml up -d --build
```

## Forbidden

- `feature_nft=true` on prod `778888` JSON
- Claiming ERC-721 / OpenSea parity / mainnet marketplace
- Wiring NFT settlement into tip-safety / forge
