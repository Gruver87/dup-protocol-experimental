# Showcase pack — DUP Protocol (funds / ПВТ / demo)

**Org:** DUP Labs · **Product:** DUP Protocol · **Author:** Uladzimir Dabranski (D.U.P.)  
**Primary tree:** [`dup-protocol-experimental`](https://github.com/Gruver87/dup-protocol-experimental) (this repo)  
**Industrial pin:** [`dup-protocol`](https://github.com/Gruver87/dup-protocol) · tag [`v1.3.1339-tip-v2-industrial`](https://github.com/Gruver87/dup-protocol/releases/tag/v1.3.1339-tip-v2-industrial)  
**Language:** English canonical · RU one-pager: [ONE_PAGER_RU.md](ONE_PAGER_RU.md)  
**Not:** public audited mainnet · not a finished pitch PDF · not a soak PASS without pack id.

This is the **single front door** for grant officers, HTP / ПВТ reviewers, and technical diligence.

---

## 60 seconds

| | |
|---|---|
| One sentence | [ELEVATOR_PITCH.md](ELEVATOR_PITCH.md) · [ONE_PAGER.md](ONE_PAGER.md) |
| What / what not | [FAQ.md](FAQ.md) · [AT_A_GLANCE.md](AT_A_GLANCE.md) |
| Brand / IP | [BRAND.md](BRAND.md) · [IP_AND_ATTRIBUTION.md](IP_AND_ATTRIBUTION.md) · Belarus TM prep [TRADEMARK_FILING_PREP_BY.md](TRADEMARK_FILING_PREP_BY.md) |

---

## 15 minutes (diligence)

1. [DILIGENCE_BRIEF.md](DILIGENCE_BRIEF.md) — claims + STRICT scoreboard  
2. [FUND_READINESS.md](FUND_READINESS.md) — fund card  
3. [EVIDENCE_MATRIX.md](EVIDENCE_MATRIX.md) — proof ledger  
4. [MAINNET_GAP_ANALYSIS.md](MAINNET_GAP_ANALYSIS.md) — honest gaps  
5. Pick **one** STRICT pack README (e.g. [`evmstrict1`](evidence/runs/evmstrict1/)) — `passed=true`, `hard_fails=0`

Deck outline (not slides): [INVESTOR_DECK_SKELETON.md](INVESTOR_DECK_SKELETON.md).

---

## Live demo (operator machine)

| Mesh | Doc | Transport |
|------|-----|-----------|
| **Experimental** (default show) | [DEMO_RUNBOOK.md](DEMO_RUNBOOK.md) | libp2p Noise/Yamux (ADR 0020) on Exp prod JSON |
| **Industrial pin** | [Pin SHOWCASE](https://github.com/Gruver87/dup-protocol/blob/master/docs/SHOWCASE.md) → `DEMO_RUNBOOK_PIN.md` | **TCP+TLS** (pin freeze) |

Do **not** present Exp libp2p demo as the pin transport. Do **not** claim a soak from a live demo session.

## Verify both repos (key surfaces)

```powershell
# From Experimental root — pin + Exp in one scoreboard
.\scripts\verify_dup_suite.ps1 -Mode Quick      # daily
.\scripts\verify_dup_suite.ps1 -Mode Standard  # recommended
.\scripts\verify_dup_suite.ps1 -Mode Full
.\scripts\verify_dup_suite.ps1 -Mode Max       # needs live mesh :18180-18182
```

Detail: [VERIFY_SUITE.md](VERIFY_SUITE.md). Does **not** start 48h soak.

---

## Security story (transport honesty)

| Tree | Default P2P | Threat doc |
|------|-------------|------------|
| Industrial pin | TCP+TLS / mTLS | Pin [THREAT_MODEL](https://github.com/Gruver87/dup-protocol/blob/master/docs/THREAT_MODEL.md) |
| Experimental | libp2p (ADR 0020) on mesh JSON; TCP+TLS packs also exist | This repo [THREAT_MODEL.md](THREAT_MODEL.md) (header notes both) |

Firm engagement path (pin): [AUDIT_ENGAGEMENT_BRIEF](https://github.com/Gruver87/dup-protocol/blob/master/docs/AUDIT_ENGAGEMENT_BRIEF.md).

---

## IP / Belarus / firm prep

| Topic | Doc |
|-------|------|
| Copyright + MIT attribution | [IP_AND_ATTRIBUTION.md](IP_AND_ATTRIBUTION.md) · [`NOTICE`](../NOTICE) |
| Belarus trademark **prep** (НЦИС — not filed) | [TRADEMARK_FILING_PREP_BY.md](TRADEMARK_FILING_PREP_BY.md) |
| NDA outline (blanks) | [FIRM_NDA_OUTLINE.md](FIRM_NDA_OUTLINE.md) |
| Firm outreach draft | [FIRM_OUTREACH_LETTER.md](FIRM_OUTREACH_LETTER.md) |
| Kickoff checklist | [FIRM_KICKOFF_CHECKLIST.md](FIRM_KICKOFF_CHECKLIST.md) |

---

## Forbidden claims (show room)

- “Mainnet ready” / listed token / public audited mainnet  
- “Soak passed” without pack id + `hard_fails=0` on disk  
- “Ethereum-compatible / Yellow Paper EVM” without Absolute honesty  
- Old GitHub names as current repos (`Absolute_Blockchain_*`, `Gruver87/experimental`)  
- Prod Long-Range / bridge ON / ERC-721 marketplace parity  

---

## Contact

**Uladzimir Dabranski (D.U.P.)** · GitHub [Gruver87](https://github.com/Gruver87) · Security: [`SECURITY.md`](../SECURITY.md)  
Legal entity / ПВТ resident company email: **not filled in-repo** (placeholders in NDA until operator completes).
