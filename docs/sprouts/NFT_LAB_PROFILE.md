# NFT marketplace lab profile (ADR 0016 Profile C / app-profile)

**Status:** sprout — **not** industrial L1 core on `778888`.  
**Mid-soak disk wave:** **CLOSED** 2026-10-03 (`6fb5640`…`18be475`) — soft escrow + HTTP sprout gate; **not** soak PASS.  
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
- Soft escrow: offer/bid debit `held_satoshi`; cancel/finalize refunds; **not** L1 escrow contract
- `offers_escrow` / `auction_escrow` = true when balance-bound (see `escrow_note`)
- HTTP GET `/nft/*` gated `feature_nft ∧ loaded ∧ ¬prod_block` (`_nft_sprout_enabled`)
- `get_stats().enabled` follows balance backend
- Port: mint/list/buy/offer/auction/cancel_auction/delist + Null fail-closed
- HTTP mutations (offer/bid/auction/accept/cancel/delist/finalize) require actor signature unless JWT admin

## Forbidden

- `feature_nft=true` on prod `778888` JSON
- Claiming ERC-721 / OpenSea parity / mainnet marketplace
- Wiring NFT settlement into tip-safety / forge
- Claiming soak / firm PASS from this lab
