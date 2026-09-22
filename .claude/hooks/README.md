# Hooks

## `pipeline-progress.sh` — Stop hook

Runs when a Claude Code session in this repo finishes a turn. It snapshots where
the active meta-analysis project stands, so progress is a file on disk rather
than something you have to scroll a transcript to reconstruct.

Registered in `.claude/settings.json`:

```json
{ "hooks": { "Stop": [ { "matcher": "", "hooks": [
  { "type": "command", "command": "bash .claude/hooks/pipeline-progress.sh", "timeout": 60 }
] } ] } }
```

### What it writes

Into `projects/<active>/.progress/`:

| File | Contents |
|---|---|
| `PROGRESS.md` | Stage board — which of `01_protocol` … `09_qa` hold artifacts, figure count, current stage |
| `progress.jsonl` | One line per turn: timestamp, session id, per-stage file counts |
| `status.txt` / `status.json` | Raw `project_status.py` output |
| `tick` | Unix timestamp; its mtime bumps on every snapshot |

### Which project

`.demo/ACTIVE_PROJECT` if present, otherwise the most recently modified
directory under `projects/`.

### This hook is a convenience, not a control mechanism

It exists so that anyone watching the worker pane — or opening the repo later —
can see where the run stands without scrolling a transcript.

Do not build liveness on it. A Claude Code session loads its hook configuration
at startup, so a worker that was already running when this hook was added or
edited keeps the old copy, and nothing outside that session can reload it. The
first run of the harness lost 40 minutes to exactly that: the hook had been
registered with a relative path, the worker had changed directory, and the
orchestrator sat waiting for a snapshot that was never going to arrive.

So `.demo/run.sh` calls this script itself after every step, and treats a
sentinel file the worker writes as the completion signal. See
[`.demo/README.md`](../../.demo/README.md).

A session listed in `.demo/DRIVER_SESSION` is an orchestrator and is skipped —
otherwise the driver and worker would wake each other in a loop.

### Notes

- Exits 0 on every path. A snapshot failure must never block a turn from ending.
- Needs `jq`, and `uv` for `project_status.py`.
- Uses BSD `stat`/`find` flags (macOS).
- `.demo/` and `projects/*/.progress/` are gitignored — they are runtime state.
