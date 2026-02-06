# Title/Abstract Screening Guide

**Study:** Post-CDK4/6 Treatment Strategies in HR+/HER2- Metastatic Breast Cancer
**Round:** 01
**Total Records:** 441
**Date:** 2026-02-06

---

## Quick Reference: Include/Exclude Criteria

### ✅ INCLUDE if ALL of the following:

1. **Population:**
   - HR+ (ER+ and/or PR+) breast cancer
   - HER2-negative
   - Advanced or metastatic disease (stage IIIB/IIIC/IV)
   - **PRIOR exposure to CDK4/6 inhibitor** (palbociclib, ribociclib, or abemaciclib)
   - Disease progression on or after CDK4/6 inhibitor

2. **Intervention:**
   - ANY systemic therapy given AFTER CDK4/6 inhibitor progression:
     - CDK4/6 inhibitor continuation/switching
     - mTOR inhibitors (everolimus)
     - Antibody-drug conjugates (sacituzumab govitecan, datopotamab deruxtecan)
     - Novel endocrine therapy (elacestrant, imlunestrant)
     - PI3K/AKT inhibitors (capivasertib, alpelisib)
     - Chemotherapy

3. **Study Design:**
   - Randomized controlled trial (Phase II or III)
   - Post-hoc analysis of post-CDK4/6 subgroup
   - Large prospective cohort study (n ≥100)

4. **Outcomes:**
   - Reports ≥1 of: PFS, OS, ORR, CBR, safety/AEs

---

### ❌ EXCLUDE if ANY of the following:

1. **Wrong Population:**
   - HER2-positive breast cancer
   - Triple-negative breast cancer (TNBC)
   - Early-stage breast cancer only (no metastatic component)
   - **NO prior CDK4/6 inhibitor exposure** (CDK4/6i-naïve)

2. **Wrong Intervention:**
   - Treatment given BEFORE CDK4/6 inhibitor progression
   - CDK4/6 inhibitor as first-line therapy (not post-progression)

3. **Wrong Study Design:**
   - Phase I dose-escalation only
   - Case report, case series (n <30)
   - Review article, editorial, letter, commentary
   - Preclinical or animal studies

4. **Wrong Outcomes:**
   - No efficacy or safety data (e.g., biomarker-only studies)

---

## Decision Codes

Use these codes in `decision_r1` and `decision_r2` columns:

| Code  | Meaning   | Action                                               |
| ----- | --------- | ---------------------------------------------------- |
| **I** | Include   | Proceed to full-text review                          |
| **E** | Exclude   | Do not retrieve full-text                            |
| **U** | Uncertain | Proceed to full-text review (when in doubt, include) |

---

## Exclusion Reason Codes

If **decision = E (Exclude)**, document reason in `exclusion_reason` column:

| Code    | Reason                                                   |
| ------- | -------------------------------------------------------- |
| **P1**  | Wrong population: HER2+ or TNBC                          |
| **P2**  | Wrong population: Early-stage only                       |
| **P3**  | Wrong population: No prior CDK4/6i exposure              |
| **I1**  | Wrong intervention: Treatment before CDK4/6i progression |
| **I2**  | Wrong intervention: Not a systemic therapy               |
| **D1**  | Wrong design: Phase I, case report, review               |
| **D2**  | Wrong design: Preclinical/animal study                   |
| **O1**  | Wrong outcomes: No efficacy/safety data                  |
| **L1**  | Language: Non-English/non-Chinese                        |
| **DUP** | Duplicate publication                                    |

---

## Screening Workflow

### Step 1: Read Title

- Does title mention breast cancer + CDK4/6 inhibitor + progression/resistance?
- **If YES → Continue to Step 2**
- **If NO but uncertain → Continue to Step 2**
- **If clearly irrelevant (e.g., other cancer types) → EXCLUDE (document reason)**

### Step 2: Read Abstract (if available)

- Check population: HR+/HER2-/metastatic/post-CDK4/6i?
- Check intervention: Treatment AFTER CDK4/6i progression?
- Check design: RCT, post-hoc analysis, or large cohort?
- Check outcomes: PFS, OS, ORR, or safety data?

### Step 3: Make Decision

- **If ALL inclusion criteria met → INCLUDE (I)**
- **If ANY exclusion criteria met → EXCLUDE (E) + document reason**
- **If uncertain → UNCERTAIN (U)** → err on side of inclusion

---

## Common Scenarios

### Scenario 1: Title mentions CDK4/6i but abstract unclear if post-progression

**Decision:** **U (Uncertain)** → Retrieve full-text to verify

### Scenario 2: Post-CDK4/6 subgroup analysis of larger trial

**Decision:** **I (Include)** → These are eligible (e.g., BOLERO-2 post-CDK4/6 subgroup)

### Scenario 3: Real-world study, n=80

**Decision:** **E (Exclude)** → Reason: D1 (cohort <100 patients)

### Scenario 4: Conference abstract only (no full-text yet)

**Decision:** **I (Include)** → Will assess full-text availability later (Stage 04)

### Scenario 5: Trial acronym mentioned (e.g., "TROPiCS-02") but no abstract

**Decision:** **I (Include)** → Known key trial, retrieve full-text

### Scenario 6: Systematic review or meta-analysis

**Decision:** **E (Exclude)** → Reason: D1 (not a primary study)
**Action:** Hand-search reference list for primary studies we may have missed

---

## Quality Checks

### Pilot Testing (before full screening):

1. Select 10 random records from decisions.csv
2. Both reviewers screen independently
3. Compare decisions → Calculate Kappa
4. **Target Kappa ≥0.60**
5. If Kappa <0.60, discuss discrepancies and refine criteria

