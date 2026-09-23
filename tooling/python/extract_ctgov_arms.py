#!/usr/bin/env python3
"""Extract arm-level trial data from ClinicalTrials.gov result records.

Tier 1 of the open-data ladder. The registry is sponsor-reported primary data,
not a secondary account of it, and for safety it is usually more complete than
the paper: the paper summarises, the registry tabulates every preferred term
with a numerator and denominator per arm.

Every value carries its provenance. Nothing is estimated:

* `pcr_events` is derived as round(pct x denom) ONLY when the registry supplies
  both the percentage and that outcome's own denominator. Validated against
  NeoSphere (NCT00545688), where 29.0/45.8/16.8/24.0 over 107/107/107/96
  reproduces the published 31/49/18/23 exactly.
* `serious_ae_n` comes from `eventGroups.seriousNumAffected`, which is a
  PATIENT-level "at least one serious AE" count. It is NOT "grade >=3", and the
  two are not interchangeable, so grade>=3 is left blank here rather than
  silently substituted.
* Cardiac events are reported per preferred term. The protocol
  (`outcomes.md` 3) forbids summing preferred terms into an "any" total,
  because one patient can contribute several terms. The largest single cardiac
  term is recorded together with the term name, as a documented lower bound.

Usage:
    uv run tooling/python/extract_ctgov_arms.py --project <name>
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
from pathlib import Path

PCR_TITLE = re.compile(r"pathologic(al)?\s+complete\s+response|(^|\W)pcr(\W|$)", re.I)
# Registries publish the overall pCR measure alongside many subgroup
# breakdowns ("pCR by Lymph Node Status", "... by Hormone Receptor Status").
# A subgroup row is not the trial's overall result, so any title qualified with
# "by <something>" is rejected outright rather than pattern-matched one case at
# a time -- an early version of this picker silently selected NeoSphere's
# lymph-node subgroup (21.5/39.3/11.2/17.7) instead of its overall
# 29.0/45.8/16.8/24.0.
PCR_EXCLUDE = re.compile(
    r"\bby\b|\bsubgroup\b|best\s+primary|event[- ]free|disease[- ]free|"
    r"overall\s+survival|biomarker|per\s+protocol",
    re.I,
)
CARDIAC = re.compile(
    r"ventricular\s+dysfunction|ejection\s+fraction|cardiac\s+failure|"
    r"cardiomyopathy|heart\s+failure|cardiac\s+disorder",
    re.I,
)
DEFN = [
    (re.compile(r"ypT0\s*/?\s*is\s*,?\s*ypN0|ypT0/is ypN0", re.I), "ypT0/is ypN0"),
    (re.compile(r"ypT0\s*,?\s*ypN0", re.I), "ypT0 ypN0"),
    (re.compile(r"in the breast|breast only|ypT0/is\b(?!.*ypN0)", re.I), "breast_only"),
]


def _root() -> Path:
    env = os.environ.get("MA_PIPE_ROOT")
    r = Path(env).resolve() if env else Path(__file__).resolve().parent.parent.parent
    assert (r / "projects").is_dir()
    return r


def pcr_definition(text: str) -> str:
    for rx, label in DEFN:
        if rx.search(text or ""):
            return label
    return "not_stated"


def pick_pcr(oms: list) -> dict | None:
    """The trial's own primary pCR measure, not a subgroup breakdown."""
    cands = [
        o
        for o in oms
        if PCR_TITLE.search(o.get("title", "") or "")
        and not PCR_EXCLUDE.search(o.get("title", "") or "")
    ]
    if not cands:
        return None
    cands.sort(key=lambda o: (o.get("type") != "PRIMARY", len(o.get("title", ""))))
    return cands[0]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project", required=True)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    proj = _root() / "projects" / args.project
    src = proj / "05_extraction" / "sources" / "ctgov"
    out = Path(args.out) if args.out else proj / "05_extraction" / "ctgov_arms.csv"

    COLS = [
        "nctid",
        "trial_name",
        "year",
        "phase",
        "country_region",
        "allocation",
        "arm_id",
        "arm_label",
        "arm_n_enrolled",
        "pcr_pct",
        "pcr_denom",
        "pcr_events",
        "pcr_derivation",
        "pcr_definition",
        "pcr_outcome_title",
        "serious_ae_n",
        "serious_ae_N",
        "cardiac_term",
        "cardiac_n",
        "cardiac_N",
        "grade3plus_ae_n",
        "grade3plus_ae_N",
        "source",
        "source_tier",
    ]
    rows = []
    for jf in sorted(src.glob("NCT*.json")):
        d = json.loads(jf.read_text())
        nct = jf.stem
        ps = d.get("protocolSection", {})
        rs = d.get("resultsSection")
        idm = ps.get("identificationModule", {})
        name = idm.get("acronym") or idm.get("briefTitle", "")[:60]
        year = (ps.get("statusModule", {}).get("startDateStruct", {}) or {}).get(
            "date", ""
        )[:4]
        design = ps.get("designModule", {})
        phase = ",".join(design.get("phases", []) or [])
        alloc = (design.get("designInfo", {}) or {}).get("allocation", "")
        locs = (ps.get("contactsLocationsModule", {}) or {}).get("locations", []) or []
        region = ";".join(
            sorted({l.get("country", "") for l in locs if l.get("country")})[:6]
        )

        if not rs:
            # Tier 2: protocol only -- arm definitions and enrolment, no outcomes
            for a in (ps.get("armsInterventionsModule", {}) or {}).get(
                "armGroups", []
            ) or []:
                rows.append(
                    {c: "" for c in COLS}
                    | {
                        "nctid": nct,
                        "trial_name": name,
                        "year": year,
                        "phase": phase,
                        "country_region": region,
                        "allocation": alloc,
                        "arm_id": a.get("label", "")[:40],
                        "arm_label": a.get("label", ""),
                        "source": f"https://clinicaltrials.gov/study/{nct} (protocol record)",
                        "source_tier": "tier2_ctgov_protocol",
                    }
                )
            continue

        # ---- Tier 1 ----
        flow = {
            g["id"]: g.get("title", "")
            for g in (rs.get("participantFlowModule", {}) or {}).get("groups", [])
        }
        enrolled = {}
        for per in (rs.get("participantFlowModule", {}) or {}).get("periods", [])[:1]:
            for ms in per.get("milestones", []):
                if (ms.get("type") or "").upper().startswith("START"):
                    for a in ms.get("achievements", []):
                        enrolled[a.get("groupId")] = a.get("numSubjects", "")

        om = pick_pcr(
            (rs.get("outcomeMeasuresModule", {}) or {}).get("outcomeMeasures", []) or []
        )
        pcr_by_group, denom_by_group, om_title, om_unit = {}, {}, "", ""
        if om:
            om_title = om.get("title", "")
            om_unit = (om.get("unitOfMeasure") or "").lower()
            for den in om.get("denoms", []) or []:
                for c in den.get("counts", []) or []:
                    denom_by_group[c.get("groupId")] = c.get("value", "")
            for cls in om.get("classes", []) or []:
                for cat in cls.get("categories", []) or []:
                    for m in cat.get("measurements", []) or []:
                        pcr_by_group.setdefault(m.get("groupId"), m.get("value", ""))
        om_groups = {g["id"]: g.get("title", "") for g in (om or {}).get("groups", [])}

        ae = rs.get("adverseEventsModule", {}) or {}
        eg = {g["id"]: g for g in ae.get("eventGroups", []) or []}
        # largest single cardiac preferred term per AE group (terms are NOT summed)
        card = {}
        for ev in (ae.get("seriousEvents", []) or []) + (
            ae.get("otherEvents", []) or []
        ):
            if not CARDIAC.search(ev.get("term", "") or ""):
                continue
            for st in ev.get("stats", []) or []:
                gid, n = st.get("groupId"), st.get("numAffected")
                if n is None:
                    continue
                cur = card.get(gid)
                if cur is None or int(n) > cur[1]:
                    card[gid] = (ev.get("term", ""), int(n), st.get("numAtRisk", ""))

        defn = pcr_definition(f"{om_title} {(om or {}).get('description', '')}")
        ids = list(om_groups) or list(eg) or list(flow)
        for i, gid in enumerate(ids):
            label = (
                om_groups.get(gid)
                or flow.get(gid)
                or (eg.get(gid, {}) or {}).get("title", "")
            )
            pct = pcr_by_group.get(gid, "")
            den = denom_by_group.get(gid, "")
            ev_n, deriv = "", "unavailable"
            if pct and den and "percentage" in om_unit:
                try:
                    ev_n = str(round(float(pct) / 100.0 * int(den)))
                    deriv = "derived_from_pct_and_n"
                except (ValueError, TypeError):
                    ev_n, deriv = "", "unavailable"
            elif pct and "participants" in om_unit and "percentage" not in om_unit:
                ev_n, deriv = pct, "reported_count"

            aeg = eg.get(list(eg)[i] if i < len(eg) else gid, {}) or {}
            cterm, cn, cN = card.get(list(eg)[i] if i < len(eg) else gid, ("", "", ""))
            rows.append(
                {c: "" for c in COLS}
                | {
                    "nctid": nct,
                    "trial_name": name,
                    "year": year,
                    "phase": phase,
                    "country_region": region,
                    "allocation": alloc,
                    "arm_id": gid,
                    "arm_label": label,
                    "arm_n_enrolled": enrolled.get(gid, "")
                    or aeg.get("seriousNumAtRisk", ""),
                    "pcr_pct": pct,
                    "pcr_denom": den,
                    "pcr_events": ev_n,
                    "pcr_derivation": deriv,
                    "pcr_definition": defn,
                    "pcr_outcome_title": om_title[:120],
                    "serious_ae_n": aeg.get("seriousNumAffected", ""),
                    "serious_ae_N": aeg.get("seriousNumAtRisk", ""),
                    "cardiac_term": cterm,
                    "cardiac_n": cn,
                    "cardiac_N": cN,
                    "grade3plus_ae_n": "",
                    "grade3plus_ae_N": "",
                    "source": f"https://clinicaltrials.gov/study/{nct}/results (outcome: {om_title[:60]})",
                    "source_tier": "tier1_ctgov_results",
                }
            )

    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)

    t1 = [r for r in rows if r["source_tier"] == "tier1_ctgov_results"]
    print(f"wrote {len(rows)} arm rows -> {out}")
    print(
        f"  tier1 (results) arms : {len(t1)} from {len({r['nctid'] for r in t1})} trials"
    )
    print(
        f"  tier2 (protocol) arms: {len(rows) - len(t1)} from {len({r['nctid'] for r in rows if r not in t1})} trials"
    )
    print(f"  arms with pCR events : {sum(1 for r in rows if r['pcr_events'])}")
    print(f"  arms with serious AE : {sum(1 for r in rows if r['serious_ae_n'] != '')}")
    print(f"  arms with cardiac    : {sum(1 for r in rows if r['cardiac_n'] != '')}")


if __name__ == "__main__":
    main()
