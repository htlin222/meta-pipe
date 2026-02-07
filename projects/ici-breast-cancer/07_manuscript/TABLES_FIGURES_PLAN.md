# Tables and Figures Plan

## Main Text Tables

### Table 1: Characteristics of Included Trials

**Content**:

- Trial name, NCT number, first author, year
- Sample size (total, ICI arm, control arm)
- ICI agent (drug, dose, schedule)
- Chemotherapy backbone
- Blinding status
- Median follow-up (months)
- Outcomes reported (pCR, EFS, OS)

**Source**: `05_extraction/round-01/extraction.csv`

**Status**: ✅ Data available, needs formatting

---

### Table 2: Efficacy Outcomes Summary

**Content**:
| Outcome | Trials (N) | ICI Group | Control Group | Effect Estimate | 95% CI | p-value | I² | Absolute Benefit | NNT |
|---------|-----------|-----------|---------------|-----------------|--------|---------|-----|------------------|-----|
| pCR | 5 (2402) | 60.1% | 47.8% | RR 1.26 | 1.16-1.37 | 0.0015 | 0% | +13.8% | 7 |
| EFS (5-year) | 3 (1681) | — | — | HR 0.66 | 0.51-0.86 | 0.021 | 0% | +9.2% | 11 |
| OS (5-year) | 2 (1348) | — | — | HR 0.48\* | 0.00-128.74 | 0.346 | 62.3% | +9.3% | 11 |

\*Both individual trials significant (KEYNOTE-522 p=0.0015, GeparNuevo p=0.0076)

**Source**:

- `06_analysis/tables/pCR_meta_analysis_results.csv`
- `06_analysis/tables/EFS_meta_analysis_results.csv`
- `06_analysis/tables/OS_meta_analysis_results.csv`

**Status**: ✅ Data available, needs integration

---

### Table 3: Safety Outcomes Summary

**Content**:
| Outcome | Trials (N) | ICI Group | Control Group | RR | 95% CI | p-value | Absolute Harm | NNH |
|---------|-----------|-----------|---------------|-----|--------|---------|---------------|-----|
| Serious AE | 2 (774) | 29.5% | 19.6% | 1.50 | 1.13-1.98 | 0.034 | +9.9% | 10 |
| Grade 3+ irAE | 1 (1174) | 13.0% | 1.5% | ~8.5 | — | — | +11.5% | 9 |
| Discontinuation | 1 (1174) | 27.6% | 14.1% | ~2.0 | — | — | +13.5% | 7 |
| Fatal AE | 2 (1615) | 0.40% | 0% | — | — | — | +0.40% | 250 |

**Source**: `06_analysis/tables/safety_meta_analysis_summary.csv`

**Status**: ✅ Data available, needs formatting

---

## Main Text Figures

### Figure 1: Forest Plots for Efficacy Outcomes

**Panel A: pCR Meta-Analysis**

- Source: `06_analysis/figures/forest_plot_pCR.png`
- Status: ✅ Generated
- Shows: 5 trials, pooled RR 1.26 (1.16-1.37), I²=0%

**Panel B: EFS Meta-Analysis**

- Source: `06_analysis/figures/forest_plot_EFS.png`
- Status: ✅ Generated
- Shows: 3 trials, pooled HR 0.66 (0.51-0.86), I²=0%

**Panel C: OS Meta-Analysis** (Optional, may move to supplement due to wide CI)

- Source: `06_analysis/figures/forest_plot_OS.png`
- Status: ✅ Generated
- Shows: 2 trials, individual both significant, pooled HR 0.48 (wide CI)

**Action needed**: Combine into multi-panel figure

---

### Figure 2: PD-L1 Subgroup Analysis

**Panel A: PD-L1-Positive Subgroup**

- Source: `06_analysis/figures/forest_plot_PDL1_subgroups.png` (subset)
- Shows: 3 trials, RR 1.27 (1.10-1.45), p=0.018

**Panel B: PD-L1-Negative Subgroup**

- Source: `06_analysis/figures/forest_plot_PDL1_subgroups.png` (subset)
- Shows: 2 trials, RR 1.75 (0.09-33.96), p=0.25

**Panel C: Interaction Test**

- Visual representation of p=0.169 (not significant)
- Conclusion: PD-L1 prognostic not predictive

**Action needed**: Extract from existing figure or recreate

