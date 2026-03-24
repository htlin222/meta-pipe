# Outcome Definitions

**Project**: gcsf-neutropenia
**Date**: 2026-03-24

---

## Primary Outcome

### 1. Incidence of Febrile Neutropenia (FN)

- **Definition**: Proportion of patients experiencing at least one episode of febrile neutropenia during the study period
- **Measurement**: ANC < 0.5 x 10^9/L (or < 1.0 x 10^9/L with predicted decline) AND temperature >= 38.3 C (single) or >= 38.0 C (sustained >= 1 hour)
- **Data type**: Dichotomous (event/no event per patient)
- **Effect measure**: Risk Ratio (RR) with 95% CI
- **Time frame**: Per chemotherapy cycle or cumulative over all cycles (preferred: all cycles)
- **Minimum reporting**: Number of events and total patients per arm
- **Priority**: Highest -- this is the primary efficacy endpoint for G-CSF prophylaxis and directly informs clinical guidelines (ASCO/NCCN recommend G-CSF when FN risk >= 20%)

---

## Secondary Outcomes

### 2. Overall Survival (OS)

- **Definition**: Time from randomization to death from any cause
- **Data type**: Time-to-event
- **Effect measure**: Hazard Ratio (HR) with 95% CI; if not available, use RR for mortality at fixed time points
- **Time frame**: End of study follow-up
- **Clinical relevance**: Critical for determining whether FN prevention translates to survival benefit

### 3. Infection-Related Mortality

- **Definition**: Death attributed to infection during or within 30 days of chemotherapy
- **Data type**: Dichotomous
- **Effect measure**: Risk Ratio (RR) with 95% CI
- **Time frame**: During chemotherapy or within 30 days of last cycle
- **Clinical relevance**: Direct measure of the most severe consequence of neutropenia

### 4. Hospitalization Rate Due to Febrile Neutropenia

- **Definition**: Proportion of patients hospitalized for FN management
- **Data type**: Dichotomous
- **Effect measure**: Risk Ratio (RR) with 95% CI
- **Time frame**: Over all chemotherapy cycles
- **Clinical relevance**: Major driver of healthcare costs and patient burden

### 5. Time to Neutrophil Recovery

- **Definition**: Days from ANC nadir to ANC >= 0.5 x 10^9/L
- **Data type**: Continuous
- **Effect measure**: Mean Difference (MD) in days with 95% CI
- **Time frame**: Per chemotherapy cycle (first cycle preferred for consistency)
- **Clinical relevance**: Shorter recovery reduces infection window and may permit on-schedule chemotherapy dosing

### 6. Adverse Events

- **Definition**: Treatment-related adverse events, reported separately:
  - **Bone pain**: Any grade, reported per patient
  - **Injection site reactions**: Any grade, reported per patient
  - **Serious adverse events (SAEs)**: Grade >= 3 per CTCAE
- **Data type**: Dichotomous (per event type)
- **Effect measure**: Risk Ratio (RR) with 95% CI
- **Time frame**: During G-CSF administration period
- **Clinical relevance**: Bone pain is the most common G-CSF side effect (10-30%); important for benefit-risk assessment

### 7. Relative Dose Intensity (RDI) of Chemotherapy

- **Definition**: Ratio of actual delivered chemotherapy dose intensity to planned dose intensity, expressed as a percentage
- **Data type**: Continuous
- **Effect measure**: Mean Difference (MD) in percentage with 95% CI
- **Time frame**: Over all planned chemotherapy cycles
- **Clinical relevance**: Higher RDI correlates with improved oncologic outcomes; G-CSF enables maintenance of planned dose schedules

---

## Summary Table

| # | Outcome | Type | Measure | Priority |
|---|---------|------|---------|----------|
| 1 | Febrile neutropenia incidence | Dichotomous | RR | **Primary** |
| 2 | Overall survival | Time-to-event | HR | Secondary |
| 3 | Infection-related mortality | Dichotomous | RR | Secondary |
| 4 | Hospitalization for FN | Dichotomous | RR | Secondary |
| 5 | Neutrophil recovery time | Continuous | MD | Secondary |
| 6 | Adverse events | Dichotomous | RR | Secondary |
| 7 | Relative dose intensity | Continuous | MD | Secondary |

---

## GRADE Assessment Plan

Each outcome will be assessed using the GRADE framework:
- **Risk of bias**: Via Cochrane RoB 2.0 tool
- **Inconsistency**: I-squared and Cochran's Q test
- **Indirectness**: Population, intervention, comparator, and outcome match
- **Imprecision**: Optimal information size and CI width
- **Publication bias**: Funnel plot + Egger's test (if >= 10 studies)

Initial certainty: HIGH (all RCTs), with potential downgrading per GRADE domains.

---

## Subgroup Analyses (Pre-specified)

1. **Cancer type**: Solid tumors vs hematologic malignancies
2. **G-CSF formulation**: Filgrastim vs pegfilgrastim vs lipegfilgrastim
3. **FN risk category**: High-risk (>= 20%) vs intermediate-risk (10-20%) chemotherapy regimens
4. **Prophylaxis timing**: Primary vs secondary prophylaxis
5. **Line of therapy**: First-line vs subsequent lines

## Sensitivity Analyses (Pre-specified)

1. Exclude studies with high risk of bias (RoB 2.0)
2. Exclude studies published only as conference abstracts
3. Fixed-effect vs random-effects model comparison
4. Leave-one-out analysis for influential studies
5. Restrict to studies using standard FN definitions (ANC < 0.5 + fever >= 38.3 C)