### Full Screening:

1. Reviewer 1 fills in `decision_r1` column
2. Reviewer 2 fills in `decision_r2` column (blinded to R1's decisions)
3. Compare R1 vs R2 → Calculate Kappa
4. Reconcile discrepancies → Fill in `final_decision` column
5. Third reviewer adjudicates if R1 ≠ R2 and no consensus

---

## Tips for Efficient Screening

### Red Flags for EXCLUDE:

- Title mentions "HER2-positive" or "triple-negative"
- Title mentions "adjuvant" or "neoadjuvant" only (no metastatic)
- Title is clearly a review ("systematic review", "meta-analysis")
- Abstract says "CDK4/6 inhibitor-naïve patients"

### Green Flags for INCLUDE:

- Title mentions trial acronym (postMONARCH, MAINTAIN, TROPiCS-02, etc.)
- Title mentions "progression on CDK4/6" or "after palbociclib"
- Title mentions known post-CDK4/6 drugs (sacituzumab govitecan, elacestrant, etc.)
- Abstract explicitly states "patients who progressed on CDK4/6 inhibitor"

---

## Example Screening Decisions

### Example 1: INCLUDE

**Title:** "Abemaciclib Plus Fulvestrant in Advanced Breast Cancer after Progression on CDK4/6 Inhibition: Results from the Phase III postMONARCH Trial"

**Decision:** **I (Include)**
**Reasoning:**

- ✅ Population: Advanced breast cancer + post-CDK4/6 progression
- ✅ Intervention: Abemaciclib + fulvestrant (CDK4/6 continuation)
- ✅ Design: Phase III RCT
- ✅ Known key trial (postMONARCH)

---

### Example 2: EXCLUDE

**Title:** "Palbociclib plus letrozole as first-line therapy in postmenopausal women with ER+/HER2- advanced breast cancer: PALOMA-2 trial"

**Decision:** **E (Exclude)**
**Exclusion Reason:** **P3** (No prior CDK4/6i exposure - this is FIRST-LINE therapy)
**Reasoning:**

- ❌ Population: CDK4/6i-naïve (first-line treatment)
- This trial is about STARTING CDK4/6i, not treatment AFTER progression

---

### Example 3: UNCERTAIN → INCLUDE

**Title:** "Real-world effectiveness of endocrine therapy in HR+/HER2- metastatic breast cancer patients with prior CDK4/6 inhibitor use"

**Decision:** **U (Uncertain) → I (Include)**
**Reasoning:**

- ✅ Population: HR+/HER2- metastatic + prior CDK4/6i
- ✅ Intervention: Endocrine therapy (post-CDK4/6i)
- ⚠️ Design: Real-world study (need to check n ≥100 in full-text)
- **Decision:** Include for full-text review to verify sample size

---

### Example 4: EXCLUDE

**Title:** "Mechanisms of resistance to CDK4/6 inhibitors in breast cancer: a systematic review"

**Decision:** **E (Exclude)**
**Exclusion Reason:** **D1** (Systematic review, not a primary study)
**Action:** Add to reference list for hand-searching

---

## Data Entry Instructions

### CSV Columns:

- `decision_r1`: Reviewer 1's decision (I/E/U)
- `decision_r2`: Reviewer 2's decision (I/E/U)
- `final_decision`: Reconciled decision after discussion (I/E)
- `exclusion_reason`: Code (P1/P2/P3/I1/I2/D1/D2/O1/L1/DUP) if E
- `notes`: Free text for any clarifications

### Example Data Entry:

| record_id | decision_r1 | decision_r2 | final_decision | exclusion_reason | notes                                     |
| --------- | ----------- | ----------- | -------------- | ---------------- | ----------------------------------------- |
| Smith2024 | I           | I           | I              |                  | Key trial (postMONARCH)                   |
| Jones2023 | E           | E           | E              | P3               | PALOMA-2, first-line CDK4/6i              |
| Lee2022   | I           | E           | I              |                  | R2 misread abstract, actually post-CDK4/6 |
| Brown2021 | U           | U           | I              |                  | Unclear from abstract, check full-text    |

---

## Inter-Rater Reliability Calculation

After completing screening:

```bash
cd /Users/htlin/meta-pipe/tooling/python
uv run ../../ma-screening-quality/scripts/dual_review_agreement.py \
  --file ../../03_screening/round-01/decisions.csv \
  --col-a decision_r1 \
  --col-b decision_r2 \
  --out ../../03_screening/round-01/agreement.md
```

**Target Kappa:** ≥0.60 (substantial agreement)

---

## Reconciliation Process

For records where `decision_r1 ≠ decision_r2`:

1. **Both reviewers meet** to discuss discrepancy
2. **Re-read title/abstract together**
3. **Consult eligibility criteria** (01_protocol/eligibility.md)
4. **Attempt consensus**
   - If consensus reached → Fill in `final_decision`
   - If no consensus → **Third reviewer (senior investigator) adjudicates**

---

## Progress Tracking

- **Total records:** 441
- **Target screening rate:** 50-100 records/hour (experienced reviewer)
- **Estimated time:** 4-9 hours per reviewer
- **Timeline:** Complete within 1 week

---

## Contact

**Questions about eligibility criteria:**

- Consult: `/Users/htlin/meta-pipe/01_protocol/eligibility.md`
- Consult: `/Users/htlin/meta-pipe/01_protocol/pico.yaml`
- Contact lead investigator: htlin

---

**Document Version:** 1.0
**Date:** 2026-02-06
**Status:** Ready for screening
