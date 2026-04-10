---
name: ma-manuscript-quarto
description: Draft and render a meta-analysis manuscript with Quarto using an IMRaD structure and embedded figures/tables. Use when preparing the final paper from analysis outputs.
---

# Ma Manuscript Quarto

## Overview

Create a Quarto manuscript with standard IMRaD sections and render to PDF and HTML.

## Inputs

- `06_analysis/figures/`
- `06_analysis/tables/`
- `02_search/round-01/dedupe.bib` or final bibliography

## Outputs

- `07_manuscript/manuscript_outline.md` (Phase 1 — outline with checklist and discussion ideas)
- `07_manuscript/00_abstract.qmd`
- `07_manuscript/01_introduction.qmd`
- `07_manuscript/02_methods.qmd`
- `07_manuscript/03_results.qmd`
- `07_manuscript/04_discussion.qmd`
- `07_manuscript/tables.qmd` (standalone PNG table images)
- `07_manuscript/figures_legends.qmd` (figure legends with embedded PNGs)
- `07_manuscript/index.qmd`
- `07_manuscript/Makefile` (sync + render automation)
- `07_manuscript/references.bib`
- `07_manuscript/index.html` (rendered HTML)
- `07_manuscript/index.pdf` (rendered PDF via Typst)
- `07_manuscript/index.docx` (rendered Word with PNG tables)
- `07_manuscript/figures/` (synced from `06_analysis/figures/`)
- `07_manuscript/tables/` (synced PNG + CSV from `06_analysis/tables/`)
- `07_manuscript/prisma_flow.md`
- `07_manuscript/prisma_flow.svg`
- `07_manuscript/evidence_map.md`
- `07_manuscript/result_claims.csv`
- `07_manuscript/result_paragraphs.md`
- `07_manuscript/result_paragraphs.qmd`
- `07_manuscript/result_summary_table.md` (auto-inserted into Results)
- `07_manuscript/traceability_table.md`
- `07_manuscript/study_characteristics.md`
- `07_manuscript/study_characteristics.csv`
- `07_manuscript/submission_checklist.md`
- `07_manuscript/03_results.qmd` (assembled)
- `09_qa/results_consistency_report.md`

## Workflow

**The workflow has two phases: Outline first, then Write. Never skip Phase 1.**

### Phase 1: Outline & Checklist (MANDATORY before any writing)

Before writing any prose, build a complete outline that serves as the blueprint.
The outline template is at `assets/quarto/manuscript_outline.md` — it contains 10 sections
that must ALL be filled in with project-specific data.

#### Step 1.1: Initialize project structure

1. Initialize a Quarto project in `07_manuscript/`.
   - Create `07_manuscript/_quarto.yml`
   - Create `07_manuscript/index.qmd`
2. Copy Quarto templates from `assets/quarto/` and adapt to the project.
   - Copy `assets/quarto/00_abstract.qmd` → `07_manuscript/00_abstract.qmd`
   - Copy `assets/quarto/01_introduction.qmd` → `07_manuscript/01_introduction.qmd`
   - Copy templates 02-04 similarly
3. Copy `assets/quarto/manuscript_outline.md` to `07_manuscript/manuscript_outline.md`.
   - Copy `assets/quarto/manuscript_outline.md` → `07_manuscript/manuscript_outline.md`

#### Step 1.2: Gather evidence (read BEFORE filling outline)

4. Build a manuscript evidence map with `scripts/build_evidence_map.py` — review all analysis outputs.
   - Use `scripts/build_evidence_map.py`
   - Write to `07_manuscript/evidence_map.md`
   - **If the script fails**: manually read `06_analysis/` R outputs, CSVs, and figure files to build the map.
   - **If `06_analysis/` is incomplete**: STOP. Return to `/ma-meta-analysis` to complete analysis first.
