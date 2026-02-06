---
name: ma-end-to-end
description: End-to-end AI-assisted meta-analysis pipeline orchestration from TOPIC.txt to final manuscript and reviewer responses. Use when the user provides a topic and wants the full meta-analysis workflow, tracking, and final paper.
---

# Ma End To End

## Overview
Coordinate the complete meta-analysis workflow, ensure every step is tracked, and produce a final manuscript with reviewer responses.

## Inputs
- `TOPIC.txt`
- Optional user constraints such as population, outcomes, time window, study types, or target journal.

## Outputs
- Standard project layout and all step artifacts described below.
- Final rendered manuscript in `07_manuscript/`.
- Reviewer notes in `08_reviews/`.

## Project Layout (Numbered)
Create a numbered top-level structure and keep every artifact in its step folder.

```
01_protocol/
02_search/
03_screening/
04_fulltext/
05_extraction/
06_analysis/
07_manuscript/
08_reviews/
09_qa/
tooling/python/   # uv project
```

## Environment Setup
1. Initialize Python tooling with uv inside `tooling/python/` using `uv init`.
2. Use `uv add` to manage dependencies for search and automation scripts.
3. Run Python scripts via `uv run` (do not call `python3` directly).
4. Use `uv tool` for any external CLI helpers that should be isolated.
5. Use R with `renv` inside `06_analysis/` for reproducible meta-analysis.

## Workflow
1. Read `TOPIC.txt` and produce protocol artifacts in `01_protocol/`.
2. Plan and run database searches, then save round-based `.bib` files in `02_search/`.
3. Screen titles and abstracts, record decisions, and generate included `.bib` in `03_screening/`.
4. Collect full texts and build a manifest in `04_fulltext/`.
5. Extract data into a normalized database in `05_extraction/`.
6. Run meta-analysis in R with `renv`, generate figures and tables in `06_analysis/`.
7. Draft and render Quarto manuscript in `07_manuscript/`.
8. Perform Reviewer 1 and Reviewer 2 checks and save notes in `08_reviews/`.
9. Maintain cross-step validation logs in `09_qa/`.
10. Add robustness checks: GRADE profiles, dual-review agreement stats, and PRISMA flow summary.
11. Optionally run `scripts/run_robustness_checks.py` via `uv run` to generate all robustness artifacts at once.
12. Apply publication-quality checks (PRISMA/MOOSE, HK, influence, SoF, claim audit, crossref).
13. Validate stage transitions with `scripts/validate_stage_transition.py` and store reports in `09_qa/`.
14. Create checkpoints before major steps with `scripts/checkpoint.py`.

## Resources
- `scripts/init_project.py` creates the numbered folder tree and a checklist.
- `scripts/run_robustness_checks.py` runs agreement stats, PRISMA flow, and GRADE summaries.
- `scripts/validate_pipeline.py` enforces checklist completion before final render.
- `scripts/final_qa_report.py` generates a final QA report and blocks on failures.
- `scripts/validate_stage_transition.py` validates continuity between stages.
- `scripts/checkpoint.py` creates and restores pipeline checkpoints.
- `scripts/hash_artifacts.py` computes SHA-256 hashes for reproducibility audit.
- `scripts/validate_module_registry.py` checks all scripts are documented across SKILL.md, CLAUDE.md, and GETTING_STARTED.md.

## Step References
Open the relevant skill for details at each stage:
- `ma-topic-intake/SKILL.md`
- `ma-search-bibliography/SKILL.md`
- `ma-screening-quality/SKILL.md`
- `ma-fulltext-management/SKILL.md`
- `ma-data-extraction/SKILL.md`
- `ma-meta-analysis/SKILL.md`
- `ma-manuscript-quarto/SKILL.md`
- `ma-peer-review/SKILL.md`
- `ma-publication-quality/SKILL.md`

## Validation
- Ensure each step writes its expected artifacts before moving to the next.
- Create and update `09_qa/pipeline-checklist.md` after every milestone.
