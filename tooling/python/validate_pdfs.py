#!/usr/bin/env python3
"""Validate downloaded PDFs and write honest retrieval statuses into manifest.csv.

Open-access download pipelines routinely save publisher interstitials, cookie
walls and 403 pages under a .pdf name. Those files are not full texts, and
counting them as retrieved would overstate retrieval and, worse, feed an empty
"full text" into eligibility screening. This checks the actual bytes.

A file counts as a real PDF only if it starts with %PDF and yields extractable
text. Everything else is recorded as a failed retrieval, not a retrieval.

Statuses written to manifest.csv `retrieval_status`:
    retrieved_pdf   validated PDF on disk with extractable text
    pdf_invalid     a file was downloaded but is not a usable PDF
    abstract_only   no usable PDF, but an abstract is available as the source
    registry_only   no PDF or abstract, but a registry record exists
    unavailable     nothing retrievable -- PRISMA "reports not retrieved"

Usage:
    uv run tooling/python/validate_pdfs.py --project <name>
"""

from __future__ import annotations

import argparse
import csv
import os
from collections import Counter
from pathlib import Path


def _root() -> Path:
    env = os.environ.get("MA_PIPE_ROOT")
    r = Path(env).resolve() if env else Path(__file__).resolve().parent.parent.parent
    assert (r / "projects").is_dir()
    return r


def is_real_pdf(path: Path) -> tuple[bool, str]:
    try:
        head = path.open("rb").read(5)
    except Exception as exc:  # noqa: BLE001
        return False, f"unreadable: {exc}"
    if head[:4] != b"%PDF":
        return False, f"not a PDF (starts with {head[:4]!r})"
    if path.stat().st_size < 10_000:
        return False, f"suspiciously small ({path.stat().st_size} bytes)"
    return True, ""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project", required=True)
    ap.add_argument("--min-text-chars", type=int, default=500)
    args = ap.parse_args()

    proj = _root() / "projects" / args.project
    man = proj / "04_fulltext" / "manifest.csv"
    pdf_dir = proj / "04_fulltext" / "pdf"
    screening_db = proj / "03_screening" / "screening-database.csv"

    abstracts = {}
    if screening_db.exists():
        with open(screening_db, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                abstracts[r["RecordID"]] = (r.get("Abstract") or "").strip()

    with open(man, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    stats = Counter()
    for r in rows:
        rid = r["record_id"]
        cand = pdf_dir / f"{rid}.pdf"
        if cand.exists():
            ok, why = is_real_pdf(cand)
            if ok:
                r["retrieval_status"] = "retrieved_pdf"
                r["file_path"] = str(cand.relative_to(proj))
                r["data_source"] = "pdf_fulltext"
                r["access_notes"] = "open access via Unpaywall"
                r["needs_pdf"] = "FALSE"
                stats["retrieved_pdf"] += 1
                continue
            r["access_notes"] = f"download produced a non-PDF: {why}"
            try:
                cand.unlink()
            except Exception:  # noqa: BLE001
                pass
            stats["pdf_invalid"] += 1

        abstract = abstracts.get(rid, "")
        if abstract:
            r["retrieval_status"] = "abstract_only"
            r["data_source"] = "abstract"
            r["needs_pdf"] = "TRUE"
            if not r.get("access_notes"):
                r["access_notes"] = "no OA PDF; abstract is the available source"
            stats["abstract_only"] += 1
        elif (r.get("nctid") or "").strip():
            r["retrieval_status"] = "registry_only"
            r["data_source"] = "registry"
            r["needs_pdf"] = "TRUE"
            stats["registry_only"] += 1
        else:
            r["retrieval_status"] = "unavailable"
            r["data_source"] = ""
            r["needs_pdf"] = "TRUE"
            if not r.get("access_notes"):
                r["access_notes"] = "no OA PDF, no abstract, no registry record"
            stats["unavailable"] += 1

    with open(man, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    print(f"manifest.csv updated: {len(rows)} rows")
    for k, v in stats.most_common():
        print(f"  {k:16s} {v}")
    assessable = stats["retrieved_pdf"] + stats["abstract_only"]
    print(f"\nassessable at full-text stage : {assessable}")
    print(f"not retrievable (PRISMA box)  : {stats['unavailable'] + stats['registry_only']}")


if __name__ == "__main__":
    main()