5. Initialize `result_claims.csv` with `scripts/init_result_claims.py` — map every result to its source.
   - Use `scripts/init_result_claims.py`
   - Write to `07_manuscript/result_claims.csv` (columns: claim_id, outcome, effect_measure, estimate, ci_lower, ci_upper, p_value, i2, figure_ref, table_ref, r_script, citation_keys)
   - **If the script fails**: manually create the CSV with columns: `claim_id, outcome, effect_measure, estimate, ci_lower, ci_upper, p_value, i2, figure_ref, table_ref, r_script, citation_keys`.
6. Read ALL of the following before filling the outline:
   - `06_analysis/` — every R script output, CSV table, figure PNG
   - `05_extraction/extraction.csv` — for study characteristics
   - `01_protocol/pico.yaml` (L1-28: all fields) — for PICO details
   - `02_search/` — search dates, database counts
   - `03_screening/round-01/agreement.md` — screening decisions, Cohen's kappa
   - `08_reviews/grade_summary.csv` — GRADE summary if available
   - Prior reviews (search PubMed for existing systematic reviews on the topic)

#### Step 1.3: Fill in the outline (the core work of Phase 1)

7. **Fill in every section of `manuscript_outline.md`**:

   **Section 1 — Project Info**: Topic, journal, word limits, PROSPERO ID.

   **Section 2 — Key Messages**: Define 3-5 take-home messages. These drive the entire manuscript.
   Test: if a paragraph doesn't serve at least one key message, it shouldn't be in the paper.

   **Section 3 — Narrative Arc**: Define the story in 6 sentences (hook → gap → approach → finding → significance → bottom line).
   Test: read the 6 sentences aloud — they should tell a coherent story.

   **Section 4 — Section Outlines**:
   - Abstract: fill the data table with exact numbers from R outputs.
   - Introduction: plan paragraph-by-paragraph with specific citations.
   - Methods: fill PICO, databases, search dates, statistical details.
   - Results: fill one outcome block per quantitative result with claim_id, estimate, CI, p-value, I², figure/table refs, R script source.
   - Discussion: fill ALL subsections with minimum point counts:
     - Principal findings: >= 3 points
     - Topic-specific interpretation: >= 1 subsection with argument + evidence + implication
     - Comparison with prior work: >= 2 named prior studies/reviews
     - Limitations: >= 2 study-level + 2 review-level + 1 outcome-level + 1 statistical
     - Implications: >= 3 clinical + 3 future research (with specific study designs)
     - Conclusions: draft the 2-3 sentence conclusion

   **Section 5 — Tables & Figures Plan**: List every table and figure with source file, panels, and draft legends.

   **Section 6 — References Plan**: List ALL BibTeX keys that will appear in the manuscript.

   **Section 7 — Word Count Targets**: Set per-section targets matching the target journal.

   **Section 8 — Supplementary Materials**: Plan search strategies, PRISMA checklist, supplementary tables/figures.

   **Section 9 — Pre-Writing Readiness Gate**: Check ALL hard requirements (data, figures, tables, references, outline completeness).

#### Step 1.4: Validate and approve

8. **Self-validate the outline**:
   - Search for `{{` in the file — must return 0 hits (no unfilled placeholders).
   - Verify Discussion has >= 3 points in each subsection.
   - Verify every outcome block in Results has claim_id, estimate, CI, p-value, figure ref.
   - Verify Section 9 (Readiness Gate) is fully checked.
9. **Present the outline to the user for review**.
   - Summarize: key messages, number of outcomes, number of tables/figures, word count targets.
   - Ask: "Is this outline approved? Any changes needed?"
10. **Do NOT proceed to Phase 2 until the user explicitly approves.**

---

### Phase 2: Write from Outline

Once the outline is approved, write each section following it exactly.

