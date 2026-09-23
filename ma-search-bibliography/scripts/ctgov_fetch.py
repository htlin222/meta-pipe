#!/usr/bin/env python3
"""Fetch ClinicalTrials.gov API v2 records and write raw JSON + BibTeX.

ClinicalTrials.gov API v2 is public and requires no API key, which makes it a usable
second source when Scopus/Embase/Cochrane credentials are unavailable (PRISMA requires
at least two sources).

Registry records are trial registrations, not journal articles. They are emitted as
@misc entries carrying the NCT id, so that downstream dedupe and screening can tell
them apart from bibliographic records.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

CTGOV_ENDPOINT = "https://clinicaltrials.gov/api/v2/studies"


def sanitize_key(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "", text)
    return cleaned[:40] or "key"


def bib_escape(text: str) -> str:
    if text is None:
        return ""
    text = str(text).replace("\n", " ").replace("\r", " ").strip()
    return text.replace("{", "\\{").replace("}", "\\}")


def extract_year(value: Any) -> str:
    match = re.search(r"(19|20)\d{2}", str(value or ""))
    return match.group(0) if match else ""


def build_bib_entry(study: Dict[str, Any], note: str) -> Optional[str]:
    proto = study.get("protocolSection", {}) or {}
    ident = proto.get("identificationModule", {}) or {}
    status = proto.get("statusModule", {}) or {}
    design = proto.get("designModule", {}) or {}
    sponsor = proto.get("sponsorCollaboratorsModule", {}) or {}

    nct_id = ident.get("nctId", "")
    if not nct_id:
        return None

    title = ident.get("officialTitle") or ident.get("briefTitle") or ""
    lead = (sponsor.get("leadSponsor", {}) or {}).get("name", "")
    year = extract_year((status.get("startDateStruct", {}) or {}).get("date"))
    phases = ",".join(design.get("phases", []) or [])
    allocation = (design.get("designInfo", {}) or {}).get("allocation", "")
    enrollment = (design.get("enrollmentInfo", {}) or {}).get("count", "")

    fields = {
        "title": title,
        "author": lead,
        "year": year,
        "howpublished": f"ClinicalTrials.gov registration {nct_id}",
        "url": f"https://clinicaltrials.gov/study/{nct_id}",
        "nctid": nct_id,
        "phase": phases,
        "allocation": allocation,
        "enrollment": enrollment,
        "overallstatus": status.get("overallStatus", ""),
        "hasresults": str(study.get("hasResults", "")),
        "note": note,
    }

    lines = [f"@misc{{{sanitize_key(nct_id)},"]
    for key, value in fields.items():
        if value not in (None, "", "None"):
            lines.append(f"  {key} = {{{bib_escape(value)}}},")
    lines.append("}\n")
    return "\n".join(lines)


def fetch_studies(
    params: Dict[str, Any],
    page_size: int,
    max_pages: int,
    sleep: float,
) -> tuple[List[Dict[str, Any]], int]:
    studies: List[Dict[str, Any]] = []
    total = 0
    page_token: Optional[str] = None

    for page in range(max_pages):
        call = dict(params)
        call["pageSize"] = page_size
        if page == 0:
            call["countTotal"] = "true"
        if page_token:
            call["pageToken"] = page_token

        resp = requests.get(CTGOV_ENDPOINT, params=call, timeout=60)
        resp.raise_for_status()
        data = resp.json()

        if page == 0:
            total = int(data.get("totalCount", 0))

        batch = data.get("studies", []) or []
        if not batch:
            break
        studies.extend(batch)

        page_token = data.get("nextPageToken")
        if not page_token:
            break
        time.sleep(sleep)

    return studies, total


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch ClinicalTrials.gov API v2 records and write JSON + BibTeX."
    )
    parser.add_argument("--cond", default=None, help="query.cond (condition terms)")
    parser.add_argument("--intr", default=None, help="query.intr (intervention terms)")
    parser.add_argument("--term", default=None, help="query.term (free-text terms)")
    parser.add_argument(
        "--filter-advanced",
        default=None,
        help='filter.advanced, e.g. "AREA[DesignAllocation]RANDOMIZED"',
    )
    parser.add_argument("--page-size", type=int, default=100, help="Results per page (max 1000)")
    parser.add_argument("--max-pages", type=int, default=50, help="Max pages to fetch")
    parser.add_argument("--sleep", type=float, default=0.34, help="Delay between pages (s)")
    parser.add_argument("--note", default="round-01;source=ctgov", help="Note for BibTeX")
    parser.add_argument("--out-json", required=True, help="Output JSON path")
    parser.add_argument("--out-bib", required=True, help="Output BibTeX path")
    parser.add_argument("--out-log", required=True, help="Output log path")
    args = parser.parse_args()

    params: Dict[str, Any] = {}
    if args.cond:
        params["query.cond"] = args.cond
    if args.intr:
        params["query.intr"] = args.intr
    if args.term:
        params["query.term"] = args.term
    if args.filter_advanced:
        params["filter.advanced"] = args.filter_advanced
    if not params:
        raise SystemExit("Provide at least one of --cond / --intr / --term")

    studies, total = fetch_studies(params, args.page_size, args.max_pages, args.sleep)
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "") + "Z"

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(
            {
                "endpoint": CTGOV_ENDPOINT,
                "params": params,
                "total_count": total,
                "retrieved": len(studies),
                "timestamp": timestamp,
                "studies": studies,
            },
            indent=2,
        )
    )

    entries = [e for e in (build_bib_entry(s, args.note) for s in studies) if e]
    out_bib = Path(args.out_bib)
    out_bib.parent.mkdir(parents=True, exist_ok=True)
    out_bib.write_text("\n".join(entries))

    out_log = Path(args.out_log)
    out_log.parent.mkdir(parents=True, exist_ok=True)
    out_log.write_text(
        "\n".join(
            [
                f"date: {timestamp}",
                f"endpoint: {CTGOV_ENDPOINT}",
                f"params: {json.dumps(params)}",
                f"total_count: {total}",
                f"retrieved: {len(studies)}",
                f"bib_entries: {len(entries)}",
                f"page_size: {args.page_size}",
                f"max_pages: {args.max_pages}",
            ]
        )
        + "\n"
    )
    print(f"ClinicalTrials.gov: total={total} retrieved={len(studies)} bib={len(entries)}")


if __name__ == "__main__":
    main()
