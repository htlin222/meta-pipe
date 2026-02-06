# Full-Text Review Guide

**Study:** Post-CDK4/6 Treatment Strategies in HR+/HER2- Metastatic Breast Cancer
**Stage:** 04 - Full-Text Assessment
**Records to Review:** 52 (26 Include + 26 Uncertain from title/abstract screening)
**Date:** 2026-02-06

---

## Overview

This guide provides detailed instructions for reviewing full-text articles to determine final inclusion/exclusion for the systematic review and network meta-analysis.

**Critical Reference Documents:**

- **Eligibility Criteria:** `01_protocol/eligibility.md`
- **PICO Framework:** `01_protocol/pico.yaml`
- **Screening Results:** `03_screening/round-01/decisions_screened_r1.csv`

---

## Workflow

```
PDF Retrieved → Read Full-Text → Apply Detailed Criteria → Make Decision (I/E) → Document Reason
```

### Step-by-Step Process:

1. **Retrieve PDF** (see PDF Retrieval Strategy below)
2. **Read full-text** focusing on:
   - Methods section (population, intervention, design)
   - Results section (sample size, outcomes)
   - Supplementary materials (subgroup data)
3. **Extract key information**:
   - % of patients with prior CDK4/6i
   - Study design (Phase II/III, RCT, cohort)
   - Sample size (total and post-CDK4/6 subgroup)
   - Outcomes reported (PFS, OS, ORR, safety)
4. **Apply detailed eligibility criteria** (see below)
5. **Make final decision**: Include (I) or Exclude (E)
6. **Document reason** if excluded
7. **Update CSV**: `fulltext_decisions.csv`

---

## Detailed Eligibility Criteria

### ✅ INCLUDE if ALL of the following:

#### 1. Population Criteria

**MUST have:**

- HR+ (ER+ and/or PR+) breast cancer (≥1% by IHC)
- HER2-negative (IHC 0-1+ or FISH non-amplified)
- Advanced or metastatic disease (stage IIIB/IIIC/IV)
- **≥50% of patients** had prior CDK4/6 inhibitor therapy
  - OR: Post-CDK4/6 subgroup explicitly analyzed and reported separately
- Disease progression on or after CDK4/6 inhibitor (RECIST v1.1 or clinical progression)

**Special Cases:**

- **Mixed population (some CDK4/6-naïve):** INCLUDE if:
  - ≥50% had prior CDK4/6i AND subgroup data extractable, OR
  - Post-CDK4/6 subgroup analyzed separately with n ≥20

- **SOLAR-1, EMERALD:** INCLUDE even if <50% had prior CDK4/6i IF:
  - Stratified by prior CDK4/6i AND subgroup results reported separately

#### 2. Intervention Criteria

**MUST be one of:**

- CDK4/6 inhibitor continuation/switching (different CDK4/6i + ET)
- mTOR inhibitors (everolimus + exemestane/fulvestrant)
- Antibody-drug conjugates (sacituzumab govitecan, datopotamab deruxtecan, etc.)
- Novel endocrine therapy (elacestrant, imlunestrant, oral SERDs)
- PI3K/AKT inhibitors (capivasertib, alpelisib, ipatasertib)
- Chemotherapy (single-agent or combination)

**Timing:** Treatment given **AFTER** CDK4/6 inhibitor progression

#### 3. Study Design Criteria

**MUST be one of:**

- Phase II or III randomized controlled trial (RCT)
- Post-hoc analysis of RCT with post-CDK4/6 subgroup (n ≥20)
- Prospective cohort study with **n ≥100** (real-world evidence)

**Comparator required:**

- At least 2 arms (intervention vs control, or intervention vs active comparator)
- Single-arm trials: EXCLUDE (unless part of network with external control)

#### 4. Outcomes Criteria

**MUST report ≥1 of:**

- **Efficacy:**
  - Progression-Free Survival (PFS) - HR with 95% CI or median with KM curve
  - Overall Survival (OS) - HR with 95% CI or median with KM curve
  - Objective Response Rate (ORR) - n/N or percentage
  - Clinical Benefit Rate (CBR) - n/N or percentage

- **Safety:**
  - Grade 3-4 adverse events (overall or specific)
  - Treatment discontinuation due to AEs
  - Treatment-related deaths

**Minimum follow-up:** ≥3 months median

---

