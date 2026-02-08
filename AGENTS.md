# Agent Instructions

AI-assisted meta-analysis pipeline. This file is auto-loaded by Claude Code.

---

## Quick Start

**New project?** → Say "brainstorm" or "help me find a topic"
**Have TOPIC.txt?** → Say "start" or "continue"
**At Stage 06?** → Say "complete manuscript" or see [Manuscript Assembly](docs/MANUSCRIPT_ASSEMBLY.md)
**Want to see an example?** → Check `projects/ici-breast-cancer/` (99% complete meta-analysis)

---

## Example: Completed Meta-Analysis

**Location**: `projects/ici-breast-cancer/`

A **real, 99% complete meta-analysis** on immune checkpoint inhibitors in triple-negative breast cancer (TNBC):

**Key Metrics**:

- 5 RCTs, N=2,402 patients
- Primary outcome: RR 1.26 (95% CI 1.16-1.37), p=0.0015, ⊕⊕⊕⊕ HIGH quality
- Manuscript: 4,921 words (compliant with Lancet Oncology, JAMA Oncology)
- Time invested: ~14 hours (vs 100+ hours manual)

**Quick Tour**:

1. `projects/ici-breast-cancer/README.md` - Complete navigation guide
2. `projects/ici-breast-cancer/00_overview/FINAL_PROJECT_SUMMARY.md` - All findings (415 lines)
3. `projects/ici-breast-cancer/07_manuscript/` - Full manuscript (5 sections + 7 tables)
4. `projects/ici-breast-cancer/06_analysis/` - All R scripts + results

**Use this as a template** when starting your own meta-analysis.

---

## 📁 Project Structure (IMPORTANT)

**All projects are now in `projects/<project-name>/` directory.**

```
meta-pipe/
├── ma-*/                    # Framework code modules
├── docs/                    # Framework documentation
├── tooling/                 # Shared tools and scripts
└── projects/                # All your meta-analysis projects
    ├── legacy/              # Historical data (migrated 2026-02-08)
    ├── ici-breast-cancer/   # Example: complete meta-analysis
    └── your-project/        # Your new projects go here
        ├── 01_protocol/
        ├── 02_search/
        ├── ...
        └── TOPIC.txt
```

**When running commands**: Replace `<project-name>` with your actual project name.

---

## When User Says "Brainstorm" or "Help me find a topic"

Use the **brainstorm-topic** skill (`.claude/skills/brainstorm-topic.md`):

1. **Ask ONE question at a time** - don't overwhelm
2. **Guide through PICO** iteratively:
   - Clinical area → Condition → Population → Intervention → Comparator → Outcomes
3. **Check feasibility** - quick PubMed search to estimate study count
4. **Present refined topic** in structured format
5. **Save to `TOPIC.txt`** once confirmed
6. **Offer to start** the pipeline

Example prompts that trigger this:

- "help me brainstorm a topic"
- "I don't know what to study"
- "help me refine my research question"
- "/brainstorm"

---

## When User Says "Complete Manuscript" or "Prepare for Submission"

**📖 See**: [Manuscript Assembly Guide](docs/MANUSCRIPT_ASSEMBLY.md)

Use the **meta-manuscript-assembly** skill - it will guide you through:

- Tables Creation (2-3h)
- Figure Assembly (1-2h)
- References Management (1-2h)
- Figure Legends (30-60min)
- Quality Assurance (30-60min)

**Expected**: 6-8 hours to publication-ready manuscript

---

## When User Says "Start" or "See TOPIC.txt"

⚠️ **MANDATORY FIRST STEP**: Run 4-hour feasibility assessment ([FEASIBILITY_CHECKLIST.md](FEASIBILITY_CHECKLIST.md)) before any data extraction or protocol writing.

**Why**: Prevents 10-40 hours of wasted work on unanswerable research questions.

Then proceed:

