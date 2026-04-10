#!/usr/bin/env python3
"""Fetch PubMed records with E-utilities and write a BibTeX file."""

from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional
import os

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


def extract_year(pubdate: Dict[str, Any]) -> str:
    if not pubdate:
        return ""
    year = pubdate.get("Year")
    if year:
        return str(year)
    medline_date = pubdate.get("MedlineDate", "")
    match = re.search(r"(19|20)\d{2}", str(medline_date))
    return match.group(0) if match else ""


def format_authors(author_list: List[Dict[str, Any]]) -> str:
    if not author_list:
        return ""
    names = []
    for author in author_list:
        last = author.get("LastName")
        initials = author.get("Initials")
        if last and initials:
            names.append(f"{last}, {initials}")
        elif last:
            names.append(str(last))
    return " and ".join(names)


def build_bib_entry(article: Dict[str, Any], note: str) -> Optional[str]:
    medline = article.get("MedlineCitation", {})
    article_data = medline.get("Article", {})

    title = article_data.get("ArticleTitle", "")
    journal = article_data.get("Journal", {}).get("Title", "")
    journal_issue = article_data.get("Journal", {}).get("JournalIssue", {})
    pubdate = journal_issue.get("PubDate", {})

    year = extract_year(pubdate)
    authors = format_authors(article_data.get("AuthorList", []) or [])

    pmid = medline.get("PMID", "")

    doi = ""
    article_ids = article.get("PubmedData", {}).get("ArticleIdList", [])
    for item in article_ids:
        try:
            if item.attributes.get("IdType") == "doi":
                doi = str(item)
        except Exception:
            continue

    volume = journal_issue.get("Volume", "")
    issue = journal_issue.get("Issue", "")
    pages = article_data.get("Pagination", {}).get("MedlinePgn", "")

    first_author = authors.split(" and ")[0] if authors else "unknown"
    key = sanitize_key(f"{first_author}{year}{pmid}")

    fields = {
        "title": title,
        "author": authors,
        "journal": journal,
        "year": year,
        "volume": volume,
        "number": issue,
        "pages": pages,
        "doi": doi,
        "pmid": str(pmid),
        "note": note,
    }

    bib_lines = [f"@article{{{key},"]
    for k, v in fields.items():
        if v:
            bib_lines.append(f"  {k} = {{{bib_escape(str(v))}}},")
    bib_lines.append("}\n")
    return "\n".join(bib_lines)


def fetch_pubmed_records(
    query: str,
    email: str,
    api_key: Optional[str],
    mindate: Optional[str],
    maxdate: Optional[str],
    datetype: str,
    batch_size: int,
) -> Iterable[Dict[str, Any]]:
    from Bio import Entrez  # imported lazily

    Entrez.email = email
    if api_key:
        Entrez.api_key = api_key

    esearch_kwargs: Dict[str, Any] = {
        "db": "pubmed",
        "term": query,
        "usehistory": "y",
        "retmax": 0,
    }
    if mindate or maxdate:
        esearch_kwargs.update({"datetype": datetype})
        if mindate:
            esearch_kwargs["mindate"] = mindate
        if maxdate:
            esearch_kwargs["maxdate"] = maxdate

    handle = Entrez.esearch(**esearch_kwargs)
    search = Entrez.read(handle)
    handle.close()

    count = int(search.get("Count", 0))
    webenv = search.get("WebEnv")
    query_key = search.get("QueryKey")

    for start in range(0, count, batch_size):
        handle = Entrez.efetch(
            db="pubmed",
            rettype="medline",
            retmode="xml",
            retstart=start,
            retmax=batch_size,
            webenv=webenv,
            query_key=query_key,
        )
        records = Entrez.read(handle)
        handle.close()
        for article in records.get("PubmedArticle", []):
            yield article


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="Fetch PubMed records and write BibTeX.")
    parser.add_argument("--query", required=True, help="PubMed query string")
    parser.add_argument("--email", required=True, help="Contact email for NCBI")
    parser.add_argument("--api-key", default=None, help="NCBI API key (or PUBMED_API_KEY env)")
    parser.add_argument("--mindate", default=None, help="Start date (YYYY/MM/DD)")
    parser.add_argument("--maxdate", default=None, help="End date (YYYY/MM/DD)")
    parser.add_argument("--datetype", default="pdat", help="Date type (pdat or edat)")
    parser.add_argument("--batch-size", type=int, default=200, help="Fetch batch size")
    parser.add_argument("--note", default="round-01", help="Note to store in BibTeX entries")
    parser.add_argument("--out-bib", required=True, help="Output .bib path")
    parser.add_argument("--out-log", required=True, help="Output log path")
    args = parser.parse_args()

    out_bib = Path(args.out_bib)
    out_log = Path(args.out_log)

    entries: List[str] = []
    count = 0
    api_key = args.api_key or os.getenv("PUBMED_API_KEY")

    for record in fetch_pubmed_records(
        query=args.query,
        email=args.email,
        api_key=api_key,
        mindate=args.mindate,
        maxdate=args.maxdate,
        datetype=args.datetype,
        batch_size=args.batch_size,
    ):
        entry = build_bib_entry(record, note=args.note)
        if entry:
            entries.append(entry)
            count += 1

    out_bib.write_text("\n".join(entries))

    log_lines = [
        f"date: {dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "")}Z",
        f"query: {args.query}",
        f"count: {count}",
        f"mindate: {args.mindate or ''}",
        f"maxdate: {args.maxdate or ''}",
        f"datetype: {args.datetype}",
        f"batch_size: {args.batch_size}",
    ]
    out_log.write_text("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
