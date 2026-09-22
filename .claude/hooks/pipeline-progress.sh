#!/usr/bin/env bash
# Stop hook: snapshot meta-analysis pipeline progress whenever a Claude Code
# session finishes a turn in this repo.
#
# Writes, for the active project:
#   projects/<name>/.progress/PROGRESS.md    human-readable stage board
#   projects/<name>/.progress/progress.jsonl append-only history (one line per turn)
#   projects/<name>/.progress/status.txt     raw project_status.py output
#   projects/<name>/.progress/tick           mtime bumps on every snapshot
#
# The `tick` file is the wake-up signal an orchestrating session can wait on:
#   .demo/wait_for_worker.sh
#
# The active project is read from .demo/ACTIVE_PROJECT, falling back to the most
# recently modified directory under projects/.
#
# A session whose id is listed in .demo/DRIVER_SESSION is the orchestrator: it
# drives the worker and must not snapshot its own turns, or the two sessions
# would wake each other in a loop.

set -uo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
DEMO="$REPO/.demo"

payload="$(cat 2>/dev/null || true)"
session_id="$(printf '%s' "$payload" | jq -r '.session_id // ""' 2>/dev/null || true)"

# Never snapshot the orchestrating session's own turns.
if [ -n "$session_id" ] && [ -f "$DEMO/DRIVER_SESSION" ] \
   && grep -qxF "$session_id" "$DEMO/DRIVER_SESSION" 2>/dev/null; then
  exit 0
fi

project=""
if [ -f "$DEMO/ACTIVE_PROJECT" ]; then
  project="$(tr -d '[:space:]' < "$DEMO/ACTIVE_PROJECT")"
fi
if [ -z "$project" ]; then
  project="$(find "$REPO/projects" -mindepth 1 -maxdepth 1 -type d -not -name 'legacy' \
             -exec stat -f '%m %N' {} + 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2- | xargs -I{} basename {})"
fi
[ -z "$project" ] && exit 0

proj_dir="$REPO/projects/$project"
[ -d "$proj_dir" ] || exit 0

out="$proj_dir/.progress"
mkdir -p "$out"
ts="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# --- stage board -------------------------------------------------------------
# A stage counts as "touched" once it holds at least one non-empty artifact.
stage_line() {
  local dir="$1" label="$2" n
  n="$(find "$proj_dir/$dir" -type f -size +0 -not -name '.*' 2>/dev/null | wc -l | tr -d ' ')"
  if [ "$n" -gt 0 ]; then
    printf '| %s | %s | ✅ | %s |\n' "$dir" "$label" "$n"
  else
    printf '| %s | %s | ⬜ | 0 |\n' "$dir" "$label"
  fi
  printf '%s' ""
}

{
  printf '# Pipeline progress — %s\n\n' "$project"
  printf '_Snapshot written by the Stop hook at %s (session `%s`)._\n\n' "$ts" "${session_id:0:8}"
  printf '| Stage | What it holds | Done | Files |\n'
  printf '|---|---|---|---|\n'
  stage_line 01_protocol   'Protocol, PICO, eligibility'
  stage_line 02_search     'Database queries, .bib results'
  stage_line 03_screening  'Title/abstract dual review'
  stage_line 04_fulltext   'PDFs, full-text eligibility'
  stage_line 05_extraction 'Extraction database'
  stage_line 06_analysis   'R scripts, figures, tables'
  stage_line 07_manuscript 'Quarto manuscript'
  stage_line 08_reviews    'GRADE, risk of bias'
  stage_line 09_qa         'QA, checklists, readiness'
  printf '\n'

  figs="$(find "$proj_dir/06_analysis" -type f \( -name '*.png' -o -name '*.pdf' -o -name '*.svg' \) 2>/dev/null | wc -l | tr -d ' ')"
  printf '**Figures produced:** %s\n\n' "$figs"

  if [ -f "$proj_dir/01_protocol/pico.yaml" ]; then
    printf '**Analysis type:**\n\n```\n%s\n```\n\n' \
      "$(grep -A3 -i 'analysis_type' "$proj_dir/01_protocol/pico.yaml" 2>/dev/null | head -8)"
  fi

  printf '## Latest stage detail\n\n```\n'
  ( cd "$REPO" && uv run tooling/python/project_status.py --project "$project" 2>&1 | tail -40 )
  printf '\n```\n'
} > "$out/PROGRESS.md" 2>/dev/null

( cd "$REPO" && uv run tooling/python/project_status.py --project "$project" --verbose \
    > "$out/status.txt" 2>&1 ) || true
( cd "$REPO" && uv run tooling/python/project_status.py --project "$project" \
    --json "$out/status.json" > /dev/null 2>&1 ) || true

# --- append-only history -----------------------------------------------------
counts=""
for d in 01_protocol 02_search 03_screening 04_fulltext 05_extraction \
         06_analysis 07_manuscript 08_reviews 09_qa; do
  n="$(find "$proj_dir/$d" -type f -size +0 -not -name '.*' 2>/dev/null | wc -l | tr -d ' ')"
  counts="${counts}\"${d}\":${n},"
done
stages_json="{${counts%,}}"

jq -nc \
  --arg ts "$ts" \
  --arg session "$session_id" \
  --arg project "$project" \
  --argjson stages "$stages_json" \
  '{ts:$ts, session:$session, project:$project, stages:$stages}' \
  >> "$out/progress.jsonl" 2>/dev/null || true

# --- wake-up signal for the orchestrating session ----------------------------
date -u +%s > "$out/tick"

printf '{"systemMessage":"📊 Pipeline snapshot written → projects/%s/.progress/PROGRESS.md","suppressOutput":true}\n' "$project"
exit 0
