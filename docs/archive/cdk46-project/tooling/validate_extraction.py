#!/usr/bin/env python3
"""Validate extracted data quality and generate summary report."""

import argparse
import csv
import json
from pathlib import Path


def load_extraction_csv(csv_path):
    """Load extraction CSV."""
    records = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)
    return records


def validate_records(records):
    """Run validation checks on extracted records."""
    issues = []
    stats = {
        "total_records": len(records),
        "fields_per_record": {},
        "missing_critical": [],
        "data_type_issues": [],
        "value_range_issues": [],
    }
    
    critical_fields = [
        "study_id", "first_author", "publication_year",
        "n_total", "n_cdk46_prior",
    ]
    
    numeric_fields = [
        "publication_year", "n_total", "n_cdk46_prior", "pct_cdk46_prior",
        "pfs_hr", "pfs_ci_lower", "pfs_ci_upper",
        "os_hr", "os_ci_lower", "os_ci_upper",
    ]
    
    for i, rec in enumerate(records, 1):
        record_id = rec.get("study_id", f"record_{i}")
        
        # Count filled fields
        filled = sum(1 for v in rec.values() if v and v.strip())
        stats["fields_per_record"][record_id] = filled
        
        # Check critical fields
        for field in critical_fields:
            if not rec.get(field) or not rec[field].strip():
                stats["missing_critical"].append(f"{record_id}: missing {field}")
        
        # Check numeric fields
        for field in numeric_fields:
            value = rec.get(field, "").strip()
            if value and value not in ["", "NR", "NA"]:
                try:
                    float(value)
                except ValueError:
                    stats["data_type_issues"].append(
                        f"{record_id}: {field} = '{value}' (not numeric)"
                    )
        
        # Check percentage ranges
        pct_fields = [f for f in rec.keys() if "pct" in f.lower() or "percent" in f.lower()]
        for field in pct_fields:
            value = rec.get(field, "").strip()
            if value and value not in ["", "NR", "NA"]:
                try:
                    pct = float(value)
                    if pct < 0 or pct > 100:
                        stats["value_range_issues"].append(
                            f"{record_id}: {field} = {pct} (out of 0-100 range)"
                        )
                except ValueError:
                    pass
        
        # Check CI consistency
        hr = rec.get("pfs_hr", "").strip()
        ci_lower = rec.get("pfs_ci_lower", "").strip()
        ci_upper = rec.get("pfs_ci_upper", "").strip()
        
        if all([hr, ci_lower, ci_upper]):
            try:
                hr_val = float(hr)
                lower_val = float(ci_lower)
                upper_val = float(ci_upper)
                
                if not (lower_val <= hr_val <= upper_val):
                    stats["value_range_issues"].append(
                        f"{record_id}: PFS CI inconsistent ({lower_val} < {hr_val} < {upper_val})"
                    )
            except ValueError:
                pass
    
    return stats


def generate_report(stats, out_md):
    """Generate markdown validation report."""
    lines = [
        "# Data Extraction Validation Report",
        "",
        f"**Date**: {Path(__file__).stat().st_mtime}",
        f"**Total Records**: {stats['total_records']}",
        "",
        "---",
        "",
        "## Summary Statistics",
        "",
        "### Fields Filled Per Record",
        "",
        "| Study ID | Filled Fields |",
        "|----------|---------------|",
    ]
    
    for study_id, count in stats["fields_per_record"].items():
        lines.append(f"| {study_id} | {count} |")
    
    lines.extend([
        "",
        "---",
        "",
        "## Validation Issues",
        "",
    ])
    
    # Missing critical fields
    if stats["missing_critical"]:
        lines.extend([
            f"### ⚠️ Missing Critical Fields ({len(stats['missing_critical'])})",
            "",
        ])
        for issue in stats["missing_critical"]:
            lines.append(f"- {issue}")
        lines.append("")
    else:
        lines.extend([
            "### ✅ All Critical Fields Present",
            "",
        ])
    
    # Data type issues
    if stats["data_type_issues"]:
        lines.extend([
            f"### ⚠️ Data Type Issues ({len(stats['data_type_issues'])})",
            "",
        ])
        for issue in stats["data_type_issues"]:
            lines.append(f"- {issue}")
        lines.append("")
    else:
        lines.extend([
            "### ✅ No Data Type Issues",
            "",
        ])
    
    # Value range issues
    if stats["value_range_issues"]:
        lines.extend([
            f"### ⚠️ Value Range Issues ({len(stats['value_range_issues'])})",
            "",
        ])
        for issue in stats["value_range_issues"]:
            lines.append(f"- {issue}")
        lines.append("")
    else:
        lines.extend([
            "### ✅ No Value Range Issues",
            "",
        ])
    
    # Overall assessment
    total_issues = (
        len(stats["missing_critical"]) +
        len(stats["data_type_issues"]) +
        len(stats["value_range_issues"])
    )
    
    lines.extend([
        "---",
        "",
        "## Overall Assessment",
        "",
    ])
    
    if total_issues == 0:
        lines.append("✅ **PASS**: All validation checks passed!")
    else:
        lines.append(f"⚠️ **REVIEW NEEDED**: {total_issues} issues found")
    
    lines.extend([
        "",
        "---",
        "",
        "## Next Steps",
        "",
        "1. Review and fix validation issues",
        "2. Verify extracted data against original PDFs",
        "3. Proceed to Stage 06 (Meta-Analysis)",
        "",
    ])
    
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Validate extraction data")
    parser.add_argument("--csv", required=True, help="Extraction CSV to validate")
    parser.add_argument("--out-md", required=True, help="Output validation report")
    args = parser.parse_args()

    csv_path = Path(args.csv)
    out_md = Path(args.out_md)

    if not csv_path.exists():
        raise SystemExit(f"❌ CSV not found: {csv_path}")

    print(f"📋 Loading extraction data from {csv_path}...")
    records = load_extraction_csv(csv_path)
    
    print(f"✅ Loaded {len(records)} records")
    print(f"🔍 Running validation checks...")
    
    stats = validate_records(records)
    
    total_issues = (
        len(stats["missing_critical"]) +
        len(stats["data_type_issues"]) +
        len(stats["value_range_issues"])
    )
    
    print(f"\n{'='*60}")
    print(f"📊 Validation Summary:")
    print(f"   ⚠️  Missing critical: {len(stats['missing_critical'])}")
    print(f"   ⚠️  Data type issues: {len(stats['data_type_issues'])}")
    print(f"   ⚠️  Value range issues: {len(stats['value_range_issues'])}")
    print(f"   📊 Total issues: {total_issues}")
    print(f"{'='*60}\n")
    
    generate_report(stats, out_md)
    
    print(f"✅ Validation report: {out_md}")
    
    if total_issues == 0:
        print("✅ All validation checks passed!")
    else:
        print(f"⚠️  Please review {total_issues} issues in the report")


if __name__ == "__main__":
    main()