1. **Ask for project name** if not already specified
2. **Read `projects/<project-name>/TOPIC.txt`** to understand the research question
3. **Check project state** - which stages are complete in `projects/<project-name>/`?
4. **Ask only essential questions** before proceeding:
   - Databases to search (PubMed, Scopus, Embase, Cochrane?)
   - Date range limits?
   - Language restrictions?
   - Study design (RCTs only, or include observational?)
5. **Initialize project** if not done:
   ```bash
   cd /Users/htlin/meta-pipe
   uv run tooling/python/init_project.py --name <project-name>
   ```
6. **Execute pipeline stages** in order, validating at each step

**⚠️ IMPORTANT**: All project data is in `projects/<project-name>/`. All commands below assume you're working with a specific project.

---

## Resume Behavior

If user says "continue", "what's next", or "status":

1. Check which stage folders have content
2. Report current progress
3. Suggest next action

---

## Rules

- **Python**: Always `uv run`, never `python3` directly
- **Dependencies**: `uv add <package>`
- **API keys**: Read from `.env` ([docs/API_SETUP.md](docs/API_SETUP.md))
- **Rounds**: Keep all `round-XX` data, never overwrite
- **Delete**: Use `rip` not `rm`

---

## Pipeline Stages

| Stage | Folder           | Key Output                | Validation          |
| ----- | ---------------- | ------------------------- | ------------------- |
| 01    | `01_protocol/`   | pico.yaml, eligibility.md | PICO complete       |
| 02    | `02_search/`     | dedupe.bib                | Records > 0         |
| 03    | `03_screening/`  | decisions.csv             | Kappa ≥ 0.60        |
| 04    | `04_fulltext/`   | manifest.csv              | PDFs collected      |
| 05    | `05_extraction/` | extraction.csv            | No missing study_id |
| 06    | `06_analysis/`   | figures/, tables/         | R scripts 01-12     |
| 07    | `07_manuscript/` | manuscript.pdf            | PRISMA complete     |
| 08    | `08_reviews/`    | grade_summary.md          | GRADE filled        |
| 09    | `09_qa/`         | final_qa_report.md        | All checks pass     |

---

## Decision Points (Ask User)

Only ask if information is missing from TOPIC.txt:

- Target population, intervention, comparator, outcomes (PICO)
- Which databases to search
- Risk-of-bias tool (RoB 2 vs ROBINS-I)
- Effect measure (RR/OR/HR/SMD/MD)
- Subgroup variables

---

## Commands Reference

<details>
<summary><strong>Stage 01: Protocol & PROSPERO</strong></summary>

```bash
cd /Users/htlin/meta-pipe/tooling/python

# Generate PROSPERO registration document from pico.yaml
uv add pyyaml
uv run generate_prospero_protocol.py \
  --pico ../../projects/<project-name>/01_protocol/pico.yaml \
  --out ../../projects/<project-name>/01_protocol/prospero_registration.md
```

Review the generated document, edit as needed, then submit to PROSPERO.
Update `prospero_id` in `pico.yaml` once registered.

</details>

<details>
<summary><strong>Stage 02: Search</strong></summary>

