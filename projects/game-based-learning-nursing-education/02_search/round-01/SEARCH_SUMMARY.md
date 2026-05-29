# Search Summary — Round 01

**Project:** Game-based Teaching Strategies in Nursing Education (RCTs)
**Run date:** 2026-05-29
**Query structure:** (Game-based teaching) AND (Nursing) AND (RCT design filter)

## Records retrieved

| Database | Records |
| --- | --- |
| PubMed/MEDLINE | 205 |
| Scopus | 292 |
| Europe PMC | 143 |
| **Merged** | 640 |
| **Deduplicated (unique)** | **315** |

→ `03_screening/round-01/screening.csv` (315 rows, ready for title/abstract screening)

## Databases NOT retrieved this round

| Database | Status | Reason |
| --- | --- | --- |
| Embase | HTTP 403 Forbidden | Elsevier key works for Scopus but has no Embase entitlement |
| Cochrane CENTRAL | HTTP 401 Unauthorized | OAuth token invalid/expired |
| CINAHL | no connector | **important for nursing** — needs EBSCOhost access (manual export) |
| ERIC | no connector | manual export needed |
| PsycINFO | no connector | APA PsycNET access needed |
| Airiti / CEPS (華藝, Chinese) | no connector | manual export needed for Chinese literature |

**Note:** Europe PMC indexes MEDLINE + PMC + preprints and partially overlaps Embase
content. For a complete protocol-compliant nursing review, **CINAHL and the Chinese
database (華藝) should be added by manual export** and merged into a round-02.

## Toolchain fixes applied (Windows cp950 bug)
- `multi_db_dedupe.py`, `search_audit.py`, `search_report.py` — added `encoding="utf-8"`
  to all `read_text`/`write_text` calls (they crashed on non-ASCII bib content under cp950).
