---
name: ma-network-meta-analysis
description: Run network meta-analysis (NMA) comparing ≥3 treatments, generate league tables, SUCRA rankings, inconsistency checks, and CINeMA GRADE. Use when analysis_type is NMA.
---

# Ma Network Meta Analysis

## Overview

Analyze extracted data using network meta-analysis methods when ≥3 treatments are compared. Produces league tables, treatment rankings, inconsistency assessments, and all NMA-specific outputs required for PRISMA-NMA compliance.

## Package Selection Guide

Pick the right R package before you start:

### 1. What's your statistical approach?

```
Do you need credible intervals & prior beliefs?
├── YES → Bayesian branch (see below)
└── NO  → Frequentist → netmeta ✅
```

### 2. Bayesian branch — What's your data type?

```
Do you have Individual Patient Data (IPD)?
├── YES → multinma ✅
└── NO  → Aggregate only
         ├── Need speed?     → nmaINLA ✅
         ├── Need reporting? → BUGSnet ✅
         └── General use     → gemtc / bnma ✅
```

### 3. Quick checklist

| Question                         | Points to             |
|----------------------------------|-----------------------|
| I'm new to NMA                   | `netmeta`             |
| I need a league table fast       | `netmeta`             |
| My journal requires Bayesian     | `gemtc` or `multinma` |
| I have both IPD + aggregate data | `multinma`            |
| MCMC is too slow for me          | `nmaINLA`             |
| I need PRISMA-NMA compliance     | `BUGSnet`             |
| I want the most modern/flexible  | `multinma`            |

**Bottom line**: Start with `netmeta` — if reviewers or your analysis demand Bayesian, move to `gemtc` or `multinma`.

See [Package Comparison](references/nma-package-comparison.md) for detailed feature matrix.

## Inputs

- `05_extraction/extraction.csv` (must include `treat1`, `treat2` columns)
- `05_extraction/data-dictionary.md`
- `01_protocol/analysis-type-decision.md` (confirmed NMA after screening)

## Outputs

- `06_analysis/nma_01_setup.R`
- `06_analysis/nma_02_data_prep.R`
- `06_analysis/nma_03_network_graph.R`
- `06_analysis/nma_04_models.R`
- `06_analysis/nma_05_inconsistency.R`
- `06_analysis/nma_06_forest.R`
- `06_analysis/nma_07_ranking.R`
- `06_analysis/nma_08_league_table.R`
- `06_analysis/nma_08_funnel.R`
- `06_analysis/nma_09_sensitivity.R`
- `06_analysis/nma_10_tables.R`
- `06_analysis/figures/` — network graph, forest plots, rankograms, funnel plot, net heat plot (300 DPI)
- `06_analysis/tables/` — league table (PNG + CSV + HTML), SUCRA rankings, contribution matrix
- `06_analysis/validation.md`

## Statistical Defaults

**Primary**: Bayesian NMA via `gemtc` (NICE/WHO/Cochrane aligned)
**Sensitivity**: Frequentist NMA via `netmeta` (supplement)

```r
# PRIMARY: Bayesian (gemtc)
library(gemtc)
model <- mtc.model(network, type = "consistency",
                   linearModel = "random", n.chain = 4)
results <- mtc.run(model, n.adapt = 5000, n.iter = 50000, thin = 10)

# SENSITIVITY: Frequentist (netmeta)
library(netmeta)
net <- netmeta(TE, seTE, treat1, treat2, studlab, data = nma_data,
               sm = "RR", random = TRUE, method.tau = "REML")
```

## Workflow

### Step 1: Setup & Data Preparation

Initialize `renv` and prepare NMA data format (contrast-based or arm-based).

- Script: `nma_01_setup.R`, `nma_02_data_prep.R`
- Verify network connectivity: `netconnection()` must show `n.subnets = 1`

### Step 2: Network Graph

Visualize the treatment network — nodes = treatments, edges = direct comparisons.

- Script: `nma_03_network_graph.R`
- Output: `figures/network_graph.png` (300 DPI)

### Step 3: Fit NMA Models

Run Bayesian primary (gemtc) + fixed vs random comparison via DIC.

- Script: `nma_04_models.R`
- **Mandatory**: Convergence diagnostics — Rhat < 1.05, ESS > 1000, trace plots

### Step 4: Inconsistency Assessment

Test agreement between direct and indirect evidence.

- Script: `nma_05_inconsistency.R`
- Methods: Node-splitting (Bayesian) + design decomposition (frequentist)
- Output: `figures/net_heat_plot.png`

### Step 5: Forest Plots

Forest plots for key comparisons vs reference treatment.

- Script: `nma_06_forest.R`
- Output: `figures/forest_*.png` (300 DPI)

### Step 6: Treatment Rankings

SUCRA scores + rankograms (Bayesian), P-scores (frequentist sensitivity).

- Script: `nma_07_ranking.R`
- Output: `tables/sucra_rankings.csv`, `figures/rankograms.png`
- **Caution**: SUCRA quantifies ranking probability, not clinical significance

### Step 7: League Table

**The league table is a core NMA output** — it shows all pairwise comparisons in a single matrix.

- Script: `nma_08_league_table.R`
- Output: `tables/league_table.png`, `tables/league_table.csv`, `tables/league_table.html`
- Format: Upper triangle = effect estimates (RR/OR/HR with 95% CrI), lower triangle = reversed comparisons
- All n×(n-1)/2 pairwise comparisons must be present

