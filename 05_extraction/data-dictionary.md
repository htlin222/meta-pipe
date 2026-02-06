# Data Extraction Dictionary

**Project**: CDK4/6 Inhibitor Post-Progression Meta-Analysis
**Date**: 2026-02-06
**Version**: 1.0

---

## Study Identification

| Field              | Type    | Required | Description                                | Example                            |
| ------------------ | ------- | -------- | ------------------------------------------ | ---------------------------------- |
| `study_id`         | string  | ✅       | Unique identifier (FirstAuthorYearJournal) | `Rugo2024TROPION`                  |
| `first_author`     | string  | ✅       | Last name of first author                  | `Rugo`                             |
| `publication_year` | integer | ✅       | Year of publication                        | `2024`                             |
| `title`            | string  | ✅       | Full article title                         | `Datopotamab Deruxtecan Versus...` |
| `journal`          | string  | ✅       | Journal name                               | `Journal of Clinical Oncology`     |
| `doi`              | string  | ⚪       | Digital Object Identifier                  | `10.1200/JCO.24.00920`             |
| `pmid`             | string  | ⚪       | PubMed ID                                  | `39265124`                         |
| `trial_name`       | string  | ⚪       | Official trial name/acronym                | `TROPION-Breast01`                 |
| `registry_id`      | string  | ⚪       | ClinicalTrials.gov ID                      | `NCT05104866`                      |

---

## Study Design

| Field               | Type    | Required | Description               | Options/Example                                       |
| ------------------- | ------- | -------- | ------------------------- | ----------------------------------------------------- |
| `study_design`      | string  | ✅       | Type of study             | `RCT`, `Single-arm`, `Observational`, `Retrospective` |
| `phase`             | string  | ⚪       | Clinical trial phase      | `Phase 2`, `Phase 3`, `Phase 1/2`                     |
| `randomization`     | string  | ✅       | Randomization method      | `1:1`, `2:1`, `Not randomized`                        |
| `blinding`          | string  | ⚪       | Blinding status           | `Open-label`, `Double-blind`, `Single-blind`          |
| `multicenter`       | boolean | ⚪       | Multicenter study         | `true`, `false`                                       |
| `countries`         | string  | ⚪       | Countries where conducted | `USA, Europe, Asia`                                   |
| `enrollment_period` | string  | ⚪       | Study enrollment dates    | `2020-01 to 2022-12`                                  |

---

## Population Characteristics

### Inclusion Criteria

| Field               | Type    | Required | Description                   | Example               |
| ------------------- | ------- | -------- | ----------------------------- | --------------------- |
| `n_total`           | integer | ✅       | Total enrolled patients       | `732`                 |
| `n_cdk46_prior`     | integer | ✅       | Number with prior CDK4/6i     | `651`                 |
| `pct_cdk46_prior`   | float   | ✅       | Percentage with prior CDK4/6i | `89.0` (%)            |
| `age_median`        | float   | ⚪       | Median age (years)            | `55.0`                |
| `age_range`         | string  | ⚪       | Age range                     | `28-82`               |
| `menopausal_status` | string  | ⚪       | Post/pre/peri-menopausal mix  | `100% postmenopausal` |

### Disease Characteristics

| Field                    | Type  | Required | Description                   | Example |
| ------------------------ | ----- | -------- | ----------------------------- | ------- |
| `hr_positive_pct`        | float | ✅       | HR+ percentage                | `100.0` |
| `her2_negative_pct`      | float | ✅       | HER2- percentage              | `100.0` |
| `metastatic_pct`         | float | ✅       | Metastatic disease percentage | `100.0` |
| `visceral_mets_pct`      | float | ⚪       | Visceral metastases           | `65.0`  |
| `bone_only_pct`          | float | ⚪       | Bone-only metastases          | `15.0`  |
| `brain_mets_pct`         | float | ⚪       | Brain metastases              | `5.0`   |
| `de_novo_metastatic_pct` | float | ⚪       | De novo metastatic            | `35.0`  |

### Prior CDK4/6 Inhibitor Details

