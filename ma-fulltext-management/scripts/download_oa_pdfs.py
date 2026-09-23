#!/usr/bin/env python3
"""Download Open Access PDFs from Unpaywall results CSV.

This script reads Unpaywall API results and attempts to download PDFs for
Open Access records. Handles common failure modes (403 errors, timeouts, etc.)
and provides detailed logging.

Usage:
    uv run download_oa_pdfs.py \\
      --in-csv unpaywall_results.csv \\
      --pdf-dir pdfs/ \\
      --out-log download.log \\
      --sleep 1 \\
      --max-retries 3
"""

import argparse
import csv
import sys
import time
from pathlib import Path

import requests


def download_pdf(url, output_path, timeout=30, max_retries=3, sleep_between_retries=2):
    """Download PDF from URL with retry logic.

    Args:
        url: PDF URL to download
        output_path: Path to save PDF
        timeout: Request timeout in seconds
        max_retries: Maximum number of retry attempts
        sleep_between_retries: Seconds to wait between retries

    Returns:
        tuple: (success: bool, message: str)
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for attempt in range(1, max_retries + 1):
        try:
            resp = requests.get(
                url, headers=headers, timeout=timeout, allow_redirects=True
            )
            resp.raise_for_status()

            # Check if response is actually a PDF
            content_type = resp.headers.get("Content-Type", "")
            if "pdf" not in content_type.lower() and not url.endswith(".pdf"):
                # Sometimes PDFs have wrong content-type, check magic bytes
                if not resp.content.startswith(b"%PDF"):
                    return False, "Not a PDF file (wrong content-type and magic bytes)"

            # Ensure parent directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write PDF
            with open(output_path, "wb") as f:
                f.write(resp.content)

            return True, f"Downloaded {len(resp.content):,} bytes"

        except requests.exceptions.Timeout:
            if attempt < max_retries:
                time.sleep(sleep_between_retries)
                continue
            return False, f"Timeout after {max_retries} attempts"

        except requests.exceptions.HTTPError as e:
            # Don't retry 4xx errors (client errors)
            if 400 <= e.response.status_code < 500:
                return False, f"{e.response.status_code} {e.response.reason}"
            # Retry 5xx errors (server errors)
            if attempt < max_retries:
                time.sleep(sleep_between_retries)
                continue
            return False, f"{e.response.status_code} after {max_retries} attempts"

        except requests.exceptions.RequestException as e:
            if attempt < max_retries:
                time.sleep(sleep_between_retries)
                continue
            return False, f"Request error: {str(e)[:100]}"

        except Exception as e:
            return False, f"Unexpected error: {str(e)[:100]}"

    return False, f"Failed after {max_retries} attempts"


def main():
    parser = argparse.ArgumentParser(
        description="Download Open Access PDFs from Unpaywall results",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--in-csv",
        required=True,
        type=Path,
        help="Input CSV from unpaywall_fetch.py (requires: record_id, is_oa, best_oa_pdf_url columns)",
    )
    parser.add_argument(
        "--pdf-dir", required=True, type=Path, help="Output directory for PDFs"
    )
    parser.add_argument(
        "--out-log", required=True, type=Path, help="Output log file path"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help=(
            "Concurrent downloads (default 1). Serially this runs at roughly 1 PDF/min: "
            "publisher URLs that block cost the full timeout x retries budget each, and "
            "the work is network-bound, so threads are the right fix."
        ),
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=1.0,
        help="Seconds to sleep between downloads (default: 1.0)",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Maximum retry attempts per PDF (default: 3)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30,
        help="HTTP request timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip PDFs that already exist (default: True)",
    )

    args = parser.parse_args()

    # Validate input CSV exists
    if not args.in_csv.exists():
        print(f"❌ Error: Input CSV not found: {args.in_csv}", file=sys.stderr)
        sys.exit(1)

    # Create PDF directory
    args.pdf_dir.mkdir(parents=True, exist_ok=True)

    # Counters
    success_count = 0
    fail_count = 0
    skipped_count = 0
    total_processed = 0

    # Open log file
    with open(args.out_log, "w", encoding="utf-8") as log_f:
        log_f.write("PDF Download Log\n")
        log_f.write("=" * 80 + "\n")
        log_f.write(f"Input CSV: {args.in_csv}\n")
        log_f.write(f"PDF directory: {args.pdf_dir}\n")
        log_f.write(f"Sleep between downloads: {args.sleep}s\n")
        log_f.write(f"Max retries: {args.max_retries}\n")
        log_f.write(f"Timeout: {args.timeout}s\n")
        log_f.write("=" * 80 + "\n\n")

        # Read and process CSV
        with open(args.in_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # Validate required columns
            required_cols = {"record_id", "is_oa", "best_oa_pdf_url"}
            if not required_cols.issubset(reader.fieldnames or []):
                print(
                    f"❌ Error: CSV missing required columns: {required_cols}",
                    file=sys.stderr,
                )
                print(f"   Found columns: {reader.fieldnames}", file=sys.stderr)
                sys.exit(1)

            jobs = []
            i = 0
            for i, row in enumerate(reader, 1):
                record_id = row.get("record_id", "").strip()
                pdf_url = row.get("best_oa_pdf_url", "").strip()
                is_oa = row.get("is_oa", "").strip()

                if is_oa != "True" or not pdf_url:
                    skipped_count += 1
                    continue

                total_processed += 1
                output_path = args.pdf_dir / f"{record_id}.pdf"

                if args.skip_existing and output_path.exists():
                    log_f.write(f"SKIP: {record_id} - already exists\n")
                    skipped_count += 1
                    continue

                jobs.append((record_id, pdf_url, output_path))

            def _one(job):
                rid, url, out = job
                ok, msg = download_pdf(
                    url, out, timeout=args.timeout, max_retries=args.max_retries
                )
                return rid, url, out, ok, msg

            workers = max(1, int(getattr(args, "workers", 1) or 1))
            print(f"Downloading {len(jobs)} PDFs with {workers} worker(s)")
            done = 0
            if workers == 1:
                results = (_one(j) for j in jobs)
            else:
                from concurrent.futures import ThreadPoolExecutor

                pool = ThreadPoolExecutor(max_workers=workers)
                results = pool.map(_one, jobs)

            for rid, pdf_url, output_path, success, msg in results:
                done += 1
                if success:
                    log_f.write(f"SUCCESS: {rid} - {msg}\n")
                    log_f.write(f"  URL: {pdf_url}\n")
                    log_f.write(f"  Path: {output_path}\n\n")
                    success_count += 1
                else:
                    log_f.write(f"FAIL: {rid} - {msg}\n")
                    log_f.write(f"  URL: {pdf_url}\n\n")
                    fail_count += 1
                if done % 25 == 0 or done == len(jobs):
                    print(
                        f"  {done}/{len(jobs)} attempted ({success_count} ok, {fail_count} failed)"
                    )
                    log_f.flush()

        # Write summary to log
        log_f.write("\n" + "=" * 80 + "\n")
        log_f.write("SUMMARY\n")
        log_f.write("=" * 80 + "\n")
        log_f.write(f"Total records in CSV: {i}\n")
        log_f.write(f"OA records with PDF URL: {total_processed}\n")
        log_f.write(f"Successfully downloaded: {success_count}\n")
        log_f.write(f"Failed downloads: {fail_count}\n")
        log_f.write(f"Skipped (existing/non-OA): {skipped_count}\n")
        if total_processed > 0:
            log_f.write(f"Success rate: {success_count / total_processed * 100:.1f}%\n")

    # Print summary to console
    print()
    print("=" * 80)
    print("📊 Download Summary:")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Failed: {fail_count}")
    print(f"  ⏭️  Skipped: {skipped_count}")
    print(f"  📁 Total PDFs in directory: {len(list(args.pdf_dir.glob('*.pdf')))}")
    print(f"  📄 Log: {args.out_log}")

    if total_processed > 0:
        print(
            f"  📈 Success rate: {success_count / total_processed * 100:.1f}% "
            f"({success_count}/{total_processed})"
        )

    # Exit with error code if any downloads failed
    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
