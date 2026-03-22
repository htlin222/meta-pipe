#!/usr/bin/env python3
"""Fetch CrossRef records and write a BibTeX file."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from env_utils import load_dotenv


def sanitize_key(text: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "", text)
    return cleaned[:40] or "key"


def bib_escape(text: str) -> str:
    if text is None:
        return ""
    text = text.replace("\n", " ").replace("\r", " ").strip()
    text = text.replace("{", "\\{").replace("}", "\\}")
    return text


def format_authors(authors: List[Dict[str, str]]) -> str:
    if not authors:
        return ""
    names = []
    for a in authors:
        family = a.get("family", "")
        given = a.get("given", "")
        if family and given:
            names.append(f"{family}, {given}")
        elif family:
            names.append(family)
    return " and ".join(names)


def extract_year(item: Dict[str, Any]) -> str:
    for field in ("published-print", "published-online", "issued", "created"):
        date_parts = item.get(field, {}).get("date-parts", [[]])
        if date_parts and date_parts[0] and date_parts[0][0]:
            return str(date_parts[0][0])
    return ""


def build_bib_entry(item: Dict[str, Any], note: str) -> Optional[str]:
    title = item.get("title", [""])[0] if item.get("title") else ""
    if not title:
        return None

    authors = format_authors(item.get("author", []))
    year = extract_year(item)
    doi = item.get("DOI", "")
    journal = ""
    if item.get("container-title"):
        journal = item["container-title"][0] if item["container-title"] else ""
    volume = item.get("volume", "")
    issue = item.get("issue", "")
    pages = item.get("page", "")

    first_author = authors.split(" and ")[0] if authors else "unknown"
    key = sanitize_key(f"{first_author}{year}{doi[-6:]}")

    fields = {
        "title": title,
        "author": authors,
        "journal": journal,
        "year": year,
        "volume": volume,
        "number": issue,
        "pages": pages,
        "doi": doi,
        "note": note,
    }

    bib_lines = [f"@article{{{key},"]
    for k, v in fields.items():
        if v:
            bib_lines.append(f"  {k} = {{{bib_escape(str(v))}}},")
    bib_lines.append("}\n")
    return "\n".join(bib_lines)


def fetch_crossref(
    query: str,
    email: str,
    rows: int = 100,
    offset: int = 0,
    filter_str: Optional[str] = None,
) -> Dict[str, Any]:
    url = "https://api.crossref.org/works"
    params: Dict[str, Any] = {
        "query": query,
        "rows": min(rows, 1000),
        "offset": offset,
        "sort": "relevance",
        "order": "desc",
    }
    if filter_str:
        params["filter"] = filter_str
    headers = {
        "User-Agent": f"meta-pipe/1.0 (mailto:{email})",
    }
    resp = requests.get(url, params=params, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Fetch CrossRef records and write BibTeX.")
    parser.add_argument("--query", required=True, help="CrossRef query string")
    parser.add_argument("--email", default="cognitive-effort-review@meta-pipe.org",
                        help="Contact email for polite pool")
    parser.add_argument("--rows", type=int, default=100, help="Max results per page")
    parser.add_argument("--max-results", type=int, default=200, help="Total max results")
    parser.add_argument("--filter", default=None, help="CrossRef filter (e.g. from-pub-date:2005)")
    parser.add_argument("--note", default="round-01", help="Note for BibTeX entries")
    parser.add_argument("--sleep", type=float, default=1.0, help="Sleep between pages")
    parser.add_argument("--out-bib", required=True, help="Output .bib path")
    parser.add_argument("--out-log", required=True, help="Output log path")
    args = parser.parse_args()

    entries: List[str] = []
    total_fetched = 0
    offset = 0

    while total_fetched < args.max_results:
        batch_size = min(args.rows, args.max_results - total_fetched)
        data = fetch_crossref(
            query=args.query,
            email=args.email,
            rows=batch_size,
            offset=offset,
            filter_str=args.filter,
        )
        items = data.get("message", {}).get("items", [])
        if not items:
            break

        for item in items:
            entry = build_bib_entry(item, note=args.note)
            if entry:
                entries.append(entry)
                total_fetched += 1

        offset += len(items)
        if len(items) < batch_size:
            break
        if total_fetched < args.max_results:
            time.sleep(args.sleep)

    Path(args.out_bib).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_bib).write_text("\n".join(entries))

    log_lines = [
        f"date: {dt.datetime.utcnow().isoformat()}Z",
        f"query: {args.query}",
        f"count: {total_fetched}",
        f"max_results: {args.max_results}",
        f"filter: {args.filter or ''}",
    ]
    Path(args.out_log).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_log).write_text("\n".join(log_lines) + "\n")

    print(f"CrossRef: fetched {total_fetched} records → {args.out_bib}")


if __name__ == "__main__":
    main()
