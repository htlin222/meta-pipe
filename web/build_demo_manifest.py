#!/usr/bin/env python3
"""Build the demo manifest for the meta-pipe web UI.

Scans the bundled example project (``projects/ici-breast-cancer/``) and emits a
self-contained ``demo_manifest.json`` that the static frontend replays stage by
stage. No API keys, no Claude tokens, no live execution -- it surfaces the real
artifacts that already live in the repo.

The gates are grounded in meta-pipe's own program and documentation, in three
classes:

* **prep**    -- things the researcher must prepare BEFORE running (environment,
                 API keys, TOPIC.txt, the hand-written search strategy, and the
                 PROSPERO registration the researcher does themselves).
* **program** -- pauses/checkpoints that exist in meta-pipe today; each carries a
                 ``basis`` pointing at where in the repo it comes from.
* **suggested** (separate ``suggestions.json``, only emitted with
                 ``--with-suggestions``) -- gates meta-pipe does NOT have that we
                 would add, each with a ``why``. These are our opinion and are
                 kept OFF the upstream PR.

Run from the repo root:

    uv run web/build_demo_manifest.py                    # PR build (no suggestions)
    uv run web/build_demo_manifest.py --with-suggestions # our deploy build
"""

from __future__ import annotations

import argparse
import csv as _csv
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

# --- helpers ---------------------------------------------------------------


def read_text(path: Path, max_chars: int = 2400) -> str:
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
    """Pull the real title/abstract screening prompt out of ai_screen.py."""
    src = repo / "tooling/python/ai_screen.py"
    if not src.exists():
        return ""
    text = src.read_text(encoding="utf-8", errors="replace")
    i = text.find("def screen_one(")
    if i == -1:
        return ""
    j = text.find('prompt = f"""', i)
    if j == -1:
        return ""
    start = j + len('prompt = f"""')
    end = text.find('"""', start)
    return text[start:end].strip() if end != -1 else ""


def screening_decision_counts(proj: Path) -> dict:
    """Count the three decision columns; in this example they are identical."""
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


# --- pre-run preparation ----------------------------------------------------
# Files / actions the researcher must have ready before meta-pipe runs at all.


def build_prep() -> list[dict]:
    return [
        {
            "title": "Toolchain installed",
            "detail": "uv (Python), R ≥ 4.2 + renv, Quarto, cmake. One-time `bash setup.sh`.",
            "basis": "README §Requirements, setup.sh",
            "required": True,
        },
        {
            "title": "API keys in .env",
            "detail": "PubMed key is required; Scopus/Embase, Cochrane, Zotero and an Unpaywall email are optional.",
            "basis": ".env.example",
            "required": True,
        },
        {
            "title": "Research question → TOPIC.txt",
            "detail": "You write the question into projects/<name>/TOPIC.txt; the pipeline cannot start without it.",
            "basis": "init_project.py, AGENTS.md",
            "required": True,
        },
        {
            "title": "Search strategy → queries.txt",
            "detail": "You translate PICO into a database Boolean query by hand and save it as queries.txt (a MeSH-expand helper exists, but the strategy is yours).",
            "basis": "ma-search-bibliography/SKILL.md Step 1",
            "required": True,
        },
        {
            "title": "PROSPERO registration (you do this yourself)",
            "detail": "meta-pipe drafts prospero_registration.md but does not register it. The author's position is that registration is out of scope for the tool — the researcher registers the protocol on PROSPERO themselves before running. We list it here as a real pre-run gate.",
            "basis": "author's stance; prospero_registration.md is a draft only",
            "required": True,
        },
    ]


# --- in-pipeline gates that exist in meta-pipe today ------------------------
# Each gate: type drives the UI control; kind="program"; basis = where it lives.


def G(type_, label, detail, basis):
    return {"type": type_, "kind": "program", "label": label, "detail": detail, "basis": basis}


