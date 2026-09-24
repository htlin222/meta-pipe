#!/usr/bin/env python3
"""Optional web frontend for meta-pipe.

Two modes, one app:

* **demo** (default) — replays the bundled ``ici-breast-cancer`` example from a
  pre-built ``demo_manifest.json``. No API key, no execution, no cost. This is
  what is deployed for the public showcase.

* **live** — drives the real pipeline. Each stage shells out to headless Claude
  (``claude -p``) inside the project directory, and progress is read back from
  ``tooling/python/project_status.py``. Because this runs Claude head-less rather
  than via an interactive Claude Code subscription, **it bills against the Claude
  API** (set ``ANTHROPIC_API_KEY``). meta-pipe's own ``.env`` convention applies;
  this app intentionally does NOT add an API-key configuration page.

Run:

    uv run web/server.py                       # demo mode
    MP_MODE=live MP_PROJECT=projects/my-ma \\
        ANTHROPIC_API_KEY=sk-... uv run web/server.py

Dependencies: ``fastapi`` and ``uvicorn`` (``uv add fastapi uvicorn``).
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

WEB = Path(__file__).resolve().parent
REPO = WEB.parent
STATIC = WEB / "static"

MODE = os.environ.get("MP_MODE", "demo").lower()
PROJECT = os.environ.get("MP_PROJECT", "projects/ici-breast-cancer")

# Stage -> the documented skill command (see AGENTS.md). Live mode hands these
# to headless Claude one at a time, pausing at the human gates the UI surfaces.
STAGE_COMMANDS = {
    "00_intake": "Use the ma-topic-intake skill to refine TOPIC.txt and run a feasibility check",
    "01_protocol": "Use the ma-search-bibliography skill to produce pico.yaml, eligibility and the PROSPERO draft",
    "02_search": "Use the ma-search-bibliography skill to run the database search and dedupe to a .bib",
    "03_screening": "Use the ma-screening-quality skill for dual title/abstract screening and report agreement",
    "04_fulltext": "Use the ma-fulltext-management skill to retrieve full text and screen eligibility",
    "05_extraction": "Use the ma-data-extraction skill to extract outcome data and assess risk of bias",
    "06_analysis": "Use the ma-meta-analysis skill to run the R meta-analysis scripts",
    "07_manuscript": "Use the ma-manuscript-quarto skill to assemble and render the manuscript",
    "08_grade": "Use the ma-peer-review skill for GRADE assessment and the SoF table",
    "09_qa": "Use the ma-publication-quality skill for the QA and overclaim audit",
}

app = FastAPI(title="meta-pipe web", docs_url=None, redoc_url=None)


@app.get("/api/mode")
def get_mode() -> dict:
    return {"mode": MODE, "project": PROJECT if MODE == "live" else None}


@app.get("/api/manifest")
def get_manifest() -> JSONResponse:
    """Demo: serve the pre-built replay. Live: project status in the same shape."""
    if MODE == "demo":
        f = STATIC / "demo_manifest.json"
        if not f.exists():
            raise HTTPException(500, "demo_manifest.json missing — run web/build_demo_manifest.py")
        return JSONResponse(json.loads(f.read_text(encoding="utf-8")))
    return JSONResponse(_live_status())


def _live_status() -> dict:
    """Read live project status via tooling/python/project_status.py."""
    proj = (REPO / PROJECT).resolve()
    if not proj.exists():
        raise HTTPException(404, f"project not found: {PROJECT}")
    out = subprocess.run(
        ["uv", "run", "tooling/python/project_status.py", "--project", str(proj), "--json"],
        cwd=REPO, capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise HTTPException(500, f"project_status failed: {out.stderr[:400]}")
    try:
        return json.loads(out.stdout)
    except json.JSONDecodeError:
        # project_status may print a human report; fall back to a minimal shape.
        return {"project": {"name": proj.name}, "raw": out.stdout[:2000]}


@app.post("/api/stage/{stage_id}/run")
def run_stage(stage_id: str):
    """Live mode only: drive one stage with headless Claude, streaming its output."""
    if MODE != "live":
        raise HTTPException(400, "stage execution is only available in live mode")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise HTTPException(400, "ANTHROPIC_API_KEY not set — live mode bills against the Claude API")
    cmd = STAGE_COMMANDS.get(stage_id)
    if not cmd:
        raise HTTPException(404, f"unknown stage: {stage_id}")
    proj = (REPO / PROJECT).resolve()

    def stream():
        proc = subprocess.Popen(
            ["claude", "-p", cmd, "--output-format", "stream-json", "--verbose"],
            cwd=proj, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1,
        )
        assert proc.stdout is not None
        for line in proc.stdout:
            yield f"data: {line.rstrip()}\n\n"
        proc.wait()
        yield f"event: done\ndata: {{\"code\": {proc.returncode}}}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


# Static assets (css/js/manifest/svg). Mounted last so /api/* wins.
app.mount("/", StaticFiles(directory=str(STATIC), html=True), name="static")


if __name__ == "__main__":
    import uvicorn

    host = os.environ.get("MP_HOST", "127.0.0.1")
    port = int(os.environ.get("MP_PORT", "8000"))
    print(f"meta-pipe web · mode={MODE} · http://{host}:{port}")
    if MODE == "live":
        print(f"  project={PROJECT}  (live mode bills against ANTHROPIC_API_KEY)")
    uvicorn.run(app, host=host, port=port)
