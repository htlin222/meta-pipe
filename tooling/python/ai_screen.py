#!/usr/bin/env python3
"""
AI-powered screening for meta-analysis projects.
Uses `claude -p` CLI (OAuth) to screen studies against project eligibility criteria.

Supports two stages:
  - abstract (default): screen title/abstract from screening-database.csv
  - fulltext: re-screen included studies against full text (web/PDF) from manifest.csv

Topic-agnostic: reads eligibility.md from any project and applies generic
PICO-based exclusion codes. Outputs conform to the dual-review schema so
the result plugs directly into dual_review_agreement.py.

Usage:
    uv run tooling/python/ai_screen.py --project <name>
    uv run tooling/python/ai_screen.py --project <name> --reviewer 2
    uv run tooling/python/ai_screen.py --project <name> --stage fulltext
    uv run tooling/python/ai_screen.py --project <name> --stage fulltext --reviewer 2
"""

import argparse
import csv
import subprocess
import sys
from pathlib import Path

META_PIPE_ROOT = Path("/Users/htlin/meta-pipe")

EXCLUSION_CODES = """\
- P1: Wrong population
- P2: Wrong age group
- I1: Wrong intervention
- I2: Intervention used for wrong indication
- C1: Wrong comparator
- S1: Wrong study design (review/meta-analysis/editorial/commentary)
- S2: Case report or small series below minimum sample size
- S3: Preclinical/in vitro/animal study
- S4: Study protocol without results
- O1: No relevant outcomes reported
- O2: Insufficient follow-up duration
- T1: Outside date range
- T2: Conference abstract too old without full publication
- L1: Language not meeting criteria
- D1: Duplicate or superseded publication
- NONE: No exclusion (use for INCLUDE or MAYBE decisions)"""


def load_eligibility_criteria(project_path: Path) -> str:
    """Load PICO criteria from project's eligibility.md."""
    eligibility_file = project_path / "01_protocol" / "eligibility.md"
    if eligibility_file.exists():
        return eligibility_file.read_text()
    return ""


def screen_fulltext_one(
    title: str,
    record_id: str,
    doi: str,
    pmid: str,
    eligibility_criteria: str,
) -> dict:
    """
    Call `claude -p` to re-screen a study at the full-text stage.
    Uses web-available full text (PubMed, journal sites) to re-apply eligibility.
    Returns dict with decision, reason, confidence, exclusion_code.
    """
    prompt = f"""You are an expert systematic reviewer performing FULL-TEXT eligibility screening for a meta-analysis.

This study was previously INCLUDED at the title/abstract stage. Your task is to re-evaluate
its eligibility using the FULL TEXT of the article. Be more stringent than abstract screening —
at this stage, the study must clearly satisfy ALL eligibility criteria.

ELIGIBILITY CRITERIA (from the project protocol -- read carefully):
{eligibility_criteria}

STUDY TO SCREEN:
Record ID: {record_id}
Title: {title}
DOI: {doi}
PMID: {pmid}

INSTRUCTIONS:
1. Search for the full text of this study using the DOI or PMID.
2. Evaluate ALL eligibility criteria against the full-text content.
3. Pay special attention to: study design details, exact population definitions,
   intervention/comparator specifics, outcome measurement methods, and follow-up duration.
4. If the full text reveals ANY eligibility violation not apparent from the abstract, EXCLUDE.
5. Document the specific reason with reference to which criterion failed.

Respond in this EXACT format (one line each, no markdown, no extra text):
DECISION: [INCLUDE/EXCLUDE]
REASON: [Brief explanation referencing specific full-text content]
CONFIDENCE: [HIGH/MEDIUM/LOW]
EXCLUSION_CODE: [code or NONE]

Exclusion codes:
{EXCLUSION_CODES}
"""

    result = subprocess.run(
        ["claude", "-p", "--model", "haiku"],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=120,
    )

    if result.returncode != 0:
        raise RuntimeError(f"claude -p failed: {result.stderr.strip()}")

    parsed = {
        "decision": "include",
        "reason": "Unable to determine — defaulting to include",
        "confidence": "LOW",
        "exclusion_code": "NONE",
    }
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if line.startswith("DECISION:"):
            parsed["decision"] = line.split(":", 1)[1].strip().lower()
        elif line.startswith("REASON:"):
            parsed["reason"] = line.split(":", 1)[1].strip()
        elif line.startswith("CONFIDENCE:"):
            parsed["confidence"] = line.split(":", 1)[1].strip()
        elif line.startswith("EXCLUSION_CODE:"):
            parsed["exclusion_code"] = line.split(":", 1)[1].strip()

    # Full-text screening only allows INCLUDE or EXCLUDE (no MAYBE)
    if parsed["decision"] not in ("include", "exclude"):
        parsed["decision"] = "include"

    return parsed


