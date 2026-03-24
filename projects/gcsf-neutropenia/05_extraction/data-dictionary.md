# Data Dictionary: extraction.csv

**Project**: gcsf-neutropenia
**Date**: 2026-03-24
**Round**: 01
**Extractor**: AI-assisted (Claude)

---

## Study Identification

| Column | Type | Description | Coding Rules |
|--------|------|-------------|--------------|
| `study_id` | string | Unique study identifier | FirstAuthorYear format (e.g., Crawford1991) |
| `first_author` | string | Last name of first author | As listed in publication |
| `year` | integer | Publication year | YYYY format |
| `journal` | string | Full journal name | No abbreviations |

## Study Characteristics

| Column | Type | Description | Coding Rules |
|--------|------|-------------|--------------|
| `country` | string | Country/region of conduct | Country name or "multinational" |
| `setting` | string | Clinical setting | "single-center" or "multicenter" |
| `cancer_type` | string | Primary cancer type | SCLC, breast cancer, NHL, colorectal cancer, multiple myeloma |
| `chemotherapy_regimen` | string | Chemotherapy protocol | Standard abbreviation with full name in parentheses for first occurrence |

## Sample Size

| Column | Type | Unit | Description | Coding Rules |
|--------|------|------|-------------|--------------|
| `n_total` | integer | patients | Total randomized patients | ITT population; sum of all arms |
| `n_intervention` | integer | patients | Patients in G-CSF arm | Number randomized to active G-CSF |
| `n_control` | integer | patients | Patients in comparator arm | Number randomized to control/comparator |

## Interventions

| Column | Type | Description | Coding Rules |
|--------|------|-------------|--------------|
| `intervention` | string | G-CSF agent, dose, route | Format: "agent dose route" (e.g., "filgrastim 5mcg/kg/day SC") |
| `comparator` | string | Control treatment | "placebo", "no GCSF (standard care)", or active comparator with dose |

## Primary Outcome: Febrile Neutropenia

| Column | Type | Unit | Description | Coding Rules | Source |
|--------|------|------|-------------|--------------|--------|
| `fn_events_intervention` | integer | events | FN events in G-CSF arm | Number of patients with at least 1 FN episode | Publication tables/text |
| `fn_events_control` | integer | events | FN events in control arm | Number of patients with at least 1 FN episode | Publication tables/text |
| `fn_rr` | float | ratio | Risk ratio for FN | Intervention vs control; values <1 favor intervention | Reported or calculated from events/N |
| `fn_rr_lci` | float | ratio | RR lower 95% CI bound | Lower bound of 95% confidence interval | Reported or calculated |
| `fn_rr_uci` | float | ratio | RR upper 95% CI bound | Upper bound of 95% confidence interval | Reported or calculated |

## Secondary Outcome: Overall Survival

| Column | Type | Unit | Description | Coding Rules | Source |
|--------|------|------|-------------|--------------|--------|
| `os_hr` | float | ratio | Hazard ratio for OS | Values <1 favor intervention; blank if not reported | Publication |
| `os_hr_lci` | float | ratio | HR lower 95% CI bound | Blank if OS HR not reported | Publication |
| `os_hr_uci` | float | ratio | HR upper 95% CI bound | Blank if OS HR not reported | Publication |

## Secondary Outcome: Infection-Related Mortality

| Column | Type | Unit | Description | Coding Rules |
|--------|------|------|-------------|--------------|
| `infection_mortality_events_int` | integer | events | Infection deaths in G-CSF arm | Count of patients; 0 if none reported |
| `infection_mortality_events_ctrl` | integer | events | Infection deaths in control arm | Count of patients; 0 if none reported |

## Secondary Outcome: Hospitalization

| Column | Type | Unit | Description | Coding Rules |
|--------|------|------|-------------|--------------|
| `hospitalization_events_int` | integer | events | FN hospitalizations in G-CSF arm | Count of patients hospitalized for FN |
| `hospitalization_events_ctrl` | integer | events | FN hospitalizations in control arm | Count of patients hospitalized for FN |

## Secondary Outcome: Neutrophil Recovery

