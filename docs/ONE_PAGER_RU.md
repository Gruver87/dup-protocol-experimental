# DUP Protocol — краткая карточка (RU) · Experimental (R&D)

**Организация:** DUP Labs · **Продукт:** DUP Protocol · **Автор:** Уладзимир Дабранский (D.U.P.)  
**Дата:** 2026-10-24 · Полный вход (EN): [SHOWCASE.md](SHOWCASE.md) · EN one-pager: [ONE_PAGER.md](ONE_PAGER.md)  
**Это дерево:** R&D sandbox. **Для ПВТ / ИП / резидентства** канон — pin-пакет:  
[PVT_HTP_SHOW_PACK_RU.md (pin)](https://github.com/Gruver87/dup-protocol/blob/master/docs/PVT_HTP_SHOW_PACK_RU.md) · [ONE_PAGER_RU (pin)](https://github.com/Gruver87/dup-protocol/blob/master/docs/ONE_PAGER_RU.md)  
**Канонический язык репозитория:** English. Этот файл — краткое резюме **Experimental**, не замена pin.

---

## Одной фразой

**DUP Protocol** — промышленный гибридный L1 (Python + Rust) с fail-closed частной prod-profile mesh-сетью, деньгами только в satoshi и доказанными 48h soak-пакетами. Два репозитория: **industrial pin** (заморозка аудита) и **Experimental** (R&D).

---

## Два репозитория

| | Pin | Experimental |
|---|-----|----------------|
| GitHub | [dup-protocol](https://github.com/Gruver87/dup-protocol) | [dup-protocol-experimental](https://github.com/Gruver87/dup-protocol-experimental) |
| Роль | Аудит-заморозка, TCP+TLS, тег `v1.3.1339-tip-v2-industrial` | libp2p, Long-Range lab, EVM depth |
| Не путать | Tip-v2 soak pin | STRICT packs Experimental |

---

## Что доказано (примеры STRICT на Experimental)

- libp2p STRICT: `lp2pstrict1`  
- Mempool STRICT: `mempool48pass1`  
- Long-Range **lab** STRICT: `lrstrict1`  
- EVM STRICT: `evmstrict1`  
- Industrial tip: `ind48pass1`  

Каждый PASS только с пакетом на диске (`passed=true`, `hard_fails=0`). Подробности: [DILIGENCE_BRIEF.md](DILIGENCE_BRIEF.md).

---

## Что мы **не** заявляем

- Публичный audited mainnet / листинг токена  
- Готовый внешний security-audit PDF (Phase 6 — prep)  
- Prod Long-Range / включённый bridge  
- Зарегистрированный товарный знак НЦИС (есть только [prep](TRADEMARK_FILING_PREP_BY.md))  
- Юрлицо / email ПВТ в репозитории (поля-заглушки в NDA)

---

## IP / Беларусь

Авторское право + MIT: [IP_AND_ATTRIBUTION.md](IP_AND_ATTRIBUTION.md).  
Подготовка заявки на ТЗ в РБ (НЦИС): [TRADEMARK_FILING_PREP_BY.md](TRADEMARK_FILING_PREP_BY.md) — **не** свидетельство о регистрации.

---

## Просьба (ask)

Для **ПВТ / оценки ИП**: сначала pin [PVT_HTP_SHOW_PACK_RU](https://github.com/Gruver87/dup-protocol/blob/master/docs/PVT_HTP_SHOW_PACK_RU.md).  
Experimental показывают как **ёмкость R&D** (STRICT packs ниже), не как industrial pin PASS.

Демо Exp: [DEMO_RUNBOOK.md](DEMO_RUNBOOK.md). FAQ (EN): [FAQ.md](FAQ.md). Контакт: GitHub [Gruver87](https://github.com/Gruver87).
