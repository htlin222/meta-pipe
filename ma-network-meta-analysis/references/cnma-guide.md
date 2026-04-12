# Component Network Meta-Analysis (CNMA): Guide

**Time**: 15 minutes
**Purpose**: Understand when and how to use Component NMA for combination therapies
**Script**: `nma_11_cnma.R`

---

## What is CNMA?

Standard NMA treats each treatment as a single entity. Component NMA (CNMA) **decomposes multi-component treatments** into their individual parts and estimates the contribution of each component.

**Mathematical basis**: In the additive model, the effect of a combination treatment A+B is:

```
effect(A+B) = effect(A) + effect(B)
```

The interaction model relaxes this:

```
effect(A+B) = effect(A) + effect(B) + interaction(A,B)
```

---

## When to Use CNMA

Use CNMA when **any** of these apply:

1. **Combination therapies** exist in the network (e.g., ACEI+ARB, Chemo+Immuno, Drug A + Drug B)
2. **Disconnected network** that could be reconnected if treatments share components
3. You want to **estimate individual component contributions** to the combination effect
4. You want to **test for synergy or antagonism** between components

### Examples

| Clinical Scenario | Standard NMA | CNMA Advantage |
|---|---|---|
| ACEI vs ARB vs ACEI+ARB | Treats ACEI+ARB as opaque | Tests if ACEI+ARB > ACEI + ARB (interaction) |
| Chemo vs Immuno vs Chemo+Immuno | 3-node network | Decomposes into chemo effect + immuno effect |
| A vs B, C+B vs D (disconnected) | Cannot fit NMA | Additive model connects via shared component B |

---

## When NOT to Use CNMA

- **All treatments are single-component** — standard NMA is sufficient
- **Additivity is clearly implausible** — known strong synergy/antagonism between components (additivity assumption fails)
- **Fewer than 3 studies involving combinations** — insufficient data to estimate component effects
- **Components cannot be identified** — treatment mechanisms are not decomposable

---

## Data Requirements

### Treatment Naming Convention

Treatments must encode their components using `+` as separator:

| Treatment Label | Components |
|---|---|
| `ACEI` | ACEI |
| `ARB` | ARB |
| `ACEI+ARB` | ACEI, ARB |
| `Placebo` | (inactive reference) |
| `Chemo+Immuno+RT` | Chemo, Immuno, RT |

### Minimum Data

- At least **some studies** must compare combination treatments
- At least **some studies** must include single-component arms (for identifiability)
- The **inactive treatment** (reference) must be defined (typically placebo or standard care)

---

## Additive vs Interaction Model

### Decision Process

```
1. Fit additive model (no interaction)
   ↓
2. Fit interaction model (with interaction terms)
   ↓
3. Compare via Q-test (likelihood ratio)
   ├─ p > 0.05 → Additive model adequate (primary)
   └─ p < 0.05 → Interaction present (report interaction model)
```

### Additive Model

- **Assumption**: Components contribute independently
- **Advantage**: More parsimonious, fewer parameters, can reconnect disconnected networks
- **Report**: Component-level effect estimates with CIs

### Interaction Model

- **No additivity assumption**: Allows synergy (positive interaction) or antagonism (negative interaction)
- **Disadvantage**: More parameters, requires more data
- **Report**: Component effects + interaction terms

### Interpretation Guide

| Interaction Test | Meaning | Action |
|---|---|---|
| p > 0.10 | No interaction | Report additive model |
| 0.05 < p < 0.10 | Borderline | Report both; discuss |
| p < 0.05 | Significant interaction | Report interaction model; discuss clinical meaning |

---

## Reconnecting Disconnected Networks

CNMA's additive model can reconnect networks that would otherwise be disconnected in standard NMA:

```
Standard NMA (disconnected):
  A --- B           C --- D
  (no link between AB and CD sub-networks)

CNMA (reconnected via shared component):
  A --- B --- ? --- C --- D
  If B appears as a component in treatments on both sides,
  the additive model creates implicit connections.
```