**Writing style**: All prose MUST follow `references/academic-writing-style.md`. Key rules:
- **AMA style** (default) — superscript numbered citations, `american-medical-association.csl`, serial comma, generic drug names
- **No contractions** (do not, cannot — never don't, can't)
- **No vague language** (determine, not "figure out"; possibly, not "maybe")
- **No imperative mood** ("The analysis was performed" — not "Run the analysis")
- **No sentence fragments** in prose ("No data were available" — not "No data.")
- **Passive voice** for Methods/Results; **active voice** for interpretation
- **Formal transitions** (However, Therefore — not But, So)
- **Precise terminology** (adverse events, not side effects; mortality, not death)
- **Complete statistics** (every claim needs estimate + 95% CI + p-value)
- **AMA numbers** — numerals with units, spell out at sentence start, "%" not "percent"
- **AMA abbreviations** — define at first use in abstract AND body; no abbreviations in title
- **No AI-flavored vocabulary** — cross-check with `human-write` skill after writing

**Writing order** (this order is intentional — write data-driven sections first):
1. Methods (most formulaic, establishes scope)
2. Results (data-driven, references Methods)
3. Discussion (interprets Results)
4. Introduction (frames the story, written after you know the results)
5. Abstract (summary of everything, written last)

#### Step 2.1: Generate structural components

11. Generate the PRISMA flow summary with `scripts/prisma_flow.py` via `uv run`, optionally writing an SVG. Use `--strict` for final renders.
    - **If the script fails**: manually create PRISMA flow from screening/fulltext data.
12. Insert the search report and audit hashes into Methods with `scripts/insert_search_report.py`.
    - **If the script fails**: manually copy search report content into the Methods information sources section.
13. Generate Results paragraph stubs with `scripts/build_result_paragraphs.py`.
    - **If the script fails**: manually write paragraph stubs from `result_claims.csv`.
14. Build study characteristics table with `scripts/build_study_characteristics.py`.
    - **If the script fails**: manually extract from `extraction.csv`.
15. Insert the traceability table into Methods with `scripts/insert_traceability_table.py`.
    - **If the script fails**: manually create: protocol registered → N databases searched → N records → N screened → N included.

#### Step 2.2: Write sections (follow outline exactly)

16. **Write Methods** (`02_methods.qmd`):
    - Follow outline Section 4.3 point by point.
    - Include all statistical analysis sub-items.
    - Reference traceability table and PRISMA flow.
    - **Checkpoint**: verify every Methods paragraph maps to an outline checkbox.

17. **Write Results** (`03_results.qmd`):
    - Follow outline Section 4.4 in the specified writing order.
    - For each outcome: copy claim_id, estimate, CI, p-value, I² from the outline.
    - Every quantitative claim MUST include: effect estimate + 95% CI + p-value.
    - Reference the specific figure and table for each outcome.
    - Use `[@key]` citations from the outline's BibTeX key lists.
    - **Checkpoint**: run `scripts/results_consistency_report.py` — must have 0 missing items.

18. **Write Discussion** (`04_discussion.qmd`):
    - Follow outline Section 4.5 subsection by subsection.
    - Write ONLY the points listed in the outline. Do NOT improvise new arguments.
    - Each subsection must have the minimum word count specified.
    - **Checkpoint**: verify every Discussion claim traces to a Result.

19. **Write Introduction** (`01_introduction.qmd`):
    - Follow outline Section 4.2 paragraph by paragraph.
    - Ensure objectives match Methods and Results reporting order.
    - **Checkpoint**: verify objectives list matches Results section structure.

20. **Write Abstract** (`00_abstract.qmd`):
    - Follow outline Section 4.1 and the data table.
    - Every number MUST match the Results section exactly.
    - **Checkpoint**: cross-check every number in Abstract against Results.

#### Step 2.3: Assemble, validate, render

