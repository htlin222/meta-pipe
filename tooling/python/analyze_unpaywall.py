#!/usr/bin/env python3
"""Analyze Unpaywall results and generate summary."""

import argparse
import csv
from pathlib import Path


def analyze(csv_path):
    """Analyze Unpaywall CSV and print summary."""
    total = 0
    oa_count = 0
    closed_count = 0
    pdf_available = 0
    oa_types = {}
    host_types = {}

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            total += 1
            is_oa = row.get("is_oa", "").strip()
            oa_status = row.get("oa_status", "").strip()
            pdf_url = row.get("best_oa_pdf_url", "").strip()
            host_type = row.get("host_type", "").strip()

            if is_oa == "True":
                oa_count += 1
                if pdf_url:
                    pdf_available += 1
                if oa_status:
                    oa_types[oa_status] = oa_types.get(oa_status, 0) + 1
                if host_type:
                    host_types[host_type] = host_types.get(host_type, 0) + 1
            elif is_oa == "False":
                closed_count += 1

    if total == 0:
        raise SystemExit("No records found in CSV")

    print("Unpaywall Analysis Results")
    print("=" * 50)
    print(f"Total records queried: {total}")
    print(f"Open Access (OA): {oa_count} ({oa_count / total * 100:.1f}%)")
    print(f"  - With PDF URL: {pdf_available} ({pdf_available / total * 100:.1f}%)")
    print(f"Closed Access: {closed_count} ({closed_count / total * 100:.1f}%)")
    print()

    if oa_types:
        print("OA Types:")
        for oa_type, count in sorted(oa_types.items(), key=lambda x: -x[1]):
            print(f"  - {oa_type}: {count}")
        print()

    if host_types:
        print("Host Types:")
        for host_type, count in sorted(host_types.items(), key=lambda x: -x[1]):
            print(f"  - {host_type}: {count}")
        print()

    print("Next Steps:")
    print(
        f"  1. PDF retrieval success rate: {pdf_available}/{total} ({pdf_available / total * 100:.1f}%)"
    )
    print(f"  2. Need manual retrieval: {closed_count} closed access records")
    print(f"  3. Institutional access may help with {closed_count} additional PDFs")


def main():
    parser = argparse.ArgumentParser(
        description="Analyze Unpaywall results and generate summary"
    )
    parser.add_argument(
        "--in-csv", required=True, type=Path,
        help="Unpaywall results CSV (must have is_oa, oa_status, best_oa_pdf_url, host_type)",
    )
    args = parser.parse_args()

    if not args.in_csv.exists():
        raise SystemExit(f"Input CSV not found: {args.in_csv}")

    analyze(args.in_csv)


if __name__ == "__main__":
    main()