### Caveats

- **Strong assumption**: Additivity must be clinically plausible
- **Always report** results WITH and WITHOUT disconnected treatments
- **Flag as sensitivity analysis**, not primary analysis
- **Discuss** why additivity is or isn't reasonable for your clinical context

---

## R Implementation

### Frequentist (Primary): `netmeta::discomb()`

```r
# Additive model
cnma_add <- discomb(TE, seTE, treat1, treat2, studlab,
                    data = nma_data, sm = "RR",
                    random = TRUE, inactive = "placebo")

# Interaction model
cnma_int <- discomb(TE, seTE, treat1, treat2, studlab,
                    data = nma_data, sm = "RR",
                    random = TRUE, inactive = "placebo",
                    C.matrix = "full")

# Forest plot of component effects
forest(cnma_add)

# Compare models
q_diff <- cnma_add$Q - cnma_int$Q
df_diff <- cnma_add$df.Q - cnma_int$df.Q
p_interaction <- pchisq(q_diff, df = df_diff, lower.tail = FALSE)
```

### Bayesian (Sensitivity): `multinma`

```r
library(multinma)

# Prepare data with component indicators
# Fit Bayesian CNMA with component regression terms
# See nma_11_cnma.R Section D for detailed template
```

### Why Frequentist Leads for CNMA

Unlike standard NMA where Bayesian (gemtc) is primary:

- `discomb()` is the **reference implementation** by Rücker et al. (2020)
- It is purpose-built for CNMA, while multinma uses general regression
- **No JAGS/Stan dependency** — easier to reproduce
- Bayesian CNMA via multinma is placed in supplement for robustness

---

## Reporting Checklist (CNMA-Specific Additions)

When reporting CNMA results, include these **in addition to** the standard NMA checklist:

- [ ] Component definitions: how treatments were decomposed
- [ ] Additive model results: component-level effect estimates with CIs
- [ ] Interaction test: Q-test results and interpretation
- [ ] Model comparison: standard NMA vs additive CNMA vs interaction CNMA (tau², I², Q)
- [ ] If network reconnected: explicit discussion of additivity assumption and its plausibility
- [ ] Bayesian concordance: multinma results in supplement (if available)

---

## Comparison: Standard NMA vs CNMA

| Aspect | Standard NMA | CNMA (Additive) | CNMA (Interaction) |
|---|---|---|---|
| Treatment model | Each treatment is unique | Treatments = sum of components | Components + interactions |
| Parameters | One per treatment pair | One per component | Components + interaction terms |
| Disconnected network | Cannot fit | May reconnect | May reconnect |
| Assumption | Consistency | Consistency + additivity | Consistency |
| Key output | League table | Component effects | Component + interaction effects |
| Package | `netmeta` / `gemtc` | `netmeta::discomb()` | `netmeta::discomb(C.matrix="full")` |

---

## References

- **Rücker G, Petropoulou M, Schwarzer G.** Network meta-analysis of multicomponent interventions. *Biom J.* 2020;62(3):808-821. doi:10.1002/bimj.201800167
- **Welton NJ, Caldwell DM, Adamopoulos E, Vedhara K.** Mixed treatment comparison meta-analysis of complex interventions: psychological interventions in coronary heart disease. *Am J Epidemiol.* 2009;169(9):1158-1165.
- **Phillippo DM.** multinma: Bayesian Network Meta-Analysis of Individual and Aggregate Data. R package.

---

## See Also

- [NMA Overview](nma-overview.md) — When to use NMA vs pairwise
- [NMA R Guide](nma-r-guide.md) — Step-by-step NMA workflow (Steps 11-13 cover CNMA)
- [NMA Assumptions](nma-assumptions.md) — Transitivity, consistency, homogeneity
- [NMA Completion Checklist](nma-completion-checklist.md) — Items 26-28 for CNMA
