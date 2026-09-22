#!/usr/bin/env bash
# Drive the worker Claude Code pane through every step in .demo/steps.conf.
#
#   .demo/run.sh [--from <step-id>] [--only <step-id>] [--dry-run]
#
# Each stdout line is an event for the orchestrating session to watch.
#
# Design notes — each of these is a bug the first run actually hit:
#
#   * Completion is a sentinel file the worker writes, plus a verify command,
#     never the agent's status. Polling status mistook the tail of the previous
#     turn for the start of the next one and "completed" a stage in 108 seconds.
#   * Submission is confirmed. A large paste can land in the input box unsent,
#     leaving Claude Code showing "ctrl+enter to send now" while the runner waits
#     for a turn that never began.
#   * The snapshot is taken by the runner every time. The Stop hook is a
#     convenience for whoever is watching the pane; a worker session started
#     before the hook was last edited silently keeps the old copy, so liveness
#     must not depend on it.
#   * The standing rules are restated on every prompt, because a run this long
#     compacts the worker's context several times.
#   * "Not finished yet" and "cannot be finished" are different. A worker that
#     is genuinely stuck writes <id>.blocked and the run stops for a person,
#     instead of burning its retries on nudges it cannot act on.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
# shellcheck source=/dev/null
. "$HERE/config.env"

PANE="$WORKER_PANE"
pd="$REPO/projects/$PROJECT"
steps_dir="$pd/.progress/steps"
log="$HERE/run.log"
HOOK="$REPO/.claude/hooks/pipeline-progress.sh"

from=""; only=""; dry=0
while [ $# -gt 0 ]; do
  case "$1" in
    --from) from="$2"; shift 2 ;;
    --only) only="$2"; shift 2 ;;
    --dry-run) dry=1; shift ;;
    *) printf 'unknown argument: %s\n' "$1" >&2; exit 2 ;;
  esac
done

mkdir -p "$steps_dir"

# Slurped once so the table can be edited while a run is in flight.
STEP_TABLE="$(cat "$HERE/steps.conf")"

say() { printf '%s %s\n' "$(date +%H:%M:%S)" "$*"; printf '%s %s\n' "$(date -u +%FT%TZ)" "$*" >> "$log"; }
status() { herdr pane get "$PANE" 2>/dev/null | jq -r '.result.pane.agent_status // "unknown"'; }
snapshot() { printf '{"session_id":"runner"}' | bash "$HOOK" >/dev/null 2>&1 || true; }

PREAMBLE='[standing rules, restated every step because your context gets compacted]
You are the worker session for a meta-pipe demonstration. Do the step below completely, then stop. No human is available, so do not ask questions: where a decision is missing, take the default this repo documents, write the choice and the reason into 01_protocol/decision-log.md, and continue.
(1) Never invent study data. Every number reaching the extraction database or the manuscript must trace to a source you actually retrieved; anything you cannot source is recorded as missing. Honest gaps are acceptable, fabricated trial results are not.
(2) Keep the audit trail: never overwrite a round-XX directory, use rip not rm, run Python via uv run, use absolute paths.
(3) Do not shrink the corpus, loosen a gate, or skip a stage to save time. If something is too slow, make it faster, or say plainly that it is too slow.

'