| Field                         | Type   | Required | Description                         | Example                              |
| ----------------------------- | ------ | -------- | ----------------------------------- | ------------------------------------ |
| `cdk46_type`                  | string | ✅       | Prior CDK4/6i type(s)               | `Palbociclib`, `Ribociclib`, `Mixed` |
| `cdk46_line`                  | string | ✅       | Line of prior CDK4/6i               | `1st-line`, `2nd-line`, `Mixed`      |
| `cdk46_setting`               | string | ✅       | Setting of prior CDK4/6i            | `Metastatic`, `Adjuvant`, `Mixed`    |
| `cdk46_duration_median`       | float  | ⚪       | Median duration on CDK4/6i (months) | `18.5`                               |
| `progression_on_cdk46_pct`    | float  | ⚪       | Progressed ON CDK4/6i               | `75.0`                               |
| `progression_after_cdk46_pct` | float  | ⚪       | Progressed AFTER CDK4/6i            | `25.0`                               |

### Prior Therapies

| Field                          | Type  | Required | Description                  | Example |
| ------------------------------ | ----- | -------- | ---------------------------- | ------- |
| `prior_chemo_lines_median`     | float | ⚪       | Median prior chemo lines     | `2.0`   |
| `prior_chemo_metastatic_pct`   | float | ⚪       | Prior chemo for metastatic   | `45.0`  |
| `prior_endocrine_lines_median` | float | ⚪       | Median prior endocrine lines | `2.0`   |

---

## Intervention Details

### Treatment Arms

| Field            | Type    | Required | Description           | Example                     |
| ---------------- | ------- | -------- | --------------------- | --------------------------- |
| `arm_1_name`     | string  | ✅       | Experimental arm name | `Datopotamab deruxtecan`    |
| `arm_1_category` | string  | ✅       | Treatment category    | `ADC`, `mTOR`, `SERD`, etc. |
| `arm_1_dose`     | string  | ✅       | Dose and schedule     | `6 mg/kg IV Q3W`            |
| `arm_1_n`        | integer | ✅       | Number randomized     | `366`                       |
| `arm_2_name`     | string  | ⚪       | Control arm name      | `Chemotherapy (TPC)`        |
| `arm_2_category` | string  | ⚪       | Treatment category    | `Chemotherapy`              |
| `arm_2_dose`     | string  | ⚪       | Dose and schedule     | `Various per TPC`           |
| `arm_2_n`        | integer | ⚪       | Number randomized     | `366`                       |

### Treatment Categories

**Use these standardized categories**:

- `ADC` - Antibody-drug conjugate
- `SERD` - Selective estrogen receptor degrader
- `mTOR` - mTOR inhibitor
- `PIK3CA` - PIK3CA inhibitor
- `CDK46_continue` - CDK4/6 inhibitor continuation
- `CDK46_switch` - Switch to different CDK4/6i
- `AKT` - AKT inhibitor
- `Chemotherapy` - Standard chemotherapy
- `Endocrine_alone` - Endocrine monotherapy

---

## Outcomes

### Primary Endpoint

| Field              | Type   | Required | Description               | Example       |
| ------------------ | ------ | -------- | ------------------------- | ------------- |
| `primary_endpoint` | string | ✅       | Primary endpoint          | `PFS by BICR` |
| `pfs_median_arm1`  | float  | ✅       | Median PFS arm 1 (months) | `6.9`         |
| `pfs_median_arm2`  | float  | ⚪       | Median PFS arm 2 (months) | `4.9`         |
| `pfs_hr`           | float  | ✅       | Hazard ratio for PFS      | `0.63`        |
| `pfs_ci_lower`     | float  | ✅       | 95% CI lower bound        | `0.52`        |
| `pfs_ci_upper`     | float  | ✅       | 95% CI upper bound        | `0.76`        |
| `pfs_p_value`      | float  | ✅       | P-value for PFS           | `0.00001`     |

### Secondary Endpoints

| Field            | Type  | Required | Description                       | Example |
| ---------------- | ----- | -------- | --------------------------------- | ------- |
| `os_median_arm1` | float | ⚪       | Median OS arm 1 (months)          | `18.5`  |
| `os_median_arm2` | float | ⚪       | Median OS arm 2 (months)          | `15.2`  |
| `os_hr`          | float | ⚪       | Hazard ratio for OS               | `0.84`  |
| `os_ci_lower`    | float | ⚪       | 95% CI lower bound                | `0.70`  |
| `os_ci_upper`    | float | ⚪       | 95% CI upper bound                | `1.01`  |
| `os_p_value`     | float | ⚪       | P-value for OS                    | `0.058` |
| `orr_arm1`       | float | ⚪       | Objective response rate arm 1 (%) | `36.0`  |
| `orr_arm2`       | float | ⚪       | Objective response rate arm 2 (%) | `22.0`  |
| `cbr_arm1`       | float | ⚪       | Clinical benefit rate arm 1 (%)   | `52.0`  |
| `cbr_arm2`       | float | ⚪       | Clinical benefit rate arm 2 (%)   | `38.0`  |

