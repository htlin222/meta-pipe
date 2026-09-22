#!/usr/bin/env python3
"""Build 03_screening/screening-database.csv, the input ai_screen.py expects.

Nothing else in the pipeline creates this file: Stage 02 produces BibTeX, and
`ai_screen.py --stage abstract` reads `03_screening/screening-database.csv`.
This script bridges the two, from either

  * the enriched CSV from `enrich_abstracts.py` (preferred — carries abstracts), or
  * a `.bib` file directly (titles only, no abstracts).

It emits the dual-review schema columns so the output plugs straight into
`ai_screen.py` and `dual_review_agreement.py`, plus a stable `RecordID` used by
`merge_screening_shards.py` to reassemble sharded runs without losing rows.

Usage:
    uv run tooling/python/build_screening_database.py --project <name> \
        --in-csv projects/<name>/03_screening/records_with_abstracts.csv
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from pathlib import Path
from typing import Dict, List

COLUMNS = [
    "RecordID",
    "Source",
    "EntryType",
    "PMID",
    "NCTID",
    "DOI",
    "Authors",
    "Year",
    "Title",
    "Journal",
    "Abstract",
    "AbstractSource",
    "abstract_missing",
    "RecordTrack",
    "LinkedTo",
    "Reviewer1_Decision",
    "Reviewer1_Reason",
    "Reviewer2_Decision",
    "Reviewer2_Reason",
    "Final_Decision",
    "Final_Reason",
    "Notes",
]


def _resolve_meta_pipe_root() -> Path:
    env_root = os.environ.get("MA_PIPE_ROOT")
    root = Path(env_root).resolve() if env_root else Path(__file__).resolve().parent.parent.parent
    assert (root / "projects").is_dir(), f"MA_PIPE_ROOT={root} has no projects/ directory"
    return root


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").replace("\n", " ")).strip()


def note_source(note: str) -> str:
    m = re.search(r"source=([a-z]+)", note or "", re.I)
    return m.group(1).lower() if m else ""


def from_enriched(path: Path) -> List[Dict[str, str]]:
    with open(path, "r", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    out = []
    for r in rows:
        out.append(
            {
                "Source": note_source(r.get("note", "")) or r.get("source", ""),
                "EntryType": r.get("entry_type", ""),
                "PMID": clean(r.get("pmid", "")),
                "NCTID": clean(r.get("nctid", "")),
                "DOI": clean(r.get("doi", "")),
                "Authors": clean(r.get("authors", "")),
                "Year": clean(r.get("year", "")),
                "Title": clean(r.get("title", "")),
                "Journal": clean(r.get("journal", "")),
                "Abstract": clean(r.get("abstract", "")),
                "AbstractSource": clean(r.get("abstract_source", "")),
                "_id": clean(r.get("record_id", "")),
            }
        )
    return out


def from_bib(path: Path) -> List[Dict[str, str]]:
    import bibtexparser

    with open(path, "r", encoding="utf-8") as fh:
        entries = bibtexparser.load(fh).entries
    out = []
    for e in entries:
        out.append(
            {
                "Source": note_source(e.get("note", "")),
                "EntryType": e.get("ENTRYTYPE", ""),
                "PMID": clean(e.get("pmid", "")),
                "NCTID": clean(e.get("nctid", "")),
                "DOI": clean(e.get("doi", "")),
                "Authors": clean(e.get("author", "")),
                "Year": clean(e.get("year", "")),
                "Title": clean(e.get("title", "")),
                "Journal": clean(e.get("journal", "")),
                "Abstract": clean(e.get("abstract", "")),
                "AbstractSource": "bibtex" if e.get("abstract") else "",
                "_id": clean(e.get("ID", "")),
            }
        )
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--project", required=True)
    parser.add_argument("--in-csv", default=None, help="enrich_abstracts.py output")
    parser.add_argument("--in-bib", default=None, help="dedupe.bib (titles only)")
    parser.add_argument("--out", default=None, help="default: 03_screening/screening-database.csv")
    args = parser.parse_args()

    if bool(args.in_csv) == bool(args.in_bib):
        sys.exit("ERROR: pass exactly one of --in-csv or --in-bib")

    root = _resolve_meta_pipe_root()
    project_path = root / "projects" / args.project
    out_csv = Path(args.out) if args.out else project_path / "03_screening" / "screening-database.csv"

    src = Path(args.in_csv or args.in_bib)
    if not src.exists():
        sys.exit(f"ERROR: {src} not found")
    records = from_enriched(src) if args.in_csv else from_bib(src)
    if not records:
        sys.exit(f"ERROR: no records read from {src}")

    seen: set = set()
    rows: List[Dict[str, str]] = []
    for i, r in enumerate(records, 1):
        rid = r.pop("_id", "") or f"rec{i:05d}"
        if rid in seen:
            rid = f"{rid}__{i:05d}"
        seen.add(rid)
        row = {c: "" for c in COLUMNS}
        row.update(r)
        row["RecordID"] = rid
        # A record whose abstract could not be retrieved is screened on its title
        # alone. That is a RETRIEVAL limitation, not an eligibility judgement, so
        # such records must resolve to unclear -> advance to full text, never to
        # exclude. The flag makes that rule enforceable downstream and countable
        # for the PRISMA flow.
        row["abstract_missing"] = "FALSE" if row["Abstract"] else "TRUE"
        rows.append(row)

    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(rows)

    with_abs = sum(1 for r in rows if r["Abstract"])
    print(f"Wrote {len(rows)} records -> {out_csv}")
    print(f"  unique RecordID : {len(seen)}")
    print(f"  with abstract   : {with_abs} ({with_abs / len(rows) * 100:.1f}%)")
    print(f"  without abstract: {len(rows) - with_abs}")
    by_src: Dict[str, int] = {}
    for r in rows:
        by_src[r["Source"] or "unknown"] = by_src.get(r["Source"] or "unknown", 0) + 1
    for k, v in sorted(by_src.items()):
        print(f"  source {k:10s}: {v}")


if __name__ == "__main__":
    main()
