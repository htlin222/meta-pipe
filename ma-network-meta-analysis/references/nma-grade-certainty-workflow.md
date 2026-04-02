# GRADE Certainty Assessment for NMA: Staged Workflow

**Reference**: Brignardello-Petersen R, et al. Advances in the GRADE approach to rate the certainty in estimates from a network meta-analysis. *J Clin Epidemiol*. 2018;93:36-44. doi: 10.1016/j.jclinepi.2017.10.005. PMID: 29051107.

**Complementary to**: CINeMA framework (Nikolakopoulou et al. BMJ 2020;371:m3983) — see `ma-peer-review/references/cinema-quick-reference.md`

---

## Core Concept: Certainty as a Continuum

Evidence certainty is best understood as a **continuum** (0-100), not merely four discrete levels (High/Moderate/Low/Very Low). Think of it as a visual analogue scale (VAS):

```
Very Low         Low            Moderate          High
|_________|_________|_____________|_______________|
0        25        50            75             100
```

**Clinical implication**: Even if direct evidence already achieves "high certainty" (e.g., VAS 80), incorporating coherent indirect evidence can push the network estimate to an even higher confidence (e.g., VAS 90) by narrowing the confidence interval. This means indirect evidence always has potential value, even when direct evidence is strong.

---

## Overview: 4-Stage Assessment Process

For **each pairwise comparison** in the network, follow these stages sequentially:

```
┌─────────────────────────────────────────────────┐
│  Stage 1: Assess DIRECT evidence                │
│  (RoB, inconsistency, indirectness, pub bias)   │
│  ⚠️ Do NOT assess imprecision yet               │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│  Stage 2: Efficiency Decision                   │
│  Direct = HIGH certainty?                       │
│  Direct contribution ≥ indirect contribution?   │
│  (Compare CI widths)                            │
└──────┬───────────────────────────┬──────────────┘
       │ BOTH Yes                  │ Either No
       ▼                           ▼
┌──────────────┐   ┌─────────────────────────────┐
│ Skip to      │   │  Stage 3: Assess INDIRECT   │
│ Stage 4      │   │  evidence                   │
│ (use direct  │   │  - Find first-order loop    │
│  certainty)  │   │  - Start from LOWEST        │
│              │   │    certainty in loop         │
│              │   │  - Evaluate intransitivity   │
└──────┬───────┘   └──────────────┬──────────────┘
       │                          │
       ▼                          ▼
┌─────────────────────────────────────────────────┐
│  Stage 4: Derive NETWORK ESTIMATE certainty     │
│  - Start from HIGHER of direct vs indirect      │
│  - Assess COHERENCE (local node-splitting!)     │
│  - Assess IMPRECISION (network CI, not          │
│    component CIs)                               │
│  - Final certainty rating                       │
└─────────────────────────────────────────────────┘
```

---

## Stage 1: Assess Direct Evidence (Without Imprecision)

For each pairwise comparison that has direct evidence, rate the following **four** domains:

| Domain | What to Assess | Judgment |
|--------|---------------|----------|
| **Risk of bias** | RoB 2 / ROBINS-I of contributing studies | No concerns / Some (-1) / Major (-2) |
| **Inconsistency** | Heterogeneity (I²) among direct studies | No concerns / Some (-1) / Major (-2) |
| **Indirectness** | PICO mismatch with target question | No concerns / Some (-1) / Major (-2) |
| **Publication bias** | Funnel plot, study registry checks | No concerns / Some (-1) / Major (-2) |

### What NOT to do at this stage

- **Do NOT assess imprecision**. The precision of the direct estimate alone is not the final precision — it will be redefined after combining with indirect evidence in the network estimate.
- **DO note the CI width** of the direct estimate. This is used in Stage 2 to judge the **contribution** of direct evidence relative to indirect evidence (narrower CI = greater contribution). This is an observational step, not a grading step.

### Output

