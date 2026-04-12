# NMA R Packages: Comparison Guide

**Time**: 10 minutes
**Purpose**: Choose the right R package for your network meta-analysis

---

## Quick Decision

| Your Situation | Use This | Why |
|---------------|----------|-----|
| **Default NMA (recommended)** | **gemtc** (primary) + **netmeta** (sensitivity) | Bayesian primary per NICE/WHO/Cochrane; frequentist sensitivity in supplement |
| **CNMA (combination treatments)** | **netmeta::discomb()** (primary) + **multinma** (Bayesian sensitivity) | discomb() is the reference CNMA implementation; multinma adds Bayesian robustness |
| Need IPD + aggregate data | **multinma** | Modern Stan-based, handles both data types |
| No JAGS available | **netmeta** only | Fall back to frequentist if JAGS install not possible |
| Cochrane review | **gemtc** primary | Cochrane Handbook supports Bayesian NMA |

---

## 2026 Recommended Workflow

### Primary Analysis: gemtc (Bayesian)

**Why Bayesian first?**
- NICE, WHO, Cochrane guidelines are Bayesian-based
- Reviewers expect Bayesian NMA; frequentist-only may trigger requests for Bayesian sensitivity
- SUCRA + rankograms are the most familiar ranking presentation
- Empirical priors (Turner/Rhodes) are mature and widely accepted
- Formal model comparison via DIC
- Convergence diagnostics are standardized (Rhat, trace plots, ESS)

### Sensitivity: netmeta (Frequentist)

**Why include frequentist?**
- One run in supplement demonstrates robustness
- If results agree (almost always), one sentence handles it
- Fast to run, no convergence concerns
- Leaves reviewers with zero methodological objections

---

## Detailed Comparison

### gemtc (Bayesian) — PRIMARY

**Version**: Stable, well-established
**Authors**: van Valkenhoef, Kuiper
**Dependencies**: rjags, JAGS (external software required)

| Feature | Support |
|---------|---------|
| Contrast-based data | Yes |
| Arm-based data | Yes |
| Consistency model | Yes |
| Inconsistency model | Yes (unrelated mean effects) |
| Node-splitting | Yes (`mtc.nodesplit()`) |
| Rankings (SUCRA) | Yes (from posterior) |
| Rankograms | Yes (rank probability plots) |
| Prior specification | Yes (vague or empirical Turner/Rhodes) |
| Model comparison | DIC |
| Convergence diagnostics | Rhat, trace plots, ESS (via coda) |

**Strengths**:
- Full Bayesian inference with credible intervals
- Empirical priors available (Turner et al., Rhodes et al.) — cite directly
- SUCRA + rankograms produced naturally from posterior distributions
- Formal model comparison via DIC (random vs fixed)
- Matches NICE/WHO/Cochrane methodological expectations
- Well-established methodology with extensive literature

**Limitations**:
- Requires JAGS installation (C++ program, ~5 min setup)
- Slower than netmeta (MCMC sampling)
- Convergence must be verified (but this is standardized)

**Install**:
1. Install JAGS: https://mcmc-jags.sourceforge.io/
2. `install.packages(c("rjags", "gemtc", "coda"))`

**Empirical Priors (Turner/Rhodes)**:
```r
# Log-OR, pharmacological vs placebo, all-cause mortality
hn.prior <- mtc.hy.prior("dlnorm", -3.95, 1.79^(-2))

# Log-OR, pharmacological vs placebo, subjective outcomes
hn.prior <- mtc.hy.prior("dlnorm", -2.56, 1.74^(-2))

# Vague prior (results ≈ frequentist)
# Just use default — no prior specification needed
```

---

### netmeta (Frequentist) — SENSITIVITY

**Version**: Actively maintained (CRAN updated Jan 2026)
**Authors**: Rücker, Schwarzer, Krahn
**Dependencies**: meta (R only, no external software)

| Feature | Support |
|---------|---------|
| Contrast-based data | Yes |
| Arm-based data | Yes (via `pairwise()`) |
| Fixed-effect model | Yes |
| Random-effects model | Yes (REML, DL, PM, ML) |
| Network graph | `netgraph()` — built-in |
| Forest plots | `forest()` — built-in |
| League table | `netleague()` |
| Rankings (P-scores) | `netrank()` |
| Inconsistency tests | `decomp.design()`, `netsplit()`, `netheat()` |
| Funnel plot | `funnel.netmeta()` (comparison-adjusted) |
| Meta-regression | `netmetareg()` |

**Strengths**:
- No external dependencies (pure R)
- Fast execution (no MCMC)
- Comprehensive visualization (network graph, heat plot)
- P-scores as alternative to SUCRA
- Excellent for sensitivity analysis and visualization

**Limitations**:
- Frequentist only (no posterior distributions)
- No informative priors
- Some reviewers may request Bayesian analysis as supplement

**Install**: `install.packages("netmeta")`

---

### multinma (Bayesian, Modern) — ADVANCED

**Version**: Newer package (Stan backend)
**Authors**: Phillippo
**Dependencies**: Stan, rstan or cmdstanr

| Feature | Support |
|---------|---------|
| IPD + aggregate data | Yes (unique feature) |
| Population adjustment | Yes (MAIC, STC) |
| Meta-regression with IPD | Yes |
| Informative priors | Yes |
| Model comparison | LOO-IC, WAIC |

**Use when**: Combining individual patient data with aggregate data, or need population-adjusted indirect comparisons.

**Install**: `install.packages("multinma")` (requires rstan or cmdstanr)

---

## Feature Matrix

| Feature | gemtc | netmeta | multinma |
|---------|-------|---------|----------|
| **Role in pipeline** | **Primary** | **Sensitivity** | Advanced / CNMA Bayesian |
| Install difficulty | Medium (JAGS) | Easy | Hard (Stan) |
| Speed | Slow (MCMC) | Fast | Medium |
| Learning curve | Medium | Low | High |
| Framework | Bayesian | Frequentist | Bayesian |
| Rankings | SUCRA + rankogram | P-scores | SUCRA |
| Priors | Turner/Rhodes or vague | N/A | Flexible |
| Model comparison | DIC | — | LOO-IC |
| IPD support | No | No | Yes |
| **CNMA support** | No | **Yes (`discomb()`)** | **Yes (component regression)** |
| **NMA meta-regression** | No | **Yes (`netmetareg()`)** | Yes |
| Network visualization | Basic | Excellent | Basic |
| NICE/WHO alignment | Yes | Partial | Yes |
| External deps | JAGS | None | Stan |

---

## See Also

- [NMA R Guide](nma-r-guide.md) — Step-by-step Bayesian NMA workflow
- [NMA Overview](nma-overview.md) — When to use NMA vs pairwise
- [Package Selection](../../ma-meta-analysis/references/r-guides/09-package-selection.md) — Full R package guide (pairwise + NMA)
