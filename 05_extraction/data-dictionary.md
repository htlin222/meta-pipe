# Data Extraction Dictionary

## TNBC Neoadjuvant Immunotherapy Meta-Analysis

**Version**: 1.0
**Date**: 2026-02-07
**Purpose**: Standardized data extraction form for LLM-assisted and manual extraction

---

## Instructions for Extractors

1. **One row per trial** (not per publication)
2. **Extract from primary publication** when available
3. **Use "NR" (not reported)** for missing data
4. **Use "NA" (not applicable)** only when truly not applicable
5. **Record page numbers** for key data points
6. **Flag uncertain values** with notes

---

## Section 1: Study Identification

### 1.1 study_id

- **Type**: Text (unique identifier)
- **Format**: First author surname + year (e.g., "Schmid2020")
- **Required**: Yes
- **Notes**: Use primary publication

### 1.2 trial_name

- **Type**: Text
- **Examples**: "KEYNOTE-522", "IMpassion031", "GeparNuevo"
- **Required**: Yes
- **Notes**: Official trial acronym/name

### 1.3 nct_number

- **Type**: Text
- **Format**: NCT########
- **Required**: If available
- **Notes**: ClinicalTrials.gov identifier

### 1.4 first_author

- **Type**: Text
- **Required**: Yes

### 1.5 publication_year

- **Type**: Integer
- **Range**: 2015-2026
- **Required**: Yes

### 1.6 journal

- **Type**: Text
- **Required**: Yes

### 1.7 doi

- **Type**: Text
- **Format**: 10.xxxx/xxxxx
- **Required**: If available

### 1.8 pmid

- **Type**: Integer
- **Required**: If available

---

## Section 2: Study Design

### 2.1 study_design

- **Type**: Categorical
- **Values**:
  - RCT_phase3
  - RCT_phase2
  - RCT_phase1b_2
- **Required**: Yes

### 2.2 randomization_ratio

- **Type**: Text
- **Examples**: "1:1", "2:1", "3:2"
- **Required**: Yes

### 2.3 blinding

- **Type**: Categorical
- **Values**:
  - open_label
  - single_blind
  - double_blind
- **Required**: Yes

### 2.4 multi_center

- **Type**: Boolean
- **Values**: Yes / No
- **Required**: Yes

### 2.5 n_centers

- **Type**: Integer
- **Required**: If available

### 2.6 n_countries

- **Type**: Integer
- **Required**: If available

### 2.7 recruitment_start_date

- **Type**: Date
- **Format**: YYYY-MM or YYYY
- **Required**: If available

### 2.8 recruitment_end_date

- **Type**: Date
- **Format**: YYYY-MM or YYYY
- **Required**: If available

### 2.9 data_cutoff_date

- **Type**: Date
- **Format**: YYYY-MM-DD or YYYY-MM
- **Required**: If available
- **Notes**: For survival outcomes

### 2.10 median_followup_months

- **Type**: Numeric (decimal)
- **Unit**: Months
- **Required**: For survival outcomes

### 2.11 followup_method

- **Type**: Text
- **Examples**: "Median (IQR)", "Median (range)", "Mean (SD)"
- **Required**: If available

---

## Section 3: Population Characteristics

### 3.1 n_randomized_total

- **Type**: Integer
- **Required**: Yes
- **Notes**: Total ITT population

### 3.2 n_intervention

- **Type**: Integer
- **Required**: Yes
- **Notes**: ICI + chemo arm

### 3.3 n_control

- **Type**: Integer
- **Required**: Yes
- **Notes**: Chemo alone arm

### 3.4 mean_age_intervention

- **Type**: Numeric (decimal)
- **Unit**: Years
- **Required**: If available

### 3.5 mean_age_control

- **Type**: Numeric (decimal)
- **Unit**: Years
- **Required**: If available

### 3.6 female_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: Yes
- **Notes**: Should be ~99-100% for TNBC

### 3.7 race_white_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If available

### 3.8 race_black_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If available

### 3.9 race_asian_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If available

### 3.10 tnbc_definition

- **Type**: Text
- **Required**: Yes
- **Examples**: "ER<1%, PR<1%, HER2-negative by IHC/FISH"