A preliminary certainty rating for direct evidence (High / Moderate / Low / Very Low), based on 4 domains only.

---

## Stage 2: Efficiency Decision

This step allows researchers to **skip detailed indirect evidence assessment** when it would not change the conclusion. This is especially valuable in large networks with many comparisons.

### Two conditions must BOTH be met:

1. **Direct evidence has HIGH certainty** (after Stage 1, excluding imprecision) — i.e., no downgrades for RoB, inconsistency, indirectness, or publication bias.
2. **Direct evidence contribution ≥ indirect evidence contribution** — assessed by comparing CI widths:
   - If the direct estimate CI is **narrower** than (or equal to) the indirect estimate CI → direct evidence dominates
   - If the direct estimate CI is **wider** than the indirect estimate CI → indirect evidence dominates

### Decision:

- **Both conditions met** → Skip Stage 3. Proceed directly to Stage 4 using the direct evidence certainty as the starting point. (The indirect evidence cannot improve an already high-certainty, dominant direct estimate.)
- **Either condition NOT met** → Proceed to Stage 3 for full indirect evidence assessment.

### Practical tip

Compare CI widths from the node-splitting output (`netsplit()` in netmeta or `mtc.nodesplit()` in gemtc). The forest plot from `nma_05_inconsistency.R` displays direct and indirect estimates side by side.

---

## Stage 3: Assess Indirect Evidence

When direct evidence is insufficient, absent, or less influential than indirect evidence, a thorough assessment of indirect evidence is required.

### Step 3a: Identify the First-Order Loop

The **first-order loop** is the shortest indirect path connecting the two treatments. For comparison A vs C:

```
First-order loop:
  A ←── direct ──→ B ←── direct ──→ C
                    ↑
              (common comparator)
```

If multiple first-order loops exist, focus on the one that contributes most to the indirect estimate (typically the one with narrowest CIs in its component comparisons).

### Step 3b: Determine Starting Certainty

The starting certainty for indirect evidence is the **LOWEST** certainty rating among the direct comparisons that form the first-order loop.

**Example**: For indirect comparison A vs C via B:
- Direct A vs B certainty = High
- Direct B vs C certainty = Moderate (downgraded for RoB)
- → Indirect A vs C starting certainty = **Moderate** (the lower of the two)

**Rationale**: The indirect estimate is only as reliable as its weakest link.

### Step 3c: Evaluate Intransitivity

Intransitivity threatens the validity of indirect comparisons. Assess whether studies in the loop are sufficiently similar in:

- **Patient characteristics**: age, disease severity, comorbidities
- **Intervention details**: dose, duration, delivery method
- **Comparator attributes**: active control vs placebo, standard of care definitions
- **Effect modifiers**: any factor that could differentially affect treatment effects

| Finding | Action |
|---------|--------|
| Similar across loop comparisons | No further downgrade |
| Some differences in effect modifiers | Downgrade -1 (some concerns) |
| Major differences (e.g., early vs metastatic) | Downgrade -2 (major concerns) |

**Detailed guide**: See `ma-submission-prep/references/transitivity-guide.md`

### Step 3d: Compare Direct and Indirect Estimates

Before proceeding to Stage 4, note:
- The **certainty levels** of direct vs indirect evidence
- The **point estimates** — are they consistent in direction and magnitude?
- These observations inform the coherence assessment in Stage 4

### Output

A certainty rating for indirect evidence (High / Moderate / Low / Very Low).

---

## Stage 4: Derive Network Estimate Certainty

The network estimate combines direct and indirect evidence. Its certainty assessment is the final, clinically actionable output.

### Step 4a: Choose Starting Point

The starting certainty for the network estimate is the **HIGHER** of:
- Direct evidence certainty (from Stage 1)
- Indirect evidence certainty (from Stage 3)

**Rationale**: The network estimate benefits from the stronger evidence source. If direct evidence is moderate and indirect is low, start at moderate.