### Follow-up

| Field              | Type   | Required | Description               | Example      |
| ------------------ | ------ | -------- | ------------------------- | ------------ |
| `followup_median`  | float  | ⚪       | Median follow-up (months) | `12.5`       |
| `data_cutoff_date` | string | ⚪       | Data cutoff date          | `2023-06-30` |

---

## Safety

### Adverse Events

| Field                           | Type    | Required | Description                    | Example |
| ------------------------------- | ------- | -------- | ------------------------------ | ------- |
| `ae_any_grade_arm1_pct`         | float   | ⚪       | Any grade AE arm 1 (%)         | `98.0`  |
| `ae_grade3plus_arm1_pct`        | float   | ⚪       | Grade ≥3 AE arm 1 (%)          | `52.0`  |
| `ae_any_grade_arm2_pct`         | float   | ⚪       | Any grade AE arm 2 (%)         | `96.0`  |
| `ae_grade3plus_arm2_pct`        | float   | ⚪       | Grade ≥3 AE arm 2 (%)          | `38.0`  |
| `sae_arm1_pct`                  | float   | ⚪       | Serious AE arm 1 (%)           | `28.0`  |
| `sae_arm2_pct`                  | float   | ⚪       | Serious AE arm 2 (%)           | `22.0`  |
| `discontinuation_ae_arm1_pct`   | float   | ⚪       | D/C due to AE arm 1 (%)        | `8.0`   |
| `discontinuation_ae_arm2_pct`   | float   | ⚪       | D/C due to AE arm 2 (%)        | `5.0`   |
| `treatment_related_deaths_arm1` | integer | ⚪       | Treatment-related deaths arm 1 | `2`     |
| `treatment_related_deaths_arm2` | integer | ⚪       | Treatment-related deaths arm 2 | `1`     |

### Common Adverse Events (≥20% in either arm)

**Extract as separate list**:

- `ae_name`: Name of adverse event
- `ae_any_arm1_pct`: Any grade in arm 1 (%)
- `ae_grade3plus_arm1_pct`: Grade ≥3 in arm 1 (%)
- `ae_any_arm2_pct`: Any grade in arm 2 (%)
- `ae_grade3plus_arm2_pct`: Grade ≥3 in arm 2 (%)

---

## Subgroup Analyses

### CDK4/6 Inhibitor Subgroups

| Field                                   | Type    | Required | Description                | Example |
| --------------------------------------- | ------- | -------- | -------------------------- | ------- |
| `subgroup_cdk46_type_available`         | boolean | ⚪       | Subgroup by CDK4/6i type   | `true`  |
| `subgroup_cdk46_line_available`         | boolean | ⚪       | Subgroup by treatment line | `true`  |
| `subgroup_progression_timing_available` | boolean | ⚪       | ON vs AFTER CDK4/6i        | `true`  |

### Biomarker Subgroups

| Field                                | Type    | Required | Description              | Example |
| ------------------------------------ | ------- | -------- | ------------------------ | ------- |
| `subgroup_esr1_mutation_available`   | boolean | ⚪       | ESR1 mutation subgroup   | `true`  |
| `subgroup_pik3ca_mutation_available` | boolean | ⚪       | PIK3CA mutation subgroup | `false` |

### Clinical Subgroups

| Field                              | Type    | Required | Description            | Example |
| ---------------------------------- | ------- | -------- | ---------------------- | ------- |
| `subgroup_visceral_mets_available` | boolean | ⚪       | Visceral mets subgroup | `true`  |
| `subgroup_prior_chemo_available`   | boolean | ⚪       | Prior chemo subgroup   | `true`  |

---

## Quality Assessment

### Risk of Bias (Cochrane RoB 2)

