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
- `06_analysis/03_models.R`
- `06_analysis/04_subgroups_meta_regression.R`
- `06_analysis/05_plots.R`
- `06_analysis/06_tables.R`
- `06_analysis/07_sensitivity.R`
- `06_analysis/08_bias.R`
- `06_analysis/09_validation.R`
- `06_analysis/figures/` PNG files at 300 dpi
- `06_analysis/tables/` CSV or HTML tables
- `06_analysis/validation.md`
- `06_analysis/renv.lock`

## Workflow

1. Initialize `renv` in `06_analysis/` and record package versions.
2. Copy the R templates from `assets/r/` into `06_analysis/` and adapt them to the study schema.
3. Compute effect sizes with `metafor::escalc` for the outcome type.
4. Fit primary models using `meta` and/or `metafor`.
5. Assess heterogeneity (I2, Q, tau2), subgroup analyses, and meta-regression when applicable.
6. Conduct sensitivity analyses and publication bias diagnostics.
7. Generate forest and funnel plots at 300 dpi.
8. Use `gtsummary` to build manuscript-ready summary tables.
9. Summarize key results and decisions in `06_analysis/validation.md`.

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
