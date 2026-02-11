---
name: ma-screening-quality
description: Perform title and abstract screening, apply inclusion and exclusion criteria, and assess study quality or risk of bias. Use when selecting eligible studies for meta-analysis.
---

# Ma Screening Quality

## Overview

Screen search results, document decisions, and assess risk of bias or quality.

## Inputs

- `02_search/round-01/dedupe.bib`
- `01_protocol/eligibility.md`

## Outputs

- `03_screening/round-01/decisions.csv`
- `03_screening/round-01/exclusions.csv`
- `03_screening/round-01/quality.csv`
- `03_screening/round-01/included.bib`
- `03_screening/round-01/agreement.md`

## Workflow

1. Calibrate screening with a small pilot set and align on criteria.
2. Screen titles and abstracts and record include, exclude, or maybe.
3. Record exclusion reasons using standardized labels.
4. Assess study quality or risk of bias using the tool appropriate for the study design.
5. Resolve conflicts and create the final `included.bib`.
6. Compute dual-review agreement with `scripts/dual_review_agreement.py` via `uv run`.

## Resources

- `references/screening-labels.md` provides standardized decision labels.
- `references/dual-review-schema.md` defines recommended decision columns.
- `scripts/dual_review_agreement.py` computes agreement and Cohen's kappa.

## Validation

- Compute agreement for dual screening when applicable.
- Confirm all included studies meet eligibility criteria.

## Pipeline Navigation

| Step | Skill                     | Stage                       |
| ---- | ------------------------- | --------------------------- |
| Prev | `/ma-search-bibliography` | 02 Search & Bibliography    |
| Next | `/ma-fulltext-management` | 04 Full-text Management     |
| All  | `/ma-end-to-end`          | Full pipeline orchestration |
