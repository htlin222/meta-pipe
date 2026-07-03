#!/usr/bin/env python3
"""Audit full-text screening reasons for 'defaulting' and other low-confidence indicators."""

import argparse
import csv
from pathlib import Path

def audit_decisions(path: Path) -> list[str]:
    issues = []
    if not path.exists():
        return [f"Missing decision file: {path}"]
    
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rid = row.get("record_id", "unknown")
            r1_reason = row.get("FT_Reviewer1_Reason", "")
            r2_reason = row.get("FT_Reviewer2_Reason", "")
            
            if "defaulting" in r1_reason.lower() or "unable to determine" in r1_reason.lower():
                issues.append(f"Low confidence (R1) for {rid}: {r1_reason}")
            if "defaulting" in r2_reason.lower() or "unable to determine" in r2_reason.lower():
                issues.append(f"Low confidence (R2) for {rid}: {r2_reason}")
                
    return issues

def main():
    parser = argparse.ArgumentParser(description="Audit screening for quality.")
    parser.add_argument("--project", required=True)
    args = parser.parse_args()
    
    project_path = Path("projects") / args.project
    ft_decisions = project_path / "04_fulltext" / "fulltext_decisions.csv"
    
    issues = audit_decisions(ft_decisions)
    if issues:
        print("⚠️  Quality issues found in full-text screening:")
        for issue in issues:
            print(f"  - {issue}")
        print("\nRecommendation: Manually verify these studies as the AI could not retrieve or read the full text.")
    else:
        print("✅ No 'defaulting' or low-confidence reasons found in full-text screening.")

if __name__ == "__main__":
    main()
