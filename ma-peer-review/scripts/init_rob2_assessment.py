#!/usr/bin/env python3
"""Initialize a Cochrane RoB 2 assessment table from extraction data.

Generates a quality.csv with one row per (study x domain) following the
Cochrane Risk of Bias 2 (RoB 2) framework for Randomized Controlled Trials.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROB2_DOMAINS = [
    "Randomization",
    "Deviations",
    "Missing data",
    "Outcome measurement",
    "Selective reporting",
]

JUDGMENT_OPTIONS = "Low / Some concerns / High"


def read_study_ids(csv_path: Path) -> list[str]:
    """Extract unique study IDs from extraction CSV."""
    if not csv_path.exists():
        return []

    with csv_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []

        id_key = None
        for key in ("study_id", "record_id", "id"):
            if key in headers:
                id_key = key
                break

        if not id_key:
            return []

        seen: set[str] = set()
        ids: list[str] = []
        for row in reader:
            sid = row.get(id_key, "").strip()
            if sid and sid not in seen:
                seen.add(sid)
                ids.append(sid)
    return ids


def write_csv(out_path: Path, study_ids: list[str]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    headers = ["record_id", "tool", "domain", "judgment", "notes"]

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        if not study_ids:
            study_ids = ["<study_id>"]

        for sid in study_ids:
            for domain in ROB2_DOMAINS:
                writer.writerow([sid, "RoB2", domain, "", ""])


def write_markdown(out_path: Path, study_ids: list[str]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Risk of Bias Assessment (Cochrane RoB 2)",
        "",
        "## Tool",
        "",
        "Cochrane Risk of Bias 2 (RoB 2) for Randomized Controlled Trials",
        "",
        "## Domains",
        "",
    ]
    for i, domain in enumerate(ROB2_DOMAINS, 1):
        lines.append(f"{i}. **{domain}**")
    lines.append("")

    lines.append("## Judgment Scale")
    lines.append("")
    lines.append("- **Low**: The study is judged to be at low risk of bias for this domain")
    lines.append(
        "- **Some concerns**: The study is judged to raise some concerns "
        "about bias for this domain"
    )
    lines.append("- **High**: The study is judged to be at high risk of bias for this domain")
    lines.append("")

    lines.append("## Overall Judgment Algorithm")
    lines.append("")
    lines.append("- **Low** overall: Low risk of bias for all domains")
    lines.append("- **Some concerns** overall: Some concerns in at least one domain, no high risk")
    lines.append("- **High** overall: High risk of bias in at least one domain, or some concerns in multiple domains")
    lines.append("")

    # Summary table
    lines.append("## Assessment Summary")
    lines.append("")
    header_cols = ["Study"] + ROB2_DOMAINS + ["Overall"]
    lines.append("| " + " | ".join(header_cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(header_cols)) + " |")

    ids = study_ids if study_ids else ["<study_id>"]
    for sid in ids:
        row = [sid] + [""] * (len(ROB2_DOMAINS) + 1)
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    lines.append("## Signalling Questions")
    lines.append("")
    lines.append("### Domain 1: Randomization process")
    lines.append("- 1.1 Was the allocation sequence random?")
    lines.append("- 1.2 Was the allocation sequence concealed until participants were enrolled?")
    lines.append("- 1.3 Did baseline differences suggest a problem with randomization?")
    lines.append("")
    lines.append("### Domain 2: Deviations from intended interventions")
    lines.append("- 2.1 Were participants aware of their assigned intervention?")
    lines.append("- 2.2 Were carers/people delivering aware of assigned intervention?")
    lines.append("- 2.3 Were there deviations due to the trial context?")
    lines.append("- 2.4 Were deviations balanced between groups?")
    lines.append("- 2.5 Was an appropriate analysis used (ITT)?")
    lines.append("")
    lines.append("### Domain 3: Missing outcome data")
    lines.append("- 3.1 Were data available for all or nearly all participants?")
    lines.append("- 3.2 Is there evidence that the result was not biased by missing data?")
    lines.append("- 3.3 Could missingness depend on the true value of the outcome?")
    lines.append("")
    lines.append("### Domain 4: Measurement of the outcome")
    lines.append("- 4.1 Was the method of measuring the outcome inappropriate?")
    lines.append("- 4.2 Could measurement differ between groups?")
    lines.append("- 4.3 Were outcome assessors aware of the intervention received?")
    lines.append("- 4.4 Could assessment have been influenced by knowledge of intervention?")
    lines.append("")
    lines.append("### Domain 5: Selection of the reported result")
    lines.append("- 5.1 Were the data analyzed in accordance with a pre-specified plan?")
    lines.append("- 5.2 Is the numerical result likely selected from multiple analyses?")
    lines.append("- 5.3 Is the numerical result likely selected from multiple measurements?")
    lines.append("")

    lines.append(
        "*Fill in the CSV file (`quality_rob2.csv`) for structured data. "
        "Use this markdown for narrative assessment.*"
    )
    lines.append("")

    out_path.write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Initialize RoB 2 assessment tables from extraction data."
    )
    parser.add_argument(
        "--extraction",
        required=True,
        help="Path to extraction CSV (for study IDs)",
    )
    parser.add_argument(
        "--out-csv",
        required=True,
        help="Output CSV path (e.g., 03_screening/round-01/quality_rob2.csv)",
    )
    parser.add_argument(
        "--out-md",
        required=True,
        help="Output markdown path (e.g., 03_screening/round-01/rob2_assessment.md)",
    )
    args = parser.parse_args()

    study_ids = read_study_ids(Path(args.extraction))
    write_csv(Path(args.out_csv), study_ids)
    write_markdown(Path(args.out_md), study_ids)

    n = len(study_ids)
    n_rows = n * len(ROB2_DOMAINS)
    print(f"RoB 2 assessment initialized: {n} studies x {len(ROB2_DOMAINS)} domains = {n_rows} rows")
    print(f"  CSV: {args.out_csv}")
    print(f"  MD:  {args.out_md}")


if __name__ == "__main__":
    main()