### ❌ EXCLUDE if ANY of the following:

#### Population Exclusions

| Code      | Reason                                                   | Example                                                        |
| --------- | -------------------------------------------------------- | -------------------------------------------------------------- |
| **FT-P1** | HER2-positive or TNBC                                    | Study includes HER2+ patients                                  |
| **FT-P2** | Early-stage only (no metastatic component)               | Adjuvant/neoadjuvant trials without metastatic recurrence data |
| **FT-P3** | <50% had prior CDK4/6i AND no separate subgroup analysis | Mixed population, no post-CDK4/6 subgroup reported             |
| **FT-P4** | Sample size too small (<20 in post-CDK4/6 subgroup)      | n=15 post-CDK4/6 patients                                      |

#### Intervention Exclusions

| Code      | Reason                                     | Example                                        |
| --------- | ------------------------------------------ | ---------------------------------------------- |
| **FT-I1** | Treatment given BEFORE CDK4/6i progression | First-line CDK4/6i trial (PALOMA-2, MONARCH 3) |
| **FT-I2** | Not a systemic therapy                     | Radiation therapy alone, surgery only          |

#### Design Exclusions

| Code      | Reason                                                | Example                                          |
| --------- | ----------------------------------------------------- | ------------------------------------------------ |
| **FT-D1** | Phase I dose-escalation only                          | Safety/pharmacokinetics study, no efficacy data  |
| **FT-D2** | Retrospective study with high bias                    | No adjustment for confounding, >20% missing data |
| **FT-D3** | Single-arm trial without comparator                   | No control group, not part of network            |
| **FT-D4** | Conference abstract only (>2 years old, no full-text) | ASCO 2022 abstract, no subsequent publication    |

#### Outcome Exclusions

| Code      | Reason                           | Example                                                    |
| --------- | -------------------------------- | ---------------------------------------------------------- |
| **FT-O1** | No efficacy or safety outcomes   | Biomarker-only study (e.g., ctDNA analysis without PFS/OS) |
| **FT-O2** | Follow-up <3 months              | Median follow-up 2 months                                  |
| **FT-O3** | Insufficient data for extraction | HR reported without 95% CI, no KM curve, no raw counts     |

#### Other Exclusions

| Code        | Reason                                  | Example                                    |
| ----------- | --------------------------------------- | ------------------------------------------ |
| **FT-DUP**  | Duplicate publication of same data      | Earlier publication of same trial          |
| **FT-LANG** | Non-English/non-Chinese, no translation | Article in French with no English abstract |

---

## Special Scenarios & Decisions

### Scenario 1: Post-CDK4/6 Subgroup in Larger Trial

**Example:** BOLERO-2 enrolled CDK4/6-naïve patients, but real-world studies report outcomes in post-CDK4/6 subsets.

**Decision:**

- **INCLUDE** if:
  - Post-CDK4/6 subgroup n ≥20
  - Hazard ratios or effect estimates reported separately for post-CDK4/6 patients
  - Clear definition of "prior CDK4/6i"

- **EXCLUDE** if:
  - Post-CDK4/6 subgroup n <20
  - No separate analysis, only mentioned in discussion
  - Cannot extract data specific to post-CDK4/6 patients

### Scenario 2: Conference Abstract vs Full-Text

**Decision:**

- **INCLUDE** if:
  - Full-text published within 2 years of abstract
  - Use most recent/complete publication

- **EXCLUDE** if:
  - Abstract >2 years old, no full-text available
  - Contacted authors, no response within 4 weeks
  - Code as **FT-D4**

### Scenario 3: Mixed CDK4/6-Naïve and Post-CDK4/6 Population

**Example:** Trial enrolls both CDK4/6-naïve and post-CDK4/6 patients.

**Decision:**

- **INCLUDE** if:
  - ≥50% had prior CDK4/6i, OR
  - Stratified by prior CDK4/6i with subgroup analysis, OR
  - Post-CDK4/6 cohort analyzed separately (n ≥20)

- **EXCLUDE** if:
  - <50% had prior CDK4/6i AND no subgroup analysis
  - Code as **FT-P3**

### Scenario 4: Real-World Evidence (RWE) Studies

**Decision:**

- **INCLUDE** if:
  - Prospective design or high-quality retrospective with:
    - n ≥100 in post-CDK4/6 cohort
    - Adjustment for confounding (propensity score, multivariable regression)
    - Missing data <20%
    - Clear exposure definition (CDK4/6i type, duration)