21. Assemble Results into `03_results.qmd` with `scripts/assemble_results.py` (also inserts `result_summary_table.md`).
22. Populate the bibliography and ensure all `[@key]` citations in all QMD files have matching entries in `references.bib`.
23. **Verify DOI existence** with `scripts/verify_doi.py`:
    ```bash
    uv run ma-manuscript-quarto/scripts/verify_doi.py \
      --bib projects/<project>/07_manuscript/references.bib \
      --out projects/<project>/09_qa/doi_verification_report.md \
      --email "your@email.com"
    ```
    - Must exit with code 0 (>= 90% DOI coverage, 0 invalid DOIs).
    - For missing DOIs, review candidates and patch: add `--patch --min-confidence 85`.
    - **If exit code 1**: add missing DOIs manually or via `--patch`.
    - **If exit code 2**: fix invalid DOIs before proceeding.
24. Generate a results consistency report with `scripts/results_consistency_report.py`.
    - **If any missing items**: fix before proceeding.
24. Initialize the submission checklist with `scripts/init_submission_checklist.py`.
25. Run `scripts/lint_qmd.py --dir 07_manuscript/` — must pass with exit code 0 (no errors).
    - **If errors**: fix with `--fix` flag, then re-run to confirm.
26. Sync, validate, and render with the all-in-one build script:
    ```bash
    bash ma-manuscript-quarto/scripts/build_manuscript.sh --project <name> --all
    ```
    Alternatively, use Makefile: `make all` from `07_manuscript/`.
    - **If render fails**: check Quarto error output, fix broken references/includes, re-render.

#### Step 2.4: Post-writing validation

28. **Run cross-section consistency checks** (outline Section 10):
    - Abstract numbers match Results numbers exactly.
    - Introduction objectives match Methods match Results reporting order.
    - Every figure/table referenced in text exists.
    - Every Discussion claim traces to a Result.
    - Conclusions contain no new findings.
    - Word counts within journal targets.
    - All citation keys resolve.
29. **Update the outline**: mark all checklist items as done, fill in actual word counts in Section 7.
30. **Report to user**: section word counts, any issues found, rendered output files.

## Build & Sync Workflow

Two build options: **`build_manuscript.sh`** (recommended, all-in-one) or **Makefile** (render only).

### `build_manuscript.sh` (Recommended)

All-in-one validation + sync + lint + render script. Runs standalone without AI — output goes to stdout.

```bash
# From repo root:
bash ma-manuscript-quarto/scripts/build_manuscript.sh --project <name>           # Validate only (fast)
bash ma-manuscript-quarto/scripts/build_manuscript.sh --project <name> --fix      # Auto-fix lint
bash ma-manuscript-quarto/scripts/build_manuscript.sh --project <name> --render   # Validate + render
bash ma-manuscript-quarto/scripts/build_manuscript.sh --project <name> --all      # Fix + render
bash ma-manuscript-quarto/scripts/build_manuscript.sh --project <name> --render --formats docx  # DOCX only
```

**7-step validation pipeline** (all results to stdout):

| Step | Check | Details |
|------|-------|---------|
| 1 | Sync | Copy figures/tables from `06_analysis/` to `07_manuscript/` |
| 2 | Citations | Verify all `[@key]` in QMD match `references.bib`; report unused bib entries |
| 3 | Word counts | Per-section word count vs journal targets |
| 4 | QMD lint | Run `lint_qmd.py` (15 rules), optional `--fix` |
| 5 | DOI coverage | Check % of bib entries with DOI fields (target: >=90%) |
| 6 | File check | Verify all figures/tables referenced in QMD exist on disk |
| 7 | Render | Quarto render to DOCX, HTML, PDF (each format independent) |

**Exit codes**: 0 = all passed, N = number of errors found.

**No `--project`?** Lists all available projects:
```
$ bash ma-manuscript-quarto/scripts/build_manuscript.sh
Available projects:
  --project hrd-parp-inhibitors
  --project ici-breast-cancer
```

### Why Sync?

Analysis scripts in `06_analysis/` produce figures (PNG) and tables (PNG + CSV + HTML + DOCX via `gt`/`flextable`). The manuscript in `07_manuscript/` references local copies so Quarto can embed them. The `sync` step copies the latest outputs before every render, ensuring the manuscript always reflects current analysis.

### Makefile (Alternative)

