---
name: ma-fulltext-management
description: Collect and manage full-text PDFs for included studies, track provenance, and prepare documents for extraction. Use when moving from screening to data extraction.
---

# Ma Fulltext Management

## Overview

Gather full texts, validate completeness, and prepare a clean manifest.

## Inputs

- `03_screening/round-01/included.bib`

## Outputs

- `04_fulltext/manifest.csv`
- `04_fulltext/unpaywall_results.csv` (optional OA lookup)
- `04_fulltext/fulltext_decisions.csv` (Stage 04b — full-text eligibility screening)
- `04_fulltext/ft_agreement.md` (Stage 04b — full-text inter-rater agreement)
- `04_fulltext/README.md`
- `04_fulltext/` PDF files
- `04_fulltext/previews/` (optional PDF image previews)

## Workflow (Web-First Hybrid — Default)

⚠️ **Default approach**: Web-based extraction first, PDF retrieval only for gaps.

### Phase 1: Web-Based Data Gathering (Default — No PDFs Needed)

1. Create `04_fulltext/` and build `manifest.csv` with `record_id`, DOI, PMID, title, and access notes.
   - Read from `03_screening/round-01/included.bib`
   - Use `references/manifest-template.csv` as template
   - Write to `04_fulltext/manifest.csv` (columns: record_id, DOI, PMID, title, access_method, confidence_score)
2. **Automatically run web extraction** for all included studies using Claude Code's `WebSearch` and `WebFetch` tools:
   - Query PubMed structured abstracts (`https://pubmed.ncbi.nlm.nih.gov/<pmid>/`)
   - Query ClinicalTrials.gov registries (`https://clinicaltrials.gov/study/<nct_id>`)
   - Search Europe PMC, journal supplementary materials
3. Record confidence scores per field (see `references/web-extraction.md` for scoring).
   - Update `04_fulltext/manifest.csv` (confidence_score column)
4. Flag studies with confidence < 0.7 for primary outcome fields → these need PDFs.
   - Mark in `04_fulltext/manifest.csv` (needs_pdf = TRUE)

### Phase 2: Targeted PDF Retrieval (Only for Low-Confidence Studies)

5. For flagged studies only (~20-30%), query Unpaywall for OA links using `scripts/unpaywall_fetch.py` via `uv run`.
   - Use `scripts/unpaywall_fetch.py`
   - Read from `04_fulltext/manifest.csv` (needs_pdf = TRUE rows)
   - Write to `04_fulltext/unpaywall_results.csv`
6. Download available PDFs with `scripts/download_oa_pdfs.py`.
   - Use `scripts/download_oa_pdfs.py`
   - Write to `04_fulltext/<record_id>.pdf`
7. Optionally render PDF previews with `scripts/render_pdf_previews.py` for visual QA.
   - Use `scripts/render_pdf_previews.py`
   - Write to `04_fulltext/previews/<record_id>_page1.png`
8. Request user to manually deposit any remaining PDFs that cannot be auto-retrieved.
   - Update `04_fulltext/manifest.csv` (access_method = "manual")
9. Run OCR only when needed and preserve original files.

### Why Web-First?

- **Speed**: 50-70% faster than PDF-only (2-3h vs 8-12h)
- **No institutional access required** for Phase 1
- **90-95% completeness** with hybrid approach
- PDFs are only needed for ~20-30% of studies

## Resources

- `references/manifest-template.csv` provides a manifest header.
- `scripts/unpaywall_fetch.py` queries Unpaywall for open-access links.
- `scripts/analyze_unpaywall.py` analyzes Unpaywall results and generates summary statistics.
- `scripts/download_oa_pdfs.py` downloads open-access PDFs automatically from Unpaywall URLs.
- `scripts/render_pdf_previews.py` renders PDF pages to PNG previews.
  Note: Unpaywall requires `UNPAYWALL_EMAIL` in `.env`.
  Note: PDF previews require `pdftoppm` or `mutool` installed.

## Stage 04b: Full-Text Eligibility Screening (PRISMA Item 16)

⚠️ **MANDATORY** — PRISMA 2020 requires reporting the number of full-text articles excluded with reasons.

After completing full-text retrieval (Phases 1-2 above), re-screen all included studies against
the full text to confirm eligibility. This step catches issues not visible at the abstract stage
(e.g., wrong population subgroup, insufficient sample size, protocol-only publications).

### Workflow

1. Run AI full-text screening (Reviewer 1):
   ```bash
   uv run tooling/python/ai_screen.py --project <project-name> --stage fulltext --reviewer 1
   ```

2. Run AI full-text screening (Reviewer 2) for dual review:
   ```bash
   uv run tooling/python/ai_screen.py --project <project-name> --stage fulltext --reviewer 2
   ```

3. Compute full-text inter-rater agreement (Cohen's kappa):
   ```bash
   uv run ma-screening-quality/scripts/dual_review_agreement.py \
     --file projects/<project-name>/04_fulltext/fulltext_decisions.csv \
     --col-a FT_Reviewer1_Decision --col-b FT_Reviewer2_Decision \
     --out projects/<project-name>/04_fulltext/ft_agreement.md
   ```

4. Resolve conflicts (if any) — update `FT_Final_Decision` and `FT_Exclusion_Code` columns.

5. Only studies with `FT_Final_Decision = include` proceed to Stage 05 (data extraction).

### Output Schema (`fulltext_decisions.csv`)

| Column | Description |
|--------|-------------|
| `record_id` | Matches manifest.csv and screening decisions |
| `title` | Study title |
| `doi` | Digital Object Identifier |
| `pmid` | PubMed ID |
| `FT_Reviewer1_Decision` | include / exclude |
| `FT_Reviewer1_Reason` | Reason with exclusion code reference |
| `FT_Reviewer2_Decision` | include / exclude |
| `FT_Reviewer2_Reason` | Reason with exclusion code reference |
| `FT_Final_Decision` | include / exclude (resolved) |
| `FT_Exclusion_Code` | Exclusion code (P1, S2, etc.) or NONE |

### Exclusion Codes

Reuses standard codes from `ma-screening-quality/references/screening-labels.md`:
P1/P2 (population), I1/I2 (intervention), C1 (comparator), S1-S4 (study design),
O1/O2 (outcomes), T1/T2 (time), L1 (language), D1 (duplicate).

### QA Thresholds

- Full-text kappa ≥ 0.60 (same threshold as abstract screening)
- All exclusions must have a documented reason and code
- `FT_Exclusion_Code` feeds directly into PRISMA flow diagram item 16

## Validation

- Ensure every included record has a matching full-text file or a documented reason for absence.
- Ensure `record_id` continuity with screening decisions.
- Ensure `fulltext_decisions.csv` exists before proceeding to Stage 05.
- Ensure all `FT_Final_Decision` values are resolved (no blanks) before extraction.

## Pipeline Navigation

| Step | Skill                   | Stage                                |
| ---- | ----------------------- | ------------------------------------ |
| Prev | `/ma-screening-quality` | 03 Screening & Quality               |
| 04b  | (this skill)            | Full-text eligibility screening      |
| Next | `/ma-data-extraction`   | 05 Data Extraction                   |
| All  | `/ma-end-to-end`        | Full pipeline orchestration          |
