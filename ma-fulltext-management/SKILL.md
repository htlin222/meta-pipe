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
- `04_fulltext/README.md`
- `04_fulltext/` PDF files
- `04_fulltext/previews/` (optional PDF image previews)

## Workflow
1. Create `04_fulltext/` and request the user to deposit PDFs there.
2. Build `manifest.csv` with `record_id`, DOI, PMID, title, file path, and access notes.
3. Optionally query Unpaywall for OA links using `scripts/unpaywall_fetch.py` via `uv run`.
4. Optionally render PDF previews with `scripts/render_pdf_previews.py` for visual QA.
5. Flag missing files and request them explicitly.
6. Run OCR only when needed and preserve original files.

## Resources
- `references/manifest-template.csv` provides a manifest header.
- `scripts/unpaywall_fetch.py` queries Unpaywall for open-access links.
- `scripts/analyze_unpaywall.py` analyzes Unpaywall results and generates summary statistics.
- `scripts/download_oa_pdfs.py` downloads open-access PDFs automatically from Unpaywall URLs.
- `scripts/render_pdf_previews.py` renders PDF pages to PNG previews.
Note: Unpaywall requires `UNPAYWALL_EMAIL` in `.env`.
Note: PDF previews require `pdftoppm` or `mutool` installed.

## Validation
- Ensure every included record has a matching full-text file or a documented reason for absence.
- Ensure `record_id` continuity with screening decisions.
