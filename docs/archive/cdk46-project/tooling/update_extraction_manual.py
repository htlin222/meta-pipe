#!/usr/bin/env python3
"""Manually update extraction CSV with reviewed data."""

import argparse
import csv
from pathlib import Path


def update_extraction(csv_path, updates, exclude_ids):
    """Update extraction CSV with manual fixes."""
    records = []
    
    # Read existing data
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            study_id = row["study_id"]
            
            # Apply updates
            if study_id in updates:
                for field, value in updates[study_id].items():
                    row[field] = str(value) if value is not None else ""
            
            # Mark excluded studies
            if study_id in exclude_ids:
                if not row.get("notes_general"):
                    row["notes_general"] = ""
                row["notes_general"] += " [EXCLUDE: Review article/Protocol - not original research]"
            
            records.append(row)
    
    # Write updated data
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    
    return len(records)


def main():
    parser = argparse.ArgumentParser(description="Update extraction CSV with manual fixes")
    parser.add_argument("--csv", required=True, help="Extraction CSV to update")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise SystemExit(f"❌ CSV not found: {csv_path}")

    # Manual updates based on PDF review
    updates = {
        "TokunagaE202539379782": {
            "n_cdk46_prior": 13,  # 78 * 0.167 = 13
            "pct_cdk46_prior": 16.7,
        }
    }
    
    # Studies to exclude (review articles/protocols)
    exclude_ids = [
        "CogliatiV2022222",      # Review article
        "DegenhardtT2023338",    # Study protocol
        "HoraniM202337860199",   # Review article
        "PrestiD2019335",        # Review article
    ]
    
    print("📝 Updating extraction data...")
    n_records = update_extraction(csv_path, updates, exclude_ids)
    
    print(f"\n✅ Updated {csv_path}")
    print(f"   - Total records: {n_records}")
    print(f"   - Updated: {len(updates)} studies")
    print(f"   - Excluded: {len(exclude_ids)} studies")
    print(f"\n📊 Summary:")
    print(f"   ✅ TokunagaE202539379782: Added n_cdk46_prior=13, pct_cdk46_prior=16.7")
    print(f"   ❌ CogliatiV2022222: Marked for exclusion (Review)")
    print(f"   ❌ DegenhardtT2023338: Marked for exclusion (Protocol)")
    print(f"   ❌ HoraniM202337860199: Marked for exclusion (Review)")
    print(f"   ❌ PrestiD2019335: Marked for exclusion (Review)")


if __name__ == "__main__":
    main()
