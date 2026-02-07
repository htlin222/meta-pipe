# R Package Selection for Meta-Analysis

**When to use**: You need to choose the right R package for your analysis
**Time**: 10-15 minutes (reading and decision)
**Stage**: 06 (Analysis planning)

---

## Quick Decision Guide

| Your Task               | Use This Package         | Why                               |
| ----------------------- | ------------------------ | --------------------------------- |
| Calculate effect sizes  | `metafor::escalc()`      | Handles 50+ effect size types     |
| Fit meta-analysis model | `metafor::rma()`         | Gold standard, most flexible      |
| Simple binary outcomes  | `meta::metabin()`        | Simpler syntax, auto forest plots |
| Assess heterogeneity    | `metafor`                | Full suite of stats + CIs         |
| Publication bias        | `metafor` + `dmetar`     | Multiple methods available        |
| Forest plots (quick)    | `meta::forest()`         | Auto-generated, publication-ready |
| Forest plots (custom)   | `metafor::forest()`      | Full control over layout          |
| Meta-regression         | `metafor::rma(mods = ~)` | Native moderator support          |
| Multilevel models       | `metafor::rma.mv()`      | Handles dependent effect sizes    |
| Robust variance         | `clubSandwich`           | Cluster-robust SE for multilevel  |
| Network meta-analysis   | `netmeta` or `gemtc`     | Frequentist or Bayesian NMA       |
| Bayesian meta-analysis  | `brms`                   | Full Bayesian inference           |
| PRISMA flow diagram     | `PRISMA2020`             | Standardized reporting            |

---

## Recommended Package Stack

**The Typical Stack** (covers ~80% of meta-analysis needs):

```r
# Core (MUST HAVE)
install.packages("metafor")      # Backbone: effect sizes, models, heterogeneity, meta-regression
install.packages("meta")         # Quick forest plots for simple RCTs

# Essential Supplements (SHOULD HAVE)
install.packages("dmetar")       # Convenient bias tools (p-curve, limit meta-analysis)
install.packages("clubSandwich") # Robust variance for multilevel models
install.packages("PublicationBias") # Sensitivity analyses for publication bias

# Network Meta-Analysis (IF NEEDED)
install.packages("netmeta")      # Frequentist NMA
install.packages("gemtc")        # Bayesian NMA
```

**Why this stack?**

| Package             | Role                                             | Coverage |
| ------------------- | ------------------------------------------------ | -------- |
| **metafor**         | Foundation - handles 80% of all analyses         | 80%      |
| **meta**            | Quick visualization - publication-ready plots    | +10%     |
| **dmetar**          | Publication bias helpers - p-curve, diagnostics  | +5%      |
| **clubSandwich**    | Advanced models - robust variance for multilevel | +3%      |
| **PublicationBias** | Sensitivity - Mathur & VanderWeele methods       | +2%      |

**Total coverage**: ~95-98% of typical meta-analysis workflows

---

## By Analysis Stage

### 1. Effect Size Calculation

**Best: `escalc()` from metafor**

**Why**: Handles widest variety (50+ types): Cohen's d, Hedges' g, log odds ratios, correlations, risk ratios, etc. Automatically computes sampling variances.

```r
library(metafor)

# Calculate log risk ratios
es <- escalc(
  measure = "RR",
  ai = events_ici,      # Events in intervention
  n1i = total_ici,      # Total in intervention
  ci = events_control,  # Events in control
  n2i = total_control,  # Total in control
  data = data
)
```

#### Package Comparison

| Package                | Strengths                                                   | Weaknesses                    |
| ---------------------- | ----------------------------------------------------------- | ----------------------------- |
| **metafor** (`escalc`) | Comprehensive, well-documented, handles nearly all ES types | Steeper learning curve        |
| **esc**                | Simpler syntax, good for converting between ES types        | Fewer ES types supported      |
| **compute.es**         | Quick conversions from test statistics                      | No longer actively maintained |

**Recommendation**: Use `metafor::escalc()` for all projects

---

### 2. Fitting the Meta-Analytic Model

**Best: `metafor` (rma(), rma.mv())**

