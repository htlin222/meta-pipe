#!/usr/bin/env python3
"""Arm-level extraction from the best available source per record.

Source preference, strongest provenance first:
    1. Europe PMC full-text XML   (tier3_epmc_fulltext)
    2. downloaded PDF             (tier3_pdf_fulltext)
    3. abstract                   (tier4_abstract)

The single rule this script exists to enforce: **a cell is copied from the
source or it is blank**. The model is instructed to answer `NR` for anything the
source does not state, and every numeric field carries a derivation label so a
Stage 06 sensitivity analysis can drop derived rows and see whether the result
moves. Percentages are never converted to counts here unless the arm N is also
present in the same source.

Usage:
    uv run tooling/python/extract_arms_llm.py --project <name> [--shard i/n]
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from pathlib import Path

COLS = [
    "record_id", "trial_name", "nctid", "year", "design", "country_region",
    "arm_label", "node", "chemo_backbone", "anthracycline", "cycles",
    "n_randomized", "n_evaluable",
    "pcr_events", "pcr_pct", "pcr_definition", "pcr_derivation",
    "efs_hr", "efs_ci", "efs_comparison", "os_hr", "os_ci", "median_followup",
    "cardiac_n", "grade3plus_ae_n", "discontinuation_ae_n",
    "hr_positive_pct", "node_positive_pct",
    "source", "source_tier", "extraction_notes",
]

NODES = """N1 chemotherapy alone (no anti-HER2)
N2 trastuzumab + chemotherapy
N3 trastuzumab + pertuzumab + chemotherapy
N4 trastuzumab + lapatinib + chemotherapy
N5 lapatinib + chemotherapy (no trastuzumab)
N6 T-DM1 +/- pertuzumab, chemotherapy-free
N7 trastuzumab + pertuzumab, chemotherapy-free
N8 T-DXd-based
N9 neratinib + trastuzumab + chemotherapy
N10 any anti-HER2 backbone + immune checkpoint inhibitor
N_other regimen matching none of the above"""


def _root() -> Path:
    env = os.environ.get("MA_PIPE_ROOT")
    r = Path(env).resolve() if env else Path(__file__).resolve().parent.parent.parent
    assert (r / "projects").is_dir()
    return r


def claude(prompt: str, timeout: int = 240) -> str:
    cmd = ["claude", "-p", "--output-format", "json", "--model", "haiku"]
    if os.environ.get("ANTHROPIC_API_KEY"):
        cmd.insert(2, "--bare")
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip()[:200])
    out = r.stdout.strip()
    try:
        env = json.loads(out)
        return str(env.get("result") or out)
    except json.JSONDecodeError:
        return out


def xml_text(p: Path, limit: int = 40000) -> str:
    raw = p.read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"<(ref-list|back|fn-group)\b.*?</\1>", " ", raw, flags=re.S | re.I)
    txt = re.sub(r"<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", txt)[:limit]


def build_prompt(rec: dict, body: str, tier: str) -> str:
    return f"""You are extracting arm-level data from a clinical trial report for a meta-analysis.

ABSOLUTE RULE: copy numbers from the SOURCE TEXT below. If the source does not
state a value, output "NR". Never estimate, infer from another trial, or recall
it from memory. A blank cell is correct; an invented cell is a serious error.

TREATMENT NODES:
{NODES}

SOURCE TYPE: {tier}
TITLE: {rec.get('title','')}
NCT: {rec.get('nctid','')}

SOURCE TEXT:
{body}

TASK: identify EVERY randomized arm and output one JSON object per arm.
Output ONLY a JSON array, no prose, no markdown fence.

Each object must have exactly these keys:
{{"arm_label": str, "node": one of N1..N10 or "N_other",
 "chemo_backbone": str or "NR", "anthracycline": "yes"/"no"/"NR", "cycles": str or "NR",
 "n_randomized": int or "NR", "n_evaluable": int or "NR",
 "pcr_events": int or "NR", "pcr_pct": float or "NR",
 "pcr_definition": "ypT0/is ypN0" | "ypT0 ypN0" | "breast_only" | "not_stated",
 "efs_hr": str or "NR", "efs_ci": str or "NR", "efs_comparison": str or "NR",
 "os_hr": str or "NR", "os_ci": str or "NR", "median_followup": str or "NR",
 "cardiac_n": int or "NR", "grade3plus_ae_n": int or "NR",
 "discontinuation_ae_n": int or "NR",
 "hr_positive_pct": float or "NR", "node_positive_pct": float or "NR",
 "source_locator": str}}