def build_stages(proj: Path, repo: Path) -> list[dict]:
    return [
        {
            "id": "00_intake", "num": "00", "name": "Topic Intake", "skill": "/ma-topic-intake",
            "summary": "With TOPIC.txt in place, Claude refines the PICO and runs a feasibility assessment.",
            "gates": [
                G("approval", "Feasibility assessment (mandatory first step)",
                  "meta-pipe requires a ~4-hour feasibility assessment before any protocol writing or extraction. The operator confirms it passed.",
                  "AGENTS.md §'When User Says Start' (MANDATORY FIRST STEP)"),
            ],
            "artifacts": [{"name": "TOPIC.txt", "kind": "text", "preview": read_head(proj / "01_protocol/TOPIC.txt", 24)}],
            "metrics": [],
        },
        {
            "id": "01_protocol", "num": "01", "name": "Protocol", "skill": "/ma-search-bibliography",
            "summary": "PICO formalised to pico.yaml with eligibility criteria. (PROSPERO is a pre-run prep gate, not a step here.)",
            "gates": [],
            "artifacts": [{"name": "pico.yaml", "kind": "code", "preview": read_head(proj / "01_protocol/pico.yaml", 35)}],
            "metrics": [],
        },
        {
            "id": "02_search", "num": "02", "name": "Search & Dedupe", "skill": "/ma-search-bibliography",
            "summary": "Your queries.txt is run against the database(s) and results are exported to a versioned .bib.",
            "gates": [],
            "artifacts": [
                {"name": "SEARCH_COMPLETION_REPORT.md", "kind": "text", "preview": read_head(proj / "02_search/SEARCH_COMPLETION_REPORT.md", 30)},
                {"name": "round-01_pubmed_log.md", "kind": "text", "preview": read_text(proj / "02_search/round-01_pubmed_log.md", 1200)},
            ],
            "metrics": [{"label": "Records identified", "value": "122"}, {"label": "Source", "value": "PubMed/MEDLINE"}],
        },
        {
            "id": "03_screening", "num": "03", "name": "Title/Abstract Screening", "skill": "/ma-screening-quality",
            "summary": "Records are screened against PICO by an LLM. The configuration below shows exactly how the two reviewer columns are produced.",
            "gates": [
                G("checkpoint", "Inter-reviewer agreement κ ≥ 0.60 before Stage 04",
                  "meta-pipe gates the 03→04 transition on Cohen's κ. In this finished example the threshold is treated as met.",
                  "ma-end-to-end/SKILL.md §Quality Gates"),
                G("decision", "Confirm analysis type: pairwise vs network",
                  "A genuine fork that changes every downstream stage; meta-pipe names this the Analysis Type Confirmation Gate (Step 8).",
                  "AGENTS.md row 03b; ma-screening-quality/SKILL.md Step 8"),
            ],
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
            "artifacts": [{"name": "AI_SCREENING_REPORT.md", "kind": "text", "preview": read_head(proj / "03_screening/AI_SCREENING_REPORT.md", 28)}],
            "metrics": [{"label": "Screened", "value": "122"}, {"label": "Excluded", "value": "117"}, {"label": "To full-text", "value": "5"}],
        },
        {
            "id": "04_fulltext", "num": "04", "name": "Full-text Retrieval & Eligibility", "skill": "/ma-fulltext-management",
            "summary": "Open-access PDFs are fetched for low-confidence studies via Unpaywall; paywalled PDFs the operator must supply.",
            "gates": [
                G("upload", "Supply paywalled full-text PDFs",
                  "meta-pipe retrieves OA PDFs automatically, but flagged/paywalled studies need the operator to place the PDF in 04_fulltext/. The interface adds an upload box for exactly that step.",
                  "ma-fulltext-management/SKILL.md Phase 2 (Targeted PDF Retrieval)"),
                G("checkpoint", "Full-text screening κ ≥ 0.60 before Stage 05",
                  "The 04→05 transition is gated on full-text screening agreement.",
                  "ma-end-to-end/SKILL.md §Quality Gates"),
            ],
            "artifacts": [
                {"name": "round-01_include_list.txt", "kind": "text", "preview": read_head(proj / "04_fulltext/round-01_include_list.txt", 12)},
                {"name": "PHASE4_SUMMARY.md", "kind": "text", "preview": read_head(proj / "04_fulltext/PHASE4_SUMMARY.md", 26)},
            ],
            "metrics": [{"label": "Full-text sought", "value": "5"}, {"label": "Included", "value": "5"}],
        },
        {
            "id": "05_extraction", "num": "05", "name": "Data Extraction & RoB", "skill": "/ma-data-extraction",
            "summary": "Structured outcome data are extracted; low-confidence fields are flagged. (A risk-of-bias schema is defined in pico.yaml.)",
            "gates": [
                G("checkpoint", "Extraction completeness — all included studies extracted",
                  "meta-pipe gates the 05→06 transition on extraction completeness.",
                  "ma-end-to-end/SKILL.md §Quality Gates"),
            ],
            "artifacts": [
                {"name": "round-01_extraction.csv", "kind": "table", "preview": read_text(proj / "05_extraction/round-01_extraction.csv", 1800)},
                {"name": "round-01_QUICK_STATS.md", "kind": "text", "preview": read_head(proj / "05_extraction/round-01_QUICK_STATS.md", 24)},
            ],
            "metrics": [{"label": "Trials", "value": "5"}, {"label": "Patients", "value": "2,402"}],
        },
        {
            "id": "06_analysis", "num": "06", "name": "Meta-Analysis (R)", "skill": "/ma-meta-analysis",
            "summary": "Random-effects pooling in R (meta/metafor): forest plots, subgroup and sensitivity analyses.",
            "gates": [
                G("checkpoint", "All figures ≥ 300 DPI before Stage 07",
                  "The 06→07 transition is gated on figure resolution.",
                  "ma-end-to-end/SKILL.md §Quality Gates"),
            ],
            "artifacts": [
                {"name": "tables_pCR_meta_analysis_results.csv", "kind": "table", "preview": read_text(proj / "06_analysis/tables_pCR_meta_analysis_results.csv", 1200)},
                {"name": "tables_safety_meta_analysis_summary.csv", "kind": "table", "preview": read_text(proj / "06_analysis/tables_safety_meta_analysis_summary.csv", 800)},
            ],
            "metrics": [{"label": "pCR RR", "value": "1.26 (1.16–1.37)"}, {"label": "EFS HR", "value": "0.66 (0.51–0.86)"}, {"label": "I²", "value": "0%"}],
        },
        {
            "id": "07_manuscript", "num": "07", "name": "Manuscript (Quarto)", "skill": "/ma-manuscript-quarto",
            "summary": "Sections, tables, figures and references are assembled and rendered.",
            "gates": [
                G("approval", "Approve the manuscript outline before any writing",
                  "meta-pipe makes Phase 1 (outline + checklist) mandatory and requires operator approval before a single section is written.",
                  "ma-manuscript-quarto/SKILL.md Phase 1 (MANDATORY before any writing)"),
            ],
            "artifacts": [{"name": "00_abstract.md", "kind": "text", "preview": read_text(proj / "07_manuscript/00_abstract.md", 2400)}],
            "metrics": [{"label": "Word count", "value": "~4,900"}, {"label": "Tables", "value": "3 + 4 supp."}],
        },
        {
            "id": "08_grade", "num": "08", "name": "GRADE & Peer Review", "skill": "/ma-peer-review",
            "summary": "GRADE certainty assessment and Summary-of-Findings table are written into the manuscript supplement.",
            "gates": [],
            "artifacts": [{"name": "SupplementaryTable4_GRADE_Profile.md", "kind": "text", "preview": read_head(proj / "07_manuscript/tables/SupplementaryTable4_GRADE_Profile.md", 30)}],
            "metrics": [{"label": "Primary outcome certainty", "value": "⊕⊕⊕⊕ HIGH"}],
        },
        {
            "id": "09_qa", "num": "09", "name": "QA & Submission Prep", "skill": "/ma-publication-quality",
            "summary": "Overclaim audit, DOI verification, PRISMA completeness and a final readiness score.",
            "gates": [
                G("checkpoint", "PRISMA 27/27 + publication readiness ≥ 95%",
                  "The final gate: validate_pipeline.py / final_qa_report.py block on failures.",
                  "ma-end-to-end/SKILL.md §Resources; ma-publication-quality/SKILL.md"),
            ],
            "artifacts": [{"name": "doi_verification_report.md", "kind": "text", "preview": read_text(proj / "09_qa/doi_verification_report.md", 1600)}],
            "metrics": [{"label": "Status", "value": "99% complete"}],
        },
    ]


