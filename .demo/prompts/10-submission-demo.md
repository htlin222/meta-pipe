Stage 10 — submission preparation, and then the thing this whole run was actually for: the demonstration record. Same standing rules.

1. Invoke `ma-submission-prep` and complete Phase 3 quality refinement — the five required items. This is the step the repo's docs warn not to skip, so do not skip it.
2. Produce the submission package in `10_submission/` (create it): cover letter, title page, highlights, the PROSPERO-style registration record, data availability statement, and the supplementary materials bundle.
3. Run `uv run tooling/python/consolidate_project_outputs.py --project-name neo-her2-ebc` and `uv run ma-end-to-end/scripts/hash_artifacts.py --root projects/neo-her2-ebc` for the reproducibility audit.
4. Write `projects/neo-her2-ebc/README.md` as a navigation guide, in the style of `projects/ici-breast-cancer/README.md`.

### The demonstration record

Write `projects/neo-her2-ebc/DEMO_WALKTHROUGH.md` — the document someone reads to learn how this repo is actually used. Cover:

- The pipeline as it ran, stage by stage: the command, the artifact it produced, the gate it had to clear.
- The gates that did real work — the feasibility check, the screening kappa, the Stage 03b analysis-type confirmation, the full-text eligibility gate, the readiness score — and what each one caught or would have caught.
- **The decisions a human still owns.** This is the most useful section and the one a demo usually omits. Name the points where the pipeline produced a defensible answer that a domain expert should still overrule, and say why.
- Wall-clock time per stage against the 22–32 hour manual estimate in `ma-end-to-end/references/time-guidance.md`.
- Where the automation was genuinely weak: which retrievals failed, which extractions needed hand verification, which numbers you could not source.
- How the orchestration worked — the Stop hook in `.claude/hooks/pipeline-progress.sh` writing a progress snapshot at the end of every turn, and a second Claude Code session reading it over the herdr socket API and sending the next step. Include the reproduction commands.

Write it for a reader deciding whether to trust this pipeline with their own review. Honest about the limits is more persuasive than polished.

Finish with: the submission package file list, the reproducibility hash file, total wall-clock time, and the one change to this repo that would most improve the next run.
