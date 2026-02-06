# Script Analysis - Reusability Assessment

**Date**: 2026-02-06
**Purpose**: Identify which scripts should be moved to `ma-*` modules for reuse

---

## Scripts Created This Session

### 1. ✅ **csv_to_bib_subset.py** - HIGHLY REUSABLE

**Current location**: `tooling/python/`
**Recommended location**: `ma-search-bibliography/scripts/`
**Purpose**: Extract BibTeX subset from CSV record IDs
**Reusability**: 🟢 **HIGH** - Any stage needing BibTeX filtering

**Use cases**:

- Stage 02: Create subsets for specific databases
- Stage 03: Extract included records after screening
- Stage 04: Create full-text retrieval subset
- Any workflow needing BibTeX filtering by ID list

**Generalization needed**:

- ✅ Already generic (takes any CSV with record_id column)
- ✅ Already uses argparse
- 🔧 Add optional `--id-column` parameter (default: "record_id")

---

### 2. ✅ **download_oa_pdfs.py** - HIGHLY REUSABLE

**Current location**: `tooling/python/`
**Recommended location**: `ma-fulltext-management/scripts/`
**Purpose**: Download PDFs from Unpaywall results CSV
**Reusability**: 🟢 **HIGH** - Any full-text retrieval workflow

**Use cases**:

- Stage 04: Automated PDF download after Unpaywall query
- Any systematic review needing OA PDFs
- Batch PDF retrieval from URL lists

**Generalization needed**:

- 🔧 Make paths configurable via argparse (currently hardcoded)
- 🔧 Add `--sleep` parameter for rate limiting
- 🔧 Add `--max-retries` parameter
- ✅ Already has good error handling and logging

**Proposed API**:

```bash
uv run ../../ma-fulltext-management/scripts/download_oa_pdfs.py \
  --in-csv unpaywall_results.csv \
  --pdf-dir pdfs/ \
  --out-log download.log \
  --sleep 1 \
  --max-retries 3
```

---

### 3. ✅ **analyze_unpaywall.py** - MODERATELY REUSABLE

**Current location**: `tooling/python/`
**Recommended location**: `ma-fulltext-management/scripts/`
**Purpose**: Analyze Unpaywall results and generate summary
**Reusability**: 🟡 **MEDIUM** - Useful for Unpaywall QA

**Use cases**:

- Stage 04: Quick assessment of OA coverage
- QA reports for retrieval success rates

**Generalization needed**:

- 🔧 Make input path configurable
- 🔧 Add `--out-md` for markdown report output
- ✅ Already provides good statistics

**Proposed API**:

```bash
uv run ../../ma-fulltext-management/scripts/analyze_unpaywall.py \
  --in-csv unpaywall_results.csv \
  --out-md unpaywall_summary.md
```

---

### 4. ⚠️ **check_key_trials_oa.py** - PROJECT-SPECIFIC

**Current location**: `tooling/python/`
**Recommended location**: ❌ Keep in `tooling/python/` (project-specific)
**Purpose**: Check OA status for specific key trials
**Reusability**: 🔴 **LOW** - Hardcoded trial names

**Use cases**:

- This project only (CDK4/6 inhibitor trials)

**Keep as-is**: Project-specific QA script

---

### 5. ✅ **update_manifest_with_results.py** - MODERATELY REUSABLE

**Current location**: `tooling/python/`
**Recommended location**: `ma-fulltext-management/scripts/`
**Purpose**: Update PDF retrieval manifest with download results
**Reusability**: 🟡 **MEDIUM** - Useful for tracking retrieval status

**Use cases**:

- Stage 04: Track which PDFs downloaded successfully
- Update retrieval status after any download attempt

**Generalization needed**:

- 🔧 Make all paths configurable
- 🔧 Make it work with any retrieval CSV (not just Unpaywall)
- ✅ Already has good status categorization

**Proposed API**:

```bash
uv run ../../ma-fulltext-management/scripts/update_retrieval_manifest.py \
  --manifest pdf_retrieval_manifest.csv \
  --unpaywall unpaywall_results.csv \
  --pdf-dir pdfs/ \
  --out-csv manifest_updated.csv
```

---

### 6. ✅ **prepare_fulltext_review.py** - HIGHLY REUSABLE

**Current location**: `tooling/python/`
**Recommended location**: `ma-fulltext-management/scripts/`
**Purpose**: Extract screening results and prepare full-text review files
**Reusability**: 🟢 **HIGH** - Standard transition from screening to full-text

**Use cases**:

- Stage 03→04 transition in ANY systematic review
- Create full-text tracking files

**Generalization needed**:

- ✅ Already configurable via argparse
- ✅ Already generic column handling

---

### 7. ✅ **auto_screening.py** - MODERATELY REUSABLE

**Current location**: `tooling/python/`
**Recommended location**: `ma-screening-quality/scripts/`
**Purpose**: AI-assisted title/abstract screening
**Reusability**: 🟡 **MEDIUM** - Needs domain adaptation

**Use cases**:

- Stage 03: Initial screening pass
- Any systematic review with keyword-based inclusion

**Generalization needed**:

- 🔧 Make keywords configurable via YAML file
- 🔧 Allow custom exclusion rules
- ✅ Already has good structure

**Proposed API**:

```bash
uv run ../../ma-screening-quality/scripts/auto_screening.py \
  --in-csv decisions.csv \
  --keywords-yaml screening_rules.yaml \
  --out-csv decisions_screened.csv
```

---