- **EXCLUDE** if:
  - Retrospective, no adjustment for confounding
  - High missing data (>20%)
  - Selection bias evident
  - Code as **FT-D2**

### Scenario 5: Multiple Publications from Same Trial

**Example:** TROPiCS-02 has primary PFS publication (2023) and OS update (2024).

**Decision:**

- **INCLUDE** most recent/complete publication
- Extract all relevant data (PFS from 2023, OS from 2024)
- Document as same trial, multiple time points
- Mark earlier publication as **FT-DUP**

---

## Data Extraction Checklist

For each **INCLUDED** study, extract:

### Study Characteristics

- [ ] Trial name/acronym
- [ ] NCT number (if available)
- [ ] Publication year
- [ ] Lead author
- [ ] Study design (Phase II/III RCT, cohort, post-hoc)
- [ ] Blinding (open-label, double-blind)
- [ ] Funding source

### Population

- [ ] Total sample size (N)
- [ ] Post-CDK4/6 subgroup size (if applicable)
- [ ] % with prior CDK4/6i exposure
- [ ] Prior CDK4/6i type (palbociclib/ribociclib/abemaciclib)
- [ ] Age (median/mean)
- [ ] ECOG performance status (% 0-1 vs ≥2)
- [ ] % with visceral metastases (liver/lung)
- [ ] Endocrine sensitivity (% endocrine-sensitive vs resistant)
- [ ] Biomarker status (PIK3CA/ESR1/TROP2 if reported)

### Intervention & Comparator

- [ ] Intervention arm: drug name + dose + schedule
- [ ] Comparator arm: drug name + dose + schedule
- [ ] Endocrine partner (AI/fulvestrant/tamoxifen)
- [ ] Treatment duration (until progression, fixed duration)

### Outcomes

- [ ] **PFS:**
  - Median PFS (months) - intervention vs comparator
  - HR (95% CI), p-value
  - KM curve available (yes/no)

- [ ] **OS:**
  - Median OS (months) - intervention vs comparator
  - HR (95% CI), p-value
  - Maturity (% events)

- [ ] **ORR:**
  - n/N or % - intervention vs comparator
  - RR or OR (95% CI)

- [ ] **Safety:**
  - Grade 3-4 AEs (any): n/N or %
  - Specific AEs (neutropenia, diarrhea, hepatotoxicity, QTc prolongation)
  - Treatment discontinuation due to AEs: n/N or %
  - Treatment-related deaths: n/N

### Risk of Bias (RCTs only)

- [ ] Randomization method (adequate/unclear)
- [ ] Allocation concealment (adequate/unclear)
- [ ] Blinding (patients/assessors)
- [ ] Attrition rate (%)
- [ ] Intention-to-treat analysis (yes/no)
- [ ] Selective reporting (suspected/no)

---

## Decision Recording

### In `fulltext_decisions.csv`, update:

1. **fulltext_available:** `yes` / `no` / `abstract_only`
2. **pdf_retrieved:** `yes` / `no` / `paywall`
3. **fulltext_decision:** `I` (include) / `E` (exclude)
4. **exclusion_reason_fulltext:** Code (e.g., FT-P3, FT-D1)
5. **prior_cdk46_percent:** % of patients with prior CDK4/6i (e.g., "89%", "100%", "<50%")
6. **study_design:** `Phase III RCT` / `Phase II RCT` / `Prospective cohort` / `Post-hoc analysis`
7. **sample_size:** Total N (post-CDK4/6 subgroup if applicable)
8. **outcomes_reported:** `PFS,OS,ORR` (comma-separated)
9. **reviewer_fulltext:** Reviewer name
10. **notes_fulltext:** Free text for any clarifications

### Example Entry:

| record_id       | fulltext_decision | exclusion_reason_fulltext | prior_cdk46_percent | study_design  | sample_size | outcomes_reported |
| --------------- | ----------------- | ------------------------- | ------------------- | ------------- | ----------- | ----------------- |
| KalinskyK202547 | I                 |                           | 100%                | Phase III RCT | 368         | PFS,OS,ORR,safety |
| Finn2016        | E                 | FT-I1                     | 0% (CDK4/6-naïve)   | Phase III RCT | 666         | PFS,OS,ORR        |

