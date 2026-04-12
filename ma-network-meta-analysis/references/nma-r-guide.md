# Network Meta-Analysis in R: Step-by-Step Guide

**Time**: 30-45 minutes
**Primary**: gemtc (Bayesian) | **Sensitivity**: netmeta (frequentist)
**Stage**: 06 (Analysis)

---

## Quick Start

```r
# PRIMARY: Bayesian NMA
library(gemtc)
network <- mtc.network(data.re = nma_data)
model <- mtc.model(network, type = "consistency", linearModel = "random")
results <- mtc.run(model, n.adapt = 5000, n.iter = 50000, thin = 10)
summary(results)
rank.probability(results)  # Rankings
sucra(rank.probability(results))  # SUCRA

# SENSITIVITY: Frequentist NMA (supplement)
library(netmeta)
net <- netmeta(TE, seTE, treat1, treat2, studlab, data = nma_data,
               sm = "RR", random = TRUE, method.tau = "REML")
```

---

## Prerequisites

1. **JAGS installed**: https://mcmc-jags.sourceforge.io/
2. R packages: `gemtc`, `rjags`, `coda`, `netmeta`, `meta`

---

## Step 1: Data Preparation

NMA data can be in **contrast-based** or **arm-based** format.

### Contrast-Based (Relative Effects)

For gemtc:
```r
gemtc_data <- data.frame(
  study     = c("Trial1", "Trial1", "Trial2"),
  treatment = c("DrugA", "Placebo", "DrugB"),
  diff      = c(0.23, NA, 0.35),     # log-scale for RR/OR
  std.err   = c(0.11, NA, 0.14)
)
network <- mtc.network(data.re = gemtc_data)
```

### Arm-Based (Events + Totals)

```r
arm_data <- data.frame(
  study      = c("Trial1", "Trial1", "Trial2", "Trial2"),
  treatment  = c("DrugA", "Placebo", "DrugB", "Placebo"),
  responders = c(45, 30, 50, 28),
  sampleSize = c(100, 100, 120, 120)
)
network <- mtc.network(data.ab = arm_data)
```

---

## Step 2: Network Connectivity

```r
# Use netmeta utility for connectivity check
library(netmeta)
nc <- netconnection(treat1, treat2, studlab, data = nma_data)
print(nc)  # Must show: n.subnets = 1
```

---

## Step 3: Network Graph

```r
# netmeta has the best visualization
net <- netmeta(TE, seTE, treat1, treat2, studlab, data = nma_data,
               sm = "RR", random = TRUE, method.tau = "REML")

netgraph(net,
         number.of.studies = TRUE,
         thickness = "number.of.studies",
         cex.points = 3)
```

---

## Step 4: Fit Bayesian NMA (Primary)

### Random-Effects with Vague Priors

```r
library(gemtc)
model_re <- mtc.model(network,
                       type = "consistency",
                       linearModel = "random",
                       n.chain = 4)

results <- mtc.run(model_re,
                    n.adapt = 5000,
                    n.iter = 50000,
                    thin = 10)
```

### With Empirical Priors (Turner/Rhodes)

```r
# Log-OR, pharmacological vs placebo, all-cause mortality
hn.prior <- mtc.hy.prior("dlnorm", -3.95, 1.79^(-2))

model_re <- mtc.model(network,
                       type = "consistency",
                       linearModel = "random",
                       n.chain = 4,
                       hy.prior = hn.prior)

results <- mtc.run(model_re, n.adapt = 5000, n.iter = 50000, thin = 10)
```

### Convergence Diagnostics (Mandatory)

```r
library(coda)

# Gelman-Rubin (all Rhat must be < 1.05)
gelman.diag(results)

# Effective sample size (should be > 1000)
effectiveSize(results)

# Trace plots (visual check for mixing)
plot(results)
```

If Rhat > 1.05: increase `n.iter` or `n.adapt`.

### Model Comparison (DIC)

```r
model_fe <- mtc.model(network, type = "consistency",
                       linearModel = "fixed", n.chain = 4)
results_fe <- mtc.run(model_fe, n.adapt = 5000, n.iter = 50000, thin = 10)

# Lower DIC = better model
summary(results)$DIC      # Random-effects
summary(results_fe)$DIC   # Fixed-effect
```

---

## Step 5: Inconsistency Assessment