```bash
cd /Users/htlin/meta-pipe/tooling/python

# Build queries from PICO
uv run ../../ma-search-bibliography/scripts/build_queries.py \
  --pico ../../projects/<project-name>/01_protocol/pico.yaml \
  --out ../../projects/<project-name>/02_search/round-01/queries.txt

# With MeSH expansion
uv run ../../ma-search-bibliography/scripts/expand_terms.py \
  --pico ../../projects/<project-name>/01_protocol/pico.yaml \
  --out ../../projects/<project-name>/02_search/round-01/expanded_terms.yaml

# PubMed search
uv add biopython requests bibtexparser pyyaml
uv run ../../ma-search-bibliography/scripts/pubmed_fetch.py \
  --query "<query>" --email "you@example.com" \
  --out-bib ../../projects/<project-name>/02_search/round-01/results.bib \
  --out-log ../../projects/<project-name>/02_search/round-01/log.md

# Scopus search (requires SCOPUS_API_KEY in .env)
uv run ../../ma-search-bibliography/scripts/scopus_fetch.py \
  --query "<query>" --out-bib ../../projects/<project-name>/02_search/round-01/scopus.bib

# Embase search (requires EMBASE_API_KEY in .env)
uv run ../../ma-search-bibliography/scripts/embase_fetch.py \
  --query "<query>" --out-bib ../../projects/<project-name>/02_search/round-01/embase.bib

# Cochrane search
uv run ../../ma-search-bibliography/scripts/cochrane_fetch.py \
  --query "<query>" --out-bib ../../projects/<project-name>/02_search/round-01/cochrane.bib

# Multi-DB merge and dedupe
uv run ../../ma-search-bibliography/scripts/multi_db_dedupe.py \
  --in-bib ../../projects/<project-name>/02_search/round-01/results.bib \
  --in-bib ../../projects/<project-name>/02_search/round-01/scopus.bib \
  --in-bib ../../projects/<project-name>/02_search/round-01/embase.bib \
  --out-merged ../../projects/<project-name>/02_search/round-01/merged.bib \
  --out-bib ../../projects/<project-name>/02_search/round-01/dedupe.bib

# Or run all databases at once
uv run ../../ma-search-bibliography/scripts/run_multi_db_search.py \
  --root ../../projects/<project-name>/../projects/<project-name> --round round-01 --email "you@example.com"

# Single-source dedupe
uv run ../../ma-search-bibliography/scripts/dedupe_bib.py \
  --in-bib ../../projects/<project-name>/02_search/round-01/results.bib \
  --out-bib ../../projects/<project-name>/02_search/round-01/dedupe.bib \
  --out-log ../../projects/<project-name>/02_search/round-01/dedupe.log

# Zotero integration (optional)
uv run ../../ma-search-bibliography/scripts/zotero_fetch.py \
  --collection-key "<key>" --out-bib ../../projects/<project-name>/02_search/round-01/zotero.bib

uv run ../../ma-search-bibliography/scripts/zotero_sync.py \
  --in-bib ../../projects/<project-name>/02_search/round-01/dedupe.bib --collection-key "<key>"
```

**📖 See**: [Zotero Setup Guide](docs/ZOTERO_SETUP.md) for detailed Zotero configuration

</details>

<details>
<summary><strong>Stage 02→03: BibTeX to CSV Conversion</strong></summary>

```bash
cd /Users/htlin/meta-pipe/tooling/python

# Convert BibTeX to CSV for screening
uv run bib_to_csv.py \
  --in-bib ../../projects/<project-name>/02_search/round-01/dedupe.bib \
  --out-csv ../../projects/<project-name>/03_screening/round-01/decisions.csv
```

This creates a CSV with columns: `record_id, entry_type, authors, year, title, journal, abstract, doi, pmid, keywords, decision_r1, decision_r2, final_decision, exclusion_reason, notes`

Fill in `decision_r1` and `decision_r2` columns during screening.

**📖 See**: [Rayyan Setup Guide](docs/RAYYAN_SETUP.md) for web-based collaborative screening alternative

</details>

<details>
<summary><strong>Stage 03: Screening</strong></summary>

Required CSV columns: `record_id, title, decision_r1, decision_r2, final_decision, exclusion_reason`

```bash
cd /Users/htlin/meta-pipe/tooling/python

# Dual-review agreement analysis
uv run ../../ma-screening-quality/scripts/dual_review_agreement.py \
  --file ../../projects/<project-name>/03_screening/round-01/decisions.csv \
  --col-a decision_r1 --col-b decision_r2 \
  --out ../../projects/<project-name>/03_screening/round-01/agreement.md
```

</details>

<details>
<summary><strong>Stage 04: Fulltext</strong></summary>

