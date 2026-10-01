# DUP Protocol thin operator SDK (experimental v0)

**Package:** `sdk/dup_sdk`  
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

c = Client("http://127.0.0.1:18180", api_key=None)  # TLS verify always on
print(c.health_live())
print(c.status_probe())
print(c.get_balance_satoshi("0x..."))
print(c.get_block_number())
```

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

## Lab

```powershell
python scripts/dup_sdk_lab.py
python scripts/dup_sdk_lab.py --base-url http://127.0.0.1:18180
```

Offline self-check always runs. Live mesh is optional — **not** a soak claim.

## Related

- Node HTTP: `api/http.py`
- AUDIT money cascade: `docs/AUDIT_90D_FIX_PLAN.md` Phase G
- Pin (do not confuse): https://github.com/Gruver87/dup-protocol
