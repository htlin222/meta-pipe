# Stage 05: Data Extraction Workflow

**Project**: CDK4/6 Inhibitor Post-Progression Meta-Analysis
**Date**: 2026-02-06
**Round**: round-01

---

## ✅ Completed Steps

### 1. Directory Structure Created

```
05_extraction/
├── data-dictionary.md           # 400+ lines defining all extraction fields
└── round-01/
    ├── pdf_texts.jsonl          # Extracted text from 10 PDFs (567,070 chars)
    └── extraction_template.csv  # Ready for manual data entry (10 records, 51 fields)
```

### 2. PDF Text Extraction ✅

**Script**: `/Users/htlin/meta-pipe/tooling/python/extract_pdf_text.py`

**Execution**:

```bash
cd /Users/htlin/meta-pipe/tooling/python
uv run extract_pdf_text.py \
  --pdf-dir ../../04_fulltext/round-01/pdfs \
  --out-jsonl ../../05_extraction/round-01/pdf_texts.jsonl \
  --pattern "*.pdf"
```

**Results**:

- ✅ Success: 10/10 PDFs
- ❌ Failed: 0/10 PDFs
- 📝 Total characters: 567,070
- 📄 Average per PDF: 56,707 characters

**Extracted PDFs**:

1. AgostiniM202478.pdf (10 pages, 41,768 chars)
2. AgrawalYN202536.pdf (17 pages, 67,799 chars)
3. CogliatiV2022222.pdf (17 pages, 65,970 chars)
4. DegenhardtT2023138.pdf (9 pages, 41,547 chars)
5. GilS2024143.pdf (8 pages, 35,485 chars)
6. HuangCS202445.pdf (8 pages, 35,608 chars)
7. Kalinsky2024TROPION.pdf (27 pages, 107,885 chars)
8. Lim202474.pdf (8 pages, 37,606 chars)
9. MarmeSYNTHIAEVELYN.pdf (10 pages, 61,806 chars)
10. Rugo2024TROPION.pdf (27 pages, 71,596 chars)

### 3. Extraction Template Created ✅

**Script**: `/Users/htlin/meta-pipe/tooling/python/create_extraction_template.py`

**Execution**:

```bash
cd /Users/htlin/meta-pipe/tooling/python
uv run create_extraction_template.py \
  --pdf-jsonl ../../05_extraction/round-01/pdf_texts.jsonl \
  --data-dict ../../05_extraction/data-dictionary.md \
  --out-csv ../../05_extraction/round-01/extraction_template.csv
```

**Output**:

- ✅ CSV with 10 records (one per PDF)
- ✅ 51 fields pre-defined from data dictionary
- ✅ Pre-filled: `study_id`, `pdf_filename`, `pdf_pages`, `pdf_chars`
- ⚪ Empty fields ready for manual entry

---

## 📋 Next Steps

### Option A: Manual Data Extraction (Traditional)

1. **Open the CSV in Excel/LibreOffice**:

   ```bash
   open /Users/htlin/meta-pipe/05_extraction/round-01/extraction_template.csv
   ```

2. **For each study**:
   - Read the corresponding PDF
   - Reference the extracted text in `pdf_texts.jsonl` if needed
   - Fill in all fields according to `data-dictionary.md`

3. **Field Priority** (fill these first):
   - ✅ Study identification: `first_author`, `publication_year`, `title`, `journal`, `doi`, `pmid`
   - ✅ Population: `n_total`, `n_cdk46_prior`, `pct_cdk46_prior`
   - ✅ Intervention: `arm_1_name`, `arm_1_category`, `arm_1_n`, `arm_2_name`, `arm_2_category`, `arm_2_n`
   - ✅ Primary outcome: `pfs_hr`, `pfs_ci_lower`, `pfs_ci_upper`, `pfs_p_value`
   - ✅ Quality: `rob_overall`

4. **Save as**: `extraction_filled.csv` when complete

---

### Option B: LLM-Assisted Extraction (Future)

If you have access to LLM APIs (OpenAI, Anthropic, etc.), you can use:

```bash
cd /Users/htlin/meta-pipe/tooling/python
uv run ../../ma-data-extraction/scripts/llm_extract.py \
  --manifest ../../04_fulltext/round-01/pdf_retrieval_manifest.csv \
  --data-dictionary ../../05_extraction/data-dictionary.md \
  --out-jsonl ../../05_extraction/round-01/llm_suggestions.jsonl
```

**Note**: This requires:

- API keys configured in `.env`
- Sufficient API credits
- Manual validation of LLM suggestions

---

## 📚 Data Dictionary Reference

All fields are defined in: `/Users/htlin/meta-pipe/05_extraction/data-dictionary.md`

### Core Field Categories

