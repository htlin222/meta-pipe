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
    print(
        "ERROR: bibtexparser not installed. Run: uv add bibtexparser", file=sys.stderr
    )
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
    # Direct efetch + ElementTree rather than Bio.Entrez: Entrez.read() builds a
    # deeply-validated object graph and measured ~2.5 min per 200-PMID batch,
    # while the same HTTP fetch takes ~8.5s. Parsing is the bottleneck, not NCBI.
    # POST is used because 200 comma-joined PMIDs overflow a sane URL length.
    import xml.etree.ElementTree as ET

    api_key = os.environ.get("PUBMED_API_KEY") or os.environ.get("NCBI_API_KEY")

    for start in range(0, len(pmids), BATCH_SIZE):
        chunk = pmids[start : start + BATCH_SIZE]
        print(f"  Entrez efetch batch {start // BATCH_SIZE + 1}: {len(chunk)} PMIDs")
        data = {
            "db": "pubmed",
            "id": ",".join(chunk),
            "rettype": "abstract",
            "retmode": "xml",
        }
        if email:
            data["email"] = email
        if api_key:
            data["api_key"] = api_key
        # Retry: a transient 400/5xx here silently loses 200 records' abstracts,
        # which downstream looks like "no abstract available" rather than a failed
        # fetch. Never let a network blip masquerade as missing data.
        root = None
        for attempt in range(1, 4):
            try:
                resp = requests.post(ENTREZ_EFETCH, data=data, timeout=REQUEST_TIMEOUT)
                resp.raise_for_status()
                root = ET.fromstring(resp.content)
                break
            except Exception as exc:
                if attempt == 3:
                    print(
                        f"  WARN: Entrez batch {start // BATCH_SIZE + 1} FAILED after "
                        f"3 attempts ({len(chunk)} PMIDs lost): {exc}",
                        file=sys.stderr,
                    )
                else:
                    print(
                        f"  retry {attempt}/3 for batch {start // BATCH_SIZE + 1}: {exc}",
                        file=sys.stderr,
                    )
                    time.sleep(2 * attempt)
        if root is None:
            continue

        for article in root.iter("PubmedArticle"):
            pmid_node = article.find("./MedlineCitation/PMID")
            if pmid_node is None or not pmid_node.text:
                continue
            parts = [
                "".join(node.itertext())
                for node in article.findall(
                    "./MedlineCitation/Article/Abstract/AbstractText"
                )
            ]
            text = clean_text(" ".join(p for p in parts if p))
            if text:
                results[pmid_node.text.strip()] = text
        time.sleep(0.15 if api_key else 0.4)  # NCBI: 10 req/s keyed, 3 req/s unkeyed
    return results


ENTREZ_ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"


def _resolve_dois_to_pmids(records: list, workers: int) -> dict[str, str]:
    """Look each record's DOI up in PubMed via the [AID] field. {record_id: pmid}."""
    from concurrent.futures import ThreadPoolExecutor, as_completed

    api_key = os.environ.get("PUBMED_API_KEY") or os.environ.get("NCBI_API_KEY")

    def lookup(doi: str) -> str:
        params = {
            "db": "pubmed",
            "term": f'"{doi}"[AID]',
            "retmode": "json",
            "retmax": 1,
        }
        if api_key:
            params["api_key"] = api_key
        try:
            resp = requests.get(ENTREZ_ESEARCH, params=params, timeout=REQUEST_TIMEOUT)
            if resp.status_code != 200:
                return ""
            ids = resp.json().get("esearchresult", {}).get("idlist", [])
            return ids[0] if ids else ""
        except Exception:  # noqa: BLE001 - a failed lookup just means no PMID
            return ""

    out: dict[str, str] = {}
    done = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(lookup, r["doi"]): r for r in records}
        for fut in as_completed(futures):
            record = futures[fut]
            done += 1
            try:
                pmid = fut.result()
            except Exception:  # noqa: BLE001
                pmid = ""
            if pmid:
                out[record["record_id"]] = pmid
            if done % 200 == 0 or done == len(records):
                print(f"  {done}/{len(records)} DOI lookups done ({len(out)} resolved)")
    return out