For projects that prefer `make`, create a Makefile in `07_manuscript/`:

```makefile
.PHONY: all html pdf docx clean sync

ANALYSIS_DIR := ../06_analysis

all: sync html pdf docx

sync:
	@mkdir -p figures tables
	@cp -f $(ANALYSIS_DIR)/figures/*.png figures/
	@cp -f $(ANALYSIS_DIR)/tables/*.png tables/
	@cp -f $(ANALYSIS_DIR)/tables/*.csv tables/

html: sync
	quarto render index.qmd --to html

pdf: sync
	quarto render index.qmd --to typst

docx: sync
	quarto render index.qmd --to docx

clean:
	command rip -f index.html index.pdf index.docx index_files/
```

### Makefile Usage

```bash
cd projects/<project>/07_manuscript

make sync     # Copy latest figures + tables from 06_analysis
make docx     # Sync + render Word (tables as PNG images)
make html     # Sync + render self-contained HTML
make pdf      # Sync + render PDF via Typst
make          # Sync + render all formats
```

### What Gets Synced

| Source (`06_analysis/`) | Destination (`07_manuscript/`) | Used By               |
| ----------------------- | ------------------------------ | --------------------- |
| `figures/*.png`         | `figures/`                     | `figures_legends.qmd` |
| `tables/*.png`          | `tables/`                      | `tables.qmd`          |
| `tables/*.csv`          | `tables/`                      | Reference data        |

### Sync Direction

**One-way**: `06_analysis → 07_manuscript`. Never edit PNGs in `07_manuscript/` directly; regenerate from R scripts in `06_analysis/` and re-run `make sync`.

## Tables as Standalone PNG Images

Tables are generated in R (via `gt` + `flextable` in `07_export_tables.R`) and exported as PNG, HTML, and DOCX. The manuscript embeds the **PNG images** directly.

### Why PNG Tables?

1. **Consistent rendering** across HTML, PDF, and DOCX outputs
2. **Publication-quality formatting** via `gt` package (colors, bold, footnotes)
3. **No Quarto table rendering issues** (complex tables with merged cells, conditional formatting)
4. **Single source of truth**: R script generates all formats; manuscript just references PNGs

### Table Export Script (`06_analysis/07_export_tables.R`)

The R script exports each table in 3 formats:

```r
library(gt)
library(flextable)

export_table <- function(gt_tbl, ft_tbl, basename, vwidth = 800) {
  gt_tbl %>% gtsave(paste0("tables/", basename, ".html"))
  gt_tbl %>% gtsave(paste0("tables/", basename, ".png"), vwidth = vwidth)
  save_as_docx(ft_tbl, path = paste0("tables/", basename, ".docx"))
}
```

### `tables.qmd` Structure

```markdown
# Tables

## Table 1. Trial Characteristics {#tbl-characteristics}

![](tables/table1_characteristics.png){width=100%}

---

## Table 2. Risk of Bias {#tbl-rob2}

![](tables/table2_rob2.png){width=100%}
```

Each table is a heading + standalone PNG image. The `{width=100%}` ensures proper scaling across formats.

### Output Formats

| Format | Table Rendering | Notes                                       |
| ------ | --------------- | ------------------------------------------- |
| HTML   | Embedded PNG    | Self-contained, sharp on retina             |
| PDF    | Embedded PNG    | Via Typst, respects width                   |
| DOCX   | Embedded PNG    | Word embeds image inline; no editable cells |

## Output Formats

The `index.qmd` YAML configures three output formats:

```yaml
format:
  html:
    toc: true
    toc-depth: 3
    number-sections: true
    embed-resources: true
  docx:
    toc: true
    number-sections: true
  typst:
    toc: true
    number-sections: true
    columns: 1
    margin:
      x: 1in
      y: 1in
    papersize: us-letter
    mainfont: "New Computer Modern"
    fontsize: 11pt
```