def screen_one(title, abstract, year, authors, journal, eligibility_criteria) -> dict:
    """
    Call `claude -p` to screen a single study.
    Returns dict with decision, reason, confidence, exclusion_code.
    """
    prompt = f"""You are an expert systematic reviewer screening studies for a meta-analysis.

ELIGIBILITY CRITERIA (from the project protocol -- read carefully):
{eligibility_criteria}

STUDY TO SCREEN:
Title: {title}
Authors: {authors}
Journal: {journal}
Year: {year}
Abstract: {abstract[:1500] if abstract else "No abstract available"}

TASK:
Based on ONLY the title and abstract, decide if this study should be:
1. INCLUDE - clearly meets all eligibility criteria
2. EXCLUDE - clearly violates one or more eligibility criteria
3. MAYBE - uncertain, needs full-text review

When in doubt, prefer MAYBE over EXCLUDE (liberal screening at title/abstract stage).

Respond in this EXACT format (one line each, no markdown, no extra text):
DECISION: [INCLUDE/EXCLUDE/MAYBE]
REASON: [Brief explanation in one sentence]
CONFIDENCE: [HIGH/MEDIUM/LOW]
EXCLUSION_CODE: [code or NONE]

Exclusion codes:
{EXCLUSION_CODES}
"""

    result = subprocess.run(
        ["claude", "-p", "--model", "haiku"],
        input=prompt,
        capture_output=True,
        text=True,
        timeout=60,
    )

    if result.returncode != 0:
        raise RuntimeError(f"claude -p failed: {result.stderr.strip()}")

    parsed = {
        "decision": "maybe",
        "reason": "Unable to determine",
        "confidence": "LOW",
        "exclusion_code": "NONE",
    }
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if line.startswith("DECISION:"):
            parsed["decision"] = line.split(":", 1)[1].strip().lower()
        elif line.startswith("REASON:"):
            parsed["reason"] = line.split(":", 1)[1].strip()
        elif line.startswith("CONFIDENCE:"):
            parsed["confidence"] = line.split(":", 1)[1].strip()
        elif line.startswith("EXCLUSION_CODE:"):
            parsed["exclusion_code"] = line.split(":", 1)[1].strip()

    return parsed