```bash
cd /Users/htlin/meta-pipe/tooling/python

# Extract BibTeX subset for full-text review (from screening results)
uv run ../../ma-search-bibliography/scripts/bib_subset_by_ids.py \
  --in-csv ../../projects/<project-name>/03_screening/round-01/decisions_screened.csv \
  --in-bib ../../projects/<project-name>/02_search/round-01/dedupe.bib \
  --out-bib ../../projects/<project-name>/04_fulltext/round-01/fulltext_subset.bib \
  --filter-column final_decision \
  --filter-value Include

# Alternative: Extract ALL records for full-text (Include + Uncertain)
uv run ../../ma-search-bibliography/scripts/bib_subset_by_ids.py \
  --in-csv ../../projects/<project-name>/04_fulltext/round-01/pdf_retrieval_manifest.csv \
  --in-bib ../../projects/<project-name>/02_search/round-01/dedupe.bib \
  --out-bib ../../projects/<project-name>/04_fulltext/round-01/fulltext_subset.bib

# Query Unpaywall API for Open Access status (ROBUST VERSION - recommended)
# This version handles HTTP 422 errors and other API issues gracefully
uv run ../../ma-fulltext-management/scripts/unpaywall_fetch_robust.py \
  --in-bib ../../projects/<project-name>/04_fulltext/round-01/fulltext_subset.bib \
  --out-csv ../../projects/<project-name>/04_fulltext/round-01/unpaywall_results.csv \
  --out-log ../../projects/<project-name>/04_fulltext/round-01/unpaywall_fetch.log \
  --out-json ../../projects/<project-name>/04_fulltext/round-01/unpaywall_results.json \
  --email "your@email.com" \
  --continue-on-error \
  --max-retries 3

# Analyze Unpaywall results
uv run ../../ma-fulltext-management/scripts/analyze_unpaywall.py \
  --in-csv ../../projects/<project-name>/04_fulltext/round-01/unpaywall_results.csv \
  --out-md ../../projects/<project-name>/04_fulltext/round-01/unpaywall_summary.md

# Download Open Access PDFs automatically
uv run ../../ma-fulltext-management/scripts/download_oa_pdfs.py \
  --in-csv ../../projects/<project-name>/04_fulltext/round-01/unpaywall_results.csv \
  --pdf-dir ../../projects/<project-name>/04_fulltext/round-01/pdfs \
  --out-log ../../projects/<project-name>/04_fulltext/round-01/pdf_download.log \
  --sleep 1 \
  --max-retries 3
```

**Expected results**:

- 40-60% PDFs downloaded automatically (Gold/Green OA)
- Remaining PDFs need manual retrieval via institutional access
- See `unpaywall_summary.md` for retrieval statistics

**📖 See**:

- [Unpaywall Robust Implementation](docs/UNPAYWALL_ROBUST.md) - Error handling details
- [Unpaywall vs Alternatives](docs/UNPAYWALL_COMPARISON.md) - Compare with other PDF sources

</details>

<details>
<summary><strong>Stage 05: Extraction</strong></summary>

**Choose extraction approach based on PDF availability:**

1. **Web-Based Extraction** (NEW) - No PDFs needed, 2-4 hours, 70-80% completeness
2. **PDF-Based Extraction** - Requires PDFs, 8-12 hours, 100% completeness
3. **Hybrid Approach** (RECOMMENDED) - Best of both, 4-6 hours, 90-95% completeness

**📖 See**: [Web-Based Extraction Guide](docs/WEB_EXTRACTION.md) for detailed comparison and workflow

---

### Option 1: Web-Based Extraction (No PDFs Needed)

**Use when**: No institutional access to PDFs, time-sensitive, or preliminary analysis