### Node-Splitting (Bayesian)

```r
nodesplit <- mtc.nodesplit(network, linearModel = "random", n.chain = 4)
nodesplit_results <- mtc.nodesplit.comparisons(nodesplit)
summary(nodesplit_results)
# p < 0.10 suggests local inconsistency
```

### Design Decomposition (via netmeta)

```r
dd <- decomp.design(net)
# Q_between-designs p < 0.05 → significant global inconsistency
```

### Net Heat Plot

```r
netheat(net, random = TRUE)
```

---

## Step 6: Forest Plots

```r
# Bayesian forest plot
forest(results)

# Frequentist forest plot (more customizable)
forest(net, reference.group = "Placebo", sortvar = TE)
```

---

## Step 7: SUCRA Rankings + Rankograms

```r
# Rank probabilities from Bayesian posterior
ranks <- rank.probability(results)
print(ranks)

# SUCRA
sucra_values <- sucra(ranks)
print(sucra_values)

# Rankogram (rank probability plot)
plot(ranks)  # Built-in rankogram
```

SUCRA interpretation: 0 = definitely worst, 1 = definitely best. Present with caution — SUCRA quantifies ranking probability, not clinical significance.

---

## Step 8: League Table

```r
# Bayesian: relative effects vs each reference
rel <- relative.effect(results, t1 = "Placebo")
summary(rel)

# Frequentist league table (supplement)
league <- netleague(net, random = TRUE, digits = 2)
```

### League Table Heatmap

A color-coded heatmap makes it easy to spot which comparisons favor which treatment at a glance. The script `nma_10_tables.R` generates this automatically, but here is the core approach for customization:

```r
library(ggplot2)
library(tidyr)

# 1. Get league matrix ordered by ranking
ranking <- netrank(net, small.values = "undesirable")
league  <- netleague(net, random = TRUE, seq = ranking, digits = 2)
mat     <- league$random

# 2. Parse each cell into numeric estimate + CI
#    Cell format is typically "0.85 [0.62, 1.17]"
parse_league_cell <- function(cell_text) {
  m <- regmatches(cell_text, regexec(
    "([0-9.-]+)\\s*[\\[\\(]([0-9.-]+)[,;]\\s*([0-9.-]+)[\\]\\)]", cell_text
  ))[[1]]
  if (length(m) == 4) {
    list(est = as.numeric(m[2]), lo = as.numeric(m[3]), hi = as.numeric(m[4]))
  } else {
    list(est = NA, lo = NA, hi = NA)
  }
}

# 3. Build long-format data frame
treat_names <- rownames(mat)
long_df <- do.call(rbind, lapply(seq_along(treat_names), function(i) {
  do.call(rbind, lapply(seq_along(treat_names), function(j) {
    if (i == j || is.na(mat[i, j])) return(NULL)
    vals <- parse_league_cell(mat[i, j])
    data.frame(
      row_treat = treat_names[i], col_treat = treat_names[j],
      estimate = vals$est, sig = (vals$lo > 1) | (vals$hi < 1),
      label = trimws(mat[i, j]), stringsAsFactors = FALSE
    )
  }))
}))

# 4. Plot
ggplot(long_df, aes(col_treat, row_treat)) +
  geom_tile(aes(fill = log(estimate)), color = "white") +
  geom_text(aes(label = label, fontface = ifelse(sig, "bold", "plain")),
            size = 3) +
  scale_fill_gradient2(
    low = "#2166AC", mid = "white", high = "#B2182B", midpoint = 0
  ) +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 0),
        panel.grid = element_blank())
```

**Customization options**:
- Change `scale_fill_gradient2` colors to match journal style
- Adjust `size` in `geom_text()` for readability (smaller for many treatments)
- For MD/SMD (non-ratio measures), use `estimate` directly instead of `log(estimate)` and set the null at 0

---

## Step 9: CINeMA (GRADE for NMA)

**This is non-negotiable for publication.** CINeMA rates certainty of evidence for each comparison across 6 domains:

1. Within-study bias (RoB)
2. Across-study bias (reporting/publication bias)
3. Indirectness (transitivity concerns)
4. Imprecision (width of credible intervals)
5. Heterogeneity (between-study variance)
6. Incoherence (inconsistency)

**Tool**: https://cinema.ispm.unibe.ch/ (web app)

