#!/usr/bin/env python3
"""Query Unpaywall for open-access links using DOI metadata."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import requests


def load_dotenv() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    sys.path.append(str(repo_root / "ma-search-bibliography" / "scripts"))
    try:
        from env_utils import load_dotenv as _load
    except Exception:
        return
    _load(repo_root)


def read_bib_entries(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Missing bib file: {path}")
    from bibtexparser import loads

    bib = loads(path.read_text())
    entries = []
    for entry in bib.entries:
        record_id = entry.get("ID", "").strip()
        doi = entry.get("doi", "").strip()
        pmid = entry.get("pmid", "").strip()
        title = entry.get("title", "").strip()
        if doi or record_id:
            entries.append(
                {
                    "record_id": record_id,
                    "doi": doi,
                    "pmid": pmid,
                    "title": title,
                }
            )
    return entries


def iter_dois(entries: Iterable[Dict[str, str]]) -> Iterable[Dict[str, str]]:
    for entry in entries:
        doi = entry.get("doi", "").strip()
        doi = doi.replace("https://doi.org/", "").replace("http://doi.org/", "").replace("doi:", "")
        doi = doi.strip()
        if not doi:
            continue
        entry = dict(entry)
        entry["doi"] = doi
        yield entry


def fetch_unpaywall(api_base: str, doi: str, email: str) -> Dict[str, Any]:
    base = api_base.rstrip("/")
    encoded = urllib.parse.quote(doi)
    url = f"{base}/v2/{encoded}"
    resp = requests.get(url, params={"email": email}, timeout=60)
    if resp.status_code == 404:
        return {"doi": doi, "error": "not_found"}
    resp.raise_for_status()
    return resp.json()


def extract_row(entry: Dict[str, str], payload: Dict[str, Any]) -> Dict[str, str]:
    best = payload.get("best_oa_location") or {}
    row = {
        "record_id": entry.get("record_id", ""),
        "doi": entry.get("doi", ""),
        "pmid": entry.get("pmid", ""),
        "title": entry.get("title", ""),
        "is_oa": str(payload.get("is_oa", "")),
        "oa_status": str(payload.get("oa_status", "")),
        "best_oa_url": str(best.get("url", "")),
        "best_oa_pdf_url": str(best.get("url_for_pdf", "")),
        "host_type": str(best.get("host_type", "")),
        "license": str(best.get("license", "")),
        "updated": str(payload.get("updated", "")),
    }
    if payload.get("error"):
        row["oa_status"] = payload.get("error")
    return row


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Fetch Unpaywall OA locations for DOI list.")
    parser.add_argument("--in-bib", required=True, help="Input BibTeX file (included studies)")
    parser.add_argument("--email", default=None, help="Contact email (or UNPAYWALL_EMAIL env)")
    parser.add_argument("--api-base", default="https://api.unpaywall.org", help="Unpaywall API base URL")
    parser.add_argument("--sleep", type=float, default=0.2, help="Sleep seconds between requests")
    parser.add_argument("--max-records", type=int, default=None, help="Max DOIs to query")
    parser.add_argument("--out-csv", required=True, help="Output CSV path")
    parser.add_argument("--out-json", default=None, help="Output JSON path (raw payloads)")
    parser.add_argument("--out-log", required=True, help="Output log path")
    args = parser.parse_args()

    email = args.email or os.getenv("UNPAYWALL_EMAIL")
    if not email:
        raise SystemExit("Missing UNPAYWALL_EMAIL (or --email)")

    entries = read_bib_entries(Path(args.in_bib))
    targets = list(iter_dois(entries))
    if args.max_records is not None:
        targets = targets[: args.max_records]

    rows: List[Dict[str, str]] = []
    payloads: List[Dict[str, Any]] = []
    missing_doi = len([e for e in entries if not e.get("doi")])

    for idx, entry in enumerate(targets, start=1):
        payload = fetch_unpaywall(args.api_base, entry["doi"], email)
        payloads.append(payload)
        rows.append(extract_row(entry, payload))
        if args.sleep:
            time.sleep(args.sleep)

    out_csv = Path(args.out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with out_csv.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "record_id",
                "doi",
                "pmid",
                "title",
                "is_oa",
                "oa_status",
                "best_oa_url",
                "best_oa_pdf_url",
                "host_type",
                "license",
                "updated",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    if args.out_json:
        out_json = Path(args.out_json)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(
            json.dumps(
                {
                    "timestamp": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "") + "Z",
                    "requested": len(targets),
                    "missing_doi": missing_doi,
                    "payloads": payloads,
                },
                indent=2,
            )
        )

    out_log = Path(args.out_log)
    out_log.parent.mkdir(parents=True, exist_ok=True)
    log_lines = [
        f"date: {dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "")}Z",
        f"input_bib: {args.in_bib}",
        f"records_in_bib: {len(entries)}",
        f"missing_doi: {missing_doi}",
        f"queried: {len(targets)}",
        f"api_base: {args.api_base}",
        f"out_csv: {out_csv}",
    ]
    if args.out_json:
        log_lines.append(f"out_json: {args.out_json}")
    out_log.write_text("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
