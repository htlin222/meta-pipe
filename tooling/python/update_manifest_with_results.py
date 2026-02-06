#!/usr/bin/env python3
"""Update pdf_retrieval_manifest.csv with Unpaywall and download results."""

import csv
from pathlib import Path


def main():
    # Input files
    manifest_path = Path("../../04_fulltext/round-01/pdf_retrieval_manifest.csv")
    unpaywall_path = Path("../../04_fulltext/round-01/unpaywall_results.csv")
    pdf_dir = Path("../../04_fulltext/round-01/pdfs")

    # Load Unpaywall results
    unpaywall_data = {}
    with open(unpaywall_path, "r", encoding="utf-8") as f:
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
    with open(manifest_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames

        for row in reader:
            record_id = row["record_id"]

            # Check if PDF was downloaded
            pdf_path = pdf_dir / f"{record_id}.pdf"
            if pdf_path.exists():
                row["retrieval_status"] = "downloaded"
                row["retrieval_method"] = "Unpaywall (automated)"
                row["pdf_path"] = str(
                    pdf_path.relative_to(Path("../../04_fulltext/round-01"))
                )
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
    output_path = Path("../../04_fulltext/round-01/pdf_retrieval_manifest_updated.csv")
    with open(output_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

    # Summary
    status_counts = {}
    for row in updated_rows:
        status = row["retrieval_status"]
        status_counts[status] = status_counts.get(status, 0) + 1

    print("📊 PDF Retrieval Status Summary")
    print("=" * 80)
    for status, count in sorted(status_counts.items(), key=lambda x: -x[1]):
        print(f"  {status:25s}: {count:2d} ({count / len(updated_rows) * 100:.1f}%)")
    print()
    print(f"✅ Updated manifest saved to: {output_path}")


if __name__ == "__main__":
    main()