### Step 4b: Assess Coherence (Local Incoherence Testing)

Coherence (consistency) means that direct and indirect evidence agree. This is assessed via **local** node-splitting tests for each comparison.

**Methods**:
- **Node-splitting** (`netsplit()` in netmeta): Tests direct vs indirect for each specific comparison
- p > 0.10 → No concerns
- 0.05 < p ≤ 0.10 → Some concerns (consider downgrade -1)
- p ≤ 0.05 → Major concerns (downgrade -1 or -2)

#### Critical Warning About Global Tests

> **Do NOT rely on global incoherence tests** (Lu and Ades model, design-by-treatment interaction model) to assume coherence. These tests are **frequently underpowered** — a non-significant global p-value does NOT mean that local incoherence is absent. Significant local incoherence can hide within a non-significant global test.
>
> **Always perform local node-splitting** for each pairwise comparison, regardless of the global test result.

#### When Incoherence Is Detected

If direct and indirect estimates conflict:
1. **Downgrade** the network estimate for incoherence (-1 or -2)
2. **For clinical decisions**: Prefer the estimate with **higher certainty**
   - Example: Direct = Moderate certainty, Indirect = Very Low certainty
   - Even if network estimate is downgraded to Low, clinical decisions should weigh the direct estimate (Moderate) more heavily
3. **Report transparently**: Present direct, indirect, AND network estimates separately in the Summary of Findings table

### Step 4c: Assess Imprecision (NOW)

Imprecision is assessed **only at the network estimate level**, using the network estimate's own CI:

| Finding | Action |
|---------|--------|
| Network CI excludes clinically meaningful difference AND includes adequate sample | No concerns |
| Network CI crosses clinical decision threshold OR marginal sample size | Some concerns (-1) |
| Network CI very wide, spans both benefit and harm | Major concerns (-2) |

**Key principle**: Even if individual direct or indirect estimates were imprecise, the network estimate may achieve adequate precision through combination. Do NOT double-downgrade for imprecision that was already resolved by evidence synthesis.

### Step 4d: Final Certainty Rating

Apply any coherence and imprecision downgrades to the starting point (Step 4a):

```
Final certainty = max(direct, indirect) − coherence downgrade − imprecision downgrade
```

Report the final rating as: **High** / **Moderate** / **Low** / **Very Low**

---

## Worked Example

**Comparison**: Citalopram vs Escitalopram (from Brignardello-Petersen 2018)

### Stage 1: Direct Evidence
- 3 RCTs directly comparing citalopram and escitalopram
- RoB: No serious concerns
- Inconsistency: I² = 0%, no concerns
- Indirectness: No concerns
- Publication bias: No concerns
- **Direct certainty (without imprecision): HIGH**
- Note: Direct CI is relatively wide (few direct studies)

### Stage 2: Efficiency Decision
- Direct certainty = HIGH ✓
- Direct CI width vs indirect CI width: Direct CI is **wider** than indirect CI ✗
- Direct evidence does NOT dominate → Proceed to Stage 3

### Stage 3: Indirect Evidence
- First-order loop: Citalopram → Placebo → Escitalopram
- Citalopram vs Placebo certainty: Moderate (some RoB concerns)
- Escitalopram vs Placebo certainty: High
- **Indirect starting certainty: MODERATE** (lowest in loop)
- Intransitivity: Some differences in patient populations → Downgrade -1
- **Indirect certainty: LOW**

### Stage 4: Network Estimate
- Starting point: max(HIGH, LOW) = **HIGH**
- Coherence: Node-splitting p = 0.03 → Major concerns → Downgrade -1
- Imprecision: Network CI crosses clinical threshold → Downgrade -1
- **Network estimate certainty: LOW** (High − 1 − 1)

### Clinical Interpretation
Despite the network estimate being LOW certainty, the **direct estimate** (Moderate certainty after adding imprecision assessment) provides a more reliable basis for clinical decisions, because the incoherence suggests the indirect pathway introduces distortion.