```bash
cd /Users/htlin/meta-pipe/tooling/python

# Step 1: Prepare study identifiers
uv run extract_study_identifiers.py \
  --in-csv ../../projects/<project-name>/03_screening/round-01/decisions_screened.csv \
  --filter-column final_decision \
  --filter-value Include \
  --out-csv ../../projects/<project-name>/05_extraction/round-01/web_extraction_manifest.csv

# Step 2: Web search for each study (PubMed API, ClinicalTrials.gov, etc.)
uv run web_search_study_data.py \
  --manifest ../../projects/<project-name>/05_extraction/round-01/web_extraction_manifest.csv \
  --data-dict ../../projects/<project-name>/05_extraction/data-dictionary.md \
  --out-jsonl ../../projects/<project-name>/05_extraction/round-01/web_extracted.jsonl \
  --out-log ../../projects/<project-name>/05_extraction/round-01/web_search.log

# Step 3: AI-assisted field population with confidence scores
uv run ai_populate_extraction.py \
  --web-data ../../projects/<project-name>/05_extraction/round-01/web_extracted.jsonl \
  --data-dict ../../projects/<project-name>/05_extraction/data-dictionary.md \
  --out-csv ../../projects/<project-name>/05_extraction/round-01/extraction_web.csv \
  --confidence-threshold 0.7

# Step 4: Flag low-confidence fields for manual review
uv run flag_low_confidence.py \
  --extraction ../../projects/<project-name>/05_extraction/round-01/extraction_web.csv \
  --confidence-threshold 0.7 \
  --out-md ../../projects/<project-name>/05_extraction/round-01/needs_verification.md
```

**Expected**: 70-80% data completeness, 2-4 hours total time

---

### Option 2: PDF-Based Extraction (Full Access Required)

**Recommended: LLM-Assisted Extraction (using Claude CLI)**

Requires: `claude` CLI (subscription) or `codex` CLI installed

```bash
cd /Users/htlin/meta-pipe/tooling/python

# Step 1: Extract PDF text
uv add pdfplumber
uv run extract_pdf_text.py \
  --pdf-dir ../../projects/<project-name>/04_fulltext/round-01/pdfs \
  --out-jsonl ../../projects/<project-name>/05_extraction/round-01/pdf_texts.jsonl \
  --pattern "*.pdf"

# Step 2: Create extraction template
uv run create_extraction_template.py \
  --pdf-jsonl ../../projects/<project-name>/05_extraction/round-01/pdf_texts.jsonl \
  --data-dict ../../projects/<project-name>/05_extraction/data-dictionary.md \
  --out-csv ../../projects/<project-name>/05_extraction/round-01/extraction_template.csv

# Step 3: Create LLM manifest
uv run create_pdf_manifest.py \
  --pdf-jsonl ../../projects/<project-name>/05_extraction/round-01/pdf_texts.jsonl \
  --out-csv ../../projects/<project-name>/05_extraction/round-01/manifest.csv

# Step 4: LLM extraction using Claude CLI (no API key needed)
uv run llm_extract_cli.py \
  --pdf-jsonl ../../projects/<project-name>/05_extraction/round-01/pdf_texts.jsonl \
  --data-dict ../../projects/<project-name>/05_extraction/data-dictionary.md \
  --out-jsonl ../../projects/<project-name>/05_extraction/round-01/llm_extracted_all.jsonl \
  --cli claude

# Step 5: Convert to CSV format
uv run jsonl_to_extraction_csv.py \
  --jsonl ../../projects/<project-name>/05_extraction/round-01/llm_extracted_all.jsonl \
  --data-dict ../../projects/<project-name>/05_extraction/data-dictionary.md \
  --out-csv ../../projects/<project-name>/05_extraction/round-01/extraction.csv

# Step 6: Manual review and updates
# (Edit extraction.csv manually to correct LLM errors)

# Step 7: Update extraction with manual corrections
uv run update_extraction_manual.py \
  --llm-jsonl ../../projects/<project-name>/05_extraction/round-01/llm_extracted_all.jsonl \
  --manual-csv ../../projects/<project-name>/05_extraction/round-01/extraction_manual.csv \
  --out-csv ../../projects/<project-name>/05_extraction/round-01/extraction.csv

# Step 8: Validate extraction quality
uv run validate_extraction.py \
  --csv ../../projects/<project-name>/05_extraction/round-01/extraction.csv \
  --out-md ../../projects/<project-name>/05_extraction/round-01/validation_report.md
```

