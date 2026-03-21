#!/usr/bin/env python3
"""Validate continuity between pipeline stages (record IDs and counts)."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Set, Tuple


def read_bib_ids(path: Path) -> Set[str]:
    if not path.exists():
        return set()
    from bibtexparser import loads

    bib = loads(path.read_text())
    return {entry.get("ID", "").strip() for entry in bib.entries if entry.get("ID")}


def read_csv_ids(path: Path, key: str) -> Set[str]:
    if not path.exists():
        return set()
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return {row.get(key, "").strip() for row in reader if row.get(key, "").strip()}


def read_decisions(path: Path, decision_col: str) -> Tuple[Set[str], Set[str]]:
    included = set()
    all_ids = set()
    if not path.exists():
        return included, all_ids
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rid = (row.get("record_id") or "").strip()
            if not rid:
                continue
            all_ids.add(rid)
            decision = (row.get(decision_col) or "").strip().lower()
            if decision == "include":
                included.add(rid)
    return included, all_ids


def load_manifest_ids(path: Path) -> Tuple[Set[str], Optional[str]]:
    if not path.exists():
        return set(), "missing_manifest"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "record_id" not in reader.fieldnames:
            return set(), "missing_record_id_column"
        ids = {row.get("record_id", "").strip() for row in reader if row.get("record_id", "").strip()}
        return ids, None


def load_extraction_ids(path: Path) -> Tuple[Set[str], Optional[str]]:
    if not path.exists():
        return set(), "missing_extraction"
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return set(), "missing_headers"
        if "record_id" in reader.fieldnames:
            ids = {row.get("record_id", "").strip() for row in reader if row.get("record_id", "").strip()}
            return ids, None
        if "study_id" in reader.fieldnames:
            ids = {row.get("study_id", "").strip() for row in reader if row.get("study_id", "").strip()}
            return ids, "record_id_missing_using_study_id"
    return set(), "missing_record_id"


def load_study_map(path: Path) -> Dict[str, str]:
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        mapping = {}
        for row in reader:
            record_id = (row.get("record_id") or "").strip()
            study_id = (row.get("study_id") or "").strip()
            if record_id and study_id:
                mapping[study_id] = record_id
        return mapping


def load_db_total(path: Path) -> Optional[int]:
    if not path.exists():
        return None
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            if (row.get("database") or "").strip().lower() == "total":
                try:
                    return int(row.get("retrieved", "0"))
                except ValueError:
                    return None
    return None


def write_report(out_path: Path, sections: List[str], json_out: Optional[Path], payload: dict) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(sections) + "\n")
    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(json.dumps(payload, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate stage transitions.")
    parser.add_argument("--root", default=None, help="Project root (default: repo root)")
    parser.add_argument("--round", default="round-01", help="Round name")
    parser.add_argument("--from-stage", required=True, help="From stage number (e.g., 02)")
    parser.add_argument("--to-stage", required=True, help="To stage number (e.g., 03)")
    parser.add_argument(
        "--check",
        action="append",
        default=None,
        choices=["record_ids_match", "counts_reconcile"],
        help="Check(s) to run",
    )
    parser.add_argument("--decisions-column", default="final_decision", help="Decision column")
    parser.add_argument("--out", default="09_qa/stage_transition_report.md", help="Output report path")
    parser.add_argument("--out-json", default=None, help="Output JSON path")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    root = Path(args.root).resolve() if args.root else repo_root

    from_stage = args.from_stage.zfill(2)
    to_stage = args.to_stage.zfill(2)
    stage_pair = f"{from_stage}->{to_stage}"

    sections = [f"# Stage Transition Validation ({stage_pair})", ""]
    payload: Dict[str, object] = {"stage_pair": stage_pair, "checks": {}, "ok": True}
    failures: List[str] = []

    round_dir = root / "02_search" / args.round
    decisions_csv = root / "03_screening" / args.round / "decisions.csv"
    included_bib = root / "03_screening" / args.round / "included.bib"
    manifest_csv = root / "04_fulltext" / "manifest.csv"
    fulltext_decisions_csv = root / "04_fulltext" / "fulltext_decisions.csv"
    extraction_csv = root / "05_extraction" / "extraction.csv"
    study_map_csv = root / "05_extraction" / "study_map.csv"

    checks = args.check or ["record_ids_match", "counts_reconcile"]

    if "record_ids_match" in checks:
        check_result = {"ok": True, "notes": []}
        if stage_pair == "02->03":
            dedupe_bib = round_dir / "dedupe.bib"
            dedupe_ids = read_bib_ids(dedupe_bib)
            _, decision_ids = read_decisions(decisions_csv, args.decisions_column)
            missing_in_bib = sorted(decision_ids - dedupe_ids)
            missing_in_decisions = sorted(dedupe_ids - decision_ids)
            check_result["notes"].append(f"dedupe_records: {len(dedupe_ids)}")
            check_result["notes"].append(f"decisions_records: {len(decision_ids)}")
            if missing_in_bib or missing_in_decisions:
                check_result["ok"] = False
                if missing_in_bib:
                    check_result["notes"].append(f"decision_ids_not_in_bib: {len(missing_in_bib)}")
                if missing_in_decisions:
                    check_result["notes"].append(f"bib_ids_not_in_decisions: {len(missing_in_decisions)}")
        elif stage_pair == "03->04":
            included_ids, _ = read_decisions(decisions_csv, args.decisions_column)
            manifest_ids, manifest_issue = load_manifest_ids(manifest_csv)
            check_result["notes"].append(f"included_records: {len(included_ids)}")
            if manifest_issue:
                check_result["ok"] = False
                check_result["notes"].append(f"manifest_issue: {manifest_issue}")
            else:
                check_result["notes"].append(f"manifest_records: {len(manifest_ids)}")
                missing = sorted(included_ids - manifest_ids)
                extra = sorted(manifest_ids - included_ids)
                if missing or extra:
                    check_result["ok"] = False
                    if missing:
                        check_result["notes"].append(f"included_missing_in_manifest: {len(missing)}")
                    if extra:
                        check_result["notes"].append(f"manifest_not_in_included: {len(extra)}")
        elif stage_pair == "04->04b":
            manifest_ids, manifest_issue = load_manifest_ids(manifest_csv)
            ft_ids, ft_issue = load_manifest_ids(fulltext_decisions_csv)
            check_result["notes"].append(f"manifest_records: {len(manifest_ids)}")
            if manifest_issue:
                check_result["ok"] = False
                check_result["notes"].append(f"manifest_issue: {manifest_issue}")
            if ft_issue:
                check_result["ok"] = False
                check_result["notes"].append(f"fulltext_decisions_issue: {ft_issue}")
            else:
                check_result["notes"].append(f"fulltext_decisions_records: {len(ft_ids)}")
                missing = sorted(manifest_ids - ft_ids)
                extra = sorted(ft_ids - manifest_ids)
                if missing or extra:
                    check_result["ok"] = False
                    if missing:
                        check_result["notes"].append(f"manifest_missing_in_ft_decisions: {len(missing)}")
                    if extra:
                        check_result["notes"].append(f"ft_decisions_not_in_manifest: {len(extra)}")
        elif stage_pair in ("04->05", "04b->05"):
            # Stage 05 should only contain studies with FT_Final_Decision=include
            # If fulltext_decisions.csv exists, use it as the source of truth
            if fulltext_decisions_csv.exists():
                ft_included, _ = read_decisions(fulltext_decisions_csv, "FT_Final_Decision")
                source_ids = ft_included
                check_result["notes"].append(f"ft_included_records: {len(ft_included)}")
            else:
                source_ids, manifest_issue = load_manifest_ids(manifest_csv)
                if manifest_issue:
                    check_result["ok"] = False
                    check_result["notes"].append(f"manifest_issue: {manifest_issue}")
                check_result["notes"].append(f"manifest_records (no FT screening): {len(source_ids)}")
                check_result["notes"].append("WARNING: fulltext_decisions.csv missing — PRISMA item 16 not met")
            extraction_ids, extraction_issue = load_extraction_ids(extraction_csv)
            mapping = load_study_map(study_map_csv)
            if extraction_issue == "record_id_missing_using_study_id" and mapping:
                mapped = {mapping.get(study_id, "") for study_id in extraction_ids}
                extraction_ids = {rid for rid in mapped if rid}
                extraction_issue = None
            if extraction_issue:
                check_result["notes"].append(f"extraction_issue: {extraction_issue}")
            if mapping:
                check_result["notes"].append(f"study_map_records: {len(mapping)}")
            check_result["notes"].append(f"extraction_records: {len(extraction_ids)}")
            if source_ids and extraction_ids:
                missing = sorted(source_ids - extraction_ids)
                extra = sorted(extraction_ids - source_ids)
                if missing or extra:
                    check_result["ok"] = False
                    if missing:
                        check_result["notes"].append(f"source_missing_in_extraction: {len(missing)}")
                    if extra:
                        check_result["notes"].append(f"extraction_not_in_source: {len(extra)}")
        else:
            check_result["notes"].append("record_id check not defined for this stage pair.")
        if not check_result["ok"]:
            failures.append("record_ids_match")
        payload["checks"]["record_ids_match"] = check_result
        sections.append("## Record ID Continuity")
        sections.extend([f"- {note}" for note in check_result["notes"]])
        sections.append("")

    if "counts_reconcile" in checks:
        count_result = {"ok": True, "notes": []}
        if stage_pair == "02->03":
            dedupe_ids = read_bib_ids(round_dir / "dedupe.bib")
            _, decision_ids = read_decisions(decisions_csv, args.decisions_column)
            total_retrieved = load_db_total(round_dir / "db_counts.csv")
            count_result["notes"].append(f"dedupe_records: {len(dedupe_ids)}")
            count_result["notes"].append(f"decisions_records: {len(decision_ids)}")
            if total_retrieved is not None:
                count_result["notes"].append(f"db_total_retrieved: {total_retrieved}")
                if total_retrieved < len(dedupe_ids):
                    count_result["ok"] = False
                    count_result["notes"].append("db_total_retrieved < dedupe_records")
            if len(dedupe_ids) != len(decision_ids):
                count_result["ok"] = False
                count_result["notes"].append("dedupe_records != decisions_records")
        elif stage_pair == "03->04":
            included_ids, _ = read_decisions(decisions_csv, args.decisions_column)
            included_bib_ids = read_bib_ids(included_bib)
            manifest_ids, manifest_issue = load_manifest_ids(manifest_csv)
            count_result["notes"].append(f"included_decisions: {len(included_ids)}")
            count_result["notes"].append(f"included_bib: {len(included_bib_ids)}")
            if manifest_issue:
                count_result["ok"] = False
                count_result["notes"].append(f"manifest_issue: {manifest_issue}")
            else:
                count_result["notes"].append(f"manifest_records: {len(manifest_ids)}")
            if included_bib_ids and len(included_bib_ids) != len(included_ids):
                count_result["ok"] = False
                count_result["notes"].append("included_bib != included_decisions")
            if manifest_ids and len(manifest_ids) != len(included_ids):
                count_result["ok"] = False
                count_result["notes"].append("manifest_records != included_decisions")
        elif stage_pair == "04->04b":
            manifest_ids, manifest_issue = load_manifest_ids(manifest_csv)
            ft_ids, ft_issue = load_manifest_ids(fulltext_decisions_csv)
            count_result["notes"].append(f"manifest_records: {len(manifest_ids)}")
            if ft_issue:
                count_result["ok"] = False
                count_result["notes"].append(f"fulltext_decisions_issue: {ft_issue}")
            else:
                count_result["notes"].append(f"fulltext_decisions_records: {len(ft_ids)}")
                if len(manifest_ids) != len(ft_ids):
                    count_result["ok"] = False
                    count_result["notes"].append("manifest_records != fulltext_decisions_records")
        elif stage_pair in ("04->05", "04b->05"):
            if fulltext_decisions_csv.exists():
                ft_included, ft_all = read_decisions(fulltext_decisions_csv, "FT_Final_Decision")
                count_result["notes"].append(f"ft_total_screened: {len(ft_all)}")
                count_result["notes"].append(f"ft_included: {len(ft_included)}")
                ft_excluded = len(ft_all) - len(ft_included)
                count_result["notes"].append(f"ft_excluded: {ft_excluded}")
                source_count = len(ft_included)
            else:
                source_ids, manifest_issue = load_manifest_ids(manifest_csv)
                if manifest_issue:
                    count_result["ok"] = False
                    count_result["notes"].append(f"manifest_issue: {manifest_issue}")
                source_count = len(source_ids)
                count_result["notes"].append(f"manifest_records (no FT screening): {source_count}")
            extraction_ids, extraction_issue = load_extraction_ids(extraction_csv)
            mapping = load_study_map(study_map_csv)
            if extraction_issue == "record_id_missing_using_study_id" and mapping:
                mapped = {mapping.get(study_id, "") for study_id in extraction_ids}
                extraction_ids = {rid for rid in mapped if rid}
                extraction_issue = None
            if extraction_issue:
                count_result["notes"].append(f"extraction_issue: {extraction_issue}")
            if mapping:
                count_result["notes"].append(f"study_map_records: {len(mapping)}")
            count_result["notes"].append(f"extraction_records: {len(extraction_ids)}")
            if source_count and extraction_ids and source_count != len(extraction_ids):
                count_result["ok"] = False
                count_result["notes"].append("source_records != extraction_records")
        else:
            count_result["notes"].append("count reconciliation not defined for this stage pair.")

        if not count_result["ok"]:
            failures.append("counts_reconcile")
        payload["checks"]["counts_reconcile"] = count_result
        sections.append("## Count Reconciliation")
        sections.extend([f"- {note}" for note in count_result["notes"]])
        sections.append("")

    if failures:
        payload["ok"] = False
        sections.append("## Status")
        sections.append(f"- FAILED checks: {', '.join(sorted(set(failures)))}")
    else:
        sections.append("## Status")
        sections.append("- All requested checks passed.")

    out_path = root / args.out
    json_out = root / args.out_json if args.out_json else None
    write_report(out_path, sections, json_out, payload)

    if failures:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
