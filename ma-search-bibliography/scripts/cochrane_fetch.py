#!/usr/bin/env python3
"""Fetch Cochrane ReviewDB API results and write raw JSON + best-effort BibTeX."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import base64
import requests

from env_utils import load_dotenv

COCHRANE_ENDPOINT = "https://api.cochrane.org/reviews"


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


def extract_entries(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    if "items" in payload and isinstance(payload["items"], list):
        return payload["items"]
    if "results" in payload and isinstance(payload["results"], list):
        return payload["results"]
    return []


def build_bib_entry(entry: Dict[str, Any], note: str, index: int) -> Optional[str]:
    title = entry.get("title", "") or entry.get("short_title", "")
    journal = entry.get("journal", "") or "Cochrane Database Syst Rev"
    doi = entry.get("doi", "")
    pub_date = entry.get("date", "") or entry.get("publish_date", "")
    year = extract_year(str(pub_date))

    authors = ""
    author_list = entry.get("authors") or entry.get("author")
    if isinstance(author_list, list):
        authors = " and ".join([str(a) for a in author_list if a])
    elif isinstance(author_list, str):
        authors = author_list

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


def build_headers(token: Optional[str], username: Optional[str], password: Optional[str]) -> Dict[str, str]:
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    elif username and password:
        creds = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
        headers["Authorization"] = f"Basic {creds}"
    return headers


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Fetch Cochrane ReviewDB records and write JSON + BibTeX.")
    parser.add_argument("--query", required=True, help="Cochrane query string for ?q=")
    parser.add_argument("--token", default=None, help="OAuth token (or COCHRANE_OAUTH_TOKEN env)")
    parser.add_argument("--username", default=None, help="Basic auth username (or COCHRANE_USERNAME env)")
    parser.add_argument("--password", default=None, help="Basic auth password (or COCHRANE_PASSWORD env)")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--per-page", type=int, default=50, help="Results per page")
    parser.add_argument("--max-pages", type=int, default=1, help="Max pages to fetch")
    parser.add_argument("--note", default="round-01;source=cochrane", help="Note for BibTeX")
    parser.add_argument("--out-json", required=True, help="Output JSON path")
    parser.add_argument("--out-bib", required=True, help="Output BibTeX path")
    parser.add_argument("--out-log", required=True, help="Output log path")
    args = parser.parse_args()

    token = args.token or os.getenv("COCHRANE_OAUTH_TOKEN")
    username = args.username or os.getenv("COCHRANE_USERNAME")
    password = args.password or os.getenv("COCHRANE_PASSWORD")

    headers = build_headers(token, username, password)

    entries: List[Dict[str, Any]] = []
    page = args.page

    for _ in range(args.max_pages):
        params = {"q": args.query, "page": page, "per_page": args.per_page}
        resp = requests.get(COCHRANE_ENDPOINT, headers=headers, params=params, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        page_entries = extract_entries(data)
        if not page_entries:
            break
        entries.extend(page_entries)
        if len(page_entries) < args.per_page:
            break
        page += 1

    out_json = Path(args.out_json)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(
        json.dumps(
            {
                "query": args.query,
                "retrieved": len(entries),
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
        f"retrieved: {len(entries)}",
        f"page_start: {args.page}",
        f"per_page: {args.per_page}",
        f"max_pages: {args.max_pages}",
    ]
    out_log.write_text("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