**Why**: Gold standard. Supports fixed-effect, random-effects (multiple tau² estimators: REML, DL, PM, etc.), and multivariate/multilevel models. Extensively validated.

```r
library(metafor)

# Random-effects model with REML
res <- rma(
  yi = yi,           # Effect sizes from escalc()
  vi = vi,           # Variances from escalc()
  data = es,
  method = "REML"    # Recommended tau² estimator
)
```

#### Package Comparison

| Package       | Strengths                                                                                      | Weaknesses                       |
| ------------- | ---------------------------------------------------------------------------------------------- | -------------------------------- |
| **metafor**   | Most flexible, multilevel models, 10+ tau² estimators, robust variance                         | More verbose syntax              |
| **meta**      | Simpler one-function interface (`metagen`, `metabin`, `metacont`), auto-generates forest plots | Less flexible for complex models |
| **rmeta**     | Lightweight                                                                                    | Outdated, limited features       |
| **bayesmeta** | Bayesian random-effects with proper priors                                                     | Narrower scope, slower           |

**Recommendation**:

- **For most projects**: Use `metafor` for flexibility
- **For simple RCT meta-analysis**: Use `meta` for simpler syntax

---

### 3. Heterogeneity Assessment

**Best: `metafor`**

**Why**: Reports Q, I², H², tau², prediction intervals, and confidence intervals for heterogeneity measures. `confint()` gives CIs for tau². Supports subgroup analysis and meta-regression natively.

```r
library(metafor)

# Fit model
res <- rma(yi, vi, data = es)

# Get heterogeneity stats
print(res)  # Shows Q, I², H², tau²

# Get CI for tau²
confint(res)

# Prediction interval
predict(res)

# Subgroup analysis
res_subgroup <- rma(yi, vi, mods = ~ subgroup, data = es)
```

#### Package Comparison

| Package     | Strengths                                                             | Weaknesses                    |
| ----------- | --------------------------------------------------------------------- | ----------------------------- |
| **metafor** | Full suite of heterogeneity stats + CIs for tau²                      | —                             |
| **meta**    | Reports I², tau², H; easy subgroup analyses                           | No CI for tau² out of the box |
| **dmetar**  | Helper functions like `find.outliers()`, built on top of meta/metafor | Add-on, not standalone        |

**Recommendation**: Use `metafor` for comprehensive heterogeneity assessment

---

### 4. Publication Bias

**Best: `metafor` + `dmetar` + `PublicationBias`**

**Why**: No single package dominates; each contributes unique methods.

```r
library(metafor)
library(dmetar)

# Funnel plot
funnel(res)

# Egger's test
regtest(res)

# Trim-and-fill
trimfill(res)

# P-curve (via dmetar)
pcurve(res)
```

#### Package Comparison

| Package             | What it does best                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------------------- |
| **metafor**         | Funnel plots, Egger's test (`regtest()`), trim-and-fill (`trimfill()`), selection models (`selmodel()`) |
| **dmetar**          | Convenient wrappers: `pcurve()`, limit meta-analysis                                                    |
| **PublicationBias** | Sensitivity analysis (Mathur & VanderWeele methods), robust to selection model assumptions              |
| **weightr**         | Vevea-Hedges weight-function models for selection                                                       |

**Recommendation**:

- Use `metafor` for standard methods (funnel plot, Egger's, trim-and-fill)
- Add `dmetar` for p-curve and limit meta-analysis
- Use `PublicationBias` for sensitivity analysis

---

### 5. Forest Plots

**Best: `meta` for quick plots, `metafor` for full customization**

**Why**: `meta` auto-generates publication-ready forest plots with one command. `metafor` requires more code but offers pixel-level control.

```r
# Quick forest plot with meta
library(meta)
res <- metabin(event.e, n.e, event.c, n.c, data = data)
forest(res)  # Done!

# Custom forest plot with metafor
library(metafor)
res <- rma(yi, vi, data = es)
forest(res,
       atransf = exp,           # Back-transform to RR
       xlim = c(-5, 5),
       header = "Study",
       mlab = "Pooled Effect")
```

#### Package Comparison

| Package        | Strengths                                                                     | Weaknesses                                   |
| -------------- | ----------------------------------------------------------------------------- | -------------------------------------------- |
| **meta**       | Auto forest plots with `forest()`, simple syntax, publication-ready defaults  | Less customization, harder to modify layouts |
| **metafor**    | Full control over layout, colors, annotations; supports complex models        | More verbose, requires manual customization  |
| **forestplot** | Advanced grid-based layouts, multiple columns, confidence bands               | Steeper learning curve, not meta-specific    |
| **orchaRd**    | Specialized for ecology/evolution meta-analysis, beautiful default aesthetics | Narrow domain focus                          |

**Recommendation**:

- **For most projects**: Use `meta::forest()` for speed
- **For publication customization**: Use `metafor::forest()` for control
- **For multi-panel layouts**: Use `forestplot` package

---

### 6. Meta-Regression

**Best: `metafor` (rma() with mods = ~)**

**Why**: Native support for continuous and categorical moderators, interaction terms, model comparison, and robust variance estimation.

```r
library(metafor)

# Simple meta-regression
res_mr <- rma(yi, vi, mods = ~ age + pdl1_status, data = es)

# Interaction term
res_int <- rma(yi, vi, mods = ~ age * treatment, data = es)

# Model comparison
anova(res, res_mr)  # Test moderators jointly
```

#### Package Comparison

| Package      | Strengths                                                                        | Weaknesses                               |
| ------------ | -------------------------------------------------------------------------------- | ---------------------------------------- |
| **metafor**  | Native meta-regression (`mods = ~`), robust SE, model comparison, residual plots | Frequentist only                         |
| **meta**     | Simple `metareg()` function for basic regression                                 | Limited to simple models, no interaction |
| **brms**     | Bayesian meta-regression with priors, non-linear models                          | Slower, requires MCMC knowledge          |
| **MCMCglmm** | Bayesian multilevel meta-regression                                              | Complex syntax, steep learning curve     |

**Recommendation**: Use `metafor` unless you need Bayesian inference (then `brms`)

---

### 7. Multilevel / Three-Level Models

**Best: `metafor` (rma.mv())**

**Why**: Handles dependent effect sizes (multiple outcomes per study, nested trials) with flexible random-effects structures. Pair with `clubSandwich` for robust variance estimation.

```r
library(metafor)
library(clubSandwich)

# Three-level model (outcomes nested within studies)
res_ml <- rma.mv(
  yi, vi,
  random = ~ 1 | study_id/outcome_id,  # Nested structure
  data = es
)

# Robust variance estimation
coef_test(res_ml, vcov = "CR2")  # Cluster-robust SE
```

#### Package Comparison

| Package                        | Strengths                                                                                | Weaknesses                      |
| ------------------------------ | ---------------------------------------------------------------------------------------- | ------------------------------- |
| **metafor** + **clubSandwich** | `rma.mv()` for multilevel models, `clubSandwich::coef_test()` for robust SE, well-tested | Frequentist only                |
| **robumeta**                   | Simple RVE (robust variance estimation) interface, good for hierarchical data            | Less flexible than metafor      |
| **brms**                       | Bayesian multilevel models, non-linear effects, priors                                   | Slower, requires MCMC expertise |

**Recommendation**: Use `metafor::rma.mv()` + `clubSandwich` for most multilevel meta-analyses

---

### 8. Network Meta-Analysis

**Best: `netmeta` (frequentist) or `gemtc` (Bayesian)**

**Why**: `netmeta` is fast and produces automatic network plots. `gemtc` offers Bayesian inference with prior flexibility.

```r
# Frequentist network meta-analysis
library(netmeta)
net <- netmeta(
  TE, seTE, treat1, treat2, studlab,
  data = network_data,
  sm = "RR"
)
netgraph(net)  # Network plot
forest(net)    # Forest plot by comparison

# Bayesian network meta-analysis
library(gemtc)
network <- mtc.network(data.ab = network_data)
model <- mtc.model(network, type = "consistency")
results <- mtc.run(model)
```

#### Package Comparison

| Package      | Strengths                                                                         | Weaknesses                           |
| ------------ | --------------------------------------------------------------------------------- | ------------------------------------ |
| **netmeta**  | Fast frequentist NMA, automatic network graphs, league tables, ranking (P-scores) | No Bayesian inference                |
| **gemtc**    | Bayesian NMA with JAGS, prior flexibility, inconsistency models                   | Slower (MCMC), requires JAGS install |
| **multinma** | Modern Bayesian NMA with Stan, IPD + aggregate data integration                   | Newer package, fewer tutorials       |
| **bnma**     | Bayesian NMA with contrast-based or arm-based models                              | Less active development              |

**Recommendation**:

- **For frequentist NMA**: Use `netmeta`
- **For Bayesian NMA**: Use `gemtc` (mature) or `multinma` (modern)

---

### 9. Reporting & Reproducibility

**Best: `PRISMA2020` for flow diagrams, `metafor` for integrated reporting**

**Why**: Standardized reporting is essential for meta-analysis. Combine PRISMA diagrams, Rmarkdown/Quarto manuscripts, and reproducible analysis scripts.

#### Tool Comparison

| Tool                  | What it does                                                                             |
| --------------------- | ---------------------------------------------------------------------------------------- |
| **PRISMA2020**        | Generate PRISMA 2020 flow diagrams from R objects (replaces PRISMAstatement)             |
| **Rmarkdown/Quarto**  | Reproducible manuscripts with embedded R code, citations, cross-references               |
| **apaTables**         | APA-formatted regression tables (not meta-specific but useful)                           |
| **papaja**            | APA manuscripts with integrated R analysis (psychology focus)                            |
| **metafor** reporting | Built-in functions: `confint()`, `forest()`, `funnel()`, `regtest()` with export options |

**Example Workflow**:

````r
# PRISMA flow diagram
library(PRISMA2020)
prisma_flow <- PRISMA_flowdiagram(
  identified = 1500,
  screened = 800,
  eligible = 50,
  included = 25
)

# Quarto manuscript with integrated analysis
# In .qmd file:
# ```{r}
# library(metafor)
# res <- rma(yi, vi, data = es)
# forest(res)
# ```
````

**Recommendation**:

- Use **PRISMA2020** for flow diagrams
- Use **Quarto** for reproducible manuscripts
- Use **metafor** built-in reporting functions for tables/figures

---

## Installation

### The Recommended Stack (Start Here)

**For 95% of meta-analyses, install these 5 packages:**

```r
# The Typical Stack (covers ~80% of needs)
install.packages(c(
  "metafor",        # Core: effect sizes, models, heterogeneity, meta-regression
  "meta",           # Quick forest plots for simple RCTs
  "dmetar",         # Publication bias helpers (p-curve, etc.)
  "clubSandwich",   # Robust variance for multilevel models
  "PublicationBias" # Sensitivity analyses
))
```

**Why this combination?**

- `metafor` handles 80% of analysis tasks
- `meta` adds quick visualization (+10%)
- `dmetar` + `PublicationBias` cover publication bias (+5%)
- `clubSandwich` enables advanced multilevel models (+3%)
- **Total**: ~95-98% of typical workflows

### Optional: Advanced Packages

```r
# Advanced forest plots
install.packages("forestplot")

# Alternative multilevel
install.packages("robumeta")      # Alternative RVE

# Network meta-analysis
install.packages("netmeta")       # Frequentist NMA
install.packages("gemtc")         # Bayesian NMA (requires JAGS)
install.packages("multinma")      # Modern Bayesian NMA (requires Stan)

# Bayesian meta-analysis
install.packages("brms")          # Requires Stan
install.packages("MCMCglmm")      # Alternative Bayesian

# Reporting
install.packages("PRISMA2020")    # PRISMA flow diagrams
install.packages("quarto")        # Reproducible manuscripts
```

---

## Common Scenarios

### Scenario 1: Simple RCT Meta-Analysis (Binary Outcome)

**Use: `meta` package**

```r
library(meta)

# Simple interface
res <- metabin(
  event.e = events_ici,
  n.e = total_ici,
  event.c = events_control,
  n.c = total_control,
  data = data,
  studlab = study_id,
  sm = "RR",
  method = "MH"
)

# Auto-generate forest plot
forest(res)
```

**Why meta not metafor**: Simpler syntax, automatic forest plots, perfect for straightforward RCT meta-analysis.

---

### Scenario 2: Complex Meta-Analysis (Multilevel, Meta-Regression)

**Use: `metafor` package**

```r
library(metafor)

# Calculate effect sizes
es <- escalc(measure = "RR",
             ai = events_ici, n1i = total_ici,
             ci = events_control, n2i = total_control,
             data = data)

# Multilevel model (trials nested within studies)
res <- rma.mv(
  yi, vi,
  random = ~ 1 | study_id/trial_id,
  data = es
)

# Meta-regression with covariates
res_mr <- rma(
  yi, vi,
  mods = ~ age + pdl1_status,
  data = es
)
```

**Why metafor not meta**: Supports multilevel models, meta-regression, multiple tau² estimators.

---

### Scenario 3: Comprehensive Publication Bias Assessment

**Use: `metafor` + `dmetar` + `PublicationBias`**

```r
library(metafor)
library(dmetar)
library(PublicationBias)

# Fit model
res <- rma(yi, vi, data = es)

# 1. Visual inspection
funnel(res)

# 2. Statistical tests
regtest(res)  # Egger's test

# 3. Trim-and-fill
trimfill(res)

# 4. P-curve
pcurve(res)

# 5. Sensitivity analysis (PublicationBias)
# (See PublicationBias documentation)
```

---

## Package Documentation

### Core Packages

- **metafor**: https://www.metafor-project.org/
  - Most comprehensive documentation
  - 100+ pages of tutorials
  - Extensively validated

- **meta**: https://cran.r-project.org/web/packages/meta/
  - Simpler interface
  - Good for beginners
  - Excellent vignettes

### Specialized Packages

- **dmetar**: https://dmetar.protectlab.org/
  - Companion to "Doing Meta-Analysis in R" book
  - Helper functions built on meta/metafor

- **PublicationBias**: https://cran.r-project.org/web/packages/PublicationBias/
  - Mathur & VanderWeele methods
  - Sensitivity analysis tools

- **weightr**: https://cran.r-project.org/web/packages/weightr/
  - Vevea-Hedges selection models

---

## Tau² Estimators

When using `metafor`, you can choose from 10+ tau² estimators:

| Estimator | When to use               | Code              |
| --------- | ------------------------- | ----------------- |
| **REML**  | Default, most reliable    | `method = "REML"` |
| **DL**    | Older studies, comparison | `method = "DL"`   |
| **PM**    | Alternative to REML       | `method = "PM"`   |
| **ML**    | Maximum likelihood        | `method = "ML"`   |

**Recommendation**: Use REML (Restricted Maximum Likelihood) unless you have specific reason otherwise.

```r
# Compare tau² estimators
res_reml <- rma(yi, vi, data = es, method = "REML")
res_dl <- rma(yi, vi, data = es, method = "DL")
res_pm <- rma(yi, vi, data = es, method = "PM")

# Compare results
rbind(
  REML = c(tau2 = res_reml$tau2, I2 = res_reml$I2),
  DL = c(tau2 = res_dl$tau2, I2 = res_dl$I2),
  PM = c(tau2 = res_pm$tau2, I2 = res_pm$I2)
)
```

---

## Decision Flowchart

```
Start: What's your analysis?
├─ Simple RCT (binary/continuous)
│  └─ Use meta (metabin, metacont)
│
├─ Need multilevel models (dependent effect sizes)?
│  └─ Use metafor (rma.mv) + clubSandwich
│
├─ Need meta-regression (moderators)?
│  └─ Use metafor (rma with mods)
│
├─ Need network meta-analysis (multiple treatments)?
│  ├─ Frequentist → Use netmeta
│  └─ Bayesian → Use gemtc or multinma
│
├─ Need Bayesian inference (priors, non-linear)?
│  └─ Use brms
│
├─ Need custom forest plot?
│  ├─ Quick → Use meta::forest()
│  └─ Custom → Use metafor::forest() or forestplot
│
├─ Need specific tau² estimator?
│  └─ Use metafor (rma with method)
│
├─ Publication bias assessment?
│  └─ Use metafor + dmetar + PublicationBias
│
└─ Need PRISMA flow diagram?
   └─ Use PRISMA2020 package
```

---

## Common Mistakes

### ❌ Don't: Use compute.es

**Why**: No longer actively maintained, outdated.

**Do instead**: Use `metafor::escalc()` or `esc` package.

### ❌ Don't: Use rmeta

**Why**: Outdated, limited features, superseded by meta and metafor.

**Do instead**: Use `meta` or `metafor`.

### ❌ Don't: Use only funnel plot for publication bias

**Why**: Visual inspection alone is insufficient.

**Do instead**: Combine multiple methods:

- Funnel plot (visual)
- Egger's test (statistical)
- Trim-and-fill (correction)
- P-curve (alternative)

---

## Quick Reference

```r
# === EFFECT SIZE CALCULATION ===
library(metafor)
es <- escalc(measure = "RR", ai, n1i, ci, n2i, data = data)

# === MODEL FITTING ===
# Simple
library(meta)
res <- metabin(event.e, n.e, event.c, n.c, data = data)

# Complex
library(metafor)
res <- rma(yi, vi, data = es, method = "REML")

# === HETEROGENEITY ===
print(res)        # Q, I², H², tau²
confint(res)      # CI for tau²
predict(res)      # Prediction interval

# === PUBLICATION BIAS ===
funnel(res)       # Visual
regtest(res)      # Egger's test
trimfill(res)     # Trim-and-fill
```

---

## See Also

- [01-forest-plots.md](01-forest-plots.md) - Create forest plots with meta/metafor
- [02-funnel-plots.md](02-funnel-plots.md) - Publication bias assessment
- [03-subgroup-plots.md](03-subgroup-plots.md) - Subgroup and meta-regression analysis
- [00-setup.md](00-setup.md) - Package installation

---

## Summary Verdict

**metafor is the backbone of meta-analysis in R**

It covers ~80% of what you need. Supplement with:

- **meta** for quick forest plots
- **dmetar** for convenient bias tools
- **PublicationBias** for sensitivity analyses
- **clubSandwich** for robust variance
- **netmeta/gemtc** for network meta-analysis

### The Recommended Stack

**For 95% of meta-analyses:**

```r
# The Typical Stack
metafor + meta + dmetar + clubSandwich + PublicationBias
```

**Installation (one command):**

```r
install.packages(c("metafor", "meta", "dmetar", "clubSandwich", "PublicationBias"))
```

### Use Cases by Complexity

| Complexity   | Packages Needed                                       | Coverage |
| ------------ | ----------------------------------------------------- | -------- |
| **Simple**   | `meta` (metabin, metacont) + `metafor` (effect sizes) | 90%      |
| **Standard** | Add `dmetar` + `PublicationBias` for publication bias | 95%      |
| **Advanced** | Add `clubSandwich` for multilevel models              | 98%      |
| **Network**  | Add `netmeta` (frequentist) or `gemtc` (Bayesian)     | 99%      |
| **Bayesian** | Add `brms` for full Bayesian inference                | 99.5%    |

### The 80/20 Rule

**Core Stack (80% of analyses)**:

- `metafor` - Effect sizes, models, heterogeneity, meta-regression
- `meta` - Quick forest plots for simple RCTs

**Essential Supplements (90-95% of analyses)**:

- `dmetar` - Helper functions and p-curve
- `clubSandwich` - Robust variance for multilevel models
- `PublicationBias` - Sensitivity analyses

**Advanced Extensions (95-99% of analyses)**:

- `netmeta`/`gemtc` - Network meta-analysis
- `PRISMA2020` - Flow diagrams
- `brms` - Bayesian inference

---

**Key Takeaway**:

**Start with the recommended stack:**

```r
metafor + meta + dmetar + clubSandwich + PublicationBias
```

This covers ~95% of meta-analysis workflows. Add specialized packages (netmeta, brms, PRISMA2020) only when needed for specific analyses.