def run_abstract_screening(args, project_path: Path) -> None:
    """Run title/abstract screening (original Stage 03 behavior)."""
    screening_db = project_path / "03_screening" / "screening-database.csv"
    round_dir = project_path / "03_screening" / args.round
    output_csv = round_dir / "decisions.csv"

    if not screening_db.exists():
        print(f"ERROR: {screening_db} not found. Run search stage first.")
        sys.exit(1)

    eligibility = load_eligibility_criteria(project_path)
    if not eligibility:
        print("WARNING: No eligibility.md found. AI will use basic heuristics.")

    round_dir.mkdir(parents=True, exist_ok=True)

    with open(screening_db, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        records = list(reader)

    print(f"Loaded {len(records)} records from {screening_db.name}")
    print(f"Filling Reviewer{args.reviewer} columns (AI screening)")

    decision_col = f"Reviewer{args.reviewer}_Decision"
    reason_col = f"Reviewer{args.reviewer}_Reason"

    screened = 0
    skipped = 0
    for i, record in enumerate(records, 1):
        if record.get(decision_col, "").strip():
            skipped += 1
            continue

        pmid = record.get("PMID", "")
        title = record.get("Title", "")
        abstract = record.get("Abstract", "")
        year = record.get("Year", "")
        authors = record.get("Authors", "")
        journal = record.get("Journal", "")

        print(f"\n[{i}/{len(records)}] PMID {pmid}")
        print(f"   {title[:80]}...")

        try:
            result = screen_one(title, abstract, year, authors, journal, eligibility)
            record[decision_col] = result["decision"]
            record[reason_col] = (
                f"{result['exclusion_code']}: {result['reason']}"
                if result["exclusion_code"] != "NONE"
                else result["reason"]
            )
            record["Notes"] = (
                record.get("Notes", "")
                + f" | AI-R{args.reviewer} confidence={result['confidence']}"
            ).strip(" |")
            screened += 1

            print(f"   -> {result['decision']} ({result['confidence']})")
            if result["exclusion_code"] != "NONE":
                print(f"      {result['exclusion_code']}: {result['reason']}")

        except Exception as e:
            print(f"   ERROR: {e}")
            record[decision_col] = "maybe"
            record[reason_col] = f"AI error: {e}"
            screened += 1

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    decisions = [r.get(decision_col, "").lower() for r in records]
    inc = decisions.count("include")
    exc = decisions.count("exclude")
    may = decisions.count("maybe")
    total = len(records)

    print(f"\n{'='*60}")
    print(f"SCREENING SUMMARY (Reviewer {args.reviewer} = AI)")
    print(f"{'='*60}")
    print(f"Total:    {total}")
    print(f"Screened: {screened}  (skipped {skipped} already decided)")
    print(f"  include: {inc} ({inc/total*100:.1f}%)")
    print(f"  exclude: {exc} ({exc/total*100:.1f}%)")
    print(f"  maybe:   {may} ({may/total*100:.1f}%)")
    print(f"{'='*60}")
    print(f"\nOutput: {output_csv}")

    if args.reviewer == 1:
        print(f"\nNext: run with --reviewer 2 for dual review, or have a human fill Reviewer2 columns.")
        print(f"Then: uv run ma-screening-quality/scripts/dual_review_agreement.py \\")
        print(f"        --file {output_csv} --col-a Reviewer1_Decision --col-b Reviewer2_Decision \\")
        print(f"        --out {round_dir}/agreement.md")


def run_fulltext_screening(args, project_path: Path) -> None:
    """Run full-text eligibility screening (Stage 04b).

    Reads manifest.csv from Stage 04, re-applies eligibility criteria against
    the full text of each included study, and outputs fulltext_decisions.csv.
    This implements PRISMA 2020 item 16 (full-text exclusion with reasons).
    """
    manifest_csv = project_path / "04_fulltext" / "manifest.csv"
    output_csv = project_path / "04_fulltext" / "fulltext_decisions.csv"

    if not manifest_csv.exists():
        print(f"ERROR: {manifest_csv} not found. Complete Stage 04 (fulltext retrieval) first.")
        sys.exit(1)

    eligibility = load_eligibility_criteria(project_path)
    if not eligibility:
        print("WARNING: No eligibility.md found. AI will use basic heuristics.")

    # Read manifest
    with open(manifest_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        manifest_records = list(reader)

    print(f"Loaded {len(manifest_records)} studies from {manifest_csv.name}")
    print(f"Filling FT_Reviewer{args.reviewer} columns (AI full-text screening)")

    # Build or load existing fulltext_decisions.csv
    ft_fieldnames = [
        "record_id",
        "title",
        "doi",
        "pmid",
        "FT_Reviewer1_Decision",
        "FT_Reviewer1_Reason",
        "FT_Reviewer2_Decision",
        "FT_Reviewer2_Reason",
        "FT_Final_Decision",
        "FT_Exclusion_Code",
    ]

    # Load existing decisions if re-running
    existing: dict[str, dict] = {}
    if output_csv.exists():
        with open(output_csv, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                rid = row.get("record_id", "").strip()
                if rid:
                    existing[rid] = row

    # Build records list from manifest
    records = []
    for m in manifest_records:
        rid = m.get("record_id", "").strip()
        if not rid:
            continue
        if rid in existing:
            records.append(existing[rid])
        else:
            records.append({
                "record_id": rid,
                "title": m.get("title", ""),
                "doi": m.get("doi", ""),
                "pmid": m.get("pmid", ""),
                "FT_Reviewer1_Decision": "",
                "FT_Reviewer1_Reason": "",
                "FT_Reviewer2_Decision": "",
                "FT_Reviewer2_Reason": "",
                "FT_Final_Decision": "",
                "FT_Exclusion_Code": "",
            })

    decision_col = f"FT_Reviewer{args.reviewer}_Decision"
    reason_col = f"FT_Reviewer{args.reviewer}_Reason"

    screened = 0
    skipped = 0
    for i, record in enumerate(records, 1):
        # Skip if this reviewer already decided
        if record.get(decision_col, "").strip():
            skipped += 1
            continue

        rid = record["record_id"]
        title = record.get("title", "")
        doi = record.get("doi", "")
        pmid = record.get("pmid", "")

        print(f"\n[{i}/{len(records)}] {rid}")
        print(f"   {title[:80]}...")

        try:
            result = screen_fulltext_one(title, rid, doi, pmid, eligibility)
            record[decision_col] = result["decision"]
            record[reason_col] = (
                f"{result['exclusion_code']}: {result['reason']}"
                if result["exclusion_code"] != "NONE"
                else result["reason"]
            )
            screened += 1

            print(f"   -> {result['decision']} ({result['confidence']})")
            if result["exclusion_code"] != "NONE":
                print(f"      {result['exclusion_code']}: {result['reason']}")

        except Exception as e:
            print(f"   ERROR: {e}")
            record[decision_col] = "include"
            record[reason_col] = f"AI error (defaulting to include): {e}"
            screened += 1

    # Resolve final decisions (after both reviewers)
    for record in records:
        r1 = record.get("FT_Reviewer1_Decision", "").strip().lower()
        r2 = record.get("FT_Reviewer2_Decision", "").strip().lower()
        if r1 and r2:
            if r1 == "exclude" or r2 == "exclude":
                # Conservative: if either reviewer excludes, mark as exclude
                # (requires conflict resolution by human if disagreed)
                record["FT_Final_Decision"] = "exclude"
                # Use the exclusion reason from whichever reviewer excluded
                if r1 == "exclude":
                    reason = record.get("FT_Reviewer1_Reason", "")
                else:
                    reason = record.get("FT_Reviewer2_Reason", "")
                # Extract exclusion code from reason string
                code = reason.split(":")[0].strip() if ":" in reason else "NONE"
                record["FT_Exclusion_Code"] = code
            else:
                record["FT_Final_Decision"] = "include"
                record["FT_Exclusion_Code"] = "NONE"

    # Write fulltext_decisions.csv
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=ft_fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)

    # Summary
    decisions = [r.get(decision_col, "").lower() for r in records]
    inc = decisions.count("include")
    exc = decisions.count("exclude")
    total = len(records)

    print(f"\n{'='*60}")
    print(f"FULL-TEXT SCREENING SUMMARY (Reviewer {args.reviewer} = AI)")
    print(f"{'='*60}")
    print(f"Total:    {total}")
    print(f"Screened: {screened}  (skipped {skipped} already decided)")
    print(f"  include: {inc} ({inc/total*100:.1f}%)" if total else "  include: 0")
    print(f"  exclude: {exc} ({exc/total*100:.1f}%)" if total else "  exclude: 0")
    print(f"{'='*60}")
    print(f"\nOutput: {output_csv}")

    # Check if both reviewers are done
    final_decisions = [r.get("FT_Final_Decision", "").strip() for r in records]
    resolved = sum(1 for d in final_decisions if d)

    if resolved == total and total > 0:
        ft_included = sum(1 for d in final_decisions if d.lower() == "include")
        ft_excluded = sum(1 for d in final_decisions if d.lower() == "exclude")
        print(f"\nFinal decisions resolved: {resolved}/{total}")
        print(f"  -> {ft_included} INCLUDE (proceed to Stage 05 extraction)")
        print(f"  -> {ft_excluded} EXCLUDE (with reasons for PRISMA flow diagram)")
        agreement_out = project_path / "04_fulltext" / "ft_agreement.md"
        print(f"\nNext: compute full-text inter-rater agreement:")
        print(f"  uv run ma-screening-quality/scripts/dual_review_agreement.py \\")
        print(f"    --file {output_csv} \\")
        print(f"    --col-a FT_Reviewer1_Decision --col-b FT_Reviewer2_Decision \\")
        print(f"    --out {agreement_out}")
    elif args.reviewer == 1:
        print(f"\nNext: run with --reviewer 2 for dual review:")
        print(f"  uv run tooling/python/ai_screen.py --project {args.project} --stage fulltext --reviewer 2")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI-powered screening for meta-analysis projects (abstract or full-text)"
    )
    parser.add_argument("--project", required=True, help="Project name under projects/")
    parser.add_argument(
        "--stage",
        choices=["abstract", "fulltext"],
        default="abstract",
        help="Screening stage: 'abstract' (default, Stage 03) or 'fulltext' (Stage 04b)",
    )
    parser.add_argument(
        "--reviewer",
        type=int,
        choices=[1, 2],
        default=1,
        help="Which reviewer column to fill (1 or 2, default: 1)",
    )
    parser.add_argument(
        "--round",
        default="round-01",
        help="Screening round directory name (default: round-01)",
    )
    args = parser.parse_args()

    project_path = META_PIPE_ROOT / "projects" / args.project

    if args.stage == "fulltext":
        run_fulltext_screening(args, project_path)
    else:
        run_abstract_screening(args, project_path)


if __name__ == "__main__":
    main()
