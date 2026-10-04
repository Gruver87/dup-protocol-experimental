# Evidence packages (Wave B)

Versioned, hashed mesh/ops artifacts. **Not** a substitute for external audit.

## How to package

```bash
python scripts/package_mesh_evidence.py \
  --out docs/evidence/runs/<commit-or-date> \
  --probe-log logs/probe_prod_mesh.txt \
  --soak-report logs/soak_report_48h.json
```

`manifest.json` binds `commit` + `sha256` of each file. Missing inputs are recorded as `status=missing` (honest).

## What belongs here

| Artifact | Proves |
|----------|--------|
| Probe log with `/health/ready` PASS ×3 | Mesh ready (Wave A) |
| Soak report `passed=true` | Long-run stability |
| Image digest / compose project id | Reproducible mesh image |

## Notable packs

| Path | Claim |
|------|--------|
| [`runs/lp2pstrict1/`](runs/lp2pstrict1/) | **libp2p STRICT 48h PASS** · host `c458ff57` · IntervalSec=60 · `hard_fails=0` `mesh_warn=0` — distinct from default `ind48pass1` / `3c801b87` |
| [`runs/3c801b87/`](runs/3c801b87/) | **libp2p 48h PASS** (ADR 0020 Experimental mesh) · host `00b1bf86` — B1 closed |
| [`runs/lrstrict1/`](runs/lrstrict1/) | **Long-Range lab STRICT 48h PASS** · host `edbfbcd9` · IntervalSec=60 · `hard_fails=0` `mesh_warn=0` — distinct from default `lr48pass1` |
| [`runs/lr48pass1/`](runs/lr48pass1/) | **Long-Range lab 48h PASS** (ADR 0017 default bar) · git `18c85dbb` — B2 closed; not BLS / not prod |
| [`runs/lr2hintensify/`](runs/lr2hintensify/) | Long-Range lab intensify 2h PASS (preflight before `lr48pass1`) |
| [`runs/lr48fail1/`](runs/lr48fail1/) | Long-Range lab 48h FAIL (historical; superseded by `lr48pass1`) |
| [`runs/lr2hmesh/`](runs/lr2hmesh/) | **Long-Range lab 3-node mesh 2h PASS** (ADR 0017) |
| [`runs/lr2h9f3a/`](runs/lr2h9f3a/) | Long-Range lab solo 2h PASS (prior / superseded for mesh claims) |
| [`runs/evmstrict1/`](runs/evmstrict1/) | **EVM STRICT 48h PASS** · host `0c369045` · IntervalSec=60 · `hard_fails=0` `mesh_warn=0` — distinct from default `evm48pass1` |
| [`runs/evm48pass1/`](runs/evm48pass1/) | **Phase 3 post-EVM-prep mesh 48h PASS** · host `8b0657cc` — not EVM-only / not mainnet |
| [`runs/mempool48pass1/`](runs/mempool48pass1/) | **Mempool+validation STRICT 48h PASS** · host `42b56ee` · `hard_fails=0` `mesh_warn=0` · sidecar refuse_fail=0 — ADR 0021 |
| [`runs/ind48pass1/`](runs/ind48pass1/) | **Industrial polish tip 48h PASS** · git `719deb4` (ADR 0021 wire on mesh) |
| [`runs/adr0021gaudit1/`](runs/adr0021gaudit1/) | ADR 0021 global R&D audit **13/13** (not a soak) |
| [`runs/0a7932c4/`](runs/0a7932c4/) | TCP+TLS 48h PASS (do not relabel as libp2p) |
| [`runs/35104db0/`](runs/35104db0/), [`runs/87f51b3e/`](runs/87f51b3e/) | libp2p 48h FAIL (historical) |

## Honesty

Funds / ПВТ scorecard: [DILIGENCE_BRIEF.md](../DILIGENCE_BRIEF.md).  
Historical Jul 2026 soak/failover claims in [EVIDENCE_MATRIX.md](../EVIDENCE_MATRIX.md) remain **operator-local** until a package for that SHA is committed or released as a GitHub Actions artifact.
