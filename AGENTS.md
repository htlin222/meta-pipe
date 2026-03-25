# Agent Instructions

AI-assisted meta-analysis pipeline. This file is auto-loaded by Claude Code.

---

## Quick Start

**First time setup?** → Run `bash setup.sh` then `bash verify_environment.sh` (see [ENVIRONMENT_QUICK_START.md](ENVIRONMENT_QUICK_START.md))
**New project?** → Say "brainstorm" or "help me find a topic" (see [ma-topic-intake](ma-topic-intake/SKILL.md))
**Have TOPIC.txt?** → Say "start" or "continue" (see [ma-end-to-end](ma-end-to-end/SKILL.md))
**At Stage 06?** → Say "complete manuscript" (see [ma-manuscript-quarto](ma-manuscript-quarto/SKILL.md))
**Want to see an example?** → Check `projects/ici-breast-cancer/` (99% complete meta-analysis)
**Want to validate the workflow?** → See [metadat Validation](ma-end-to-end/references/metadat-validation.md)

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
├── ma-*/                    # Framework code modules (each has SKILL.md)
├── docs/archive/            # Archived documentation
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

## Pipeline Stages & Skills

**Each stage has a dedicated skill with commands and workflow guidance**

| Stage | Skill                       | Key Tasks                           | Invoke                           |
| ----- | --------------------------- | ----------------------------------- | -------------------------------- |
| 00    | `/ma-topic-intake`          | Brainstorming, feasibility checks   | `/brainstorm` or use skill       |
| 01-02 | `/ma-search-bibliography`   | PROSPERO, search, dedupe            | Use skill for detailed commands  |
| 03    | `/ma-screening-quality`     | Dual-review screening, kappa        | Use skill for detailed commands  |
| 03b   | `/ma-screening-quality`     | **Analysis type confirmation gate** | Confirm NMA vs pairwise (Step 8) |
| 04    | `/ma-fulltext-management`   | PDF retrieval, Unpaywall            | Use skill for detailed commands  |
| 04b   | `/ma-fulltext-management`   | **Full-text eligibility screening** | `ai_screen.py --stage fulltext`  |
| 05    | `/ma-data-extraction`       | Data extraction, RoB assessment     | Use skill for detailed commands  |
| 06a   | `/ma-meta-analysis`         | Pairwise MA (R scripts 01-12)       | Use skill for detailed commands  |
| 06b   | `/ma-network-meta-analysis` | NMA (R scripts nma_01-10)           | Use skill for detailed commands  |
| 07    | `/ma-manuscript-quarto`     | Manuscript assembly, rendering      | Use skill for detailed commands  |
| 08    | `/ma-peer-review`           | GRADE assessment, SoF table         | Use skill for detailed commands  |
| 09    | `/ma-publication-quality`   | QA, overclaim audit, readiness      | Use skill for detailed commands  |
| 10    | `/ma-submission-prep`       | PROSPERO, final checks, submit      | Use skill for detailed commands  |

**Orchestration**: `/ma-end-to-end` - Complete workflow management | `/ma-agent-teams` - Agent team coordination

