#!/usr/bin/env python3
"""Build the demo manifest for the meta-pipe web UI.

Scans the bundled example project (``projects/ici-breast-cancer/``) and emits a
self-contained ``demo_manifest.json`` that the static frontend replays stage by
stage. No API keys, no Claude tokens, no live execution -- it simply surfaces the
real artifacts that already live in the repo.

Run from the repo root:

    uv run web/build_demo_manifest.py

Or point it at a different finished project:

    uv run web/build_demo_manifest.py --project projects/your-project
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

# --- helpers ---------------------------------------------------------------


def read_text(path: Path, max_chars: int = 2400) -> str:
    """Read a file, collapse to a preview, never explode if it is missing."""
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace").strip()
    if len(text) > max_chars:
        text = text[:max_chars].rstrip() + "\n\n[... truncated for demo ...]"
    return text


def read_head(path: Path, n_lines: int, max_chars: int = 2400) -> str:
    if not path.exists():
        return ""
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    text = "\n".join(lines[:n_lines]).strip()
    if len(text) > max_chars:
        text = text[:max_chars].rstrip() + "\n[... truncated ...]"
    return text


def extract_screen_prompt(repo: Path) -> str:
    """Pull the real title/abstract screening prompt out of ai_screen.py.

    This is the actual prompt meta-pipe sends to the model. We surface it
    verbatim so the operator can see — and edit — what drives screening.
    """
    src = repo / "tooling/python/ai_screen.py"
    if not src.exists():
        return ""
    text = src.read_text(encoding="utf-8", errors="replace")
    marker = "def screen_one("
    i = text.find(marker)
    if i == -1:
        return ""
    j = text.find('prompt = f"""', i)
    if j == -1:
        return ""
    start = j + len('prompt = f"""')
    end = text.find('"""', start)
    return text[start:end].strip() if end != -1 else ""


def screening_decision_counts(proj: Path) -> dict:
    """Count the three decision columns in the screened CSV.

    In this example Reviewer1, Reviewer2 and the final decision are identical —
    because meta-pipe's `--reviewer 1/2` runs the *same* model and prompt and
    only writes a different column. We surface the real counts so this is
    self-evident rather than asserted.
    """
    import csv as _csv

    f = proj / "03_screening" / "round-01_decisions_ai_screened.csv"
    out = {"columns": ["decision_r1", "decision_r2", "final_decision"], "counts": {}, "total": 0}
    if not f.exists():
        return out
    rows = list(_csv.DictReader(f.open(encoding="utf-8", errors="replace")))
    out["total"] = len(rows)
    for col in out["columns"]:
        c = {"include": 0, "maybe": 0, "exclude": 0}
        for r in rows:
            v = (r.get(col) or "").strip().lower()
            if v in c:
                c[v] += 1
        out["counts"][col] = c
    out["identical"] = len({tuple(sorted(out["counts"][c].items())) for c in out["columns"]}) == 1
    return out


# --- stage definitions -----------------------------------------------------
# Each stage maps a pipeline phase to (a) the human gate that pauses it and
# (b) the real artifacts produced. The gates are not glossed over: the UI makes
# the operator clear each one by hand, so the amount of human input the pipeline
# actually needs is felt rather than narrated.

GATE_NONE = None


