# DUP Protocol thin operator SDK (experimental v0.1)

**Package:** `sdk/dup_sdk` · **Version:** 0.1.2  
**Audience:** operators / diligence / scripts on **dup-protocol-experimental**  
**Not:** public audited mainnet · industrial pin official SDK · wallet custody · full geth

## Install / path

From repo root (no PyPI publish in v0):

```powershell
$env:PYTHONPATH = "$PWD;$env:PYTHONPATH"
python -c "from sdk.dup_sdk import Client, HONESTY; print(HONESTY)"
```

## Quick start

```python
from sdk.dup_sdk import Client

# TLS verify always on. Auth optional for public GETs; required for many POSTs / eth_* on prod mesh.
c = Client(
    "http://127.0.0.1:18180",
    api_key=None,           # X-API-Key (RPC_API_KEYS)
    bearer_token=None,      # Authorization: Bearer <admin JWT or RPC key>
)
print(c.health_live())
print(c.status_probe())
print(c.get_balance_satoshi("0x..."))
print(c.get_block_number())  # may 401 without bearer/api_key on jwt_enforce mesh
```

### Auth from env (preferred)

```powershell
$env:DUP_SDK_BASE_URL = "http://127.0.0.1:18180"
$env:DUP_SDK_API_KEY = "<rpc-key>"          # or RPC_API_KEYS
$env:DUP_SDK_BEARER = "<admin-jwt-or-key>"  # or DUP_SDK_JWT / ABS_ADMIN_JWT
# Mint admin JWT (needs JWT_SECRET): python scripts/mint_admin_jwt.py
python -c "from sdk.dup_sdk import Client; c=Client.from_env(); print(c.auth_configured(), c.get_block_number())"
```

Never hardcode secrets in source. Placeholder strings (`changeme`, `secret`, …) are refused.

## Money honesty

- Prefer `*_satoshi` integers (1 ABS = 1_000_000 satoshi).
- Non-integral float without satoshi twin → `MoneyRefuse`.
- `verify_tls=False` → refused at construct time.

## Submit

```python
# raw RLP / eth path
c.submit_signed_tx(raw_tx_hex="0x...")

# signed JSON body (must carry satoshi or whole ABS)
c.submit_signed_tx({
    "from": "0x...",
    "to": "0x...",
    "amount_satoshi": 1_000_000,
    "fee_satoshi": 10_000,
    "nonce": 0,
    "signature": "...",
    "public_key": "...",
})
```

## NFT marketplace (read-only)

App-profile sprout — **not** prod `feature_nft` on 778888.

```python
print(c.get_nft_stats())
print(c.get_nft_token("abs_genesis_crown"))
print(c.get_nft_listings())
```

Lab: `python scripts/nft_lab.py` · profile: `docs/sprouts/NFT_LAB_PROFILE.md`

Offline self-check always runs. Live mesh is optional — **not** a soak claim.  
If `DUP_SDK_BEARER` / `RPC_API_KEYS` are set, lab retries `eth_blockNumber` with auth.

## Related

- Node HTTP: `api/http.py`
- JWT mint: `scripts/mint_admin_jwt.py`
- AUDIT money cascade: `docs/AUDIT_90D_FIX_PLAN.md` Phase G
- Pin (do not confuse): https://github.com/Gruver87/dup-protocol
