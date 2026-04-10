#!/usr/bin/env python3
"""Validate that all checklists are complete.

In ``draft`` quality mode (set via ``init_project.py --mode draft``, read
from ``.ma_meta.json``) unchecked items and missing artifacts are surfaced
as NOTES instead of FAILURES. Draft runs intentionally skip full dual
review, PROSPERO, etc., so treating those deviations as hard failures
would defeat the purpose of the mode.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# Import project_meta from tooling/python/ — it lives outside this script's
# directory, so extend sys.path at import time.
_TOOLING = Path(__file__).resolve().parents[2] / "tooling" / "python"
if str(_TOOLING) not in sys.path:
    sys.path.insert(0, str(_TOOLING))

try:
    from project_meta import get_quality_mode  # type: ignore
except ImportError:  # pragma: no cover — fallback if tooling missing
    def get_quality_mode(_: Path) -> str:
        return "strict"


CHECKLISTS = [
    "01_protocol/CHECKLIST.md",
    "02_search/CHECKLIST.md",
    "03_screening/CHECKLIST.md",
    "04_fulltext/CHECKLIST.md",
    "05_extraction/CHECKLIST.md",
    "06_analysis/CHECKLIST.md",
    "07_manuscript/CHECKLIST.md",
    "08_reviews/CHECKLIST.md",
    "09_qa/CHECKLIST.md",
]

UNCHECKED_RE = re.compile(r"^\s*-\s*\[\s*\]\s+", re.IGNORECASE)


def validate(root: Path) -> tuple[bool, list[str]]:
    issues: list[str] = []
    for rel in CHECKLISTS:
        path = root / rel
        if not path.exists():
            issues.append(f"Missing checklist: {rel}")
            continue
        lines = path.read_text().splitlines()
        for line in lines:
            if UNCHECKED_RE.match(line):
                issues.append(f"Unchecked: {rel} :: {line.strip()}")

    search_dir = root / "02_search"
    audit_files = list(search_dir.glob("round-*/search_audit.json")) if search_dir.exists() else []
    if not audit_files:
        issues.append("Missing search audit: 02_search/round-XX/search_audit.json")

    return (len(issues) == 0, issues)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate pipeline checklists.")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of human text.",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    mode = get_quality_mode(root)
    ok, issues = validate(root)

    if args.json:
        print(
            json.dumps(
                {"mode": mode, "passed": ok, "issues": issues},
                indent=2,
            )
        )
        # Draft mode always exits 0 on JSON output — the caller can inspect
        # the issues list directly.
        if mode == "draft":
            return
        raise SystemExit(0 if ok else 2)

    if mode == "draft":
        if ok:
            print("[draft] All checklists completed.")
            return
        print(
            "[draft] Pipeline has unchecked items. These are NOTES in "
            "draft mode, not failures — re-run in strict mode before "
            "submission."
        )
        for issue in issues:
            print(f"  note: {issue}")
        return

    if not ok:
        print("Checklist validation failed:")
        for issue in issues:
            print(f"- {issue}")
        raise SystemExit(2)
    print("All checklists completed.")


if __name__ == "__main__":
    main()
