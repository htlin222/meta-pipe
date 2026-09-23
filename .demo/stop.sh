#!/usr/bin/env bash
# Stop the detached runner. Does not touch the worker: a turn already in flight
# finishes, and any background work it started keeps going.
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pidfile="$HERE/runner.pid"
if [ -f "$pidfile" ] && kill -0 "$(cat "$pidfile")" 2>/dev/null; then
  kill "$(cat "$pidfile")" && printf 'runner stopped (pid %s)\n' "$(cat "$pidfile")"
  rm -f "$pidfile"
else
  pkill -f "$HERE/run.sh" 2>/dev/null && printf 'stopped a runner with no pidfile\n' \
    || printf 'no runner running\n'
  rm -f "$pidfile"
fi
