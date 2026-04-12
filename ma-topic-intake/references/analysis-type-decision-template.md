# Analysis Type Decision Log

**Project**: [project-name]
**Created**: [date]
**Last Updated**: [date]

---

## Stage 1: Preliminary Assessment (Protocol Phase)

**Decision**: `pairwise` | `nma_candidate`
**Date**: [date]
**Basis**: Treatment count from TOPIC.txt / PICO

| Criterion | Value | Notes |
|-----------|-------|-------|
| Distinct treatments | [N] | List: [treatment1, treatment2, ...] |
| Common comparator exists | Yes/No/Unknown | [e.g., placebo, standard care] |
| Head-to-head trials expected | Yes/No/Unknown | |
| Initial recommendation | pairwise / nma_candidate | |

**Rationale**: [1-2 sentences]

> **Note**: If `nma_candidate`, this must be confirmed after screening (Stage 2 below).

---

## Stage 2: Confirmation Gate (Post-Screening / Post-Extraction)

**Triggered at**: `03_screening` | `05_extraction`
**Date**: [date]

### 2a. Study Design Profile

| Study Design | Count | % of Total |
|-------------|-------|------------|
| RCT (head-to-head) | | |
| RCT (vs placebo/control) | | |
| Single-arm trial | | |
| Observational (comparative) | | |
| Observational (single-arm) | | |
| **Total** | | 100% |

**Comparative study proportion**: [X]% (target: >70% for NMA)

### 2b. Network Connectivity

- [ ] Common comparator identified: [name]
- [ ] Network is connected (no isolated nodes)
- [ ] ≥2 studies per comparison (for key comparisons)
- [ ] Network geometry sketch:

```
Treatment A ---[N studies]--- Placebo ---[N studies]--- Treatment B
                                |
                           [N studies]
                                |
                           Treatment C
```

### 2c. Transitivity Assessment

Transitivity requires that study populations across different comparisons are similar enough that patients could, in principle, have been randomized to any of the treatments.

| Factor | Comparison 1 vs 2 | Comparison 1 vs 3 | Comparison 2 vs 3 | Concern |
|--------|-------------------|-------------------|-------------------|---------|
| Age range | | | | Low/Mod/High |
| Disease stage | | | | Low/Mod/High |
| Line of therapy | | | | Low/Mod/High |
| ECOG/PS | | | | Low/Mod/High |
| Prior treatments | | | | Low/Mod/High |
| Biomarker status | | | | Low/Mod/High |
| Geographic region | | | | Low/Mod/High |

**Overall transitivity**: Plausible / Uncertain / Implausible

### 2c-bis. CNMA Suitability (If Combination Treatments Exist)

> Complete this section only if the network includes combination therapies (e.g., "ACEI+ARB", "Chemo+Immuno"). Skip if all treatments are single-component.

| Criterion | Value | Notes |
|-----------|-------|-------|
| Combination treatments present in network | Yes/No | List: [e.g., ACEI+ARB, Chemo+Immuno] |
| Components identifiable from treatment labels | Yes/No | Can each treatment be decomposed into named components? |
| Additivity assumption clinically plausible | Yes/No/Uncertain | Are component effects likely independent? |
| Disconnected network that CNMA could reconnect | Yes/No | Does standard NMA fail due to disconnection? |
| ≥3 studies involving combination treatments | Yes/No | Sufficient data for component estimation? |

**CNMA recommendation**: Run nma_11_cnma.R / Skip CNMA

**Rationale**: [1-2 sentences on whether CNMA adds value for this network]

---

### 2d. Decision Matrix

| Criterion | Threshold | Actual | Pass? |
|-----------|-----------|--------|-------|
| Comparative study proportion | >70% | [X]% | Y/N |
| Network connected | Yes | | Y/N |
| ≥2 studies per key comparison | Yes | | Y/N |
| Transitivity plausible | Yes/Uncertain | | Y/N |
| Total included studies | ≥10 for NMA | [N] | Y/N |

**Pass count**: [X]/5

### 2e. Confirmed Decision

| Criteria Met | Decision | Action |
|-------------|----------|--------|
| 5/5 | **NMA confirmed** | Proceed with `ma-network-meta-analysis` |
| 4/5 (transitivity uncertain) | **NMA with sensitivity** | NMA + pairwise sensitivity analysis |
| 3/5 | **Downgrade to pairwise** | Use direct comparisons only |
| ≤2/5 or mostly single-arm | **Alternative analysis** | See options below |

**Final decision**: `nma` | `pairwise` | `pooled_proportion` | `narrative`

**Rationale**: [2-3 sentences explaining the confirmation or change]

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
| [date] | Preliminary | — | [decision] | Initial assessment from PICO |
| [date] | Confirmation | [preliminary] | [confirmed] | [reason for change or confirmation] |
