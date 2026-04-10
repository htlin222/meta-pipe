# Changelog

All notable changes to meta-pipe are documented in this file.

## [Unreleased]

### Added
- Sprint 2 of pipeline design fixes (#38)
  - `init_project.py`: `--mode {strict,draft}` flag. Draft mode writes `.ma_meta.json` with `quality_mode: draft` and a `DRAFT_MODE.md` notice so fast-prototype runs are explicit and non-publishable
  - `tooling/python/project_meta.py`: shared helper that reads `.ma_meta.json` (single source of truth for project quality mode)
  - `validate_pipeline.py`: reads quality mode and reports unchecked items as NOTES (exit 0) in draft mode, FAILURES (exit 2) in strict mode; added `--json` output for programmatic consumers
  - `ma-data-extraction/templates/prognostic_factor.yaml` + `.md`: 19-field 2×2 extraction template for binary exposure → binary outcome studies. Plugs directly into `create_extraction_template.py`
- Sprint 1 of pipeline design fixes (#38)
  - `ma-search-bibliography/scripts/enrich_abstracts.py`: new abstract enrichment stage (Entrez → CrossRef → OpenAlex fallbacks) so dedupe.bib records reach screening with abstracts populated
  - `tooling/python/CLAUDE_CLI_FLAGS.md`: documents required `claude` CLI flags, minimum version (2.1.100), and the `--bare` + `ANTHROPIC_API_KEY` auth interaction
  - `scopus_fetch.py`: reports `opensearch:totalResults`, warns on silent truncation, adds `--strict-cap` flag
  - `ai_screen.py`: startup `_assert_claude_cli()` check verifies `--bare` and `--output-format` flags exist

### Changed
- `ai_screen.py`: `_invoke_claude()` now uses `claude -p --bare --output-format json` when `ANTHROPIC_API_KEY` is set, cutting per-call input tokens from ~10k → ~1.5k; falls back to non-bare with a one-time warning when only OAuth is available
- `ai_screen.py`: `META_PIPE_ROOT` resolved from `$MA_PIPE_ROOT` or module-relative path instead of hardcoded `/Users/htlin/meta-pipe`
- `tooling/python/pyproject.toml`: pinned `rapidfuzz`, `lxml` (biopython, bibtexparser, requests were already present); ran `uv lock`

### Fixed
- Fix hooks schema in `.claude/settings.local.json` (matcher + hooks array structure)

## [2026-03-24]

### Added
- Agent teams orchestration framework for parallel meta-analysis (#28)
  - Hook scripts for `TaskCompleted` and `TeammateIdle` events
  - Team spawn helper (`tooling/python/team_spawn_helper.py`)
  - Role-specific prompts in `ma-agent-teams/prompts/`
  - G-CSF neutropenia NMA test project for agent teams validation
- Academic and Non-Commercial Use License (English + Chinese)

### Fixed
- Verification script bugs (#26)
- `setup.sh` fails on macOS ARM: R package 'fs' requires cmake (#24)
- Missing file noted when creating new projects (#22)

## [2026-03-22]

### Added
- Peters' test for binary outcomes and low-power caveat in bias analysis
- Semi-automated GRADE with computed suggestions and rationale (#16)
- Stage 04b full-text eligibility screening (PRISMA item 16)
- CITATION.cff with Lin HT as first author (#14)
- Manuscript `.gitignore` and Vancouver citation style

## [2026-03-21]

### Added
- Manuscript scaffold, dashboard plan, and Python test suite
- Publish workflow to high-IF journal article (#9)

### Fixed
- League table heatmap not included (#3)

## [2026-03-19]

### Added
- `.gitignore` for ici-breast-cancer project
- Script to create GitHub private repositories

## [2026-02-17]

### Added
- Phase 2 enhancements (AI automation 95-98%)
  - `publication_readiness_score.py` — objective 0-100% score
  - `validate_nma_outputs.py` — NMA-specific validation (7 checks)
  - Enhanced `claim_audit.py` — overclaim detection (12 patterns)
  - `nma-completion-checklist.md` — 25-item pre-submission checklist

## [2026-02-08]

### Changed
- Migrated all projects to `projects/<project-name>/` structure
- Legacy data moved to `projects/legacy/`

## [2026-02-06]

### Added
- Initial release of meta-pipe
- Complete meta-analysis pipeline: 10 stages from topic intake to submission
- Skills: `ma-topic-intake`, `ma-search-bibliography`, `ma-screening-quality`, `ma-fulltext-management`, `ma-data-extraction`, `ma-meta-analysis`, `ma-network-meta-analysis`, `ma-manuscript-quarto`, `ma-peer-review`, `ma-publication-quality`
- End-to-end orchestration (`ma-end-to-end`)
- Module registry validation and management
- LLM-assisted data extraction tools (Stage 05)
- PROSPERO protocol generator, RoB 2 and ROBINS-I assessment tools
- Generalized PDF retrieval tools for systematic reviews
- Example project: ICI in triple-negative breast cancer (5 RCTs, N=2,402)
