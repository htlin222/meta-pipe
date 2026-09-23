#!/usr/bin/env python3
"""Create a JSON search audit with query hashes and parameters."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


def parse_kv(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    data: dict[str, str] = {}
    for line in path.read_text().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if key:
            data[key] = value
    return data


def read_query(path: Path, section: str) -> str:
    content = path.read_text().splitlines()
    start = None
    for i, line in enumerate(content):
        if line.strip().lower() == f"[{section}]":
            start = i + 1
            break
    if start is None:
        return ""
    query_lines = []
    for line in content[start:]:
        if line.strip().startswith("["):
            break
        if line.strip().startswith("#"):
            continue
        if line.strip():
            query_lines.append(line.strip())
    return " ".join(query_lines)


def hash_query(query: str, params: dict[str, str]) -> str:
    payload = json.dumps({"query": query, "params": params}, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate search audit JSON.")
    parser.add_argument("--root", default=".", help="Project root")
    parser.add_argument("--round", default="round-01", help="Search round")
    parser.add_argument("--queries", default=None, help="queries.txt path")
    parser.add_argument("--out", default=None, help="Output JSON path")
    args = parser.parse_args()

    root = Path(args.root)
    round_dir = root / "02_search" / args.round
    queries_path = Path(args.queries) if args.queries else round_dir / "queries.txt"

    endpoints = {
        "pubmed": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/",
        "scopus": "https://api.elsevier.com/content/search/scopus",
        "embase": "https://api.elsevier.com/content/embase/article",
        "cochrane": "https://api.cochrane.org/reviews",
        "ctgov": "https://clinicaltrials.gov/api/v2/studies",
    }

    logs = {
        "pubmed": round_dir / "log.md",
        "scopus": round_dir / "scopus.log",
        "embase": round_dir / "embase.log",
        "cochrane": round_dir / "cochrane.log",
        "ctgov": round_dir / "ctgov_log.txt",
    }

    audit = {"round": args.round, "databases": []}

    for db, log_path in logs.items():
        query = read_query(queries_path, db) if queries_path.exists() else ""
        params = parse_kv(log_path)
        audit_entry = {
            "database": db,
            "endpoint": endpoints.get(db, ""),
            "query": query,
            "query_hash": hash_query(query, params),
            "params": params,
            "log_path": str(log_path),
        }
        audit["databases"].append(audit_entry)

    out_path = Path(args.out) if args.out else round_dir / "search_audit.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(audit, indent=2) + "\n")


if __name__ == "__main__":
    main()