### 3.11 er_cutoff

- **Type**: Text
- **Examples**: "<1%", "<10%"
- **Required**: Yes

### 3.12 pr_cutoff

- **Type**: Text
- **Examples**: "<1%", "<10%"
- **Required**: Yes

### 3.13 her2_definition

- **Type**: Text
- **Required**: Yes
- **Examples**: "IHC 0-1+ or IHC 2+ FISH-negative"

---

## Section 4: Disease Characteristics

### 4.1 tumor_stage_inclusion

- **Type**: Text
- **Required**: Yes
- **Examples**: "T1c-T4, N0-N3, M0", "Stage II-III"

### 4.2 stage_2_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If available

### 4.3 stage_3_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If available

### 4.4 clinical_t_stage_t1_t2_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If available

### 4.5 clinical_t_stage_t3_t4_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If available

### 4.6 node_positive_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If available

### 4.7 pdl1_positive_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If available
- **Notes**: Use trial-specific cutoff

### 4.8 pdl1_assay

- **Type**: Text
- **Examples**: "SP142", "22C3", "SP263"
- **Required**: If PDL1 tested

### 4.9 pdl1_cutoff

- **Type**: Text
- **Examples**: "≥1% IC", "CPS≥1", "≥1% TC or IC"
- **Required**: If PDL1 tested

### 4.10 tils_assessed

- **Type**: Boolean
- **Values**: Yes / No
- **Required**: Yes

### 4.11 tils_high_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If TILs assessed
- **Notes**: Use trial-specific cutoff

### 4.12 tils_cutoff

- **Type**: Text
- **Examples**: "≥5%", "≥10%", "≥20%"
- **Required**: If TILs assessed

### 4.13 brca_mutation_tested

- **Type**: Boolean
- **Values**: Yes / No
- **Required**: Yes

### 4.14 brca_mutation_positive_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If BRCA tested

---

## Section 5: Intervention Details

### 5.1 ici_agent

- **Type**: Categorical
- **Values**:
  - pembrolizumab
  - atezolizumab
  - durvalumab
  - nivolumab
  - other
- **Required**: Yes

### 5.2 ici_dose

- **Type**: Text
- **Examples**: "200 mg Q3W", "1200 mg Q3W", "10 mg/kg Q2W"
- **Required**: Yes

### 5.3 ici_start_timing

- **Type**: Categorical
- **Values**:
  - with_first_chemo_dose
  - after_chemo_starts
  - before_chemo
- **Required**: Yes

### 5.4 ici_neoadjuvant_cycles

- **Type**: Integer
- **Required**: Yes
- **Notes**: Number of ICI doses before surgery

### 5.5 ici_adjuvant_continuation

- **Type**: Boolean
- **Values**: Yes / No
- **Required**: Yes

### 5.6 ici_adjuvant_cycles

- **Type**: Integer
- **Required**: If adjuvant continuation = Yes

### 5.7 ici_total_duration_weeks

- **Type**: Integer
- **Unit**: Weeks
- **Required**: Yes
- **Notes**: Total planned ICI duration (neoadjuvant + adjuvant)

### 5.8 chemo_regimen_intervention

- **Type**: Text
- **Required**: Yes
- **Examples**: "dose-dense AC-T", "carboplatin-paclitaxel", "anthracycline-taxane"

### 5.9 chemo_regimen_control

- **Type**: Text
- **Required**: Yes
- **Notes**: Must match intervention arm backbone

### 5.10 anthracycline_included

- **Type**: Boolean
- **Values**: Yes / No
- **Required**: Yes

### 5.11 taxane_type

- **Type**: Categorical
- **Values**:
  - paclitaxel
  - docetaxel
  - nab_paclitaxel
  - mixed
- **Required**: Yes

### 5.12 platinum_included

- **Type**: Boolean
- **Values**: Yes / No
- **Required**: Yes

### 5.13 platinum_type

- **Type**: Categorical
- **Values**:
  - carboplatin
  - cisplatin
  - NA
- **Required**: If platinum = Yes

### 5.14 total_chemo_cycles

- **Type**: Integer
- **Required**: Yes

