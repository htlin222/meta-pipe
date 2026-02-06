#!/usr/bin/env python3
"""Download Open Access PDFs from Unpaywall results."""

import csv
import sys
import time
from pathlib import Path
import requests


def download_pdf(url, output_path, timeout=30):
    """Download PDF from URL."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        resp.raise_for_status()

        # Check if response is PDF
        content_type = resp.headers.get("Content-Type", "")
        if "pdf" not in content_type.lower() and not url.endswith(".pdf"):
            # Sometimes PDFs have wrong content-type, check magic bytes
            if not resp.content.startswith(b"%PDF"):
                return False, "Not a PDF file"

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(resp.content)

        return True, f"Downloaded {len(resp.content)} bytes"

    except requests.exceptions.Timeout:
        return False, "Timeout"
    except requests.exceptions.RequestException as e:
        return False, f"Request error: {str(e)[:50]}"
    except Exception as e:
        return False, f"Error: {str(e)[:50]}"


def main():
    csv_path = Path("../../04_fulltext/round-01/unpaywall_results.csv")
    pdf_dir = Path("../../04_fulltext/round-01/pdfs")
    log_path = Path("../../04_fulltext/round-01/pdf_download.log")

    pdf_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    fail_count = 0
    skipped_count = 0

    with open(log_path, "w", encoding="utf-8") as log_f:
        log_f.write("PDF Download Log\n")
        log_f.write("=" * 80 + "\n\n")

        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader, 1):
                record_id = row.get("record_id", "").strip()
                pdf_url = row.get("best_oa_pdf_url", "").strip()
                is_oa = row.get("is_oa", "").strip()

                if is_oa != "True" or not pdf_url:
                    skipped_count += 1
                    continue

                output_path = pdf_dir / f"{record_id}.pdf"

                # Skip if already exists
                if output_path.exists():
                    print(f"[{i:2d}] ⏭️  SKIP: {record_id} (already exists)")
                    log_f.write(f"SKIP: {record_id} - already exists\n")
                    skipped_count += 1
                    continue

                print(f"[{i:2d}] 📥 Downloading: {record_id}")
                success, msg = download_pdf(pdf_url, output_path)

                if success:
                    print(f"     ✅ {msg}")
                    log_f.write(f"SUCCESS: {record_id} - {msg}\n")
                    log_f.write(f"  URL: {pdf_url}\n")
                    log_f.write(f"  Path: {output_path}\n\n")
                    success_count += 1
                else:
                    print(f"     ❌ {msg}")
                    log_f.write(f"FAIL: {record_id} - {msg}\n")
                    log_f.write(f"  URL: {pdf_url}\n\n")
                    fail_count += 1

                # Rate limiting
                time.sleep(1)

    print()
    print("=" * 80)
    print(f"📊 Download Summary:")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Failed: {fail_count}")
    print(f"  ⏭️  Skipped: {skipped_count}")
    print(f"  📁 Total PDFs in directory: {len(list(pdf_dir.glob('*.pdf')))}")
    print(f"  📄 Log: {log_path}")


if __name__ == "__main__":
    main()