**Share your work**: `/post-to-discussion` - Post your completed project to [GitHub Discussions](https://github.com/htlin222/meta-pipe/discussions) with figures and results

**Note**: Skills are invoked using the `Skill` tool. Each skill contains both workflow guidance and complete command references.

---

## Agent Teams (Experimental)

Coordinate multiple Claude Code instances for parallel meta-analysis pipeline work.

### Quick Commands

- "Create a team for project X" → Full pipeline team (all stages)
- "Parallel screen project X" → Dual-review screening team only
- "Analysis team for project X" → Statistician + manuscript writer + QA auditor

### How It Works

- Lead reads `/ma-agent-teams` skill for orchestration playbook
- Teammates spawned with role-specific prompts from `ma-agent-teams/prompts/`
- Shared task list tracks dependencies; hooks enforce quality gates
- Each teammate owns specific directories (no cross-teammate file writes)

### Generate Spawn Prompts

```bash
uv run tooling/python/team_spawn_helper.py --project <project-name> --role <role> [--list]
```

### Prerequisites

- Claude Code v2.1.32+
- Enabled via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `.claude/settings.local.json`

### Team Roles

| Role                    | Stages | File Ownership              |
| ----------------------- | ------ | --------------------------- |
| protocol-architect      | 00-01  | `01_protocol/**`            |
| search-specialist       | 02     | `02_search/**`              |
| screener-a / screener-b | 03     | `03_screening/**`           |
| fulltext-manager        | 04     | `04_fulltext/**`            |
| data-extractor          | 05     | `05_extraction/**`          |
| statistician            | 06     | `06_analysis/**`            |
| manuscript-writer       | 07     | `07_manuscript/**`          |
| qa-auditor              | 08-09  | `08_reviews/**`, `09_qa/**` |

---

## When User Says "Start" or "See TOPIC.txt"

⚠️ **MANDATORY FIRST STEP**: Run 4-hour feasibility assessment ([Feasibility Checklist](ma-topic-intake/references/feasibility-checklist.md)) before any data extraction or protocol writing.

**Why**: Prevents 10-40 hours of wasted work on unanswerable research questions.

Then proceed:

1. **Ask for project name** if not already specified
2. **Read `projects/<project-name>/TOPIC.txt`** to understand the research question
3. **Check project state** - which stages are complete in `projects/<project-name>/`?
4. **Ask only essential questions** before proceeding:
   - Databases to search — **PubMed + Scopus are mandatory minimum** (PRISMA requires ≥2 databases); optionally add Embase, Cochrane
   - Date range limits?
   - Language restrictions?
   - Study design (RCTs only, or include observational?)
5. **Preliminary analysis type** (two-stage decision — confirmed after screening):
   - If TOPIC.txt describes ≥3 treatments → `analysis_type.preliminary: nma_candidate` (provisional)
   - If TOPIC.txt describes 2 treatments → `analysis_type.preliminary: pairwise`
   - Copy `analysis-type-decision-template.md` → `01_protocol/analysis-type-decision.md`, fill Stage 1
   - **`nma_candidate` requires confirmation after screening** (see Step 3b in end-to-end)
6. **Initialize project** if not done:
   ```bash
   cd /Users/htlin/meta-pipe
   uv run tooling/python/init_project.py --name <project-name>
   ```
7. **Execute pipeline stages** in order, validating at each step

**⚠️ IMPORTANT**: All project data is in `projects/<project-name>/`. All commands are in module-specific `SKILL.md` files.

---

## When User Says "Continue" or "Status"

See [ma-end-to-end/SKILL.md](ma-end-to-end/SKILL.md) for detailed resume behavior.

**Quick summary**:

```bash
cd /Users/htlin/meta-pipe/tooling/python

# 1. Check project status
uv run project_status.py --project <project-name> --verbose

# 2. Show last session summary
uv run session_log.py --project <project-name> resume

# 3. Check for NEXT_STEPS file
ls -t projects/<project-name>/NEXT_STEPS_*.md | head -1
```

Then provide personalized report with next actions.

---

## When User Says "Complete Manuscript" or "Prepare for Submission"

See [ma-manuscript-quarto/SKILL.md](ma-manuscript-quarto/SKILL.md) for detailed workflow.

**Phase 1 (MANDATORY)**: Fill `manuscript_outline.md` and get user approval before writing any sections.

**Phase 2**: Use the **meta-manuscript-assembly** skill (6-8 hours to 90% publication-ready manuscript)

**Phase 3 (QUALITY REFINEMENT)** ⚠️ **DO NOT SKIP** - See [ma-submission-prep/SKILL.md](ma-submission-prep/SKILL.md)

- Transforms 90% → 95-98% readiness (+10% acceptance rate)
- 5 Required Items (Total: 2-3 hours)
- ROI: Prevents 6-12 months revision delay

---

## Rules

- **Environment**:
  - First-time setup: `bash setup.sh` (30-60 min, one-time)
  - Verify anytime: `bash verify_environment.sh` (2 min)
  - See [ENVIRONMENT_QUICK_START.md](ENVIRONMENT_QUICK_START.md) for details
- **Python**: Always `uv run`, never `python3` directly
- **Dependencies**:
  - Python: `uv add <package>` in `tooling/python/`
  - R: `install.packages()` then `renv::snapshot()` in project root
- **API keys**: Read from `.env` ([ma-search-bibliography/references/api-setup.md](ma-search-bibliography/references/api-setup.md))
- **Rounds**: Keep all `round-XX` data, never overwrite
- **Delete**: Use `rip` not `rm`

---

## Decision Points (Ask User)

Only ask if information is missing from TOPIC.txt:

- Target population, intervention, comparator, outcomes (PICO)
- **Analysis type (pairwise vs network)**: preliminary by treatment count (≥3 → `nma_candidate`), confirmed after screening with transitivity assessment
- Additional databases beyond PubMed + Scopus (mandatory minimum): Embase? Cochrane?
- Risk-of-bias tool (RoB 2 vs ROBINS-I)
- Effect measure (RR/OR/HR/SMD/MD)
- Subgroup variables

---

## Documentation Quick Links

**Essential Guides**:

- [Time Investment Guidance](ma-end-to-end/references/time-guidance.md) - Realistic timeline expectations (22-32 hours)
- [Getting Started](GETTING_STARTED.md) - Detailed step-by-step guide

**Module-Specific**:

- Each `ma-*/SKILL.md` contains commands, validation criteria, and key outputs
- Each `ma-*/references/` contains detailed methodology guides

**Network Meta-Analysis** (for ≥3 treatments):

- [NMA Overview](ma-network-meta-analysis/references/nma-overview.md) - When to use NMA vs pairwise MA (10 min)
- [NMA R Guide](ma-network-meta-analysis/references/nma-r-guide.md) - Step-by-step Bayesian NMA workflow (30-45 min)
- [NMA Completion Checklist](ma-network-meta-analysis/references/nma-completion-checklist.md) - 25-item systematic checklist

**R Resources**:

- [R Figure Generation Guide](ma-meta-analysis/references/r-figure-guide.md) - Task-based guides
  - [Forest Plots](ma-meta-analysis/references/r-guides/01-forest-plots.md) - 15-30 min
  - [Table 1](ma-meta-analysis/references/r-guides/05-table1-gtsummary.md) - 30-60 min
  - [Multi-Panel Figures](ma-meta-analysis/references/r-guides/04-multi-panel.md) - 15-20 min

**Journal Preparation**:

- [Journal Formatting](ma-publication-quality/references/journal-formatting.md) - Lancet/JAMA/Nature Medicine requirements
- [Supplementary Materials Template](ma-manuscript-quarto/references/supplementary-materials-template.md)

**Example Project**:

- [ICI in TNBC Meta-Analysis](projects/ici-breast-cancer/) - Complete 99% finished project (5 RCTs, N=2,402)
  - See `projects/ici-breast-cancer/README.md` for navigation
  - Use as template for your own meta-analysis

---

## QA Thresholds

See [ma-end-to-end/SKILL.md](ma-end-to-end/SKILL.md) for complete QA threshold table.

**Key validation points**:

- Dual-review kappa ≥ 0.60
- Figure DPI ≥ 300
- PRISMA checklist 27/27 (or 32/32 for NMA)
- Publication readiness score ≥ 95%

---

## Phase 2 Enhancements (2026-02-17)

**AI Automation**: 95-98% (up from 85-90%)

See [ma-publication-quality/SKILL.md](ma-publication-quality/SKILL.md) for details on:

1. **`publication_readiness_score.py`** — Objective 0-100% score (8 components)
2. **`validate_nma_outputs.py`** — NMA-specific validation (7 checks)
3. **Enhanced `claim_audit.py`** — Overclaim detection (12 patterns)
4. **`nma-completion-checklist.md`** — 25-item pre-submission checklist

**Impact**:

- Manual QA time: 8-12h → **3-4h** (-60%)
- NMA checklist errors: 40% → **<5%**
- Overclaim detection: 0% → **95%**
- Publication readiness clarity: Subjective → **Objective 0-100%**
