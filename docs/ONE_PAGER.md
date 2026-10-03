# DUP Protocol — one-pager (EN)

**DUP Labs** · **DUP Protocol** · Uladzimir Dabranski (D.U.P.)  
**Date:** 2026-10-03 · Full path: [SHOWCASE.md](SHOWCASE.md) · RU: [ONE_PAGER_RU.md](ONE_PAGER_RU.md)

---

## One sentence

**DUP Protocol** is an industrial **hybrid L1** (Python + Rust) with a fail-closed private prod-profile mesh, satoshi-honest money, and evidence-backed 48h soaks — split into an **audit-freeze pin** and an **R&D sandbox**.

---

## Architecture (one line)

`API / RPC → Core + Mempool → Consensus / P2P / Sync → Storage / Rocks → abs_native (Rust)`

Pin transport: **TCP+TLS**. Experimental mesh default: **libp2p** (ADR 0020). Money: **satoshi integers**.

---

## Two repos

| | Pin | Experimental |
|---|-----|----------------|
| GitHub | [`dup-protocol`](https://github.com/Gruver87/dup-protocol) | [`dup-protocol-experimental`](https://github.com/Gruver87/dup-protocol-experimental) |
| Role | Audit freeze `v1.3.1339-tip-v2-industrial` | libp2p / LR lab / EVM depth / mempool Rust |
| Show | Tip-v2 soak [`375d14f`](https://github.com/Gruver87/dup-protocol/tree/master/docs/evidence/runs/375d14f) | STRICT packs below |

---

## Evidence scoreboard (Experimental STRICT — cite packs)

| Pack | Proves |
|------|--------|
| [`lp2pstrict1`](evidence/runs/lp2pstrict1/) | libp2p industrial STRICT 48h |
| [`mempool48pass1`](evidence/runs/mempool48pass1/) | Mempool+validation STRICT 48h |
| [`lrstrict1`](evidence/runs/lrstrict1/) | Long-Range **lab** STRICT 48h |
| [`evmstrict1`](evidence/runs/evmstrict1/) | EVM mesh STRICT 48h |
| [`ind48pass1`](evidence/runs/ind48pass1/) | Industrial polish tip 48h |

Every claim: pack README + `passed=true` + `hard_fails=0`. Detail: [DILIGENCE_BRIEF.md](DILIGENCE_BRIEF.md).

---

## Ask

Technical diligence / grant / ПВТ review of the **private mesh + on-disk evidence** — not a token listing, not “mainnet ready.”

Live demo: [DEMO_RUNBOOK.md](DEMO_RUNBOOK.md). FAQ: [FAQ.md](FAQ.md).

---

## Forbidden

Public audited mainnet · soak without pack id · prod Long-Range · bridge ON · ERC-721 parity · inventing company email / TM registration.