# --- our suggestions (NOT shipped in the PR) -------------------------------
# Gates meta-pipe does NOT have that we would add, each with a rationale.


def build_suggestions() -> list[dict]:
    return [
        {
            "title": "Two genuinely independent reviewers + conflict resolution",
            "where": "Screening (Stage 03)",
            "why": "meta-pipe's `--reviewer 1/2` runs one model with one prompt and writes two columns; in the example decision_r1 = decision_r2 = final (all 27/63/32). Cochrane Handbook §6.4 expects two independent reviewers and a recorded conflict-resolution step.",
        },
        {
            "title": "Multi-database search + cross-source de-duplication",
            "where": "Search (Stage 02)",
            "why": "The example searched only PubMed (122 records) and the dedupe step is a no-op. Cochrane Handbook §4.4 expects at least MEDLINE + Embase + CENTRAL.",
        },
        {
            "title": "Risk-of-bias assessment as an enforced gate",
            "where": "Extraction / RoB (Stage 05)",
            "why": "pico.yaml defines a RoB 2 schema, but no per-study × domain assessment is required before analysis runs. We would gate Stage 06 on a completed RoB matrix.",
        },
        {
            "title": "GRADE certainty sign-off gate",
            "where": "GRADE (Stage 08)",
            "why": "GRADE certainty is hand-written with no gate. Downgrade/upgrade judgements should be confirmed before any publication-quality certainty claim is made.",
        },
        {
            "title": "Search-strategy builder & ≥ 2-database validator",
            "where": "Search prep",
            "why": "queries.txt is authored entirely by hand (only a MeSH-expand helper exists). Nothing validates database coverage or strategy completeness before the search runs.",
        },
    ]