**Expected results**:

- 100% success rate (all PDFs processed)
- 65-70% time savings vs manual extraction
- Some missing fields will need manual review
- See `validation_report.md` for data quality issues

</details>

<details>
<summary><strong>Risk of Bias Assessment</strong></summary>

**⚠️ IMPORTANT**: Perform after extraction is complete (`extraction.csv` ready)

**Choose assessment tool based on study design:**

- **RoB 2** for randomized controlled trials (RCTs)
- **ROBINS-I** for non-randomized studies (cohort, case-control)

```bash
cd /Users/htlin/meta-pipe/tooling/python

# RoB 2 for RCTs
uv run ../../ma-peer-review/scripts/init_rob2_assessment.py \
  --extraction ../../projects/<project-name>/05_extraction/round-01/extraction.csv \
  --out-csv ../../projects/<project-name>/05_extraction/round-01/quality_rob2.csv \
  --out-md ../../projects/<project-name>/05_extraction/round-01/rob2_assessment.md

# ROBINS-I for cohort/observational studies
uv run ../../ma-peer-review/scripts/init_robins_i_assessment.py \
  --extraction ../../projects/<project-name>/05_extraction/round-01/extraction.csv \
  --out-csv ../../projects/<project-name>/05_extraction/round-01/quality_robins_i.csv \
  --out-md ../../projects/<project-name>/05_extraction/round-01/robins_i_assessment.md
```

**Assessment domains:**

**RoB 2** (5 domains):

1. Randomization process
2. Deviations from intended interventions
3. Missing outcome data
4. Measurement of the outcome
5. Selection of the reported result

**ROBINS-I** (7 domains):

1. Confounding
2. Selection of participants
3. Classification of interventions
4. Deviations from intended interventions
5. Missing data
6. Measurement of outcomes
7. Selection of the reported result

**Expected time**: 2-3 hours for 10-20 studies (dual review recommended)

**Templates**: `ma-peer-review/references/rob2-template.md`, `ma-peer-review/references/robins-i-template.md`

</details>

<details>
<summary><strong>Stage 06: Analysis (R)</strong></summary>

**⚠️ IMPORTANT**: All statistical analysis and figure generation must be done in R.

**📖 See**: [R Figure Generation Guide](docs/R_FIGURE_GUIDE.md) for package resources and examples

Run in order from `06_analysis/`:

**Core analysis (ma-meta-analysis/assets/r/):**

```r
# Execute R scripts in order
01_setup.R                    # Load packages, set theme
02_effect_sizes.R             # Calculate RR/OR/HR
03_models.R                   # Random-effects meta-analysis
04_subgroups_meta_regression.R # Subgroup analysis
05_plots.R                    # Forest plots, funnel plots (300 DPI)
06_tables.R                   # Summary tables
07_sensitivity.R              # Sensitivity analysis
08_bias.R                     # Publication bias assessment
09_validation.R               # Leave-one-out analysis
```

**Publication quality (ma-publication-quality/assets/r/):**

```r
10_hakn_prediction.R           # Hartung-Knapp prediction intervals
11_influence_diagnostics.R     # Influence analysis
12_sof_table.R                 # Summary of Findings table
```

**Figure export**:

```r
# Always export at 300 DPI
ggsave("figures/figure1.png", width=10, height=8, dpi=300)

# For base R plots
png("figures/figure1.png", width=10, height=8, units="in", res=300)
forest(res)
dev.off()
```

**R Package Resources**:

- **CRAN**: https://cran.r-project.org/ (official repository)
- **Tidyverse**: https://www.tidyverse.org/ (ggplot2, dplyr)
- **Bioconductor**: https://bioconductor.org/ (bioinformatics)
- **rOpenSci**: https://ropensci.org/ (peer-reviewed tools)
- **R-universe**: https://r-universe.dev/ (search all packages)

