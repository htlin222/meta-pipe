# Script Migration Summary

**Date**: 2026-02-06
**Purpose**: Document migration of reusable scripts to `ma-*` modules

---

## What Was Done

### Scripts Migrated to ma-\* Modules

| Original Script        | New Location                      | New Name               | Status                 |
| ---------------------- | --------------------------------- | ---------------------- | ---------------------- |
| `csv_to_bib_subset.py` | `ma-search-bibliography/scripts/` | `bib_subset_by_ids.py` | ✅ Generalized & Moved |
| `download_oa_pdfs.py`  | `ma-fulltext-management/scripts/` | `download_oa_pdfs.py`  | ✅ Generalized & Moved |
| `analyze_unpaywall.py` | `ma-fulltext-management/scripts/` | `analyze_unpaywall.py` | ✅ Generalized & Moved |

### Scripts Kept in tooling/python (Project-Specific)

| Script                            | Reason                                            |
| --------------------------------- | ------------------------------------------------- |
| `check_key_trials_oa.py`          | Hardcoded trial names for CDK4/6 project          |
| `auto_screening.py`               | Needs keyword YAML config before generalizing     |
| `update_manifest_with_results.py` | Needs more work to generalize                     |
| `prepare_fulltext_review.py`      | Already generic, could move but currently working |
| `bib_to_csv.py`                   | Already exists in ma-search-bibliography          |

---

## Changes Made for Generalization

### 1. bib_subset_by_ids.py

**Before**:

```python
# Hardcoded column name
record_id = row.get("record_id")
```

**After**:

```python
# Configurable column name
parser.add_argument("--id-column", default="record_id")
record_id = row.get(args.id_column)
```

**New features**:

- `--filter-column` and `--filter-value` for conditional filtering
- Better error messages for missing columns
- Validation of CSV structure

---

### 2. download_oa_pdfs.py

**Before**:

```python
# Hardcoded paths
csv_path = Path("../../04_fulltext/round-01/unpaywall_results.csv")
pdf_dir = Path("../../04_fulltext/round-01/pdfs")
```

**After**:

```python
# Configurable paths
parser.add_argument("--in-csv", required=True, type=Path)
parser.add_argument("--pdf-dir", required=True, type=Path)
parser.add_argument("--out-log", required=True, type=Path)
```

**New features**:

- Retry logic with configurable `--max-retries`
- Configurable `--sleep` for rate limiting
- Configurable `--timeout` for HTTP requests
- `--skip-existing` flag
- Better error handling (separate 4xx vs 5xx)
- PDF magic byte validation
- Comprehensive logging
- Exit code reflects success/failure

---

### 3. analyze_unpaywall.py

**Before**:

```python
# Hardcoded path, console only
csv_path = Path("../../04_fulltext/round-01/unpaywall_results.csv")
print(...)
```

**After**:

```python
# Configurable paths, markdown output
parser.add_argument("--in-csv", required=True, type=Path)
parser.add_argument("--out-md", type=Path)
```

**New features**:

- Optional markdown output with tables
- License analysis
- Percentage breakdowns
- Recommendations section in markdown
- Better formatting for console output

---

## Documentation Updates

### 1. CLAUDE.md

**Updated Section**: Stage 04: Fulltext

**Before**:

```bash
uv run ../../ma-fulltext-management/scripts/unpaywall_fetch.py \
  --in-bib ../../03_screening/round-01/included.bib \
  --out-csv ../../04_fulltext/unpaywall_results.csv
```

**After**:

```bash
# Extract BibTeX subset for full-text review
uv run ../../ma-search-bibliography/scripts/bib_subset_by_ids.py \
  --in-csv ../../03_screening/round-01/decisions_screened.csv \
  --in-bib ../../02_search/round-01/dedupe.bib \
  --out-bib ../../04_fulltext/round-01/fulltext_subset.bib \
  --filter-column final_decision \
  --filter-value Include

# Query Unpaywall API
uv run ../../ma-fulltext-management/scripts/unpaywall_fetch.py \
  --in-bib ../../04_fulltext/round-01/fulltext_subset.bib \
  --out-csv ../../04_fulltext/round-01/unpaywall_results.csv \
  --out-log ../../04_fulltext/round-01/unpaywall_fetch.log \
  --email "your@email.com"

# Analyze results
uv run ../../ma-fulltext-management/scripts/analyze_unpaywall.py \
  --in-csv ../../04_fulltext/round-01/unpaywall_results.csv \
  --out-md ../../04_fulltext/round-01/unpaywall_summary.md

# Download PDFs
uv run ../../ma-fulltext-management/scripts/download_oa_pdfs.py \
  --in-csv ../../04_fulltext/round-01/unpaywall_results.csv \
  --pdf-dir ../../04_fulltext/round-01/pdfs \
  --out-log ../../04_fulltext/round-01/pdf_download.log \
  --sleep 1 \
  --max-retries 3
```

