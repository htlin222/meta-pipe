# Network Meta-Analysis: When and Why

**Time**: 10 minutes
**Purpose**: Decide whether your research question requires NMA or standard pairwise MA

---

## What is Network Meta-Analysis?

Network meta-analysis (NMA), also called mixed-treatment comparison (MTC), simultaneously compares **three or more treatments** using both:

- **Direct evidence**: Head-to-head comparisons from trials
- **Indirect evidence**: Inferred comparisons through a common comparator

Example: If trials compare A vs B and B vs C, NMA can estimate the A vs C effect indirectly through B.

---

## Decision Criteria

### Use NMA when ALL of these apply:

1. **≥3 distinct treatments** are being compared
2. **Connected network**: At least one path of evidence connects all treatments
3. **Transitivity assumption is plausible**: Study populations, designs, and effect modifiers are sufficiently similar across comparisons
4. **Clinical question demands ranking**: Decision-makers need to know which treatment is "best"

### Use standard pairwise MA when:

1. Only **2 treatments** are compared (intervention vs control)
2. Network would be **disconnected** (isolated treatment comparisons)
3. Treatments are too **heterogeneous** to assume transitivity
4. Research question is about a **single specific comparison**, not ranking

---

## Decision Flowchart

```
How many treatments?
├─ 2 treatments → Standard pairwise MA (ma-meta-analysis)
└─ ≥3 treatments
   ├─ Are all treatments connected? (shared comparators)
   │  ├─ No → Can CNMA reconnect via shared components?
   │  │  ├─ Yes → Component NMA (nma_11_cnma.R) — additive model
   │  │  └─ No → Cannot do NMA. Consider separate pairwise MAs
   │  └─ Yes
   │     ├─ Is transitivity plausible?
   │     │  ├─ No → Discuss limitations; consider sensitivity analyses
   │     │  └─ Yes → Network Meta-Analysis (ma-network-meta-analysis)
   │     ├─ Do combination treatments exist?
   │     │  ├─ Yes → Run CNMA extension (nma_11_cnma.R) after standard NMA
   │     │  └─ No → Standard NMA sufficient
   │     └─ Do you need treatment rankings?
   │        ├─ Yes → NMA with SUCRA rankings (Bayesian)
   │        └─ No → NMA still valid for indirect comparisons
```

---

## Key Differences from Pairwise MA

| Aspect | Pairwise MA | Network MA |
|--------|------------|------------|
| Comparisons | A vs B only | A vs B vs C vs D... |
| Evidence | Direct only | Direct + indirect |
| Assumptions | Homogeneity | Homogeneity + transitivity + consistency |
| Key output | Pooled effect (1 comparison) | League table (all pairwise comparisons) |
| Rankings | Not applicable | SUCRA + rankograms (Bayesian) |
| Certainty | GRADE | CINeMA (GRADE for NMA) |
| Reporting | PRISMA 2020 | PRISMA-NMA extension |
| Primary R package | meta/metafor | gemtc (Bayesian) |
| Sensitivity R package | — | netmeta (frequentist) |

---

## 2026 Methodological Consensus

### Bayesian as Primary Analysis

NICE, WHO, and Cochrane methodological guidelines use Bayesian NMA as their framework. Most PRISMA-NMA reporting examples are Bayesian. Reviewers expect Bayesian NMA — using frequentist as primary occasionally triggers requests for Bayesian sensitivity analysis. Starting with Bayesian avoids this.

### Empirical Priors Are Mature

Turner et al. and Rhodes et al. established empirical priors for different outcome types (OR, HR, MD) that are widely accepted. You can cite them directly without needing to justify the prior choice. Vague priors also work — results will closely match frequentist estimates.

### Frequentist as Supplement

Run `netmeta` once and place results in the supplement. If results agree with Bayesian (they almost always will), one sentence establishes robustness. Reviewers have no room for objection.

### CINeMA is Non-Negotiable

CINeMA (Confidence in Network Meta-Analysis) is the GRADE framework adapted for NMA. It rates certainty of evidence for each comparison across 6 domains. Omitting CINeMA is a common reason for reviewer rejection in 2026.

---

## Top Reviewer Rejection Reasons (2026)

Ranked by frequency:

1. **Inconsistency handling inadequate** — Must use ≥2 methods (node-splitting + global test)
2. **Transitivity assumption not justified** — Need table of study characteristics by comparison with explicit narrative
3. **CINeMA / GRADE for NMA not done** — Rate certainty per comparison
4. **Method choice issues** — Using Bayesian primary eliminates this concern entirely

Spend your time on items 1-3, not agonizing over Bayesian vs frequentist.

---

## The Three NMA Assumptions

### 1. Homogeneity
Same as pairwise MA: studies within each comparison are sufficiently similar.

### 2. Transitivity
Study characteristics that modify the treatment effect are balanced across comparisons. If A vs B studies enroll younger patients than B vs C studies, indirect estimates of A vs C may be biased.

### 3. Consistency
Direct and indirect evidence for the same comparison agree. Tested statistically via node-splitting and design decomposition.

See [nma-assumptions.md](nma-assumptions.md) for detailed assessment methods.

---

## Pipeline Integration

When `analysis_type: nma` is set in `pico.yaml`:

1. **Extraction** (Stage 05): Include `treat1`, `treat2` columns for each comparison
2. **Analysis** (Stage 06): Use `nma_*.R` scripts — Bayesian primary (gemtc), frequentist sensitivity (netmeta)
3. **CINeMA** (Stage 06): Rate certainty for all pairwise comparisons
4. **Manuscript** (Stage 07): Report per PRISMA-NMA checklist
5. **QA** (Stage 09): Verify convergence, consistency, CINeMA completion, PRISMA-NMA compliance

---

## CNMA Extension (Combination Therapies)

When your network includes **combination treatments** (e.g., Drug A + Drug B), Component NMA (CNMA) can:

1. **Decompose** combination effects into individual component contributions
2. **Test interactions** between components (synergy/antagonism)
3. **Reconnect disconnected networks** by assuming additive component effects

CNMA is run **after** the standard NMA workflow (nma_01–10) as an optional extension using `nma_11_cnma.R`.

- **Frequentist** (primary): `netmeta::discomb()` — the reference implementation
- **Bayesian** (sensitivity): `multinma::nma()` with component regression

See [CNMA Guide](cnma-guide.md) for detailed decision criteria, data requirements, and reporting.

---

## Advanced Extensions

| Extension | Script | When to Use |
|---|---|---|
| Component NMA (CNMA) | `nma_11_cnma.R` | Combination treatments in network |
| NMA Meta-Regression | `nma_12_meta_regression.R` | Study-level covariates available |
| Transitivity Testing | `nma_13_transitivity_tests.R` | Always (supplements clinical assessment) |

---

## Further Reading

- [NMA R Guide](nma-r-guide.md) — Step-by-step Bayesian NMA workflow with gemtc
- [NMA Assumptions](nma-assumptions.md) — How to assess transitivity and consistency
- [NMA Reporting Checklist](nma-reporting-checklist.md) — PRISMA-NMA 32-item checklist
- [Package Comparison](nma-package-comparison.md) — gemtc vs netmeta vs multinma
- [CNMA Guide](cnma-guide.md) — Component NMA for combination therapies