- **HTML**: Self-contained (`embed-resources: true`), good for review and sharing
- **DOCX**: Word format for journal submission and co-author editing; tables render as PNG images
- **PDF**: Via Typst engine (faster than LaTeX, good typography)

## Discussion Guidance

**Discussion is the hardest section to write well. The outline (Phase 1) does the thinking; Phase 2 does the writing.**

### Why outline Discussion first?

Without pre-planned ideas, agents tend to produce generic Discussions that:
- Repeat Results as prose (adds no value)
- Use vague limitations ("this study has limitations")
- Omit topic-specific insights that make the paper publishable
- Miss comparisons with prior work

The outline's Discussion section forces the agent to brainstorm SPECIFIC ideas before writing.

### What makes a good Discussion?

**Structure** (from the outline template):
1. **Principal findings** (~200-300 words): Clinical significance, not statistics. "NNT=7 means 1 in 7 patients benefits" > "RR was 1.26".
2. **Topic-specific interpretation** (~200-400 words): This is YOUR unique contribution. What insight does pooling these studies reveal that individual trials couldn't show? Examples:
   - Surrogate endpoint validation (pCR predicts OS)
   - Biomarker reinterpretation (PD-L1 is prognostic, not predictive)
   - Dose-response patterns across studies
   - Subgroup findings that resolve clinical controversies
3. **Comparison with prior work** (~200-400 words): NAME specific reviews. State their finding, your finding, and explain WHY they agree or differ. "Smith et al. (2023) found X; we found Y, likely because our analysis includes Z."
4. **Limitations** (~200-400 words): Organize by level (study / review / outcome / statistical). Be HONEST — reviewers will find these anyway. Better to address them proactively.
5. **Implications and future research** (~200-300 words): Clinical recommendations must be supported by GRADE certainty. Future research must be SPECIFIC: "A Phase III RCT comparing X vs Y in Z population with W outcome and >= N months follow-up."
6. **Conclusions** (~50-100 words): Main finding + certainty + clinical bottom line. Must reinforce key messages.

### Minimum requirements for Discussion outline

| Subsection | Minimum points | Minimum named references |
|------------|---------------|-------------------------|
| Principal findings | 3 | 0 (your own results) |
| Topic-specific interpretation | 1 subsection (3 points) | 2 |
| Comparison with prior work | 2 named reviews/studies | 2 |
| Limitations (study-level) | 2 | 0 |
| Limitations (review-level) | 2 | 0 |
| Limitations (outcome-level) | 1 | 0 |
| Limitations (statistical) | 1 | 0 |
| Clinical implications | 3 | 1 (guideline) |
| Future research directions | 3 (with study design) | 0 |

### Phase 2 writing rules

When writing Discussion from the outline:
- Follow the planned points IN ORDER. Do not rearrange.
- Do NOT add new arguments that were not in the approved outline.
- If you discover a missing argument while writing, flag it to the user rather than adding it silently.
- Every factual claim must have a citation (`[@key]`).
- Avoid the phrase "further research is needed" without specifying WHAT research.

## Quarto Syntax Reference

See `references/quarto-syntax-guide.md` for the complete reference covering:

- `_quarto.yml` project configuration (`type: manuscript`)
- Cross-references: `{#fig-label}`, `{#tbl-label}`, `{#sec-label}`, `{#eq-label}`
- Figures with alt-text, sizing, subfigures (`layout-ncol`)
- Tables (pipe and grid), subtables, caption placement
- Citations: `[@key]` parenthetical, `@key` in-text, `[-@key]` suppress author
- Includes: `{{< include file.qmd >}}`, page breaks: `{{< pagebreak >}}`
- PDF options, journal extensions, callouts

**Key rules**: labels must be lowercase, use hyphens (not underscores), and always include the prefix.

## QMD Linter & Formatter

Run `scripts/lint_qmd.py` to validate manuscript files against Quarto best practices:

