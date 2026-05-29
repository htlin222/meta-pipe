# Game-based Teaching Strategies in Nursing Education — SR/MA

遊戲導向教學策略於護理教育之成效：系統性回顧與統合分析（RCT only）

**Status:** Round-01 automated pipeline complete. **Provisional / abstract-derived — requires
full-text extraction and dual human verification before submission.**

## Headline results
- **640** records (PubMed 205 · Scopus 292 · Europe PMC 143) → **315** after de-duplication.
- **88** studies provisionally included (61 RCTs confirmed from abstract; 27 pending full text).
- **5** studies with extractable data pooled (L2 knowledge/skill): **Hedges' g = 0.65
  (95% CI 0.24–1.05), p = 0.002, I² = 71%**; GRADE certainty Low–Very low.
- No eligible study reported NWKM Level-4 (patient/system) outcomes.

## Final report
- **[`GBL_Nursing_SRMA_Report.pdf`](GBL_Nursing_SRMA_Report.pdf)** — 10-page submittable PDF
  (same as `07_manuscript/manuscript.pdf`).

## Pipeline / folder map
| Stage | Folder | Key outputs |
|---|---|---|
| Protocol | `01_protocol/` | `eligibility.md`, `pico.yaml` |
| Search | `02_search/round-01/` | `queries.txt`, per-DB `.bib`, `dedupe.bib`, `SEARCH_SUMMARY.md`, `prisma_flow.py` |
| Screening | `03_screening/` | `screening-database.csv`, AI decisions, `round-01/chunks/` |
| Extraction | `05_data_extraction/` | `data_extraction.csv`, `dimension_counts.json`, `dimension_table.md/.py` |
| Meta-analysis | `06_meta_analysis/` | `meta_input.csv`, `meta_analysis.py`, `meta_results.json`, `forest_plot_L2.png` |
| Quality | `06_quality_assessment/` | `rob2.csv`, `rob2_traffic_light.png`, `grade_summary.md` |
| Figures | `figures/` | `prisma_flow.png`, `dimension_bars.png` |
| Manuscript | `07_manuscript/` | `manuscript.qmd` → `manuscript.pdf` |

## Reproduce
```bash
# search (PubMed+Scopus+EuropePMC)
cd tooling/python && uv run python ../../ma-search-bibliography/scripts/run_multi_db_search.py \
  --root ../../projects/game-based-learning-nursing-education --round round-01 \
  --email <you> --queries .../02_search/round-01/queries.txt \
  --skip-embase --skip-cochrane --skip-zotero
# analysis + figures
uv run --with matplotlib python .../06_meta_analysis/meta_analysis.py
uv run --with matplotlib python .../02_search/round-01/prisma_flow.py
uv run --with matplotlib python .../05_data_extraction/dimension_table.py
uv run --with matplotlib python .../06_quality_assessment/rob2_grade.py
# manuscript
cd .../07_manuscript && quarto render manuscript.qmd --to typst
```

## Known limitations (must address before submission)
1. Only 3/8 protocol databases searched — **CINAHL & Chinese (華藝) are missing** and central to nursing.
2. Screening / extraction / RoB 2 / GRADE were **single-reviewer (AI)**, not dual human.
3. Effect sizes extracted from **abstracts only** → just 5/88 poolable; 27 await RCT confirmation.
4. No publication-bias test (<10 pooled studies); L2 pooled knowledge + skill together.

_Generated with an automated Claude Code SR/MA pipeline._
