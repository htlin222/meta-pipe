# Web-Based AI Extraction (Alternative to PDF)

**Purpose**: Use Claude Code's web search to extract data directly from online sources, bypassing PDF download and reading
**Time**: 2-4 hours (vs 8-12 hours for PDF-based extraction)
**Stage**: 05 (Extraction) - Alternative approach

---

## When to Use This Approach

### ✅ Use Web-Based Extraction When:

- **No institutional access** to paywalled PDFs
- **Time-sensitive** projects (need results fast)
- **Preliminary analysis** to check feasibility
- **Supplementary data** that may be in online appendices
- **Recent publications** with detailed online abstracts

### ❌ Avoid Web-Based Extraction When:

- **High-stakes submission** to top-tier journals (reviewers may question)
- **Complex data** not available in abstracts (e.g., subgroup analyses)
- **Risk of bias assessment** requires full Methods section
- **Original data** needed (only in full text, not abstracts)

---

## How It Works

### Data Sources (in priority order)

1. **PubMed/PMC abstracts** (structured abstracts with N, outcomes)
2. **ClinicalTrials.gov** (trial registrations with detailed methods)
3. **Journal websites** (may have supplementary tables)
4. **Google Scholar** (can find preprints, conference abstracts)
5. **Europe PMC** (similar to PubMed, sometimes more complete)
6. **Cochrane Library** (systematic review abstracts)

### What Can Be Extracted

| Data Field                   | Availability | Confidence |
| ---------------------------- | ------------ | ---------- |
| **Study design**             | High         | 95%        |
| **Sample size (total)**      | High         | 90%        |
| **Intervention details**     | Medium       | 75%        |
| **Primary outcome**          | High         | 85%        |
| **Event counts**             | Medium-Low   | 60%        |
| **Baseline characteristics** | Low          | 40%        |
| **Risk of bias details**     | Very Low     | 20%        |

---

## Workflow

### Step 1: Prepare Study List

```bash
cd /Users/htlin/meta-pipe/tooling/python

# Extract study identifiers from screening results
uv run extract_study_identifiers.py \
  --in-csv ../../03_screening/round-01/decisions_screened.csv \
  --filter-column final_decision \
  --filter-value Include \
  --out-csv ../../05_extraction/round-01/web_extraction_manifest.csv
```

Output: `web_extraction_manifest.csv`

| study_id  | doi         | pmid     | title | journal | year |
| --------- | ----------- | -------- | ----- | ------- | ---- |
| Smith2020 | 10.1001/... | 32123456 | ...   | NEJM    | 2020 |

### Step 2: Web Search for Each Study

**Script**: `web_search_study_data.py`

For each study:

1. Query PubMed API for structured abstract
2. Query ClinicalTrials.gov if trial registration exists
3. Use WebSearch tool to find supplementary materials
4. Extract available data fields from each source
5. Mark confidence level for each field

```bash
uv run web_search_study_data.py \
  --manifest ../../05_extraction/round-01/web_extraction_manifest.csv \
  --data-dict ../../05_extraction/data-dictionary.md \
  --out-jsonl ../../05_extraction/round-01/web_extracted.jsonl \
  --out-log ../../05_extraction/round-01/web_search.log
```

### Step 3: AI-Assisted Field Population

**Using Claude Code's capabilities:**

```bash
# Use Claude Code to interpret web search results and fill extraction CSV
uv run ai_populate_extraction.py \
  --web-data ../../05_extraction/round-01/web_extracted.jsonl \
  --data-dict ../../05_extraction/data-dictionary.md \
  --out-csv ../../05_extraction/round-01/extraction_web.csv \
  --confidence-threshold 0.7
```

Output includes confidence scores:

| study_id  | n_total | events_intervention | events_control | confidence |
| --------- | ------- | ------------------- | -------------- | ---------- |
| Smith2020 | 400     | 45                  | 67             | 0.85       |
| Jones2021 | 250     | NULL                | NULL           | 0.40       |

### Step 4: Flag Low-Confidence Fields

```bash
# Generate report of fields that need manual verification
uv run flag_low_confidence.py \
  --extraction ../../05_extraction/round-01/extraction_web.csv \
  --confidence-threshold 0.7 \
  --out-md ../../05_extraction/round-01/needs_verification.md
```

### Step 5: Manual Verification

For studies with low confidence (<0.7), user should:

1. Check original PDF (if available)
2. Email corresponding author for clarification
3. Mark as "data not available" if cannot verify

---

## Expected Results

### Coverage Estimates

**For typical RCT meta-analysis:**

- ✅ 100% Study design, Sample size (from abstracts)
- ✅ 80-90% Primary outcome (event counts)
- ⚠️ 50-70% Baseline characteristics
- ❌ 20-30% Detailed risk of bias data

### Time Savings

| Approach                 | Time       | Success Rate             |
| ------------------------ | ---------- | ------------------------ |
| **PDF-based** (current)  | 8-12 hours | 100% (if PDFs available) |
| **Web-based** (new)      | 2-4 hours  | 70-80% completeness      |
| **Hybrid** (recommended) | 4-6 hours  | 90-95% completeness      |

### Confidence Scores

- **0.9-1.0**: Data directly from structured abstract/trial registry
- **0.7-0.89**: Data inferred from multiple sources with consistency
- **0.5-0.69**: Data from single unstructured source
- **<0.5**: Data not found or conflicting between sources

