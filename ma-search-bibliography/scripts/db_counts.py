#!/usr/bin/env python3
"""Summarize per-database retrieval counts for PRISMA."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


def parse_count(path: Path) -> int | None:
    if not path.exists():
        return None
    pattern = re.compile(r"^(count|retrieved)\s*:\s*(\d+)")
    for line in path.read_text().splitlines():
        match = pattern.match(line.strip())
        if match:
            return int(match.group(2))
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Create per-database count summaries.")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--round", default="round-01", help="Search round")
    parser.add_argument("--out-csv", default=None, help="Output CSV path")
    parser.add_argument("--out-md", default=None, help="Output Markdown path")
    args = parser.parse_args()

    root = Path(args.root)
    round_dir = root / "02_search" / args.round

    files = {
        "pubmed": round_dir / "log.md",
        "scopus": round_dir / "scopus.log",
        "embase": round_dir / "embase.log",
        "cochrane": round_dir / "cochrane.log",
        "ctgov": round_dir / "ctgov_log.txt",
    }

    rows = []
    total = 0
    for db, path in files.items():
        count = parse_count(path)
        rows.append((db, count if count is not None else "NA", str(path)))
        if isinstance(count, int):
            total += count

    out_csv = Path(args.out_csv) if args.out_csv else round_dir / "db_counts.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["database", "retrieved", "log_path"])
        writer.writerows(rows)
        writer.writerow(["total", total, "-"])

    out_md = Path(args.out_md) if args.out_md else round_dir / "db_counts.md"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Database Retrieval Counts",
        "",
        "| Database | Retrieved |",
        "| --- | --- |",
    ]
    for db, count, _ in rows:
        lines.append(f"| {db} | {count} |")
    lines.append(f"| total | {total} |")
    out_md.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