Use `renv` for reproducibility. Copy R scripts from asset folders to `06_analysis/`.

</details>

<details>
<summary><strong>Stage 07: Manuscript</strong></summary>

**📖 See**: [Manuscript Assembly Guide](docs/MANUSCRIPT_ASSEMBLY.md) for detailed workflow

```bash
# PRISMA flow
uv run ../../ma-manuscript-quarto/scripts/prisma_flow.py \
  --root ../../projects/<project-name>/../projects/<project-name> --round round-01 --decisions-column final_decision \
  --out ../../projects/<project-name>/07_manuscript/prisma_flow.md \
  --out-svg ../../projects/<project-name>/07_manuscript/prisma_flow.svg

# Evidence map (verify what exists before writing Results)
uv run ../../ma-manuscript-quarto/scripts/build_evidence_map.py \
  --root ../../projects/<project-name>/../projects/<project-name> --round round-01 \
  --out projects/<project-name>/07_manuscript/evidence_map.md

# Result claims table
uv run ../../ma-manuscript-quarto/scripts/init_result_claims.py \
  --root ../../projects/<project-name>/.. --out projects/<project-name>/07_manuscript/result_claims.csv

# Generate result paragraphs
uv run ../../ma-manuscript-quarto/scripts/build_result_paragraphs.py \
  --claims projects/<project-name>/07_manuscript/result_claims.csv \
  --out projects/<project-name>/07_manuscript/result_paragraphs.md

# Study characteristics table
uv run ../../ma-manuscript-quarto/scripts/build_study_characteristics.py \
  --extraction projects/<project-name>/05_extraction/extraction.csv \
  --out-csv projects/<project-name>/07_manuscript/study_characteristics.csv \
  --out-md projects/<project-name>/07_manuscript/study_characteristics.md \
  --results projects/<project-name>/07_manuscript/03_results.qmd

# Assemble Results into 03_results.qmd
uv run ../../ma-manuscript-quarto/scripts/assemble_results.py \
  --results projects/<project-name>/07_manuscript/03_results.qmd \
  --paragraphs projects/<project-name>/07_manuscript/result_paragraphs.qmd

# Submission checklist (journal-specific)
uv run ../../ma-manuscript-quarto/scripts/init_submission_checklist.py \
  --project <project-name> --journal "<target journal>" \
  --out projects/<project-name>/07_manuscript/submission_checklist.md

# Results consistency report (QA)
uv run ../../ma-manuscript-quarto/scripts/results_consistency_report.py \
  --root ../../projects/<project-name>/.. \
  --out projects/<project-name>/09_qa/results_consistency_report.md \
  --strict

# Render
uv run ../../ma-manuscript-quarto/scripts/render_manuscript.py \
  --root ../../projects/<project-name>/.. --index projects/<project-name>/07_manuscript/index.qmd
```

</details>

<details>
<summary><strong>Stage 08: GRADE</strong></summary>

```bash
uv run ../../ma-peer-review/scripts/init_grade_summary.py \
  --extraction ../../projects/<project-name>/05_extraction/extraction.csv \
  --out-csv ../../projects/<project-name>/08_reviews/grade_summary.csv \
  --out-md ../../projects/<project-name>/08_reviews/grade_summary.md

uv run ../../ma-peer-review/scripts/auto_grade_suggestion.py \
  --grade ../../projects/<project-name>/08_reviews/grade_summary.csv \
  --out-csv ../../projects/<project-name>/08_reviews/grade_suggestions.csv
```

</details>

<details>
<summary><strong>Stage 09: QA</strong></summary>