| Column | Type | Unit | Description | Coding Rules |
|--------|------|------|-------------|--------------|
| `neutrophil_recovery_days_int` | float | days | ANC recovery time in G-CSF arm | Mean days from nadir to ANC >= 0.5 x 10^9/L; cycle 1 preferred |
| `neutrophil_recovery_days_ctrl` | float | days | ANC recovery time in control arm | Mean days from nadir to ANC >= 0.5 x 10^9/L; cycle 1 preferred |

## Secondary Outcome: Adverse Events

| Column | Type | Unit | Description | Coding Rules |
|--------|------|------|-------------|--------------|
| `adverse_events_bone_pain_int` | integer | events | Bone pain events in G-CSF arm | Count of patients reporting any-grade bone pain |
| `adverse_events_bone_pain_ctrl` | integer | events | Bone pain events in control arm | Count of patients; 0 for no-GCSF arms where not applicable |

## Secondary Outcome: Relative Dose Intensity

| Column | Type | Unit | Description | Coding Rules |
|--------|------|------|-------------|--------------|
| `rdi_mean_int` | float | % | Mean RDI in G-CSF arm | Percentage (0-100); blank if not reported |
| `rdi_mean_ctrl` | float | % | Mean RDI in control arm | Percentage (0-100); blank if not reported |

## Risk of Bias & Study Design

| Column | Type | Description | Coding Rules |
|--------|------|-------------|--------------|
| `risk_of_bias_overall` | string | Overall RoB 2.0 judgment | "low", "some_concerns", or "high" |
| `study_phase` | string | Clinical trial phase | "II" or "III" |
| `blinding` | string | Blinding status | "double-blind" or "open-label" |
| `allocation_concealment` | string | Concealment adequacy | "adequate", "unclear", or "inadequate" |
| `followup_duration` | string | Duration of follow-up | Free text: cycles, weeks, or months |
| `primary_prophylaxis` | string | Primary vs secondary G-CSF | "yes" (primary) or "no" (secondary) |

## NMA Classification

| Column | Type | Description | Coding Rules |
|--------|------|-------------|--------------|
| `nma_comparison` | string | Treatment comparison for NMA | Format: "treatment1_vs_treatment2" using NMA node names: filgrastim, pegfilgrastim, lipegfilgrastim, placebo |

---

## NMA Treatment Nodes

| Node | Definition | Studies |
|------|-----------|---------|
| `filgrastim` | Filgrastim (Neupogen) or biosimilar, any dose, daily SC | Crawford1991, Trillet-Lenoir1993, Pettengell1992, TimmerBonte2005, delGiglio2008, Doorduijn2003 |
| `pegfilgrastim` | Pegfilgrastim (Neulasta), single SC dose per cycle | Vogel2005, Balducci2007, Hecht2010, Romieu2007, Kosaka2015, Hegg2016, Bozzoli2015 |
| `lipegfilgrastim` | Lipegfilgrastim (Lonquex), single SC dose per cycle | Bondarenko2013, Buchner2014 |
| `placebo` | Placebo, no GCSF, or standard care without GCSF | Used as comparator node |

## Head-to-Head Comparisons (for NMA connectivity)

| Comparison | Studies |
|-----------|---------|
| filgrastim vs placebo | Crawford1991, Trillet-Lenoir1993, Pettengell1992, TimmerBonte2005, delGiglio2008, Doorduijn2003 |
| pegfilgrastim vs placebo | Vogel2005, Balducci2007, Hecht2010, Romieu2007, Kosaka2015, Hegg2016, Bozzoli2015 |
| pegfilgrastim vs filgrastim | Holmes2002, Green2003, Grigg2003 |
| lipegfilgrastim vs pegfilgrastim | Bondarenko2013, Buchner2014 |

## Missing Data Conventions

- Empty cell: outcome not reported in the study
- `0`: explicitly reported as zero events
- All numeric fields use period (`.`) as decimal separator

## Data Sources

- Primary: Published manuscript (main text, tables, figures)
- Secondary: Supplementary materials, ClinicalTrials.gov registry data
- Tertiary: Cochrane systematic reviews for cross-validation (Mhaskar 2014, Cooper 2011, Lyman 2002)
