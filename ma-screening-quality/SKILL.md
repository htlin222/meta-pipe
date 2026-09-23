---
name: ma-screening-quality
description: Perform title and abstract screening, apply inclusion and exclusion criteria, and assess study quality or risk of bias. Use when selecting eligible studies for meta-analysis.
---

# Ma Screening Quality

## Overview

Screen search results, document decisions, and assess risk of bias or quality.

## Inputs

- `03_screening/screening-database.csv` (created by search stage)
- `01_protocol/eligibility.md`

## Outputs

- `03_screening/round-01/decisions.csv`
- `03_screening/round-01/exclusions.csv`
- `03_screening/round-01/quality.csv`
- `03_screening/round-01/included.bib`
- `03_screening/round-01/agreement.md`

## Commands

### AI Screening (Reviewer 1)

```bash
# AI screens all records as Reviewer 1 (uses claude -p with OAuth)
uv run tooling/python/ai_screen.py --project <project-name>

# AI screens as Reviewer 2 (for dual AI review)
uv run tooling/python/ai_screen.py --project <project-name> --reviewer 2

# Specify a different round
uv run tooling/python/ai_screen.py --project <project-name> --round round-02
```

### Parallel Screening (`--shard`) — required for corpora above a few hundred records

`ai_screen.py` makes one `claude -p` call per record per reviewer and runs
serially: roughly **14 s per record** measured. A 2,700-record corpus under dual
review is ~21 hours that way. `--shard i/n` splits the work so shards run
concurrently.

```bash
# Build the input ai_screen.py expects (nothing else in the pipeline creates it)
uv run tooling/python/build_screening_database.py --project <name> \
    --in-csv projects/<name>/03_screening/records_with_abstracts.csv

# Fan out: N shards per reviewer, all concurrent
for i in $(seq 1 32); do
  uv run tooling/python/ai_screen.py --project <name> --stage abstract \
      --reviewer 1 --shard $i/32 &
done; wait

# Same for reviewer 2, then merge (fails loudly if any record is lost)
uv run tooling/python/merge_screening_shards.py --project <name> --round round-01
```

- Records are assigned by **stride** (`records[i-1::n]`), so the shards partition
  the corpus exactly — no record is screened twice or skipped, and each shard
  sees a comparable mix rather than one era or one source.
- Each shard writes `<round>/shards/decisions.r<R>.shard-<i>-of-<n>.csv` and
  never touches `<round>/decisions.csv`, so concurrent shards and the two
  reviewers cannot clobber each other.
- **Dual-review safety (fixed, D-029)**: a reviewer pass now **merges into** an
  existing `decisions.csv` instead of replacing it, seeding from the file on disk
  and overlaying only the column it owns. Before this fix, `--reviewer 2` re-read
  the pristine `screening-database.csv` (whose `Reviewer1_*` columns are empty)
  and overwrote `decisions.csv`, silently destroying half of an independent dual
  review — the exact thing the kappa measures. A guard now **refuses to write** if
  the pass would reduce the number of populated cells in any column it does not
  own, so this class of data loss fails loudly instead of passing silently.
- `merge_screening_shards.py` refuses to write unless every reviewer's shard set
  is complete and covers the corpus exactly — a dropped record silently corrupts
  the PRISMA flow, so it is treated as a hard error.

### Dual-Review Agreement

```bash
# Compute Cohen's kappa after both reviewers finish
uv run ma-screening-quality/scripts/dual_review_agreement.py \
  --file projects/<project-name>/03_screening/round-01/decisions.csv \
  --col-a Reviewer1_Decision --col-b Reviewer2_Decision \
  --out projects/<project-name>/03_screening/round-01/agreement.md
```

## Workflow

1. **AI Screening (Reviewer 1)**: Run `ai_screen.py --project <name>` to auto-screen all records against `eligibility.md`.
   - Read from `01_protocol/eligibility.md`
   - Read from `03_screening/screening-database.csv`
   - Write to `03_screening/round-01/decisions.csv` (fills `Reviewer1_Decision` and `Reviewer1_Reason` columns)
2. **Human/AI Reviewer 2**: Either run `ai_screen.py --reviewer 2` for dual-AI review, or have a human fill `Reviewer2_Decision` and `Reviewer2_Reason` columns manually.
   - Update `03_screening/round-01/decisions.csv` (adds `Reviewer2_Decision` and `Reviewer2_Reason` columns)
