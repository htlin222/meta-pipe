#!/usr/bin/env python3
"""LLM-assisted data extraction using claude CLI or codex exec."""

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def check_cli_available():
    """Check which CLI tools are available."""
    claude = shutil.which("claude")
    codex = shutil.which("codex")
    return claude, codex


def build_extraction_prompt(record_id, pdf_text, fields, data_dict_snippet):
    """Build the extraction prompt for the LLM."""
    prompt = f"""You are a systematic review data extraction assistant.

Extract structured data from this clinical trial PDF text.

**Study ID**: {record_id}

**Fields to extract** (return as JSON):
{', '.join(fields[:20])}  {"... (and more)" if len(fields) > 20 else ""}

**Data Dictionary Reference**:
{data_dict_snippet[:1000]}...

**Instructions**:
1. Extract ONLY the requested fields from the PDF text
2. Return valid JSON with exact field names
3. Use `null` for missing/not reported values
4. For numeric fields: extract numbers only (e.g., "12.5" not "12.5 months")
5. For categorical fields: use exact categories from data dictionary
6. Include confidence intervals as separate lower/upper fields

**PDF Text**:
{pdf_text[:8000]}

Return JSON only (no markdown, no explanation):
"""
    return prompt


def call_claude_cli(prompt, timeout=120):
    """Call claude CLI in print mode."""
    try:
        result = subprocess.run(
            ["claude", "-p"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            return None, f"claude CLI error: {result.stderr}"
        return result.stdout.strip(), None
    except subprocess.TimeoutExpired:
        return None, "Timeout"
    except Exception as e:
        return None, str(e)


def call_codex_exec(prompt, timeout=120):
    """Call codex exec mode."""
    try:
        result = subprocess.run(
            ["codex", "exec", prompt],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0:
            return None, f"codex exec error: {result.stderr}"
        return result.stdout.strip(), None
    except subprocess.TimeoutExpired:
        return None, "Timeout"
    except Exception as e:
        return None, str(e)


def extract_json_from_response(text):
    """Extract JSON from LLM response (may have markdown wrapper)."""
    # Try to parse as-is
    try:
        return json.loads(text), None
    except:
        pass
    
    # Try to extract from markdown code block
    import re
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1)), None
        except Exception as e:
            return None, f"JSON parse error: {e}"
    
    # Try to find any JSON object
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0)), None
        except Exception as e:
            return None, f"JSON parse error: {e}"
    
    return None, "No JSON found in response"


def main():
    parser = argparse.ArgumentParser(description="LLM extraction using claude/codex CLI")
    parser.add_argument("--pdf-jsonl", required=True, help="PDF texts from extract_pdf_text.py")
    parser.add_argument("--data-dict", required=True, help="Data dictionary markdown")
    parser.add_argument("--out-jsonl", required=True, help="Output JSONL with extracted data")
    parser.add_argument("--limit", type=int, help="Limit number of PDFs to process")
    parser.add_argument("--cli", choices=["claude", "codex", "auto"], default="auto")
    parser.add_argument("--timeout", type=int, default=120, help="Timeout per PDF in seconds")
    args = parser.parse_args()

    # Check available CLIs
    claude_path, codex_path = check_cli_available()
    
    if args.cli == "auto":
        if claude_path:
            cli_tool = "claude"
            cli_func = call_claude_cli
            print(f"✅ Using claude CLI: {claude_path}")
        elif codex_path:
            cli_tool = "codex"
            cli_func = call_codex_exec
            print(f"✅ Using codex exec: {codex_path}")
        else:
            raise SystemExit("❌ Neither 'claude' nor 'codex' CLI found. Please install one.")
    elif args.cli == "claude":
        if not claude_path:
            raise SystemExit("❌ 'claude' CLI not found")
        cli_tool = "claude"
        cli_func = call_claude_cli
        print(f"✅ Using claude CLI: {claude_path}")
    else:  # codex
        if not codex_path:
            raise SystemExit("❌ 'codex' CLI not found")
        cli_tool = "codex"
        cli_func = call_codex_exec
        print(f"✅ Using codex exec: {codex_path}")

    # Load data dictionary
    data_dict_path = Path(args.data_dict)
    if not data_dict_path.exists():
        raise SystemExit(f"❌ Data dictionary not found: {data_dict_path}")
    
    data_dict_text = data_dict_path.read_text(encoding="utf-8")
    
    # Parse field names from data dictionary
    import re
    fields = re.findall(r'`([a-z_][a-z0-9_]*)`', data_dict_text)
    # Remove duplicates while preserving order
    seen = set()
    unique_fields = []
    for f in fields:
        if f not in seen:
            seen.add(f)
            unique_fields.append(f)
    
    print(f"📋 Extracted {len(unique_fields)} field names from data dictionary")

    # Load PDF texts
    pdf_jsonl = Path(args.pdf_jsonl)
    if not pdf_jsonl.exists():
        raise SystemExit(f"❌ PDF JSONL not found: {pdf_jsonl}")
    
    pdf_records = []
    with pdf_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                pdf_records.append(json.loads(line))
    
    # Filter successful extractions
    pdf_records = [r for r in pdf_records if r.get("error") is None]
    
    if args.limit:
        pdf_records = pdf_records[:args.limit]
    
    print(f"📄 Processing {len(pdf_records)} PDFs")

    # Process each PDF
    out_jsonl = Path(args.out_jsonl)
    out_jsonl.parent.mkdir(parents=True, exist_ok=True)
    
    results = []
    success_count = 0
    error_count = 0
    
    with out_jsonl.open("w", encoding="utf-8") as f:
        for i, pdf_rec in enumerate(pdf_records, 1):
            record_id = pdf_rec["record_id"]
            pdf_text = pdf_rec["text"]
            
            print(f"\n[{i}/{len(pdf_records)}] Processing {record_id}...", end=" ")
            
            # Build prompt
            prompt = build_extraction_prompt(
                record_id=record_id,
                pdf_text=pdf_text,
                fields=unique_fields,
                data_dict_snippet=data_dict_text,
            )
            
            # Call LLM
            response, error = cli_func(prompt, timeout=args.timeout)
            
            if error:
                print(f"❌ {error}")
                result = {
                    "record_id": record_id,
                    "status": "error",
                    "error": error,
                    "extracted_data": None,
                }
                error_count += 1
            else:
                # Parse JSON from response
                extracted_data, parse_error = extract_json_from_response(response)
                
                if parse_error:
                    print(f"⚠️  {parse_error}")
                    result = {
                        "record_id": record_id,
                        "status": "parse_error",
                        "error": parse_error,
                        "raw_response": response[:500],
                        "extracted_data": None,
                    }
                    error_count += 1
                else:
                    print(f"✅ Extracted {len(extracted_data)} fields")
                    result = {
                        "record_id": record_id,
                        "status": "success",
                        "error": None,
                        "extracted_data": extracted_data,
                    }
                    success_count += 1
            
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
            results.append(result)

    # Summary
    print(f"\n{'='*60}")
    print(f"📊 Extraction Summary:")
    print(f"   ✅ Success: {success_count}/{len(pdf_records)}")
    print(f"   ❌ Errors: {error_count}/{len(pdf_records)}")
    print(f"   📁 Output: {out_jsonl}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
