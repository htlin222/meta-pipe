#!/usr/bin/env python3
"""Query Unpaywall for open-access links using DOI metadata - ROBUST VERSION.

This version handles API errors gracefully and continues processing other records.
"""

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


def fetch_unpaywall(api_base: str, doi: str, email: str, max_retries: int = 3) -> Dict[str, Any]:
    """Fetch Unpaywall data with robust error handling.

    Args:
        api_base: Unpaywall API base URL
        doi: DOI to query
        email: Contact email
        max_retries: Maximum number of retries for transient errors

    Returns:
        Dictionary with either successful payload or error information
    """
    base = api_base.rstrip("/")
    encoded = urllib.parse.quote(doi)
    url = f"{base}/v2/{encoded}"

    for attempt in range(max_retries):
        try:
            resp = requests.get(url, params={"email": email}, timeout=60)

            # Handle specific status codes
            if resp.status_code == 404:
                return {"doi": doi, "error": "not_found", "error_detail": "DOI not found in Unpaywall"}

            if resp.status_code == 422:
                return {
                    "doi": doi,
                    "error": "unprocessable",
                    "error_detail": f"Unpaywall cannot process this DOI (HTTP 422)"
                }

            if resp.status_code == 429:
                # Rate limit - wait longer and retry
                wait_time = (attempt + 1) * 2
                print(f"  Rate limited for DOI {doi}, waiting {wait_time}s...", file=sys.stderr)
                time.sleep(wait_time)
                continue

            # Raise for other bad status codes
            resp.raise_for_status()
            return resp.json()

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"  Timeout for DOI {doi}, retrying ({attempt+1}/{max_retries})...", file=sys.stderr)
                time.sleep((attempt + 1) * 1)
                continue
            return {"doi": doi, "error": "timeout", "error_detail": "Request timeout after retries"}

        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"  Request error for DOI {doi}, retrying ({attempt+1}/{max_retries})...", file=sys.stderr)
                time.sleep((attempt + 1) * 1)
                continue
            return {
                "doi": doi,
                "error": "request_failed",
                "error_detail": f"Request exception: {str(e)[:100]}"
            }

    return {"doi": doi, "error": "max_retries", "error_detail": "Max retries exceeded"}


def extract_row(entry: Dict[str, str], payload: Dict[str, Any]) -> Dict[str, str]:
    """Extract CSV row from Unpaywall payload with error handling."""
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
        "error": "",
        "error_detail": "",
    }

    # Handle errors
    if payload.get("error"):
        row["oa_status"] = payload.get("error", "")
        row["error"] = payload.get("error", "")
        row["error_detail"] = payload.get("error_detail", "")

    return row


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(
        description="Fetch Unpaywall OA locations for DOI list (robust version)."
    )
    parser.add_argument("--in-bib", required=True, help="Input BibTeX file (included studies)")
    parser.add_argument("--email", default=None, help="Contact email (or UNPAYWALL_EMAIL env)")
    parser.add_argument("--api-base", default="https://api.unpaywall.org", help="Unpaywall API base URL")
    parser.add_argument("--sleep", type=float, default=0.2, help="Sleep seconds between requests")
    parser.add_argument("--max-retries", type=int, default=3, help="Max retries for transient errors")
    parser.add_argument("--max-records", type=int, default=None, help="Max DOIs to query")
    parser.add_argument("--out-csv", required=True, help="Output CSV path")
    parser.add_argument("--out-json", default=None, help="Output JSON path (raw payloads)")
    parser.add_argument("--out-log", required=True, help="Output log path")
    parser.add_argument("--continue-on-error", action="store_true", help="Continue processing on errors")
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

    # Error tracking
    error_count = 0
    success_count = 0
    error_types: Dict[str, int] = {}

    print(f"Processing {len(targets)} DOIs from {args.in_bib}...", file=sys.stderr)

    for idx, entry in enumerate(targets, start=1):
        print(f"  [{idx}/{len(targets)}] {entry['doi'][:40]}...", end=" ", file=sys.stderr)

        payload = fetch_unpaywall(args.api_base, entry["doi"], email, max_retries=args.max_retries)
        payloads.append(payload)
        rows.append(extract_row(entry, payload))

        # Track errors
        if payload.get("error"):
            error_count += 1
            error_type = payload.get("error", "unknown")
            error_types[error_type] = error_types.get(error_type, 0) + 1
            print(f"ERROR: {payload.get('error')}", file=sys.stderr)
        else:
            success_count += 1
            oa_status = payload.get("oa_status", "none")
            print(f"OK ({oa_status})", file=sys.stderr)

        if args.sleep:
            time.sleep(args.sleep)

    # Write CSV output
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
                "error",
                "error_detail",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    # Write JSON output if requested
    if args.out_json:
        out_json = Path(args.out_json)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(
            json.dumps(
                {
                    "timestamp": dt.datetime.utcnow().isoformat() + "Z",
                    "requested": len(targets),
                    "missing_doi": missing_doi,
                    "success_count": success_count,
                    "error_count": error_count,
                    "error_types": error_types,
                    "payloads": payloads,
                },
                indent=2,
            )
        )

    # Write log output with enhanced statistics
    out_log = Path(args.out_log)
    out_log.parent.mkdir(parents=True, exist_ok=True)
    log_lines = [
        f"# Unpaywall Fetch Log (Robust Version)",
        f"",
        f"**Date**: {dt.datetime.utcnow().isoformat()}Z",
        f"**Input BibTeX**: {args.in_bib}",
        f"**API Base**: {args.api_base}",
        f"",
        f"## Results Summary",
        f"",
        f"- Total records in BibTeX: {len(entries)}",
        f"- Records missing DOI: {missing_doi}",
        f"- DOIs queried: {len(targets)}",
        f"- Successful queries: {success_count}",
        f"- Failed queries: {error_count}",
        f"- Success rate: {success_count/len(targets)*100:.1f}%",
        f"",
        f"## Error Breakdown",
        f"",
    ]

    if error_types:
        for error_type, count in sorted(error_types.items(), key=lambda x: -x[1]):
            log_lines.append(f"- `{error_type}`: {count} ({count/len(targets)*100:.1f}%)")
    else:
        log_lines.append("- No errors ✅")

    log_lines.extend([
        f"",
        f"## Output Files",
        f"",
        f"- CSV: `{out_csv}`",
    ])

    if args.out_json:
        log_lines.append(f"- JSON: `{args.out_json}`")

    log_lines.append(f"- Log: `{out_log}`")

    out_log.write_text("\n".join(log_lines) + "\n")

    print(f"\n✅ Complete: {success_count} success, {error_count} errors", file=sys.stderr)
    print(f"📄 Output written to: {out_csv}", file=sys.stderr)
    print(f"📋 Log written to: {out_log}", file=sys.stderr)


if __name__ == "__main__":
    main()
