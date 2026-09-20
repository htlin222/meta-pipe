---
name: ma-network-meta-analysis
description: Run network meta-analysis in R with gemtc (Bayesian, primary) and netmeta (frequentist, sensitivity), generate network graphs, league tables, SUCRA rankings, inconsistency diagnostics, and CINeMA GRADE assessment. Use when comparing ≥3 treatments with direct and indirect evidence.
---

# Ma Network Meta Analysis

## Overview

Analyze extracted data comparing three or more treatments using network meta-analysis methods. **Primary analysis is Bayesian (gemtc)** per 2026 NICE/WHO/Cochrane methodological consensus. Frequentist sensitivity (netmeta) goes in supplement.

## Methodological Rationale (2026 Consensus)

- **Bayesian primary**: NICE, WHO, Cochrane guidelines are Bayesian-based; reviewers expect Bayesian NMA
- **Empirical priors**: Turner et al. and Rhodes et al. priors for different outcome types (OR, HR, MD) are widely accepted — cite directly, no need to justify
- **Vague priors**: Also acceptable; results will closely match frequentist
- **SUCRA + rankogram**: Most familiar ranking presentation for reviewers; produced directly from posterior distributions
- **CINeMA (GRADE for NMA)**: More important than method choice — top reviewer concern after inconsistency and transitivity
- **Frequentist sensitivity**: Run netmeta once, place in supplement; if results agree (almost always), one sentence establishes robustness

## When to Use

- Research question compares **≥3 distinct treatments** (not just intervention vs control)
- Evidence network includes both **direct and indirect comparisons**
- `analysis_type: nma` is set in `01_protocol/pico.yaml`

## Inputs

- `05_extraction/extraction.csv` with columns: `study_id`, `treat1`, `treat2`, `TE` (treatment effect), `seTE` (standard error), plus arm-level data if available
- `05_extraction/data-dictionary.md`
- `01_protocol/pico.yaml` with `analysis_type: nma`

## Outputs

- `06_analysis/nma_01_setup.R` through `nma_10_tables.R`
- `06_analysis/figures/` — network graph, forest plots, rankogram, heat plot, funnel plot (300 DPI)
- `06_analysis/tables/` — league table, SUCRA rankings, CINeMA summary as PNG/CSV
- `06_analysis/validation.md` — NMA-specific validation summary
- `06_analysis/renv.lock`

## Workflow

1. Initialize `renv` in `06_analysis/` and install gemtc, rjags, netmeta, meta, metafor, ggplot2, gt.
   - Run `renv::init()` in `06_analysis/`
   - Creates `06_analysis/renv.lock`
2. Copy NMA R templates from `ma-network-meta-analysis/assets/r/` into `06_analysis/` and adapt to study schema.
   - Copy `assets/r/nma_01_setup.R` through `nma_10_tables.R` → `06_analysis/`
3. Prepare data in contrast-based or arm-based format for gemtc.
   - Read from `05_extraction/extraction.csv` (columns: study_id, treat1, treat2, TE, seTE)
   - In `06_analysis/nma_02_prepare_data.R`
4. Verify network connectivity with `netconnection()` and visualize geometry with `netgraph()`.
   - In `06_analysis/nma_03_network_graph.R` (use netmeta::netconnection(), netmeta::netgraph())
   - Write to `06_analysis/figures/network-graph.png` (png(..., res=300))
5. **Fit Bayesian NMA with gemtc** (primary): consistency model, random effects, empirical priors (Turner/Rhodes) or vague priors. Check convergence (Rhat, trace plots, effective sample size).
   - In `06_analysis/nma_04_bayesian_model.R` (use gemtc::mtc.network(), gemtc::mtc.model(), gemtc::mtc.run())
6. Assess inconsistency: node-splitting (`mtc.nodesplit()`), unrelated mean effects model, and design decomposition via netmeta.
   - In `06_analysis/nma_05_inconsistency.R` (use gemtc::mtc.nodesplit())
7. Generate forest plots from posterior distributions at 300 DPI.
   - In `06_analysis/nma_06_forest_plots.R`
   - Write to `06_analysis/figures/nma-forest.png` (png(..., res=300))
8. Compute SUCRA rankings and rankograms from posterior samples.
   - In `06_analysis/nma_07_rankings.R` (use gemtc::rank.probability())
   - Write to `06_analysis/figures/rankogram.png`