---

## Section 6: Primary Outcome - pCR

### 6.1 pcr_definition

- **Type**: Text
- **Required**: Yes
- **Examples**:
  - "ypT0/Tis ypN0"
  - "ypT0 ypN0"
  - "ypT0/Tis ypN0/N+"

### 6.2 pcr_intervention_n

- **Type**: Integer
- **Required**: Yes
- **Notes**: Number with pCR in intervention arm

### 6.3 pcr_intervention_total

- **Type**: Integer
- **Required**: Yes
- **Notes**: Total evaluable for pCR in intervention arm

### 6.4 pcr_control_n

- **Type**: Integer
- **Required**: Yes
- **Notes**: Number with pCR in control arm

### 6.5 pcr_control_total

- **Type**: Integer
- **Required**: Yes
- **Notes**: Total evaluable for pCR in control arm

### 6.6 pcr_rate_intervention_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: Yes
- **Calculation**: (pcr_intervention_n / pcr_intervention_total) × 100

### 6.7 pcr_rate_control_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: Yes
- **Calculation**: (pcr_control_n / pcr_control_total) × 100

### 6.8 pcr_risk_ratio

- **Type**: Numeric (decimal)
- **Required**: If reported

### 6.9 pcr_rr_95ci_lower

- **Type**: Numeric (decimal)
- **Required**: If RR reported

### 6.10 pcr_rr_95ci_upper

- **Type**: Numeric (decimal)
- **Required**: If RR reported

### 6.11 pcr_odds_ratio

- **Type**: Numeric (decimal)
- **Required**: If reported

### 6.12 pcr_or_95ci_lower

- **Type**: Numeric (decimal)
- **Required**: If OR reported

### 6.13 pcr_or_95ci_upper

- **Type**: Numeric (decimal)
- **Required**: If OR reported

### 6.14 pcr_p_value

- **Type**: Numeric (decimal)
- **Required**: If reported
- **Notes**: Record exact p-value if given (not just "<0.05")

---

## Section 7: pCR Subgroups

### 7.1 pcr_pdl1_positive_intervention_n

- **Type**: Integer
- **Required**: If PDL1 subgroup reported

### 7.2 pcr_pdl1_positive_intervention_total

- **Type**: Integer
- **Required**: If PDL1 subgroup reported

### 7.3 pcr_pdl1_positive_control_n

- **Type**: Integer
- **Required**: If PDL1 subgroup reported

### 7.4 pcr_pdl1_positive_control_total

- **Type**: Integer
- **Required**: If PDL1 subgroup reported

### 7.5 pcr_pdl1_negative_intervention_n

- **Type**: Integer
- **Required**: If PDL1 subgroup reported

### 7.6 pcr_pdl1_negative_intervention_total

- **Type**: Integer
- **Required**: If PDL1 subgroup reported

### 7.7 pcr_pdl1_negative_control_n

- **Type**: Integer
- **Required**: If PDL1 subgroup reported

### 7.8 pcr_pdl1_negative_control_total

- **Type**: Integer
- **Required**: If PDL1 subgroup reported

### 7.9 pcr_tils_high_intervention_n

- **Type**: Integer
- **Required**: If TILs subgroup reported

### 7.10 pcr_tils_high_intervention_total

- **Type**: Integer
- **Required**: If TILs subgroup reported

### 7.11 pcr_tils_high_control_n

- **Type**: Integer
- **Required**: If TILs subgroup reported

### 7.12 pcr_tils_high_control_total

- **Type**: Integer
- **Required**: If TILs subgroup reported

### 7.13 pcr_tils_low_intervention_n

- **Type**: Integer
- **Required**: If TILs subgroup reported

### 7.14 pcr_tils_low_intervention_total

- **Type**: Integer
- **Required**: If TILs subgroup reported

### 7.15 pcr_tils_low_control_n

- **Type**: Integer
- **Required**: If TILs subgroup reported

### 7.16 pcr_tils_low_control_total

- **Type**: Integer
- **Required**: If TILs subgroup reported

---

## Section 8: Event-Free Survival (EFS)

### 8.1 efs_definition

