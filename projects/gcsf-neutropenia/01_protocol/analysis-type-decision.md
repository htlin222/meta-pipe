# Analysis Type Decision Log

**Project**: gcsf-neutropenia
**Created**: 2026-03-24
**Last Updated**: 2026-03-24

---

## Stage 1: Preliminary Assessment (Protocol Phase)

**Decision**: `nma_candidate`
**Date**: 2026-03-24
**Basis**: Treatment count from TOPIC.txt / PICO

| Criterion | Value | Notes |
|-----------|-------|-------|
| Distinct treatments | 4 | Filgrastim, pegfilgrastim, lipegfilgrastim, placebo/no G-CSF |
| Common comparator exists | Yes | Placebo or no G-CSF prophylaxis serves as common comparator |
| Head-to-head trials expected | Yes | Multiple RCTs compare pegfilgrastim vs filgrastim directly (e.g., Green 2003, Holmes 2002) |
| Initial recommendation | nma_candidate | >= 3 active treatments plus common comparator |

**Rationale**: The research question involves three distinct G-CSF formulations (filgrastim, pegfilgrastim, lipegfilgrastim) all compared against placebo/no prophylaxis. Published literature includes both placebo-controlled trials for each agent and head-to-head trials (particularly pegfilgrastim vs filgrastim), suggesting a connected network is plausible. NMA would enable ranking of formulations and indirect comparisons where direct evidence is sparse (e.g., lipegfilgrastim vs filgrastim).

> **Note**: If `nma_candidate`, this must be confirmed after screening (Stage 2 below).

---

## Stage 2: Confirmation Gate (Post-Screening / Post-Extraction)

**Triggered at**: _pending_
**Date**: _pending_

### 2a. Study Design Profile

| Study Design | Count | % of Total |
|-------------|-------|------------|
| RCT (head-to-head) | | |
| RCT (vs placebo/control) | | |
| Single-arm trial | | |
| Observational (comparative) | | |
| Observational (single-arm) | | |
| **Total** | | 100% |

**Comparative study proportion**: _pending_ (target: >70% for NMA)

### 2b. Network Connectivity

- [ ] Common comparator identified: Placebo / no G-CSF
- [ ] Network is connected (no isolated nodes)
- [ ] >= 2 studies per comparison (for key comparisons)
- [ ] Network geometry sketch:

```
Filgrastim ---[N studies]--- Placebo/No G-CSF ---[N studies]--- Pegfilgrastim
                                    |
                               [N studies]
                                    |
                             Lipegfilgrastim
        Filgrastim ---[N studies]--- Pegfilgrastim
```

### 2c. Transitivity Assessment

Transitivity requires that study populations across different comparisons are similar enough that patients could, in principle, have been randomized to any of the treatments.

| Factor | Filgrastim vs Placebo | Pegfilgrastim vs Placebo | Lipegfilgrastim vs Placebo | Concern |
|--------|----------------------|-------------------------|---------------------------|---------|
| Age range | | | | Low/Mod/High |
| Disease stage | | | | Low/Mod/High |
| Line of therapy | | | | Low/Mod/High |
| ECOG/PS | | | | Low/Mod/High |
| Prior treatments | | | | Low/Mod/High |
| Biomarker status | | | | Low/Mod/High |
| Geographic region | | | | Low/Mod/High |

**Overall transitivity**: _pending_

### 2d. Decision Matrix

| Criterion | Threshold | Actual | Pass? |
|-----------|-----------|--------|-------|
| Comparative study proportion | >70% | _pending_ | |
| Network connected | Yes | _pending_ | |
| >= 2 studies per key comparison | Yes | _pending_ | |
| Transitivity plausible | Yes/Uncertain | _pending_ | |
| Total included studies | >= 10 for NMA | _pending_ | |

**Pass count**: _pending_/5

### 2e. Confirmed Decision

| Criteria Met | Decision | Action |
|-------------|----------|--------|
| 5/5 | **NMA confirmed** | Proceed with `ma-network-meta-analysis` |
| 4/5 (transitivity uncertain) | **NMA with sensitivity** | NMA + pairwise sensitivity analysis |
| 3/5 | **Downgrade to pairwise** | Use direct comparisons only |
| <= 2/5 or mostly single-arm | **Alternative analysis** | See options below |

**Final decision**: _pending_

**Rationale**: _pending_

---

## Alternative Analysis Options (if NMA not feasible)

| Scenario | Recommended Approach |
|----------|---------------------|
| Mostly single-arm, no comparators | Pooled proportion meta-analysis (event rates, response rates) |
| Some comparative + some single-arm | Pairwise MA (comparative subset) + pooled proportions (single-arm) |
| Comparative but disconnected network | Separate pairwise MAs per connected component |
| Comparative but transitivity violated | Pairwise MA + narrative comparison across treatments |
| Sparse network (<2 studies/comparison) | Pairwise MA for well-represented comparisons |
| Sufficient data, transitivity uncertain | NMA with MAIC/STC adjustment as sensitivity analysis |

---

## Change Log

| Date | Stage | Previous | New | Reason |
|------|-------|----------|-----|--------|
| 2026-03-24 | Preliminary | -- | nma_candidate | Initial assessment: 3 G-CSF formulations + placebo = 4 treatment nodes |
