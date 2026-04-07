# Pre-Pooling Assumption Checks for Pairwise Meta-Analysis

**Time**: ~5 min per outcome type | **Script**: `02a_pre_pool_diagnostics.R`

## Why Check Before Pooling?

A pooled estimate from a random-effects model is only meaningful when the included studies are estimating a *common underlying effect* that varies within a plausible range. When this assumption is severely violated, the pooled estimate:

- Obscures important clinical heterogeneity
- Gives false precision (narrow CI despite wide true variation)
- May not apply to any real clinical setting (the "average" of contradictory effects)
- Can mislead decision-makers who treat the single number as definitive

The Cochrane Handbook (§10.10.4) explicitly warns: *"When there is considerable variation in results, and particularly if there is inconsistency in the direction of effect, it may be misleading to quote an average value for the intervention effect."*

## Traffic-Light Advisory System

The `02a_pre_pool_diagnostics.R` script runs 5 checks and produces an overall advisory:

| Level | Meaning | Action |
|-------|---------|--------|
| **GREEN** | Assumptions reasonably met | Proceed with pooling |
| **YELLOW** | Moderate concerns | Pool with caution; always report prediction intervals; explore heterogeneity sources |
| **RED** | Major concerns | Pooled estimate may be misleading; consider narrative synthesis; must justify pooling |

**Overall level** = worst level across all individual checks.

## The 5 Diagnostic Checks

### 1. Study Count (k)

| Threshold | Level | Rationale |
|-----------|-------|-----------|
| k < 2 | RED | Cannot pool a single study |
| k = 2 | YELLOW | tau² is very poorly estimated with 2 studies; the random-effects model has minimal information to estimate between-study variance |
| k >= 3 | GREEN | Minimum for meaningful pooling |

**Note**: Even with k >= 3, all other checks still apply. A large k does not guarantee homogeneity.

### 2. Heterogeneity (I², Q-test, tau²)

A preliminary random-effects model (REML) is fitted to extract heterogeneity statistics.

| Threshold | Level | Rationale |
|-----------|-------|-----------|
| I² > 75% | RED | Substantial heterogeneity (Higgins & Thompson 2002); most variation is between-study, not sampling error |
| I² 50–75% | YELLOW | Moderate heterogeneity; pooled estimate is less reliable |
| I² < 50% | GREEN | Low to moderate heterogeneity |

**Important**: I² alone is insufficient. Always consider:
- **tau²** (absolute between-study variance) — clinically meaningful even if I² is moderate
- **Q-test p-value** — low power when k is small; non-significant Q does NOT prove homogeneity
- **Prediction interval** (see check 4) — the most informative measure of true variation

### 3. Prediction Interval

The 95% prediction interval estimates the range within which the true effect of a **future study** would likely fall (IntHout et al. 2016; Riley et al. 2011).

| Threshold | Level | Rationale |
|-----------|-------|-----------|
| Crosses null (0 for SMD/MD, 1 for RR/OR) | YELLOW | The true effect could go in either direction in a new setting |
| Does not cross null | GREEN | Effect direction is consistent across plausible settings |

**Why this matters**: A pooled RR of 0.70 with CI [0.55, 0.90] looks convincing. But if the prediction interval is [0.30, 1.60], a future study might find *no benefit or even harm*. The prediction interval reveals what the CI hides.

### 4. Effect Direction Consistency

Examines what proportion of studies show effects in the same direction.

| Threshold | Level | Rationale |
|-----------|-------|-----------|
| < 60% agreement | RED | Studies are nearly split — they may not be estimating the same effect |
| 60–75% agreement | YELLOW | Notable disagreement in direction |
| >= 75% agreement | GREEN | Reasonable directional consistency |

### 5. Outlier Detection

Externally studentized residuals (Viechtbauer & Cheung 2010) identify studies whose effect sizes are extreme relative to the model.

| Threshold | Level | Rationale |
|-----------|-------|-----------|
| Any |z| > 2 | YELLOW | Potential outlier — should be investigated in sensitivity analysis |
| None | GREEN | No extreme values detected |

**Note**: Requires k >= 3. Outliers are flagged for investigation, not automatic removal.

## What to Do at Each Level

### GREEN: Proceed

- Run `03_models.R` as normal
- Report pooled estimate with CI **and** prediction interval
- Continue with subgroup/sensitivity analyses as planned

### YELLOW: Proceed with Caution

- Run `03_models.R` — the pooled estimate is computed but flagged
- **Must report prediction interval** alongside CI in all outputs
- Prioritize heterogeneity exploration (subgroup analysis, meta-regression)
- Sensitivity analyses (leave-one-out, exclude outliers) are critical
- In the manuscript, explicitly discuss the limitations of pooling

### RED: Consider Alternatives

Before relying on the pooled estimate:

1. **Investigate heterogeneity sources** — can you identify clinical/methodological subgroups that explain the variation?
2. **Subgroup analysis first** — if subgroups are more homogeneous, pool within subgroups instead of overall
3. **Narrative synthesis** — if heterogeneity cannot be explained, describe individual study results qualitatively rather than forcing a single number
4. **If you still pool** — prominently display the prediction interval; clearly state that the pooled estimate should be interpreted with great caution; justify why pooling is still informative despite the concerns

## How It Integrates with the Pipeline

```
02_effect_sizes.R
       │
       ▼
02a_pre_pool_diagnostics.R  ──→  02a_diagnostics_report.md
       │                          (human-readable traffic light)
       │  pooling_advisory
       ▼  (R object)
03_models.R  ──→  Advisory-aware output with prediction intervals
       │
       ▼
04_subgroups_meta_regression.R  (explore heterogeneity sources)
       │
       ▼
07_sensitivity.R  (test robustness; exclude flagged outliers)
```

The `pooling_advisory` object flows through the R environment. Downstream scripts can access `pooling_advisory$overall` to adjust their behavior (e.g., adding caveats to figures, tables, and manuscript text).

## References

1. **Cochrane Handbook** §10.10.4 — "When heterogeneity cannot be explained"
2. **Higgins JPT, Thompson SG** (2002). Quantifying heterogeneity in a meta-analysis. *Stat Med* 21:1539-58. PMID: 12111919
3. **IntHout J, Ioannidis JPA, Rovers MM, Goeman JJ** (2016). Plea for routinely presenting prediction intervals in meta-analysis. *BMJ Open* 6:e010247. PMID: 27406637
4. **Riley RD, Higgins JPT, Deeks JJ** (2011). Interpretation of random effects meta-analyses. *BMJ* 342:d549. PMID: 21310794
5. **Viechtbauer W, Cheung MW-L** (2010). Outlier and influence diagnostics for meta-analysis. *Res Synth Methods* 1:112-25. PMID: 26061377
