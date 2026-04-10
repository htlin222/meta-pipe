#!/usr/bin/env python3
"""Initialize a numbered meta-analysis project tree."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path


VALID_MODES = ("strict", "draft")

MODE_DESCRIPTIONS = {
    "strict": (
        "Full dual-review, PROSPERO protocol, GRADE, PRISMA 27/27, "
        "publication readiness ≥95% — the publication track."
    ),
    "draft": (
        "Fast prototype: single-reviewer screening OK, PROSPERO deferred, "
        "validate_pipeline treats deviations as notes instead of failures. "
        "Outputs are watermarked so a draft run cannot accidentally be "
        "submitted as a publication."
    ),
}


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content)


def write_meta(root: Path, name: str, mode: str) -> None:
    """Write .ma_meta.json — the single source of truth for project mode."""
    meta_path = root / ".ma_meta.json"
    meta = {
        "project_name": name,
        "quality_mode": mode,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "schema_version": 1,
    }
    meta_path.write_text(json.dumps(meta, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Initialize meta-analysis project folders."
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Project name (will be created in projects/<name>/)",
    )
    parser.add_argument(
        "--root", help="Override: specify custom root directory (advanced users only)"
    )
    parser.add_argument(
        "--mode",
        choices=VALID_MODES,
        default="strict",
        help=(
            "Quality mode. 'strict' (default) is the submission track. "
            "'draft' relaxes dual-review/PROSPERO/GRADE gates for fast "
            "prototype runs and watermarks outputs as non-publishable."
        ),
    )
    args = parser.parse_args()

    # Determine project root
    if args.root:
        # Advanced: user specified custom root
        root = Path(args.root).resolve()
    else:
        # Default: create in projects/<name>/
        # Script is in tooling/python/, go up 2 levels to repo root
        script_dir = Path(__file__).resolve().parent
        repo_root = script_dir.parent.parent
        root = repo_root / "projects" / args.name

        if root.exists():
            print(f"⚠️  Project '{args.name}' already exists at: {root}")
            response = input("Continue anyway? [y/N]: ")
            if response.lower() != "y":
                print("Aborted.")
                return

    print(f"📁 Creating project at: {root}")
    print(f"   Mode: {args.mode} — {MODE_DESCRIPTIONS[args.mode]}")

    dirs = [
        "01_protocol",
        "02_search/round-01",
        "03_screening/round-01",
        "04_fulltext",
        "05_extraction",
        "06_analysis/figures",
        "06_analysis/tables",
        "07_manuscript",
        "08_reviews",
        "09_qa",
        "09_qa/checkpoints",
        "tooling/python",
    ]

    for d in dirs:
        (root / d).mkdir(parents=True, exist_ok=True)

    write_if_missing(root / "TOPIC.txt", "<Paste your meta-analysis topic here>\n")

    checklist = """# Pipeline Checklist

- [ ] 01_protocol complete (PICO, eligibility, outcomes, search plan)
- [ ] 02_search round-01 complete (queries, results, dedupe, log)
- [ ] 03_screening round-01 complete (decisions, exclusions, quality, included)
- [ ] 04_fulltext complete (manifest + PDFs)
- [ ] 04b_fulltext_screening complete (fulltext_decisions.csv + ft_agreement.md)
- [ ] 05_extraction complete (db, csv, data dictionary, log)
- [ ] 06_analysis complete (scripts, figures, tables, validation)
- [ ] 07_manuscript complete (IMRaD + renders)
- [ ] 08_reviews complete (reviewer1, reviewer2, action items)
"""
    write_if_missing(root / "09_qa" / "pipeline-checklist.md", checklist)

    write_meta(root, args.name, args.mode)

    if args.mode == "draft":
        draft_notice = (
            "# DRAFT MODE\n\n"
            "This project was initialized with `--mode draft`.\n\n"
            "What that means:\n"
            "- Single-reviewer screening is permitted\n"
            "- PROSPERO registration is deferred (a TODO is acceptable)\n"
            "- validate_pipeline.py reports unchecked items as NOTES, not FAILURES\n"
            "- Rendered manuscripts are watermarked 'DRAFT — NOT FOR SUBMISSION'\n\n"
            "**Do not submit this project to a journal without first re-running "
            "in `--mode strict` and clearing every gate.**\n\n"
            "To convert: edit `.ma_meta.json` and set `quality_mode: strict`,\n"
            "then run full dual-review screening, PROSPERO registration, and\n"
            "the complete Stage 08-09 QA sequence.\n"
        )
        write_if_missing(root / "DRAFT_MODE.md", draft_notice)

    print(f"✅ Project initialized at: {root}")
    print(f"\nNext steps:")
    print(f"1. Edit {root}/TOPIC.txt with your research question")
    print(f"2. Launch Claude Code and say: 'Start project {args.name}'")


if __name__ == "__main__":
    main()
