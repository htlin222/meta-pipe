#!/usr/bin/env python3
"""Resolve dual-review conflicts into Final_Decision, then emit included.bib.

Resolution rules, in order:

1. **abstract_missing == TRUE  ->  unclear (advance to full text).**
   A record whose abstract could not be retrieved is screened on its title
   alone. That is a RETRIEVAL limitation, not an eligibility judgement, so it
   may never be excluded at title/abstract stage. This rule wins over both
   reviewers: even two concordant EXCLUDEs are overridden, because neither
   reviewer had the evidence to exclude on.

2. **Registry records (RecordTrack startswith 'registry')** are not
   bibliographic records and are not screened as studies. `registry_linked`
   annotates its publication; `registry_unlinked` is a separate Stage 04 track.

3. **Agreement** -> that decision.

4. **Disagreement** -> the more inclusive of the two, i.e. any INCLUDE or MAYBE
   beats EXCLUDE. Standard conservative practice at title/abstract stage: the
   cost of a false include is one full text read, the cost of a false exclude is
   a missed study that never resurfaces.

Usage:
    uv run tooling/python/resolve_screening_conflicts.py --project <name> [--round round-01]
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List

RANK = {"include": 3, "maybe": 2, "unclear": 2, "exclude": 1, "": 0}


def _resolve_meta_pipe_root() -> Path:
    env_root = os.environ.get("MA_PIPE_ROOT")
    root = Path(env_root).resolve() if env_root else Path(__file__).resolve().parent.parent.parent
    assert (root / "projects").is_dir(), f"MA_PIPE_ROOT={root} has no projects/ directory"
    return root


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project", required=True)
    ap.add_argument("--round", default="round-01")
    ap.add_argument("--in-bib", default=None, help="corpus .bib for included.bib extraction")
    args = ap.parse_args()

    root = _resolve_meta_pipe_root()
    proj = root / "projects" / args.project
    round_dir = proj / "03_screening" / args.round
    dec_csv = round_dir / "decisions.csv"
    if not dec_csv.exists():
        sys.exit(f"ERROR: {dec_csv} not found -- run merge_screening_shards.py first")

    with open(dec_csv, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    n_in = len(rows)
    stats = Counter()
    for r in rows:
        r1 = (r.get("Reviewer1_Decision") or "").strip().lower()
        r2 = (r.get("Reviewer2_Decision") or "").strip().lower()
        track = (r.get("RecordTrack") or "").strip()
        missing = (r.get("abstract_missing") or "").strip().upper() == "TRUE"

        if track.startswith("registry"):
            r["Final_Decision"] = "registry_track"
            r["Final_Reason"] = f"Not screened as a study; handled on the {track} track (D-028)"
            stats[f"registry:{track}"] += 1
            continue

        if missing:
            r["Final_Decision"] = "unclear"
            r["Final_Reason"] = (
                "abstract_missing=TRUE: screened on title alone; advanced to full text. "
                "A missing abstract is a retrieval artefact, never an exclusion (D-027)."
            )
            stats["rule:abstract_missing->unclear"] += 1
            if "exclude" in (r1, r2):
                stats["rule:override_of_exclude"] += 1
            continue

        if r1 and r1 == r2:
            r["Final_Decision"] = r1
            r["Final_Reason"] = f"Both reviewers agreed: {r1}"
            stats[f"agree:{r1}"] += 1
        elif not r1 or not r2:
            r["Final_Decision"] = "unclear"
            r["Final_Reason"] = "Missing a reviewer decision; advanced to full text"
            stats["incomplete->unclear"] += 1
        else:
            winner = r1 if RANK.get(r1, 0) >= RANK.get(r2, 0) else r2
            r["Final_Decision"] = winner
            r["Final_Reason"] = f"Conflict ({r1} vs {r2}) resolved to the more inclusive: {winner}"
            stats[f"conflict->{winner}"] += 1

    with open(dec_csv, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    assert len(rows) == n_in, "row count changed during resolution"

    print(f"Resolved {len(rows)} records -> {dec_csv}")
    for k, v in sorted(stats.items()):
        print(f"  {k:36s} {v}")
    final = Counter((r.get("Final_Decision") or "").lower() for r in rows)
    print("\nFinal_Decision distribution:")
    for k, v in final.most_common():
        print(f"  {k or '(blank)':20s} {v}")

    # ---- included.bib: everything advancing to full text ----
    advance = {r["RecordID"] for r in rows if (r.get("Final_Decision") or "") in ("include", "unclear", "maybe")}
    in_bib = Path(args.in_bib) if args.in_bib else proj / "02_search" / "round-03" / "dedupe.bib"
    out_bib = round_dir / "included.bib"
    if not in_bib.exists():
        sys.exit(f"ERROR: corpus bib not found: {in_bib}")

    import bibtexparser

    with open(in_bib, encoding="utf-8") as fh:
        entries = bibtexparser.load(fh).entries
    keep = [e for e in entries if e.get("ID", "") in advance]

    from bibtexparser.bwriter import BibTexWriter
    from bibtexparser import loads

    writer = BibTexWriter()
    writer.indent = "  "
    writer.order_entries_by = None
    db = loads("")
    db.entries = keep
    out_bib.write_text(writer.write(db), encoding="utf-8")

    print(f"\nincluded.bib: {len(keep)} records advancing to full text -> {out_bib}")
    if len(keep) != len(advance):
        print(
            f"  WARNING: {len(advance) - len(keep)} advancing RecordIDs had no matching "
            f"bib entry in {in_bib.name}"
        )


if __name__ == "__main__":
    main()
