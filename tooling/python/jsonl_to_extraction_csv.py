#!/usr/bin/env python3
"""Convert LLM extracted JSONL to extraction CSV format."""

import argparse
import csv
import json
from pathlib import Path


def load_field_names_from_dict(data_dict_path):
    """Extract field names from data dictionary."""
    import re
    text = data_dict_path.read_text(encoding="utf-8")
    fields = re.findall(r'`([a-z_][a-z0-9_]*)`', text)
    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for f in fields:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return unique


def main():
    parser = argparse.ArgumentParser(description="Convert JSONL to extraction CSV")
    parser.add_argument("--jsonl", required=True, help="Input JSONL from llm_extract_cli.py")
    parser.add_argument("--data-dict", required=True, help="Data dictionary for field order")
    parser.add_argument("--out-csv", required=True, help="Output CSV file")
    args = parser.parse_args()

    jsonl_path = Path(args.jsonl)
    data_dict_path = Path(args.data_dict)
    out_csv = Path(args.out_csv)

    if not jsonl_path.exists():
        raise SystemExit(f"❌ JSONL not found: {jsonl_path}")
    
    if not data_dict_path.exists():
        raise SystemExit(f"❌ Data dictionary not found: {data_dict_path}")

    # Load field names from data dictionary
    all_fields = load_field_names_from_dict(data_dict_path)
    print(f"📋 Loaded {len(all_fields)} fields from data dictionary")

    # Load JSONL records
    records = []
    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rec = json.loads(line)
                if rec["status"] == "success" and rec["extracted_data"]:
                    records.append(rec)
    
    print(f"📄 Loaded {len(records)} successfully extracted records")

    # Prepare CSV rows
    csv_rows = []
    for rec in records:
        row = {}
        extracted = rec["extracted_data"]
        
        # Fill in all fields
        for field in all_fields:
            value = extracted.get(field)
            
            # Convert to string for CSV
            if value is None:
                row[field] = ""
            elif isinstance(value, (list, dict)):
                row[field] = json.dumps(value, ensure_ascii=False)
            elif isinstance(value, bool):
                row[field] = "TRUE" if value else "FALSE"
            else:
                row[field] = str(value)
        
        csv_rows.append(row)

    # Write CSV
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_fields)
        writer.writeheader()
        writer.writerows(csv_rows)
    
    print(f"✅ Created CSV: {out_csv}")
    print(f"   - {len(csv_rows)} records")
    print(f"   - {len(all_fields)} fields")


if __name__ == "__main__":
    main()
