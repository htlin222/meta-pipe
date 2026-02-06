# Tests

Unit tests and connection tests for the meta-analysis pipeline.

## Quick Start

```bash
cd tooling/python

# Unit tests only (fast, no network)
uv run ../../tests/run_tests.py

# Connection tests only (requires .env)
uv run ../../tests/run_tests.py --conn

# All tests
uv run ../../tests/run_tests.py --all
```

---

## Test Fixtures

Simulated data for testing each pipeline stage.

## Directory Structure

```
tests/fixtures/
├── 01_protocol/
│   ├── pico.yaml           # Sample PICO definition
│   └── eligibility.md      # Inclusion/exclusion criteria
├── 02_search/
│   ├── results.bib         # PubMed results (8 records, 1 duplicate)
│   ├── scopus.bib          # Scopus results (3 records, 1 duplicate)
│   ├── log.md              # Search log
│   └── db_counts.csv       # Database counts for PRISMA
├── 03_screening/
│   ├── decisions.csv       # Dual-review decisions (9 records)
│   └── quality.csv         # RoB 2 assessments
├── 04_fulltext/
│   ├── manifest.csv        # PDF manifest (7 included studies)
│   └── sample_abstract.txt # Sample abstract text
├── 05_extraction/
│   ├── data-dictionary.md  # Outcome definitions
│   └── extraction.csv      # Extracted data (7 studies, 18 rows)
└── 08_reviews/
    └── grade_summary.csv   # GRADE evidence table
```

## Test Scenario

**Topic**: CBT for major depression vs. TAU/waitlist

**Studies included**: 7 RCTs

- 2 excluded (wrong population, wrong intervention)
- 2 duplicates removed during deduplication

**Outcomes**:

- O1: HDRS (5 studies)
- O2: Response rate (3 studies)
- O3: PHQ-9 (2 studies)

## Running Tests

### Test deduplication

```bash
cd tooling/python
uv run ../../ma-search-bibliography/scripts/dedupe_bib.py \
  --in-bib ../../tests/fixtures/02_search/results.bib \
  --out-bib /tmp/test_dedupe.bib \
  --out-log /tmp/test_dedupe.log
# Expected: 7 unique records (1 duplicate removed)
```

### Test multi-DB merge

```bash
uv run ../../ma-search-bibliography/scripts/multi_db_dedupe.py \
  --in-bib ../../tests/fixtures/02_search/results.bib \
  --in-bib ../../tests/fixtures/02_search/scopus.bib \
  --out-merged /tmp/test_merged.bib \
  --out-bib /tmp/test_final.bib \
  --out-log /tmp/test_merge.log
# Expected: 9 unique records
```

### Test dual-review agreement

```bash
uv run ../../ma-screening-quality/scripts/dual_review_agreement.py \
  --file ../../tests/fixtures/03_screening/decisions.csv \
  --col-a decision_r1 \
  --col-b decision_r2 \
  --out /tmp/test_agreement.md
# Expected: High agreement (only 1 discrepancy)
```

### Test GRADE summary

```bash
uv run ../../ma-peer-review/scripts/init_grade_summary.py \
  --extraction ../../tests/fixtures/05_extraction/extraction.csv \
  --out-csv /tmp/test_grade.csv \
  --out-md /tmp/test_grade.md
```

### Test RoB 2 assessment

```bash
uv run ../../ma-peer-review/scripts/init_rob2_assessment.py \
  --extraction ../../tests/fixtures/05_extraction/extraction.csv \
  --out-csv /tmp/test_rob2.csv \
  --out-md /tmp/test_rob2.md
# Expected: 7 studies x 5 domains = 35 rows
```

### Test ROBINS-I assessment

```bash
uv run ../../ma-peer-review/scripts/init_robins_i_assessment.py \
  --extraction ../../tests/fixtures/05_extraction/extraction.csv \
  --out-csv /tmp/test_robins_i.csv \
  --out-md /tmp/test_robins_i.md
# Expected: 7 studies x 7 domains = 49 rows
```

### Test PROSPERO generation

```bash
uv run generate_prospero_protocol.py \
  --pico ../../01_protocol/pico.yaml \
  --out /tmp/test_prospero.md
# Expected: Formatted PROSPERO registration document
```

## Expected Results

| Stage      | Input      | Output       | Validation                  |
| ---------- | ---------- | ------------ | --------------------------- |
| Dedupe     | 8 PubMed   | 7 unique     | 1 duplicate by DOI          |
| Merge      | 11 total   | 9 unique     | 2 duplicates removed        |
| Screening  | 9 records  | 7 included   | 2 excluded with reasons     |
| Extraction | 7 studies  | 18 data rows | All required fields present |
| GRADE      | 3 outcomes | 3 GRADE rows | Certainty: moderate/low     |
| RoB 2      | 7 studies  | 35 rows      | 5 domains per study         |
| ROBINS-I   | 7 studies  | 49 rows      | 7 domains per study         |
| PROSPERO   | pico.yaml  | 1 document   | All PROSPERO fields filled  |

---

## Connection Tests

Tests API connectivity for each database. Requires `.env` with API keys.

```bash
uv run ../../tests/test_db_connections.py
```

| Database  | API         | Required Key                                |
| --------- | ----------- | ------------------------------------------- |
| PubMed    | E-utilities | `PUBMED_API_KEY` (optional but recommended) |
| Scopus    | Elsevier    | `SCOPUS_API_KEY`                            |
| Zotero    | Zotero API  | `ZOTERO_API_KEY`, `ZOTERO_LIBRARY_ID`       |
| Unpaywall | REST        | `UNPAYWALL_EMAIL`                           |
