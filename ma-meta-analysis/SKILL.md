---
name: ma-meta-analysis
description: Run statistical meta-analysis in R with renv, generate effect estimates, heterogeneity, and publication bias diagnostics, and export figures and tables. Use when analyzing extracted study data.
---

# Ma Meta Analysis

## Overview

Analyze extracted data using standard meta-analysis methods and produce validated outputs.

## Inputs

- `05_extraction/extraction.csv`
- `05_extraction/data-dictionary.md`

## Outputs

- `06_analysis/01_setup.R`
- `06_analysis/02_effect_sizes.R`
- `06_analysis/02a_pre_pool_diagnostics.R`
- `06_analysis/02a_diagnostics_report.md`
- `06_analysis/03_models.R`
- `06_analysis/04_subgroups_meta_regression.R`
- `06_analysis/05_plots.R`
- `06_analysis/06_tables.R`
- `06_analysis/07_sensitivity.R`
- `06_analysis/08_bias.R`
- `06_analysis/09_validation.R`
- `06_analysis/07_export_tables.R`
- `06_analysis/figures/` PNG files at 300 dpi
- `06_analysis/tables/` PNG + HTML + DOCX + CSV tables (via `gt` + `flextable`)
- `06_analysis/validation.md`
- `06_analysis/renv.lock`

## Statistical Defaults

All models must use **REML + Hartung-Knapp** (Cochrane mandate, July 2025):

```r
# meta:    metagen(..., method.tau = "REML", hakn = TRUE)
# metafor: rma(..., method = "REML", test = "knha")
```

Run DerSimonian-Laird as sensitivity analysis for comparison, but REML + HKSJ is the primary result.

## Workflow

1. Initialize `renv` in `06_analysis/` and record package versions.
   - Run `renv::init()` in `06_analysis/`
   - Creates `06_analysis/renv.lock`
2. Copy the R templates from `assets/r/` into `06_analysis/` and adapt them to the study schema.
   - Copy `assets/r/01_setup.R` → `06_analysis/01_setup.R`
   - Copy templates 02-09 similarly
3. Compute effect sizes with `metafor::escalc` for the outcome type.
   - In `06_analysis/02_effect_sizes.R` (use `metafor::escalc()` function)
4. **Run pre-pooling diagnostics** to check whether assumptions for pooling are met.
   - In `06_analysis/02a_pre_pool_diagnostics.R`
   - Produces traffic-light advisory (GREEN/YELLOW/RED) → `06_analysis/02a_diagnostics_report.md`
   - Checks: study count, I²/Q/tau², prediction interval, effect direction consistency, outliers
   - If RED: consider narrative synthesis; see `references/pre-pooling-assumptions.md`
   - If YELLOW: proceed with caution; always report prediction intervals
5. Fit primary models using `meta` and/or `metafor` with REML + Hartung-Knapp defaults.
   - In `06_analysis/03_models.R` (L10-30: metagen(..., method.tau = "REML", hakn = TRUE))
   - Models are advisory-aware: warnings and prediction intervals are shown based on step 4
6. Assess heterogeneity (I2, Q, tau2), subgroup analyses, and meta-regression when applicable.
   - In `06_analysis/04_subgroups_meta_regression.R`
7. Conduct sensitivity analyses and publication bias diagnostics.
   - In `06_analysis/07_sensitivity.R`
   - In `06_analysis/08_bias.R`
8. Generate forest and funnel plots at 300 dpi.
   - In `06_analysis/05_plots.R`
   - Write to `06_analysis/figures/*.png` (png(..., res=300, width=3000, height=2400))
9. Use `gtsummary` to build manuscript-ready summary tables.
   - In `06_analysis/06_tables.R` (use `gtsummary::tbl_summary()`)
10. Export tables as PNG/HTML/DOCX via `gt` + `flextable` for manuscript sync.
    - In `06_analysis/07_export_tables.R`
    - Write to `06_analysis/tables/*.png`, `06_analysis/tables/*.html`, `06_analysis/tables/*.docx`
11. Summarize key results and decisions in `06_analysis/validation.md`.
    - Write to `06_analysis/validation.md`

## Pre-Pooling Traffic-Light Advisory

Before computing pooled estimates, `02a_pre_pool_diagnostics.R` checks 5 assumptions and produces an advisory:

| Level | Meaning | Action |
|-------|---------|--------|
| **GREEN** | Assumptions met | Proceed normally |
| **YELLOW** | Moderate concerns | Pool with caution; report prediction intervals; explore heterogeneity |
| **RED** | Major concerns | Pooled estimate may mislead; consider narrative synthesis |

See `references/pre-pooling-assumptions.md` for full details on thresholds and recommended actions.

## Resources

- `assets/r/` provides a scaffolded R workflow that maps to the standard steps.
- `references/r-meta-roadmap.md` summarizes the expected analysis tasks.

## Validation

- Reproduce key estimates from at least one study subset.
- Confirm that effect sizes match the extraction units and directionality.

## Pipeline Navigation

| Step | Skill                   | Stage                       |
| ---- | ----------------------- | --------------------------- |
| Prev | `/ma-data-extraction`   | 05 Data Extraction          |
| Next | `/ma-manuscript-quarto` | 07 Manuscript Drafting      |
| All  | `/ma-end-to-end`        | Full pipeline orchestration |
