# Eligibility Criteria

## Early TNBC Neoadjuvant Immunotherapy Meta-Analysis

**Date**: 2026-02-07
**Version**: 1.0
**Based on**: pico.yaml v1.0

---

## Study Selection Criteria

### Inclusion Criteria

#### 1. Study Design

- ✅ **Randomized controlled trials (RCTs)**
- ✅ **Phase II or Phase III trials**
- ✅ Parallel-group design
- ✅ Minimum 20 patients per arm

#### 2. Population

- ✅ **Triple-negative breast cancer (TNBC)**
  - ER-negative: <1% nuclear staining by IHC
  - PR-negative: <1% nuclear staining by IHC
  - HER2-negative: IHC 0-1+, or IHC 2+ with FISH/ISH negative (ratio <2.0)
- ✅ **Early-stage or locally advanced**
  - Clinical stage I-III (T1-4, N0-3, M0)
  - Resectable disease at diagnosis
  - Candidate for curative-intent surgery
- ✅ **Neoadjuvant (preoperative) setting**
- ✅ Adults (age ≥18 years)

#### 3. Intervention

- ✅ **Immune checkpoint inhibitor (ICI) + neoadjuvant chemotherapy**
  - PD-1 or PD-L1 inhibitors: pembrolizumab, atezolizumab, durvalumab, nivolumab, camrelizumab, or similar
  - Combined with standard neoadjuvant chemotherapy (anthracycline, taxane, platinum, or combinations)

#### 4. Comparator

- ✅ **Same chemotherapy without ICI**
  - Placebo + chemotherapy (preferred)
  - Chemotherapy alone (acceptable)

#### 5. Outcomes

Must report at least ONE of:

- ✅ **Pathologic complete response (pCR)** - ypT0/Tis ypN0
- ✅ **Event-free survival (EFS)**
- ✅ **Overall survival (OS)**
- ✅ **Disease-free survival (DFS)**

---

### Exclusion Criteria

#### 1. Study Design

- ❌ Non-randomized studies
- ❌ Single-arm trials
- ❌ Observational studies (cohort, case-control)
- ❌ Case reports, case series
- ❌ Phase I dose-finding studies
- ❌ Reviews, meta-analyses, editorials, commentaries
- ❌ Study protocols without results
- ❌ Duplicate publications (include only most recent/complete)

#### 2. Population

- ❌ **Metastatic or stage IV disease (M1)**
- ❌ **Not exclusively triple-negative**
  - Mixed populations (TNBC + ER+ or HER2+) unless TNBC subgroup data available separately
- ❌ **Not neoadjuvant setting**
  - Adjuvant (post-surgery) trials
  - Metastatic/palliative treatment trials
- ❌ **Prior systemic therapy** for current breast cancer
- ❌ Recurrent breast cancer

#### 3. Intervention

- ❌ No immune checkpoint inhibitor
- ❌ ICI given as monotherapy (without chemotherapy)
- ❌ Non-PD-1/PD-L1 ICIs only (e.g., CTLA-4 inhibitors alone)
- ❌ ICI given only in adjuvant phase (not during neoadjuvant)

#### 4. Comparator

- ❌ No control group
- ❌ Different chemotherapy regimens between arms
- ❌ Active comparator (different ICI or targeted therapy)

#### 5. Outcomes

- ❌ No relevant outcomes reported
- ❌ Outcomes reported only as abstracts without sufficient data for meta-analysis

---

## Detailed Eligibility Guidance

### Population-Related Decisions

#### Q1: Mixed Populations (TNBC + Other Subtypes)

**Scenario**: Trial includes TNBC, ER+, and HER2+ patients

**Decision**:

- ✅ **INCLUDE** if TNBC-specific subgroup data available for outcomes
- ❌ **EXCLUDE** if only combined results reported
- **Action**: Contact authors to request TNBC subgroup data if not published

---

#### Q2: Inflammatory Breast Cancer (IBC)

**Scenario**: Trial includes inflammatory TNBC

**Decision**:

- ✅ **INCLUDE** if IBC is explicitly allowed in trial eligibility
- ✅ **INCLUDE** if <10% of participants are IBC
- ⚠️ **INCLUDE with sensitivity analysis** if 10-25% are IBC
- ❌ **EXCLUDE** if >25% are IBC (different biology and prognosis)

---

#### Q3: Bilateral Breast Cancer

**Scenario**: Patient has bilateral breast cancer

**Decision**:

- ✅ **INCLUDE** if both sides are TNBC
- ❌ **EXCLUDE** if one side is non-TNBC (mixed phenotype)
- **Action**: Extract data per patient (not per tumor)

---

### Intervention-Related Decisions

#### Q4: ICI Timing (Neoadjuvant + Adjuvant)

**Scenario**: ICI given during neoadjuvant phase AND continued after surgery (adjuvant)

**Decision**:

- ✅ **INCLUDE** - This is common practice (e.g., KEYNOTE-522)
- **Action**: Extract data on adjuvant continuation for subgroup/sensitivity analysis
- **Analysis**: Primary analysis includes all; sensitivity analysis separates neoadjuvant-only effect if possible

---

#### Q5: Different Chemotherapy Backbones

**Scenario**: Trials use different chemotherapy regimens (AC-T, carboplatin-paclitaxel, etc.)

**Decision**:

- ✅ **INCLUDE ALL** as long as both arms receive same chemotherapy
- **Rationale**: Standard neoadjuvant regimens for TNBC; heterogeneity expected
- **Action**: Subgroup analysis by chemotherapy type

---

#### Q6: ICI Dose Variations

**Scenario**: Different trials use different ICI doses (e.g., pembrolizumab 200mg Q3W vs 400mg Q6W)

**Decision**:

- ✅ **INCLUDE** if doses are within approved therapeutic range
- **Rationale**: Dose variations within range are clinically equivalent
- **Action**: Extract dose information; sensitivity analysis if concern

---

### Comparator-Related Decisions

#### Q7: Placebo vs No Placebo

**Scenario**: Some trials use placebo + chemo, others just chemo alone

**Decision**:

- ✅ **INCLUDE BOTH**
- **Rationale**: Blinding is ideal but open-label acceptable for objective outcomes (pCR, survival)
- **Action**: Sensitivity analysis by blinding status

---

#### Q8: Cross-Over Design

**Scenario**: Control arm allowed to cross over to ICI after progression

**Decision**:

- ✅ **INCLUDE** for pCR analysis (measured before crossover)
- ⚠️ **CAUTION** for survival analysis (crossover dilutes effect)
- **Action**: Note crossover rates; interpret survival results cautiously

---

### Outcome-Related Decisions

#### Q9: Different pCR Definitions

**Scenario**: Trials define pCR differently (ypT0/Tis ypN0 vs ypT0 ypN0)

**Decision**:

- ✅ **INCLUDE ALL** definitions
- **Preference**: ypT0/Tis ypN0 (most common)
- **Action**: Extract all definitions; sensitivity analysis by pCR definition

**pCR Definition Hierarchy** (in order of preference):

1. ypT0/Tis ypN0 (no invasive cancer in breast and nodes)
2. ypT0 ypN0 (no invasive or in situ cancer in breast and nodes)
3. ypT0/Tis (breast only, regardless of nodes)

---

#### Q10: Survival Outcomes - EFS vs DFS

**Scenario**: Some trials report EFS, others DFS

**Decision**:

- ✅ **INCLUDE BOTH**
- **Rationale**: EFS and DFS are similar but differ in event definition
- **Action**: Extract separately; do NOT pool EFS and DFS; analyze as separate outcomes

**Definitions**:

- **EFS**: From randomization to progression/recurrence/second cancer/death
- **DFS**: From surgery to recurrence/death
- **OS**: From randomization to death (most important)

---

#### Q11: Immature Survival Data

**Scenario**: Recent trial published pCR but survival data not yet mature

**Decision**:

- ✅ **INCLUDE** for pCR analysis
- ⏳ **PENDING** for survival analysis (wait for mature data or exclude from survival meta-analysis)
- **Action**: Note median follow-up; include in sensitivity analysis if events <50% maturity

---

### Language and Publication Type

#### Q12: Non-English Publications

**Scenario**: Relevant trial published in Chinese, Spanish, etc.

**Decision**:

- ✅ **INCLUDE** - No language restriction
- **Action**: Translate abstract and full text; extract data; assess risk of bias

---

#### Q13: Conference Abstracts

**Scenario**: Trial results presented at ASCO but full publication not yet available

**Decision**:

- ✅ **INCLUDE** if sufficient data for meta-analysis
- **Preference**: Full publications over abstracts
- **Action**:
  - Search for subsequent full publication
  - Contact authors for missing data
  - Sensitivity analysis excluding abstracts

---

#### Q14: Duplicate Publications

**Scenario**: KEYNOTE-522 has 3 publications (pCR 2020, EFS 2022, OS 2024)

**Decision**:

- ✅ **INCLUDE** latest/most complete publication
- **Action**:
  - Cite all publications
  - Extract pCR from 2020, EFS from 2022, OS from 2024
  - Avoid double-counting participants

---

## Data Extraction Priorities

When extracting data, prioritize in this order:

### For pCR:

1. ypT0/Tis ypN0 (preferred)
2. Number of events (n/N for each arm)
3. Percentage with 95% CI
4. Risk ratio or odds ratio with 95% CI

### For Survival (EFS/DFS/OS):

1. Hazard ratio with 95% CI
2. Median survival times
3. Kaplan-Meier curves (if HR not reported, use digitization)
4. Number of events and total patients

### For Adverse Events:

1. Grade 3-4 treatment-related AEs (n/N)
2. Immune-related AEs (irAEs) by type
3. Treatment discontinuation due to AEs

---

## Handling Special Cases

### Case 1: Trial Stopped Early

**Decision**: ✅ INCLUDE but note in risk of bias assessment

### Case 2: Post-Hoc or Unplanned Subgroup

**Decision**: ✅ INCLUDE but assess risk of selective reporting bias

### Case 3: Unpublished Data from Trial Registry

**Decision**: ✅ INCLUDE if results posted on ClinicalTrials.gov with sufficient detail

### Case 4: Industry-Sponsored Trials

**Decision**: ✅ INCLUDE; assess funding bias in risk of bias assessment

### Case 5: Multiple Trial Arms (3+ arms)

**Decision**:

- If 2 ICI arms vs 1 control: Combine ICI arms (avoid double-counting control)
- If ICI + X vs ICI alone vs control: Include only ICI vs control comparison

---

## Screening Process

### Level 1: Title/Abstract Screening

**Include if**:

- RCT in TNBC
- Neoadjuvant setting
- ICI intervention

**Exclude if**:

- Clearly not RCT
- Clearly metastatic
- No ICI
- Review/editorial

**Uncertain if**:

- Abstract unclear → Proceed to full-text

### Level 2: Full-Text Screening

Apply all eligibility criteria systematically

**Document exclusion reasons**:

- Wrong population (not TNBC, metastatic, etc.)
- Wrong intervention (no ICI, wrong timing)
- Wrong comparator (no control, different chemo)
- Wrong outcomes (no pCR or survival)
- Wrong study design (not RCT)
- Duplicate publication

---

## Conflict Resolution

### Between Reviewers

1. Discuss discordant decisions
2. Refer to this eligibility document
3. Consult third reviewer if no consensus

### Missing Information

1. Contact study authors via email
2. Wait 2 weeks for response
3. If no response, decide based on available information
4. Document as "unclear" in risk of bias

---

## Updates and Amendments

Any changes to eligibility criteria after protocol registration must be:

- Documented with date and rationale
- Reported in PROSPERO amendment
- Disclosed in manuscript

---

**Version**: 1.0
**Date**: 2026-02-07
**Next Review**: Before starting screening
**Approved by**: Meta-analysis team