Export your NMA results and RoB assessments, upload to CINeMA, rate each domain, and include the CINeMA summary table in your manuscript.

---

## Step 10: Frequentist Sensitivity (Supplement)

```r
# One run, place in supplement
net <- netmeta(TE, seTE, treat1, treat2, studlab,
               data = nma_data, sm = "RR",
               random = TRUE, method.tau = "REML")

# If results agree with Bayesian (they almost always will):
# "Frequentist sensitivity analysis using netmeta yielded
#  consistent results (Supplement Table SX)."
```

---

## Step 11: Component NMA (If Combination Treatments Exist)

If your network includes combination treatments (e.g., "DrugA+DrugB"), use CNMA to decompose effects:

```r
# Frequentist CNMA (primary) — additive model
cnma_add <- discomb(TE, seTE, treat1, treat2, studlab,
                    data = nma_data, sm = "RR",
                    random = TRUE, inactive = "placebo")
forest(cnma_add)

# Interaction model
cnma_int <- discomb(TE, seTE, treat1, treat2, studlab,
                    data = nma_data, sm = "RR",
                    random = TRUE, inactive = "placebo",
                    C.matrix = "full")

# Test interaction significance
q_diff <- cnma_add$Q - cnma_int$Q
df_diff <- cnma_add$df.Q - cnma_int$df.Q
p_interaction <- pchisq(q_diff, df = df_diff, lower.tail = FALSE)
# p > 0.05 → additive model sufficient
```

**Full template**: `nma_11_cnma.R` | **Guide**: [CNMA Guide](cnma-guide.md)

---

## Step 12: NMA Meta-Regression (If Covariates Available)

Explore heterogeneity sources with study-level covariates:

```r
# Continuous covariate
reg <- netmetareg(net_re, ~ mean_age)
bubble(reg)  # Bubble plot

# Categorical covariate
reg_cat <- netmetareg(net_re, ~ factor(risk_of_bias))

# Compare tau² reduction
cat("Baseline tau²:", net_re$tau2, "→ Adjusted:", reg$tau2)
```

**Full template**: `nma_12_meta_regression.R`

---

## Step 13: Statistical Transitivity Testing

Supplement clinical transitivity assessment with quantitative tests:

```r
# Compare effect modifier distributions across comparisons
kruskal.test(mean_age ~ comparison, data = nma_data)

# Meta-regression as transitivity proxy
# Large tau² changes when adjusting suggest modifier violates transitivity
reg <- netmetareg(net_re, ~ modifier)

# Direct vs full NMA comparison (Salanti 2012)
ns <- netsplit(net_re)  # Already run in nma_05
```

**Full template**: `nma_13_transitivity_tests.R`

---

## Common Pitfalls

1. **Skipping convergence diagnostics**: Always check Rhat, ESS, and trace plots
2. **Disconnected network**: Always check with `netconnection()` first
3. **Ignoring transitivity**: Document why populations are comparable across comparisons
4. **Over-interpreting SUCRA**: SUCRA quantifies ranking probability, not clinical significance
5. **Omitting CINeMA**: Top-3 reviewer rejection reason in 2026
6. **Wrong effect scale**: Use log-scale for RR/OR/HR in contrast data

---

## Turner/Rhodes Empirical Priors Reference

| Outcome Type | Prior | Source |
|-------------|-------|--------|
| All-cause mortality (pharma vs placebo) | `dlnorm(-3.95, 1.79^-2)` | Turner 2012 |
| Subjective outcomes (pharma vs placebo) | `dlnorm(-2.56, 1.74^-2)` | Turner 2012 |
| Semi-objective outcomes | `dlnorm(-3.40, 1.69^-2)` | Turner 2012 |
| Objective outcomes | `dlnorm(-4.18, 1.55^-2)` | Turner 2012 |

Use `mtc.hy.prior()` to set these in gemtc.

---

## See Also

- [NMA Overview](nma-overview.md) — Decision criteria for NMA vs pairwise
- [NMA Assumptions](nma-assumptions.md) — Transitivity, consistency, homogeneity
- [NMA Reporting Checklist](nma-reporting-checklist.md) — PRISMA-NMA items
- [Package Comparison](nma-package-comparison.md) — gemtc vs netmeta vs multinma
- [Package Selection](../../ma-meta-analysis/references/r-guides/09-package-selection.md) — Full R package guide
