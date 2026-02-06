# Getting Started

Quick guide to run the meta-analysis pipeline with uv, R/renv, and Quarto.

## Prerequisites

- `uv` on PATH
- R (≥ 4.2) + `renv`
- Quarto
- API keys in `.env` ([setup guide](docs/API_SETUP.md))

## 0. Configure API Keys

```bash
cp .env.example .env  # Edit with your keys
```

Minimum: `PUBMED_API_KEY` — [Get from NCBI](https://www.ncbi.nlm.nih.gov/account/)

## 1. Initialize Project

```bash
cd tooling/python && uv init
uv run ../../ma-end-to-end/scripts/init_project.py --root ../..
```

## 2. Edit TOPIC.txt

Write your research question in `TOPIC.txt`.

## 3. Create Protocol (Stage 01)

Use `ma-topic-intake` to generate: `pico.yaml`, `eligibility.md`, `outcomes.md`, `search-plan.md`

### Generate PROSPERO Registration

```bash
cd tooling/python
uv add pyyaml
uv run generate_prospero_protocol.py \
  --pico ../../01_protocol/pico.yaml \
  --out ../../01_protocol/prospero_registration.md
```

Review, edit, and submit to [PROSPERO](https://www.crd.york.ac.uk/prospero/). Update `prospero_id` in `pico.yaml` once registered.

## 4. Run Search (Stage 02)

<details>
<summary><strong>PubMed (basic)</strong></summary>

```bash
cd tooling/python
uv add biopython requests bibtexparser pyyaml
uv run ../../ma-search-bibliography/scripts/pubmed_fetch.py \
  --query "<your query>" --email "you@example.com" \
  --out-bib ../../02_search/round-01/results.bib \
  --out-log ../../02_search/round-01/log.md
uv run ../../ma-search-bibliography/scripts/dedupe_bib.py \
  --in-bib ../../02_search/round-01/results.bib \
  --out-bib ../../02_search/round-01/dedupe.bib \
  --out-log ../../02_search/round-01/dedupe.log
```

</details>

<details>
<summary><strong>Multi-DB (Scopus, Embase, Cochrane)</strong></summary>

```bash
# Scopus
uv run ../../ma-search-bibliography/scripts/scopus_fetch.py \
  --query "<query>" --out-bib ../../02_search/round-01/scopus.bib

# Embase
uv run ../../ma-search-bibliography/scripts/embase_fetch.py \
  --query "<query>" --out-bib ../../02_search/round-01/embase.bib

# Merge all
uv run ../../ma-search-bibliography/scripts/multi_db_dedupe.py \
  --in-bib ../../02_search/round-01/results.bib \
  --in-bib ../../02_search/round-01/scopus.bib \
  --out-merged ../../02_search/round-01/merged.bib \
  --out-bib ../../02_search/round-01/dedupe.bib
```

Or run all at once:

```bash
uv run ../../ma-search-bibliography/scripts/run_multi_db_search.py \
  --root ../.. --round round-01 --email "you@example.com"
```

</details>

<details>
<summary><strong>Build queries from PICO</strong></summary>

```bash
uv run ../../ma-search-bibliography/scripts/build_queries.py \
  --pico ../../01_protocol/pico.yaml \
  --out ../../02_search/round-01/queries.txt

# With MeSH expansion
uv run ../../ma-search-bibliography/scripts/expand_terms.py \
  --pico ../../01_protocol/pico.yaml \
  --out ../../02_search/round-01/expanded_terms.yaml
```

</details>

<details>
<summary><strong>Zotero sync</strong></summary>

```bash
# Fetch from Zotero
uv run ../../ma-search-bibliography/scripts/zotero_fetch.py \
  --collection-key "<key>" --out-bib ../../02_search/round-01/zotero.bib

# Sync back to Zotero
uv run ../../ma-search-bibliography/scripts/zotero_sync.py \
  --in-bib ../../02_search/round-01/dedupe.bib --collection-key "<key>"
```

</details>

## 5. Screen Studies (Stage 03)

Fill `03_screening/round-01/decisions.csv` with columns: `record_id, title, decision_r1, decision_r2, final_decision, exclusion_reason`

```bash
uv run ../../ma-screening-quality/scripts/dual_review_agreement.py \
  --file ../../03_screening/round-01/decisions.csv \
  --col-a decision_r1 --col-b decision_r2 \
  --out ../../03_screening/round-01/agreement.md
```

## 6. Collect Fulltext (Stage 04)

Place PDFs in `04_fulltext/` and fill `manifest.csv`.

<details>
<summary><strong>Unpaywall lookup</strong></summary>

```bash
uv run ../../ma-fulltext-management/scripts/unpaywall_fetch.py \
  --in-bib ../../03_screening/round-01/included.bib \
  --out-csv ../../04_fulltext/unpaywall_results.csv
```

</details>

## 7. Extract Data (Stage 05)

Fill `05_extraction/extraction.csv` and `data-dictionary.md`.

<details>
<summary><strong>LLM-assisted extraction</strong></summary>

```bash
uv add pdfplumber
uv run ../../ma-data-extraction/scripts/llm_extract.py \
  --manifest ../../04_fulltext/manifest.csv \
  --data-dictionary ../../05_extraction/data-dictionary.md \
  --out-jsonl ../../05_extraction/llm_suggestions.jsonl
```

</details>

## 8. Run Analysis (Stage 06)

**Core analysis (ma-meta-analysis/assets/r/):**

```
01_setup.R → 02_effect_sizes.R → 03_models.R → 04_subgroups_meta_regression.R
→ 05_plots.R → 06_tables.R → 07_sensitivity.R → 08_bias.R → 09_validation.R
```

**Publication quality (ma-publication-quality/assets/r/):**

```
10_hakn_prediction.R    # Hartung-Knapp prediction intervals
11_influence_diagnostics.R  # Leave-one-out influence analysis
12_sof_table.R          # Summary of Findings table
```

Use `renv` for reproducibility. Copy R scripts from asset folders to `06_analysis/`.

## 9. Assemble Manuscript (Stage 07)

<details>
<summary><strong>PRISMA flow + render</strong></summary>

```bash
uv run ../../ma-manuscript-quarto/scripts/prisma_flow.py \
  --root ../.. --round round-01 --decisions-column final_decision \
  --out ../../07_manuscript/prisma_flow.md --out-svg ../../07_manuscript/prisma_flow.svg

uv run ../../ma-manuscript-quarto/scripts/build_evidence_map.py \
  --root ../.. --round round-01 \
  --out 07_manuscript/evidence_map.md

uv run ../../ma-manuscript-quarto/scripts/init_result_claims.py \
  --root ../.. \
  --out 07_manuscript/result_claims.csv
Render will fail if any claim is missing `effect_estimate`, `ci`, `p_value`, or `citation_keys`.
Fill `citation_keys` as comma-separated BibTeX keys (e.g., `smith2020,doe2019`).

uv run ../../ma-manuscript-quarto/scripts/build_result_paragraphs.py \
  --claims 07_manuscript/result_claims.csv \
  --out 07_manuscript/result_paragraphs.md
This also writes `07_manuscript/result_paragraphs.qmd` and `07_manuscript/result_summary_table.md`.
Set `RESULTS_MIN_WORDS` in your environment to change minimum words per claim paragraph (default 25).

uv run ../../ma-manuscript-quarto/scripts/build_study_characteristics.py \
  --extraction 05_extraction/extraction.csv \
  --out-csv 07_manuscript/study_characteristics.csv \
  --out-md 07_manuscript/study_characteristics.md \
  --results 07_manuscript/03_results.qmd

uv run ../../ma-manuscript-quarto/scripts/assemble_results.py \
  --results 07_manuscript/03_results.qmd \
  --paragraphs 07_manuscript/result_paragraphs.qmd
This also inserts `result_summary_table.md` into `03_results.qmd`.

uv run ../../ma-manuscript-quarto/scripts/init_submission_checklist.py \
  --journal "<target journal>" \
  --out 07_manuscript/submission_checklist.md

uv run ../../ma-manuscript-quarto/scripts/results_consistency_report.py \
  --root ../.. \
  --out 09_qa/results_consistency_report.md \
  --strict

uv run ../../ma-manuscript-quarto/scripts/insert_traceability_table.py \
  --root ../.. --round round-01 \
  --methods 07_manuscript/02_methods.qmd \
  --out-table 07_manuscript/traceability_table.md

uv run ../../ma-manuscript-quarto/scripts/render_manuscript.py \
  --root ../.. --index 07_manuscript/index.qmd
```

</details>

## 10. Risk of Bias Assessment

<details>
<summary><strong>RoB 2 (for RCTs)</strong></summary>

```bash
cd tooling/python
uv run ../../ma-peer-review/scripts/init_rob2_assessment.py \
  --extraction ../../05_extraction/round-01/extraction.csv \
  --out-csv ../../03_screening/round-01/quality_rob2.csv \
  --out-md ../../03_screening/round-01/rob2_assessment.md
```

</details>

<details>
<summary><strong>ROBINS-I (for cohort/observational studies)</strong></summary>

```bash
cd tooling/python
uv run ../../ma-peer-review/scripts/init_robins_i_assessment.py \
  --extraction ../../05_extraction/round-01/extraction.csv \
  --out-csv ../../03_screening/round-01/quality_robins_i.csv \
  --out-md ../../03_screening/round-01/robins_i_assessment.md
```

</details>

## 11. GRADE & Reviews (Stage 08)

<details>
<summary><strong>GRADE summary</strong></summary>

```bash
cd tooling/python
uv run ../../ma-peer-review/scripts/init_grade_summary.py \
  --extraction ../../05_extraction/extraction.csv \
  --out-csv ../../08_reviews/grade_summary.csv \
  --out-md ../../08_reviews/grade_summary.md

uv run ../../ma-peer-review/scripts/auto_grade_suggestion.py \
  --grade ../../08_reviews/grade_summary.csv \
  --out-csv ../../08_reviews/grade_suggestions.csv \
  --out-md ../../08_reviews/grade_suggestions.md
```

</details>

## 12. Final QA (Stage 09)

```bash
uv run ../../ma-end-to-end/scripts/final_qa_report.py \
  --root ../.. --round round-01 \
  --out 09_qa/final_qa_report.md --out-json 09_qa/final_qa_report.json
```

<details>
<summary><strong>Publication quality checks</strong></summary>

```bash
# Init checklists
uv run ../../ma-publication-quality/scripts/init_reporting_checklists.py \
  --root ../.. --include-moose

# Claim audit
uv run ../../ma-publication-quality/scripts/claim_audit.py \
  --abstract ../../07_manuscript/00_abstract.qmd \
  --results ../../07_manuscript/03_results.qmd \
  --out ../../09_qa/claim_audit.md

# Cross-reference check
uv run ../../ma-publication-quality/scripts/crossref_check.py \
  --manuscript-dir ../../07_manuscript \
  --figures-dir ../../06_analysis/figures \
  --out ../../09_qa/crossref_report.md

# Hash artifacts for reproducibility audit
uv run ../../ma-end-to-end/scripts/hash_artifacts.py \
  --root ../.. --out 09_qa/artifact_hashes.json
```

</details>

<details>
<summary><strong>Checkpoints</strong></summary>

```bash
# Create
uv run ../../ma-end-to-end/scripts/checkpoint.py --create --name pre-analysis

# List
uv run ../../ma-end-to-end/scripts/checkpoint.py --list

# Restore
uv run ../../ma-end-to-end/scripts/checkpoint.py --restore --name pre-analysis --yes
```

</details>

---

## Notes

- Always use `uv run` for Python scripts
- Keep all `round-XX` data (never overwrite)
- If PRISMA shows NA, check that `db_counts.csv` and `decisions.csv` exist
