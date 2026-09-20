# PRISMA-NMA Reporting Checklist

**Time**: 15 minutes (to review and map to your outputs)
**Standard**: PRISMA Extension for Network Meta-Analyses (Hutton et al., 2015)
**Items**: 32 items (27 PRISMA 2009 + 5 NMA-specific)

---

## How to Use This Checklist

1. Complete your NMA analysis using `nma_*.R` scripts
2. Work through each item below when drafting the manuscript
3. Mark each item as done and note the manuscript section/page
4. Items marked with **[NMA]** are specific to network meta-analysis

---

## Title

| # | Item | Description | Pipeline Output |
|---|------|-------------|-----------------|
| 1 | Title | Identify the report as a systematic review incorporating a network meta-analysis | 07_manuscript/00_abstract.qmd |

## Abstract

| # | Item | Description | Pipeline Output |
|---|------|-------------|-----------------|
| 2 | Structured abstract | Include: background, methods (including data sources, eligibility, NMA methods), results (treatments compared, rankings), conclusions | 07_manuscript/00_abstract.qmd |

## Introduction

| # | Item | Description | Pipeline Output |
|---|------|-------------|-----------------|
| 3 | Rationale | Describe why comparing multiple treatments is important | 07_manuscript/01_introduction.qmd |
| 4 | Objectives | State PICO with all treatments of interest | 01_protocol/pico.yaml |

## Methods

| # | Item | Description | Pipeline Output |
|---|------|-------------|-----------------|
| 5 | Protocol | PROSPERO registration; state if protocol was published | 01_protocol/prospero_registration.md |
| 6 | Eligibility | Inclusion/exclusion criteria including study designs | 01_protocol/eligibility.md |
| 7 | Information sources | Databases searched with dates | 02_search/round-01/search_audit.json |
| 8 | Search | Full search strategy for at least one database | 02_search/round-01/queries.txt |
| 9 | Study selection | Screening process, number of reviewers | 03_screening/round-01/agreement.md |
| 10 | Data collection | Data extraction process, forms used | 05_extraction/data-dictionary.md |
| 11 | Data items | Variables extracted per study | 05_extraction/data-dictionary.md |
| 12 | Risk of bias | Tool used (RoB 2, ROBINS-I), assessment process | 05_extraction/round-01/quality_rob2.csv |
| 13 | Summary measures | Effect measures (RR, OR, MD, SMD) | 06_analysis/nma_04_models.R |
| 14 | **[NMA] Methods of analysis** | Describe NMA method (frequentist/Bayesian), software, model (fixed/random), tau² estimator | 06_analysis/nma_04_models.R |
| 15 | **[NMA] Assessment of transitivity** | How transitivity was assessed across comparisons | 06_analysis/nma_05_inconsistency.R |
| 16 | **[NMA] Assessment of consistency** | Methods to evaluate consistency (node-splitting, design decomposition) | 06_analysis/nma_05_inconsistency.R |
| 17 | Risk of bias across studies | Methods for assessing publication bias | 06_analysis/nma_08_funnel.R |
| 18 | Additional analyses | Sensitivity, subgroup, meta-regression plans | 06_analysis/nma_09_sensitivity.R |

## Results

| # | Item | Description | Pipeline Output |
|---|------|-------------|-----------------|
| 19 | Study selection | PRISMA flow diagram with NMA-specific counts | 07_manuscript/prisma_flow.svg |
| 20 | Study characteristics | Table of included studies with treatments compared | 07_manuscript/study_characteristics.md |
| 21 | Risk of bias within studies | RoB summary across studies | 06_analysis/figures/ |
| 22 | **[NMA] Network geometry** | Network graph showing treatments and connections | 06_analysis/figures/network_graph.png |
| 23 | Results of individual studies | Effect estimates from each study | 06_analysis/nma_prepared_data.csv |
| 24 | Synthesis of results | NMA results: league table, forest plots | 06_analysis/tables/nma_league_table_bayesian.csv |
| 25 | **[NMA] Exploration of inconsistency** | Results of consistency assessment | 06_analysis/nma_inconsistency_report.txt |
| 26 | Risk of bias across studies | Funnel plot results | 06_analysis/figures/nma_funnel.png |
| 27 | Additional analyses | Sensitivity analysis results, leave-one-out | 06_analysis/nma_sensitivity_report.txt |
| 28 | **[NMA] Treatment rankings** | P-scores or SUCRA with uncertainty | 06_analysis/tables/nma_rankings.csv |

## Discussion

| # | Item | Description | Pipeline Output |
|---|------|-------------|-----------------|
| 29 | Summary of evidence | Key findings with GRADE certainty | 08_reviews/grade_summary.md |
| 30 | Limitations | Study and review level, including NMA assumptions | 07_manuscript/04_discussion.qmd |
| 31 | Conclusions | Clinical implications for treatment selection | 07_manuscript/04_discussion.qmd |

## Funding

| # | Item | Description | Pipeline Output |
|---|------|-------------|-----------------|
| 32 | Funding | Sources of support, role of funders | 07_manuscript/ |

---

## NMA-Specific Items Summary

The 5 NMA-specific extensions (items 14-16, 22, 25, 28) require:

1. **NMA methods description** (item 14): Package (netmeta), model (random-effects), tau² estimator (REML)
2. **Transitivity assessment** (item 15): Comparison of study characteristics across different treatment comparisons
3. **Consistency assessment** (items 16, 25): Design decomposition Q-test, node-splitting results, net heat plot
4. **Network geometry** (item 22): Network graph with node sizes and edge widths
5. **Treatment rankings** (item 28): P-scores with interpretation caveats

---

## Mapping to Pipeline Scripts

| PRISMA-NMA Item | NMA Script |
|-----------------|------------|
| Network geometry | nma_03_network_graph.R |
| NMA methods | nma_04_models.R |
| Transitivity | nma_05_inconsistency.R |
| Consistency | nma_05_inconsistency.R |
| Forest plots | nma_06_forest_plots.R |
| Rankings | nma_07_ranking.R |
| Publication bias | nma_08_funnel.R |
| Sensitivity | nma_09_sensitivity.R |
| Tables | nma_10_tables.R |

---

## Reference

Hutton B, Salanti G, Caldwell DM, et al. The PRISMA Extension Statement for Reporting of Systematic Reviews Incorporating Network Meta-analyses of Health Care Interventions: Checklist and Explanations. *Ann Intern Med*. 2015;162(11):777-784.
