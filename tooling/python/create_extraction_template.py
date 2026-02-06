#!/usr/bin/env python3
"""Create extraction template CSV from data dictionary and PDF list."""

import argparse
import csv
import json
from pathlib import Path


def create_extraction_template(pdf_jsonl, data_dict, output_csv):
    """Create extraction template CSV."""

    # Read extracted PDF texts
    records = []
    with open(pdf_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            if not record.get("error"):
                records.append(record)

    print(f"✅ Loaded {len(records)} successfully extracted PDFs")

    # Define core fields from data dictionary
    # These are the REQUIRED fields for inclusion
    core_fields = [
        # Study Identification
        "study_id",
        "first_author",
        "publication_year",
        "title",
        "journal",
        "doi",
        "pmid",
        "trial_name",
        # Study Design
        "study_design",
        "phase",
        "randomization",
        # Population
        "n_total",
        "n_cdk46_prior",
        "pct_cdk46_prior",
        "age_median",
        "hr_positive_pct",
        "her2_negative_pct",
        "metastatic_pct",
        # CDK4/6i Details
        "cdk46_type",
        "cdk46_line",
        "cdk46_setting",
        # Intervention
        "arm_1_name",
        "arm_1_category",
        "arm_1_dose",
        "arm_1_n",
        "arm_2_name",
        "arm_2_category",
        "arm_2_dose",
        "arm_2_n",
        # Primary Outcomes
        "primary_endpoint",
        "pfs_median_arm1",
        "pfs_median_arm2",
        "pfs_hr",
        "pfs_ci_lower",
        "pfs_ci_upper",
        "pfs_p_value",
        # Secondary Outcomes
        "os_median_arm1",
        "os_median_arm2",
        "os_hr",
        "os_ci_lower",
        "os_ci_upper",
        "os_p_value",
        "orr_arm1",
        "orr_arm2",
        # Safety
        "ae_grade3plus_arm1_pct",
        "ae_grade3plus_arm2_pct",
        # Quality
        "rob_overall",
        # Notes
        "notes_general",
    ]

    # Create template rows
    template_rows = []
    for record in records:
        row = {field: "" for field in core_fields}
        row["study_id"] = record["record_id"]
        row["pdf_filename"] = record["filename"]
        row["pdf_pages"] = record["extracted_pages"]
        row["pdf_chars"] = len(record["text"])
        template_rows.append(row)

    # Write to CSV
    fieldnames = ["study_id", "pdf_filename", "pdf_pages", "pdf_chars"] + core_fields[
        1:
    ]

    with open(output_csv, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(template_rows)

    print(f"✅ Created extraction template: {output_csv}")
    print(f"   - {len(template_rows)} records")
    print(f"   - {len(fieldnames)} fields")
    print()
    print("📋 Next steps:")
    print("  1. Open the CSV in Excel/LibreOffice")
    print("  2. Read each PDF and fill in the data")
    print("  3. Refer to data-dictionary.md for field definitions")
    print("  4. Use the extracted text in pdf_texts.jsonl for reference")


def main():
    parser = argparse.ArgumentParser(description="Create extraction template CSV")
    parser.add_argument(
        "--pdf-jsonl",
        required=True,
        type=Path,
        help="Input JSONL file with extracted PDF texts",
    )
    parser.add_argument(
        "--data-dict",
        required=True,
        type=Path,
        help="Data dictionary markdown file",
    )
    parser.add_argument(
        "--out-csv",
        required=True,
        type=Path,
        help="Output extraction template CSV",
    )

    args = parser.parse_args()

    create_extraction_template(args.pdf_jsonl, args.data_dict, args.out_csv)


if __name__ == "__main__":
    main()
