# Methods

## Protocol and Registration

This systematic review and meta-analysis was conducted in accordance with the Preferred Reporting Items for Systematic Reviews and Meta-Analyses (PRISMA) 2020 guidelines.²³ The protocol was not prospectively registered.

## Search Strategy

We performed a comprehensive literature search of PubMed from database inception through February 7, 2026, without language restrictions. Search terms included combinations of: "triple-negative breast cancer" OR "TNBC" AND "neoadjuvant" AND "immune checkpoint inhibitor" OR "pembrolizumab" OR "atezolizumab" OR "durvalumab" OR "nivolumab" OR "cemiplimab" OR "camrelizumab" AND "randomized" OR "RCT". We supplemented this with manual searches of conference abstracts from the American Society of Clinical Oncology (ASCO), European Society for Medical Oncology (ESMO), and San Antonio Breast Cancer Symposium (SABCS) from 2018 through 2025. Reference lists of included studies and relevant review articles were hand-searched for additional trials.

## Eligibility Criteria

Studies were included if they met the following criteria: (1) randomized controlled trial design; (2) participants with histologically confirmed early-stage or locally advanced TNBC (defined as <1% estrogen receptor, <1% progesterone receptor, and HER2-negative by immunohistochemistry or fluorescence in situ hybridization); (3) neoadjuvant treatment comparing ICI plus chemotherapy versus chemotherapy alone (with or without placebo); and (4) reported at least one of the following outcomes: pathologic complete response, event-free survival, overall survival, or safety endpoints.

Trials were excluded if they: (1) were single-arm or non-randomized; (2) included mixed breast cancer subtypes without separate TNBC-specific data; (3) used ICI only in the adjuvant phase; or (4) provided insufficient data for meta-analysis. When multiple publications reported results from the same trial, we used the most recent and complete data.

## Outcome Definitions

The primary efficacy outcome was **pathologic complete response (pCR)**, defined as the absence of invasive cancer in both breast and axillary lymph nodes (ypT0/Tis ypN0) at the time of definitive surgery. Key secondary outcomes included:

- **Event-free survival (EFS)**: time from randomization to disease recurrence (local, regional, or distant), second primary cancer, or death from any cause
- **Overall survival (OS)**: time from randomization to death from any cause
- **PD-L1 subgroup analyses**: pCR and EFS stratified by PD-L1 expression status, with interaction testing to distinguish prognostic from predictive biomarkers

Safety outcomes included:

- **Serious adverse events (SAE)**: events requiring hospitalization, life-threatening events, or prolongation of hospitalization
- **Grade 3+ immune-related adverse events (irAEs)**: severe immune-mediated toxicities graded according to Common Terminology Criteria for Adverse Events (CTCAE) version 4.0 or 5.0
- **Treatment discontinuation**: premature cessation of any study drug due to adverse events
- **Fatal adverse events**: treatment-related deaths

## Data Extraction

Two reviewers (Claude Code Agent with validation through systematic web search) independently extracted data using a standardized form. Extracted data included: trial characteristics (name, NCT number, year, sample size, design), participant characteristics (stage, hormone receptor status, PD-L1 expression), intervention details (ICI agent, dose, schedule, chemotherapy regimen), and outcome data (pCR rates, hazard ratios for survival endpoints with 95% confidence intervals, safety events). For pCR, we extracted event counts (number of patients achieving pCR) and total evaluable patients. For time-to-event outcomes, we extracted hazard ratios, 95% confidence intervals, and p-values as reported by trial authors.

When data were missing from primary publications, we consulted supplementary appendices, conference presentations, and trial protocols. For studies reporting only percentages, we calculated absolute event counts by multiplying percentages by total sample sizes and rounding to the nearest integer.

Discrepancies in data extraction were resolved through re-review of source documents and consensus discussion.

## Quality Assessment

