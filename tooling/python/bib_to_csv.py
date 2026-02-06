#!/usr/bin/env python3
"""
Convert BibTeX file to CSV for screening.
Extracts: record_id, authors, year, title, journal, abstract
"""

import sys
import csv
import argparse
from pathlib import Path

try:
    import bibtexparser
except ImportError:
    print(
        "ERROR: bibtexparser not installed. Run: uv add bibtexparser", file=sys.stderr
    )
    sys.exit(1)


def extract_fields(entry):
    """Extract relevant fields from BibTeX entry."""
    return {
        "record_id": entry.get("ID", ""),
        "entry_type": entry.get("ENTRYTYPE", ""),
        "authors": entry.get("author", ""),
        "year": entry.get("year", ""),
        "title": entry.get("title", ""),
        "journal": entry.get("journal", entry.get("publicationName", "")),
        "abstract": entry.get("abstract", entry.get("description", "")),
        "doi": entry.get("doi", ""),
        "pmid": entry.get("pmid", ""),
        "keywords": entry.get("keywords", ""),
    }


def main():
    parser = argparse.ArgumentParser(description="Convert BibTeX to CSV for screening")
    parser.add_argument("--in-bib", required=True, help="Input .bib file")
    parser.add_argument("--out-csv", required=True, help="Output .csv file")
    args = parser.parse_args()

    # Read BibTeX
    print(f"Reading {args.in_bib}...")
    with open(args.in_bib, "r", encoding="utf-8") as f:
        bib_database = bibtexparser.load(f)

    print(f"Found {len(bib_database.entries)} entries")

    # Extract fields
    records = [extract_fields(entry) for entry in bib_database.entries]

    # Write CSV
    print(f"Writing {args.out_csv}...")
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "record_id",
            "entry_type",
            "authors",
            "year",
            "title",
            "journal",
            "abstract",
            "doi",
            "pmid",
            "keywords",
            "decision_r1",
            "decision_r2",
            "final_decision",
            "exclusion_reason",
            "notes",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for record in records:
            # Add empty screening columns
            record["decision_r1"] = ""
            record["decision_r2"] = ""
            record["final_decision"] = ""
            record["exclusion_reason"] = ""
            record["notes"] = ""
            writer.writerow(record)

    print(f"✓ Created {args.out_csv} with {len(records)} records")
    print("\nNext steps:")
    print("1. Fill in decision_r1 and decision_r2 columns (include/exclude)")
    print("2. Reconcile discrepancies in final_decision column")
    print("3. Document exclusion_reason for excluded records")


if __name__ == "__main__":
    main()
