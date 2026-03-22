#!/usr/bin/env python3
"""Fetch Semantic Scholar records and write a BibTeX file."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from env_utils import load_dotenv

S2_API_BASE = "https://api.semanticscholar.org/graph/v1"
S2_FIELDS = "paperId,title,authors,year,externalIds,journal,citationCount,abstract"
MAX_RETRIES = 4


def s2_get(url: str, params: Dict[str, Any], timeout: int = 60) -> requests.Response:
    """GET with exponential backoff for 429 rate limits."""
    for attempt in range(MAX_RETRIES + 1):
        resp = requests.get(url, params=params, timeout=timeout)
        if resp.status_code == 429:
            wait = 2 ** (attempt + 1)
            print(f"  Rate limited, waiting {wait}s (attempt {attempt + 1}/{MAX_RETRIES + 1})")
            time.sleep(wait)
            continue
        return resp
    return resp  # return last response even if still 429


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
    return " and ".join(a.get("name", "") for a in authors if a.get("name"))


def build_bib_entry(paper: Dict[str, Any], note: str) -> Optional[str]:
    title = paper.get("title", "")
    if not title:
        return None

    authors = format_authors(paper.get("authors", []))
    year = str(paper.get("year", "")) if paper.get("year") else ""
    ext_ids = paper.get("externalIds") or {}
    doi = ext_ids.get("DOI", "")
    pmid = ext_ids.get("PubMed", "")
    journal_info = paper.get("journal") or {}
    journal = journal_info.get("name", "")
    volume = journal_info.get("volume", "")
    pages = journal_info.get("pages", "")
    s2id = paper.get("paperId", "")

    first_author = authors.split(" and ")[0] if authors else "unknown"
    key = sanitize_key(f"{first_author}{year}{s2id[:6]}")

    fields = {
        "title": title,
        "author": authors,
        "journal": journal,
        "year": year,
        "volume": volume,
        "pages": pages,
        "doi": doi,
        "pmid": pmid,
        "note": note,
        "s2id": s2id,
    }

    bib_lines = [f"@article{{{key},"]
    for k, v in fields.items():
        if v:
            bib_lines.append(f"  {k} = {{{bib_escape(str(v))}}},")
    bib_lines.append("}\n")
    return "\n".join(bib_lines)


def search_s2(
    query: str,
    limit: int = 100,
    offset: int = 0,
    year: Optional[str] = None,
    fields_of_study: Optional[str] = None,
) -> Dict[str, Any]:
    url = f"{S2_API_BASE}/paper/search"
    params: Dict[str, Any] = {
        "query": query,
        "limit": min(limit, 100),
        "offset": offset,
        "fields": S2_FIELDS,
    }
    if year:
        params["year"] = year
    if fields_of_study:
        params["fieldsOfStudy"] = fields_of_study
    resp = s2_get(url, params=params, timeout=60)
    resp.raise_for_status()
    return resp.json()


def fetch_paper_by_doi(doi: str) -> Optional[Dict[str, Any]]:
    url = f"{S2_API_BASE}/paper/DOI:{doi}"
    params = {"fields": S2_FIELDS}
    resp = s2_get(url, params=params, timeout=30)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()


def fetch_citations(paper_id: str, limit: int = 100) -> List[Dict[str, Any]]:
    url = f"{S2_API_BASE}/paper/{paper_id}/citations"
    params = {"fields": S2_FIELDS, "limit": min(limit, 1000)}
    resp = s2_get(url, params=params, timeout=60)
    if resp.status_code == 404:
        return []
    resp.raise_for_status()
    data = resp.json()
    if not data or not data.get("data"):
        return []
    return [c["citingPaper"] for c in data["data"] if c.get("citingPaper")]


def fetch_references(paper_id: str, limit: int = 100) -> List[Dict[str, Any]]:
    url = f"{S2_API_BASE}/paper/{paper_id}/references"
    params = {"fields": S2_FIELDS, "limit": min(limit, 1000)}
    resp = s2_get(url, params=params, timeout=60)
    if resp.status_code == 404:
        return []
    resp.raise_for_status()
    data = resp.json()
    if not data or not data.get("data"):
        return []
    return [r["citedPaper"] for r in data["data"] if r.get("citedPaper")]


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Fetch Semantic Scholar records and write BibTeX.")
    parser.add_argument("--query", default=None, help="Search query string")
    parser.add_argument("--doi", action="append", default=[], help="Fetch specific DOI(s)")
    parser.add_argument("--cite-chain", action="append", default=[],
                        help="DOI(s) to fetch citations+references for")
    parser.add_argument("--limit", type=int, default=100, help="Max results per query page")
    parser.add_argument("--max-results", type=int, default=200, help="Total max search results")
    parser.add_argument("--year", default=None, help="Year range (e.g. 2005-2025)")
    parser.add_argument("--fields-of-study", default=None, help="Filter by field (e.g. Psychology)")
    parser.add_argument("--note", default="round-01", help="Note for BibTeX entries")
    parser.add_argument("--sleep", type=float, default=1.0, help="Sleep between API calls")
    parser.add_argument("--out-bib", required=True, help="Output .bib path")
    parser.add_argument("--out-log", required=True, help="Output log path")
    args = parser.parse_args()

    papers: Dict[str, Dict[str, Any]] = {}  # keyed by paperId to dedupe

    # 1. Keyword search
    if args.query:
        offset = 0
        total = 0
        while total < args.max_results:
            batch = min(args.limit, args.max_results - total)
            data = search_s2(
                query=args.query,
                limit=batch,
                offset=offset,
                year=args.year,
                fields_of_study=args.fields_of_study,
            )
            results = data.get("data", [])
            if not results:
                break
            for p in results:
                pid = p.get("paperId")
                if pid:
                    papers[pid] = p
                    total += 1
            offset += len(results)
            if data.get("total", 0) <= offset:
                break
            if total < args.max_results:
                time.sleep(args.sleep)

    # 2. Fetch specific DOIs
    for doi in args.doi:
        paper = fetch_paper_by_doi(doi)
        if paper and paper.get("paperId"):
            papers[paper["paperId"]] = paper
        time.sleep(args.sleep)

    # 3. Citation chaining
    chain_count = 0
    for doi in args.cite_chain:
        paper = fetch_paper_by_doi(doi)
        if not paper or not paper.get("paperId"):
            continue
        pid = paper["paperId"]
        papers[pid] = paper
        time.sleep(args.sleep)

        # Forward citations (papers that cite this one)
        citing = fetch_citations(pid, limit=50)
        for c in citing:
            cpid = c.get("paperId")
            if cpid:
                papers[cpid] = c
                chain_count += 1
        time.sleep(args.sleep)

        # Backward references (papers this one cites)
        refs = fetch_references(pid, limit=50)
        for r in refs:
            rpid = r.get("paperId")
            if rpid:
                papers[rpid] = r
                chain_count += 1
        time.sleep(args.sleep)

    # Build BibTeX entries
    entries: List[str] = []
    for paper in papers.values():
        entry = build_bib_entry(paper, note=args.note)
        if entry:
            entries.append(entry)

    Path(args.out_bib).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_bib).write_text("\n".join(entries))

    log_lines = [
        f"date: {dt.datetime.utcnow().isoformat()}Z",
        f"query: {args.query or ''}",
        f"doi_lookups: {len(args.doi)}",
        f"citation_chains: {len(args.cite_chain)}",
        f"chain_papers: {chain_count}",
        f"total_unique: {len(papers)}",
        f"bib_entries: {len(entries)}",
        f"year_filter: {args.year or ''}",
    ]
    Path(args.out_log).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out_log).write_text("\n".join(log_lines) + "\n")

    print(f"Semantic Scholar: {len(entries)} entries → {args.out_bib}")


if __name__ == "__main__":
    main()
