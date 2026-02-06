#!/usr/bin/env python3
"""
AI-assisted title/abstract screening for systematic review.
Based on eligibility criteria in 01_protocol/eligibility.md
"""

import csv
import sys
import re
from pathlib import Path

# Screening criteria based on 01_protocol/eligibility.md
INCLUDE_KEYWORDS = {
    "population": [
        "HR+",
        "HR positive",
        "hormone receptor positive",
        "ER+",
        "ER positive",
        "HER2-",
        "HER2 negative",
        "HER2-negative",
        "metastatic",
        "advanced",
        "stage IV",
        "CDK4/6",
        "palbociclib",
        "ribociclib",
        "abemaciclib",
        "progression",
        "progressed",
        "failure",
        "resistant",
        "resistance",
        "post-CDK",
        "after CDK",
        "following CDK",
    ],
    "key_trials": [
        "postMONARCH",
        "MAINTAIN",
        "PALMIRA",
        "TROPiCS",
        "TROPION",
        "EMBER",
        "EMERALD",
        "CAPItello",
        "SOLAR",
        "BOLERO",
    ],
    "post_cdk_drugs": [
        "everolimus",
        "sacituzumab",
        "datopotamab",
        "elacestrant",
        "imlunestrant",
        "capivasertib",
        "alpelisib",
        "fulvestrant",
    ],
}

EXCLUDE_KEYWORDS = {
    "wrong_population": [
        "HER2-positive",
        "HER2+",
        "HER2 positive",
        "triple-negative",
        "triple negative",
        "TNBC",
        "adjuvant",
        "neoadjuvant",
        "CDK4/6 inhibitor-naïve",
        "CDK4/6-naïve",
    ],
    "wrong_design": [
        "systematic review",
        "meta-analysis",
        "review article",
        "case report",
        "case series",
        "preclinical",
        "in vitro",
        "animal",
        "mouse",
        "rat",
    ],
}


def screen_record(record_id, title, abstract, year):
    """
    Screen a single record based on title and abstract.

    Returns:
        decision (str): "I" (include), "E" (exclude), or "U" (uncertain)
        exclusion_reason (str): Code if excluded
        notes (str): Reasoning for decision
    """
    # Combine title and abstract for screening
    text = f"{title} {abstract}".lower()

    # Check for key trial names (automatic include)
    for trial in INCLUDE_KEYWORDS["key_trials"]:
        if trial.lower() in text:
            return "I", "", f"Key trial: {trial}"

    # Check for exclusion criteria first

    # Wrong population
    for keyword in EXCLUDE_KEYWORDS["wrong_population"]:
        if keyword.lower() in text:
            if "triple-negative" in keyword.lower() or "tnbc" in keyword.lower():
                return "E", "P1", f"TNBC population (keyword: {keyword})"
            if "her2-positive" in keyword.lower() or "her2+" in keyword.lower():
                return "E", "P1", f"HER2+ population (keyword: {keyword})"
            if "adjuvant" in keyword.lower() or "neoadjuvant" in keyword.lower():
                # Check if metastatic also mentioned
                if "metastatic" not in text and "advanced" not in text:
                    return "E", "P2", f"Early-stage only (keyword: {keyword})"
            if "naïve" in keyword.lower() or "naive" in keyword.lower():
                return "E", "P3", f"CDK4/6i-naïve population (keyword: {keyword})"

    # Wrong design
    for keyword in EXCLUDE_KEYWORDS["wrong_design"]:
        if keyword.lower() in text:
            if (
                "systematic review" in keyword.lower()
                or "meta-analysis" in keyword.lower()
            ):
                return "E", "D1", f"Review/meta-analysis (keyword: {keyword})"
            if "case report" in keyword.lower() or "case series" in keyword.lower():
                return "E", "D1", f"Case report/series (keyword: {keyword})"
            if keyword in ["preclinical", "in vitro", "animal", "mouse", "rat"]:
                return "E", "D2", f"Preclinical/animal study (keyword: {keyword})"

    # Check for inclusion criteria
    has_hr_positive = any(
        kw in text
        for kw in [
            "hr+",
            "hr positive",
            "hormone receptor positive",
            "er+",
            "er positive",
        ]
    )
    has_her2_negative = any(
        kw in text for kw in ["her2-", "her2 negative", "her2-negative"]
    )
    has_metastatic = any(kw in text for kw in ["metastatic", "advanced", "stage iv"])
    has_cdk46 = any(
        kw in text
        for kw in [
            "cdk4/6",
            "cdk 4/6",
            "palbociclib",
            "ribociclib",
            "abemaciclib",
            "ibrance",
            "kisqali",
            "verzenio",
        ]
    )
    has_progression = any(
        kw in text
        for kw in [
            "progression",
            "progressed",
            "failure",
            "resistant",
            "resistance",
            "post-cdk",
            "after cdk",
            "following cdk",
            "subsequent",
        ]
    )
    has_post_cdk_drug = any(kw in text for kw in INCLUDE_KEYWORDS["post_cdk_drugs"])

    # Decision logic
    if (
        has_hr_positive
        and has_her2_negative
        and has_metastatic
        and has_cdk46
        and has_progression
    ):
        return (
            "I",
            "",
            "Meets all inclusion criteria (HR+/HER2-/metastatic/post-CDK4/6)",
        )

    if (
        has_hr_positive
        and has_her2_negative
        and has_metastatic
        and has_cdk46
        and has_post_cdk_drug
    ):
        return "I", "", "HR+/HER2-/metastatic/CDK4/6 + post-CDK4/6 drug mentioned"

    if has_hr_positive and has_metastatic and has_cdk46 and has_progression:
        # Missing HER2 status but otherwise eligible
        return "U", "", "Likely eligible, HER2 status unclear from title/abstract"

    if has_cdk46 and has_progression and has_metastatic:
        # Missing HR+/HER2- but mentions progression
        return "U", "", "Post-CDK4/6 progression mentioned, HR/HER2 status unclear"

    if has_cdk46 and not has_progression:
        # CDK4/6 mentioned but no progression - likely first-line study
        return (
            "E",
            "P3",
            "CDK4/6i mentioned but no progression/resistance (likely first-line)",
        )

    # If none of the above, likely not relevant
    if not has_cdk46:
        return "E", "I1", "No CDK4/6 inhibitor mentioned"

    # Default to uncertain if unclear
    return "U", "", "Unclear eligibility from title/abstract, review full-text"