postamble() {
  cat <<EOF

[how this step is checked]
When the step is genuinely finished, write \`projects/$PROJECT/.progress/steps/$1.done\` containing a short summary of what you produced and anything you could not. Write it last, write it once, and never write it for work you did not do.

If you cannot finish because something is genuinely outside your reach — a missing credential, a dependency that will not install, a methodological decision that needs a human — write \`projects/$PROJECT/.progress/steps/$1.blocked\` instead, saying what is blocking you and what you would need to proceed. That stops the run and escalates to a person. Use it when you are stuck, not when the work is merely long: a blocker you could resolve by trying harder is not a blocker.
EOF
}

# Paste, then confirm the turn actually started; force the send if it did not.
submit() {
  local text="$1" i s
  s="$(status)"
  if [ "$s" != "working" ]; then
    herdr pane send-keys "$PANE" esc >/dev/null 2>&1
    sleep 1
  fi
  herdr agent prompt "$PANE" "$text" >/dev/null 2>&1
  sleep 5
  [ "$(status)" = "working" ] && return 0
  for i in 1 2 3; do
    say "  … prompt sat unsent (try $i) — forcing send"
    herdr pane send-keys "$PANE" "ctrl+enter" >/dev/null 2>&1
    sleep 5
    [ "$(status)" = "working" ] && return 0
    herdr pane send-keys "$PANE" "enter" >/dev/null 2>&1
    sleep 5
    [ "$(status)" = "working" ] && return 0
  done
  return 1
}

verify() { ( cd "$pd" && eval "$1" ) >/dev/null 2>&1; }

# Wait for the sentinel. Returns 0 sentinel, 1 stalled, 2 agent blocked,
# 3 worker went quiet without writing it, 4 worker declared itself blocked.
#
# The budget is an INACTIVITY budget, not a wall clock. A worker that is
# visibly working does not get killed for taking a long time — the first run
# had a stage legitimately spend 35 minutes fetching abstracts, and an absolute
# deadline would have shot it mid-flight. Liveness comes from the pane's
# revision counter, which advances whenever the terminal produces output.
await() {
  local sentinel="$1" idle_budget_s="$2" settled=0 s rev last_rev="" last_change
  last_change="$(date +%s)"
  while :; do
    [ -f "$sentinel" ] && return 0
    [ -f "${sentinel%.done}.blocked" ] && return 4
    s="$(status)"
    case "$s" in
      blocked) return 2 ;;
      idle|done)
        settled=$((settled+1))
        [ "$settled" -ge "$SETTLE_POLLS" ] && { [ -f "$sentinel" ] && return 0; return 3; }
        ;;
      *) settled=0 ;;
    esac

    rev="$(herdr pane get "$PANE" 2>/dev/null | jq -r '.result.pane.revision // ""')"
    if [ -n "$rev" ] && [ "$rev" != "$last_rev" ]; then
      last_rev="$rev"; last_change="$(date +%s)"
    elif [ $(( $(date +%s) - last_change )) -ge "$idle_budget_s" ]; then
      return 1
    fi
    sleep "$POLL_SECONDS"
  done
}

run_step() {
  local id="$1" prompt_file="$2" timeout_min="$3" check="$4"
  local sentinel="$steps_dir/$id.done" rc attempt=0 body

  rm -f "$sentinel" "$steps_dir/$id.blocked"
  body="$PREAMBLE$(cat "$prompt_file")$(postamble "$id")"

  while [ "$attempt" -lt 3 ]; do
    attempt=$((attempt+1))
    say "▶ step $id ($(basename "$prompt_file")) attempt $attempt, stalls after ${timeout_min}m of no output"

    if ! submit "$body"; then
      say "✖ step $id could not be submitted to the pane"
      return 1
    fi

    await "$sentinel" $(( timeout_min * 60 )); rc=$?
    snapshot

    case "$rc" in
      4) say "✖ step $id — the worker reports it is blocked and needs a person:"
         sed 's/^/     /' "$steps_dir/$id.blocked" | head -25
         return 1 ;;
      2) say "⚠ step $id BLOCKED — instructing it to decide and continue"
         body="You are blocked on a question and no human is available. Choose the option this repo documents as the default, record the choice and your reasoning in 01_protocol/decision-log.md, finish the step, and write the .done sentinel. Do not ask again."
         continue ;;
      1) say "✖ step $id produced no output for ${timeout_min}m — stalled"
         return 1 ;;
      3) say "⚠ step $id went quiet without writing its sentinel — nudging"
         body="You stopped without writing projects/$PROJECT/.progress/steps/$id.done, so the step is not finished. Do not re-plan from scratch and do not start anything new: complete what the last instruction asked for, then write that file. If something genuinely blocks you, write the blocker into 01_protocol/decision-log.md and say so plainly instead of writing the sentinel."
         continue ;;
    esac

    if verify "$check"; then
      say "✓ step $id complete and verified"
      return 0
    fi

    say "⚠ step $id wrote its sentinel but verification failed: $check"
    rm -f "$sentinel"
    body="You wrote the .done sentinel for step $id, but the check that guards this step still fails:

    $check

That check runs with the working directory at projects/$PROJECT/. Look at what it is asserting, produce what is genuinely missing, and only then write the sentinel again. If the check itself is wrong rather than your work, say so and explain why instead of forcing it."
  done

  say "✖ step $id failed after 3 attempts"
  return 1
}

say "=== run start (project=$PROJECT pane=$PANE) ==="

if [ "$dry" = 1 ]; then
  while IFS='|' read -r id prompt timeout check; do
    case "$id" in ''|'#'*) continue ;; esac
    printf '%-4s %-26s %4sm  ' "$id" "$prompt" "$timeout"
    [ -f "$HERE/prompts/$prompt" ] || { printf 'MISSING PROMPT\n'; continue; }
    verify "$check" && printf 'already satisfied\n' || printf 'pending\n'
  done <<< "$STEP_TABLE"
  exit 0
fi

if [ "$(status)" = "working" ]; then
  say "… worker is mid-turn; waiting for it to settle before taking over"
  while [ "$(status)" = "working" ]; do sleep "$POLL_SECONDS"; done
  snapshot
fi

started=0
while IFS='|' read -r id prompt timeout check; do
  case "$id" in ''|'#'*) continue ;; esac

  [ -n "$only" ] && [ "$id" != "$only" ] && continue
  if [ -n "$from" ] && [ "$started" = 0 ]; then
    [ "$id" = "$from" ] && started=1 || continue
  fi

  if [ -f "$steps_dir/$id.done" ] && verify "$check"; then
    say "⏭ step $id already complete"
    continue
  fi
  if verify "$check"; then
    say "⏭ step $id artifacts already present — accepting without re-running"
    touch "$steps_dir/$id.done"
    continue
  fi

  printf '%s' "$id" > "$HERE/CURRENT_STEP"
  if ! run_step "$id" "$HERE/prompts/$prompt" "$timeout" "$check"; then
    say "=== run stopped at step $id — needs a look ==="
    exit 1
  fi
  [ -n "$only" ] && break
done <<< "$STEP_TABLE"

say "=== run finished ==="
