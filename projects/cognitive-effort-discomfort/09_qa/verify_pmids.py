#!/usr/bin/env python3
"""Verify PMIDs exist in PubMed and titles match BibTeX entries.

For each entry with a PMID in included.bib:
  1. Fetch the PubMed record via E-utilities efetch
  2. Compare returned title to BibTeX title (similarity threshold 0.7)
  3. Report: verified, invalid (PMID not found), mismatched (title differs)

Usage:
    PYTHONPATH=ma-search-bibliography/scripts:tooling/python \
    uv run --project tooling/python projects/cognitive-effort-discomfort/09_qa/verify_pmids.py
"""

from __future__ import annotations

import os
import re
import sys
import time
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ma-search-bibliography" / "scripts"))
from env_utils import load_dotenv


def clean_title(title: str) -> str:
    title = title.lower()
    title = re.sub(r"[^\w\s]", " ", title)
    return re.sub(r"\s+", " ", title).strip()


def title_similarity(t1: str, t2: str) -> float:
    c1 = clean_title(t1)
    c2 = clean_title(t2)
    if not c1 or not c2:
        return 0.0
    return SequenceMatcher(None, c1, c2).ratio()


def main():
    load_dotenv()
    project = Path(__file__).resolve().parents[1]
    bib_path = project / "03_screening" / "round-01" / "included.bib"

    from bibtexparser import loads
    bib = loads(bib_path.read_text())

    # Collect entries with PMIDs
    pmid_entries = []
    for entry in bib.entries:
        pmid = entry.get("pmid", "").strip()
        if pmid and pmid.isdigit():
            pmid_entries.append({
                "key": entry.get("ID", ""),
                "pmid": pmid,
                "title": entry.get("title", ""),
                "doi": entry.get("doi", ""),
            })

    if not pmid_entries:
        print("No entries with PMIDs found.")
        return

    print(f"Found {len(pmid_entries)} entries with PMIDs to verify.")

    # Import BioPython Entrez
    from Bio import Entrez
    Entrez.email = "cognitive-effort-review@meta-pipe.org"
    api_key = os.getenv("PUBMED_API_KEY")
    if api_key:
        Entrez.api_key = api_key

    results = []
    batch_size = 20

    for i in range(0, len(pmid_entries), batch_size):
        batch = pmid_entries[i:i + batch_size]
        pmids = [e["pmid"] for e in batch]

        try:
            handle = Entrez.efetch(db="pubmed", id=",".join(pmids), retmode="xml")
            records = Entrez.read(handle)
            handle.close()
        except Exception as e:
            for entry in batch:
                results.append({**entry, "status": "error", "pubmed_title": "", "similarity": 0, "note": str(e)})
            time.sleep(1)
            continue

        # Map PMID to fetched article
        fetched = {}
        for article in records.get("PubmedArticle", []):
            medline = article.get("MedlineCitation", {})
            pm = str(medline.get("PMID", ""))
            art_title = medline.get("Article", {}).get("ArticleTitle", "")
            fetched[pm] = art_title

        for entry in batch:
            pmid = entry["pmid"]
            if pmid in fetched:
                pubmed_title = fetched[pmid]
                sim = title_similarity(entry["title"], pubmed_title)
                if sim >= 0.7:
                    status = "verified"
                else:
                    status = "mismatched"
                results.append({
                    **entry,
                    "status": status,
                    "pubmed_title": pubmed_title,
                    "similarity": round(sim, 3),
                    "note": "",
                })
            else:
                results.append({
                    **entry,
                    "status": "invalid",
                    "pubmed_title": "",
                    "similarity": 0,
                    "note": "PMID not found in PubMed",
                })

        time.sleep(0.5)

    # Generate report
    verified = [r for r in results if r["status"] == "verified"]
    invalid = [r for r in results if r["status"] == "invalid"]
    mismatched = [r for r in results if r["status"] == "mismatched"]
    errors = [r for r in results if r["status"] == "error"]

    lines = [
        "# PMID Verification Report\n",
        f"**Total entries with PMIDs**: {len(results)}\n",
        "## Summary\n",
        f"| Status | Count |",
        f"|--------|-------|",
        f"| Verified (PMID exists + title matches) | {len(verified)} |",
        f"| Invalid (PMID not found) | {len(invalid)} |",
        f"| Mismatched (PMID exists, title differs) | {len(mismatched)} |",
        f"| Error (API failure) | {len(errors)} |",
        "",
    ]

    if invalid:
        lines.append("## Invalid PMIDs\n")
        lines.append("| Key | PMID | BibTeX Title | Note |")
        lines.append("|-----|------|-------------|------|")
        for r in invalid:
            lines.append(f"| `{r['key']}` | {r['pmid']} | {r['title'][:60]}... | {r['note']} |")
        lines.append("")

    if mismatched:
        lines.append("## Mismatched Titles\n")
        lines.append("| Key | PMID | Similarity | BibTeX Title | PubMed Title |")
        lines.append("|-----|------|-----------|--------------|-------------|")
        for r in mismatched:
            lines.append(f"| `{r['key']}` | {r['pmid']} | {r['similarity']:.1%} | {r['title'][:40]}... | {r['pubmed_title'][:40]}... |")
        lines.append("")

    if verified:
        lines.append(f"## Verified PMIDs ({len(verified)} entries)\n")
        lines.append("<details>")
        lines.append("<summary>All verified — click to expand</summary>\n")
        lines.append("| Key | PMID | Similarity |")
        lines.append("|-----|------|-----------|")
        for r in verified:
            lines.append(f"| `{r['key']}` | {r['pmid']} | {r['similarity']:.1%} |")
        lines.append("</details>\n")

    # Pass/fail
    if invalid or mismatched:
        lines.append(f"\n**Result**: FAIL — {len(invalid)} invalid, {len(mismatched)} mismatched")
    else:
        lines.append(f"\n**Result**: PASS — all {len(verified)} PMIDs verified with matching titles")

    report_path = project / "09_qa" / "pmid_verification_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nReport written to {report_path}")
    print(f"  Verified: {len(verified)}")
    print(f"  Invalid: {len(invalid)}")
    print(f"  Mismatched: {len(mismatched)}")
    print(f"  Errors: {len(errors)}")


if __name__ == "__main__":
    main()
