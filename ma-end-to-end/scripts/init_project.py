#!/usr/bin/env python3
"""Initialize a numbered meta-analysis project tree."""

from __future__ import annotations

import argparse
from pathlib import Path


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content)


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
    args = parser.parse_args()

    # Determine project root
    if args.root:
        # Advanced: user specified custom root
        root = Path(args.root).resolve()
    else:
        # Default: create in projects/<name>/
        # Assume script is in ma-end-to-end/scripts/, so go up 2 levels to repo root
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

    print(f"✅ Project initialized at: {root}")
    print(f"\nNext steps:")
    print(f"1. Edit {root}/TOPIC.txt with your research question")
    print(f"2. Launch Claude Code and say: 'Start project {args.name}'")


if __name__ == "__main__":
    main()
