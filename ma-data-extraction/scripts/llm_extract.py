#!/usr/bin/env python3
"""LLM-assisted data extraction from PDFs into structured JSON suggestions."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import requests


def load_dotenv() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    sys.path.append(str(repo_root / "ma-search-bibliography" / "scripts"))
    try:
        from env_utils import load_dotenv as _load
    except Exception:
        return
    _load(repo_root)


def read_manifest(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Missing manifest: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for row in reader:
            rows.append({k: (v or "").strip() for k, v in row.items()})
        for row in rows:
            row["_manifest_dir"] = str(path.parent)
        return rows


def parse_fields_from_dictionary(path: Path) -> List[str]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    fields = re.findall(r"`([^`]+)`", text)
    seen = set()
    ordered = []
    for field in fields:
        if field not in seen:
            seen.add(field)
            ordered.append(field)
    return ordered


def extract_text_with_pdfplumber(pdf_path: Path, max_pages: int) -> Optional[str]:
    try:
        import pdfplumber  # type: ignore
    except Exception:
        return None
    texts = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for idx, page in enumerate(pdf.pages):
            if idx >= max_pages:
                break
            text = page.extract_text() or ""
            texts.append(text)
    return "\n".join(texts).strip()


def extract_text_with_pypdf(pdf_path: Path, max_pages: int) -> Optional[str]:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception:
        return None
    reader = PdfReader(str(pdf_path))
    texts = []
    for idx, page in enumerate(reader.pages):
        if idx >= max_pages:
            break
        text = page.extract_text() or ""
        texts.append(text)
    return "\n".join(texts).strip()


def extract_pdf_text(pdf_path: Path, max_pages: int) -> str:
    text = extract_text_with_pdfplumber(pdf_path, max_pages)
    if text:
        return text
    text = extract_text_with_pypdf(pdf_path, max_pages)
    if text:
        return text
    raise SystemExit(
        "No PDF parser available. Install one of: pdfplumber or pypdf (via uv add)."
    )


def build_prompt(
    record: Dict[str, str],
    fields: List[str],
    pdf_text: str,
    max_chars: int,
) -> str:
    clipped = pdf_text[:max_chars]
    field_list = ", ".join(fields) if fields else "<define your schema>"
    header = [
        "You are assisting with meta-analysis data extraction.",
        "Extract the requested fields from the study text.",
        "Return JSON only. Use null for missing values.",
        "Include page numbers or sections in `page_reference` when possible.",
        "",
        f"Record ID: {record.get('record_id') or ''}",
        f"Title: {record.get('title') or ''}",
        f"DOI: {record.get('doi') or ''}",
        f"PMID: {record.get('pmid') or ''}",
        "",
        f"Fields: {field_list}",
        "",
        "Study text:",
        clipped,
    ]
    return "\n".join(header).strip()


def call_llm(
    api_base: str,
    api_key: str,
    model: str,
    prompt: str,
    temperature: float,
    max_tokens: int,
    extra_headers: Dict[str, str],
) -> str:
    url = api_base.rstrip("/") + "/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    headers.update(extra_headers)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a careful extraction assistant."},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()
    return str(data.get("choices", [{}])[0].get("message", {}).get("content", "")).strip()


def parse_json_response(text: str) -> Tuple[Optional[dict], Optional[str]]:
    try:
        return json.loads(text), None
    except Exception as exc:
        return None, f"{exc.__class__.__name__}: {exc}"


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(description="LLM-assisted extraction from PDFs.")
    parser.add_argument("--manifest", default="04_fulltext/manifest.csv", help="Manifest CSV")
    parser.add_argument(
        "--data-dictionary",
        default="05_extraction/data-dictionary.md",
        help="Data dictionary markdown",
    )
    parser.add_argument("--out-jsonl", default="05_extraction/llm_suggestions.jsonl")
    parser.add_argument("--out-log", default="05_extraction/llm_extract.log")
    parser.add_argument("--prompts-dir", default=None, help="Optional directory to save prompts")
    parser.add_argument("--limit", type=int, default=None, help="Max records to process")
    parser.add_argument("--max-pages", type=int, default=5, help="Max PDF pages to parse")
    parser.add_argument("--max-chars", type=int, default=12000, help="Max text characters per prompt")
    parser.add_argument("--min-chars", type=int, default=400, help="Skip PDFs with less text")
    parser.add_argument("--dry-run", action="store_true", help="Generate prompts without calling LLM")
    parser.add_argument("--api-base", default=None, help="LLM API base URL")
    parser.add_argument("--api-key", default=None, help="LLM API key")
    parser.add_argument("--model", default=None, help="LLM model name")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max-tokens", type=int, default=800)
    args = parser.parse_args()

    api_base = args.api_base or os.getenv("LLM_API_BASE", "")
    api_key = args.api_key or os.getenv("LLM_API_KEY", "")
    model = args.model or os.getenv("LLM_MODEL", "")
    extra_headers: Dict[str, str] = {}
    extra_headers_json = os.getenv("LLM_HEADERS_JSON")
    if extra_headers_json:
        try:
            extra_headers.update(json.loads(extra_headers_json))
        except Exception:
            pass

    if not args.dry_run and (not api_base or not api_key or not model):
        raise SystemExit("Missing LLM_API_BASE / LLM_API_KEY / LLM_MODEL (or pass via args)")

    manifest_rows = read_manifest(Path(args.manifest))
    fields = parse_fields_from_dictionary(Path(args.data_dictionary))
    if args.limit is not None:
        manifest_rows = manifest_rows[: args.limit]

    out_jsonl = Path(args.out_jsonl)
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    prompts_dir = Path(args.prompts_dir) if args.prompts_dir else None
    if prompts_dir:
        prompts_dir.mkdir(parents=True, exist_ok=True)

    processed = 0
    skipped = 0
    errors = 0

    with out_jsonl.open("w", encoding="utf-8") as handle:
        for row in manifest_rows:
            file_path = row.get("file_path", "")
            if not file_path:
                skipped += 1
                continue
            manifest_dir = Path(row.get("_manifest_dir", "."))
            pdf_path = Path(file_path)
            if not pdf_path.is_absolute():
                pdf_path = (manifest_dir / pdf_path).resolve()
            if not pdf_path.exists():
                skipped += 1
                continue

            try:
                text = extract_pdf_text(pdf_path, args.max_pages)
            except SystemExit as exc:
                errors += 1
                record = {
                    "record_id": row.get("record_id", ""),
                    "file_path": file_path,
                    "error": str(exc),
                }
                handle.write(json.dumps(record) + "\n")
                continue

            if len(text) < args.min_chars:
                skipped += 1
                continue

            prompt = build_prompt(row, fields, text, args.max_chars)
            prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
            if prompts_dir:
                prompt_path = prompts_dir / f"{row.get('record_id') or pdf_path.stem}.prompt.txt"
                prompt_path.write_text(prompt, encoding="utf-8")

            response_text = ""
            parsed = None
            parse_error = None
            status = "ok"

            if args.dry_run:
                status = "dry_run"
            else:
                try:
                    response_text = call_llm(
                        api_base=api_base,
                        api_key=api_key,
                        model=model,
                        prompt=prompt,
                        temperature=args.temperature,
                        max_tokens=args.max_tokens,
                        extra_headers=extra_headers,
                    )
                    parsed, parse_error = parse_json_response(response_text)
                except Exception as exc:
                    status = "error"
                    errors += 1
                    response_text = f"{exc.__class__.__name__}: {exc}"

            record = {
                "timestamp": dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "") + "Z",
                "record_id": row.get("record_id", ""),
                "file_path": file_path,
                "model": model,
                "prompt_hash": prompt_hash,
                "status": status,
                "parse_error": parse_error,
                "response_text": response_text,
                "parsed": parsed,
            }
            handle.write(json.dumps(record) + "\n")
            processed += 1

    out_log = Path(args.out_log)
    out_log.parent.mkdir(parents=True, exist_ok=True)
    log_lines = [
        f"date: {dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "")}Z",
        f"manifest: {args.manifest}",
        f"records: {len(manifest_rows)}",
        f"processed: {processed}",
        f"skipped: {skipped}",
        f"errors: {errors}",
        f"dry_run: {args.dry_run}",
        f"model: {model}",
    ]
    out_log.write_text("\n".join(log_lines) + "\n")


if __name__ == "__main__":
    main()