def build_stages(proj: Path, repo: Path) -> list[dict]:
    return [
        {
            "id": "00_intake",
            "num": "00",
            "name": "Topic Intake",
            "skill": "/ma-topic-intake",
            "summary": "Operator states the research question; Claude refines PICO and runs a feasibility check.",
            "gate": {
                "type": "input",
                "label": "Research question (text input)",
                "detail": "The pipeline cannot start without a human-supplied topic. In live mode this is a text box; here we replay the real TOPIC.txt.",
            },
            "artifacts": [
                {"name": "TOPIC.txt", "kind": "text", "preview": read_head(proj / "01_protocol/TOPIC.txt", 24)},
            ],
            "metrics": [],
        },
        {
            "id": "01_protocol",
            "num": "01",
            "name": "Protocol & PROSPERO",
            "skill": "/ma-search-bibliography",
            "summary": "PICO formalised to pico.yaml, eligibility criteria and the PROSPERO registration draft.",
            "gate": {
                "type": "human-action",
                "label": "PROSPERO registration (off-platform)",
                "detail": "Registering the protocol on PROSPERO is a manual human action on an external website -- a web UI can draft it but cannot complete it.",
            },
            "artifacts": [
                {"name": "pico.yaml", "kind": "code", "preview": read_head(proj / "01_protocol/pico.yaml", 35)},
                {"name": "prospero_registration.md", "kind": "text", "preview": read_head(proj / "01_protocol/prospero_registration.md", 30)},
            ],
            "metrics": [],
        },
        {
            "id": "02_search",
            "num": "02",
            "name": "Search & Dedupe",
            "skill": "/ma-search-bibliography",
            "summary": "Database search (PubMed/MEDLINE) executed via API, results deduplicated to a clean .bib.",
            "gate": GATE_NONE,
            "artifacts": [
                {"name": "SEARCH_COMPLETION_REPORT.md", "kind": "text", "preview": read_head(proj / "02_search/SEARCH_COMPLETION_REPORT.md", 30)},
                {"name": "round-01_pubmed_log.md", "kind": "text", "preview": read_text(proj / "02_search/round-01_pubmed_log.md", 1200)},
            ],
            "metrics": [{"label": "Records identified", "value": "122"}, {"label": "Source", "value": "PubMed/MEDLINE"}],
        },
        {
            "id": "03_screening",
            "num": "03",
            "name": "Title/Abstract Screening",
            "skill": "/ma-screening-quality",
            "summary": "Records are screened against PICO by an LLM. meta-pipe labels this dual-review; the configuration below shows exactly how the two reviewer columns are produced.",
            "gate": {
                "type": "decision",
                "label": "Confirm analysis type: pairwise vs network meta-analysis",
                "detail": "A genuine fork that changes every downstream stage. The operator must choose -- the pipeline pauses here for a yes/no decision.",
            },
            # The real LLM configuration, surfaced verbatim and made editable so
            # the operator can see what actually drives screening.
            "llm": {
                "source": "tooling/python/ai_screen.py",
                "model": "claude -p --model haiku",
                "prompt": extract_screen_prompt(repo),
                "reviewer_mechanism": (
                    "`--reviewer 1` and `--reviewer 2` call the same model with the same prompt and only "
                    "write a different CSV column (Reviewer1_Decision / Reviewer2_Decision). The script even "
                    "prints: \"run with --reviewer 2 for dual review, or have a human fill Reviewer2 columns.\""
                ),
                "decisions": screening_decision_counts(proj),
            },
            "artifacts": [
                {"name": "AI_SCREENING_REPORT.md", "kind": "text", "preview": read_head(proj / "03_screening/AI_SCREENING_REPORT.md", 28)},
            ],
            "metrics": [
                {"label": "Screened", "value": "122"},
                {"label": "Excluded", "value": "117"},
                {"label": "To full-text", "value": "5"},
            ],
        },
        {
            "id": "04_fulltext",
            "num": "04",
            "name": "Full-text Retrieval & Eligibility",
            "skill": "/ma-fulltext-management",
            "summary": "Open-access PDFs fetched automatically (Unpaywall); paywalled PDFs must be uploaded by the operator.",
            "gate": {
                "type": "upload",
                "label": "Upload paywalled full-text PDFs",
                "detail": "The single most common upload point. Automated retrieval covers OA papers; the rest require a human to supply the PDF. In live mode this is a file-drop box.",
            },
            "artifacts": [
                {"name": "round-01_include_list.txt", "kind": "text", "preview": read_head(proj / "04_fulltext/round-01_include_list.txt", 12)},
                {"name": "PHASE4_SUMMARY.md", "kind": "text", "preview": read_head(proj / "04_fulltext/PHASE4_SUMMARY.md", 26)},
            ],
            "metrics": [{"label": "Full-text sought", "value": "5"}, {"label": "Retrieved", "value": "5"}, {"label": "Included", "value": "5"}],
        },
        {
            "id": "05_extraction",
            "num": "05",
            "name": "Data Extraction & RoB",
            "skill": "/ma-data-extraction",
            "summary": "Structured outcome data + risk-of-bias assessment. Low-confidence fields flagged for human review.",
            "gate": {
                "type": "review",
                "label": "Verify extracted data & risk-of-bias judgements",
                "detail": "AI proposes; a human confirms. Numbers feeding the meta-analysis must be checked -- the pipeline pauses for operator sign-off.",
            },
            "artifacts": [
                {"name": "round-01_extraction.csv", "kind": "table", "preview": read_text(proj / "05_extraction/round-01_extraction.csv", 1800)},
                {"name": "round-01_QUICK_STATS.md", "kind": "text", "preview": read_head(proj / "05_extraction/round-01_QUICK_STATS.md", 24)},
            ],
            "metrics": [{"label": "Trials", "value": "5"}, {"label": "Patients", "value": "2,402"}],
        },
        {
            "id": "06_analysis",
            "num": "06",
            "name": "Meta-Analysis (R)",
            "skill": "/ma-meta-analysis",
            "summary": "Random-effects pooling in R (meta/metafor): forest plots, subgroup and sensitivity analyses.",
            "gate": GATE_NONE,
            "artifacts": [
                {"name": "tables_pCR_meta_analysis_results.csv", "kind": "table", "preview": read_text(proj / "06_analysis/tables_pCR_meta_analysis_results.csv", 1200)},
                {"name": "tables_safety_meta_analysis_summary.csv", "kind": "table", "preview": read_text(proj / "06_analysis/tables_safety_meta_analysis_summary.csv", 800)},
                {"name": "tables_PDL1_subgroup_comparison.csv", "kind": "table", "preview": read_text(proj / "06_analysis/tables_PDL1_subgroup_comparison.csv", 600)},
            ],
            "metrics": [
                {"label": "pCR RR", "value": "1.26 (1.16–1.37)"},
                {"label": "EFS HR", "value": "0.66 (0.51–0.86)"},
                {"label": "I²", "value": "0%"},
            ],
        },
        {
            "id": "07_manuscript",
            "num": "07",
            "name": "Manuscript (Quarto)",
            "skill": "/ma-manuscript-quarto",
            "summary": "Sections, tables, figures and references assembled and rendered to a journal-ready manuscript.",
            "gate": GATE_NONE,
            "artifacts": [
                {"name": "00_abstract.md", "kind": "text", "preview": read_text(proj / "07_manuscript/00_abstract.md", 2400)},
            ],
            "metrics": [{"label": "Word count", "value": "~4,900"}, {"label": "Tables", "value": "3 + 4 supp."}],
        },
        {
            "id": "08_grade",
            "num": "08",
            "name": "GRADE & Peer Review",
            "skill": "/ma-peer-review",
            "summary": "GRADE certainty assessment and Summary-of-Findings table; internal peer-review pass.",
            "gate": {
                "type": "review",
                "label": "Confirm GRADE certainty judgements",
                "detail": "GRADE downgrade/upgrade decisions are judgement calls a human must endorse.",
            },
            "artifacts": [
                {"name": "SupplementaryTable4_GRADE_Profile.md", "kind": "text", "preview": read_head(proj / "07_manuscript/tables/SupplementaryTable4_GRADE_Profile.md", 30)},
            ],
            "metrics": [{"label": "Primary outcome certainty", "value": "⊕⊕⊕⊕ HIGH"}],
        },
        {
            "id": "09_qa",
            "num": "09",
            "name": "QA & Submission Prep",
            "skill": "/ma-publication-quality",
            "summary": "Overclaim audit, DOI verification, PRISMA completeness, final readiness check.",
            "gate": GATE_NONE,
            "artifacts": [
                {"name": "doi_verification_report.md", "kind": "text", "preview": read_text(proj / "09_qa/doi_verification_report.md", 1600)},
            ],
            "metrics": [{"label": "Status", "value": "99% complete"}],
        },
    ]