### 8. ✅ **bib_to_csv.py** - HIGHLY REUSABLE

**Current location**: `tooling/python/`
**Recommended location**: `ma-search-bibliography/scripts/`
**Purpose**: Convert BibTeX to CSV for screening
**Reusability**: 🟢 **HIGH** - Standard stage 02→03 transition

**Use cases**:

- Stage 02→03 transition in ANY systematic review
- Export BibTeX to spreadsheet format

**Generalization needed**:

- ✅ Already generic
- ✅ Already configurable

---

## Summary: Scripts to Move

### 🟢 High Priority (Move to ma-\* modules)

| Script                       | Module                            | New Name               | API Changes             |
| ---------------------------- | --------------------------------- | ---------------------- | ----------------------- |
| `csv_to_bib_subset.py`       | `ma-search-bibliography/scripts/` | `bib_subset_by_ids.py` | Add `--id-column` param |
| `download_oa_pdfs.py`        | `ma-fulltext-management/scripts/` | `download_oa_pdfs.py`  | Make paths configurable |
| `prepare_fulltext_review.py` | `ma-fulltext-management/scripts/` | ✅ Already named well  | ✅ Already generic      |
| `bib_to_csv.py`              | `ma-search-bibliography/scripts/` | ✅ Already named well  | ✅ Already generic      |

### 🟡 Medium Priority (Generalize first, then move)

| Script                            | Module                            | Generalization Needed                                             |
| --------------------------------- | --------------------------------- | ----------------------------------------------------------------- |
| `analyze_unpaywall.py`            | `ma-fulltext-management/scripts/` | Make paths configurable, add MD output                            |
| `update_manifest_with_results.py` | `ma-fulltext-management/scripts/` | Rename to `update_retrieval_manifest.py`, make paths configurable |
| `auto_screening.py`               | `ma-screening-quality/scripts/`   | Make keywords configurable via YAML                               |

### 🔴 Low Priority (Keep project-specific)

| Script                   | Reason                                 |
| ------------------------ | -------------------------------------- |
| `check_key_trials_oa.py` | Hardcoded trial names for this project |

---

## Proposed File Structure After Moving

```
ma-search-bibliography/
├── scripts/
│   ├── bib_to_csv.py                  ← Already exists
│   ├── bib_subset_by_ids.py           ← Move from csv_to_bib_subset.py
│   └── ...existing scripts...

ma-fulltext-management/
├── scripts/
│   ├── unpaywall_fetch.py             ← Already exists
│   ├── download_oa_pdfs.py            ← NEW (move from tooling)
│   ├── analyze_unpaywall.py           ← NEW (move from tooling)
│   ├── update_retrieval_manifest.py   ← NEW (move from tooling)
│   ├── prepare_fulltext_review.py     ← NEW (move from tooling)
│   └── ...existing scripts...

ma-screening-quality/
├── scripts/
│   ├── auto_screening.py              ← NEW (move from tooling, generalize)
│   └── ...existing scripts...
```

---

## Next Steps

1. **Generalize high-priority scripts** (add argparse for hardcoded paths)
2. **Move to appropriate ma-\* modules**
3. **Update CLAUDE.md** with new script references
4. **Test in clean environment** to ensure portability
5. **Update skill documentation** (if applicable)

---

## Impact on CLAUDE.md

Add to `<details><summary><strong>Stage 04: Fulltext</strong></summary>`:

```bash
# Extract BibTeX subset for full-text review
uv run ../../ma-search-bibliography/scripts/bib_subset_by_ids.py \
  --in-csv ../../03_screening/round-01/decisions.csv \
  --in-bib ../../02_search/round-01/dedupe.bib \
  --out-bib ../../04_fulltext/round-01/fulltext_subset.bib \
  --id-column record_id

# Prepare full-text review files
uv run ../../ma-fulltext-management/scripts/prepare_fulltext_review.py \
  --in-csv ../../03_screening/round-01/decisions_screened_r1.csv \
  --out-dir ../../04_fulltext/round-01

# Unpaywall fetch (already exists)
uv run ../../ma-fulltext-management/scripts/unpaywall_fetch.py \
  --in-bib ../../04_fulltext/round-01/fulltext_subset.bib \
  --out-csv ../../04_fulltext/round-01/unpaywall_results.csv \
  --out-log ../../04_fulltext/round-01/unpaywall_fetch.log \
  --email "user@example.com"

# Download Open Access PDFs (NEW)
uv run ../../ma-fulltext-management/scripts/download_oa_pdfs.py \
  --in-csv ../../04_fulltext/round-01/unpaywall_results.csv \
  --pdf-dir ../../04_fulltext/round-01/pdfs \
  --out-log ../../04_fulltext/round-01/pdf_download.log \
  --sleep 1

# Analyze Unpaywall results (NEW)
uv run ../../ma-fulltext-management/scripts/analyze_unpaywall.py \
  --in-csv ../../04_fulltext/round-01/unpaywall_results.csv \
  --out-md ../../04_fulltext/round-01/unpaywall_summary.md

# Update retrieval manifest (NEW)
uv run ../../ma-fulltext-management/scripts/update_retrieval_manifest.py \
  --manifest ../../04_fulltext/round-01/pdf_retrieval_manifest.csv \
  --unpaywall ../../04_fulltext/round-01/unpaywall_results.csv \
  --pdf-dir ../../04_fulltext/round-01/pdfs \
  --out-csv ../../04_fulltext/round-01/manifest_updated.csv
```
