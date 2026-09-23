#!/usr/bin/env python3
"""RoB 2 assessment for randomized trials, from retrieved full text only.

A risk-of-bias judgement needs the methods section. An abstract cannot support
one: it does not say how the sequence was generated, whether allocation was
concealed, how many patients were lost, or whether the analysis was
pre-specified. So trials whose full text was not retrieved are recorded as
`no_full_text` with every domain blank -- not as "low risk" and not as "some
concerns", because neither has been assessed.

Each domain gets its own written rationale. These trials share a bias profile
worth naming: they are overwhelmingly OPEN LABEL, and their primary endpoint is
pCR read by a pathologist. That combination is benign for D4 when pathology is
centrally reviewed and materially concerning when it is local and the assessor
knows the arm, so D4 must be judged per trial rather than boilerplated.

Usage:
    uv run tooling/python/assess_rob2.py --project <name> [--shard i/n]
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import subprocess
from pathlib import Path

COLS = [
    "record_id", "trial_name", "nctid", "outcome_assessed",
    "d1_randomization", "d1_rationale",
    "d2_deviations", "d2_rationale",
    "d3_missing_data", "d3_rationale",
    "d4_measurement", "d4_rationale",
    "d5_selective_reporting", "d5_rationale",
    "overall", "overall_rationale", "source", "source_tier",
]


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
    try:
        return str(json.loads(r.stdout.strip()).get("result") or r.stdout)
    except json.JSONDecodeError:
        return r.stdout


def xml_text(p: Path, limit: int = 40000) -> str:
    raw = p.read_text(encoding="utf-8", errors="replace")
    raw = re.sub(r"<(ref-list|back)\b.*?</\1>", " ", raw, flags=re.S | re.I)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw))[:limit]


PROMPT = """You are performing a Cochrane Risk of Bias 2 (RoB 2) assessment of a
randomized trial, for the outcome PATHOLOGICAL COMPLETE RESPONSE (pCR).

Judge ONLY from the source text below. If the source does not describe a domain,
judge "Some concerns" and say explicitly in the rationale that the information
was not reported -- do NOT assume good practice from a journal's reputation and
do NOT judge "Low" merely because nothing bad is mentioned.

Context that matters for these trials specifically: neoadjuvant anti-HER2 trials
are usually OPEN LABEL, and pCR is assessed by a pathologist. For D4, the
decisive question is whether pathology was assessed CENTRALLY/BLINDED or
LOCALLY by someone aware of allocation. Say which applies for THIS trial.

SOURCE TEXT:
{body}

Output ONLY a JSON object, no prose, no markdown fence:
{{"d1_randomization": "Low"|"Some concerns"|"High", "d1_rationale": "<= 40 words, specific to this trial",
 "d2_deviations": ..., "d2_rationale": ...,
 "d3_missing_data": ..., "d3_rationale": ...,
 "d4_measurement": ..., "d4_rationale": ...,
 "d5_selective_reporting": ..., "d5_rationale": ...,
 "overall": "Low"|"Some concerns"|"High", "overall_rationale": "<= 40 words"}}

RoB 2 overall rule: High if ANY domain is High; Low only if ALL domains are Low;
otherwise Some concerns.
"""


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project", required=True)
    ap.add_argument("--shard", default=None)
    args = ap.parse_args()

    proj = _root() / "projects" / args.project
    ft = {r["record_id"]: r for r in csv.DictReader(open(proj / "04_fulltext/fulltext_decisions.csv", encoding="utf-8"))}
    man = {r["record_id"]: r for r in csv.DictReader(open(proj / "04_fulltext/manifest.csv", encoding="utf-8"))}
    inc = sorted([r for r in ft.values() if r["FT_Final_Decision"] == "include"], key=lambda r: r["record_id"])

    out_dir = proj / "08_reviews" / "rob2_shards"
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.shard:
        i, n = (int(x) for x in args.shard.split("/"))
        inc = inc[i - 1::n]
        out_csv = out_dir / f"rob2.shard-{i:03d}-of-{n:03d}.csv"
    else:
        out_csv = proj / "08_reviews" / "rob2_assessment.csv"

    epmc = proj / "05_extraction/sources/epmc"
    rows = []
    for k, rec in enumerate(inc, 1):
        rid = rec["record_id"]
        m = man.get(rid, {})
        base = {c: "" for c in COLS} | {
            "record_id": rid, "trial_name": (rec.get("title") or "")[:90],
            "nctid": m.get("nctid", ""), "outcome_assessed": "pCR",
        }
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
            body, tier, src = "", "no_full_text", ""

        if not body.strip():
            base["source_tier"] = "no_full_text"
            base["overall"] = "not_assessable"
            base["overall_rationale"] = (
                "No full text retrieved. RoB 2 needs the methods section; an abstract "
                "cannot support a judgement, so no domain is rated."
            )
            rows.append(base)
            print(f"[{k}/{len(inc)}] {rid}: not assessable (no full text)")
            continue
        try:
            txt = claude(PROMPT.format(body=body))
            mm = re.search(r"\{.*\}", txt, re.S)
            d = json.loads(mm.group(0)) if mm else {}
        except Exception as e:
            base["source_tier"] = tier
            base["overall"] = "error"
            base["overall_rationale"] = f"assessment error: {e}"[:150]
            rows.append(base)
            print(f"[{k}/{len(inc)}] {rid}: ERROR")
            continue
        base.update({c: str(d.get(c, ""))[:400] for c in COLS if c in d})
        base["source"], base["source_tier"] = src, tier
        rows.append(base)
        print(f"[{k}/{len(inc)}] {rid}: overall={base.get('overall','')}")

    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {len(rows)} rows -> {out_csv}")


if __name__ == "__main__":
    main()