def main() -> None:
    ap = argparse.ArgumentParser(description="Build demo_manifest.json for the meta-pipe web UI")
    ap.add_argument("--project", default="projects/ici-breast-cancer", help="finished project to replay")
    ap.add_argument("--repo-root", default=str(Path(__file__).resolve().parent.parent), help="meta-pipe repo root")
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    proj = (repo / args.project).resolve()
    web = repo / "web"
    assets = web / "static" / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    if not proj.exists():
        raise SystemExit(f"project not found: {proj}")

    # Copy display assets (PRISMA flow) into the static tree so the site is self-contained.
    prisma_src = proj / "figures/prisma_flow_static.svg"
    if prisma_src.exists():
        shutil.copy2(prisma_src, assets / "prisma_flow_static.svg")

    manifest = {
        "project": {
            "name": proj.name,
            "title": "Neoadjuvant Immunotherapy + Chemotherapy vs Chemotherapy Alone for Early TNBC",
            "subtitle": "A systematic review & meta-analysis of randomized controlled trials",
            "headline": [
                {"label": "RCTs", "value": "5"},
                {"label": "Patients", "value": "2,402"},
                {"label": "pCR RR", "value": "1.26 (1.16–1.37)"},
                {"label": "Certainty", "value": "⊕⊕⊕⊕ HIGH"},
            ],
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        },
        "stages": build_stages(proj, repo),
        "output": {
            "prisma_svg": "assets/prisma_flow_static.svg" if prisma_src.exists() else "",
            "abstract": read_text(proj / "07_manuscript/00_abstract.md", 3000),
            "downloads": [
                {"label": "manuscript.pdf", "note": "rendered in live mode via Quarto"},
                {"label": "PRISMA 2020 flow diagram", "note": "shown above"},
                {"label": "forest plots + SoF table", "note": "produced by stage 06 / 08"},
            ],
        },
    }

    out = web / "static" / "demo_manifest.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size:,} bytes, {len(manifest['stages'])} stages)")


if __name__ == "__main__":
    main()
