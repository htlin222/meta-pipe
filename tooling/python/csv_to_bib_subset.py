#!/usr/bin/env python3
"""Extract BibTeX entries for records in CSV manifest."""

import argparse
import csv
import sys
from pathlib import Path

import bibtexparser


def main():
    parser = argparse.ArgumentParser(
        description="Extract BibTeX subset from CSV manifest"
    )
    parser.add_argument("--in-csv", required=True, help="Input CSV manifest")
    parser.add_argument("--in-bib", required=True, help="Full BibTeX file")
    parser.add_argument("--out-bib", required=True, help="Output BibTeX subset")
    args = parser.parse_args()

    # Read record IDs from CSV
    record_ids = set()
    with open(args.in_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get("record_id"):
                record_ids.add(row["record_id"])

    print(f"Found {len(record_ids)} record IDs in CSV")

    # Read full BibTeX
    with open(args.in_bib, "r", encoding="utf-8") as f:
        bib_database = bibtexparser.load(f)

    print(f"Loaded {len(bib_database.entries)} entries from BibTeX")

    # Filter entries
    matched_entries = []
    for entry in bib_database.entries:
        if entry.get("ID") in record_ids:
            matched_entries.append(entry)

    print(f"Matched {len(matched_entries)} entries")

    # Create output database
    output_db = bibtexparser.bibdatabase.BibDatabase()
    output_db.entries = matched_entries

    # Write output
    with open(args.out_bib, "w", encoding="utf-8") as f:
        bibtexparser.dump(output_db, f)

    print(f"Wrote {len(matched_entries)} entries to {args.out_bib}")


if __name__ == "__main__":
    main()