| Category               | Fields                                                                                                  | Required |
| ---------------------- | ------------------------------------------------------------------------------------------------------- | -------- |
| **Study ID**           | study_id, first_author, publication_year, title, journal, doi, pmid, trial_name                         | ✅       |
| **Study Design**       | study_design, phase, randomization                                                                      | ✅       |
| **Population**         | n_total, n_cdk46_prior, pct_cdk46_prior, age_median, hr_positive_pct, her2_negative_pct, metastatic_pct | ✅       |
| **CDK4/6i Details**    | cdk46_type, cdk46_line, cdk46_setting                                                                   | ✅       |
| **Intervention**       | arm*1_name, arm_1_category, arm_1_dose, arm_1_n, arm_2*\*                                               | ✅       |
| **Primary Outcomes**   | primary_endpoint, pfs_median_arm1/2, pfs_hr, pfs_ci_lower/upper, pfs_p_value                            | ✅       |
| **Secondary Outcomes** | os*\*, orr*\*                                                                                           | ⚪       |
| **Safety**             | ae_grade3plus_arm1/2_pct                                                                                | ⚪       |
| **Quality**            | rob_overall                                                                                             | ✅       |
| **Notes**              | notes_general                                                                                           | ⚪       |

### Treatment Categories (Standardized)

Use these exact values for `arm_*_category`:

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

## 🔍 Quality Checks

Before moving to Stage 06 (Analysis), ensure:

### Completeness

- [ ] All 10 studies have `study_id` filled
- [ ] All required fields (✅) are filled (or marked `NR` if not reported)
- [ ] All treatment arms have category assigned

### Consistency

- [ ] `n_cdk46_prior` ≤ `n_total`
- [ ] All percentages are 0-100
- [ ] Confidence intervals: `pfs_ci_lower` < `pfs_hr` < `pfs_ci_upper`
- [ ] P-values are in range 0-1

### Validation Script (Future)

```bash
uv run ../../ma-data-extraction/scripts/validate_extraction.py \
  --in-csv ../../05_extraction/round-01/extraction_filled.csv \
  --data-dict ../../05_extraction/data-dictionary.md \
  --out-report ../../05_extraction/round-01/validation_report.md
```

---

## 📊 Expected Timeline

| Task                                | Estimated Time | Status      |
| ----------------------------------- | -------------- | ----------- |
| PDF text extraction                 | 2 min          | ✅ Complete |
| Template creation                   | 1 min          | ✅ Complete |
| Manual data extraction (10 studies) | 4-6 hours      | ⏳ Pending  |
| Quality checks                      | 30 min         | ⏳ Pending  |
| Dual extraction (if required)       | +4-6 hours     | ⏳ Pending  |

---

## 🎯 Tips for Data Extraction

### Reading PDFs Efficiently

1. **Study identification**: Usually in title/header
2. **Sample sizes**: Look in "Methods" → "Participants" or Table 1
3. **CDK4/6i prior**: Check inclusion criteria or baseline characteristics
4. **Outcomes**: Usually in Results section or forest plot figures
5. **Hazard ratios**: Look for "HR (95% CI)" in text or tables
6. **Risk of bias**: May need to assess yourself using Cochrane RoB 2 tool

### Common Pitfalls

- ❌ Don't confuse ITT vs per-protocol sample sizes
- ❌ Don't miss confidence intervals in figure legends
- ❌ Check if HRs are for PFS or OS (we need both)
- ❌ Verify if percentages are out of total N or per-arm N
- ❌ Check units: months vs years for survival times

### Missing Data

- Use `NR` for "Not Reported" (critical missing data)
- Use `NA` for "Not Applicable" (not relevant to study design)
- Add explanation in `notes_general` field

---

## 🔄 Moving to Stage 06: Analysis

Once extraction is complete:

1. **Rename file**:

   ```bash
   mv extraction_template.csv extraction.csv
   ```

2. **Run validation** (if script available)

3. **Proceed to analysis**:
   ```bash
   cd /Users/htlin/meta-pipe/06_analysis
   # Copy R scripts from ma-meta-analysis/assets/r/
   # Run 01_setup.R → 02_effect_sizes.R → ... → 09_validation.R
   ```

---

## 📁 File Locations

| File                | Path                                             | Purpose              |
| ------------------- | ------------------------------------------------ | -------------------- |
| Data dictionary     | `05_extraction/data-dictionary.md`               | Field definitions    |
| PDF texts           | `05_extraction/round-01/pdf_texts.jsonl`         | Extracted PDF text   |
| Extraction template | `05_extraction/round-01/extraction_template.csv` | Ready for data entry |
| Original PDFs       | `04_fulltext/round-01/pdfs/`                     | Source documents     |

---

## 📞 Support

If you encounter issues:

1. **Check data dictionary**: `/Users/htlin/meta-pipe/05_extraction/data-dictionary.md`
2. **Review PDF text**: Search in `pdf_texts.jsonl` for specific terms
3. **Validation errors**: Will be reported in Stage 06 or QA stage

---

**Stage 05 Setup Complete**: 2026-02-06
**Ready for Manual Extraction**: ✅
**Next Stage**: Stage 06 (Meta-Analysis) - pending data extraction completion
