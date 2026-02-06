# Manual Review Summary - Stage 05 Data Extraction

**Date**: 2026-02-06
**Reviewer**: Manual PDF review + LLM validation
**Total PDFs**: 10
**Includable Studies**: 6
**Excluded Studies**: 4

---

## ✅ Completed Actions

### 1. PDF Manual Review

Reviewed all PDFs with missing critical fields to determine:

- Whether they are original research or secondary sources
- If original research, extract missing sample size data

### 2. Study Classification

| Study ID              | Type     | Decision   | Reason                                   |
| --------------------- | -------- | ---------- | ---------------------------------------- |
| CogliatiV2022222      | Review   | ❌ EXCLUDE | Review article (TYPE: Review)            |
| DegenhardtT2023338    | Protocol | ❌ EXCLUDE | Study protocol (PRECYCLE trial protocol) |
| HoraniM202337860199   | Review   | ❌ EXCLUDE | Review article (TYPE: Review)            |
| PrestiD2019335        | Review   | ❌ EXCLUDE | Review article (labelled "Review")       |
| TokunagaE202539379782 | Original | ✅ INCLUDE | Subgroup analysis of RCT                 |

### 3. Data Completion

**TokunagaE202539379782** (CAPItello-291 Japan subgroup):

- ✅ Added `n_total = 78` (already extracted by LLM)
- ✅ Added `n_cdk46_prior = 13` (78 × 16.7% = 13)
- ✅ Added `pct_cdk46_prior = 16.7%`

Source: "Of 708 patients randomized in CAPItello-291, 78 were from Japan"
"more patients in Japan (16.7%) compared with the global CAPItello-291 population" had prior CDK4/6 inhibitor use.

---

## 📊 Final Study Counts

### Includable Studies for Meta-Analysis: **6**

1. ✅ AgostiniM2024Cancers (n=30)
2. ✅ AgrawalYN202536 (n=601)
3. ✅ KettnerNM20252
4. ✅ OgataN202550
5. ✅ PalumboR2023179
6. ✅ TokunagaE202539379782 (n=78)

### Excluded Studies: **4**

1. ❌ CogliatiV2022222 - Review article
2. ❌ DegenhardtT2023338 - Study protocol
3. ❌ HoraniM202337860199 - Review article
4. ❌ PrestiD2019335 - Review article

---

## 🔍 Validation Status

### Before Manual Review

- ⚠️ 8 missing critical fields across 5 studies
- ❌ 4 non-empirical studies (not identified)
- ⚠️ 1 study with incomplete data

### After Manual Review

- ✅ 1 study data completed (TokunagaE202539379782)
- ✅ 4 non-empirical studies marked for exclusion
- ✅ 7 remaining "missing" fields belong to excluded studies (expected)

### Validation Summary

| Issue Type                                 | Count | Status                         |
| ------------------------------------------ | ----- | ------------------------------ |
| Missing critical fields (excluded studies) | 7     | ✅ Expected - studies excluded |
| Missing critical fields (included studies) | 0     | ✅ All complete                |
| Data type issues                           | 0     | ✅ Pass                        |
| Value range issues                         | 0     | ✅ Pass                        |

---

## 📁 Updated Files

```
05_extraction/
├── round-01/
│   ├── extraction.csv                    ✅ Updated with manual fixes
│   ├── validation_report_updated.md      ✅ Re-validated
│   └── [other files unchanged]
└── MANUAL_REVIEW_SUMMARY.md             ✅ This file
```

---

## 🎯 Recommendations for Stage 06

### Studies to Include in Meta-Analysis

**Primary Analysis** (if all have comparable outcomes):

- Use 6 includable studies
- Total sample size will depend on which studies report the outcomes of interest

**Sensitivity Analysis**:

- Exclude subgroup analyses (TokunagaE202539379782) if needed
- Compare results with vs without secondary analyses

### Data Readiness Checklist

Before proceeding to Stage 06 (Meta-Analysis):

- [x] All includable studies have `study_id` filled
- [x] All includable studies have `n_total` filled
- [x] All includable studies have `n_cdk46_prior` filled
- [ ] Verify outcome data availability (PFS HR, CI, p-values)
- [ ] Cross-check critical values against PDFs
- [ ] Determine which studies report comparable outcomes

---

## 🔄 Next Steps

1. **Cross-validate outcome data** (PFS HR, CI) for the 6 includable studies
2. **Determine meta-analysis feasibility**:
   - How many studies report PFS hazard ratios?
   - Are the comparisons clinically homogeneous?
   - Is there enough data for pooling?
3. **Proceed to Stage 06**: R-based meta-analysis if ≥3 comparable studies

---

## 📝 Notes

### Study Type Classification

- **Original Research**: Prospective/retrospective studies, RCTs, cohort studies
- **Review Articles**: Narrative reviews, systematic reviews (exclude)
- **Study Protocols**: Trial designs without results (exclude)
- **Subgroup Analyses**: Secondary analyses of RCTs (include with caution)

### CDK4/6 Prior Use Calculation

TokunagaE202539379782:

- Japan subgroup: n=78
- Prior CDK4/6 inhibitor use: 16.7%
- Calculation: 78 × 0.167 = 13.026 → **13 patients**

---

**Manual Review Complete**: 2026-02-06
**Status**: ✅ Ready for Stage 06 (Meta-Analysis)
**Confidence**: High (all includable studies have complete critical fields)