```bash
uv run ../../ma-end-to-end/scripts/final_qa_report.py \
  --root ../../projects/<project-name>/../projects/<project-name> --round round-01 \
  --out projects/<project-name>/09_qa/final_qa_report.md --out-json projects/<project-name>/09_qa/final_qa_report.json

# Publication quality checks
uv run ../../ma-publication-quality/scripts/init_reporting_checklists.py \
  --root ../../projects/<project-name>/.. --include-moose

uv run ../../ma-publication-quality/scripts/claim_audit.py \
  --abstract ../../projects/<project-name>/07_manuscript/00_abstract.qmd \
  --results ../../projects/<project-name>/07_manuscript/03_results.qmd \
  --out ../../projects/<project-name>/09_qa/claim_audit.md

uv run ../../ma-publication-quality/scripts/crossref_check.py \
  --manuscript-dir ../../projects/<project-name>/07_manuscript \
  --figures-dir ../../projects/<project-name>/06_analysis/figures \
  --out ../../projects/<project-name>/09_qa/crossref_report.md

# Hash artifacts for reproducibility audit
uv run ../../ma-end-to-end/scripts/hash_artifacts.py \
  --root ../../projects/<project-name>/.. --out projects/<project-name>/09_qa/artifact_hashes.json
```

</details>

<details>
<summary><strong>Checkpoints</strong></summary>

```bash
# Create checkpoint before risky operations
uv run ../../ma-end-to-end/scripts/checkpoint.py --create --name pre-analysis

# List checkpoints
uv run ../../ma-end-to-end/scripts/checkpoint.py --list

# Restore (requires --yes)
uv run ../../ma-end-to-end/scripts/checkpoint.py --restore --name pre-analysis --yes
```

</details>

---

## QA Thresholds

| Check                       | Threshold | Action if Failed             |
| --------------------------- | --------- | ---------------------------- |
| Dual-review kappa           | ≥ 0.60    | Flag, require reconciliation |
| Missing study_id            | 0         | Block extraction             |
| Numeric fields              | ≥ 0       | Block analysis               |
| PRISMA NA counts            | 0         | Reconcile before render      |
| Result-to-table mapping     | 100%      | Block manuscript             |
| Figure DPI                  | ≥ 300     | Re-export from R             |
| Figure panel labels         | Required  | Add A, B, C labels           |
| Reference DOI coverage      | ≥ 90%     | Manual DOI lookup            |
| Citation mapping            | 100%      | Block manuscript render      |
| Word count (target journal) | ±10%      | Edit for compliance          |
| PRISMA checklist items      | 27/27     | Block submission             |

---

## Documentation

**Essential**:

- [Time Investment Guidance](docs/TIME_GUIDANCE.md) - Realistic timeline expectations (22-32 hours)
- [Manuscript Assembly](docs/MANUSCRIPT_ASSEMBLY.md) - Stage 07 complete workflow (6-8 hours)
- [R Figure Generation](docs/R_FIGURE_GUIDE.md) - Task-based guides (Progressive Disclosure)
  - [Forest Plots](docs/r-guides/01-forest-plots.md) - 15-30 min
  - [Table 1](docs/r-guides/05-table1-gtsummary.md) - 30-60 min
  - [Multi-Panel Figures](docs/r-guides/04-multi-panel.md) - 15-20 min
- [Journal Formatting](docs/JOURNAL_FORMATTING.md) - Lancet/JAMA/Nature Medicine requirements

**Reference**:

- [Web-Based Extraction](docs/WEB_EXTRACTION.md) - Alternative to PDF extraction (NEW)
- [Skill Generalization](docs/SKILL_GENERALIZATION.md) - Extract workflows at 95%+ completion
- [API Setup](docs/API_SETUP.md) - Configure API keys for Scopus/Embase
- [Getting Started](GETTING_STARTED.md) - Detailed step-by-step guide

**Example Project**:

- [ICI in TNBC Meta-Analysis](projects/ici-breast-cancer/) - Complete 99% finished project (5 RCTs, N=2,402)
  - See `projects/ici-breast-cancer/README.md` for navigation
  - Use as template for your own meta-analysis

**Templates**: Each `ma-*/references/` folder contains protocol and analysis templates