3. **Compute agreement**: Run `dual_review_agreement.py` to calculate Cohen's kappa (target >= 0.60).
   - Use `scripts/dual_review_agreement.py`
   - Write to `03_screening/round-01/agreement.md`
4. **Resolve conflicts**: Review records where Reviewer 1 and 2 disagree; fill `Final_Decision`.
   - Update `03_screening/round-01/decisions.csv` (`Final_Decision` column)
5. **Record exclusion reasons** using standardized labels from `references/screening-labels.md`.
   - Write to `03_screening/round-01/exclusions.csv`
6. **Quality/RoB assessment**: Assess included studies using the tool appropriate for the study design.
   - Write to `03_screening/round-01/quality.csv`
7. **Create `included.bib`** from final included studies.
   - Write to `03_screening/round-01/included.bib`

## How `ai_screen.py` Works

- **Topic-agnostic**: reads `eligibility.md` from any project, passes it to Claude as screening criteria
- **Uses `claude -p --model haiku`**: OAuth-based, no API key needed, fast and cheap
- **Skips already-decided rows**: safe to re-run if interrupted
- **`--shard i/n`**: screen one stride-selected shard, for concurrent execution (see above)
- **Liberal screening**: when uncertain, defaults to MAYBE (standard practice at title/abstract stage)
- **Generic exclusion codes**: P1/P2 (population), I1/I2 (intervention), C1 (comparator), S1-S4 (study design), O1/O2 (outcomes), T1/T2 (time), L1 (language), D1 (duplicate)

## Resources

- `references/screening-labels.md` provides standardized decision labels.
- `references/dual-review-schema.md` defines recommended decision columns.
- `scripts/dual_review_agreement.py` computes agreement and Cohen's kappa.
- `tooling/python/build_screening_database.py` builds `03_screening/screening-database.csv` from `dedupe.bib` or from `enrich_abstracts.py` output.
- `tooling/python/merge_screening_shards.py` reassembles `ai_screen.py --shard` outputs into one `decisions.csv`, failing loudly on any lost or duplicated record.

## Step 8: Analysis Type Confirmation Gate

**When**: After screening is complete and included studies are identified.
**Why**: The preliminary NMA vs Pairwise decision (from Stage 01) was based on treatment count alone. Now we have actual study data to validate that decision.

**Trigger**: If `01_protocol/pico.yaml` has `analysis_type.preliminary: nma_candidate`

### Procedure

1. Tally study designs among included studies (RCT head-to-head, RCT vs control, single-arm, observational)
   - Read from `03_screening/round-01/decisions.csv` (`Final_Decision` == "INCLUDE")
2. Compute comparative study proportion (target: >70% for NMA)
3. Assess network connectivity (common comparator? isolated nodes?)
4. Preliminary transitivity check (similar populations across comparisons?)
5. Record decision in `01_protocol/analysis-type-decision.md` (Stage 2)
   - Update `01_protocol/analysis-type-decision.md` (fill Stage 2 section)
6. Update `01_protocol/pico.yaml` with confirmed analysis type
   - Update `01_protocol/pico.yaml` (L23: analysis_type.confirmed field)
   - Update `01_protocol/pico.yaml` (L24: analysis_type.confirmation_stage = "03_screening")
7. If changed from preliminary: document reason in `01_protocol/decision-log.md`
   - Append to `01_protocol/decision-log.md`

**If >30% single-arm studies**: NMA transitivity assumption is very strong — consider pairwise MA + pooled proportions instead.

## Validation

- Compute agreement for dual screening when applicable (kappa >= 0.60).
- Confirm all included studies meet eligibility criteria.
- **If `nma_candidate`**: Confirm or change analysis type before proceeding to Stage 04.

## Stage Exit: Stamp the artifact

Before marking this stage complete, record provenance for the decisions
CSV so downstream readers can tell whether screening was dual-review,
single-reviewer, AI-only, etc. See
[artifact-stamping.md](../ma-end-to-end/references/artifact-stamping.md)
for the full convention.

```bash
uv run tooling/python/session_log.py --project <project-name> append \
  --stage 03_screening \
  --artifact 03_screening/round-01/decisions.csv \
  --generator ai \
  --deviation "single reviewer"  # omit if dual review completed
```

## Pipeline Navigation

| Step | Skill                     | Stage                       |
| ---- | ------------------------- | --------------------------- |
| Prev | `/ma-search-bibliography` | 02 Search & Bibliography    |
| Next | `/ma-fulltext-management` | 04 Full-text Management     |
| All  | `/ma-end-to-end`          | Full pipeline orchestration |
