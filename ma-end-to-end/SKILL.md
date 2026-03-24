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
   - Read from `projects/<project-name>/TOPIC.txt`
   - Use `/ma-topic-intake` skill
   - Write to `01_protocol/pico.yaml`, `01_protocol/eligibility.md`, `01_protocol/outcomes.md`, `01_protocol/search-plan.md`, `01_protocol/decision-log.md`
1b. **Preliminary** analysis type: ≥3 treatments → `nma_candidate`, 2 treatments → `pairwise`.
    - Record in `01_protocol/pico.yaml` (L22: analysis_type.preliminary field)
    - Record in `01_protocol/analysis-type-decision.md` (Stage 1 section)
2. Plan and run database searches, then save round-based `.bib` files in `02_search/`.
   - Use `/ma-search-bibliography` skill
   - Write to `02_search/round-01/queries.txt`, `02_search/round-01/results.bib`, `02_search/round-01/dedupe.bib`, `02_search/round-01/log.md`
3. Screen titles and abstracts, record decisions, and generate included `.bib` in `03_screening/`.
   - Use `/ma-screening-quality` skill
   - Write to `03_screening/round-01/decisions.csv`, `03_screening/round-01/included.bib`, `03_screening/round-01/agreement.md`
3b. **Analysis Type Confirmation Gate** (if `nma_candidate`):
    - Tally study designs, assess network connectivity and transitivity
    - If >30% single-arm → strongly consider downgrading to pairwise + pooled proportions
    - Confirm in `01_protocol/analysis-type-decision.md` (Stage 2 section)
    - Update `01_protocol/pico.yaml` (L23: analysis_type.confirmed field)
    - **Do NOT proceed to Stage 06 without confirmed analysis type**
4. Collect full texts and build a manifest in `04_fulltext/`.
   - Use `/ma-fulltext-management` skill
   - Write to `04_fulltext/manifest.csv`, `04_fulltext/*.pdf`
4b. **Full-text eligibility screening** (PRISMA 2020 item 16 — mandatory).
    - Use `/ma-fulltext-management` skill (Stage 04b section)
    - Run `uv run tooling/python/ai_screen.py --project <name> --stage fulltext --reviewer 1`
    - Run `uv run tooling/python/ai_screen.py --project <name> --stage fulltext --reviewer 2`
    - Compute kappa: `uv run ma-screening-quality/scripts/dual_review_agreement.py --file 04_fulltext/fulltext_decisions.csv --col-a FT_Reviewer1_Decision --col-b FT_Reviewer2_Decision --out 04_fulltext/ft_agreement.md`
    - Resolve conflicts, then only `FT_Final_Decision = include` rows proceed to Stage 05
    - Write to `04_fulltext/fulltext_decisions.csv`, `04_fulltext/ft_agreement.md`
5. Extract data into a normalized database in `05_extraction/`.
   - **Input**: Only studies with `FT_Final_Decision = include` from `04_fulltext/fulltext_decisions.csv`
   - Use `/ma-data-extraction` skill
   - Write to `05_extraction/extraction.sqlite`, `05_extraction/extraction.csv`, `05_extraction/data-dictionary.md`
6. Run meta-analysis in R with `renv`, generate figures and tables in `06_analysis/`.
   - Route by `analysis_type.confirmed`: `pairwise` | `nma` | `pooled_proportion` | `narrative`
   - Use `/ma-meta-analysis` skill for pairwise
   - Use `/ma-network-meta-analysis` skill for NMA
   - Write to `06_analysis/*.R`, `06_analysis/figures/*.png`, `06_analysis/tables/*.csv`, `06_analysis/renv.lock`
7. Draft and render Quarto manuscript in `07_manuscript/`.
   - Use `/ma-manuscript-quarto` skill
   - Write to `07_manuscript/*.qmd`, `07_manuscript/index.html`, `07_manuscript/index.pdf`
8. Perform Reviewer 1 and Reviewer 2 checks and save notes in `08_reviews/`.
   - Use `/ma-peer-review` skill
   - Write to `08_reviews/grade_summary.csv`, `08_reviews/rob2_assessment.csv`
9. Maintain cross-step validation logs in `09_qa/`.
   - Write to `09_qa/pipeline-checklist.md`
10. Add robustness checks: GRADE profiles, dual-review agreement stats, and PRISMA flow summary.
    - Use `scripts/run_robustness_checks.py`
11. Optionally run `scripts/run_robustness_checks.py` via `uv run` to generate all robustness artifacts at once.
    - Use `scripts/run_robustness_checks.py`
12. Apply publication-quality checks (PRISMA/MOOSE, HK, influence, SoF, claim audit, crossref).
    - Use `/ma-publication-quality` skill
    - Write to `09_qa/claim_audit.md`, `09_qa/crossref_report.md`, `09_qa/reporting_checklist_audit.md`
13. Validate stage transitions with `scripts/validate_stage_transition.py` and store reports in `09_qa/`.
    - Use `scripts/validate_stage_transition.py`
    - Write to `09_qa/stage_transition_report.md`
14. Create checkpoints before major steps with `scripts/checkpoint.py`.
    - Use `scripts/checkpoint.py`
    - Creates `.checkpoint/` snapshots

## Agent Teams (Parallel Mode)

When running with agent teams enabled (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`), the pipeline can leverage parallel teammates for independent stages.

### Parallelism Opportunities

| Phase | Stages | Parallelism | Teammates |
|-------|--------|-------------|-----------|
| Foundation | 00-02 | Sequential (hard dependencies) | protocol-architect → search-specialist |
| Screening | 03 | **Parallel** (dual independent review) | screener-a + screener-b simultaneously |
| Processing | 04-06 | Sequential (each depends on prior) | fulltext-manager → data-extractor → statistician |
| Synthesis | 07-09 | **Parallel** (independent outputs) | manuscript-writer + qa-auditor simultaneously |

### How to Start

1. User says "create a team for [project]" or "start team mode"
2. Lead reads `/ma-agent-teams` skill for the orchestration playbook
3. Lead creates shared task list with 12 tasks and dependencies
4. Lead spawns teammates in phased order (see SKILL.md for details)
5. Hooks enforce quality gates at stage transitions

### Quality Gates (Lead Enforces)

- **Stage 03→04**: Screening kappa ≥ 0.60 (lead computes after both reviewers finish)
- **Stage 04→05**: FT screening kappa ≥ 0.60
- **Stage 05→06**: Extraction completeness (all included studies extracted)
- **Stage 06→07**: All figures ≥ 300 DPI
- **Stage 09**: PRISMA 27/27 (or 32/32 for NMA), publication readiness ≥ 95%

### Generate Spawn Prompts

```bash
uv run tooling/python/team_spawn_helper.py --project <project-name> --role <role-name>
```

See `ma-agent-teams/SKILL.md` for complete orchestration details.

---

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
