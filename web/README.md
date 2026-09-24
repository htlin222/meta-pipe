# meta-pipe · optional web frontend

A small, dependency-light web UI for the pipeline. It is **additive and
opt-in** — it does not touch any `ma-*/SKILL.md`, the CLI workflow, or the
subscription-based Claude Code experience. If you ignore this directory,
nothing changes.

It exists to answer one question visually: *what does meta-pipe look like as a
website?* The answer is a **thin shell** — the pipeline walks stage by stage and
**pauses wherever a human operator must step in** (type a topic, upload a
paywalled PDF, confirm pairwise-vs-network, sign off on extraction/GRADE). Those
pauses are the point, and the UI makes them prominent.

The UI is **bilingual (English / 繁體中文)** via a header toggle. Narrative text
is bilingual in the manifest; code, file paths, `basis` lines, prompts and
medical values stay in English.

## Two modes

| Mode | What it does | Cost |
| ---- | ------------ | ---- |
| **demo** (default) | Replays the bundled `projects/ici-breast-cancer/` example from a pre-built `demo_manifest.json`. No execution. | none |
| **live** | Drives the real pipeline: each stage shells out to headless `claude -p` in the project dir; progress is read from `tooling/python/project_status.py`. | **Claude API** — see below |

> **Billing note.** Running meta-pipe as a website means stages execute via
> *headless* Claude, which bills against the **Claude API**
> (`ANTHROPIC_API_KEY`), not an interactive Claude Code subscription. This
> frontend deliberately does **not** add an API-key configuration page — it
> follows meta-pipe's existing `.env` convention.

## Gates

The UI does not gloss over the operator's work. Gates come in two classes, both
grounded in meta-pipe's own program:

- **Pre-run preparation** — what the researcher must have ready before the
  pipeline starts: toolchain, `.env` keys, `TOPIC.txt`, the hand-written
  `queries.txt` search strategy, and **PROSPERO registration** (meta-pipe drafts
  it but does not register — the researcher does that themselves; this is the
  author's stated position). The run cannot begin until each is ticked.
- **In-pipeline gates** — pauses/checkpoints that exist in meta-pipe today
  (feasibility, κ ≥ 0.60, the 03b analysis-type confirmation, paywalled-PDF
  supply, extraction completeness, figure DPI, outline approval, PRISMA 27/27).
  Each gate cites its `basis` in the repo so it is verifiable.

`build_demo_manifest.py --with-suggestions` additionally emits a
`suggestions.json` describing gates meta-pipe does **not** have that we would add
(real dual review, multi-database search, RoB/GRADE sign-off, a strategy
validator), each with a rationale. That file is **our opinion and is kept out of
the upstream PR** — the default build omits it.

## Quick start

```bash
# 1. (re)build the demo replay manifest from the bundled example
uv run web/build_demo_manifest.py

# 2a. Serve the static demo with anything — no Python needed
cd web/static && python3 -m http.server 8000

# 2b. …or run the app (also exposes the live-mode API)
uv add fastapi uvicorn
uv run web/server.py                      # demo mode, http://127.0.0.1:8000

# 3. Live mode (drives the real pipeline; bills the Claude API)
MP_MODE=live MP_PROJECT=projects/my-ma \
  ANTHROPIC_API_KEY=sk-... uv run web/server.py
```

## Layout

```
web/
├── build_demo_manifest.py   # scans a finished project -> static/demo_manifest.json
├── server.py                # FastAPI app: demo replay + live orchestration
├── static/                  # the frontend (plain HTML/CSS/JS, no build step)
│   ├── index.html
│   ├── style.css
│   ├── app.js
│   ├── demo_manifest.json   # generated
│   └── assets/              # copied display artifacts (PRISMA flow, …)
└── README.md
```

`web/static/` is fully self-contained, so the demo can be served by any static
host (nginx, GitHub Pages, `python -m http.server`). A public demo built this
way runs at <https://metapipe.nature.edu.kg>.