---

## Quality Assurance

### Inter-Rater Reliability

- **Dual independent review** of all 52 full-texts
- Calculate Cohen's Kappa for agreement
- **Target Kappa ≥0.80** for full-text screening
- Reconcile discrepancies with third reviewer

### Pilot Test (Recommended)

- Select 10 random full-texts
- Both reviewers assess independently
- Compare decisions and extraction
- Refine criteria if Kappa <0.80

---

## PDF Retrieval Strategy

### Method 1: Unpaywall API (Automated)

**Priority:** Use this first (free, legal Open Access)

```bash
cd /Users/htlin/meta-pipe/tooling/python
uv run ../../ma-fulltext-management/scripts/unpaywall_fetch.py \
  --in-csv ../../04_fulltext/round-01/pdf_retrieval_manifest.csv \
  --out-csv ../../04_fulltext/round-01/unpaywall_results.csv \
  --pdf-dir ../../04_fulltext/round-01/pdfs
```

**Expected success rate:** ~40-60% (Open Access articles)

### Method 2: PubMed Central (PMC)

For records with PMID, check PMC for free full-text:

- https://www.ncbi.nlm.nih.gov/pmc/
- Download PDF directly if available

### Method 3: Institutional Access

**If affiliated with university/hospital:**

- Use library proxy or VPN
- Search via PubMed, Scopus, or Web of Science
- Download PDFs directly

### Method 4: Author Contact

For paywalled articles not available via methods 1-3:

1. Find corresponding author email
2. Send polite request:
   - Subject: "Request for full-text: [Title]"
   - Body: "We are conducting a systematic review on post-CDK4/6 treatments and would appreciate a copy of your article: [citation]. Thank you."
3. Wait 2-4 weeks for response

### Method 5: Interlibrary Loan (ILL)

For critical articles (e.g., key trials) still unavailable:

- Submit ILL request through university library
- Typical turnaround: 1-2 weeks

---

## Troubleshooting

### Issue: PDF Retrieved but Unreadable (Scanned Image)

**Solution:** Use OCR tool or request text version from authors

### Issue: Supplementary Materials Not Available

**Solution:**

1. Check journal website directly (sometimes not on publisher site)
2. Contact authors
3. Exclude if critical data only in supplements and unavailable

### Issue: Conference Abstract, Full-Text Never Published

**Decision:**

- If >2 years since abstract: EXCLUDE (code: FT-D4)
- Contact trial investigators for unpublished data
- If key trial (e.g., postMONARCH): wait additional 4 weeks for response

### Issue: Article in Non-English Language

**Decision:**

- If English abstract available: Review abstract + use Google Translate for Methods/Results
- If no English abstract and critical trial: Seek professional translation
- Otherwise: EXCLUDE (code: FT-LANG)

---

## Timeline

| Task                                        | Duration  | Cumulative |
| ------------------------------------------- | --------- | ---------- |
| PDF retrieval (automated)                   | 1-2 days  | Day 1-2    |
| PDF retrieval (manual)                      | 3-5 days  | Day 3-7    |
| Full-text review (52 articles, 2 reviewers) | 1-2 weeks | Week 2-3   |
| Inter-rater reliability calculation         | 1 day     | Week 3     |
| Reconciliation of discrepancies             | 2-3 days  | Week 3-4   |
| Data extraction (included studies)          | 1-2 weeks | Week 4-6   |

**Total estimated time:** 4-6 weeks

---

## Expected Outcomes

Based on title/abstract screening (52 records):

| Expected Result             | Count | Percentage |
| --------------------------- | ----- | ---------- |
| **Include after full-text** | 15-25 | 29-48%     |
| **Exclude after full-text** | 27-37 | 52-71%     |

**Common full-text exclusion reasons:**

1. <50% had prior CDK4/6i, no subgroup analysis (FT-P3)
2. Sample size too small (FT-P4)
3. Insufficient data for extraction (FT-O3)
4. Duplicate publication (FT-DUP)

---

## Contact

**Questions about eligibility:**

- Consult: `01_protocol/eligibility.md`
- Consult: `01_protocol/pico.yaml`
- Contact: htlin

**Data extraction questions:**

- See: Stage 05 data dictionary (to be created)

---

**Document Version:** 1.0
**Date:** 2026-02-06
**Status:** Ready for full-text review
