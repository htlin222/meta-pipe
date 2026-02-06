#!/usr/bin/env python3
"""Create manifest CSV from PDFs for LLM extraction."""

import argparse
import csv
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf-jsonl", required=True, help="PDF texts JSONL from extract_pdf_text.py")
    parser.add_argument("--out-csv", required=True, help="Output manifest CSV")
    args = parser.parse_args()

    pdf_jsonl = Path(args.pdf_jsonl)
    out_csv = Path(args.out_csv)
    
    if not pdf_jsonl.exists():
        raise SystemExit(f"❌ PDF JSONL not found: {pdf_jsonl}")
    
    records = []
    with pdf_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                if data.get("error") is None:  # Only successful extractions
                    records.append({
                        "record_id": data["record_id"],
                        "file_path": data["pdf_path"],
                        "title": "",  # Will be extracted by LLM
                        "doi": "",
                        "pmid": "",
                    })
    
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["record_id", "file_path", "title", "doi", "pmid"])
        writer.writeheader()
        writer.writerows(records)
    
    print(f"✅ Created manifest: {out_csv}")
    print(f"   - {len(records)} PDF records")


if __name__ == "__main__":
    main()
