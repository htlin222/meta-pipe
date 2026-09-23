#!/usr/bin/env python3
"""SHA-256 manifest of the artifacts a reader would need to reproduce a review.

Two things this script used to get wrong, both of which defeat its purpose:

* It hashed only `06_analysis/figures` and `06_analysis/tables`. A figure's
  checksum proves the PNG has not changed; it says nothing about whether the
  numbers behind it did. The extraction database, the analysis scripts, the
  search strings and the rendered manuscript are what a reproducibility audit
  actually needs, and they are included here.
* It keyed the manifest by ABSOLUTE path, so a manifest generated on one
  machine could not be verified on another. Keys are now relative to the
  project root.

Verify a manifest later with:
    uv run ma-end-to-end/scripts/hash_artifacts.py --root <project> --verify <manifest>

Usage:
    uv run ma-end-to-end/scripts/hash_artifacts.py --root projects/<name> [--out PATH]
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

# group -> (subdirectory, glob). Order is the order a reader would check them.
GROUPS: list[tuple[str, str, str]] = [
    ("protocol", "01_protocol", "*.md"),
    ("protocol", "01_protocol", "*.yaml"),
    ("search_strategies", "02_search", "round-*/queries.txt"),
    ("screening", "03_screening", "round-*/decisions.csv"),
    ("fulltext", "04_fulltext", "*.csv"),
    ("extraction", "05_extraction", "*.csv"),
    ("extraction", "05_extraction", "*.sqlite"),
    ("analysis_code", "06_analysis", "*.R"),
    ("analysis_code", "06_analysis", "renv.lock"),
    ("analysis_inputs", "06_analysis", "nma_*.csv"),
    ("tables", "06_analysis/tables", "*.*"),
    ("figures", "06_analysis/figures", "*.png"),
    ("manuscript", "07_manuscript", "*.qmd"),
    ("manuscript", "07_manuscript", "index.pdf"),
    ("manuscript", "07_manuscript", "index.html"),
    ("manuscript", "07_manuscript", "references.bib"),
    ("supplementary", "07_manuscript/supplementary", "*.*"),
    ("certainty", "08_reviews", "*.csv"),
    ("certainty", "08_reviews", "*.md"),
    ("qa", "09_qa", "*.md"),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build(root: Path) -> dict:
    groups: dict[str, dict[str, str]] = {}
    for group, subdir, pattern in GROUPS:
        base = root / subdir
        if not base.exists():
            continue
        for p in sorted(base.glob(pattern)):
            if not p.is_file():
                continue
            groups.setdefault(group, {})[str(p.relative_to(root))] = sha256(p)
    total = sum(len(v) for v in groups.values())
    return {
        "project": root.name,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "algorithm": "sha256",
        "paths_relative_to": "project root",
        "file_count": total,
        "group_counts": {k: len(v) for k, v in sorted(groups.items())},
        "files": {k: v for k, v in sorted(groups.items())},
    }


def verify(root: Path, manifest_path: Path) -> int:
    data = json.loads(manifest_path.read_text())
    missing, changed, ok = [], [], 0
    for group, files in data.get("files", {}).items():
        for rel, want in files.items():
            p = root / rel
            if not p.exists():
                missing.append(rel)
            elif sha256(p) != want:
                changed.append(rel)
            else:
                ok += 1
    print(f"{ok} unchanged, {len(changed)} changed, {len(missing)} missing")
    for rel in changed[:20]:
        print(f"  CHANGED  {rel}")
    for rel in missing[:20]:
        print(f"  MISSING  {rel}")
    return 1 if (changed or missing) else 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", default=".", help="Project root")
    ap.add_argument(
        "--out",
        default="09_qa/artifact_hashes.json",
        help="Output path, relative to --root",
    )
    ap.add_argument(
        "--verify",
        default=None,
        help="Verify an existing manifest instead of writing one",
    )
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if args.verify:
        raise SystemExit(verify(root, Path(args.verify).resolve()))

    data = build(root)
    out_path = (root / args.out).resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, indent=2) + "\n")
    print(f"{data['file_count']} artifacts hashed -> {out_path.relative_to(root)}")
    for k, n in data["group_counts"].items():
        print(f"  {k:20s} {n:4d}")


if __name__ == "__main__":
    main()
