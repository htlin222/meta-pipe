#!/usr/bin/env bash
# Start the runner detached from this terminal and from whatever session
# launched it.
#
#   .demo/start.sh [--from <id>] [--only <id>]
#   .demo/stop.sh
#   .demo/status.sh
#
# Why this exists: a runner started as a background job of a Claude Code session
# is a child of that session's shell, and dies with it. Sessions end — they are
# restarted, they crash, they get closed — and a multi-hour pipeline run must not
# depend on one staying open. This puts the runner in its own session (via
# setsid, or Python's os.setsid on macOS where setsid is absent), so the only
# thing that stops it is stop.sh or the machine.

set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pidfile="$HERE/runner.pid"
outfile="$HERE/runner.out"

if [ -f "$pidfile" ] && kill -0 "$(cat "$pidfile")" 2>/dev/null; then
  printf 'runner already running (pid %s)\n' "$(cat "$pidfile")"
  printf 'use .demo/stop.sh first, or .demo/status.sh to see where it is\n'
  exit 1
fi

if command -v setsid >/dev/null 2>&1; then
  setsid nohup bash "$HERE/run.sh" "$@" >> "$outfile" 2>&1 &
  echo $! > "$pidfile"
else
  # macOS has no setsid; detach with a Python double-fork instead.
  python3 - "$HERE" "$pidfile" "$outfile" "$@" <<'PY'
import os, sys
here, pidfile, outfile, *args = sys.argv[1:]
if os.fork() == 0:
    os.setsid()
    fd = os.open(outfile, os.O_WRONLY | os.O_CREAT | os.O_APPEND)
    os.dup2(fd, 1); os.dup2(fd, 2)
    os.close(os.open(os.devnull, os.O_RDONLY))
    pid = os.fork()
    if pid == 0:
        os.execvp("bash", ["bash", os.path.join(here, "run.sh"), *args])
    open(pidfile, "w").write(str(pid))
    os._exit(0)
os.wait()
PY
fi

sleep 2
if [ -f "$pidfile" ] && kill -0 "$(cat "$pidfile")" 2>/dev/null; then
  printf 'runner detached (pid %s) — survives this session ending\n' "$(cat "$pidfile")"
  printf 'follow it with:  tail -f %s\n' "$HERE/run.log"
else
  printf 'runner failed to start; see %s\n' "$outfile"
  exit 1
fi