---

### Figure 3: Safety Forest Plots

**Panel A: Serious Adverse Events**

- Source: `06_analysis/figures/forest_plot_safety_sae.png`
- Status: ✅ Generated
- Shows: 2 trials, RR 1.50 (1.13-1.98), p=0.034

**Panel B: Publication Bias (Funnel Plot)** (Optional)

- pCR funnel plot: `06_analysis/figures/funnel_plot_pCR.png`
- Egger's test p=0.713 (no bias)

**Action needed**: Combine SAE with funnel plot

---

## Supplementary Tables

### Supplementary Table 1: Risk of Bias Assessment

**Content**: RoB 2 tool results for all 5 trials across 5 domains

**Status**: ⚠️ Not yet created (mentioned in Results)

**Action needed**: Create RoB 2 assessment

---

### Supplementary Table 2: PD-L1 Subgroup Detailed Results

**Content**:

- Breakdown by trial and PD-L1 definition
- pCR rates by subgroup
- EFS data by PD-L1 (KEYNOTE-522)

**Source**: `06_analysis/tables/PDL1_subgroup_comparison.csv`

**Status**: ✅ Data available

---

### Supplementary Table 3: Individual Trial pCR Results

**Content**: Detailed pCR data by trial including:

- Study characteristics
- pCR definition
- Events/total
- Individual RR with CI

**Source**: `06_analysis/tables/pCR_meta_analysis_results.csv`

**Status**: ✅ Data available

---

### Supplementary Table 4: GRADE Evidence Profile

**Content**:
| Outcome | Quality of Evidence | Risk of Bias | Inconsistency | Indirectness | Imprecision | Publication Bias |
|---------|---------------------|--------------|---------------|--------------|-------------|------------------|
| pCR | ⊕⊕⊕⊕ (HIGH) | Low | Low | Low | Low | Undetected |
| EFS | ⊕⊕⊕◯ (MODERATE) | Low | Low | Low | Serious\* | Undetected |
| OS | ⊕⊕◯◯ (LOW) | Low | Serious** | Low | Very serious\*** | Unassessable |
| Safety (SAE) | ⊕⊕◯◯ (LOW) | Low | Low | Serious\*\*\*\* | Serious | Unassessable |

\*Limited follow-up (<5 years)
**I²=62.3% \***Wide CI (k=2, Hartung-Knapp)
\*\*\*\*Heterogeneous definitions

**Status**: ⚠️ Needs creation

---

## Supplementary Figures

### Supplementary Figure 1: Leave-One-Out Sensitivity Analyses

**Panel A: pCR** - Not generated (I²=0%, not needed)
**Panel B: EFS** - Source: `06_analysis/figures/efs_leave_one_out.png` ✅
**Panel C: OS** - Source: `06_analysis/figures/os_leave_one_out.png` ✅

---

### Supplementary Figure 2: Funnel Plots (Publication Bias)

**Panel A: pCR** - Source: `06_analysis/figures/funnel_plot_pCR.png` ✅
**Panel B: EFS** - Source: `06_analysis/figures/funnel_plot_EFS.png` ✅
**Panel C: OS** - Not applicable (k=2)

---

## Summary of File Status

### ✅ Already Generated (Ready to Use)

- All forest plots (pCR, EFS, OS, PD-L1, Safety)
- All funnel plots (pCR, EFS)
- All leave-one-out plots (EFS, OS)
- All results CSV tables
- Safety summary table

### ⚠️ Needs Creation

- **Table 1**: Trial characteristics (extract from extraction.csv)
- **Table 2**: Integrated efficacy summary (combine existing CSVs)
- **Table 3**: Integrated safety summary (reformat existing)
- **Supplementary Table 1**: RoB 2 assessment
- **Supplementary Table 4**: GRADE evidence profile
- **Multi-panel figures**: Combine existing PNGs

### 📋 Priority Actions

1. Create Table 1 (Trial Characteristics) from extraction.csv
2. Create integrated efficacy table (Table 2)
3. Reformat safety table (Table 3)
4. Create RoB 2 assessment (Supplementary Table 1)
5. Create GRADE profile (Supplementary Table 4)
6. Combine forest plots into multi-panel figures

---

**Estimated completion time**: ~30-45 minutes
**Files needed**: Manuscript-ready tables (CSV → formatted tables) and figure assembly
