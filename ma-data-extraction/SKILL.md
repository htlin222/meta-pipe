---
name: ma-data-extraction
description: Define extraction schema, extract study data from full texts, and store it in a structured database for meta-analysis. Use when moving from full-text collection to statistical analysis.
---

# Ma Data Extraction

## Overview

Extract consistent data, capture provenance, and build a clean analysis dataset.

## Inputs

- `04_fulltext/manifest.csv`
- `01_protocol/outcomes.md`

## Outputs

- `05_extraction/extraction.sqlite`
- `05_extraction/extraction.csv`
- `05_extraction/llm_suggestions.jsonl` (optional)
- `05_extraction/data-dictionary.md`
- `05_extraction/extraction-log.md`
- `05_extraction/study_map.csv` (optional if `record_id` not in extraction CSV)
- `05_extraction/source.csv` (optional source references)
- `05_extraction/source_validation.md` (optional)

## Workflow

1. Define a data dictionary that covers outcomes, covariates, and study identifiers.
2. Initialize a normalized SQLite database using `scripts/init_extraction_db.py` via `uv run`.
3. Extract data with double-entry or verification where possible.
4. Optionally run `scripts/llm_extract.py` via `uv run` to generate extraction suggestions for manual review.
5. Record unit conversions and assumptions in `05_extraction/extraction-log.md`.
6. Export a tidy CSV for analysis and lock the database snapshot.
7. **Fallback – WebSearch gap-fill**: For any remaining missing or low-confidence fields, use Claude Code's `WebSearch` tool directly to look up each study (by DOI, PMID, or title+author) and populate the gaps. See details in **WebSearch Fallback** below.
8. (Recommended) Record source references in `05_extraction/source.csv` and validate with `scripts/validate_sources.py`.

## Resources

- `scripts/init_extraction_db.py` initializes a standard extraction schema.
- `scripts/llm_extract.py` provides LLM-assisted extraction suggestions.
- `scripts/validate_sources.py` validates extraction vs source references.
- `references/data-dictionary-template.md` provides a dictionary scaffold.
- `references/study-map-template.csv` maps `record_id` to `study_id` if needed.
- `references/source-template.csv` for source references.
  Note: `llm_extract.py` requires a PDF parser such as `pdfplumber` or `pypdf` (install via `uv add`).

## WebSearch Fallback

When extraction has missing or uncertain fields and PDFs are unavailable, Claude Code can fill gaps directly using its built-in `WebSearch` and `WebFetch` tools — no scripts or API keys required.

### When to Use

- Fields left NULL or marked low-confidence after PDF/LLM extraction
- No institutional PDF access for specific studies
- Need quick verification of a value already extracted

### Procedure

1. **Identify gaps**: Scan `extraction.csv` for NULL or empty cells in critical columns (e.g., `n_total`, `events_intervention`, `events_control`, `mean`, `sd`).
2. **Search per study**: For each study with gaps, run `WebSearch` with the query pattern:
   - `"<first_author> <year> <journal> <intervention> <outcome> results"` or
   - `"<DOI>"` or `"PMID:<pmid> abstract"`
3. **Fetch structured sources**: Use `WebFetch` on high-value URLs:
   - PubMed abstract: `https://pubmed.ncbi.nlm.nih.gov/<pmid>/`
   - ClinicalTrials.gov: `https://clinicaltrials.gov/study/<nct_id>`
   - Europe PMC: `https://europepmc.org/article/MED/<pmid>`
4. **Extract and fill**: Read the returned content, extract the missing values, and update `extraction.csv`.
5. **Tag provenance**: For every web-filled value, append `[web]` in the `notes` column (e.g., `n_total from PubMed abstract [web]`).
6. **Log in extraction-log.md**: Record which studies/fields were filled via web search, with source URLs.

### Confidence Rules

| Source                          | Confidence | Action                   |
| ------------------------------- | ---------- | ------------------------ |
| PubMed structured abstract      | 0.90       | Accept                   |
| ClinicalTrials.gov registry     | 0.85       | Accept                   |
| Journal webpage / press release | 0.70       | Accept with note         |
| Conference abstract only        | 0.60       | Flag for verification    |
| No source found                 | —          | Leave NULL, document gap |

### Limitations

- Cannot access paywalled full-text content via WebFetch
- Event counts by subgroup are rarely in abstracts
- Risk-of-bias details require full Methods section
- Always cross-check web-filled values if PDFs become available later

## Validation

- Run consistency checks on missingness, ranges, and duplicated entries.
- Reconcile any discrepancies between double entries before analysis.
- Validate source coverage with `scripts/validate_sources.py` when sources are available.

## Pipeline Navigation

| Step | Skill                     | Stage                       |
| ---- | ------------------------- | --------------------------- |
| Prev | `/ma-fulltext-management` | 04 Full-text Management     |
| Next | `/ma-meta-analysis`       | 06 Statistical Analysis     |
| All  | `/ma-end-to-end`          | Full pipeline orchestration |