---

## Relationship to CINeMA

| Aspect | CINeMA (Nikolakopoulou 2020) | Staged Workflow (Brignardello-Petersen 2018) |
|--------|------------------------------|----------------------------------------------|
| **Purpose** | Tool for operationalizing assessment | Conceptual framework for combining evidence |
| **Scope** | 6-domain rating per comparison | Sequential logic for direct → indirect → network |
| **Imprecision** | Assessed as domain 4 (flat) | Deferred to network estimate stage only |
| **Efficiency** | No shortcut mechanism | Formal 2-condition shortcut for high-certainty direct evidence |
| **Indirect evidence** | Contribution matrix informs weight | First-order loop + lowest certainty starting point |
| **Global tests** | Listed alongside local tests | Explicit warning about underpowered global tests |

**Use both together**: CINeMA provides the structured tool and domains; the staged workflow guides the order and logic of assessment. When using CINeMA web app, keep the staged workflow in mind to correctly sequence your judgments.

---

## Pipeline Integration

```bash
# Step 1: Generate node-splitting results (direct vs indirect comparison)
cd projects/<project-name>/06_analysis
Rscript nma_05_inconsistency.R
# → Outputs: netsplit forest plot, CI widths for direct and indirect

# Step 2: Generate contribution matrix
# In R: netcontrib(nma_model) from netmeta package
# Or use CINeMA web app (https://cinema.ispm.unibe.ch/)

# Step 3: Apply staged workflow per comparison
# Use this document as a checklist for each pairwise comparison

# Step 4: Record assessments
# Save to: 08_reviews/cinema_assessment.csv
# Include columns for: direct_certainty, indirect_certainty,
#   network_certainty, coherence_judgment, imprecision_judgment
```

---

## Quick Checklist (Per Comparison)

- [ ] Stage 1: Direct evidence rated on 4 domains (RoB, inconsistency, indirectness, publication bias)
- [ ] Stage 1: Imprecision NOT assessed yet (only CI width noted for contribution)
- [ ] Stage 2: Efficiency shortcut evaluated (both conditions checked)
- [ ] Stage 3: Indirect evidence rated from lowest certainty in first-order loop (if applicable)
- [ ] Stage 3: Intransitivity assessed for indirect pathway
- [ ] Stage 4: Starting point = higher of direct and indirect certainty
- [ ] Stage 4: Coherence assessed via LOCAL node-splitting (not just global test)
- [ ] Stage 4: Imprecision assessed using NETWORK estimate CI
- [ ] Stage 4: When incoherence detected, higher-certainty estimate noted for clinical decisions
- [ ] Final certainty rating recorded

---

## References

- Brignardello-Petersen R, Bonner A, Alexander PE, et al. Advances in the GRADE approach to rate the certainty in estimates from a network meta-analysis. *J Clin Epidemiol*. 2018;93:36-44. doi: 10.1016/j.jclinepi.2017.10.005. PMID: 29051107.
- Nikolakopoulou A, Higgins JPT, Papakonstantinou T, et al. CINeMA: An approach for assessing confidence in the results of a network meta-analysis. *PLoS Med*. 2020;17(4):e1003082.
- Puhan MA, Schünemann HJ, Murad MH, et al. A GRADE Working Group approach for rating the quality of treatment effect estimates from network meta-analysis. *BMJ*. 2014;349:g5630.

---

**See also**:
- `ma-peer-review/references/grade-assessment-guide.md` — CINeMA 6-domain details
- `ma-peer-review/references/cinema-quick-reference.md` — CINeMA practical quick reference
- `ma-submission-prep/references/transitivity-guide.md` — Intransitivity assessment guide
- `ma-network-meta-analysis/references/nma-completion-checklist.md` — Pre-submission checklist

**Last updated**: 2026-04-02
