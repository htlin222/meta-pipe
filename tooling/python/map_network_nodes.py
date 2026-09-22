#!/usr/bin/env python3
"""Stage 03b: map screened-in records to the N1-N10 nodes fixed at Stage 01.

This is a TRIAGE aid for the analysis-type gate, not an extraction step. It
matches agent names in title+abstract, which is enough to see the shape of the
network and to spot orphan nodes, but it is NOT arm-level data and nothing it
produces may reach the extraction database or the manuscript as a trial result.
Arm-level node assignment happens at Stage 05 from full texts.

Anything matching no node is reported as `N_other` for escalation per
eligibility.md 3, rather than being forced into a neighbouring node.

Usage:
    uv run tooling/python/map_network_nodes.py --project <name> [--round round-01]
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Agent vocabulary. Order matters only for reporting, not for assignment:
# a record may signal several nodes, which is expected for multi-arm trials.
TRASTUZUMAB = r"trastuzumab|herceptin|biosimilar trastuzumab"
PERTUZUMAB = r"pertuzumab|perjeta"
LAPATINIB = r"lapatinib|tykerb"
NERATINIB = r"neratinib"
TDM1 = r"t-dm1|trastuzumab emtansine|ado-trastuzumab|kadcyla"
TDXD = r"t-dxd|trastuzumab deruxtecan|ds-8201|enhertu"
ICI = r"atezolizumab|pembrolizumab|durvalumab|nivolumab|toripalimab|camrelizumab|sintilimab|tislelizumab|penpulimab"
CHEMO = (
    r"chemotherapy|docetaxel|paclitaxel|carboplatin|cisplatin|doxorubicin|epirubicin|"
    r"cyclophosphamide|anthracycline|taxane|nab-paclitaxel|capecitabine|ddac|\bac\b|\btch\b|\btchp\b"
)
CHEMO_FREE = r"chemotherapy-free|chemotherapy free|without chemotherapy|chemo-free|de-escalat"
OTHER_ANTIHER2 = (
    r"pyrotinib|tucatinib|margetuximab|inetetamab|zanidatamab|disitamab|rc48|"
    r"trastuzumab duocarmazine|syd985|shr-a1811|trastuzumab rezetecan|arx788|a166|"
    r"bat8001|mrg002|afatinib|poziotinib|zenocutuzumab|mcla-128"
)

NODE_LABELS = {
    "N1": "Chemotherapy alone",
    "N2": "Trastuzumab + chemotherapy (network reference)",
    "N3": "Trastuzumab + pertuzumab + chemotherapy",
    "N4": "Trastuzumab + lapatinib + chemotherapy",
    "N5": "Lapatinib + chemotherapy",
    "N6": "T-DM1 +/- pertuzumab (chemotherapy-free)",
    "N7": "Trastuzumab + pertuzumab (chemotherapy-free)",
    "N8": "T-DXd-based",
    "N9": "Neratinib + trastuzumab + chemotherapy",
    "N10": "Anti-HER2 backbone + immune checkpoint inhibitor",
    "N_other": "Regimen not mapping to N1-N10 (escalate per eligibility.md 3)",
}


def has(pattern: str, text: str) -> bool:
    return bool(re.search(pattern, text, re.I))


def nodes_for(text: str) -> set:
    t = text
    found = set()
    tra, per, lap = has(TRASTUZUMAB, t), has(PERTUZUMAB, t), has(LAPATINIB, t)
    ner, dm1, dxd = has(NERATINIB, t), has(TDM1, t), has(TDXD, t)
    ici, chemo = has(ICI, t), has(CHEMO, t)
    free = has(CHEMO_FREE, t)
    other = has(OTHER_ANTIHER2, t)

    if dxd:
        found.add("N8")
    if dm1:
        found.add("N6")
    if ner and tra:
        found.add("N9")
    if tra and per:
        found.add("N7" if free else "N3")
    if tra and lap:
        found.add("N4")
    if lap and not tra:
        found.add("N5")
    if tra and not per and not lap and not ner and chemo:
        found.add("N2")
    if ici and (tra or per or chemo):
        found.add("N10")
    if chemo and not (tra or per or lap or ner or dm1 or dxd or other):
        found.add("N1")
    if other and not found:
        found.add("N_other")
    return found


def _root() -> Path:
    env = os.environ.get("MA_PIPE_ROOT")
    r = Path(env).resolve() if env else Path(__file__).resolve().parent.parent.parent
    assert (r / "projects").is_dir()
    return r


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--project", required=True)
    ap.add_argument("--round", default="round-01")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    proj = _root() / "projects" / args.project
    dec = proj / "03_screening" / args.round / "decisions.csv"
    if not dec.exists():
        sys.exit(f"ERROR: {dec} not found")

    with open(dec, encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))

    advancing = [
        r for r in rows if (r.get("Final_Decision") or "").lower() in ("include", "unclear", "maybe")
    ]
    included = [r for r in rows if (r.get("Final_Decision") or "").lower() == "include"]

    node_counts = Counter()
    node_records = defaultdict(list)
    unmapped = []
    for r in included:
        text = f"{r.get('Title','')} {r.get('Abstract','')}"
        ns = nodes_for(text)
        if not ns:
            unmapped.append(r["RecordID"])
            continue
        for n in ns:
            node_counts[n] += 1
            node_records[n].append(r["RecordID"])

    multi = sum(1 for r in included if len(nodes_for(f"{r.get('Title','')} {r.get('Abstract','')}")) >= 2)

    print("=" * 62)
    print("STAGE 03b NODE TRIAGE (title/abstract signal, NOT arm-level data)")
    print("=" * 62)
    print(f"records screened        : {len(rows)}")
    print(f"advancing to full text  : {len(advancing)}")
    print(f"Final_Decision=include  : {len(included)}")
    print(f"  ...signalling >=2 nodes (multi-arm candidates): {multi}")
    print(f"  ...mapping to no node : {len(unmapped)}")
    print()
    print(f"{'node':8s} {'n':>5s}  label")
    for n in list(NODE_LABELS):
        print(f"{n:8s} {node_counts.get(n,0):>5d}  {NODE_LABELS[n]}")

    out = Path(args.out) if args.out else proj / "03_screening" / args.round / "node_triage.json"
    out.write_text(
        json.dumps(
            {
                "screened": len(rows),
                "advancing": len(advancing),
                "included": len(included),
                "multi_node_records": multi,
                "unmapped_record_ids": unmapped,
                "node_counts": dict(node_counts),
                "node_records": {k: v for k, v in node_records.items()},
                "caveat": (
                    "Title/abstract keyword triage for the Stage 03b gate only. "
                    "Not arm-level data; must not reach extraction or the manuscript."
                ),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
