#!/usr/bin/env python3
"""Enrich a deduplicated BibTeX corpus with abstracts.

Reads a .bib file (typically ``02_search/round-XX/dedupe.bib``) and writes a
CSV (``03_screening/round-XX/records_with_abstracts.csv``) where every record
has an ``abstract`` column populated from whichever source succeeds first:

    PMID  → NCBI Entrez efetch (batched)
    DOI   → CrossRef /works/{doi}
    fallback → OpenAlex search by title+year

Records that still lack an abstract after all sources are marked with
``abstract_source = unavailable`` so downstream screening can treat them
deliberately instead of silently dropping them.

Usage:
    uv run ma-search-bibliography/scripts/enrich_abstracts.py \\
        --in-bib projects/X/02_search/round-01/dedupe.bib \\
        --out-csv projects/X/03_screening/round-01/records_with_abstracts.csv

Environment:
    ENTREZ_EMAIL   (recommended) — NCBI courtesy header
    CROSSREF_EMAIL (recommended) — CrossRef polite-pool header
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
import time
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import quote

try:
    import bibtexparser
except ImportError:
    print("ERROR: bibtexparser not installed. Run: uv add bibtexparser", file=sys.stderr)
    sys.exit(1)

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: uv add requests", file=sys.stderr)
    sys.exit(1)

from env_utils import load_dotenv

ENTREZ_EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
CROSSREF_WORKS = "https://api.crossref.org/works/"
OPENALEX_WORKS = "https://api.openalex.org/works"

BATCH_SIZE = 200
REQUEST_TIMEOUT = 30


def clean_text(text: str | None) -> str:
    if not text:
        return ""
    return " ".join(text.split()).strip()


def fetch_pubmed_abstracts(pmids: list[str], email: str | None) -> dict[str, str]:
    """Fetch abstracts for a list of PMIDs via Entrez efetch (batched)."""
    results: dict[str, str] = {}
    if not pmids:
        return results
    try:
        from Bio import Entrez  # type: ignore
    except ImportError:
        print("WARN: biopython not available; skipping Entrez lookups", file=sys.stderr)
        return results
    if email:
        Entrez.email = email

    for start in range(0, len(pmids), BATCH_SIZE):
        chunk = pmids[start : start + BATCH_SIZE]
        print(f"  Entrez efetch batch {start // BATCH_SIZE + 1}: {len(chunk)} PMIDs")
        try:
            handle = Entrez.efetch(
                db="pubmed",
                id=",".join(chunk),
                rettype="abstract",
                retmode="xml",
            )
            records = Entrez.read(handle)
            handle.close()
        except Exception as exc:
            print(f"  WARN: Entrez batch failed: {exc}", file=sys.stderr)
            continue

        for article in records.get("PubmedArticle", []):
            try:
                medline = article["MedlineCitation"]
                pmid = str(medline["PMID"])
                abstract_node = medline.get("Article", {}).get("Abstract", {})
                parts = abstract_node.get("AbstractText", [])
                if isinstance(parts, list):
                    text = " ".join(str(p) for p in parts if p)
                else:
                    text = str(parts)
                if text:
                    results[pmid] = clean_text(text)
            except Exception as exc:
                print(f"  WARN: could not parse PubMed record: {exc}", file=sys.stderr)
        time.sleep(0.4)  # stay under NCBI 3 req/s without API key
    return results


def fetch_crossref_abstract(doi: str, mailto: str | None) -> str:
    """Fetch abstract from CrossRef by DOI (often JATS-wrapped XML)."""
    if not doi:
        return ""
    headers = {"User-Agent": f"meta-pipe/1.0 (mailto:{mailto or 'unknown'})"}
    try:
        resp = requests.get(
            CROSSREF_WORKS + quote(doi, safe=""),
            headers=headers,
            timeout=REQUEST_TIMEOUT,
        )
        if resp.status_code != 200:
            return ""
        payload = resp.json().get("message", {})
    except Exception as exc:
        print(f"  WARN: CrossRef lookup failed for {doi}: {exc}", file=sys.stderr)
        return ""
    raw = payload.get("abstract", "")
    if not raw:
        return ""
    import re as _re

    no_tags = _re.sub(r"<[^>]+>", " ", raw)
    return clean_text(no_tags)


def fetch_openalex_abstract(title: str, year: str, mailto: str | None) -> str:
    """Fallback: search OpenAlex by title (+year) and reconstruct the inverted index."""
    if not title:
        return ""
    params = {
        "search": title[:250],
        "per-page": 5,
    }
    if year:
        params["filter"] = f"publication_year:{year}"
    if mailto:
        params["mailto"] = mailto
    try:
        resp = requests.get(OPENALEX_WORKS, params=params, timeout=REQUEST_TIMEOUT)
        if resp.status_code != 200:
            return ""
        works = resp.json().get("results", [])
    except Exception as exc:
        print(f"  WARN: OpenAlex lookup failed: {exc}", file=sys.stderr)
        return ""
    if not works:
        return ""
    best = works[0]
    inverted = best.get("abstract_inverted_index")
    if not inverted:
        return ""
    positions: list[tuple[int, str]] = []
    for word, idxs in inverted.items():
        for idx in idxs:
            positions.append((idx, word))
    positions.sort()
    return clean_text(" ".join(word for _, word in positions))


def extract_pmid(entry: dict[str, Any]) -> str:
    """BibTeX entries store PMID under various keys."""
    for key in ("pmid", "PMID", "eprint"):
        value = entry.get(key, "").strip()
        if value and value.isdigit():
            return value
    return ""


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--in-bib", required=True, help="Input .bib file")
    parser.add_argument("--out-csv", required=True, help="Output .csv file")
    parser.add_argument(
        "--min-coverage",
        type=float,
        default=0.0,
        help="Exit non-zero if abstract coverage below this fraction (0-1). Default 0.",
    )
    parser.add_argument(
        "--skip-crossref", action="store_true", help="Skip CrossRef fallback"
    )
    parser.add_argument(
        "--skip-openalex", action="store_true", help="Skip OpenAlex fallback"
    )
    args = parser.parse_args()

    entrez_email = os.environ.get("ENTREZ_EMAIL") or os.environ.get("NCBI_EMAIL")
    crossref_mailto = os.environ.get("CROSSREF_EMAIL") or entrez_email

    in_bib = Path(args.in_bib)
    out_csv = Path(args.out_csv)
    if not in_bib.exists():
        sys.exit(f"ERROR: {in_bib} not found")
    out_csv.parent.mkdir(parents=True, exist_ok=True)

    print(f"Reading {in_bib}...")
    with open(in_bib, "r", encoding="utf-8") as fh:
        bib_db = bibtexparser.load(fh)
    print(f"Loaded {len(bib_db.entries)} entries")

    records = []
    pmids_to_fetch: list[str] = []
    for entry in bib_db.entries:
        abstract = clean_text(entry.get("abstract") or entry.get("description") or "")
        record = {
            "record_id": entry.get("ID", ""),
            "entry_type": entry.get("ENTRYTYPE", ""),
            "authors": clean_text(entry.get("author", "")),
            "year": entry.get("year", "").strip(),
            "title": clean_text(entry.get("title", "")),
            "journal": clean_text(entry.get("journal", entry.get("publicationName", ""))),
            "doi": entry.get("doi", "").strip(),
            "pmid": extract_pmid(entry),
            "keywords": clean_text(entry.get("keywords", "")),
            "abstract": abstract,
            "abstract_source": "bibtex" if abstract else "",
        }
        if not abstract and record["pmid"]:
            pmids_to_fetch.append(record["pmid"])
        records.append(record)

    # Phase 1: Entrez batch lookup
    if pmids_to_fetch:
        print(f"Phase 1: Entrez efetch for {len(pmids_to_fetch)} PMIDs")
        pubmed = fetch_pubmed_abstracts(pmids_to_fetch, entrez_email)
        for record in records:
            if record["abstract"]:
                continue
            pubmed_abstract = pubmed.get(record["pmid"])
            if pubmed_abstract:
                record["abstract"] = pubmed_abstract
                record["abstract_source"] = "pubmed"

    # Phase 2: CrossRef by DOI
    if not args.skip_crossref:
        needs = [r for r in records if not r["abstract"] and r["doi"]]
        if needs:
            print(f"Phase 2: CrossRef lookup for {len(needs)} DOIs")
        for i, record in enumerate(needs, 1):
            if i % 25 == 0:
                print(f"  {i}/{len(needs)} CrossRef lookups done")
            abstract = fetch_crossref_abstract(record["doi"], crossref_mailto)
            if abstract:
                record["abstract"] = abstract
                record["abstract_source"] = "crossref"
            time.sleep(0.1)

    # Phase 3: OpenAlex fallback
    if not args.skip_openalex:
        needs = [r for r in records if not r["abstract"] and r["title"]]
        if needs:
            print(f"Phase 3: OpenAlex fallback for {len(needs)} records")
        for i, record in enumerate(needs, 1):
            if i % 25 == 0:
                print(f"  {i}/{len(needs)} OpenAlex lookups done")
            abstract = fetch_openalex_abstract(
                record["title"], record["year"], crossref_mailto
            )
            if abstract:
                record["abstract"] = abstract
                record["abstract_source"] = "openalex"
            time.sleep(0.1)

    for record in records:
        if not record["abstract"]:
            record["abstract_source"] = "unavailable"

    fieldnames = [
        "record_id",
        "entry_type",
        "authors",
        "year",
        "title",
        "journal",
        "doi",
        "pmid",
        "keywords",
        "abstract",
        "abstract_source",
    ]
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    total = len(records)
    with_abs = sum(1 for r in records if r["abstract"])
    coverage = with_abs / total if total else 0.0
    breakdown: dict[str, int] = {}
    for record in records:
        breakdown[record["abstract_source"]] = (
            breakdown.get(record["abstract_source"], 0) + 1
        )

    print(f"\n{'=' * 60}")
    print("ABSTRACT ENRICHMENT SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total records:    {total}")
    print(f"With abstract:    {with_abs} ({coverage * 100:.1f}%)")
    print("Sources:")
    for source, count in sorted(breakdown.items(), key=lambda kv: -kv[1]):
        print(f"  {source:<12} {count}")
    print(f"{'=' * 60}")
    print(f"\nOutput: {out_csv}")

    if coverage < args.min_coverage:
        sys.exit(
            f"ERROR: coverage {coverage * 100:.1f}% below "
            f"--min-coverage {args.min_coverage * 100:.1f}%"
        )


if __name__ == "__main__":
    main()