```r
# --- Bayesian league table (gemtc) ---
# Relative effects vs each treatment
rel <- relative.effect(results, t1 = "Placebo")
summary(rel)

# Full league table: loop over all reference treatments
treatments <- network$treatments$id
league_matrix <- matrix(NA, nrow = length(treatments), ncol = length(treatments),
                        dimnames = list(treatments, treatments))
for (ref in treatments) {
  rel <- relative.effect(results, t1 = ref)
  # Extract point estimates and CrI into matrix
}

# --- Frequentist league table (netmeta) ---
league <- netleague(net, random = TRUE, digits = 2)
print(league)

# --- Export as publication-ready table ---
# Use gt package for PNG/HTML output
library(gt)
league_gt <- gt(league_df) |>
  tab_header(title = "League Table: All Pairwise Comparisons") |>
  tab_footnote("Values are RR (95% CrI). Read across rows vs columns.")
gtsave(league_gt, "tables/league_table.png")
gtsave(league_gt, "tables/league_table.html")
write.csv(league_df, "tables/league_table.csv", row.names = FALSE)
```

### Step 7b: Comparison-Adjusted Funnel Plot

Assess small-study effects and publication bias in the network.

- Script: `nma_08_funnel.R`
- Output: `figures/nma_funnel.png` (300 DPI)
- Treatments ordered by P-score; asymmetry suggests potential small-study effects
- Note: Standard Egger's test does not directly apply to NMA — the comparison-adjusted funnel is the primary diagnostic (Chaimani & Salanti, 2012)

### Step 8: Sensitivity Analysis

Frequentist (netmeta) concordance check + leave-one-out.

- Script: `nma_09_sensitivity.R`
- If Bayesian and frequentist agree: one sentence in manuscript establishes robustness

### Step 9: Combined Tables & Export

Compile all tables (league table, rankings, inconsistency) for manuscript/supplement.

- Script: `nma_10_tables.R`
- Export as PNG (300 DPI), HTML, DOCX, CSV via `gt` + `flextable`

### Step 10: CINeMA (GRADE for NMA)

Rate certainty of evidence per comparison across 6 domains. **Non-negotiable for publication.**

- Tool: https://cinema.ispm.unibe.ch/
- Reference: Nikolakopoulou A, Higgins JPT, Papakonstantinou T, et al. CINeMA: An approach for assessing confidence in the results of a network meta-analysis. *PLoS Med*. 2020;17(4):e1003082. [PMC7122720](https://pmc.ncbi.nlm.nih.gov/articles/PMC7122720/)
- Output: `08_reviews/cinema_assessment.csv`

**6 CINeMA Domains** (rate per pairwise comparison):

| Domain | What it assesses | Downgrade trigger |
|--------|-----------------|-------------------|
| Within-study bias | Risk of bias in contributing studies | Majority high/some concerns RoB |
| Reporting bias | Publication/selective reporting bias | Funnel asymmetry, small-study effects |
| Indirectness | Transitivity violations | Population/intervention differences across comparisons |
| Imprecision | Width of credible/confidence intervals | CrI crosses clinical decision threshold |
| Heterogeneity | Between-study variance | Large tau², high I² in direct comparisons |
| Incoherence | Direct vs indirect evidence disagreement | Significant node-splitting p-values |

**Judgment levels**: No concerns → Some concerns (-1) → Major concerns (-2)

**Workflow** (manual — CINeMA is web-only, no R automation exists):
1. Export NMA results + RoB data from R
2. Upload to [CINeMA web app](https://cinema.ispm.unibe.ch/)
3. Rate each domain per pairwise comparison
4. Download summary CSV → save as `08_reviews/cinema_assessment.csv`
5. Include as Table S10 in supplement

`nma_09_sensitivity.R` generates a blank `cinema_template.csv` to help structure your ratings.

## Validation

- Convergence: All Rhat < 1.05, ESS > 1000
- Consistency: Node-splitting p-values reported, inconsistency discussed
- League table: All n×(n-1)/2 comparisons present
- Rankings: SUCRA with uncertainty, no overclaims
- CINeMA: All key comparisons assessed
- PRISMA-NMA: 32/32 items addressed

Run automated checks:
```bash
cd /home/user/meta-pipe
uv run ma-network-meta-analysis/scripts/validate_nma_outputs.py \
  --root projects/<project-name>
```

See [NMA Completion Checklist](references/nma-completion-checklist.md) for the full 25-item pre-submission checklist.

## Resources

- [NMA Overview](references/nma-overview.md) — When to use NMA vs pairwise (10 min)
- [NMA R Guide](references/nma-r-guide.md) — Step-by-step Bayesian workflow (30-45 min)
- [NMA Assumptions](references/nma-assumptions.md) — Transitivity, consistency, homogeneity
- [Package Comparison](references/nma-package-comparison.md) — gemtc vs netmeta vs multinma
- [NMA Reporting Checklist](references/nma-reporting-checklist.md) — PRISMA-NMA 32-item checklist
- [NMA Completion Checklist](references/nma-completion-checklist.md) — 25-item pre-submission checklist

## Pipeline Navigation

| Step | Skill                   | Stage                       |
| ---- | ----------------------- | --------------------------- |
| Prev | `/ma-data-extraction`   | 05 Data Extraction          |
| Next | `/ma-manuscript-quarto` | 07 Manuscript Drafting      |
| Alt  | `/ma-meta-analysis`     | 06a Pairwise (if ≤2 treatments) |
| All  | `/ma-end-to-end`        | Full pipeline orchestration |
