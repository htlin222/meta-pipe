#!/usr/bin/env python3
"""Extract text from PDFs for data extraction."""

import argparse
import json
from pathlib import Path

import pdfplumber


def extract_text_from_pdf(pdf_path, max_pages=None):
    """Extract text from PDF file.

    Args:
        pdf_path: Path to PDF file
        max_pages: Maximum number of pages to extract (None = all)

    Returns:
        dict: Extracted text with metadata
    """
    result = {
        "pdf_path": str(pdf_path),
        "filename": pdf_path.name,
        "record_id": pdf_path.stem,
        "total_pages": 0,
        "extracted_pages": 0,
        "text": "",
        "pages": [],
        "error": None,
    }

    try:
        with pdfplumber.open(pdf_path) as pdf:
            result["total_pages"] = len(pdf.pages)

            # Limit pages if specified
            pages_to_extract = pdf.pages[:max_pages] if max_pages else pdf.pages

            all_text = []
            for i, page in enumerate(pages_to_extract, 1):
                page_text = page.extract_text()
                if page_text:
                    all_text.append(page_text)
                    result["pages"].append(
                        {
                            "page_number": i,
                            "text": page_text,
                            "char_count": len(page_text),
                        }
                    )

            result["extracted_pages"] = len(result["pages"])
            result["text"] = "\n\n".join(all_text)

    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Extract text from PDFs for data extraction"
    )
    parser.add_argument(
        "--pdf-dir", required=True, type=Path, help="Directory containing PDFs"
    )
    parser.add_argument(
        "--out-jsonl",
        required=True,
        type=Path,
        help="Output JSONL file with extracted text",
    )
    parser.add_argument(
        "--max-pages", type=int, help="Max pages to extract per PDF (default: all)"
    )
    parser.add_argument(
        "--pattern", default="*.pdf", help="File pattern (default: *.pdf)"
    )

    args = parser.parse_args()

    # Find all PDFs
    pdf_files = sorted(args.pdf_dir.glob(args.pattern))
    if not pdf_files:
        print(f"❌ No PDFs found in {args.pdf_dir} matching {args.pattern}")
        return

    print(f"📚 Found {len(pdf_files)} PDFs to process")
    print()

    # Extract text from each PDF
    results = []
    success_count = 0
    fail_count = 0

    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"[{i:2d}/{len(pdf_files)}] 📄 {pdf_path.name}")

        result = extract_text_from_pdf(pdf_path, max_pages=args.max_pages)

        if result["error"]:
            print(f"         ❌ Error: {result['error']}")
            fail_count += 1
        else:
            pages_info = f"{result['extracted_pages']}/{result['total_pages']} pages"
            char_count = len(result["text"])
            print(f"         ✅ Extracted {pages_info}, {char_count:,} characters")
            success_count += 1

        results.append(result)

    # Write output JSONL
    args.out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_jsonl, "w", encoding="utf-8") as f:
        for result in results:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")

    print()
    print("=" * 80)
    print("📊 Extraction Summary:")
    print(f"  ✅ Success: {success_count}")
    print(f"  ❌ Failed: {fail_count}")
    print(f"  📁 Output: {args.out_jsonl}")
    print()

    # Calculate total characters
    total_chars = sum(len(r["text"]) for r in results if not r["error"])
    print(f"  📝 Total characters extracted: {total_chars:,}")
    print(f"  📄 Average characters per PDF: {total_chars // success_count:,}")


if __name__ == "__main__":
    main()
