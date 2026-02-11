---
name: ma-manuscript-quarto
description: Draft and render a meta-analysis manuscript with Quarto using an IMRaD structure and embedded figures/tables. Use when preparing the final paper from analysis outputs.
---

# Ma Manuscript Quarto

## Overview

Create a Quarto manuscript with standard IMRaD sections and render to PDF and HTML.

## Inputs

- `06_analysis/figures/`
- `06_analysis/tables/`
- `02_search/round-01/dedupe.bib` or final bibliography

## Outputs

- `07_manuscript/00_abstract.qmd`
- `07_manuscript/01_introduction.qmd`
- `07_manuscript/02_methods.qmd`
- `07_manuscript/03_results.qmd`
- `07_manuscript/04_discussion.qmd`
- `07_manuscript/index.qmd`
- `07_manuscript/references.bib`
- `07_manuscript/manuscript.pdf`
- `07_manuscript/manuscript.html`
- `07_manuscript/prisma_flow.md`
- `07_manuscript/prisma_flow.svg`
- `07_manuscript/evidence_map.md`
- `07_manuscript/result_claims.csv`
- `07_manuscript/result_paragraphs.md`
- `07_manuscript/result_paragraphs.qmd`
- `07_manuscript/result_summary_table.md` (auto-inserted into Results)
- `07_manuscript/traceability_table.md`
- `07_manuscript/study_characteristics.md`
- `07_manuscript/study_characteristics.csv`
- `07_manuscript/submission_checklist.md`
- `07_manuscript/03_results.qmd` (assembled)
- `09_qa/results_consistency_report.md`

## Workflow

1. Initialize a Quarto project in `07_manuscript/`.
2. Copy Quarto templates from `assets/quarto/` and adapt to the project.
3. Embed figures and tables with captions and cross-references.
4. Include PRISMA-style reporting elements and a flow diagram when applicable.
5. Generate the PRISMA flow summary with `scripts/prisma_flow.py` via `uv run`, optionally writing an SVG. Use `--strict` for final renders.
6. Insert the search report and audit hashes into Methods with `scripts/insert_search_report.py`.
7. Build a manuscript evidence map with `scripts/build_evidence_map.py` and review key results before writing.
8. Initialize `result_claims.csv` with `scripts/init_result_claims.py` and draft Results from it.
9. Generate Results paragraph stubs with `scripts/build_result_paragraphs.py`.
10. Build study characteristics table with `scripts/build_study_characteristics.py`.
11. Insert the traceability table into Methods with `scripts/insert_traceability_table.py`.
12. Assemble Results into `03_results.qmd` with `scripts/assemble_results.py` (also inserts `result_summary_table.md`).
13. Populate the bibliography and ensure citation keys match.
14. Generate a results consistency report with `scripts/results_consistency_report.py`.
15. Initialize the submission checklist with `scripts/init_submission_checklist.py`.
16. Render to PDF and HTML with `scripts/render_manuscript.py` (blocks if checklists incomplete).

## Discussion Guidance

- Interpret the main effect estimates and clinical or practical significance.
- Discuss heterogeneity, sensitivity analyses, and publication bias.
- Compare findings to prior reviews and explain divergences.
- State limitations, generalizability, and future research needs.

## Resources

- `assets/quarto/` provides an IMRaD Quarto scaffold.
- `scripts/prisma_flow.py` generates a PRISMA flow diagram summary and optional SVG.
- `scripts/insert_search_report.py` injects search report content into Methods.
- `scripts/build_evidence_map.py` creates a checklist of outputs to base writing on.
- `scripts/init_result_claims.py` seeds a results-to-evidence table for drafting.
- `scripts/build_result_paragraphs.py` creates paragraph stubs and a summary table for Results writing.
- `scripts/build_study_characteristics.py` generates the study characteristics table from extraction.
- `scripts/insert_traceability_table.py` inserts a protocol→search→screening→inclusion table into Methods.
- The traceability narrative is auto-inserted into `02_methods.qmd` near Study Selection.
- `scripts/assemble_results.py` injects result paragraphs into `03_results.qmd`.
- `scripts/results_consistency_report.py` checks claim/output/citation consistency.
- `scripts/init_submission_checklist.py` seeds a journal submission checklist.
- `scripts/render_manuscript.py` validates checklists before rendering.

## Validation

- Ensure all figures are 300 dpi and tables are reproducible.
- Cross-check that every result in the text appears in the analysis outputs.
- Review `07_manuscript/evidence_map.md` before drafting Results.
- Ensure each results paragraph maps to `07_manuscript/result_claims.csv`.
- Verify `07_manuscript/traceability_table.md` is inserted into `02_methods.qmd`.
- Ensure each claim includes effect estimate, confidence interval, and p-value.
- Ensure `03_results.qmd` contains all claim IDs and their figure/table refs.
- Ensure `09_qa/results_consistency_report.md` has no missing items.
- Ensure each claim includes `citation_keys` and the citations appear in Results.
  Note: `citation_keys` should be comma-separated BibTeX keys present in `07_manuscript/references.bib`.
- Note: set `RESULTS_MIN_WORDS` to control minimum words per claim paragraph (default 25).
- Ensure the study characteristics table is inserted into `03_results.qmd`.
- Ensure `submission_checklist.md` is tailored to the target journal.

## Pipeline Navigation

| Step | Skill               | Stage                       |
| ---- | ------------------- | --------------------------- |
| Prev | `/ma-meta-analysis` | 06 Statistical Analysis     |
| Next | `/ma-peer-review`   | 08 Peer Review & GRADE      |
| All  | `/ma-end-to-end`    | Full pipeline orchestration |
