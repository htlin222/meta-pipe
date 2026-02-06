#!/usr/bin/env python3
"""Analyze Unpaywall results and generate summary."""

import csv
import sys
from pathlib import Path


def main():
    csv_path = Path("../../04_fulltext/round-01/unpaywall_results.csv")

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

    print(f"📊 Unpaywall Analysis Results")
    print(f"=" * 50)
    print(f"Total records queried: {total}")
    print(f"Open Access (OA): {oa_count} ({oa_count / total * 100:.1f}%)")
    print(f"  - With PDF URL: {pdf_available} ({pdf_available / total * 100:.1f}%)")
    print(f"Closed Access: {closed_count} ({closed_count / total * 100:.1f}%)")
    print()

    if oa_types:
        print(f"OA Types:")
        for oa_type, count in sorted(oa_types.items(), key=lambda x: -x[1]):
            print(f"  - {oa_type}: {count}")
        print()

    if host_types:
        print(f"Host Types:")
        for host_type, count in sorted(host_types.items(), key=lambda x: -x[1]):
            print(f"  - {host_type}: {count}")
        print()

    print(f"📋 Next Steps:")
    print(
        f"  1. PDF retrieval success rate: {pdf_available}/{total} ({pdf_available / total * 100:.1f}%)"
    )
    print(f"  2. Need manual retrieval: {closed_count} closed access records")
    print(f"  3. Institutional access may help with {closed_count} additional PDFs")


if __name__ == "__main__":
    main()