---

### 2. ma-fulltext-management/README.md

**Created**: Comprehensive documentation for all scripts

**Sections**:

- Overview
- Installation
- Workflow (Stage 03 → 04)
- Script Reference
- Troubleshooting
- Expected Retrieval Rates
- Development Notes

---

## Impact on Future Projects

### Reusable Across Any Systematic Review

These scripts can now be used in ANY systematic review project:

1. **bib_subset_by_ids.py** - Any time you need to filter BibTeX by CSV IDs
   - After screening
   - After full-text review
   - For subgroup extraction

2. **download_oa_pdfs.py** - Any PDF retrieval workflow
   - Works with any Unpaywall results CSV
   - Configurable for different file structures
   - Handles common failure modes

3. **analyze_unpaywall.py** - Quick OA coverage assessment
   - Before starting retrieval
   - For grant proposals (estimate costs)
   - For feasibility assessment

---

## Testing Checklist

- [x] Scripts moved to correct modules
- [x] All argparse parameters work correctly
- [x] Error handling for missing files
- [x] Help text is comprehensive
- [x] CLAUDE.md updated
- [x] README.md created for ma-fulltext-management
- [ ] Test in clean environment (future)
- [ ] Update skill documentation (if needed)

---

## Next Steps (Optional)

### Medium Priority

1. **Generalize auto_screening.py**
   - Move keyword lists to YAML config
   - Add to ma-screening-quality module
   - Document in CLAUDE.md

2. **Generalize update_manifest_with_results.py**
   - Make compatible with any retrieval CSV
   - Add to ma-fulltext-management
   - Rename to `update_retrieval_manifest.py`

3. **Move prepare_fulltext_review.py**
   - Already generic enough
   - Just needs to be relocated
   - Add to ma-fulltext-management

### Low Priority

1. **Create skill for PDF retrieval**
   - Document best practices
   - Include institutional access workflow
   - Add to `.claude/skills/`

2. **Add integration tests**
   - Test full Stage 03→04 workflow
   - Verify all scripts work together
   - Add to ma-end-to-end tests

---

## Files Changed

```
ma-search-bibliography/
└── scripts/
    └── bib_subset_by_ids.py          [NEW]

ma-fulltext-management/
├── scripts/
│   ├── download_oa_pdfs.py           [NEW]
│   └── analyze_unpaywall.py          [NEW]
└── README.md                          [NEW]

tooling/python/
├── SCRIPT_ANALYSIS.md                 [NEW]
└── MIGRATION_SUMMARY.md              [NEW]

CLAUDE.md                              [UPDATED - Stage 04 section]
```

---

## Benefits

### For Current Project (CDK4/6 Meta-Analysis)

✅ Clear documentation of retrieval workflow
✅ Reproducible commands for future rounds
✅ Detailed logging for troubleshooting

### For Future Projects

✅ Reusable PDF retrieval pipeline
✅ Consistent Stage 03→04 transition
✅ Reduced development time (scripts already written)
✅ Best practices captured in documentation

### For Collaboration

✅ Other researchers can use these tools
✅ Clear documentation for new team members
✅ Standard workflow across projects

---

## Lessons Learned

### What Worked Well

1. **Developing in tooling/python first** - Easier to iterate
2. **Testing with real data** - Caught edge cases
3. **Comprehensive logging** - Made debugging easier
4. **Retry logic for downloads** - Handled transient failures

### What Could Be Improved

1. **Plan for reusability earlier** - Some hardcoded paths initially
2. **Write tests alongside development** - Would catch regressions
3. **Document as you go** - Easier than writing docs later

---

## Conclusion

**Scripts migrated**: 3 major tools
**Documentation created**: 2 comprehensive guides
**Impact**: All future systematic reviews can use these tools

**Estimated time saved per project**: 4-6 hours (no need to rewrite PDF retrieval)

---

## Questions for Next Session

1. Should we create a skill file for PDF retrieval workflow?
2. Should we add integration tests for Stage 03→04 transition?
3. Should we generalize the remaining project-specific scripts?

---

**Migration completed**: 2026-02-06
**Next review**: Before next systematic review project
