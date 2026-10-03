# FAQ — DUP Protocol / DUP Labs (investor-safe)

**Audience:** grant officers, HTP / ПВТ, technical advisors.  
**Canonical:** English · RU summary: [ONE_PAGER_RU.md](ONE_PAGER_RU.md)  
**Source of truth for claims:** [DILIGENCE_BRIEF.md](DILIGENCE_BRIEF.md) · [SHOWCASE.md](SHOWCASE.md)

---

### What is DUP Protocol?

An **industrial hybrid L1** (Python orchestration + Rust/PyO3 hot path) with a fail-closed private prod-profile mesh and evidence-backed 48h soaks. Org face: **DUP Labs**. Author: **Uladzimir Dabranski (D.U.P.)**.

### Why two GitHub repositories?

| Repo | Role |
|------|------|
| [`dup-protocol`](https://github.com/Gruver87/dup-protocol) | Audit-freeze **industrial pin** (TCP+TLS). Tag `v1.3.1339-tip-v2-industrial`. |
| [`dup-protocol-experimental`](https://github.com/Gruver87/dup-protocol-experimental) | R&D sandbox (libp2p, Long-Range lab, EVM depth, mempool Rust). Phases 1–5 closed with packs. |

Do not conflate pin tip-v2 evidence with Experimental soaks.

### Is this a public mainnet / listed token?

**No.** Ready for technical diligence on a private mesh / R&D L1. Not public audited mainnet. Not a listed token sale.

### Has an external security firm finished an audit?

**No.** Phase 6 / firm engagement is **prep** (checklists, outreach drafts, pack `phase6prep1`). Not firm PASS.

### What does “soak PASS” mean here?

Only a packaged run under `docs/evidence/runs/<id>/` with report `passed=true` and `hard_fails=0` (STRICT packs also require `mesh_warn=0` / documented bar). Live demo ≠ soak.

### What transport do I see in a demo?

- **Experimental demo** ([DEMO_RUNBOOK.md](DEMO_RUNBOOK.md)): default Exp mesh JSON uses **libp2p** (ADR 0020).  
- **Pin demo** (pin `DEMO_RUNBOOK_PIN.md`): **TCP+TLS**.  
TCP+TLS 48h packs also exist on Experimental (`0a7932c4`) — do not relabel as libp2p.

### How is money represented?

**Satoshi integers only.** Float-only amounts are refused on the wire. See diligence brief + industrial tip pack [`ind48pass1`](evidence/runs/ind48pass1/).

### Is Long-Range production-ready?

**No.** ADR 0017 work is **lab-only**. Prod JSON keeps `feature_long_range=false`. Lab STRICT pack: [`lrstrict1`](evidence/runs/lrstrict1/).

### Is the bridge on?

**No** on prod mesh. Bridge stays OFF until audited L1 cutover ([MAINNET_GAP_ANALYSIS.md](MAINNET_GAP_ANALYSIS.md)).

### Is the NFT marketplace ERC-721 / OpenSea?

**No.** App-profile sprout; prod `feature_nft=false`. Soft escrow is not an L1 escrow contract. See [NFT_LAB_PROFILE.md](sprouts/NFT_LAB_PROFILE.md).

### What about AI agents / AI validator?

Lab sprouts only. Prod `feature_ai_agents=false` / `feature_ai_validator=false`. Not consensus-wired. See [AI_LAB_PROFILE.md](sprouts/AI_LAB_PROFILE.md).

### Former name “Absolute Blockchain”?

Same trees / evidence. Current brand: **DUP Labs / DUP Protocol**. Old Desktop folder names may still say `Absolute_*` — path only, not the GitHub name.

### Belarus trademark / patent?

**Prep pack only** for НЦИС trademark filing: [TRADEMARK_FILING_PREP_BY.md](TRADEMARK_FILING_PREP_BY.md). Not a registration certificate. Not a utility patent grant. Copyright + MIT attribution: [IP_AND_ATTRIBUTION.md](IP_AND_ATTRIBUTION.md).

### Who do we contact?

GitHub [Gruver87](https://github.com/Gruver87) · [`SECURITY.md`](../SECURITY.md). Company email / ПВТ legal entity fields in [FIRM_NDA_OUTLINE.md](FIRM_NDA_OUTLINE.md) are **placeholders** until the operator fills them — we do not invent contacts in-repo.

### Where do I start for a show?

[SHOWCASE.md](SHOWCASE.md).
