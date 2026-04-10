#!/usr/bin/env python3
"""Fetch Scopus Search API results and write raw JSON + best-effort BibTeX."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import requests

from env_utils import load_dotenv

SCOPUS_ENDPOINT = "https://api.elsevier.com/content/search/scopus"

DEFAULT_FIELDS = "dc:title,dc:creator,prism:publicationName,prism:coverDate,dc:description,prism:doi"


def sanitize_key(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "", text)
    return cleaned[:40] or "key"


def bib_escape(text: str) -> str:
    if text is None:
        return ""
    text = text.replace("\n", " ").replace("\r", " ").strip()
    text = text.replace("{", "\\{").replace("}", "\\}")
    return text


def extract_year(value: str) -> str:
    if not value:
        return ""
    match = re.search(r"(19|20)\d{2}", value)
    return match.group(0) if match else ""


def build_bib_entry(entry: Dict[str, Any], note: str, index: int) -> Optional[str]:
    title = entry.get("dc:title", "") or entry.get("title", "")
    journal = entry.get("prism:publicationName", "") or entry.get("publicationName", "")
    doi = entry.get("prism:doi", "") or entry.get("doi", "")
    cover_date = entry.get("prism:coverDate", "") or entry.get("coverDate", "")
    year = extract_year(str(cover_date))

    creator = entry.get("dc:creator", "")
    if isinstance(creator, list):
        authors = " and ".join([str(a) for a in creator if a])
    else:
        authors = str(creator) if creator else ""

    first_author = authors.split(" and ")[0] if authors else "unknown"
    key = sanitize_key(f"{first_author}{year}{index}")

    fields = {
        "title": title,
        "author": authors,
        "journal": journal,
        "year": year,
        "doi": doi,
        "note": note,
    }

    bib_lines = [f"@article{{{key},"]
    for k, v in fields.items():
        if v:
            bib_lines.append(f"  {k} = {{{bib_escape(str(v))}}},")
    bib_lines.append("}\n")
    return "\n".join(bib_lines)


def fetch_page(
    api_key: str,
    inst_token: Optional[str],
    query: str,
    start: int,
    count: int,
    fields: str,
) -> Dict[str, Any]:
    headers = {
        "X-ELS-APIKey": api_key,
        "Accept": "application/json",
    }
    if inst_token:
        headers["X-ELS-Insttoken"] = inst_token

    params = {
        "query": query,
        "start": start,
        "count": count,
        "field": fields,
    }

    resp = requests.get(SCOPUS_ENDPOINT, headers=headers, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Fetch Scopus records and write JSON + BibTeX.")
    parser.add_argument("--query", required=True, help="Scopus query string")
    parser.add_argument("--api-key", default=None, help="Scopus API key (or SCOPUS_API_KEY env)")
    parser.add_argument("--inst-token", default=None, help="Institution token (or SCOPUS_INST_TOKEN env)")
    parser.add_argument("--count", type=int, default=25, help="Records per page (max 100)")
    parser.add_argument("--start", type=int, default=0, help="Start index")
    parser.add_argument("--max-records", type=int, default=None, help="Max records to fetch")
    parser.add_argument("--fields", default=DEFAULT_FIELDS, help="Comma-separated field list")
    parser.add_argument("--note", default="round-01;source=scopus", help="Note for BibTeX")
    parser.add_argument("--out-json", required=True, help="Output JSON path")
    parser.add_argument("--out-bib", required=True, help="Output BibTeX path")
    parser.add_argument("--out-log", required=True, help="Output log path")
    parser.add_argument(
        "--strict-cap",
        action="store_true",
        help="Exit non-zero if total results exceeds --max-records (silent truncation guard)",
    )
    args = parser.parse_args()

    api_key = args.api_key or os.getenv("SCOPUS_API_KEY")
    inst_token = args.inst_token or os.getenv("SCOPUS_INST_TOKEN")

    if not api_key:
        raise SystemExit("Missing SCOPUS_API_KEY")

    start = args.start
    total_fetched = 0
    total_available = 0
    entries: List[Dict[str, Any]] = []

    while True:
        data = fetch_page(api_key, inst_token, args.query, start, args.count, args.fields)
        search_results = data.get("search-results", {})
        if total_available == 0:
            try:
                total_available = int(search_results.get("opensearch:totalResults", 0))
            except (TypeError, ValueError):
                total_available = 0
            if total_available:
                target = min(total_available, args.max_records or total_available)
                print(
                    f"Scopus reports {total_available} total results; "
                    f"fetching {target}."
                )
        page_entries = search_results.get("entry", [])
        if not page_entries:
            break
        entries.extend(page_entries)
        total_fetched += len(page_entries)

        if args.max_records and total_fetched >= args.max_records:
            break
        if len(page_entries) < args.count:
            break
        start += args.count

    cap_hit = bool(
        args.max_records
        and total_available
        and total_available > args.max_records
    )
    if cap_hit:
        print(
            f"WARNING: --max-records={args.max_records} truncated "
            f"{total_available - args.max_records} records silently. "
            f"Re-run with a larger cap or add --strict-cap to fail fast."
        )

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(
            {
                "query": args.query,
                "retrieved": total_fetched,
                "timestamp": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "") + "Z",
                "entries": entries,
            },
            indent=2,
        )
    )

    bib_entries = []
    for idx, entry in enumerate(entries, start=1):
        bib_entry = build_bib_entry(entry, args.note, idx)
        if bib_entry:
            bib_entries.append(bib_entry)

    out_bib = Path(args.out_bib)
    out_bib.parent.mkdir(parents=True, exist_ok=True)
    out_bib.write_text("\n".join(bib_entries))

    out_log = Path(args.out_log)
    out_log.parent.mkdir(parents=True, exist_ok=True)
    log_lines = [
        f"date: {dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "")}Z",
        f"query: {args.query}",
        f"total_available: {total_available}",
        f"retrieved: {total_fetched}",
        f"cap_hit: {cap_hit}",
        f"start: {args.start}",
        f"count: {args.count}",
        f"max_records: {args.max_records or ''}",
        f"fields: {args.fields}",
    ]
    out_log.write_text("\n".join(log_lines) + "\n")

    if cap_hit and args.strict_cap:
        raise SystemExit(
            f"--strict-cap: Scopus returned {total_available} results but "
            f"--max-records={args.max_records} truncated the response."
        )


if __name__ == "__main__":
    main()