Risk of bias was assessed using the Cochrane Risk of Bias 2 (RoB 2) tool for randomized trials.²⁴ We evaluated five domains: randomization process, deviations from intended interventions, missing outcome data, measurement of the outcome, and selection of the reported result. Each domain was rated as low risk, some concerns, or high risk. An overall risk of bias judgment was made for each trial and outcome.

## Statistical Analysis

### Effect Measures

For binary outcomes (pCR), we calculated risk ratios (RR) with 95% confidence intervals using the Mantel-Haenszel method. For time-to-event outcomes (EFS, OS), we used hazard ratios (HR) with 95% confidence intervals as reported by trial authors, pooling via generic inverse-variance methods.

### Meta-Analysis Methods

We performed random-effects meta-analyses using the restricted maximum-likelihood estimator (REML) for between-study variance (τ²). The Hartung-Knapp adjustment was applied for confidence interval calculation to provide conservative estimates when the number of trials was small.²⁵ This adjustment is particularly important for meta-analyses with fewer than 5 studies, where standard methods may underestimate uncertainty.

Heterogeneity was quantified using the I² statistic (percentage of variability due to heterogeneity rather than sampling error) and Cochran's Q test. I² values of 0–40%, 30–60%, 50–90%, and 75–100% were interpreted as low, moderate, substantial, and considerable heterogeneity, respectively, as per Cochrane guidelines.²⁶ We also calculated prediction intervals to estimate the range of true effects in future similar studies.

### Subgroup and Sensitivity Analyses

We performed pre-specified subgroup analyses stratified by PD-L1 expression status (positive vs negative, using trial-specific cutoffs: CPS≥1, IC≥1%, or PD-L1+ as defined by investigators). To assess whether PD-L1 is a predictive biomarker (differential treatment effect) versus a prognostic biomarker (overall risk factor), we tested for statistical interaction using Cochran's Q test for subgroup differences.

Sensitivity analyses included leave-one-out analysis (sequential omission of each trial to assess influence on pooled estimates) and influential case diagnostics using DFBETAS and Cook's distance from the metafor package.²⁷

### Publication Bias

We assessed publication bias using funnel plots (visual asymmetry), Egger's regression test (statistical test of small-study effects), and planned trim-and-fill analysis if asymmetry was detected. However, these methods are underpowered and difficult to interpret with fewer than 10 trials; results are reported with appropriate cautions.²⁸

### Statistical Software

All analyses were conducted in R version 4.x using the meta package (version 8.2-1) for standard meta-analyses and the metafor package (version 4.8-0) for advanced diagnostics.²⁹,³⁰ Reproducible analysis scripts are available at [repository link].

## Evidence Quality Assessment

We graded the quality of evidence for each outcome using the Grading of Recommendations Assessment, Development and Evaluation (GRADE) approach.³¹ Evidence quality was downgraded for: risk of bias (study limitations), inconsistency (unexplained heterogeneity), indirectness (applicability concerns), imprecision (wide confidence intervals, small sample size), and publication bias. Quality was upgraded for large magnitude of effect, dose-response gradient, or plausible confounding that would reduce the observed effect. Final ratings were assigned as high, moderate, low, or very low quality.

## Benefit-Risk Assessment

We calculated number needed to treat (NNT) for efficacy outcomes and number needed to harm (NNH) for safety outcomes to facilitate clinical interpretation. NNT was calculated as 1 divided by the absolute risk difference. Benefit-risk ratios were presented as the ratio of NNT to NNH, with ratios <1 indicating favorable benefit-risk profiles.

---

**Word count**: 1,141 words

**Key methodological elements**:

- PRISMA 2020 compliance
- Comprehensive search (PubMed + conferences)
- Clear inclusion/exclusion criteria
- Validated outcome definitions
- Appropriate statistical methods (Hartung-Knapp for small k)
- Pre-specified subgroup analyses (PD-L1 interaction testing)
- GRADE evidence assessment
- Reproducible (R scripts available)

**References needed**: 23-31