- **Type**: Text
- **Required**: If EFS reported
- **Examples**: "Time from randomization to recurrence, progression, or death"

### 8.2 efs_events_intervention

- **Type**: Integer
- **Required**: If EFS reported

### 8.3 efs_events_control

- **Type**: Integer
- **Required**: If EFS reported

### 8.4 efs_hazard_ratio

- **Type**: Numeric (decimal)
- **Required**: If EFS reported

### 8.5 efs_hr_95ci_lower

- **Type**: Numeric (decimal)
- **Required**: If EFS HR reported

### 8.6 efs_hr_95ci_upper

- **Type**: Numeric (decimal)
- **Required**: If EFS HR reported

### 8.7 efs_p_value

- **Type**: Numeric (decimal)
- **Required**: If EFS reported

### 8.8 efs_3year_intervention_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If reported

### 8.9 efs_3year_control_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If reported

### 8.10 efs_5year_intervention_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If reported

### 8.11 efs_5year_control_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If reported

---

## Section 9: Overall Survival (OS)

### 9.1 os_events_intervention

- **Type**: Integer
- **Required**: If OS reported

### 9.2 os_events_control

- **Type**: Integer
- **Required**: If OS reported

### 9.3 os_hazard_ratio

- **Type**: Numeric (decimal)
- **Required**: If OS reported

### 9.4 os_hr_95ci_lower

- **Type**: Numeric (decimal)
- **Required**: If OS HR reported

### 9.5 os_hr_95ci_upper

- **Type**: Numeric (decimal)
- **Required**: If OS HR reported

### 9.6 os_p_value

- **Type**: Numeric (decimal)
- **Required**: If OS reported

### 9.7 os_3year_intervention_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If reported

### 9.8 os_3year_control_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If reported

### 9.9 os_5year_intervention_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If reported

### 9.10 os_5year_control_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If reported

---

## Section 10: Safety Outcomes

### 10.1 ae_any_grade_intervention_n

- **Type**: Integer
- **Required**: If AE reported

### 10.2 ae_any_grade_intervention_total

- **Type**: Integer
- **Required**: If AE reported

### 10.3 ae_any_grade_control_n

- **Type**: Integer
- **Required**: If AE reported

### 10.4 ae_any_grade_control_total

- **Type**: Integer
- **Required**: If AE reported

### 10.5 ae_grade_3_4_intervention_n

- **Type**: Integer
- **Required**: Yes

### 10.6 ae_grade_3_4_intervention_total

- **Type**: Integer
- **Required**: Yes

### 10.7 ae_grade_3_4_control_n

- **Type**: Integer
- **Required**: Yes

### 10.8 ae_grade_3_4_control_total

- **Type**: Integer
- **Required**: Yes

### 10.9 ae_grade_5_intervention_n

- **Type**: Integer
- **Required**: If reported
- **Notes**: Treatment-related deaths

### 10.10 ae_grade_5_control_n

- **Type**: Integer
- **Required**: If reported

### 10.11 immune_related_ae_any_intervention_n

- **Type**: Integer
- **Required**: If irAE reported

### 10.12 immune_related_ae_any_control_n

- **Type**: Integer
- **Required**: If irAE reported

### 10.13 immune_related_ae_grade_3_4_intervention_n

- **Type**: Integer
- **Required**: If irAE reported

### 10.14 immune_related_ae_grade_3_4_control_n

- **Type**: Integer
- **Required**: If irAE reported

### 10.15 discontinuation_due_to_ae_intervention_n

- **Type**: Integer
- **Required**: If reported

### 10.16 discontinuation_due_to_ae_control_n

- **Type**: Integer
- **Required**: If reported

---

## Section 11: Surgery Outcomes

### 11.1 surgery_performed_intervention_n

- **Type**: Integer
- **Required**: If reported

### 11.2 surgery_performed_control_n

- **Type**: Integer
- **Required**: If reported

### 11.3 bcs_rate_intervention_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If reported
- **Notes**: Breast-conserving surgery rate

### 11.4 bcs_rate_control_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If reported

### 11.5 mastectomy_rate_intervention_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If reported

### 11.6 mastectomy_rate_control_percent