| Field                     | Type   | Required | Description                 | Options                        |
| ------------------------- | ------ | -------- | --------------------------- | ------------------------------ |
| `rob_randomization`       | string | ✅       | Bias from randomization     | `Low`, `Some concerns`, `High` |
| `rob_deviations`          | string | ✅       | Bias from deviations        | `Low`, `Some concerns`, `High` |
| `rob_missing_data`        | string | ✅       | Bias from missing data      | `Low`, `Some concerns`, `High` |
| `rob_outcome_measurement` | string | ✅       | Bias in outcome measurement | `Low`, `Some concerns`, `High` |
| `rob_selective_reporting` | string | ✅       | Bias in selective reporting | `Low`, `Some concerns`, `High` |
| `rob_overall`             | string | ✅       | Overall risk of bias        | `Low`, `Some concerns`, `High` |

---

## Notes

| Field                | Type | Required | Description                | Example                                |
| -------------------- | ---- | -------- | -------------------------- | -------------------------------------- |
| `notes_population`   | text | ⚪       | Special population notes   | `Excluded patients with brain mets`    |
| `notes_intervention` | text | ⚪       | Special intervention notes | `Dose reductions allowed`              |
| `notes_outcomes`     | text | ⚪       | Special outcome notes      | `PFS by investigator longer than BICR` |
| `notes_quality`      | text | ⚪       | Quality/bias notes         | `Industry sponsored, open-label`       |
| `notes_general`      | text | ⚪       | General notes              | `Abstract only, full text pending`     |

---

## Extraction Guidelines

### Required Fields

**Minimum data for inclusion**:

- Study identification (study_id, first_author, year, title)
- Population (n_total, n_cdk46_prior, pct_cdk46_prior)
- Intervention (arm_1_name, arm_1_category, arm_1_n)
- Primary outcome (pfs_hr, pfs_ci_lower, pfs_ci_upper, pfs_p_value)
- Quality assessment (rob_overall)

### Missing Data

**How to handle**:

- Leave blank if not reported
- Use `NR` (Not Reported) for critical missing data
- Use `NA` (Not Applicable) if not relevant to study design
- Add note in `notes_*` fields explaining missing data

### Subgroup Data

**If reported**:

- Extract hazard ratios for CDK4/6i subgroups
- Note interaction p-values
- Priority: Prior CDK4/6i type, line, and progression timing

### Multi-Arm Trials

**If >2 arms**:

- Extract all relevant comparisons
- Create separate rows for each comparison
- Use `study_id_arm1vsarm2` format

---

## Validation Rules

### Consistency Checks

1. **Sample sizes**: `n_cdk46_prior` ≤ `n_total`
2. **Percentages**: All percentages 0-100
3. **Confidence intervals**: `ci_lower` < `HR` < `ci_upper`
4. **P-values**: 0-1 range
5. **Treatment categories**: Must match predefined list

### Completeness Checks

1. **All required fields** filled
2. **HR with CI and p-value** (all or none)
3. **Both arms** if RCT (arm_1 and arm_2)
4. **Risk of bias** domains assessed

---

## Example Entry

```json
{
  "study_id": "Rugo2024TROPION",
  "first_author": "Rugo",
  "publication_year": 2024,
  "title": "Datopotamab Deruxtecan Versus Chemotherapy in Previously Treated HR+/HER2- Metastatic Breast Cancer",
  "journal": "Journal of Clinical Oncology",
  "doi": "10.1200/JCO.24.00920",
  "trial_name": "TROPION-Breast01",

  "study_design": "RCT",
  "phase": "Phase 3",
  "randomization": "1:1",
  "blinding": "Open-label",

  "n_total": 732,
  "n_cdk46_prior": 651,
  "pct_cdk46_prior": 89.0,
  "age_median": 55.0,

  "arm_1_name": "Datopotamab deruxtecan",
  "arm_1_category": "ADC",
  "arm_1_dose": "6 mg/kg IV Q3W",
  "arm_1_n": 366,
  "arm_2_name": "Chemotherapy (TPC)",
  "arm_2_category": "Chemotherapy",
  "arm_2_n": 366,

  "primary_endpoint": "PFS by BICR",
  "pfs_median_arm1": 6.9,
  "pfs_median_arm2": 4.9,
  "pfs_hr": 0.63,
  "pfs_ci_lower": 0.52,
  "pfs_ci_upper": 0.76,
  "pfs_p_value": 0.00001,

  "rob_overall": "Some concerns"
}
```

---

**End of Data Dictionary**
**Version**: 1.0
**Last Updated**: 2026-02-06
