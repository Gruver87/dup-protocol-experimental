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
python -m pytest tests/unit/test_nft_marketplace_harden.py tests/unit/test_nft_uow.py tests/unit/test_nft_ports.py tests/unit/test_exp_ai_nft_marketplace_wave.py -q
# optional staging:
docker compose -p abs-staging-app -f docker-compose.staging.app.yml up -d --build
```

## Honesty (2026-10-03)

- Settlement raises inside `atomic()` (no partial commit on royalty fail)
- Paid paths require store `atomic()` (`nft_uow_required`)
- Offer expiry enforced; auction finalize refuses before `ends_at`
- `offers_escrow` / `auction_escrow` = false (balance re-check only)
- `get_stats().enabled` follows balance backend
- Port: mint/list/buy/offer/auction/delist + Null fail-closed
- HTTP mutations (offer/bid/auction/accept/cancel/delist/finalize) require actor signature unless JWT admin

## Forbidden

- `feature_nft=true` on prod `778888` JSON
- Claiming ERC-721 / OpenSea parity / mainnet marketplace
- Wiring NFT settlement into tip-safety / forge
- Claiming soak / firm PASS from this lab