RULES:
- pcr_events: give the COUNT only if the source states a count. If the source
  gives only a percentage, put the percentage in pcr_pct and "NR" in pcr_events.
  Do NOT multiply it out yourself.
- grade3plus_ae_n must be the number of PATIENTS with at least one grade >=3
  event. Do NOT sum individual adverse-event terms - one patient can have
  several. If only per-term counts exist, answer "NR".
- cardiac_n: patients with symptomatic cardiac dysfunction or a protocol-defined
  LVEF decline. If only asymptomatic LVEF data exist, still report it and say so
  in source_locator.
- source_locator: where in the source each arm's numbers came from, e.g.
  "Table 2" / "Results, para 3" / "abstract".
- If the source is an abstract and does not break results down by arm, output
  one object per arm with "NR" for the values you cannot attribute to a specific
  arm. Do NOT assign an unattributed number to an arm.
"""


def parse(text: str) -> list:
    m = re.search(r"\[.*\]", text, re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
        return data if isinstance(data, list) else []
    except json.JSONDecodeError:
        return []


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project", required=True)
    ap.add_argument("--shard", default=None)
    args = ap.parse_args()

    proj = _root() / "projects" / args.project
    ft = {r["record_id"]: r for r in csv.DictReader(open(proj / "04_fulltext/fulltext_decisions.csv", encoding="utf-8"))}
    man = {r["record_id"]: r for r in csv.DictReader(open(proj / "04_fulltext/manifest.csv", encoding="utf-8"))}
    sdb = {r["RecordID"]: r for r in csv.DictReader(open(proj / "03_screening/screening-database.csv", encoding="utf-8"))}
    inc = [r for r in ft.values() if r["FT_Final_Decision"] == "include"]
    inc.sort(key=lambda r: r["record_id"])

    out_dir = proj / "05_extraction" / "llm_shards"
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.shard:
        i, n = (int(x) for x in args.shard.split("/"))
        inc = inc[i - 1::n]
        out_csv = out_dir / f"arms.shard-{i:03d}-of-{n:03d}.csv"
    else:
        out_csv = proj / "05_extraction" / "arms_llm.csv"

    epmc = proj / "05_extraction/sources/epmc"
    rows = []
    for k, rec in enumerate(inc, 1):
        rid = rec["record_id"]
        m = man.get(rid, {})
        s = sdb.get(rid, {})
        xmlf = epmc / f"{rid}.xml"
        pdff = proj / "04_fulltext" / (m.get("file_path") or "")
        if xmlf.exists():
            body, tier, src = xml_text(xmlf), "tier3_epmc_fulltext", f"EuropePMC fullTextXML {rid}"
        elif m.get("file_path") and pdff.exists():
            try:
                from extract_pdf_text import extract_text_from_pdf
                body = (extract_text_from_pdf(pdff, max_pages=14) or {}).get("text", "")[:40000]
            except Exception:
                body = ""
            tier, src = "tier3_pdf_fulltext", str(pdff.relative_to(proj))
        else:
            body, tier, src = (s.get("Abstract") or "")[:8000], "tier4_abstract", f"abstract ({m.get('source','')})"

        base = {c: "" for c in COLS} | {
            "record_id": rid, "trial_name": (rec.get("title") or "")[:90],
            "nctid": m.get("nctid", ""), "year": m.get("year", ""),
            "country_region": "", "source": src, "source_tier": tier,
        }
        if not body.strip():
            base["extraction_notes"] = "no source text available"
            rows.append(base)
            print(f"[{k}/{len(inc)}] {rid}: NO SOURCE")
            continue
        try:
            arms = parse(claude(build_prompt({**base, "title": rec.get("title", "")}, body, tier)))
        except Exception as e:
            base["extraction_notes"] = f"extraction error: {e}"
            rows.append(base)
            print(f"[{k}/{len(inc)}] {rid}: ERROR {e}")
            continue
        if not arms:
            base["extraction_notes"] = "model returned no parsable arms"
            rows.append(base)
            print(f"[{k}/{len(inc)}] {rid}: no arms parsed")
            continue
        for a in arms:
            r = dict(base)
            for c in COLS:
                v = a.get(c)
                if v is not None and str(v).strip().upper() != "NR":
                    r[c] = str(v).strip()
            r["pcr_derivation"] = (
                "reported_count" if r["pcr_events"] else
                ("pct_only_no_count" if r["pcr_pct"] else "unavailable")
            )
            r["extraction_notes"] = str(a.get("source_locator", ""))[:120]
            rows.append(r)
        print(f"[{k}/{len(inc)}] {rid}: {len(arms)} arms ({tier})")

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {len(rows)} rows -> {out_csv}")


if __name__ == "__main__":
    main()
