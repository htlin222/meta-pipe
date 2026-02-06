# Stage 04: Full-Text Review Preparation - Complete

**Date:** 2026-02-06
**Status:** ✅ Ready for PDF retrieval and full-text assessment

---

## Summary

Stage 04 preparation is complete. All necessary files, guides, and tracking systems are in place to begin full-text review of 52 candidate studies.

---

## Files Created

### ✅ Core Working Files

1. **`fulltext_decisions.csv`** (52 records)
   - Primary working file for full-text review
   - Contains all 52 records from title/abstract screening (26 I + 26 U)
   - Pre-populated with screening decisions and notes
   - Empty columns for full-text assessment

2. **`pdf_retrieval_manifest.csv`** (52 records)
   - Tracking system for PDF retrieval
   - Contains DOI (98%), PMID (23%), and basic metadata
   - Columns for retrieval method, status, and file path

### ✅ Guidance Documents

3. **`fulltext_review_guide.md`** (Comprehensive, 200+ lines)
   - Detailed eligibility criteria for full-text assessment
   - Special scenarios and decision rules
   - Data extraction checklist
   - Quality assurance procedures
   - Timeline estimates (4-6 weeks)

4. **`pdf_retrieval_instructions.md`** (Detailed, 300+ lines)
   - 4-tier retrieval strategy (Unpaywall → PMC → Institutional → Author contact)
   - Expected success rates (75-100%)
   - Priority list for 10 key trials
   - File naming conventions
   - Troubleshooting guide

5. **`STAGE04_SUMMARY.md`** (This file)
   - Overview of Stage 04 preparation
   - Quick start guide
   - Next steps

---

## Key Statistics

### Records for Full-Text Review: 52

| Screening Decision | Count | Percentage |
| ------------------ | ----- | ---------- |
| Include (I)        | 26    | 50%        |
| Uncertain (U)      | 26    | 50%        |

### Metadata Availability:

| Identifier | Count | Percentage | Usefulness                      |
| ---------- | ----- | ---------- | ------------------------------- |
| DOI        | 51    | 98.1%      | ⭐⭐⭐ (Critical for retrieval) |
| PMID       | 12    | 23.1%      | ⭐⭐ (Helpful for PMC access)   |

### Key Trials Included: 10/10 (100%) ✅

All 10 essential trials successfully identified in title/abstract screening:

- postMONARCH ✓
- MAINTAIN ✓
- PALMIRA ✓
- TROPiCS-02 ✓
- TROPION-Breast01 ✓
- EMBER-3 ✓
- EMERALD ✓
- CAPItello-291 ✓
- SOLAR-1 ✓
- BOLERO-2 post-CDK4/6 ✓

---

## Expected Outcomes

### PDF Retrieval (Tier 1-4):

- **Target:** ≥45 PDFs retrieved (≥87%)
- **Critical:** All 10 key trials must be retrieved

### Full-Text Assessment:

- **Expected final inclusion:** 15-25 studies (~29-48% of 52 reviewed)
- **Expected exclusions:** 27-37 studies (~52-71%)

### Common Full-Text Exclusion Reasons:

1. <50% had prior CDK4/6i, no subgroup analysis (FT-P3)
2. Sample size too small (<20 in post-CDK4/6 subgroup) (FT-P4)
3. Insufficient data for extraction (FT-O3)
4. Duplicate publication (FT-DUP)

---

## Quick Start Guide

### Step 1: PDF Retrieval (Days 1-7)

**Priority Action:** Retrieve 10 key trials first

```bash
# Method 1: Automated (if Unpaywall script available)
cd /Users/htlin/meta-pipe/tooling/python
uv run ../../ma-fulltext-management/scripts/unpaywall_fetch.py \
  --in-csv ../../04_fulltext/round-01/pdf_retrieval_manifest.csv \
  --out-csv ../../04_fulltext/round-01/unpaywall_results.csv \
  --pdf-dir ../../04_fulltext/round-01/pdfs \
  --email "your.email@example.com"

# Method 2: Manual (see pdf_retrieval_instructions.md)
# - Check Unpaywall manually: https://unpaywall.org/
# - Access via institutional library
# - Contact authors for paywalled articles
```

**Update manifest after each retrieval:**

- `retrieval_method`: unpaywall/pmc/institutional/author
- `retrieval_status`: success/pending/paywall/not_found
- `pdf_path`: 04_fulltext/round-01/pdfs/[RecordID].pdf

### Step 2: Full-Text Review (Weeks 1-3)

**For each PDF:**

1. **Read full-text** focusing on:
   - Methods: Population, intervention, design
   - Results: Sample size, outcomes (PFS, OS, ORR)
   - Check % with prior CDK4/6i

2. **Apply detailed criteria** (see `fulltext_review_guide.md`)

3. **Make decision:**
   - Include (I) if meets ALL criteria
   - Exclude (E) if fails ANY criterion
   - Document exclusion reason (FT-P1/P2/P3, FT-I1/I2, FT-D1/D2, FT-O1/O2)

4. **Update `fulltext_decisions.csv`:**
   - `fulltext_decision`: I or E
   - `exclusion_reason_fulltext`: Code (if E)
   - `prior_cdk46_percent`: e.g., "89%", "100%", "<50%"
   - `study_design`: Phase III RCT / Phase II RCT / Prospective cohort
   - `sample_size`: Total N
   - `outcomes_reported`: PFS,OS,ORR,safety

### Step 3: Quality Assurance (Week 3-4)

**Dual independent review:**

- Reviewer 2 independently assesses all 52 full-texts
- Calculate Cohen's Kappa (target ≥0.80)
- Reconcile discrepancies with third reviewer

