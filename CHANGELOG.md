# Changelog

All notable changes to meta-pipe are documented in this file.

## [Unreleased]

### Added
- Open-data extraction ladder — recovers arm-level trial data without institutional access, which is what most of a run outside a university network is otherwise missing
  - `tooling/python/extract_ctgov_arms.py` — per-arm outcomes and adverse-event counts from ClinicalTrials.gov results. Sponsor-reported primary data, often more complete than the paper: papers summarise safety, the registry tabulates every term with a numerator and denominator per arm
  - `tooling/python/extract_arms_llm.py` — arm-level extraction from the best available source per record, strongest provenance first
  - `tooling/python/consolidate_extraction.py` — merges registry and extracted arms by provenance rather than convenience
  - `tooling/python/assess_rob2.py` — RoB 2 from retrieved full text only; an abstract cannot support a risk-of-bias judgement and the script refuses to pretend otherwise
  - `ma-data-extraction/references/open-data-sources.md` — the five tiers, with measured coverage: on one review, 18 PDFs retrieved against 27 recoverable from Europe PMC, 8 of 27 registered trials with posted results, and 41% of included studies carrying an NCT id that appeared nowhere in the manifest
- `ai_screen.py --shard i/n` — stratified sharding so screening runs in parallel; the serial path measured 13.8 s/record, which is 21 hours for two reviewers over 2,756 records. With `merge_screening_shards.py`, which verifies the merged count equals the input exactly, because a lost record is a corrupted PRISMA flow
- `ma-search-bibliography/scripts/ctgov_fetch.py` — ClinicalTrials.gov as a searchable source
- `tooling/python/build_screening_database.py` — bridges Stage 02's BibTeX to the CSV `ai_screen.py` expects; nothing else in the pipeline did

### Fixed
- **Full-text screening was screening abstracts.** Downloaded PDFs were never read, so the full-text kappa measured nothing. Three defects compounded it: `exclude` was the fallback for a parse or retrieval failure, which turns infrastructure failure into an eligibility exclusion; 51 of 122 "PDFs" were HTML interstitials (a paywall returns a login page, not a 404); and the text was never extracted. All three produce plausible-looking numbers, which is why none of them surfaced until the outputs were read
- `ai_screen.py` reviewer-2 pass overwrote reviewer 1's column, silently halving an independent dual review while the kappa still computed
- `build_queries.py` emitted PubMed field tags into the Scopus query (`TITLE-ABS-KEY("Breast Neoplasms"[MeSH])`), which Scopus accepts silently and answers with nonsense
- `create_pdf_manifest.py` never mined NCT ids from titles and abstracts, leaving the column empty for every row
- `download_oa_pdfs.py` recorded an OA landing page with no direct PDF link as unavailable, under-reporting what is reachable
- `publication_readiness_score.py` used file size as a DPI proxy. The proxy points the wrong way: R's `png(res=300)` writes the right pixels and no `pHYs` chunk, so the file declares 72 dpi while being larger than `ragg::agg_png`, which declares 300. It now reads the chunk
- Three scoring bugs in `publication_readiness_score.py` that let it report 124/100

### Added
- Orchestration harness (`.demo/`) — drives a worker Claude Code pane through the pipeline from a second session over the [herdr socket API](https://herdr.dev/docs/socket-api/), one stage at a time
  - `preflight.sh` — 40+ checks that the environment can *finish* a run before it starts. Checks that things run rather than that they are installed: compiles a JAGS model through `rjags`, renders a PDF through Quarto, authenticates each API key live, and lints every prompt so a script path or CLI flag that does not exist is caught in seconds instead of mid-stage
  - `run.sh` — steps the worker through `steps.conf`. Completion is a sentinel file the worker writes **and** a verify command that inspects the artifacts, never the agent's status; liveness is the pane's revision counter, so the budget is an inactivity timeout rather than a wall clock; a worker that is genuinely stuck writes `<id>.blocked` and the run stops for a person
  - `steps.conf` — per-stage timeout and verify command. Verify checks content (a kappa in the agreement file, a confirmed analysis type in `pico.yaml`, a minimum figure count), not mere file existence
  - `prompts/` — one prompt per stage, with the standing rules re-sent on every step so they survive the worker's context compaction
  - `reset.sh` — archives a finished run and re-initializes the project; `--keep-search` carries the slowest, most rate-limited stage forward
  - `README.md` — the design rationale, written as the list of failures each guard exists to prevent
- `.claude/hooks/pipeline-progress.sh` — Stop hook that snapshots pipeline progress after every turn to `projects/<name>/.progress/` (`PROGRESS.md` stage board, append-only `progress.jsonl`, `status.json`). Documented in `.claude/hooks/README.md`, including why it must not be used for liveness: a session started before the hook was last edited keeps the old copy, and nothing outside that session can reload it

### Fixed
- Replace deprecated `datetime.utcnow()` with timezone-aware `datetime.now(timezone.utc)` across 13 files (29 call sites). Output string shape preserved (`...Z` suffix, no `+00:00`). Eliminates all pytest `DeprecationWarning`s
- `tests/test_project_status.py::test_all_stages_complete` — update fixture to create `04_fulltext/manifest.csv` matching the current validation lambda (was creating `round-01/unpaywall_results.csv` from an earlier schema)

### Added
- Sprint 3 of pipeline design fixes (#38)
  - `session_log.py append` subcommand — writes append-only provenance stamps to `09_qa/sessions/artifact_stamps.jsonl` (who/stage/deviations) and attaches to the active session when one exists
  - `ma-end-to-end/references/artifact-stamping.md` — documents the stage-exit provenance convention
  - Stage-exit stamping snippets wired into `ma-screening-quality`, `ma-data-extraction`, `ma-meta-analysis`, and `ma-manuscript-quarto` SKILL files
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
