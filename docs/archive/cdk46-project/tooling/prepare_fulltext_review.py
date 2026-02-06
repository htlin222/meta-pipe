#!/usr/bin/env python3
"""
Prepare full-text review for Stage 04.
Extract records marked I or U from title/abstract screening.
"""

import csv
import sys
from pathlib import Path


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Prepare full-text review")
    parser.add_argument(
        "--screening-csv", required=True, help="Input screening decisions CSV"
    )
    parser.add_argument("--out-csv", required=True, help="Output full-text review CSV")
    parser.add_argument(
        "--out-manifest", required=True, help="Output PDF retrieval manifest"
    )
    args = parser.parse_args()

    # Read screening results
    records = []
    with open(args.screening_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Include records with decision I or U
            if row.get("decision_r1") in ["I", "U"]:
                records.append(row)

    print(f"Found {len(records)} records for full-text review")

    # Create full-text review CSV
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "record_id",
            "authors",
            "year",
            "title",
            "journal",
            "doi",
            "pmid",
            "abstract",
            "screening_decision",
            "screening_notes",
            # Full-text review fields
            "fulltext_available",
            "pdf_retrieved",
            "fulltext_decision",
            "exclusion_reason_fulltext",
            "prior_cdk46_percent",
            "study_design",
            "sample_size",
            "outcomes_reported",
            "reviewer_fulltext",
            "notes_fulltext",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for record in records:
            # Copy relevant fields
            row = {
                "record_id": record.get("record_id", ""),
                "authors": record.get("authors", ""),
                "year": record.get("year", ""),
                "title": record.get("title", ""),
                "journal": record.get("journal", ""),
                "doi": record.get("doi", ""),
                "pmid": record.get("pmid", ""),
                "abstract": record.get("abstract", ""),
                "screening_decision": record.get("decision_r1", ""),
                "screening_notes": record.get("notes", ""),
                # Initialize empty full-text fields
                "fulltext_available": "",
                "pdf_retrieved": "",
                "fulltext_decision": "",
                "exclusion_reason_fulltext": "",
                "prior_cdk46_percent": "",
                "study_design": "",
                "sample_size": "",
                "outcomes_reported": "",
                "reviewer_fulltext": "",
                "notes_fulltext": "",
            }
            writer.writerow(row)

    print(f"✓ Created full-text review CSV: {args.out_csv}")

    # Create PDF retrieval manifest
    with open(args.out_manifest, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "record_id",
            "title",
            "doi",
            "pmid",
            "retrieval_method",
            "pdf_path",
            "retrieval_status",
            "notes",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for record in records:
            row = {
                "record_id": record.get("record_id", ""),
                "title": record.get("title", "")[:100],  # Truncate long titles
                "doi": record.get("doi", ""),
                "pmid": record.get("pmid", ""),
                "retrieval_method": "",  # To be filled: unpaywall, pubmed, manual
                "pdf_path": "",
                "retrieval_status": "pending",
                "notes": "",
            }
            writer.writerow(row)

    print(f"✓ Created PDF retrieval manifest: {args.out_manifest}")

    # Summary statistics
    has_doi = sum(1 for r in records if r.get("doi"))
    has_pmid = sum(1 for r in records if r.get("pmid"))
    include_count = sum(1 for r in records if r.get("decision_r1") == "I")
    uncertain_count = sum(1 for r in records if r.get("decision_r1") == "U")

    print("\n--- Summary ---")
    print(f"Total records for full-text: {len(records)}")
    print(f"  Include (I): {include_count}")
    print(f"  Uncertain (U): {uncertain_count}")
    print(f"Records with DOI: {has_doi} ({has_doi / len(records) * 100:.1f}%)")
    print(f"Records with PMID: {has_pmid} ({has_pmid / len(records) * 100:.1f}%)")
    print("\nNext steps:")
    print("1. Retrieve PDFs using Unpaywall API or manual download")
    print("2. Review full-text against detailed eligibility criteria")
    print("3. Update fulltext_decision column (I/E)")
    print("4. Document exclusion_reason_fulltext if excluded")


if __name__ == "__main__":
    main()
