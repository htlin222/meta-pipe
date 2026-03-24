# Decision Log

**Project**: gcsf-neutropenia
**Created**: 2026-03-24
**Last Updated**: 2026-03-24

---

## Decisions

### DEC-001: Analysis Type — Preliminary NMA Candidate

- **Date**: 2026-03-24
- **Stage**: 01_protocol
- **Decision**: Set `analysis_type.preliminary: nma_candidate`
- **Rationale**: The research question involves three distinct G-CSF formulations (filgrastim, pegfilgrastim, lipegfilgrastim) compared against placebo/no G-CSF. This yields at least 4 treatment nodes, making network meta-analysis a candidate approach. Multiple head-to-head trials comparing G-CSF formulations exist in the literature, supporting potential network connectivity.
- **Status**: Preliminary -- requires confirmation after screening (Stage 2 gate)
- **Action**: Proceed with protocol development; re-assess after title/abstract screening when study design profile is known.

### DEC-002: Primary Outcome — Febrile Neutropenia Incidence

- **Date**: 2026-03-24
- **Stage**: 01_protocol
- **Decision**: Use incidence of febrile neutropenia (FN) as the primary outcome
- **Rationale**: FN is the most clinically relevant and consistently reported endpoint in G-CSF prophylaxis trials. It is the basis for guideline thresholds (ASCO/NCCN recommend G-CSF when FN risk >= 20%). Nearly all RCTs report FN as a primary or key secondary endpoint, ensuring high data availability.
- **Status**: Final

### DEC-003: Effect Measure — Risk Ratio for Dichotomous Outcomes

- **Date**: 2026-03-24
- **Stage**: 01_protocol
- **Decision**: Use Risk Ratio (RR) as the primary effect measure for dichotomous outcomes
- **Rationale**: RR is more interpretable than OR for common events. FN incidence can be 20-40% in control arms, making OR a poor approximation of RR. RR is also the standard measure used in prior meta-analyses of G-CSF prophylaxis (Kuderer 2007, Mhaskar 2014).
- **Status**: Final

### DEC-004: Study Design Restriction — RCTs Only

- **Date**: 2026-03-24
- **Stage**: 01_protocol
- **Decision**: Include only randomized controlled trials
- **Rationale**: The literature on G-CSF prophylaxis is mature with numerous large RCTs available. RCT-only inclusion minimizes confounding and provides the strongest evidence base. Observational studies would introduce significant heterogeneity due to indication bias (sicker patients more likely to receive G-CSF).
- **Status**: Final

### DEC-005: No Date or Language Restrictions

- **Date**: 2026-03-24
- **Stage**: 01_protocol
- **Decision**: Apply no date or language restrictions to the search
- **Rationale**: Filgrastim was first approved in 1991; early trials remain relevant. Language restrictions introduce bias (Cochrane Handbook 4.3.1). Translation tools are available for non-English studies.
- **Status**: Final

### DEC-006: Risk of Bias Tool — RoB 2.0

- **Date**: 2026-03-24
- **Stage**: 01_protocol
- **Decision**: Use Cochrane RoB 2.0 tool for risk of bias assessment
- **Rationale**: All included studies will be RCTs, making RoB 2.0 the appropriate tool. It provides domain-level and overall judgments aligned with GRADE assessment requirements.
- **Status**: Final

### DEC-007: Databases — PubMed + Scopus + Embase + CENTRAL

- **Date**: 2026-03-24
- **Stage**: 01_protocol
- **Decision**: Search 4 databases (PubMed, Scopus, Embase, Cochrane CENTRAL)
- **Rationale**: PubMed and Scopus are mandatory per pipeline requirements. Embase adds strong coverage of European and drug-focused literature. Cochrane CENTRAL is a curated RCT registry that improves sensitivity. Four databases exceed the PRISMA minimum of 2.
- **Status**: Final

---

## Assumptions

| # | Assumption | Impact if Wrong | Mitigation |
|---|-----------|-----------------|------------|
| A1 | Sufficient head-to-head trials exist between G-CSF formulations to form a connected network | NMA not feasible; downgrade to pairwise | Confirmation gate after screening (Stage 2) |
| A2 | Transitivity is plausible across G-CSF formulations (similar patient populations) | NMA estimates biased | Pre-specified transitivity assessment; sensitivity analyses |
| A3 | FN definition is consistent across trials | Heterogeneity in outcome measurement | Sensitivity analysis restricting to standard FN definition |
| A4 | Biosimilar G-CSF agents are clinically equivalent to reference products | Misclassification in treatment nodes | Group biosimilars with reference product; sensitivity analysis separating them |

---

## Unresolved Items

| # | Item | Blocking? | Resolution Plan |
|---|------|-----------|----------------|
| U1 | Include biosimilar-specific trials in the network? | No | Default: group with reference product. Decide after screening reveals the data landscape. |
| U2 | How to handle crossover trial designs? | No | Use first-period data only if crossover washout is inadequate. Decide at extraction stage. |
| U3 | Include secondary prophylaxis trials alongside primary? | No | Default: include both with subgroup analysis. May separate if clinical heterogeneity is excessive. |
