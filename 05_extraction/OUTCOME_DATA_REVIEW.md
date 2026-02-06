# Outcome Data Manual Review - Stage 05

**Date**: 2026-02-06
**Reviewer**: Research Expert (Manual PDF Review)
**Purpose**: Extract PFS HR data for meta-analysis feasibility

---

## 📋 Summary of Findings

**Total studies reviewed**: 6 (after excluding 4 review articles/protocols)
**Studies with PFS HR data**: 2
**Studies without PFS HR**: 4

### Studies with Usable PFS HR Data: 2

| Study ID              | Comparison                                      | PFS HR | 95% CI    | p-value | Notes                             |
| --------------------- | ----------------------------------------------- | ------ | --------- | ------- | --------------------------------- |
| AgrawalYN202536       | Palbociclib+ET vs Capecitabine                  | 1.00   | 0.76-1.31 | 1.00    | PEARL trial, Luminal A+B subgroup |
| TokunagaE202539379782 | Capivasertib+Fulvestrant vs Placebo+Fulvestrant | 0.73   | 0.40-1.28 | NS      | CAPItello-291 Japan subgroup      |

### Studies without PFS HR Data: 4

| Study ID             | Study Type                      | Reason for No HR                                                   |
| -------------------- | ------------------------------- | ------------------------------------------------------------------ |
| AgostiniM2024Cancers | Single-arm retrospective cohort | No control group; only reported median PFS = 3.7 months            |
| KettnerNM20252       | Biomarker study                 | Focused on IL-6 as predictive marker; no clinical trial component  |
| OgataN202550         | Review article                  | ❌ Should be EXCLUDED - systematic review, not original research   |
| PalumboR2023179      | Observational study (ET vs CT)  | Compared ET vs CT after CDK4/6i; not relevant to research question |

---

## 📊 Detailed Findings

### 1. AgostiniM2024Cancers ❌ No HR

**Study Design**: Retrospective single-arm cohort
**Population**: 30 women with HR+/HER2- MBC
**Intervention**: Fulvestrant 500mg monotherapy after CDK4/6i progression
**Outcomes**:

- Median PFS: 3.7 months (range 1-9.7 months)
- 23/30 patients progressed
- No comparator arm → **No HR available**

**Conclusion**: Cannot be included in meta-analysis (no control group)

---

### 2. AgrawalYN202536 ✅ Has HR

**Study Design**: Post-hoc transcriptomics analysis of PEARL Phase III RCT
**Population**: 601 patients with AI-resistant HR+/HER2- MBC
**Comparison**:

- Arm 1: Palbociclib + Endocrine Therapy
- Arm 2: Capecitabine

**Primary Outcome - PFS HR by PAM50 Subtype**:

| PAM50 Subtype   | PFS HR   | 95% CI        | p-value  |
| --------------- | -------- | ------------- | -------- |
| Luminal A       | 0.76     | 0.52-1.11     | 0.16     |
| Luminal B       | 1.53     | 1.01-2.32     | 0.04     |
| **Luminal A+B** | **1.00** | **0.76-1.31** | **1.00** |
| Non-luminal     | 13.3     | 1.69-107      | 0.002    |

**Interpretation**:

- Overall (Luminal A+B): Palbociclib+ET vs Capecitabine showed **no difference** (HR=1.00)
- Luminal B subgroup: Capecitabine was **better** (HR=1.53, favoring capecitabine)
- This is a **transcriptomics biomarker study**, not a direct CDK4/6i continuation study

**Relevance to Meta-Analysis**:

- ⚠️ **Moderate relevance** - compares CDK4/6i+ET vs chemotherapy in AI-resistant setting
- But: No prior CDK4/6i exposure (n_cdk46_prior = 0)
- This is **first-line** CDK4/6i, not continuation after progression

---

### 3. KettnerNM20252 ❌ No HR

**Study Design**: Biomarker discovery study
**Focus**: IL-6 as predictive marker for CDK4/6i resistance
**Population**: 166 patients with HR+/HER2- MBC treated with palbociclib
**Findings**:

- Circulating IL-6 levels increased at progression
- IL-6 knockdown re-sensitized resistant cells
- STAT3 inhibitor (TTI-101) reduced tumor growth in PDX models

**Conclusion**: **Not a clinical trial** with PFS HR data; biomarker study only

---

### 4. OgataN202550 ❌ EXCLUDE (Review)

**Study Type**: **Systematic Review**
**Title**: "Efficiency of Fulvestrant Monotherapy After CDK4/6 Inhibitor Exposure: Is This a Viable Choice?"

**Content**:

- Reviewed 10 clinical trials with 1038 patients
- Reported median PFS of fulvestrant monotherapy = 3.18 months (range 1.9-5.3 months)
- Analyzed trials: EMERALD, SERENA-2, AMEERA-3, ELAINE-1, CAPItello-291, VERONICA, post-MONARCH, PACE, PALMIRA, MAINTAIN

**Action Required**:

- ❌ **EXCLUDE from analysis** - this is a review article, not original research
- ✅ **Update extraction.csv** to mark for exclusion
- ℹ️ Could reference these 10 trials for discussion section

---

### 5. PalumboR2023179 ❌ No Relevant HR

**Study Design**: Prospective observational monocentric cohort study
**Population**: 48 patients progressed on palbociclib + ET
**Comparison**:

- Group 1: Endocrine Therapy (ET) - 10 patients
- Group 2: Chemotherapy (CT) - 38 patients

**Outcomes**:

- Median PFS2 (overall): 5 months (95% CI 4-48 months)
- Median PFS2 (ET): 10 months
- Median PFS2 (CT): 5 months
- **HR for CT vs ET**: 2.64 (95% CI 1.02-6.83), p=0.0451
  - Inverted: **HR for ET vs CT**: 0.38 (95% CI 0.15-0.98)

**Why Not Included**:

- This compares **ET vs CT** after CDK4/6i progression
- **Neither group** continued CDK4/6i
- Not relevant to our research question (CDK4/6i continuation strategies)
- Would need to identify studies comparing CDK4/6i continuation vs standard treatment

**Conclusion**: Interesting data but **not relevant** to meta-analysis on CDK4/6i continuation

---

### 6. TokunagaE202539379782 ✅ Has HR

**Study Design**: Subgroup analysis of CAPItello-291 Phase III RCT
**Population**: 78 patients from Japan (subset of 708 global trial)
**Prior CDK4/6i exposure**: 13/78 (16.7%)
**Comparison**:

- Arm 1: Capivasertib + Fulvestrant (n=37)
- Arm 2: Placebo + Fulvestrant (n=41)

**Primary Outcome - PFS HR**:

| Population               | Median PFS (Arm 1) | Median PFS (Arm 2) | HR       | 95% CI        | Notes                            |
| ------------------------ | ------------------ | ------------------ | -------- | ------------- | -------------------------------- |
| **Overall Japan**        | 13.9 months        | 7.6 months         | **0.73** | **0.40-1.28** | Numerically favored capivasertib |
| PIK3CA/AKT1/PTEN-altered | 13.9 months        | 9.1 months         | 0.65     | 0.29-1.39     | Biomarker-selected subgroup      |
| Non-altered              | NR                 | NR                 | 0.69     | 0.26-1.68     | Exploratory analysis             |

**Intervention**:

- Capivasertib (AKT inhibitor) 400mg BID, 4 days on/3 days off
- Combined with fulvestrant 500mg IM per standard schedule

**Relevance to Meta-Analysis**:

- ✅ **Highly relevant** - evaluates targeted therapy after CDK4/6i
- ✅ Has prior CDK4/6i exposure (16.7%)
- ✅ Clean HR data with confidence intervals
- ⚠️ Subgroup analysis (Japan only) - smaller sample size
- ⚠️ Not CDK4/6i continuation, but AKT inhibitor addition

---

## 🎯 Meta-Analysis Feasibility Assessment

### Can We Proceed with Meta-Analysis?

**Answer: ⚠️ NOT FEASIBLE with current studies**

### Reasons:

1. **Only 2 studies have PFS HR data**:
   - Minimum 3 studies needed for meta-analysis
   - Only have: AgrawalYN202536 and TokunagaE202539379782

2. **Studies are clinically heterogeneous**:
   - **AgrawalYN202536**: Palbociclib+ET vs Capecitabine (first-line CDK4/6i, no prior CDK4/6i)
   - **TokunagaE202539379782**: Capivasertib+Fulvestrant vs Placebo+Fulvestrant (post-CDK4/6i)
   - Different populations, different interventions → **Cannot pool**

3. **Research question mismatch**:
   - Our PICO: CDK4/6i continuation/rechallenge vs standard treatment after CDK4/6i progression
   - Available studies: Compare different agents (AKT inhibitor, chemotherapy) not CDK4/6i continuation

4. **Studies to exclude**:
   - OgataN202550 (review article - should be excluded)
   - AgostiniM2024Cancers (single-arm, no HR)
   - KettnerNM20252 (biomarker study, no clinical outcomes)
   - PalumboR2023179 (ET vs CT, not relevant comparison)

---

## 📝 Recommendations

### Option A: Revise Research Question

**Current focus**: CDK4/6i continuation after progression
**Available data**: Various targeted therapies (AKT inhibitor, different CDK4/6i) vs standard treatment

**Revised question could be**:

- "Efficacy of targeted therapies after CDK4/6i progression in HR+/HER2- MBC"
- Broader scope: Include AKT inhibitors, PI3K inhibitors, CDK4/6i rechallenge

But still only 2 studies → insufficient for meta-analysis

### Option B: Expand Search

Need to find more studies that report:

- CDK4/6i continuation (same drug beyond progression)
- CDK4/6i switch (different CDK4/6i after progression)
- Targeted therapies (AKT/PI3K/mTOR inhibitors) after CDK4/6i

**Potential trials to look for**:

- MAINTAIN trial (ribociclib continuation)
- PACE trial (palbociclib continuation)
- PALMIRA trial (palbociclib rechallenge)
- postMONARCH (abemaciclib continuation)

_Note: OgataN202550 review mentions these trials - could trace primary sources_

### Option C: Narrative Review Instead

With insufficient quantitative data for meta-analysis, consider:

- Systematic narrative review
- Qualitative synthesis of treatment strategies
- Case series analysis (AgostiniM, PalumboR as descriptive evidence)

---

## 🔄 Next Steps

1. **Immediate action needed**:
   - ❌ Mark OgataN202550 for exclusion (review article)
   - ✅ Update extraction.csv with HR data for 2 studies
   - ✅ Document meta-analysis infeasibility

2. **Decision point**:
   - **If proceeding with Stage 06**: Cannot perform quantitative meta-analysis
   - **If expanding search**: Look for MAINTAIN, PACE, PALMIRA, postMONARCH trials
   - **If changing direction**: Convert to narrative review

3. **User consultation required**:
   - Discuss research question revision
   - Decide whether to expand literature search
   - Consider alternative study designs (narrative review, pooled analysis)

---

**Manual Review Complete**: 2026-02-06
**Status**: ⚠️ Meta-analysis NOT FEASIBLE with current 6 studies
**Recommendation**: Expand literature search or revise to narrative review
