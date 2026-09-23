#!/usr/bin/env python3
"""Merge Tier-1 registry arms and LLM-extracted arms into the extraction database.

Precedence is by provenance, not convenience. Where ClinicalTrials.gov posted
results exist for a trial, those arms win: they are sponsor-reported per-arm
data with numerator and denominator, whereas an abstract gives a percentage and
leaves the denominator to be found elsewhere.

pCR event counts are set by exactly one of three routes, and the route is always
recorded in `pcr_derivation` so Stage 06 can drop the derived rows and re-run:

    reported_count          the source states the count
    derived_from_pct_and_n  round(pct x N) where BOTH came from a source
    nct_arm_n               as above, with N taken from the trial registry
    unavailable             neither -- the cell stays blank

A percentage is never multiplied by a denominator borrowed from a different
population, and an arm N is never inferred from a trial total.

Usage:
    uv run tooling/python/consolidate_extraction.py --project <name>
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
import os
import re
import sqlite3
from pathlib import Path

COLS = [
    "trial_id",
    "record_id",
    "trial_name",
    "nctid",
    "year",
    "design",
    "phase",
    "country_region",
    "arm_label",
    "node",
    "chemo_backbone",
    "anthracycline",
    "cycles",
    "n_randomized",
    "n_evaluable",
    "pcr_events",
    "pcr_pct",
    "pcr_denominator",
    "pcr_definition",
    "pcr_derivation",
    "efs_hr",
    "efs_ci",
    "efs_comparison",
    "os_hr",
    "os_ci",
    "median_followup",
    "cardiac_n",
    "cardiac_term",
    "serious_ae_events",
    "serious_ae_atrisk",
    "grade3plus_ae_n",
    "discontinuation_ae_n",
    "hr_positive_pct",
    "node_positive_pct",
    "source",
    "source_tier",
    "extraction_notes",
]


def _root() -> Path:
    env = os.environ.get("MA_PIPE_ROOT")
    r = Path(env).resolve() if env else Path(__file__).resolve().parent.parent.parent
    assert (r / "projects").is_dir()
    return r


def num(v):
    try:
        return float(str(v).replace("%", "").strip())
    except (ValueError, AttributeError):
        return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project", required=True)
    args = ap.parse_args()

    proj = _root() / "projects" / args.project
    ex = proj / "05_extraction"

    ct = list(csv.DictReader(open(ex / "ctgov_arms.csv", encoding="utf-8")))

    # Tier-1 rows are keyed by NCT id, but the screening record they satisfy is
    # keyed by record_id. Leaving record_id blank breaks the chain back to
    # Stage 04 -- validate_stage_transition then reports those trials as
    # "included but never extracted" when in fact they were extracted from the
    # registry. Resolve the link where the manifest supplies it.
    # A trial usually has SEVERAL publications (primary report, 5-year update,
    # biomarker paper), so the map is many-to-one. Label the trial with a
    # report that survived full-text screening -- picking arbitrarily can
    # stamp the arms with a record that was excluded as a duplicate.
    ft_included: set[str] = set()
    ft_path = proj / "04_fulltext" / "fulltext_decisions.csv"
    if ft_path.exists():
        ft_included = {
            r["record_id"]
            for r in csv.DictReader(open(ft_path, encoding="utf-8"))
            if (r.get("FT_Final_Decision") or "").strip() == "include"
        }
    nct_candidates: dict[str, list[str]] = {}
    man_path = proj / "04_fulltext" / "manifest.csv"
    if man_path.exists():
        for r in csv.DictReader(open(man_path, encoding="utf-8")):
            for n in re.findall(r"NCT\d{8}", r.get("nctid", "") or ""):
                nct_candidates.setdefault(n, []).append(r.get("record_id", ""))
    nct_to_record = {
        n: next((c for c in sorted(cands) if c in ft_included), sorted(cands)[0])
        for n, cands in nct_candidates.items()
        if cands
    }
    llm = []
    for f in sorted(glob.glob(str(ex / "llm_shards" / "*.csv"))):
        llm += list(csv.DictReader(open(f, encoding="utf-8")))

    # registry arm N, for converting an abstract percentage into a count
    nct_arm_n: dict[str, list] = {}
    for r in ct:
        n = num(r.get("arm_n_enrolled")) or num(r.get("pcr_denom"))
        if r["nctid"] and n:
            nct_arm_n.setdefault(r["nctid"], []).append((r["arm_label"], int(n)))

    t1_ncts = {r["nctid"] for r in ct if r["source_tier"] == "tier1_ctgov_results"}
    rows = []

    # --- Tier 1 arms, authoritative ---
    for r in ct:
        if r["source_tier"] != "tier1_ctgov_results":
            continue
        rows.append(
            {c: "" for c in COLS}
            | {
                "trial_id": r["nctid"],
                "record_id": nct_to_record.get(r["nctid"], ""),
                "trial_name": r["trial_name"],
                "nctid": r["nctid"],
                "year": r["year"],
                "phase": r["phase"],
                "design": r["allocation"],
                "country_region": r["country_region"],
                "arm_label": r["arm_label"],
                "node": "",
                "n_randomized": r["arm_n_enrolled"],
                "pcr_events": r["pcr_events"],
                "pcr_pct": r["pcr_pct"],
                "pcr_denominator": r["pcr_denom"],
                "pcr_definition": r["pcr_definition"],
                "pcr_derivation": r["pcr_derivation"],
                "cardiac_n": r["cardiac_n"],
                "cardiac_term": r["cardiac_term"],
                "serious_ae_events": r["serious_ae_n"],
                "serious_ae_atrisk": r["serious_ae_N"],
                "source": r["source"],
                "source_tier": r["source_tier"],
                "extraction_notes": f"registry outcome: {r['pcr_outcome_title'][:80]}",
            }
        )

    # --- LLM arms; skip trials already covered by Tier 1 to avoid double-counting ---
    skipped = 0
    for r in llm:
        nct = (r.get("nctid") or "").split(";")[0]
        if nct and nct in t1_ncts:
            skipped += 1
            continue
        row = {c: "" for c in COLS}
        for c in COLS:
            if c in r:
                row[c] = r[c]
        row["trial_id"] = nct or r["record_id"]
        row["nctid"] = nct

        ev, pct = row.get("pcr_events", ""), num(row.get("pcr_pct"))
        n_arm = num(row.get("n_randomized")) or num(row.get("n_evaluable"))
        if ev.strip():
            row["pcr_derivation"] = "reported_count"
            row["pcr_denominator"] = str(int(n_arm)) if n_arm else ""
        elif pct is not None and n_arm:
            row["pcr_events"] = str(round(pct / 100.0 * n_arm))
            row["pcr_denominator"] = str(int(n_arm))
            row["pcr_derivation"] = "derived_from_pct_and_n"
        elif pct is not None and nct and len(nct_arm_n.get(nct, [])) == 1:
            # only when the registry leaves no ambiguity about which arm
            lbl, n = nct_arm_n[nct][0]
            row["pcr_events"] = str(round(pct / 100.0 * n))
            row["pcr_denominator"] = str(n)
            row["pcr_derivation"] = "nct_arm_n"
            row["extraction_notes"] = (
                row.get("extraction_notes", "")
                + f" | arm N from registry ({nct}, {lbl})"
            ).strip(" |")
        else:
            row["pcr_derivation"] = "unavailable"
        rows.append(row)

    out_csv = ex / "extraction.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)

    db = ex / "extraction.sqlite"
    if db.exists():
        db.unlink()
    con = sqlite3.connect(db)
    con.execute(f"CREATE TABLE arms ({','.join(f'{c} TEXT' for c in COLS)})")
    con.executemany(
        f"INSERT INTO arms VALUES ({','.join('?' * len(COLS))})",
        [[r[c] for c in COLS] for r in rows],
    )
    con.execute("CREATE INDEX idx_trial ON arms(trial_id)")
    con.execute("CREATE INDEX idx_node ON arms(node)")
    con.commit()
    con.close()

    import collections

    print(f"extraction.csv / extraction.sqlite: {len(rows)} arm rows")
    print(
        f"  Tier-1 registry arms kept        : {sum(1 for r in rows if r['source_tier'] == 'tier1_ctgov_results')}"
    )
    print(f"  LLM arms dropped as Tier-1 dupes : {skipped}")
    print(
        f"  distinct trials                  : {len({r['trial_id'] for r in rows if r['trial_id']})}"
    )
    print(
        "  pcr_derivation:",
        dict(collections.Counter(r["pcr_derivation"] for r in rows)),
    )
    print(
        "  source_tier   :", dict(collections.Counter(r["source_tier"] for r in rows))
    )


if __name__ == "__main__":
    main()
