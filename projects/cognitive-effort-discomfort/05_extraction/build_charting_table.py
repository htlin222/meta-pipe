#!/usr/bin/env python3
"""
Build scoping review charting table from included BibTeX entries.
Extracts metadata and classifies studies based on title/abstract content.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ma-search-bibliography" / "scripts"))


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().strip())


def detect_study_design(title: str, abstract: str) -> str:
    combined = normalize(f"{title} {abstract}")
    if any(t in combined for t in ["randomized", "randomised", "rct", "random assignment"]):
        return "RCT"
    if any(t in combined for t in ["within-subject", "within subject", "crossover", "repeated measures", "counterbalanced"]):
        return "within-subjects"
    if any(t in combined for t in ["between-subject", "between subject", "between-group"]):
        return "between-subjects"
    if any(t in combined for t in ["fmri", "neuroimaging", "eeg", "mrs", "pet scan", "bold"]):
        return "neuroimaging"
    if any(t in combined for t in ["review", "meta-analysis", "systematic", "narrative review"]):
        return "review"
    if any(t in combined for t in ["model", "framework", "theory", "computational model", "proposes", "we argue"]):
        return "theoretical"
    if any(t in combined for t in ["observational", "cohort", "cross-sectional", "survey"]):
        return "observational"
    if any(t in combined for t in ["experiment", "participants", "n =", "task"]):
        return "experimental"
    return "unclassified"


def detect_population(title: str, abstract: str) -> str:
    combined = normalize(f"{title} {abstract}")
    if any(t in combined for t in ["healthy", "non-clinical", "normal volunteers", "healthy adults", "healthy participants"]):
        return "healthy adults"
    if any(t in combined for t in ["tension-type headache", "tth", "migraine", "headache patients"]):
        return "TTH/headache patients"
    if any(t in combined for t in ["theory", "model", "framework", "review"]):
        return "N/A (theoretical)"
    if any(t in combined for t in ["participants", "volunteers", "subjects", "students"]):
        return "healthy adults"
    return "unspecified"


def detect_sample_size(abstract: str) -> str:
    combined = normalize(abstract)
    # Try to find N = XX or n = XX patterns
    patterns = [
        r"n\s*=\s*(\d+)", r"(\d+)\s*participants", r"(\d+)\s*subjects",
        r"(\d+)\s*volunteers", r"(\d+)\s*healthy\s*adults",
        r"sample\s*(?:of|size)\s*(\d+)",
    ]
    for pat in patterns:
        m = re.search(pat, combined)
        if m:
            n = int(m.group(1))
            if 5 <= n <= 10000:
                return str(n)
    return ""


def detect_task(title: str, abstract: str) -> str:
    combined = normalize(f"{title} {abstract}")
    tasks = []
    task_map = {
        "n-back": "N-back", "nback": "N-back", "2-back": "N-back", "3-back": "N-back",
        "stroop": "Stroop", "flanker": "Flanker", "go/no-go": "Go/No-Go",
        "working memory": "working memory", "cognitive control": "cognitive control",
        "simulated workday": "simulated workday", "sustained attention": "sustained attention",
        "continuous performance": "continuous performance",
        "attentional control": "attentional control",
        "task switching": "task switching", "decision making": "decision making",
        "effort-based decision": "effort-based decision",
    }
    for key, val in task_map.items():
        if key in combined:
            tasks.append(val)
    return "; ".join(tasks[:3]) if tasks else ""


def detect_outcome(title: str, abstract: str) -> str:
    combined = normalize(f"{title} {abstract}")
    outcomes = []
    outcome_map = {
        "effort discounting": "effort discounting", "indifference point": "effort discounting",
        "subjective effort": "subjective effort ratings", "vas": "VAS ratings",
        "fatigue rating": "fatigue ratings", "subjective fatigue": "fatigue ratings",
        "pupil": "pupillometry", "fmri": "fMRI", "bold": "fMRI",
        "mrs": "MRS", "spectroscopy": "MRS", "glutamate": "MRS glutamate",
        "eeg": "EEG", "erp": "ERP",
        "reaction time": "reaction time", "accuracy": "task performance",
        "headache": "headache ratings", "pericranial": "pericranial tenderness",
        "skin conductance": "autonomic measures", "heart rate": "autonomic measures",
    }
    for key, val in outcome_map.items():
        if key in combined and val not in outcomes:
            outcomes.append(val)
    return "; ".join(outcomes[:4]) if outcomes else ""


def detect_discomfort_type(title: str, abstract: str) -> str:
    combined = normalize(f"{title} {abstract}")
    types = []
    if any(t in combined for t in ["headache", "head pain", "cephalic", "pericranial"]):
        types.append("head-localized")
    if any(t in combined for t in ["fatigue", "tired", "exhaustion"]):
        types.append("general fatigue")
    if any(t in combined for t in ["somatic", "bodily", "physical"]):
        types.append("somatic")
    if any(t in combined for t in ["motivation", "effort avoidance", "demand avoidance"]):
        types.append("motivational")
    if any(t in combined for t in ["aversive", "discomfort", "unpleasant"]):
        types.append("aversive signal")
    return "; ".join(types[:2]) if types else "N/A"


def detect_framework(title: str, abstract: str) -> str:
    combined = normalize(f"{title} {abstract}")
    frameworks = []
    if any(t in combined for t in ["opportunity cost", "kurzban"]):
        frameworks.append("opportunity cost")
    if any(t in combined for t in ["expected value of control", "evc", "shenhav"]):
        frameworks.append("EVC")
    if any(t in combined for t in ["predictive processing", "prediction error", "active inference", "free energy"]):
        frameworks.append("predictive processing")
    if any(t in combined for t in ["metabolic", "glutamate", "glycogen", "energetic"]):
        frameworks.append("metabolic")
    if any(t in combined for t in ["peripheral", "pericranial", "nocicepti", "muscle"]):
        frameworks.append("peripheral")
    if any(t in combined for t in ["interocepti", "allostatic"]):
        frameworks.append("interoceptive")
    return "; ".join(frameworks) if frameworks else "unspecified"


def extract_key_finding(abstract: str) -> str:
    """Extract conclusion-like sentences from abstract."""
    if not abstract:
        return ""
    sentences = re.split(r'(?<=[.!?])\s+', abstract)
    # Look for conclusion markers
    for s in reversed(sentences):
        sl = s.lower()
        if any(t in sl for t in ["suggest", "conclude", "findings", "results", "demonstrate", "show that", "indicate"]):
            return s.strip()[:200]
    # Fall back to last sentence
    if sentences:
        return sentences[-1].strip()[:200]
    return ""


def main():
    project = Path(__file__).resolve().parents[1]
    bib_path = project / "03_screening" / "round-01" / "included.bib"
    decisions_path = project / "03_screening" / "round-01" / "decisions_final.csv"

    from bibtexparser import loads
    bib = loads(bib_path.read_text())

    # Load layer assignments from decisions
    layer_map = {}
    with decisions_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["decision"] == "include":
                layer_map[row["record_id"]] = row.get("layer_tag", "")

    charting_rows = []
    for entry in bib.entries:
        rid = entry.get("ID", "")
        title = entry.get("title", "")
        abstract = entry.get("abstract", "")
        year = entry.get("year", "")
        doi = entry.get("doi", "")
        pmid = entry.get("pmid", "")
        journal = entry.get("journal", "")
        authors = entry.get("author", "")

        # Shorten author list
        author_list = authors.split(" and ")
        if len(author_list) > 3:
            short_authors = f"{author_list[0]} et al."
        else:
            short_authors = "; ".join(author_list)

        charting_rows.append({
            "study_id": rid,
            "authors": short_authors,
            "year": year,
            "title": title,
            "doi": doi,
            "pmid": pmid,
            "journal": journal,
            "layer": layer_map.get(rid, ""),
            "study_design": detect_study_design(title, abstract),
            "population": detect_population(title, abstract),
            "sample_size": detect_sample_size(abstract),
            "cognitive_task": detect_task(title, abstract),
            "task_duration": "",  # Hard to extract automatically
            "outcome_measures": detect_outcome(title, abstract),
            "discomfort_type": detect_discomfort_type(title, abstract),
            "key_finding": extract_key_finding(abstract),
            "theoretical_framework": detect_framework(title, abstract),
            "limitations": "",  # Requires full-text review
        })

    # Write charting table
    out_path = project / "05_extraction" / "charting_table.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "study_id", "authors", "year", "title", "doi", "pmid", "journal",
            "layer", "study_design", "population", "sample_size",
            "cognitive_task", "task_duration", "outcome_measures",
            "discomfort_type", "key_finding", "theoretical_framework", "limitations",
        ])
        writer.writeheader()
        writer.writerows(charting_rows)

    # Summary
    designs = {}
    layers_dist = {}
    for row in charting_rows:
        d = row["study_design"]
        designs[d] = designs.get(d, 0) + 1
        for l in row["layer"].split(";"):
            l = l.strip()
            if l:
                layers_dist[l] = layers_dist.get(l, 0) + 1

    print(f"Charting table: {len(charting_rows)} studies → {out_path}")
    print(f"\nStudy design distribution:")
    for d, c in sorted(designs.items(), key=lambda x: -x[1]):
        print(f"  {d}: {c}")
    print(f"\nLayer distribution:")
    for l, c in sorted(layers_dist.items()):
        print(f"  {l}: {c}")


if __name__ == "__main__":
    main()