```bash
# Report only
uv run ma-manuscript-quarto/scripts/lint_qmd.py \
  --dir projects/<project>/07_manuscript/

# Auto-fix + report
uv run ma-manuscript-quarto/scripts/lint_qmd.py \
  --dir projects/<project>/07_manuscript/ \
  --fix --out-md /tmp/lint_report.md
```

**Checks** (15 rules, L001-L015):

| Severity | Rules                                                                                                                                           |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| error    | L001 underscore in labels, L002 uppercase labels, L011 missing YAML, L012 missing bib, L013 missing include                                     |
| warning  | L003 figure no label, L004 table no label, L005 footnote numbers, L006 \\newpage, L007 bare URL, L010 skipped heading, L014 missing figure file |
| style    | L008 trailing whitespace, L009 no blank before heading, L015 double blank lines                                                                 |

**Auto-fixable**: L006, L008, L009, L015. Exit codes: 0 clean, 1 warnings, 2 errors.

## Resources

- `assets/quarto/manuscript_outline.md` — **Outline & checklist template** (Phase 1). Copy to `07_manuscript/` and fill in before writing.
- `assets/quarto/` provides an IMRaD Quarto scaffold.
- `references/academic-writing-style.md` — **Academic writing style hub** (summary + validation checklist). Required reading before Phase 2.
  - `references/style-no-ai-casual.md` — Rule 1 detail: contractions, vague language, imperative mood, fragments
  - `references/style-professional-register.md` — Rule 2 detail: sentence structure, passive/active voice, transitions, terminology
  - `references/style-ama-guide.md` — Rule 3 detail: AMA citations, bibliography, numbers, abbreviations, drug names, P values
- `references/quarto-syntax-guide.md` — Quarto syntax reference for meta-analysis manuscripts.
- `scripts/verify_doi.py` verifies DOI existence via Crossref API and finds missing DOIs by title search. Outputs markdown report + optional CSV. Supports auto-patching.
- `scripts/lint_qmd.py` validates and auto-fixes QMD/MD files against Quarto best practices.
- `scripts/prisma_flow.py` generates a PRISMA flow diagram summary and optional SVG.
- `scripts/insert_search_report.py` injects search report content into Methods.
- `scripts/build_evidence_map.py` creates a checklist of outputs to base writing on.
- `scripts/init_result_claims.py` seeds a results-to-evidence table for drafting.
- `scripts/build_result_paragraphs.py` creates paragraph stubs and a summary table for Results writing.
- `scripts/build_study_characteristics.py` generates the study characteristics table from extraction.
- `scripts/insert_traceability_table.py` inserts a protocol→search→screening→inclusion table into Methods.
- The traceability narrative is auto-inserted into `02_methods.qmd` near Study Selection.
- `scripts/assemble_results.py` injects result paragraphs into `03_results.qmd`.
- `scripts/results_consistency_report.py` checks claim/output/citation consistency.
- `scripts/init_submission_checklist.py` seeds a journal submission checklist.
- `scripts/render_manuscript.py` validates checklists before rendering.
- `scripts/build_manuscript.sh` **all-in-one build script** — sync, validate citations, word counts, lint, DOI check, render. Runs standalone without AI. Usage: `bash ma-manuscript-quarto/scripts/build_manuscript.sh --project <name> [--fix] [--render] [--all]`.

## Validation

### Phase 1 gate (before writing)

| Check | How to verify | Pass criteria | Fail action |
|-------|---------------|---------------|-------------|
| No placeholders | `grep -c '{{' manuscript_outline.md` | 0 hits | Fill remaining placeholders |
| Key messages defined | Section 2 of outline | 3-5 messages, no blanks | Brainstorm with user |
| Narrative arc coherent | Section 3 of outline | All 6 fields filled | Revise story structure |
| Discussion fully planned | Section 4.5 of outline | All minimums met (see table in Discussion Guidance) | Add more points |
| Evidence map reviewed | `evidence_map.md` exists | All outputs listed | Run `build_evidence_map.py` |
| Result claims mapped | `result_claims.csv` exists | All results have claim_id | Run `init_result_claims.py` |
| Figures exist | `ls 06_analysis/figures/*.png` | All outline figures present | Return to analysis stage |
| Tables exist | `ls 06_analysis/tables/*.png` | All outline tables present | Run R export script |
| References ready | `references.bib` exists | Keys match outline Section 6 | Build BibTeX file |
| User approved | Asked user | Explicit "yes" | Address feedback |