def main():
    import argparse

    parser = argparse.ArgumentParser(description="AI-assisted screening")
    parser.add_argument("--in-csv", required=True, help="Input decisions CSV")
    parser.add_argument(
        "--out-csv", required=True, help="Output decisions CSV with decision_r1"
    )
    parser.add_argument("--reviewer", default="AI_R1", help="Reviewer name")
    args = parser.parse_args()

    # Read input CSV
    records = []
    with open(args.in_csv, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    print(f"Processing {len(records)} records...")

    # Screen each record
    for i, record in enumerate(records, 1):
        if i % 50 == 0:
            print(f"  Processed {i}/{len(records)} records...")

        record_id = record["record_id"]
        title = record.get("title", "")
        abstract = record.get("abstract", "")
        year = record.get("year", "")

        decision, exclusion_reason, notes = screen_record(
            record_id, title, abstract, year
        )

        record["decision_r1"] = decision
        if exclusion_reason:
            record["exclusion_reason"] = exclusion_reason
        if notes:
            record["notes"] = notes

    # Write output CSV
    with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
        fieldnames = list(records[0].keys())
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    # Summary statistics
    include_count = sum(1 for r in records if r["decision_r1"] == "I")
    exclude_count = sum(1 for r in records if r["decision_r1"] == "E")
    uncertain_count = sum(1 for r in records if r["decision_r1"] == "U")

    print(f"\n✓ Screening complete!")
    print(f"  Include (I): {include_count} ({include_count / len(records) * 100:.1f}%)")
    print(f"  Exclude (E): {exclude_count} ({exclude_count / len(records) * 100:.1f}%)")
    print(
        f"  Uncertain (U): {uncertain_count} ({uncertain_count / len(records) * 100:.1f}%)"
    )
    print(
        f"  For full-text: {include_count + uncertain_count} ({(include_count + uncertain_count) / len(records) * 100:.1f}%)"
    )
    print(f"\nOutput: {args.out_csv}")


if __name__ == "__main__":
    main()
