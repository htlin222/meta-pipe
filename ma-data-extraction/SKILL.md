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

## Workflow (Web-First Hybrid — Default)

⚠️ **Default approach**: Run web-based extraction FIRST, then use PDFs only for gaps.

### Phase 1: Web-Based Extraction (Default — Run First)

1. Define a data dictionary that covers outcomes, covariates, and study identifiers.
   - Write to `05_extraction/data-dictionary.md` (use `references/data-dictionary-template.md`)
2. Initialize a normalized SQLite database using `scripts/init_extraction_db.py` via `uv run`.
   - Use `scripts/init_extraction_db.py`
   - Creates `05_extraction/extraction.sqlite`
3. **Run WebSearch extraction for ALL included studies** — see **WebSearch Extraction (Default)** below.
   - Read from `03_screening/round-01/included.bib` or `04_fulltext/manifest.csv`
   - This fills 70-80% of data fields automatically from PubMed, ClinicalTrials.gov, etc.
   - Tag all web-sourced values with `[web]` in the `notes` column
   - Write to `05_extraction/extraction.sqlite` (studies table)
4. Review confidence scores: flag studies/fields with confidence < 0.7.

### Phase 2: PDF-Based Extraction (Only for Gaps)

5. For studies with low-confidence fields, run `scripts/llm_extract.py` via `uv run` on available PDFs.
   - Use `scripts/llm_extract.py`
   - Read PDFs from `04_fulltext/*.pdf`
   - Write to `05_extraction/llm_suggestions.jsonl`
6. Extract remaining data with double-entry or verification where possible.
   - Update `05_extraction/extraction.sqlite`
7. Record unit conversions and assumptions in `05_extraction/extraction-log.md`.
   - Write to `05_extraction/extraction-log.md`
8. Export a tidy CSV for analysis and lock the database snapshot.
   - Export `05_extraction/extraction.csv` from SQLite
9. (Recommended) Record source references in `05_extraction/source.csv` and validate with `scripts/validate_sources.py`.
   - Write to `05_extraction/source.csv` (use `references/source-template.csv`)
   - Validate with `scripts/validate_sources.py` → `05_extraction/source_validation.md`

## Resources

- `scripts/init_extraction_db.py` initializes a standard extraction schema.
- `scripts/llm_extract.py` provides LLM-assisted extraction suggestions.
- `scripts/validate_sources.py` validates extraction vs source references.
- `references/data-dictionary-template.md` provides a dictionary scaffold.
- `references/study-map-template.csv` maps `record_id` to `study_id` if needed.
- `references/source-template.csv` for source references.
  Note: `llm_extract.py` requires a PDF parser such as `pdfplumber` or `pypdf` (install via `uv add`).

## WebSearch Extraction (Default)

⚠️ **This is the DEFAULT first step** — Claude Code should run this BEFORE attempting PDF-based extraction. No scripts or API keys required.

### When to Use

- **ALWAYS** — run as Phase 1 for every extraction workflow
- Fills 70-80% of fields from structured online sources
- Identifies exactly which studies need PDF follow-up

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

## Stage Exit: Stamp the artifact

Record provenance for the locked extraction CSV. See
[artifact-stamping.md](../ma-end-to-end/references/artifact-stamping.md).

```bash
uv run tooling/python/session_log.py --project <project-name> append \
  --stage 05_extraction \
  --artifact 05_extraction/extraction.csv \
  --generator ai \
  --deviation "single-extractor"  # omit if double-extracted
```

## Pipeline Navigation

| Step | Skill                     | Stage                       |
| ---- | ------------------------- | --------------------------- |
| Prev | `/ma-fulltext-management` | 04 Full-text Management     |
| Next | `/ma-meta-analysis`       | 06 Statistical Analysis     |
| All  | `/ma-end-to-end`          | Full pipeline orchestration |
