# Decision Log

**Project**: dlbcl-frontline-nma
**Created**: 2026-03-25

---

## Decisions

### D001: Analysis Type — NMA Candidate (2026-03-25)
- **Decision**: Preliminary analysis type set to `nma_candidate`
- **Rationale**: ≥6 treatments, all compared against R-CHOP in Phase III RCTs
- **Status**: Awaiting confirmation after screening (Stage 3b)

### D002: Study Design Restriction — Phase III RCTs Only (2026-03-25)
- **Decision**: Exclude Phase II, single-arm, and observational studies
- **Rationale**: NMA requires randomized comparative data for valid indirect comparisons. Phase II data (COALITION, EPCORE NHL-2 Phase II) excluded due to lack of randomized R-CHOP comparator arm
- **Impact**: Limits to ~7-10 trials but ensures methodological rigor

### D003: ROBUST Trial Handling (2026-03-25)
- **Decision**: Include ROBUST in overall NMA; flag as ABC-only population
- **Rationale**: ROBUST enrolled only ABC/non-GCB DLBCL. It contributes to the lenalidomide node. Will be used directly in COO subgroup NMA. For overall NMA, note population restriction in sensitivity analysis.
- **Alternative considered**: Exclude ROBUST from overall NMA — rejected because it would leave only ECOG-E1412 for lenalidomide comparison

### D004: POLARIX Data Version (2026-03-25)
- **Decision**: Use 5-year data (JCO 2026) as primary; note 2-year data for sensitivity
- **Rationale**: Most mature follow-up available; aligns with updated effect estimates (PFS HR 0.77)

### D005: Subgroup Strategy (2026-03-25)
- **Decision**: Perform subgroup NMAs for COO, IPI, DEL, age only if ≥3 trials report subgroup HRs
- **Rationale**: Sparse subgroup data → underpowered NMA if too few trials contribute. Report available data descriptively if <3 trials.

### D006: TP53 Mutation — Discussion Only (2026-03-25)
- **Decision**: Do not attempt TP53 subgroup NMA; address in Discussion as unmet need
- **Rationale**: Very few trials report TP53 outcomes. Insufficient data for quantitative synthesis.

---

## Assumptions

1. All included trials used standard R-CHOP (rituximab 375 mg/m² + CHOP q21d × 6-8 cycles) as comparator — will verify during extraction
2. PFS definitions are sufficiently similar across trials for pooling (Lugano/Cheson criteria)
3. ITT populations used for all efficacy analyses
4. Transitivity is plausible given similar eligibility criteria across trials (untreated DLBCL, ECOG 0-2, adequate organ function)

## Unresolved Items

1. Whether to include trials with obinutuzumab maintenance (GOYA had optional maintenance — verify)
2. Whether R2-CHOP (ECOG-E1412) and ROBUST should be treated as same node (R-CHOP+lenalidomide) or separate — depends on dose/schedule similarity
3. Exact number of additional Phase III trials beyond the 7 pre-identified — to be determined by systematic search
