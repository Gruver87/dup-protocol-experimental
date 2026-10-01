# Firm kickoff checklist (Phase 6) — human / org

**Product:** DUP Protocol · **Org:** DUP Labs  
**Purpose:** close the two remaining **human** external-audit tracker items.  
**This file is not an audit report and not a PASS.**

Automated prep: `.\scripts\verify_audit_engagement_prep.ps1` (must stay green).  
Tracker: `python scripts/external_audit_tracker.py --list` → expect **6/8** until firm evidence lands.

---

## Before first firm call

- [ ] Confirm firm scope = **industrial pin** [`dup-protocol`](https://github.com/Gruver87/dup-protocol) tag `v1.3.1339-tip-v2-industrial` (not Experimental as “audited”)
- [ ] Paste current SHAs into the engagement letter:
  - Pin: `git -C <pin-repo> rev-list -n 1 v1.3.1339-tip-v2-industrial`
  - Experimental (optional R&D appendix): `git rev-parse HEAD` in this repo
- [ ] Attach / link evidence pack IDs from [`EXTERNAL_AUDIT_ENGAGEMENT.md`](EXTERNAL_AUDIT_ENGAGEMENT.md)
- [ ] NDA drafted / signed
- [ ] Disclosure channel agreed ([`SECURITY.md`](../SECURITY.md) + private advisory)
- [ ] Secrets rotation plan cited ([`SECRET_ROTATION.md`](SECRET_ROTATION.md)) — no `.env` in prod
- [ ] Ceremony dry-run status noted ([`CEREMONY_DRY_RUN.md`](CEREMONY_DRY_RUN.md)); live ceremony still gated

## During engagement

- [ ] Schedule **penetration test** (tracker label: `External penetration test scheduled`)
- [ ] Schedule / execute **third-party L1 (+ EVM subset) review** (tracker: `Third-party smart-contract / L1 security audit completed`)
- [ ] Firm gets read-only mesh access **or** sealed compose + audit zip (`.\scripts\export_audit_pack.ps1` on pin)
- [ ] Findings triage by severity: money / tip / P2P / honesty / DX

## After firm delivers evidence

Only then mark tracker items (real note + https URL — no TBD/placeholder):

```powershell
python scripts/external_audit_tracker.py --set "External penetration test scheduled" `
  --note "<vendor> scheduled <ISO-date>" --evidence-url "https://..."
python scripts/external_audit_tracker.py --set "Third-party smart-contract / L1 security audit completed" `
  --note "<vendor> report <id>" --evidence-url "https://..."
python scripts/external_audit_tracker.py --list
```

Place PDF under agreed path (pin preferred): `audits/<firm>/report.pdf`.

Re-verify honesty:

```powershell
.\scripts\verify_audit_engagement_prep.ps1
```

If human items are marked with real evidence, the “must stay pending” assert in prep will change — update the prep script / units only when evidence is real.

## Forbidden claims until both human items have evidence

- “Audited” / “mainnet-ready” / listed ABS  
- Closing MAINNET_GAP external-audit checkboxes as done without PDF  
- Painting Experimental soak packs as pin audit PASS  

---

**Related:** [`EXTERNAL_AUDIT_ENGAGEMENT.md`](EXTERNAL_AUDIT_ENGAGEMENT.md) · [`AUDITS.md`](AUDITS.md) · pack [`evidence/runs/phase6prep1/`](evidence/runs/phase6prep1/)
