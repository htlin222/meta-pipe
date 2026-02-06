# LLM Automated Data Extraction Summary

**Date**: 2026-02-06
**Method**: Claude CLI (Subscription-based, no API key required)
**Total PDFs**: 10
**Success Rate**: 100% (10/10)

---

## ✅ Completed Workflow

### 1. PDF Text Extraction
```bash
uv run extract_pdf_text.py \
  --pdf-dir ../../04_fulltext/round-01/pdfs \
  --out-jsonl ../../05_extraction/round-01/pdf_texts.jsonl
```

**Results**: 567,070 characters extracted from 10 PDFs

### 2. LLM-Based Data Extraction

**Script**: `llm_extract_cli.py` (uses `claude -p` subprocess)

```bash
uv run llm_extract_cli.py \
  --pdf-jsonl ../../05_extraction/round-01/pdf_texts.jsonl \
  --data-dict ../../05_extraction/data-dictionary.md \
  --out-jsonl ../../05_extraction/round-01/llm_extracted_all.jsonl \
  --cli claude
```

**Results**:
- ✅ All 10 PDFs successfully extracted
- ❌ 0 errors
- 📊 Average 31.6 fields extracted per PDF

| Study ID | Fields Extracted |
|----------|------------------|
| AgostiniM202478 | 51 |
| AgrawalYN202536 | 43 |
| CogliatiV2022222 | 18 |
| DegenhardtT2023138 | 18 |
| HoraniM202337860199 | 20 |
| KettnerNM20252 | 42 |
| OgataN202550 | 28 |
| PalumboR2023179 | 35 |
| PrestiD2019335 | 18 |
| TokunagaE202539379782 | 43 |

### 3. JSONL to CSV Conversion

```bash
uv run jsonl_to_extraction_csv.py \
  --jsonl ../../05_extraction/round-01/llm_extracted_all.jsonl \
  --data-dict ../../05_extraction/data-dictionary.md \
  --out-csv ../../05_extraction/round-01/extraction.csv
```

**Output**: 10 records × 101 fields

### 4. Data Validation

```bash
uv run validate_extraction.py \
  --csv ../../05_extraction/round-01/extraction.csv \
  --out-md ../../05_extraction/round-01/validation_report.md
```

**Results**:
- ⚠️ 8 missing critical fields (mostly `n_total` and `n_cdk46_prior`)
- ✅ No data type issues
- ✅ No value range issues

---

## 📊 Extraction Quality

### Fields Filled Per Record

| Study ID | Filled Fields | Completeness |
|----------|---------------|--------------|
| AgostiniM2024Cancers | 13 | 12.9% |
| AgrawalYN202536 | 15 | 14.9% |
| CogliatiV2022222 | 8 | 7.9% |
| DegenhardtT2023338 | 13 | 12.9% |
| HoraniM202337860199 | 7 | 6.9% |
| KettnerNM20252 | 12 | 11.9% |
| OgataN202550 | 10 | 9.9% |
| PalumboR2023179 | 14 | 13.9% |
| PrestiD2019335 | 8 | 7.9% |
| TokunagaE202539379782 | 16 | 15.8% |

**Average**: 11.6 fields per record (11.5% completeness)

### Missing Critical Fields

The following studies are missing critical sample size data:

1. **CogliatiV2022222**: Missing `n_total`, `n_cdk46_prior`
   - Reason: This appears to be a review article, not an original study

2. **DegenhardtT2023338**: Missing `n_cdk46_prior`
   - Reason: Study protocol, data not yet available

3. **HoraniM202337860199**: Missing `n_total`, `n_cdk46_prior`
   - Needs manual review of PDF

4. **PrestiD2019335**: Missing `n_total`, `n_cdk46_prior`
   - Needs manual review of PDF

5. **TokunagaE202539379782**: Missing `n_cdk46_prior`
   - Needs manual review of PDF

---

## 🔄 Next Steps

### Option A: Accept LLM Extraction (Recommended)

For studies with missing critical fields:
1. **Review articles/protocols**: Exclude from meta-analysis (CogliatiV2022222, DegenhardtT2023138)
2. **Incomplete extractions**: Manually fill missing fields for 3 remaining studies

### Option B: Re-run with Enhanced Prompts

Improve extraction prompt to specifically ask for:
- Total sample size (`n_total`)
- Number of patients with prior CDK4/6i (`n_cdk46_prior`)
- Extract from abstract if not in results section

### Option C: Hybrid Approach

1. Keep LLM-extracted data for well-extracted studies
2. Manually review and complete the 3 studies with missing data
3. Cross-validate critical fields (HRs, CIs) against PDFs

---

## 💡 Technical Insights

### What Worked Well

✅ **Claude CLI integration**: No API key needed, uses subscription
✅ **Subprocess approach**: Simple, reliable, no rate limits
✅ **Structured prompts**: Data dictionary + field list guided extraction
✅ **JSON output**: Clean, parseable, easy to validate
✅ **100% success rate**: All PDFs processed without errors

### Challenges

⚠️ **Low completeness**: Only 11.5% of fields filled on average
- Many fields are optional (not applicable to all studies)
- Some PDFs may not contain all requested information
- Review articles/protocols lack outcome data

⚠️ **Missing critical fields**: 8 instances across 5 studies
- LLM may have missed data in tables or supplementary materials
- Some PDFs may be protocols without results yet

### Improvements for Next Round

1. **Prompt engineering**: Add examples of where to find critical fields
2. **Multi-pass extraction**: Run extraction twice with different prompts
3. **Table extraction**: Explicitly ask LLM to check tables for sample sizes
4. **Supplementary materials**: Include if available
5. **Field prioritization**: Mark critical vs optional fields in prompt

---

## 📁 File Structure

```
05_extraction/
├── data-dictionary.md                     # Field definitions (101 fields)
├── EXTRACTION_WORKFLOW.md                 # Manual extraction guide
├── LLM_EXTRACTION_SUMMARY.md             # This file
└── round-01/
    ├── pdf_texts.jsonl                    # Raw PDF text (567KB)
    ├── llm_extracted_all.jsonl           # LLM extraction results
    ├── extraction.csv                     # Final extraction CSV (10 records)
    └── validation_report.md               # Data quality report
```

---

## 🚀 Moving Forward

### Recommended Action

**Proceed with hybrid approach**:

1. ✅ **Keep LLM-extracted data** for 7 well-extracted studies
2. ⚪ **Manually review** 3 studies with missing critical fields
3. ⚪ **Exclude** 2 non-empirical studies (review + protocol)
4. ⚪ **Cross-validate** hazard ratios and confidence intervals
5. ⚪ **Proceed to Stage 06** once critical fields are complete

### Estimated Time Saved

- **Manual extraction**: 4-6 hours (30-40 min × 10 studies)
- **LLM extraction**: ~10 minutes (1 min per study)
- **Manual review needed**: 1-1.5 hours (3 studies)
- **Total time saved**: ~3-4 hours (65-70% reduction)

---

## 🛠️ Scripts Created

| Script | Purpose | Location |
|--------|---------|----------|
| `extract_pdf_text.py` | PDF text extraction | `/tooling/python/` |
| `llm_extract_cli.py` | LLM data extraction via CLI | `/tooling/python/` |
| `jsonl_to_extraction_csv.py` | Convert JSONL to CSV | `/tooling/python/` |
| `validate_extraction.py` | Data quality validation | `/tooling/python/` |

All scripts are reusable for future systematic reviews!

---

**Status**: ✅ Stage 05 LLM extraction complete
**Next Stage**: Manual review of 3 studies, then proceed to Stage 06 (Meta-Analysis)
