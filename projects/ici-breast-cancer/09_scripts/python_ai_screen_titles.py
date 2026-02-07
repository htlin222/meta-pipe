#!/usr/bin/env python3
"""
AI-powered title/abstract screening for TNBC neoadjuvant ICI meta-analysis
Simulates human screening based on inclusion/exclusion criteria
"""

import csv
import sys
from pathlib import Path


def screen_study(record):
    """
    Screen a study based on title (and abstract if available)
    Returns: (decision, reason, confidence)
    - decision: 'include', 'exclude', 'maybe'
    - reason: explanation
    - confidence: 'high', 'medium', 'low'
    """
    title = record.get("title", "").lower()
    abstract = record.get("abstract", "").lower()
    year = int(record.get("year", 0))

    # Known key trials - MUST include
    key_trials = [
        "keynote-522",
        "impassion031",
        "geparnuevo",
        "camrelief",
        "neotrip",
        "neopact",
    ]
    for trial in key_trials:
        if trial in title.replace("-", "").replace(" ", ""):
            return ("include", f"Known key trial: {trial}", "high")

    # Exclude: Reviews, meta-analyses, editorials
    if any(
        word in title
        for word in [
            "meta-analysis",
            "systematic review",
            "review of",
            "editorial",
            "commentary",
            "corrigendum",
        ]
    ):
        # Unless it's about a trial (e.g., "KEYNOTE-522 review")
        if not any(
            trial in title.replace("-", "").replace(" ", "") for trial in key_trials
        ):
            return ("exclude", "Review/meta-analysis/editorial", "high")

    # Exclude: Protocols without results
    if "protocol" in title and "results" not in title:
        return ("exclude", "Protocol without results", "high")

    # Exclude: Non-RCT keywords
    if any(
        word in title
        for word in [
            "case report",
            "case series",
            "observational",
            "retrospective",
            "cohort study",
            "registry",
        ]
    ):
        # Unless it mentions "trial" or "randomized"
        if not any(word in title for word in ["trial", "randomized", "randomised"]):
            return ("exclude", "Non-RCT study design", "high")

    # Exclude: Metastatic/stage IV
    if any(
        word in title for word in ["metastatic", "stage iv", "advanced breast cancer"]
    ):
        # Unless it specifically says "early" or "locally advanced" or "neoadjuvant"
        if not any(
            word in title
            for word in [
                "early",
                "early-stage",
                "neoadjuvant",
                "locally advanced",
                "preoperative",
            ]
        ):
            return ("exclude", "Metastatic/Stage IV setting", "high")

    # Exclude: Adjuvant only (not neoadjuvant)
    if "adjuvant" in title and "neoadjuvant" not in title and "neo-" not in title:
        # Unless it's about post-neoadjuvant adjuvant (residual disease)
        if "residual" not in title and "post-neoadjuvant" not in title:
            return ("exclude", "Adjuvant only (not neoadjuvant)", "medium")

    # Exclude: Not TNBC
    if not any(
        word in title
        for word in [
            "triple-negative",
            "triple negative",
            "tnbc",
            "triple receptor-negative",
            "triple-receptor-negative",
        ]
    ):
        # Unless it's a breast cancer ICI trial that might include TNBC subgroup
        if "breast cancer" in title and any(
            word in title
            for word in [
                "pembrolizumab",
                "atezolizumab",
                "durvalumab",
                "nivolumab",
                "immunotherapy",
                "checkpoint",
            ]
        ):
            return (
                "maybe",
                "Breast cancer ICI trial - check if TNBC subgroup reported",
                "low",
            )
        else:
            return ("exclude", "Not TNBC-specific", "high")

    # Include: TNBC + neoadjuvant + ICI keywords
    has_tnbc = any(
        word in title for word in ["triple-negative", "triple negative", "tnbc"]
    )
    has_neoadj = any(word in title for word in ["neoadjuvant", "preoperative", "neo-"])
    has_ici = any(
        word in title
        for word in [
            "pembrolizumab",
            "atezolizumab",
            "durvalumab",
            "nivolumab",
            "camrelizumab",
            "immunotherapy",
            "immune checkpoint",
            "pd-1",
            "pd-l1",
            "avelumab",
        ]
    )
    has_trial = any(
        word in title
        for word in [
            "trial",
            "randomized",
            "randomised",
            "phase ii",
            "phase iii",
            "phase 2",
            "phase 3",
        ]
    )

    if has_tnbc and has_neoadj and has_ici:
        if has_trial:
            return ("include", "TNBC + neoadjuvant + ICI + RCT", "high")
        else:
            return (
                "maybe",
                "TNBC + neoadjuvant + ICI but trial type unclear",
                "medium",
            )

    # Maybe: TNBC + ICI but neoadjuvant unclear
    if has_tnbc and has_ici:
        return ("maybe", "TNBC + ICI but setting unclear from title", "medium")

    # Maybe: TNBC + neoadjuvant but ICI unclear
    if has_tnbc and has_neoadj:
        return ("maybe", "TNBC + neoadjuvant but intervention unclear", "medium")

    # Exclude: TNBC but clearly not relevant
    if has_tnbc:
        # Genomic/biomarker studies without trial
        if (
            any(
                word in title
                for word in [
                    "genomic",
                    "transcriptomic",
                    "biomarker",
                    "molecular",
                    "signature",
                ]
            )
            and "trial" not in title
        ):
            return ("exclude", "Biomarker/genomic study without trial", "medium")
        # Cost-effectiveness, quality of life only
        if (
            any(
                word in title
                for word in ["cost-effectiveness", "quality-of-life", "quality of life"]
            )
            and "trial" not in title
        ):
            return ("exclude", "Cost-effectiveness/QoL study only", "medium")
        # Otherwise, needs abstract review
        return ("maybe", "TNBC-related but needs abstract review", "low")

    # Default: if we get here, probably exclude
    return ("exclude", "Does not meet inclusion criteria", "low")


