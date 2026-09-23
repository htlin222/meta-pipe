#!/usr/bin/env bash
# One command to see where everything stands after coming back to a session.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/.." && pwd)"
# shellcheck source=/dev/null
. "$HERE/config.env"
pd="$REPO/projects/$PROJECT"

printf '\033[1mrunner\033[0m   '
if [ -f "$HERE/runner.pid" ] && kill -0 "$(cat "$HERE/runner.pid")" 2>/dev/null; then
  printf 'running (pid %s)\n' "$(cat "$HERE/runner.pid")"
else
  printf '\033[31mnot running\033[0m — start with .demo/start.sh\n'
fi

printf '\033[1mworker\033[0m   %s\n' \
  "$(herdr pane get "$WORKER_PANE" 2>/dev/null | jq -r '.result.pane | "\(.agent_status)  rev=\(.revision)"')"

printf '\033[1mstep\033[0m     %s\n' "$(cat "$HERE/CURRENT_STEP" 2>/dev/null || echo '-')"

printf '\033[1mdone\033[0m     %s\n' \
  "$(ls "$pd/.progress/steps/" 2>/dev/null | sed 's/\.done$//' | tr '\n' ' ')"

n="$(pgrep -f 'ai_screen' 2>/dev/null | wc -l | tr -d ' ')"
[ "$n" -gt 0 ] && printf '\033[1mscreening\033[0m %s shard processes alive\n' "$n"

printf '\033[1mchanged\033[0m  '
last="$(find "$pd" -type f -not -path '*/.progress/*' -newermt "$(date -v-999M -u +%Y-%m-%dT%H:%M:%S)" -print0 2>/dev/null | xargs -0 stat -f '%m %N' 2>/dev/null | sort -rn | head -1)"
if [ -n "$last" ]; then
  printf '%s  (%s)\n' "$(date -r "${last%% *}" +%H:%M:%S)" "$(basename "${last#* }")"
else
  printf 'nothing recent\n'
fi

printf '\n\033[1mlast events\033[0m\n'
tail -6 "$HERE/run.log" 2>/dev/null | sed 's/^/  /'
