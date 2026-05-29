#!/usr/bin/env python3
"""Merge multiple BibTeX files and deduplicate records."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Dict, Tuple


def norm_doi(value: str) -> str:
    if not value:
        return ""
    value = value.strip().lower()
    value = value.replace("https://doi.org/", "").replace("http://doi.org/", "")
    return value


def norm_title(value: str) -> str:
    if not value:
        return ""
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def score_entry(entry: Dict[str, str]) -> Tuple[int, int]:
    fields = [v for v in entry.values() if isinstance(v, str) and v.strip()]
    has_doi = 1 if entry.get("doi") else 0
    return (len(fields), has_doi)


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge and deduplicate BibTeX files.")
    parser.add_argument("--in-bib", action="append", required=True, help="Input .bib (repeatable)")
    parser.add_argument("--out-bib", required=True, help="Output deduped .bib")
    parser.add_argument("--out-log", required=True, help="Output log file")
    parser.add_argument("--out-merged", default=None, help="Optional merged .bib output")
    args = parser.parse_args()

    from bibtexparser import loads
    from bibtexparser.bwriter import BibTexWriter

    all_entries = []
    counts = []
    for bib_path in args.in_bib:
        text = Path(bib_path).read_text(encoding="utf-8")
        db = loads(text)
        counts.append((bib_path, len(db.entries)))
        all_entries.extend(db.entries)

    merged_count = len(all_entries)

    deduped: Dict[str, Dict[str, str]] = {}
    collisions = 0

    for entry in all_entries:
        doi = norm_doi(entry.get("doi", ""))
        pmid = entry.get("pmid", "").strip()
        title = norm_title(entry.get("title", ""))

        key = doi or pmid or title
        if not key:
            key = entry.get("ID")

        if key in deduped:
            collisions += 1
            if score_entry(entry) > score_entry(deduped[key]):
                deduped[key] = entry
        else:
            deduped[key] = entry

    writer = BibTexWriter()
    writer.indent = "  "
    writer.order_entries_by = None

    out_db = loads("")
    out_db.entries = list(deduped.values())
    Path(args.out_bib).write_text(writer.write(out_db), encoding="utf-8")

    if args.out_merged:
        merged_db = loads("")
        merged_db.entries = all_entries
        Path(args.out_merged).write_text(writer.write(merged_db), encoding="utf-8")

    log_lines = ["inputs:"]
    for path, count in counts:
        log_lines.append(f"- {path}: {count}")
    log_lines.extend(
        [
            f"merged_records: {merged_count}",
            f"deduped_records: {len(out_db.entries)}",
            f"collisions: {collisions}",
        ]
    )
    Path(args.out_log).write_text("\n".join(log_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
