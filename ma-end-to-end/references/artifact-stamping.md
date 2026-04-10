# Artifact provenance stamping

Every AI-generated pipeline artifact should be stamped so a future reader
can answer three questions without hunting through scattered
`agreement.md` files:

1. **Who generated this?** (AI session, human, or hybrid)
2. **At what stage?** (`03_screening`, `05_extraction`, ...)
3. **Which quality gates were relaxed?** (single reviewer, PROSPERO
   deferred, etc.)

The provenance log lives at
`projects/<name>/09_qa/sessions/artifact_stamps.jsonl` — one JSON object
per line, append-only.

## When to stamp

**At every stage exit**, immediately before marking the pipeline
checklist item complete. If a human would put "done" next to a task,
that is the moment to stamp the artifact.

Also stamp when:

- An AI session produces an output a human would normally sign off on
  (screening decisions, extraction rows, RoB judgments, GRADE ratings)
- A quality gate was relaxed for a valid reason (draft mode, or strict
  mode with a documented deviation)

## How to stamp

```bash
uv run tooling/python/session_log.py --project <name> append \
  --stage 03_screening \
  --artifact 03_screening/round-01/decisions.csv \
  --generator ai \
  --deviation "single reviewer" \
  --deviation "PROSPERO deferred" \
  --notes "Draft mode run; kappa not computed."
```

Flags:

- `--stage` (required): the numbered stage (`03_screening`,
  `05_extraction`, ...).
- `--artifact` (required): path or identifier of the file produced.
- `--generator` (default `ai`): `ai`, `human`, or `hybrid`.
- `--deviation` (repeatable): one per deviation from strict pipeline.
- `--notes`: free-text context.

The stamp is also attached to the current session (if one is active via
`session_log.py start`), so it surfaces in `session_log.py resume`.

## What a stamp looks like

```json
{
  "timestamp": "2026-04-10T15:48:16.418709Z",
  "stage": "03_screening",
  "artifact": "03_screening/round-01/decisions.csv",
  "generator": "ai",
  "deviations": ["single reviewer", "PROSPERO deferred"],
  "notes": "Draft mode run; kappa not computed."
}
```

## Why not just update `session_log.py update`?

`update` records what happened during a session in aggregate (tasks,
decisions, open questions). A stamp is specifically about *artifact
provenance*: it must survive session boundaries, be grep-friendly, and
work even when no session is active (e.g., a script run from cron or CI).

Stamps therefore get their own append-only JSONL file that is never
rewritten.