**Hard stop**: Do NOT proceed to Phase 2 if any check fails.

### Phase 2 checkpoints (during writing)

| After writing... | Run checkpoint | Pass criteria |
|------------------|----------------|---------------|
| Methods | Outline Section 4.3 all checked | Every Methods item covered |
| Results | `scripts/results_consistency_report.py` | 0 missing items |
| Discussion | Verify each claim traces to Results | No orphan claims |
| Introduction | Objectives match Results structure | Same number and order |
| Abstract | Cross-check numbers vs Results | Exact match |
| **Every section** | Academic writing style check (`references/academic-writing-style.md`) | No contractions, no fragments, no vague language, no imperative mood |
| **Every section** | `human-write` AI vocabulary scan | Score <= 4 (light AI flavor) |

### Final validation (after all writing)

- Run `scripts/lint_qmd.py --dir 07_manuscript/` — must pass with exit code 0 (no errors).
- Verify academic writing style compliance (`references/academic-writing-style.md`):
  - 0 contractions in prose (search `n't`, `'re`, `'ve`, `'ll`; exclude Crohn's, Hodgkin's).
  - 0 sentence fragments in prose paragraphs.
  - 0 imperative-mood sentences in prose (parenthetical "see Table S1" is acceptable).
  - 0 vague terms (maybe, figure out, a lot, stuff, things, basically).
  - Formal transitions varied (no single transition > 2 uses per subsection).
- Run `human-write` AI vocabulary scan — score must be <= 4.
- Ensure all figures are 300 DPI and tables are reproducible.
- Cross-check that every result in the text appears in the analysis outputs.
- Ensure each results paragraph maps to `07_manuscript/result_claims.csv`.
- Verify `07_manuscript/traceability_table.md` is inserted into `02_methods.qmd`.
- Ensure each claim includes effect estimate, confidence interval, and p-value.
- Ensure `03_results.qmd` contains all claim IDs and their figure/table refs.
- Ensure `09_qa/results_consistency_report.md` has no missing items.
- Ensure each claim includes `citation_keys` and the citations appear in Results.
  Note: `citation_keys` should be comma-separated BibTeX keys present in `07_manuscript/references.bib`.
- Note: set `RESULTS_MIN_WORDS` to control minimum words per claim paragraph (default 25).
- Ensure the study characteristics table is inserted into `03_results.qmd`.
- Ensure `submission_checklist.md` is tailored to the target journal.
- Run cross-section consistency checks (outline Section 10):
  - Abstract numbers match Results exactly.
  - Introduction objectives match Results reporting order.
  - Every figure/table referenced in text exists in the manuscript.
  - Conclusions contain no new findings not in Results.
  - Word counts within journal targets.
  - All `[@key]` citations resolve in `references.bib`.

## Stage Exit: Stamp the artifact

Record provenance for the rendered manuscript. See
[artifact-stamping.md](../ma-end-to-end/references/artifact-stamping.md).

```bash
uv run tooling/python/session_log.py --project <project-name> append \
  --stage 07_manuscript \
  --artifact 07_manuscript/index.qmd \
  --generator ai \
  --deviation "draft mode"  # omit in strict mode
```

## Pipeline Navigation

| Step | Skill               | Stage                       |
| ---- | ------------------- | --------------------------- |
| Prev | `/ma-meta-analysis` | 06 Statistical Analysis     |
| Next | `/ma-peer-review`   | 08 Peer Review & GRADE      |
| All  | `/ma-end-to-end`    | Full pipeline orchestration |
