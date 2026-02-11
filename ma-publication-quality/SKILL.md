---
name: ma-publication-quality
description: Publication-quality checks and enhancements for high-impact journal submissions, including PRISMA/MOOSE reporting, robust meta-analysis diagnostics (Hartung-Knapp, prediction intervals, influence), GRADE Summary of Findings, claim audits, and cross-reference validation. Use when preparing the final manuscript and QA package.
---

# Ma Publication Quality

## Overview

Add high-impact-journal quality controls: reporting checklists, robustness diagnostics, GRADE SoF outputs, and manuscript consistency audits.

## Inputs

- `06_analysis/` outputs
- `07_manuscript/` Quarto files
- `08_reviews/grade_summary.csv`
- `02_search/round-01/search_report.md`
- `02_search/round-01/search_audit.json`

## Outputs

- `06_analysis/tables/hakn_summary.txt`
- `06_analysis/tables/prediction_intervals.csv`
- `06_analysis/figures/baujat_*.png`
- `06_analysis/figures/influence_*.png`
- `06_analysis/tables/grade_summary.html`
- `07_manuscript/prisma_checklist.md`
- `07_manuscript/moose_checklist.md` (if observational)
- `09_qa/claim_audit.md`
- `09_qa/crossref_report.md`
- `09_qa/reporting_checklist_audit.md`
- `09_qa/claim_table_check.md`

## Workflow

1. Initialize reporting checklists with `scripts/init_reporting_checklists.py`.
2. Copy R templates from `assets/r/` into `06_analysis/` and run after the primary model scripts.
3. Generate GRADE Summary of Findings table from `08_reviews/grade_summary.csv`.
4. Run claim audit on Abstract vs Results and save to `09_qa/claim_audit.md`.
5. Run reporting checklist completion audit and save to `09_qa/reporting_checklist_audit.md`.
6. Run claim-to-table check and save to `09_qa/claim_table_check.md`.
7. Run cross-reference check to ensure figures/tables are referenced in manuscript.
8. Update checklists and re-run `final_qa_report.py`.

## Resources

- `assets/r/` contains robust diagnostics and SoF scripts.
- `scripts/claim_audit.py` checks numeric claims in Abstract vs Results.
- `scripts/check_reporting_completion.py` checks PRISMA/MOOSE completion.
- `scripts/claim_table_check.py` checks Results numeric claims vs tables.
- `scripts/crossref_check.py` checks for unreferenced figures/tables.
- `scripts/init_reporting_checklists.py` copies PRISMA/MOOSE templates.
- `references/prisma2020-checklist-template.md`
- `references/moose-checklist-template.md`

## Validation

- Do not render final manuscript until PRISMA/MOOSE checklists are filled.
- Ensure all figures/tables are referenced in Results.

## Pipeline Navigation

| Step | Skill             | Stage                       |
| ---- | ----------------- | --------------------------- |
| Prev | `/ma-peer-review` | 08 Peer Review & GRADE      |
| Next | `/ma-end-to-end`  | Final QA & orchestration    |
| All  | `/ma-end-to-end`  | Full pipeline orchestration |
