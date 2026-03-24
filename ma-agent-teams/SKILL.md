---
name: ma-agent-teams
description: Orchestrate agent team for meta-analysis pipeline. Creates team, spawns teammates, manages task list and handoffs between pipeline stages.
---

# Agent Teams Orchestration

Coordinate multiple Claude Code instances as a team for parallel meta-analysis work.

## Prerequisites

- Claude Code v2.1.32+
- `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `.claude/settings.local.json`

## When to Use

- User says "create a team for [project]" or "start team mode"
- User says "parallel screen [project]" (dual-review only)
- Project has passed feasibility assessment (Stage 00 complete)
- Parallel work adds real value (≥2 independent stages ready)

## When NOT to Use

- Small projects (< 5 studies expected)
- Sequential-only work (single stage at a time)
- User prefers single-session mode (existing `ma-end-to-end` workflow)

---

## Team Composition

| Role | Teammate Name | Stages | File Ownership | Model |
|------|--------------|--------|----------------|-------|
| Protocol Architect | `protocol-architect` | 00-01 | `01_protocol/**` | sonnet |
| Search Specialist | `search-specialist` | 02 | `02_search/**` | sonnet |
| Screening Reviewer A | `screener-a` | 03 | `03_screening/**` (reviewer 1 columns) | sonnet |
| Screening Reviewer B | `screener-b` | 03 | `03_screening/**` (reviewer 2 columns) | sonnet |
| Fulltext Manager | `fulltext-manager` | 04 | `04_fulltext/**` | sonnet |
| Data Extractor | `data-extractor` | 05 | `05_extraction/**` | sonnet |
| Statistician | `statistician` | 06 | `06_analysis/**` | opus |
| Manuscript Writer | `manuscript-writer` | 07 | `07_manuscript/**` | opus |
| QA Auditor | `qa-auditor` | 08-09 | `08_reviews/**`, `09_qa/**` | sonnet |

**Note**: Not all roles are needed for every run. The lead selects roles based on which stages need work.

---

## Phased Spawning Strategy

### Phase 1: Sequential Foundation (Stages 00-02)

These stages have hard sequential dependencies — spawn one at a time.

1. Spawn `protocol-architect` → wait for completion
2. Validate: `01_protocol/pico.yaml` and `01_protocol/eligibility.md` exist
3. Spawn `search-specialist` → wait for completion
4. Validate: `02_search/round-01/dedupe.bib` exists with > 0 entries

### Phase 2: Parallel Screening (Stage 03)

Dual-review requires two independent reviewers working simultaneously.

1. Spawn `screener-a` AND `screener-b` simultaneously
2. **Critical**: screener-a and screener-b must NOT message each other until BOTH complete
3. Lead waits for both to finish
4. Lead computes kappa agreement:
   ```bash
   uv run ma-screening-quality/scripts/dual_review_agreement.py \
     --file projects/{{project-name}}/03_screening/round-01/decisions.csv \
     --col-a Reviewer1_Decision --col-b Reviewer2_Decision \
     --out projects/{{project-name}}/03_screening/round-01/agreement.md
   ```
5. **Quality gate**: kappa ≥ 0.60 required. If failed, lead resolves conflicts and re-runs.

### Phase 3: Sequential Processing (Stages 04-06)

These stages depend on prior outputs.

1. Spawn `fulltext-manager` → wait for completion
2. Validate: `04_fulltext/manifest.csv` and `04_fulltext/fulltext_decisions.csv` exist
3. Spawn `data-extractor` → wait for completion
4. Validate: `05_extraction/round-01/extraction.csv` exists
5. Spawn `statistician` → wait for completion
6. Validate: `06_analysis/figures/` and `06_analysis/tables/` exist

### Phase 4: Parallel Synthesis (Stages 07-09)

Manuscript and QA can work in parallel.

1. Spawn `manuscript-writer` AND `qa-auditor` simultaneously
2. `manuscript-writer` drafts sections from analysis outputs
3. `qa-auditor` runs GRADE assessment and PRISMA checklist
4. They message each other for revision cycles
5. Lead synthesizes final outputs

---

## Task List Template

Create these tasks at team start. The lead creates all tasks, teammates claim them.

```
1. "Develop protocol and PICO" [no dependencies]
   → owner: protocol-architect
   → done when: 01_protocol/pico.yaml, eligibility.md, search-plan.md exist

2. "Run literature search and deduplication" [depends: 1]
   → owner: search-specialist
   → done when: 02_search/round-01/dedupe.bib exists

3. "Screen titles/abstracts - Reviewer 1" [depends: 2]
   → owner: screener-a
   → done when: Reviewer1_Decision column populated in decisions.csv

4. "Screen titles/abstracts - Reviewer 2" [depends: 2]
   → owner: screener-b
   → done when: Reviewer2_Decision column populated in decisions.csv

5. "Reconcile screening and compute kappa" [depends: 3, 4]
   → owner: lead
   → done when: agreement.md shows kappa ≥ 0.60, included.bib created

6. "Retrieve full-text PDFs" [depends: 5]
   → owner: fulltext-manager
   → done when: 04_fulltext/manifest.csv exists

7. "Full-text eligibility screening" [depends: 6]
   → owner: fulltext-manager
   → done when: fulltext_decisions.csv and ft_agreement.md exist

8. "Extract study data and assess RoB" [depends: 7]
   → owner: data-extractor
   → done when: 05_extraction/round-01/extraction.csv exists

9. "Run meta-analysis in R" [depends: 8]
   → owner: statistician
   → done when: 06_analysis/figures/ and tables/ populated

10. "Draft manuscript" [depends: 9]
    → owner: manuscript-writer
    → done when: 07_manuscript/index.qmd exists

11. "GRADE assessment and peer review" [depends: 9]
    → owner: qa-auditor
    → done when: 08_reviews/grade_summary.csv exists

12. "Publication QA and PRISMA checklist" [depends: 10, 11]
    → owner: qa-auditor
    → done when: 09_qa/pipeline-checklist.md complete
```

---

## Handoff Protocol

Each stage produces specific artifacts that the next stage consumes.

| From → To | Handoff Artifacts | Validation |
|-----------|-------------------|------------|
| 01 → 02 | `pico.yaml`, `eligibility.md`, `search-plan.md` | pico.yaml exists, has population + intervention fields |
| 02 → 03 | `round-01/dedupe.bib`, `round-01/log.md` | dedupe.bib has > 0 entries |
| 03 → 04 | `round-01/included.bib`, `round-01/agreement.md` | kappa ≥ 0.60 in agreement.md |
| 04 → 05 | `fulltext_decisions.csv`, `ft_agreement.md` | FT kappa ≥ 0.60, ≥ 1 included study |
| 05 → 06 | `round-01/extraction.csv`, `data-dictionary.md` | extraction.csv has required columns |
| 06 → 07 | `figures/*.png`, `tables/*.csv` | All figures ≥ 300 DPI |
| 06 → 08 | All analysis outputs | validation.md passes |
| 07+08 → 09 | `index.qmd`, `grade_summary.csv` | Both exist |

---

## Spawn Instructions for Lead

To spawn a teammate:

1. Generate the spawn prompt:
   ```bash
   uv run tooling/python/team_spawn_helper.py --project {{project-name}} --role {{role-name}}
   ```
2. Use the output as the teammate's spawn prompt
3. Specify the model from the Team Composition table
4. Optionally require plan approval for complex stages (statistician, manuscript-writer)

Available roles: `protocol-architect`, `search-specialist`, `screening-reviewer`, `fulltext-manager`, `data-extractor`, `statistician`, `manuscript-writer`, `qa-auditor`

---

## Messaging Patterns

### Lead → Teammate
- **Task assignment**: "Your next task is ready: [task description]"
- **Handoff data**: "Stage N outputs are at: [paths]. Proceed with your stage."
- **Quality feedback**: "Validation failed: [details]. Please fix and resubmit."

### Teammate → Lead
- **Stage complete**: "Stage N complete. Outputs at: [paths]. Ready for validation."
- **Blocker found**: "Blocked: [description]. Need [resolution]."
- **Question**: "Clarification needed: [question about methodology/scope]"

### Teammate → Teammate (rare)
- `manuscript-writer` → `qa-auditor`: "Draft ready for review at 07_manuscript/index.qmd"
- `qa-auditor` → `manuscript-writer`: "Revision needed: [specific feedback]"

### Broadcast (use sparingly)
- Lead broadcasts only for: team-wide status updates, project scope changes

---

## Quality Gates (Lead Enforces)

| Gate | Threshold | Action if Failed |
|------|-----------|-----------------|
| Screening kappa | ≥ 0.60 | Lead resolves conflicts, does NOT spawn Stage 04 |
| FT screening kappa | ≥ 0.60 | Lead resolves conflicts, does NOT spawn Stage 05 |
| Extraction completeness | All included studies extracted | Lead identifies gaps, messages data-extractor |
| Figure DPI | ≥ 300 | Lead rejects, messages statistician to regenerate |
| PRISMA checklist | 27/27 items | Lead identifies gaps, assigns to relevant teammate |

---

## Team Templates

### Full Pipeline Team
All 8 roles. Use for complete meta-analysis from TOPIC.txt to manuscript.

### Parallel Screening Team
Only `screener-a` + `screener-b`. Use when Stage 02 is complete and dual-review is needed.
Lead handles kappa computation and conflict resolution.

### Analysis + Writing Team
Only `statistician` + `manuscript-writer` + `qa-auditor`. Use when Stage 05 is complete.
Three teammates work in parallel on analysis, writing, and review.

---

## Resuming After Interruption

If a team session is interrupted:

1. Check project status:
   ```bash
   uv run tooling/python/project_status.py --project {{project-name}} --verbose
   ```
2. Identify which stages are complete vs incomplete
3. Spawn new teammates for incomplete stages (old teammates cannot be resumed)
4. Provide checkpoint context in spawn prompts: "Stage N was partially complete. Files already created: [list]"

---

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Teammate crashes mid-stage | Lead detects via idle notification; spawns replacement with partial progress context |
| NMA vs pairwise routing | Lead handles Stage 03b gate; spawns statistician with appropriate SKILL.md reference |
| Teammate context exhaustion | Teammate messages lead before hitting limit; lead spawns fresh teammate with checkpoint |
| Large project (50+ studies) | Split extraction across 2-3 data-extractor teammates, each assigned study subsets |
| Dual-review independence | screener-a and screener-b MUST NOT message each other until both complete |
