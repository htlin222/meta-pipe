#!/usr/bin/env python3
"""
Keyword-based screening for cognitive effort scoping review.
Screens deduplicated BibTeX records against inclusion/exclusion criteria.
Assigns layer tags (L1-L5) based on keyword matching.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

# Add search scripts to path for bibtexparser
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ma-search-bibliography" / "scripts"))

INCLUSION_KEYWORDS = {
    "L1": [
        "cognitive effort", "mental effort", "effort cost", "effort aversion",
        "opportunity cost model", "effort paradox", "subjective effort",
        "effort allocation", "effort-based decision", "demand avoidance",
        "cognitive demand", "effort discounting",
    ],
    "L2": [
        "glutamate", "glycogen", "metabolic cost", "neuro-metabolic",
        "prefrontal fatigue", "cognitive fatigue neuroimaging",
        "cerebral metabol", "brain energy", "astrocyt", "neural cost",
        "lactate brain", "glucose brain cognit",
    ],
    "L3": [
        "expected value of control", "dorsal anterior cingulate", "dacc",
        "effort meter", "cognitive control cost", "anterior cingulate effort",
        "control demand", "evc model", "shenhav",
    ],
    "L4": [
        "interoceptive", "prediction error", "allostatic", "active inference",
        "free energy", "predictive processing", "interoception",
        "bodily prediction", "allostasis", "homeostatic",
    ],
    "L5": [
        "headache cognitiv", "headache mental", "tension-type headache",
        "pericranial tender", "head pain stress", "stress hyperalgesia",
        "cognitive stress headache", "mental fatigue headache",
        "head discomfort", "cephalic",
    ],
}

EXCLUSION_PATTERNS = [
    r"\banimal\b", r"\bmice\b", r"\brat\b", r"\brodent\b",
    r"\bpediatric\b", r"\bchild\b", r"\badolescent\b",
    r"\bpharmacol\b.*\btrial\b",
    r"\bcancer\b", r"\btumor\b", r"\boncol\b",
    r"\bdiabetes\b", r"\bcardiovasc\b",
    r"\bsurgical\b", r"\bpost-operative\b",
]

# Broader relevance terms (at least 2 must match for inclusion if no layer keyword hit)
RELEVANCE_TERMS = [
    "cognitive effort", "mental effort", "mental fatigue", "cognitive fatigue",
    "cognitive load", "sustained attention", "working memory",
    "effort", "fatigue", "discomfort", "aversive",
    "anterior cingulate", "prefrontal", "insula",
    "interocepti", "prediction error",
]


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def match_layer(title: str, abstract: str) -> list[str]:
    combined = normalize(f"{title} {abstract}")
    matched = []
    for layer, keywords in INCLUSION_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in combined:
                matched.append(layer)
                break
    return matched


def is_excluded(title: str, abstract: str) -> tuple[bool, str]:
    combined = normalize(f"{title} {abstract}")
    for pat in EXCLUSION_PATTERNS:
        if re.search(pat, combined):
            return True, f"Matched exclusion: {pat}"
    return False, ""


def relevance_score(title: str, abstract: str) -> int:
    combined = normalize(f"{title} {abstract}")
    return sum(1 for term in RELEVANCE_TERMS if term.lower() in combined)


def main():
    project = Path(__file__).resolve().parents[1]
    bib_path = project / "02_search" / "round-01" / "dedupe.bib"

    if not bib_path.exists():
        print(f"Missing: {bib_path}")
        sys.exit(1)

    from bibtexparser import loads
    bib = loads(bib_path.read_text())

    decisions = []
    included_entries = []

    for entry in bib.entries:
        record_id = entry.get("ID", "")
        title = entry.get("title", "")
        abstract = entry.get("abstract", "")
        year = entry.get("year", "")
        doi = entry.get("doi", "")
        pmid = entry.get("pmid", "")
        authors = entry.get("author", "")

        # Check exclusion
        excluded, reason = is_excluded(title, abstract)
        if excluded:
            decisions.append({
                "record_id": record_id, "title": title, "year": year,
                "doi": doi, "pmid": pmid,
                "decision": "exclude", "layer_tag": "",
                "exclusion_reason": reason, "relevance_score": 0,
            })
            continue

        # Check layer match
        layers = match_layer(title, abstract)
        rel_score = relevance_score(title, abstract)

        if layers:
            decision = "include"
            layer_tag = ";".join(sorted(set(layers)))
        elif rel_score >= 3:
            decision = "include"
            layer_tag = "multi"
        elif rel_score >= 2:
            decision = "maybe"
            layer_tag = "borderline"
        else:
            decision = "exclude"
            layer_tag = ""

        decisions.append({
            "record_id": record_id, "title": title, "year": year,
            "doi": doi, "pmid": pmid,
            "decision": decision, "layer_tag": layer_tag,
            "exclusion_reason": "" if decision != "exclude" else "low relevance",
            "relevance_score": rel_score,
        })

        if decision in ("include", "maybe"):
            included_entries.append(entry)

    # Write decisions CSV
    out_dir = project / "03_screening" / "round-01"
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / "decisions.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "record_id", "title", "year", "doi", "pmid",
            "decision", "layer_tag", "exclusion_reason", "relevance_score",
        ])
        writer.writeheader()
        writer.writerows(decisions)

    # Write included bib
    from bibtexparser.bwriter import BibTexWriter
    writer_bib = BibTexWriter()
    writer_bib.indent = "  "
    writer_bib.order_entries_by = None

    included_db = bib
    included_db.entries = included_entries
    (out_dir / "included.bib").write_text(writer_bib.write(included_db))

    # Write exclusions
    excluded_rows = [d for d in decisions if d["decision"] == "exclude"]
    exc_path = out_dir / "exclusions.csv"
    with exc_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "record_id", "title", "year", "doi", "exclusion_reason",
        ])
        writer.writeheader()
        for row in excluded_rows:
            writer.writerow({k: row[k] for k in ["record_id", "title", "year", "doi", "exclusion_reason"]})

    # Summary
    n_include = sum(1 for d in decisions if d["decision"] == "include")
    n_maybe = sum(1 for d in decisions if d["decision"] == "maybe")
    n_exclude = sum(1 for d in decisions if d["decision"] == "exclude")

    print(f"Screening complete:")
    print(f"  Total:    {len(decisions)}")
    print(f"  Include:  {n_include}")
    print(f"  Maybe:    {n_maybe}")
    print(f"  Exclude:  {n_exclude}")

    # Layer distribution
    layer_counts = {}
    for d in decisions:
        if d["decision"] in ("include", "maybe") and d["layer_tag"]:
            for tag in d["layer_tag"].split(";"):
                layer_counts[tag] = layer_counts.get(tag, 0) + 1
    print(f"\n  Layer distribution:")
    for layer in sorted(layer_counts):
        print(f"    {layer}: {layer_counts[layer]}")


if __name__ == "__main__":
    main()
