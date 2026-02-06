#!/usr/bin/env python3
"""Initialize a ROBINS-I assessment table from extraction data.

Generates a quality CSV with one row per (study x domain) following the
ROBINS-I (Risk Of Bias In Non-randomised Studies of Interventions) framework
for observational/cohort studies.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

ROBINS_I_DOMAINS = [
    "Confounding",
    "Selection of participants",
    "Classification of interventions",
    "Deviations from intended interventions",
    "Missing data",
    "Measurement of outcomes",
    "Selection of the reported result",
]

JUDGMENT_OPTIONS = "Low / Moderate / Serious / Critical / No information"


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
            for domain in ROBINS_I_DOMAINS:
                writer.writerow([sid, "ROBINS-I", domain, "", ""])


def write_markdown(out_path: Path, study_ids: list[str]) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Risk of Bias Assessment (ROBINS-I)",
        "",
        "## Tool",
        "",
        "ROBINS-I (Risk Of Bias In Non-randomised Studies of Interventions)",
        "",
        "## When to Use",
        "",
        "Use ROBINS-I for **non-randomised studies** (cohort studies, case-control "
        "studies, cross-sectional studies) that compare health effects of two or more "
        "interventions. For RCTs, use RoB 2 instead.",
        "",
        "## Domains",
        "",
    ]
    for i, domain in enumerate(ROBINS_I_DOMAINS, 1):
        lines.append(f"{i}. **{domain}**")
    lines.append("")

    lines.append("## Judgment Scale")
    lines.append("")
    lines.append("- **Low**: The study is comparable to a well-performed RCT for this domain")
    lines.append("- **Moderate**: The study is sound but cannot be considered comparable to a well-performed RCT")
    lines.append("- **Serious**: The study has some important problems")
    lines.append("- **Critical**: The study is too problematic to provide useful evidence")
    lines.append("- **No information**: Insufficient information to make a judgment")
    lines.append("")

    lines.append("## Overall Judgment Algorithm")
    lines.append("")
    lines.append("- **Low** overall: Low risk of bias for all domains")
    lines.append("- **Moderate** overall: Low or moderate risk for all domains")
    lines.append("- **Serious** overall: Serious risk in at least one domain, no critical")
    lines.append("- **Critical** overall: Critical risk in at least one domain")
    lines.append("")

    # Summary table
    lines.append("## Assessment Summary")
    lines.append("")
    header_cols = ["Study"] + ROBINS_I_DOMAINS + ["Overall"]
    lines.append("| " + " | ".join(header_cols) + " |")
    lines.append("| " + " | ".join(["---"] * len(header_cols)) + " |")

    ids = study_ids if study_ids else ["<study_id>"]
    for sid in ids:
        row = [sid] + [""] * (len(ROBINS_I_DOMAINS) + 1)
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    lines.append("## Signalling Questions")
    lines.append("")
    lines.append("### Domain 1: Bias due to confounding")
    lines.append("- 1.1 Is there potential for confounding of the effect of intervention?")
    lines.append("- 1.2 Was the analysis based on splitting participants by intervention received?")
    lines.append("- 1.3 Were confounding domains measured validly and reliably?")
    lines.append("- 1.4 Did the authors control for confounding appropriately?")
    lines.append("")
    lines.append("### Domain 2: Bias in selection of participants")
    lines.append("- 2.1 Was selection into the study related to intervention and outcome?")
    lines.append("- 2.2 Was selection into the study related to intervention and outcome (time-varying)?")
    lines.append("- 2.3 Do start of follow-up and start of intervention coincide?")
    lines.append("")
    lines.append("### Domain 3: Bias in classification of interventions")
    lines.append("- 3.1 Were intervention groups clearly defined?")
    lines.append("- 3.2 Was information used to define intervention recorded at start of intervention?")
    lines.append("- 3.3 Could classification of intervention status have been affected by outcome?")
    lines.append("")
    lines.append("### Domain 4: Bias due to deviations from intended interventions")
    lines.append("- 4.1 Were there deviations from the intended intervention beyond what would be expected?")
    lines.append("- 4.2 Were important co-interventions balanced across groups?")
    lines.append("- 4.3 Was an appropriate analysis used to account for deviations?")
    lines.append("")
    lines.append("### Domain 5: Bias due to missing data")
    lines.append("- 5.1 Were outcome data available for all or nearly all participants?")
    lines.append("- 5.2 Were participants excluded due to missing data on intervention status?")
    lines.append("- 5.3 Were participants excluded due to missing data on other variables?")
    lines.append("- 5.4 Are the proportions of missing data balanced across groups?")
    lines.append("")
    lines.append("### Domain 6: Bias in measurement of outcomes")
    lines.append("- 6.1 Could the outcome measure have been influenced by knowledge of intervention?")
    lines.append("- 6.2 Were outcome assessors aware of the intervention received?")
    lines.append("- 6.3 Were the methods of outcome assessment comparable across groups?")
    lines.append("")
    lines.append("### Domain 7: Bias in selection of the reported result")
    lines.append("- 7.1 Is the reported effect estimate likely selected from multiple outcome measurements?")
    lines.append("- 7.2 Is the reported effect estimate likely selected from multiple analyses?")
    lines.append("- 7.3 Is the reported effect estimate likely selected from different subgroups?")
    lines.append("")

    lines.append(
        "*Fill in the CSV file (`quality_robins_i.csv`) for structured data. "
        "Use this markdown for narrative assessment.*"
    )
    lines.append("")

    out_path.write_text("\n".join(lines))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Initialize ROBINS-I assessment tables from extraction data."
    )
    parser.add_argument(
        "--extraction",
        required=True,
        help="Path to extraction CSV (for study IDs)",
    )
    parser.add_argument(
        "--out-csv",
        required=True,
        help="Output CSV path (e.g., 03_screening/round-01/quality_robins_i.csv)",
    )
    parser.add_argument(
        "--out-md",
        required=True,
        help="Output markdown path (e.g., 03_screening/round-01/robins_i_assessment.md)",
    )
    args = parser.parse_args()

    study_ids = read_study_ids(Path(args.extraction))
    write_csv(Path(args.out_csv), study_ids)
    write_markdown(Path(args.out_md), study_ids)

    n = len(study_ids)
    n_rows = n * len(ROBINS_I_DOMAINS)
    print(f"ROBINS-I assessment initialized: {n} studies x {len(ROBINS_I_DOMAINS)} domains = {n_rows} rows")
    print(f"  CSV: {args.out_csv}")
    print(f"  MD:  {args.out_md}")


if __name__ == "__main__":
    main()
