# DUP Protocol Ops Console

Same-origin industrial UI for Experimental nodes (DUP Labs).

## URLs

| Path | What |
|------|------|
| `/` or `/console` | Ops console (default) |
| `/console/assets/*` | CSP-bound JS/CSS |
| `/explorer` | Legacy feature explorer |

## Panels

| View | Live sources |
|------|----------------|
| Overview | `/status?probe=1`, sparklines, feature badges |
| Mesh & Sync | `/sync/status`, `/p2p/topology`, `/p2p/security`, `/p2p/peer-score`, `POST /p2p/reconnect` |
| Live Metrics | `GET /metrics` |
| Mempool | `/mempool`, store demote honesty |
| Chain | `/blocks` |
| EVM | `/evm/status`, `/evm/supported-opcodes` |
| Features | `/features`, `/native/crypto`, `/chain/genesis/ceremony` |
| Evidence | Sealed pack index (honesty only — not live soak) |
| Wallets | EIP-1193 + watchlist |
| Council | ADR 0022 watch (staging `778889`) |
| Markets | `/market/snapshot`, `/market/fx` |
| Security | CSP / non-goals |

## Security

- `Content-Security-Policy`: `default-src 'self'` (no CDN, no inline scripts)
- Path resolve via realpath allowlist under `web/console` + `web/explorer` only
- No private-key forms that POST to the node
- EIP-1193 connect + `wallet_switchEthereumChain` / `wallet_addEthereumChain` + `eth_sendTransaction`
- Session watchlist is sessionStorage only; theme in localStorage
- CORS still allow-list only
- Council panel is **watch-only** (staging `778889`); no genesis mint from console

## Wallets

1. Set REST base (http_port) and JSON-RPC (rpc_port, auto-derived from `/status`).
2. Connect injected wallet → **Switch to DUP** (uses node `chain_id`).
3. Send ABS via wallet-signed `eth_sendTransaction` (wei, 18 decimals).

## Markets

`GET /market/snapshot` and `GET /market/fx` are **ops orientation only** (not consensus / not L1 oracle).

- Exchange clocks: NYSE, LSE, Xetra, MOEX, **BCSE (Minsk)**, TSE, HKEX, SSE, ASX, crypto venues
- Crypto: CoinGecko simple price
- FX: Frankfurter USD+EUR crosses + **BYN** (Yahoo) + converter presets EUR→BYN / USD→BYN
- Macro: Yahoo chart basket (gold/silver/oil/gas/copper, indices, mega-caps)

Server-side allowlist + TLS verify; browser CSP stays `connect-src 'self'`.

## Launcher

```powershell
.\scripts\open_ops_console.ps1          # solo + ONE main tab /
.\scripts\open_ops_console.ps1 -OpenOnly
.\scripts\open_ops_console.ps1 -AllTabs # multi-tab tour
```

Auto-refresh cycles **15s → 60s → 5m → Paused** (soft strip update; full remount only on manual Refresh / nav).

## Honesty panels

Console surfaces `mempool_store` demote, `under_mesh`, pack-fallback metrics when present on `/status` / `/metrics`. `/health/ready` also carries informational `mempool_store` + `rocks_native_pack_fallbacks` (does **not** gate ready).

Evidence panel names sealed packs (`evmstrict1`, `lp2pstrict1`, …) — **does not** claim live PASS.

## Operator check

```powershell
python -m pytest -q tests/unit/test_web_console_static.py tests/unit/test_console_wallets_council.py --tb=line
# with a node up:
# open http://127.0.0.1:<http_port>/
```

Not soak evidence. Not mainnet.
