#!/usr/bin/env python3
"""Merge sharded ai_screen.py outputs back into one decisions.csv.

`ai_screen.py --shard i/n` writes one file per (reviewer, shard) under
``<round>/shards/``. This script reassembles them into a single
``<round>/decisions.csv`` carrying both reviewers' columns.

It is deliberately strict: screening feeds the PRISMA flow, so a silently
dropped or duplicated record corrupts the published numbers. The merge fails
loudly if the reassembled record set does not exactly equal the input corpus.

Usage:
    uv run tooling/python/merge_screening_shards.py --project <name> [--round round-01]
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from pathlib import Path
from typing import Dict, List

SHARD_RE = re.compile(r"^decisions\.r(?P<rev>\d+)\.shard-(?P<i>\d+)-of-(?P<n>\d+)\.csv$")


def _resolve_meta_pipe_root() -> Path:
    env_root = os.environ.get("MA_PIPE_ROOT")
    root = Path(env_root).resolve() if env_root else Path(__file__).resolve().parent.parent.parent
    assert (root / "projects").is_dir(), f"MA_PIPE_ROOT={root} has no projects/ directory"
    return root


def load_csv(path: Path) -> tuple[List[str], List[Dict[str, str]]]:
    with open(path, "r", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        return list(reader.fieldnames or []), list(reader)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--project", required=True)
    parser.add_argument("--round", default="round-01")
    parser.add_argument(
        "--key", default="RecordID", help="Unique record key column (default: RecordID)"
    )
    parser.add_argument(
        "--out", default=None, help="Output CSV (default: <round>/decisions.csv)"
    )
    args = parser.parse_args()

    root = _resolve_meta_pipe_root()
    project_path = root / "projects" / args.project
    screening_db = project_path / "03_screening" / "screening-database.csv"
    round_dir = project_path / "03_screening" / args.round
    shard_dir = round_dir / "shards"
    out_csv = Path(args.out) if args.out else round_dir / "decisions.csv"

    if not screening_db.exists():
        sys.exit(f"ERROR: {screening_db} not found")
    if not shard_dir.is_dir():
        sys.exit(f"ERROR: {shard_dir} not found — run ai_screen.py --shard first")

    fieldnames, base_records = load_csv(screening_db)
    if args.key not in fieldnames:
        sys.exit(f"ERROR: key column {args.key!r} not in {screening_db}")

    merged: Dict[str, Dict[str, str]] = {r[args.key]: dict(r) for r in base_records}
    if len(merged) != len(base_records):
        sys.exit(
            f"ERROR: {args.key} is not unique in {screening_db} "
            f"({len(base_records)} rows, {len(merged)} distinct keys)"
        )

    # Collect shard files, grouped by reviewer so we can check each reviewer's
    # shard set is complete before trusting the merge.
    by_reviewer: Dict[int, Dict[int, Path]] = {}
    totals: Dict[int, int] = {}
    for path in sorted(shard_dir.glob("decisions.r*.shard-*.csv")):
        m = SHARD_RE.match(path.name)
        if not m:
            print(f"  skipping unrecognised file: {path.name}")
            continue
        rev, i, n = int(m["rev"]), int(m["i"]), int(m["n"])
        by_reviewer.setdefault(rev, {})[i] = path
        totals.setdefault(rev, n)
        if totals[rev] != n:
            sys.exit(f"ERROR: reviewer {rev} has mixed shard totals ({totals[rev]} vs {n})")

    if not by_reviewer:
        sys.exit(f"ERROR: no shard files found in {shard_dir}")

    problems: List[str] = []
    for rev in sorted(by_reviewer):
        n = totals[rev]
        missing = sorted(set(range(1, n + 1)) - set(by_reviewer[rev]))
        if missing:
            problems.append(f"reviewer {rev}: missing shard(s) {missing} of {n}")
    if problems:
        sys.exit("ERROR: incomplete shard set\n  " + "\n  ".join(problems))

    seen_per_reviewer: Dict[int, set] = {}
    for rev in sorted(by_reviewer):
        dcol, rcol = f"Reviewer{rev}_Decision", f"Reviewer{rev}_Reason"
        seen: set = set()
        for i in sorted(by_reviewer[rev]):
            _, rows = load_csv(by_reviewer[rev][i])
            for row in rows:
                key = row.get(args.key, "")
                if key not in merged:
                    sys.exit(f"ERROR: shard row {key!r} not present in {screening_db.name}")
                if key in seen:
                    sys.exit(f"ERROR: record {key!r} appears in more than one shard (reviewer {rev})")
                seen.add(key)
                for col in (dcol, rcol):
                    if row.get(col, "").strip():
                        merged[key][col] = row[col]
                note = row.get("Notes", "").strip()
                if note:
                    existing = merged[key].get("Notes", "").strip()
                    if note not in existing:
                        merged[key]["Notes"] = f"{existing} | {note}".strip(" |")
        seen_per_reviewer[rev] = seen
        print(f"  reviewer {rev}: {len(seen)} records across {totals[rev]} shards")

    # Hard gate: every reviewer must cover the corpus exactly.
    expected = set(merged)
    for rev, seen in seen_per_reviewer.items():
        if seen != expected:
            lost, extra = sorted(expected - seen)[:5], sorted(seen - expected)[:5]
            sys.exit(
                f"ERROR: reviewer {rev} covered {len(seen)} of {len(expected)} records. "
                f"missing e.g. {lost} extra e.g. {extra}"
            )

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for rec in base_records:
            writer.writerow(merged[rec[args.key]])

    _, check = load_csv(out_csv)
    if len(check) != len(base_records):
        sys.exit(f"ERROR: wrote {len(check)} rows, expected {len(base_records)}")

    print(f"\nOK: merged {len(check)} records (input had {len(base_records)}) -> {out_csv}")
    for rev in sorted(by_reviewer):
        col = f"Reviewer{rev}_Decision"
        filled = sum(1 for r in check if r.get(col, "").strip())
        vals: Dict[str, int] = {}
        for r in check:
            v = r.get(col, "").strip().lower()
            if v:
                vals[v] = vals.get(v, 0) + 1
        breakdown = "  ".join(f"{k}={v}" for k, v in sorted(vals.items()))
        print(f"  Reviewer{rev}: {filled}/{len(check)} decided   {breakdown}")


if __name__ == "__main__":
    main()
