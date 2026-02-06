#!/usr/bin/env python3
"""Check Open Access status for 10 key trials."""

import csv
from pathlib import Path

KEY_TRIALS = [
    "postMONARCH",
    "MAINTAIN",
    "PALMIRA",
    "TROPiCS",
    "TROPION",
    "EMBER-3",
    "EMERALD",
    "CAPItello",
    "SOLAR-1",
    "BOLERO-2",
]


def main():
    csv_path = Path("../../04_fulltext/round-01/unpaywall_results.csv")

    print("🔍 Key Trial Open Access Status")
    print("=" * 80)

    found_trials = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            record_id = row.get("record_id", "")
            title = row.get("title", "")
            is_oa = row.get("is_oa", "")
            pdf_url = row.get("best_oa_pdf_url", "")
            oa_status = row.get("oa_status", "")

            # Check if any key trial name is in record_id or title
            for trial in KEY_TRIALS:
                if trial.upper() in record_id.upper() or trial.upper() in title.upper():
                    status = "✅ OA" if is_oa == "True" else "❌ Closed"
                    pdf_status = "✅ PDF" if pdf_url else "❌ No PDF"
                    found_trials.append(trial)
                    print(
                        f"{status} | {pdf_status} | {oa_status:10s} | {record_id[:30]:30s} | {title[:60]}"
                    )
                    break

    print()
    print(f"Found {len(found_trials)}/10 key trials in Unpaywall results")
    print(f"Missing trials: {set(KEY_TRIALS) - set(found_trials)}")


if __name__ == "__main__":
    main()
