#!/usr/bin/env python3
"""Check outcome data completeness for meta-analysis feasibility."""

import argparse
import csv
from pathlib import Path


def check_outcomes(csv_path, exclude_ids):
    """Check which studies have complete outcome data."""
    
    # Key outcome fields for meta-analysis
    outcome_fields = {
        "PFS": ["pfs_hr", "pfs_ci_lower", "pfs_ci_upper"],
        "OS": ["os_hr", "os_ci_lower", "os_ci_upper"],
        "ORR": ["orr_arm1", "orr_arm2"],
    }
    
    records = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["study_id"] not in exclude_ids:
                records.append(row)
    
    print(f"📊 Outcome Data Completeness Check")
    print(f"{'='*70}")
    print(f"\n✅ Includable Studies: {len(records)}\n")
    
    # Check each outcome type
    for outcome_type, fields in outcome_fields.items():
        print(f"\n{outcome_type} Data:")
        print(f"{'-'*70}")
        
        complete_studies = []
        incomplete_studies = []
        
        for rec in records:
            study_id = rec["study_id"]
            has_all = all(rec.get(f, "").strip() for f in fields)
            
            if has_all:
                complete_studies.append(study_id)
                values = [rec.get(f, "") for f in fields]
                print(f"  ✅ {study_id}: {', '.join(values)}")
            else:
                incomplete_studies.append(study_id)
                missing = [f for f in fields if not rec.get(f, "").strip()]
                print(f"  ❌ {study_id}: Missing {', '.join(missing)}")
        
        print(f"\n  Summary: {len(complete_studies)}/{len(records)} studies have complete {outcome_type} data")
    
    print(f"\n{'='*70}")
    print(f"\n📋 Meta-Analysis Feasibility:")
    
    # Count studies with each outcome
    pfs_count = sum(1 for r in records if all(r.get(f, "").strip() for f in outcome_fields["PFS"]))
    os_count = sum(1 for r in records if all(r.get(f, "").strip() for f in outcome_fields["OS"]))
    orr_count = sum(1 for r in records if all(r.get(f, "").strip() for f in outcome_fields["ORR"]))
    
    print(f"  • PFS (Hazard Ratio): {pfs_count} studies")
    print(f"  • OS (Hazard Ratio): {os_count} studies")
    print(f"  • ORR (Response Rate): {orr_count} studies")
    
    print(f"\n💡 Recommendation:")
    if pfs_count >= 3:
        print(f"  ✅ Proceed with PFS meta-analysis ({pfs_count} studies)")
    else:
        print(f"  ⚠️  Insufficient data for PFS meta-analysis (need ≥3, have {pfs_count})")
    
    if os_count >= 3:
        print(f"  ✅ Proceed with OS meta-analysis ({os_count} studies)")
    else:
        print(f"  ⚠️  Insufficient data for OS meta-analysis (need ≥3, have {os_count})")
    
    if orr_count >= 3:
        print(f"  ✅ Consider ORR meta-analysis ({orr_count} studies)")
    else:
        print(f"  ℹ️  Limited data for ORR meta-analysis ({orr_count} studies)")


def main():
    parser = argparse.ArgumentParser(description="Check outcome data completeness")
    parser.add_argument("--csv", required=True, help="Extraction CSV")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    if not csv_path.exists():
        raise SystemExit(f"❌ CSV not found: {csv_path}")

    # Studies to exclude (from manual review)
    exclude_ids = [
        "CogliatiV2022222",
        "DegenhardtT2023338",
        "HoraniM202337860199",
        "PrestiD2019335",
    ]

    check_outcomes(csv_path, exclude_ids)


if __name__ == "__main__":
    main()