def main() -> None:
    ap = argparse.ArgumentParser(description="Build demo_manifest.json for the meta-pipe web UI")
    ap.add_argument("--project", default="projects/ici-breast-cancer", help="finished project to replay")
    ap.add_argument("--repo-root", default=str(Path(__file__).resolve().parent.parent), help="meta-pipe repo root")
    ap.add_argument("--with-suggestions", action="store_true",
                    help="also emit suggestions.json (our opinion; keep OFF the upstream PR)")
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    proj = (repo / args.project).resolve()
    web = repo / "web"
    static = web / "static"
    assets = static / "assets"
    assets.mkdir(parents=True, exist_ok=True)

    if not proj.exists():
        raise SystemExit(f"project not found: {proj}")

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
        "prep": build_prep(),
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

    out = static / "demo_manifest.json"
    out.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    msg = f"wrote {out.name} ({out.stat().st_size:,} bytes, {len(manifest['stages'])} stages, {len(manifest['prep'])} prep gates)"

    sug = static / "suggestions.json"
    if args.with_suggestions:
        sug.write_text(json.dumps({"suggestions": build_suggestions()}, indent=2, ensure_ascii=False), encoding="utf-8")
        msg += f"; wrote {sug.name} ({len(build_suggestions())} suggestions)"
    else:
        # Keep the PR build clean: never leave a stale suggestions.json behind.
        if sug.exists():
            sug.unlink()
        msg += "; suggestions.json omitted (PR build)"
    print(msg)


if __name__ == "__main__":
    main()
