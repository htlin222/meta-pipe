# Driving the pipeline from a second Claude Code session

One Claude Code session (the **worker**) runs the meta-analysis. A second session
(the **orchestrator**) sends it one stage at a time over the
[herdr socket API](https://herdr.dev/docs/socket-api/), checks what came back,
and decides whether to advance. The pipeline is long enough that a human cannot
sit through it, and unreliable enough in places that nobody should let it run
unwatched — this is the middle path.

```
orchestrator ── herdr agent prompt ──▶ worker runs one stage
      ▲                                      │
      │                              writes <id>.done
      │                                      │
      └──── verify command passes ◀──────────┘
```

## Run it

```bash
.demo/preflight.sh          # never skip this
.demo/start.sh              # run it detached — survives the session ending
.demo/status.sh             # where everything stands; the first command on coming back
.demo/stop.sh               # stop the runner; the worker's current turn finishes

.demo/start.sh --from 06    # resume from a step
.demo/start.sh --only 07    # one step
.demo/start.sh --await 03   # a step is already running: wait, do not resubmit
.demo/run.sh --dry-run      # what is already satisfied

.demo/reset.sh --yes --keep-search   # archive and start clean
```

Set `WORKER_PANE` and `DRIVER_SESSIONS` in `config.env` first — `herdr pane list`
finds the pane id.

Progress at any moment: `projects/<project>/.progress/PROGRESS.md`.

## Files

| File | Role |
|---|---|
| `config.env` | pane id, project name, driver session ids, poll timing |
| `preflight.sh` | proves the environment can finish the run, before it starts |
| `steps.conf` | `id \| prompt \| timeout \| verify command` |
| `prompts/` | one file per stage — the actual instructions to the worker |
| `run.sh` | the runner |
| `start.sh` / `stop.sh` / `status.sh` | detached lifecycle |
| `prompts/_shakedown/` | mid-run repairs from the first run, and why each is now unnecessary |
| `reset.sh` | archive a finished run, re-init the project |
| `run.log` | append-only event log |

## What the first run broke, and what now prevents it

Every guard here exists because the shakedown run hit the thing it guards.

**A stage "completed" in 108 seconds.** Completion was inferred from
`agent_status`, and the poller caught the tail of the previous turn. Completion
is now a sentinel file the worker writes (`.progress/steps/<id>.done`) *and* a
verify command that inspects the artifacts. Status is used only for liveness.

**A prompt sat in the input box, unsent.** A large paste can land in Claude
Code's composer without submitting; the pane shows `ctrl+enter to send now` and
the runner waits forever for a turn that never began. `submit()` now confirms the
agent actually entered `working`, and forces the send if it did not.

**The Stop hook silently stopped firing.** It was registered with a relative
path, and the worker had changed directory. Worse, a worker session started
before the hook was last edited keeps the old copy — you cannot fix that from
outside the session. The hook is now a convenience for whoever is watching the
pane; the runner takes its own snapshot after every step regardless.

**Verification accepted empty files.** The old gate was "does this path exist".
`steps.conf` verify commands check content: a kappa in the agreement file, a
confirmed analysis type in `pico.yaml`, at least four figures, more than two
data rows in the extraction CSV.

**A flag typo cost a whole stage.** `--stage title` where the script spells it
`--stage abstract`. Preflight now lints every prompt: each script it names must
exist, and each flag it passes must appear in that script's `--help`.

**Dependencies were discovered at hour 1.5.** JAGS, `rjags`, `netmeta`, `gemtc`
and LaTeX were all missing, and Stage 06's primary analysis is
gemtc → rjags → JAGS. Preflight checks that things *run*, not that they are
installed: it compiles a JAGS model and renders a PDF. `rjags` from CRAN links
`libjags.4`, so a Homebrew JAGS 5 installs cleanly and then fails to load —
"installed" would have passed, "compiles a model" does not.

**Adding an API key broke manuscript rendering.** Quarto's dotenv treats every
key in `.env.example` as required and non-empty, so once a partially-filled
`.env` existed, `quarto render` died at the repo root before reading the
document. It reads only the current directory, so rendering from
`07_manuscript/` is fine. Preflight tests it the way Stage 07 runs it, and warns
about the repo-root trap.

**An idle agent is not an idle pipeline.** The worker legitimately ends a turn
while background shells it started keep working, and 16 screening shards write
only on completion — the tree can be quiet for 25 minutes while everything is
fine. Nudging then interrupts work in flight. Busy now means "files changed
recently **or** a live process names this project".

**The runner died with the session that launched it.** It was a background job
of that shell. `start.sh` puts it in its own session, so a multi-hour run does
not depend on a terminal staying open, and `--await` attaches to a step already
running instead of resubmitting a prompt for work the worker is still doing.

**A verify command must be able to fail.** The first version of one step checked
a condition that was already true before the step ran, so the runner skipped it
and reported success. Write the check so it would fail on a plausible
half-finished attempt — that is the whole job of the check.

**The worker's context compacts mid-run.** Several times, over this many stages.
The standing rules — do not invent data, do not shrink the corpus to save time,
keep the audit trail — are re-sent as a preamble on every prompt rather than
stated once at the start.

## Adding a stage

Add a prompt to `prompts/`, add a line to `steps.conf`, run `preflight.sh` to
lint it. Write the verify command so it would fail on a plausible half-finished
attempt, not merely on an empty directory.

## Known limits

- macOS-specific (`stat -f`, Homebrew paths).
- One worker pane at a time; stages are sequential because the pipeline is.
- The orchestrator still has to read what the worker actually concluded. The
  harness guarantees a stage *ran and produced artifacts* — it cannot tell you
  the meta-analysis is any good.
