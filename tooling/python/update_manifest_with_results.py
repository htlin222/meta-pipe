#!/usr/bin/env python3
"""Update pdf_retrieval_manifest.csv with Unpaywall and download results."""

import argparse
import csv
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Update PDF retrieval manifest with Unpaywall and download results"
    )
    parser.add_argument(
        "--manifest", required=True, type=Path,
        help="Input PDF retrieval manifest CSV",
    )
    parser.add_argument(
        "--unpaywall", required=True, type=Path,
        help="Unpaywall results CSV",
    )
    parser.add_argument(
        "--pdf-dir", required=True, type=Path,
        help="Directory containing downloaded PDFs",
    )
    parser.add_argument(
        "--out-csv", required=True, type=Path,
        help="Output updated manifest CSV",
    )
    args = parser.parse_args()

    for path, label in [(args.manifest, "Manifest"), (args.unpaywall, "Unpaywall CSV")]:
        if not path.exists():
            raise SystemExit(f"{label} not found: {path}")

    # Load Unpaywall results
    unpaywall_data = {}
    with open(args.unpaywall, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            record_id = row["record_id"]
            unpaywall_data[record_id] = {
                "is_oa": row.get("is_oa", ""),
                "oa_status": row.get("oa_status", ""),
                "pdf_url": row.get("best_oa_pdf_url", ""),
            }

    # Update manifest
    updated_rows = []
    with open(args.manifest, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        for row in reader:
            record_id = row["record_id"]

            # Check if PDF was downloaded
            pdf_path = args.pdf_dir / f"{record_id}.pdf"
            if pdf_path.exists():
                row["retrieval_status"] = "downloaded"
                row["retrieval_method"] = "Unpaywall (automated)"
                row["pdf_path"] = str(pdf_path)
            elif record_id in unpaywall_data:
                oa_info = unpaywall_data[record_id]
                if oa_info["is_oa"] == "True":
                    row["retrieval_status"] = "OA-download-failed"
                    row["retrieval_method"] = f"Unpaywall ({oa_info['oa_status']})"
                    row["notes"] = (
                        f"403 error or access blocked. PDF URL: {oa_info['pdf_url'][:50]}"
                    )
                else:
                    row["retrieval_status"] = "closed-access"
                    row["retrieval_method"] = "Manual retrieval needed"
                    row["notes"] = "Not available via Unpaywall (closed access)"
            else:
                row["retrieval_status"] = "not-queried"
                row["notes"] = "No DOI for Unpaywall query"

            updated_rows.append(row)

    # Write updated manifest
    with open(args.out_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    # Summary
    status_counts = {}
    for row in updated_rows:
        status = row.get("retrieval_status", "unknown")
        status_counts[status] = status_counts.get(status, 0) + 1

    print("PDF Retrieval Status Summary")
    print("=" * 80)
    for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
        print(f"  {status:25s}: {count:2d} ({count / len(updated_rows) * 100:.1f}%)")
    print()
    print(f"Updated manifest saved to: {args.out_csv}")


if __name__ == "__main__":
    main()