### Step 4: Data Extraction (Weeks 4-6)

**For included studies:**

- Extract detailed data for meta-analysis
- Use Stage 05 data dictionary (to be created)
- Record HRs, 95% CIs, sample sizes, etc.

---

## Timeline

| Phase                                  | Duration  | Cumulative | Status            |
| -------------------------------------- | --------- | ---------- | ----------------- |
| **Stage 01: Protocol**                 | 1 week    | Week 1     | ✅ Complete       |
| **Stage 02: Search**                   | 1 week    | Week 2     | ✅ Complete       |
| **Stage 03: Title/Abstract Screening** | 1 week    | Week 3     | ✅ Complete       |
| **Stage 04A: PDF Retrieval**           | 1 week    | Week 4     | ⏳ Ready to start |
| **Stage 04B: Full-Text Review**        | 2-3 weeks | Week 5-7   | ⏳ Pending        |
| **Stage 05: Data Extraction**          | 2-3 weeks | Week 7-10  | ⏳ Pending        |
| **Stage 06: Analysis**                 | 2-3 weeks | Week 10-13 | ⏳ Pending        |
| **Stage 07: Manuscript**               | 2-3 weeks | Week 13-16 | ⏳ Pending        |

**Current Progress:** End of Week 3

---

## Critical Success Factors

### ✅ Must-Haves:

1. **Retrieve all 10 key trials** - Highest priority
2. **Dual independent review** - Quality standard
3. **Document all exclusion reasons** - Transparency
4. **Kappa ≥0.80 for full-text** - Inter-rater reliability

### ⚠️ Potential Challenges:

| Challenge                              | Mitigation                           |
| -------------------------------------- | ------------------------------------ |
| Paywall blocking PDFs                  | Use author contact for key trials    |
| Insufficient post-CDK4/6 subgroup data | Extract from supplementary materials |
| Discrepancies between reviewers        | Third reviewer adjudication          |
| Time constraints                       | Prioritize 10 key trials first       |

---

## Next Actions

### Immediate (This Week):

1. ✅ **Verify Unpaywall script availability**

   ```bash
   ls /Users/htlin/meta-pipe/ma-fulltext-management/scripts/unpaywall_fetch.py
   ```

2. ✅ **Run Unpaywall retrieval** (if script available)
   - Expected: 20-30 PDFs retrieved automatically
   - Update manifest with results

3. ✅ **Manual retrieval for 10 key trials**
   - Check institutional access
   - Download directly from journals
   - Contact authors if needed

### This Week:

4. ⏳ **Complete PDF retrieval** (target: ≥45 PDFs)

5. ⏳ **Begin full-text review**
   - Start with 10 key trials
   - Use `fulltext_review_guide.md`
   - Update `fulltext_decisions.csv`

### Next 2-3 Weeks:

6. ⏳ **Complete full-text review** (all 52 records)

7. ⏳ **Calculate inter-rater reliability** (Kappa)

8. ⏳ **Reconcile discrepancies**

9. ⏳ **Proceed to Stage 05: Data Extraction** (for ~15-25 included studies)

---

## Directory Structure

```
/Users/htlin/meta-pipe/
├── 01_protocol/
│   ├── pico.yaml ✅
│   └── eligibility.md ✅
├── 02_search/
│   └── round-01/
│       ├── dedupe.bib (447 records) ✅
│       └── key_trials_verification_updated.md ✅
├── 03_screening/
│   └── round-01/
│       ├── decisions_screened_r1.csv (447 records) ✅
│       ├── screening_summary.md ✅
│       └── screening_guide.md ✅
├── 04_fulltext/
│   └── round-01/
│       ├── pdfs/ (empty, ready for PDFs) ✅
│       ├── fulltext_decisions.csv (52 records) ✅
│       ├── pdf_retrieval_manifest.csv (52 records) ✅
│       ├── fulltext_review_guide.md ✅
│       ├── pdf_retrieval_instructions.md ✅
│       └── STAGE04_SUMMARY.md (this file) ✅
├── 05_extraction/ (pending Stage 05)
├── 06_analysis/ (pending Stage 06)
└── 07_manuscript/ (pending Stage 07)
```

---

## Resources

### Key Documents (Read These First):

1. **Eligibility criteria:** `01_protocol/eligibility.md`
2. **PICO framework:** `01_protocol/pico.yaml`
3. **Full-text review guide:** `04_fulltext/round-01/fulltext_review_guide.md`
4. **PDF retrieval instructions:** `04_fulltext/round-01/pdf_retrieval_instructions.md`

### Working Files:

- **Main CSV:** `04_fulltext/round-01/fulltext_decisions.csv`
- **Retrieval tracking:** `04_fulltext/round-01/pdf_retrieval_manifest.csv`

### Reference:

- **Screening results:** `03_screening/round-01/screening_summary.md`
- **Key trials verified:** `02_search/round-01/key_trials_verification_updated.md`

---

## Support

**Questions?**

- **Eligibility criteria:** See `01_protocol/eligibility.md` or `fulltext_review_guide.md`
- **PDF retrieval:** See `pdf_retrieval_instructions.md`
- **Technical issues:** Check CLAUDE.md in project root

**Contact:** htlin

---

## Version History

| Version | Date       | Changes                               |
| ------- | ---------- | ------------------------------------- |
| 1.0     | 2026-02-06 | Initial Stage 04 preparation complete |

---

**Status:** ✅ **Stage 04 ready for execution**

**Next milestone:** PDF retrieval complete (target: 1 week)