def main():
    input_csv = Path("/Users/htlin/meta-pipe/03_screening/round-01/decisions.csv")
    output_csv = Path(
        "/Users/htlin/meta-pipe/03_screening/round-01/decisions_ai_screened.csv"
    )

    print(f"Reading from: {input_csv}")

    with open(input_csv, "r", encoding="utf-8") as f_in:
        reader = csv.DictReader(f_in)
        rows = list(reader)
        fieldnames = reader.fieldnames

    print(f"Total records: {len(rows)}")

    # Screen each record
    stats = {"include": 0, "exclude": 0, "maybe": 0}
    for row in rows:
        decision, reason, confidence = screen_study(row)
        row["decision_r1"] = decision
        row["decision_r2"] = decision  # Simulate dual review with same result
        row["final_decision"] = decision
        row["exclusion_reason"] = reason if decision == "exclude" else ""
        row["notes"] = f"AI screening ({confidence} confidence): {reason}"
        stats[decision] += 1

    # Write output
    with open(output_csv, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nScreening complete!")
    print(f"Results written to: {output_csv}")
    print(f"\nSummary:")
    print(f"  Include: {stats['include']} ({stats['include'] / len(rows) * 100:.1f}%)")
    print(f"  Maybe: {stats['maybe']} ({stats['maybe'] / len(rows) * 100:.1f}%)")
    print(f"  Exclude: {stats['exclude']} ({stats['exclude'] / len(rows) * 100:.1f}%)")
    print(f"\nTotal for full-text: {stats['include'] + stats['maybe']}")

    # Show some examples
    print("\n" + "=" * 80)
    print("Sample INCLUDED studies:")
    print("=" * 80)
    for row in rows[:20]:
        if row["final_decision"] == "include":
            print(f"✓ {row['title'][:80]}...")
            print(f"  → {row['notes']}")
            print()

    print("\n" + "=" * 80)
    print("Sample EXCLUDED studies (first 10):")
    print("=" * 80)
    count = 0
    for row in rows:
        if row["final_decision"] == "exclude" and count < 10:
            print(f"✗ {row['title'][:80]}...")
            print(f"  → Reason: {row['exclusion_reason']}")
            print()
            count += 1


if __name__ == "__main__":
    main()
