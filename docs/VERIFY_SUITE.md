# Verify suite — pin + Experimental (operator)

**Brand:** DUP Labs · DUP Protocol  
**Goal:** one entry to exercise the **key working surfaces** of both repos.  
**Not:** 48h soak start · Docker rebuild (unless `-RebuildLibp2p`) · public mainnet claim.

---

## Canonical dual-repo command (from Experimental root)

```powershell
cd C:\Users\vovun\Desktop\Absolute_Blockchain_Experimental

# Daily / after a disk wave (~minutes)
.\scripts\verify_dup_suite.ps1 -Mode Quick

# Recommended full offline+RD check
.\scripts\verify_dup_suite.ps1 -Mode Standard

# Pin industrial evidence bar + Exp RD + libp2p hard
.\scripts\verify_dup_suite.ps1 -Mode Full

# Everything including live mesh hard (ports 18180–18182 must be up)
.\scripts\verify_dup_suite.ps1 -Mode Max
```

Custom pin path:

```powershell
.\scripts\verify_dup_suite.ps1 -Mode Standard -PinRoot "C:\Users\vovun\Desktop\Absolute_Blockchain_Ultimate_Hybrid"
```

Report: `data/verify_dup_suite.json`  
Legacy alias: `.\scripts\verify_absolute_unified.ps1` → same suite.

---

## What each mode runs

| Mode | Pin (`verify_project`) | Exp gate | Midsoak pytest | AI/NFT labs | Showcase docs | Exp RD | ADR 0019 hard | Mesh probe | `verify_full_blockchain --hard` |
|------|------------------------|----------|----------------|-------------|---------------|--------|---------------|------------|----------------------------------|
| Quick | quick | yes | yes | yes | yes | — | — | opt `-WithMeshProbe` | — |
| Standard | standard | yes | yes | yes | yes | yes | yes | opt | — |
| Full | industrial | yes | yes | yes | yes | yes | yes | opt | — |
| Max | industrial | yes | yes | yes | yes | yes | yes | yes | yes |

---

## Per-repo alone (if you only want one tree)

### Industrial pin (Hybrid / `dup-protocol`)

```powershell
cd C:\Users\vovun\Desktop\Absolute_Blockchain_Ultimate_Hybrid
.\scripts\verify_project.ps1 -Mode Quick
.\scripts\verify_project.ps1 -Mode Standard
.\scripts\verify_project.ps1 -Mode Industrial
.\scripts\verify_project.ps1 -Mode Max
```

Pin live TCP+TLS demo (not soak): [DEMO_RUNBOOK_PIN.md](DEMO_RUNBOOK_PIN.md)

### Experimental only

```powershell
cd C:\Users\vovun\Desktop\Absolute_Blockchain_Experimental

# Fail-closed deep check (needs live mesh for hard)
.\scripts\verify_hard_all.ps1

# Or flexible:
.\scripts\verify_full_blockchain.ps1 -Hard
.\scripts\verify_full_blockchain.ps1 -SkipLive

# Mid-soak honesty only (no docker recreate)
.\scripts\verify_midsoak_honesty.ps1 -All

# AUDIT 90D A–H
.\scripts\verify_audit_90d_all.ps1
```

---

## Honesty

- Green suite ≠ public audited mainnet  
- Green suite ≠ new 48h soak PASS (packs stay on disk under `docs/evidence/runs/`)  
- Exp libp2p PASS ≠ pin cutover (pin stays TCP+TLS)  
- During a running soak: prefer `-Mode Quick` / `Standard` / `Full`; use `Max` only if you accept a live probe against the existing mesh (no recreate)

---

## Showcase

Front door: [SHOWCASE.md](SHOWCASE.md)
