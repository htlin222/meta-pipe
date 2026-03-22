#!/usr/bin/env python3
"""
Round 2 screening: tighter criteria to reduce included set to ~40-80 studies
for full charting. Focuses on studies that specifically address cognitive effort
and discomfort/fatigue, not just tangentially mention relevant terms.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ma-search-bibliography" / "scripts"))

# Must have at least one EFFORT term AND one OUTCOME term
EFFORT_TERMS = [
    "cognitive effort", "mental effort", "cognitive load", "cognitive demand",
    "cognitive control", "working memory", "n-back", "stroop", "sustained attention",
    "cognitive task", "mental task", "cognitive work", "mental workload",
    "executive function", "attentional control", "task demand",
    "effortful", "demanding task", "high demand",
]

OUTCOME_TERMS = [
    "fatigue", "discomfort", "aversive", "effort cost", "effort discounting",
    "subjective effort", "tiredness", "exhaustion", "depletion",
    "headache", "head pain", "somatic", "pericranial",
    "interocepti", "bodily", "allostatic",
    "glutamate", "metabolic", "glycogen", "dacc", "anterior cingulate",
    "anterior insula", "prediction error",
    "opportunity cost", "expected value of control",
]

# Core theoretical papers to always include (by author/year patterns)
SEED_PATTERNS = [
    "kurzban.*2013", "inzlicht.*2018", "shenhav.*2017", "shenhav.*2013",
    "wiehler.*2022", "christie.*schrater", "christie.*2015",
    "otto.*zijlstra", "otto.*2018", "yee.*shenhav", "yee.*2022",
    "friston.*2010", "seth.*friston", "seth.*2016",
    "cathcart.*2009", "cathcart.*2010",
    "pessiglione", "musslick",
]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def has_terms(text: str, terms: list[str]) -> list[str]:
    matched = []
    for t in terms:
        if t.lower() in text:
            matched.append(t)
    return matched


def is_seed(authors: str, year: str, title: str) -> bool:
    combined = normalize(f"{authors} {year} {title}")
    for pat in SEED_PATTERNS:
        if re.search(pat, combined):
            return True
    return False


def assign_layer(title: str, abstract: str) -> str:
    combined = normalize(f"{title} {abstract}")
    layers = []
    if any(t in combined for t in ["opportunity cost", "effort paradox", "effort valuation", "demand avoidance", "effort discounting"]):
        layers.append("L1")
    if any(t in combined for t in ["glutamate", "glycogen", "metabolic cost", "neuro-metabolic", "astrocyt", "brain energy"]):
        layers.append("L2")
    if any(t in combined for t in ["expected value of control", "evc", "dorsal anterior cingulate", "dacc", "effort meter"]):
        layers.append("L3")
    if any(t in combined for t in ["interocepti", "prediction error", "allostatic", "active inference", "free energy", "predictive processing"]):
        layers.append("L4")
    if any(t in combined for t in ["headache", "head pain", "pericranial", "tension-type", "stress hyperalgesia", "cephalic"]):
        layers.append("L5")
    if not layers:
        layers.append("general")
    return ";".join(layers)


def main():
    project = Path(__file__).resolve().parents[1]
    r1_decisions = project / "03_screening" / "round-01" / "decisions.csv"
    bib_path = project / "02_search" / "round-01" / "dedupe.bib"

    # Load round 1 included/maybe records
    r1_included = set()
    with r1_decisions.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["decision"] in ("include", "maybe"):
                r1_included.add(row["record_id"])

    from bibtexparser import loads
    bib = loads(bib_path.read_text())

    decisions = []
    included_entries = []

    for entry in bib.entries:
        rid = entry.get("ID", "")
        if rid not in r1_included:
            continue

        title = entry.get("title", "")
        abstract = entry.get("abstract", "")
        year = entry.get("year", "")
        doi = entry.get("doi", "")
        pmid = entry.get("pmid", "")
        authors = entry.get("author", "")

        combined = normalize(f"{title} {abstract}")

        # Always include seed papers
        if is_seed(authors, year, title):
            layer = assign_layer(title, abstract)
            decisions.append({
                "record_id": rid, "title": title, "year": year,
                "doi": doi, "pmid": pmid, "authors": authors[:80],
                "decision": "include", "layer_tag": layer,
                "reason": "seed paper",
            })
            included_entries.append(entry)
            continue

        # Must have effort AND outcome terms
        effort_hits = has_terms(combined, EFFORT_TERMS)
        outcome_hits = has_terms(combined, OUTCOME_TERMS)

        if effort_hits and outcome_hits:
            layer = assign_layer(title, abstract)
            decisions.append({
                "record_id": rid, "title": title, "year": year,
                "doi": doi, "pmid": pmid, "authors": authors[:80],
                "decision": "include", "layer_tag": layer,
                "reason": f"effort:{effort_hits[0]}; outcome:{outcome_hits[0]}",
            })
            included_entries.append(entry)
        elif len(outcome_hits) >= 3:
            # Highly relevant theoretical paper
            layer = assign_layer(title, abstract)
            decisions.append({
                "record_id": rid, "title": title, "year": year,
                "doi": doi, "pmid": pmid, "authors": authors[:80],
                "decision": "include", "layer_tag": layer,
                "reason": f"theory:{';'.join(outcome_hits[:3])}",
            })
            included_entries.append(entry)
        else:
            decisions.append({
                "record_id": rid, "title": title, "year": year,
                "doi": doi, "pmid": pmid, "authors": authors[:80],
                "decision": "exclude", "layer_tag": "",
                "reason": "insufficient effort+outcome overlap",
            })

    # Write final screening
    out_dir = project / "03_screening" / "round-01"
    final_csv = out_dir / "decisions_final.csv"
    with final_csv.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "record_id", "title", "year", "doi", "pmid", "authors",
            "decision", "layer_tag", "reason",
        ])
        writer.writeheader()
        writer.writerows(decisions)

    # Overwrite included.bib
    from bibtexparser.bwriter import BibTexWriter
    bib_writer = BibTexWriter()
    bib_writer.indent = "  "
    bib_writer.order_entries_by = None
    included_db = bib
    included_db.entries = included_entries
    (out_dir / "included.bib").write_text(bib_writer.write(included_db))

    n_include = sum(1 for d in decisions if d["decision"] == "include")
    n_exclude = sum(1 for d in decisions if d["decision"] == "exclude")

    print(f"Round 2 screening:")
    print(f"  Input (R1 included+maybe): {len(decisions)}")
    print(f"  Final include: {n_include}")
    print(f"  Exclude: {n_exclude}")

    layer_counts = {}
    for d in decisions:
        if d["decision"] == "include":
            for tag in d["layer_tag"].split(";"):
                layer_counts[tag] = layer_counts.get(tag, 0) + 1
    print(f"\n  Layer distribution:")
    for layer in sorted(layer_counts):
        print(f"    {layer}: {layer_counts[layer]}")


if __name__ == "__main__":
    main()
