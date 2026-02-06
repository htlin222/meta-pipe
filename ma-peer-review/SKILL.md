---
name: ma-peer-review
description: Act as Reviewer 1 and Reviewer 2 for a meta-analysis manuscript, checking rigor, reproducibility, and reporting compliance. Use when validating the final paper before submission.
---

# Ma Peer Review

## Overview
Perform structured peer review and produce actionable feedback and validation checks.

## Inputs
- `07_manuscript/` rendered outputs
- `06_analysis/validation.md`
- `01_protocol/` and `03_screening/` artifacts

## Outputs
- `08_reviews/reviewer1.md`
- `08_reviews/reviewer2.md`
- `08_reviews/action-items.md`
- `08_reviews/grade_summary.csv`
- `08_reviews/grade_summary.md`
- `08_reviews/grade_suggestions.csv` (optional)
- `08_reviews/grade_suggestions.md` (optional)
- `03_screening/round-01/quality_rob2.csv` (RoB 2 for RCTs)
- `03_screening/round-01/rob2_assessment.md` (RoB 2 narrative)
- `03_screening/round-01/quality_robins_i.csv` (ROBINS-I for observational)
- `03_screening/round-01/robins_i_assessment.md` (ROBINS-I narrative)

## Workflow
1. Reviewer 1 focuses on methodology, inclusion criteria, and statistical validity.
2. Reviewer 2 focuses on clarity, reporting completeness, and reproducibility.
3. Record issues with severity, location, and recommended fixes.
4. Create a consolidated action list with owners and status.
5. Initialize GRADE summary tables with `scripts/init_grade_summary.py` via `uv run`.
6. Optionally generate preliminary GRADE suggestions with `scripts/auto_grade_suggestion.py`.

## Resources
- `references/reporting-checks.md` for PRISMA-style reporting checks.
- `references/grade-template.md` for GRADE evidence profiling.
- `references/grade-summary-schema.md` for GRADE summary columns.
- `references/rob2-template.md` for RoB 2 per-study assessment (RCTs).
- `references/robins-i-template.md` for ROBINS-I per-study assessment (observational).
- `scripts/init_grade_summary.py` for generating GRADE summary tables.
- `scripts/auto_grade_suggestion.py` for initial certainty suggestions.
- `scripts/init_rob2_assessment.py` for initializing RoB 2 assessment tables.
- `scripts/init_robins_i_assessment.py` for initializing ROBINS-I assessment tables.

## Validation
- Verify that methods and results are consistent with the protocol.
- Confirm that all outputs are reproducible from the stored data and scripts.