def _fill_concurrently(needs: list, fetch, source_label: str, workers: int) -> None:
    """Run a per-record lookup concurrently and fill in whatever comes back.

    These phases are network-bound one-request-per-record loops: serially they
    ran at ~8 lookups/min, so ~1,000 DOIs took roughly two hours. Threads are
    the right fix (all the time is spent waiting on HTTP, not on CPU).
    Failures are swallowed per record — a record simply keeps an empty abstract
    and is later marked `unavailable`, never dropped.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    done = 0
    filled = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(fetch, r): r for r in needs}
        for fut in as_completed(futures):
            record = futures[fut]
            done += 1
            try:
                abstract = fut.result()
            except Exception:  # noqa: BLE001 - one bad record must not abort the phase
                abstract = ""
            if abstract:
                record["abstract"] = abstract
                record["abstract_source"] = source_label
                filled += 1
            if done % 100 == 0 or done == len(needs):
                print(
                    f"  {done}/{len(needs)} {source_label} lookups done ({filled} filled)"
                )


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
    parser.add_argument(
        "--workers",
        type=int,
        default=16,
        help=(
            "Concurrent HTTP workers for the CrossRef/OpenAlex phases (default: 16). "
            "These phases are one request per record and network-bound; serially they "
            "run at roughly 8 lookups/min, so ~1000 DOIs takes ~2h."
        ),
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
            "journal": clean_text(
                entry.get("journal", entry.get("publicationName", ""))
            ),
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

    # Phase 1b: DOI -> PMID, then a second Entrez pass.
    # Records found only by Scopus often ARE indexed in PubMed; they simply did
    # not match the PubMed query, so they arrive with a DOI but no PMID. Looking
    # the DOI up in PubMed recovers a full MEDLINE abstract, which is better
    # quality than the CrossRef fallback and avoids sending the record to
    # title-only screening.
    if not args.skip_crossref:
        need_pmid = [
            r for r in records if not r["abstract"] and r["doi"] and not r["pmid"]
        ]
        if need_pmid:
            print(
                f"Phase 1b: DOI->PMID resolution for {len(need_pmid)} records "
                f"({args.workers} workers)"
            )
            resolved = _resolve_dois_to_pmids(need_pmid, args.workers)
            if resolved:
                print(f"  resolved {len(resolved)} PMIDs; refetching abstracts")
                more = fetch_pubmed_abstracts(list(resolved.values()), entrez_email)
                filled = 0
                for record in need_pmid:
                    pmid = resolved.get(record["record_id"])
                    if not pmid:
                        continue
                    record["pmid"] = pmid
                    abstract = more.get(pmid)
                    if abstract:
                        record["abstract"] = abstract
                        record["abstract_source"] = "pubmed_via_doi"
                        filled += 1
                print(f"  Phase 1b filled {filled} abstracts")

    # Phase 2: CrossRef by DOI
    if not args.skip_crossref:
        needs = [r for r in records if not r["abstract"] and r["doi"]]
        if needs:
            print(
                f"Phase 2: CrossRef lookup for {len(needs)} DOIs "
                f"({args.workers} workers)"
            )
            _fill_concurrently(
                needs,
                lambda r: fetch_crossref_abstract(r["doi"], crossref_mailto),
                "crossref",
                args.workers,
            )

    # Phase 3: OpenAlex fallback
    if not args.skip_openalex:
        needs = [r for r in records if not r["abstract"] and r["title"]]
        if needs:
            print(
                f"Phase 3: OpenAlex fallback for {len(needs)} records "
                f"({args.workers} workers)"
            )
            _fill_concurrently(
                needs,
                lambda r: fetch_openalex_abstract(
                    r["title"], r["year"], crossref_mailto
                ),
                "openalex",
                args.workers,
            )

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