- **Type**: Numeric (decimal)
- **Range**: 0-100
- **Required**: If reported

---

## Section 12: Quality and Funding

### 12.1 funding_source

- **Type**: Categorical
- **Values**:
  - industry
  - government
  - mixed
  - non_profit
  - NR
- **Required**: Yes

### 12.2 industry_sponsor

- **Type**: Text
- **Examples**: "Merck", "Roche/Genentech", "AstraZeneca"
- **Required**: If industry funded

### 12.3 coi_declared

- **Type**: Boolean
- **Values**: Yes / No
- **Required**: Yes

### 12.4 trial_registration_prospective

- **Type**: Boolean
- **Values**: Yes / No
- **Required**: Yes

### 12.5 itt_analysis

- **Type**: Boolean
- **Values**: Yes / No
- **Required**: Yes

---

## Section 13: Extractor Metadata

### 13.1 extractor_initials

- **Type**: Text
- **Required**: Yes
- **Notes**: For quality control

### 13.2 extraction_date

- **Type**: Date
- **Format**: YYYY-MM-DD
- **Required**: Yes

### 13.3 extraction_method

- **Type**: Categorical
- **Values**:
  - llm_assisted
  - manual
  - dual_manual
- **Required**: Yes

### 13.4 verification_status

- **Type**: Categorical
- **Values**:
  - unverified
  - verified_single
  - verified_dual
- **Required**: Yes

### 13.5 notes

- **Type**: Long text
- **Required**: No
- **Notes**: Any clarifications, uncertainties, or discrepancies

---

## Validation Rules

### Critical Fields (Must Not Be Missing)

1. study_id
2. trial_name
3. n_randomized_total
4. ici_agent
5. chemo_regimen_intervention
6. pcr_intervention_n
7. pcr_intervention_total
8. pcr_control_n
9. pcr_control_total
10. ae_grade_3_4_intervention_n
11. ae_grade_3_4_control_n

### Cross-Field Validations

1. `n_randomized_total` should equal `n_intervention + n_control` (±5% tolerance for ITT vs modified ITT)
2. `pcr_rate_intervention_percent` should match `(pcr_intervention_n / pcr_intervention_total) × 100`
3. `pcr_rate_control_percent` should match `(pcr_control_n / pcr_control_total) × 100`
4. If `pdl1_positive_percent` is reported, `pdl1_assay` and `pdl1_cutoff` must be specified
5. `ici_total_duration_weeks` should match `(ici_neoadjuvant_cycles + ici_adjuvant_cycles) × weeks_per_cycle`

### Plausibility Checks

1. `pcr_rate_intervention_percent` should be 20-80% (typical range for TNBC + ICI)
2. `pcr_rate_control_percent` should be 15-60% (typical range for TNBC + chemo)
3. `ae_grade_3_4_intervention` should be ≥ `ae_grade_3_4_control` (ICI adds toxicity)
4. `female_percent` should be ≥98% (TNBC is rare in males)
5. `median_followup_months` should be ≥12 for survival outcomes

---

## Data Sources Priority

1. **Primary publication** (main results paper)
2. **Supplementary materials** (extended data)
3. **Protocol publication** (design details)
4. **ClinicalTrials.gov** (if publication missing data)
5. **Updated analyses** (e.g., 5-year follow-up papers)

---

## Common Pitfalls

1. **pCR definition varies**: KEYNOTE-522 uses ypT0/Tis ypN0, GeparNuevo uses ypT0 ypN0 - extract both the definition AND the data
2. **PDL1 cutoffs differ**: SP142 ≥1% IC vs 22C3 CPS≥1 - record assay and cutoff
3. **ITT vs modified ITT**: Some trials exclude patients who didn't start treatment - note which population
4. **Survival outcomes**: EFS vs DFS vs iDFS definitions vary - extract the exact definition
5. **Safety population**: May differ from ITT - record denominators

---

## Version History

- **1.0** (2026-02-07): Initial version for TNBC neoadjuvant immunotherapy meta-analysis

---

**Total fields**: 160+
**Required fields**: 45
**Estimated extraction time per study**: 15-20 minutes (manual), 5-7 minutes (LLM-assisted + verification)
