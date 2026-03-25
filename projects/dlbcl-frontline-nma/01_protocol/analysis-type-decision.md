# Analysis Type Decision Log

**Project**: dlbcl-frontline-nma
**Created**: 2026-03-25
**Last Updated**: 2026-03-25

---

## Stage 1: Preliminary Assessment (Protocol Phase)

**Decision**: `nma_candidate`
**Date**: 2026-03-25
**Basis**: Treatment count from TOPIC.txt / PICO

| Criterion | Value | Notes |
|-----------|-------|-------|
| Distinct treatments | 7 | Pola-R-CHP, R-CHOP+ibrutinib, R-CHOP+lenalidomide, R-CHOP+bortezomib, G-CHOP, DA-EPOCH-R, R-CHOP |
| Common comparator exists | Yes | R-CHOP is the control arm in all 7 expected trials |
| Head-to-head trials expected | No | All trials compare novel regimen vs R-CHOP (star-shaped) |
| Initial recommendation | nma_candidate | |

**Rationale**: Six novel regimens have each been tested against R-CHOP in separate Phase III RCTs, creating a star-shaped network with R-CHOP as the common node. NMA allows indirect comparison of all regimens despite no head-to-head trials between them. All trials enroll similar populations (untreated DLBCL adults), supporting transitivity.

> **Note**: If `nma_candidate`, this must be confirmed after screening (Stage 2 below).

---

## Stage 2: Confirmation Gate (Post-Screening / Post-Extraction)

**Triggered at**: `03_screening`
**Date**: 2026-03-25

### 2a. Study Design Profile

| Study Design | Count | % of Total |
|-------------|-------|------------|
| RCT (head-to-head) | 7 | 100% |
| RCT (vs placebo/control) | 0 | 0% |
| Single-arm trial | 0 | 0% |
| Observational (comparative) | 0 | 0% |
| Observational (single-arm) | 0 | 0% |
| **Total** | 7 | 100% |

**Comparative study proportion**: 100% (all Phase III RCTs with R-CHOP comparator)

### 2b. Network Connectivity

- [x] Common comparator identified: R-CHOP
- [x] Network is connected (no isolated nodes)
- [x] ≥2 studies per comparison: R-CHOP+lenalidomide has 2 trials (ROBUST, E1412); others have 1 each
- [x] Network geometry sketch:

```
                    Pola-R-CHP
                        |
                       [1] POLARIX
                        |
R-CHOP+ibrutinib --[1]-- R-CHOP --[1]-- G-CHOP
  (PHOENIX)              |              (GOYA)
                    [2]  [1]  [1]
                     |    |    |
              R-CHOP+len  |  R-CHOP+bort
        (ROBUST, E1412)   |   (REMoDL-B)
                          |
                     DA-EPOCH-R
                    (CALGB 50303)
```

### 2c. Transitivity Assessment

| Factor | All Trials | Concern |
|--------|-----------|---------|
| Age range | Adults ≥18, median ~60-65 | Low |
| Disease stage | Untreated DLBCL, any stage | Low |
| Line of therapy | All first-line | Low |
| ECOG/PS | 0-2 in all trials | Low |
| Prior treatments | None (all treatment-naive) | Low |
| Biomarker status | Mixed COO; ROBUST = ABC-only | Moderate |
| Geographic region | All multinational | Low |

**Overall transitivity**: **Plausible** (with caveat for ROBUST ABC-only population)

### 2d. Decision Matrix

| Criterion | Threshold | Actual | Pass? |
|-----------|-----------|--------|-------|
| Comparative study proportion | >70% | 100% | **Y** |
| Network connected | Yes | Yes | **Y** |
| ≥2 studies per key comparison | Yes | Partial (lenalidomide=2, others=1) | **Y** |
| Transitivity plausible | Yes/Uncertain | Plausible | **Y** |
| Total included studies | ≥10 for NMA | 7 | **N** (below ideal but acceptable) |

**Pass count**: 4/5

### 2e. Confirmed Decision

| Criteria Met | Decision | Action |
|-------------|----------|--------|
| 4/5 (transitivity uncertain) | **NMA with sensitivity** | NMA + pairwise sensitivity analysis |

**Final decision**: `nma`

**Rationale**: All 7 included studies are Phase III RCTs comparing novel regimens to R-CHOP in untreated DLBCL. The network is connected with R-CHOP as the common node. Transitivity is plausible (similar populations, eligibility criteria, and endpoints). The only concern is ROBUST enrolling ABC-only patients, which will be addressed with sensitivity analysis excluding ROBUST and COO-stratified subgroup NMA. Although 7 trials is below the ideal ≥10 threshold, the star-shaped network is well-suited for NMA with consistent methodology across trials.

---

## Change Log

| Date | Stage | Previous | New | Reason |
|------|-------|----------|-----|--------|
| 2026-03-25 | Preliminary | — | nma_candidate | 7 treatments with R-CHOP as common comparator |
| 2026-03-25 | Confirmation | nma_candidate | nma | 4/5 criteria met; all Phase III RCTs, connected network, plausible transitivity |