9. Create comparison-adjusted funnel plot.
   - In `06_analysis/nma_08_funnel.R` (use netmeta::funnel())
   - Write to `06_analysis/figures/funnel-nma.png`
10. Run frequentist sensitivity with `netmeta(method.tau="REML")` — place in supplement.
    - In `06_analysis/nma_09_sensitivity.R` (use netmeta::netmeta(..., method.tau="REML"))
11. Export league table (full pairwise comparisons), heatmap, and rankings as gt/PNG at 300 DPI.
    - In `06_analysis/nma_10_tables.R` (gemtc::relative.effect.table() primary, netmeta::netleague() supplement, gt::gtsave())
    - Write to `06_analysis/tables/nma_league_table_bayesian.csv`, `nma_league_table_frequentist.csv`, `league_table_heatmap.png`, `nma_summary.png`
    - Every cell in these tables/heatmaps = row vs column (network estimate). The raw `netleague()` file (`nma_league_table_netleague.csv/.xlsx`) is different: lower triangle = network (column vs row), upper = direct estimates
    - Set `NMA_SM` / `NMA_SMALL_VALUES` / `NMA_REF_TREAT` once in `nma_01_setup.R`; they drive netrank(), rank.probability(preferredDirection) and heatmap colour direction
12. **Run CINeMA assessment** (GRADE for NMA) — rate certainty of each comparison.
    - Manual or via CINeMA web app (https://cinema.ispm.unibe.ch/)
    - Write to `06_analysis/tables/cinema-summary.csv`
13. Document transitivity assessment, assumptions, and decisions in `06_analysis/validation.md`.
    - Write to `06_analysis/validation.md`

## Key Priorities (Reviewer Rejection Prevention)

Ranked by frequency of reviewer objections (2026):

1. **Inconsistency handling** — Must use ≥2 methods (node-splitting + global test)
2. **Transitivity argument** — Table of study characteristics by comparison, explicit narrative
3. **CINeMA / GRADE for NMA** — Rate certainty per comparison; omission is a common rejection reason
4. **Method choice** — Bayesian primary handles this automatically

## Resources

- `assets/r/` provides 10 scaffolded NMA R scripts (nma_01 through nma_10).
- `references/nma-overview.md` — when to use NMA vs pairwise MA.
- `references/nma-r-guide.md` — step-by-step R workflow (Bayesian primary + frequentist sensitivity).
- `references/nma-reporting-checklist.md` — PRISMA-NMA 32-item checklist.
- `references/nma-package-comparison.md` — gemtc vs netmeta vs multinma.
- `references/nma-assumptions.md` — transitivity, consistency, homogeneity assessment.
- `references/nma-oncology-tte.md` — oncology time-to-event NMA: PH testing, Guyot IPD reconstruction, multinma M-splines, RMST.

## Validation

- Verify network is connected (`netconnection()` returns single component).
- Confirm Bayesian model convergence (Rhat < 1.05, adequate ESS, visual trace plots).
- Check inconsistency via ≥2 methods (node-splitting + design decomposition or UME model).
- Complete CINeMA assessment for all key comparisons.
- Ensure all figures exported at ≥300 DPI.
- Complete PRISMA-NMA checklist before manuscript submission.

## NMA Quality Checklist

- [ ] Network connectivity verified
- [ ] Network graph with node/edge sizing created
- [ ] Transitivity assumption documented (table of characteristics by comparison)
- [ ] Bayesian NMA fitted with convergence diagnostics (Rhat, trace plots, ESS)
- [ ] Empirical or vague priors documented and justified
- [ ] Node-splitting for local inconsistency
- [ ] Global inconsistency test (design decomposition or UME model)
- [ ] Net heat plot generated
- [ ] SUCRA rankings with rankograms computed
- [ ] League table with all pairwise comparisons (posterior medians + 95% CrI)
- [ ] Comparison-adjusted funnel plot created
- [ ] **CINeMA (GRADE for NMA) completed** — rate certainty per comparison
- [ ] Frequentist sensitivity (netmeta) in supplement
- [ ] PRISMA-NMA checklist completed

## Pipeline Navigation

| Step | Skill                   | Stage                       |
| ---- | ----------------------- | --------------------------- |
| Prev | `/ma-data-extraction`   | 05 Data Extraction          |
| Next | `/ma-manuscript-quarto` | 07 Manuscript Drafting      |
| Alt  | `/ma-meta-analysis`     | 06 Pairwise Meta-Analysis   |
| All  | `/ma-end-to-end`        | Full pipeline orchestration |
