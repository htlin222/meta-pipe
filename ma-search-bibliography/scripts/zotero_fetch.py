#!/usr/bin/env python3
"""Fetch Zotero items via the Read API and write BibTeX."""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
from pathlib import Path
from typing import Optional

import requests

from env_utils import load_dotenv

BASE_URL = "https://api.zotero.org"
DEFAULT_LIMIT = 100


def build_prefix(library_type: str, library_id: str) -> str:
    library_type = (library_type or "").strip().lower()
    if library_type == "user":
        return f"{BASE_URL}/users/{library_id}"
    if library_type == "group":
        return f"{BASE_URL}/groups/{library_id}"
    raise SystemExit("library-type must be 'user' or 'group'")


def count_bib_entries(text: str) -> int:
    return len(re.findall(r"^@", text, flags=re.MULTILINE))


def fetch_page(
    session: requests.Session,
    url: str,
    api_key: Optional[str],
    start: int,
    limit: int,
    fmt: str,
) -> requests.Response:
    headers = {
        "Zotero-API-Version": "3",
        "Accept": "text/plain",
    }
    if api_key:
        headers["Zotero-API-Key"] = api_key
    params = {
        "format": fmt,
        "start": start,
        "limit": limit,
    }
    resp = session.get(url, headers=headers, params=params, timeout=60)
    resp.raise_for_status()
    return resp


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Fetch Zotero items and write BibTeX.")
    parser.add_argument("--library-type", default=None, help="user or group (or ZOTERO_LIBRARY_TYPE)")
    parser.add_argument("--library-id", default=None, help="Library ID (or ZOTERO_LIBRARY_ID)")
    parser.add_argument(
        "--collection-key", default=None, help="Collection key (or ZOTERO_COLLECTION_KEY)"
    )
    parser.add_argument("--api-key", default=None, help="Zotero API key (or ZOTERO_API_KEY)")
    parser.add_argument("--format", default="bibtex", help="Export format (default: bibtex)")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Page size (max 100)")
    parser.add_argument("--out-bib", required=True, help="Output BibTeX path")
    parser.add_argument("--out-log", required=True, help="Output log path")
    args = parser.parse_args()

    api_key = args.api_key or os.getenv("ZOTERO_API_KEY")
    library_type = args.library_type or os.getenv("ZOTERO_LIBRARY_TYPE")
    library_id = args.library_id or os.getenv("ZOTERO_LIBRARY_ID")
    collection_key = args.collection_key or os.getenv("ZOTERO_COLLECTION_KEY")

    if not library_type or not library_id:
        raise SystemExit("Missing library type or library id.")

    prefix = build_prefix(library_type, library_id)
    if collection_key:
        url = f"{prefix}/collections/{collection_key}/items"
    else:
        url = f"{prefix}/items"

    out_bib = Path(args.out_bib)
    out_log = Path(args.out_log)

    session = requests.Session()
    start = 0
    limit = max(1, min(args.limit, 100))
    total_results = None
    pages = 0
    total_entries = 0
    chunks: list[str] = []

    while True:
        resp = fetch_page(session, url, api_key, start, limit, args.format)
        text = resp.text.strip()
        if not text:
            break
        chunks.append(text)
        pages += 1
        total_entries += count_bib_entries(text)

        if total_results is None:
            try:
                total_results = int(resp.headers.get("Total-Results", ""))
            except ValueError:
                total_results = None

        start += limit
        if total_results is not None and start >= total_results:
            break
        if count_bib_entries(text) < limit:
            break

    out_bib.write_text("\n\n".join(chunks) + ("\n" if chunks else ""))

    log_lines = [
        f"date: {dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "")}Z",
        f"library_type: {library_type}",
        f"library_id: {library_id}",
        f"collection_key: {collection_key or ''}",
        f"format: {args.format}",
        f"limit: {limit}",
        f"pages: {pages}",
        f"total_results: {total_results or ''}",
        f"fetched_entries: {total_entries}",
    ]
    out_log.write_text("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