---

## Hybrid Approach (Recommended)

**Best of both worlds:**

1. **Phase 1**: Web-based extraction for all studies (2-3 hours)
   - Gets 70-80% of data quickly
   - Identifies which studies need PDFs

2. **Phase 2**: PDF-based extraction for low-confidence studies only (2-3 hours)
   - Focus effort on ~20-30% of studies
   - Manual review where web data is incomplete

3. **Total time**: 4-6 hours (vs 8-12 hours for PDF-only)
4. **Total completeness**: 90-95%

### Decision Tree

```
Start: Extract data for Study X
├─ Web search finds structured abstract?
│  ├─ Yes → Extract from abstract (confidence 0.85+)
│  │  ├─ All fields complete? → Done ✅
│  │  └─ Missing fields? → Flag for PDF retrieval
│  └─ No → Try ClinicalTrials.gov
│     ├─ Found? → Extract from registry (confidence 0.80+)
│     └─ Not found? → Flag for PDF retrieval (REQUIRED)
└─ Low confidence fields (<0.7) → PDF required
```

---

## Implementation Scripts

### New Scripts Needed

1. **`extract_study_identifiers.py`**
   - Input: `decisions_screened.csv`
   - Output: `web_extraction_manifest.csv`
   - Purpose: Prepare list with DOI/PMID for web search

2. **`web_search_study_data.py`**
   - Input: `web_extraction_manifest.csv`, `data-dictionary.md`
   - Output: `web_extracted.jsonl`
   - Purpose: Query PubMed API, ClinicalTrials.gov, web search

3. **`ai_populate_extraction.py`**
   - Input: `web_extracted.jsonl`, `data-dictionary.md`
   - Output: `extraction_web.csv` with confidence scores
   - Purpose: Use Claude to interpret web data and populate CSV

4. **`flag_low_confidence.py`**
   - Input: `extraction_web.csv`
   - Output: `needs_verification.md`
   - Purpose: List studies/fields needing PDF review

5. **`merge_web_pdf_extraction.py`**
   - Input: `extraction_web.csv`, `extraction_pdf.csv`
   - Output: `extraction_final.csv`
   - Purpose: Combine web + PDF data, prioritize PDF when both exist

---

## Quality Checks

### Before Analysis, Verify:

1. **Confidence threshold**: All critical fields ≥0.7
2. **Missing data pattern**: Not systematic (e.g., all intervention arms)
3. **Cross-validation**: Spot-check 5-10 studies against PDFs
4. **Documentation**: Log all sources used per study

### Red Flags (Stop and Get PDFs):

- ❌ >30% of studies have confidence <0.7 for primary outcome
- ❌ Conflicting data between sources (e.g., different sample sizes)
- ❌ Missing key moderators needed for meta-regression
- ❌ Reviewer comments questioning data accuracy

---

## Advantages vs Disadvantages

### ✅ Advantages

1. **Speed**: 50-70% faster than PDF-based
2. **Accessibility**: No institutional access needed
3. **Structured data**: APIs return JSON/XML (easier to parse)
4. **Real-time**: Can extract from preprints before publication
5. **Scalability**: Can process 100+ studies quickly

### ❌ Disadvantages

1. **Completeness**: 20-30% data may be missing
2. **Accuracy risk**: Abstracts may have errors vs full text
3. **Credibility**: Reviewers may question lack of PDF verification
4. **Limited details**: Complex outcomes not in abstracts
5. **Risk of bias**: Cannot assess without full Methods

---

## Validation Study

**To validate this approach, compare web-based vs PDF-based extraction:**

```bash
# Extract 20 studies using both methods
uv run validation_study.py \
  --web-csv ../../05_extraction/web_extracted.csv \
  --pdf-csv ../../05_extraction/pdf_extracted.csv \
  --out-report ../../05_extraction/validation_report.md
```

**Metrics to calculate:**

- Agreement rate per field (%)
- Mean absolute error for continuous variables
- Sensitivity/specificity for event counts
- Time savings (minutes per study)

---

## Citation in Manuscript

**If using web-based extraction, disclose in Methods:**

> "Data extraction was performed using a hybrid approach. For each included study, we first extracted available data from PubMed structured abstracts, ClinicalTrials.gov registries, and supplementary online materials using AI-assisted web search (Claude Code). Studies with incomplete data (confidence <0.7 for primary outcomes) or missing critical fields were retrieved as full-text PDFs for manual extraction. Data accuracy was validated by cross-checking 10 randomly selected studies between web-based and PDF-based extraction methods, with 95% agreement for primary outcome event counts."

---

## Recommendation

**Start with Hybrid Approach:**

1. Web-based extraction for all studies (fast, 70-80% complete)
2. PDF retrieval only for low-confidence studies (~20-30%)
3. Manual review for discrepancies
4. Validation study on 10 studies to document accuracy

**This balances speed, accuracy, and credibility for publication.**

---

## See Also

- [Unpaywall Robust Implementation](UNPAYWALL_ROBUST.md) - PDF retrieval when needed
- [LLM-Assisted Extraction](../CLAUDE.md#stage-05-extraction) - Full PDF-based workflow
- [Time Investment Guidance](TIME_GUIDANCE.md) - Time estimates for each approach
