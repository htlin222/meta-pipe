#!/usr/bin/env python3
"""Generate a per-database search report with queries and counts."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
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


def read_query(path: Path, section: str) -> str:
    content = path.read_text().splitlines()
    start = None
    for i, line in enumerate(content):
        if line.strip().lower() == f"[{section}]":
            start = i + 1
            break
    if start is None:
        return ""
    query_lines = []
    for line in content[start:]:
        if line.strip().startswith("["):
            break
        if line.strip().startswith("#"):
            continue
        if line.strip():
            query_lines.append(line.strip())
    return " ".join(query_lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate per-DB search report.")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--round", default="round-01", help="Search round")
    parser.add_argument("--queries", default=None, help="queries.txt path")
    parser.add_argument("--out-csv", default=None, help="Output CSV path")
    parser.add_argument("--out-md", default=None, help="Output Markdown path")
    args = parser.parse_args()

    root = Path(args.root)
    round_dir = root / "02_search" / args.round
    queries_path = Path(args.queries) if args.queries else round_dir / "queries.txt"

    logs = {
        "pubmed": round_dir / "log.md",
        "scopus": round_dir / "scopus.log",
        "embase": round_dir / "embase.log",
        "cochrane": round_dir / "cochrane.log",
    }

    rows = []
    for db, log_path in logs.items():
        query = read_query(queries_path, db) if queries_path.exists() else ""
        count = parse_count(log_path)
        rows.append((db, query, count if count is not None else "NA", str(log_path)))

    out_csv = Path(args.out_csv) if args.out_csv else round_dir / "search_report.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["database", "query", "retrieved", "log_path"])
        writer.writerows(rows)

    out_md = Path(args.out_md) if args.out_md else round_dir / "search_report.md"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Search Report",
        "",
        f"Generated: {dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "")}Z",
        "",
        "| Database | Retrieved |",
        "| --- | --- |",
    ]
    for db, _, count, _ in rows:
        lines.append(f"| {db} | {count} |")
    lines.append("")
    lines.append("## Queries")
    for db, query, _, _ in rows:
        lines.append("")
        lines.append(f"### {db}")
        lines.append(query or "(missing)")

    out_md.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
