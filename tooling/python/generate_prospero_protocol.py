#!/usr/bin/env python3
"""Generate a PROSPERO-format registration document from pico.yaml."""

from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

import yaml


def load_pico(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def build_prospero(pico: dict) -> str:
    meta = pico.get("meta", {})
    pop = pico.get("population", {})
    interv = pico.get("intervention", {})
    comp = pico.get("comparator", {})
    outcomes = pico.get("outcomes", {})
    design = pico.get("study_design", {})
    search = pico.get("search_strategy", {})
    rob = pico.get("risk_of_bias", {})
    synth = pico.get("data_synthesis", {})
    grade = pico.get("grade_assessment", {})
    reporting = pico.get("reporting", {})
    contact = pico.get("contact", {})
    timeline = pico.get("timeline", {})

    sections: list[str] = []

    # Header
    sections.append("# PROSPERO Registration Draft")
    sections.append("")
    sections.append(
        "This document is auto-generated from `pico.yaml` for submission "
        "to the International Prospective Register of Systematic Reviews "
        "(PROSPERO)."
    )
    sections.append("")
    sections.append("---")
    sections.append("")

    # 1. Review title
    sections.append("## 1. Review title")
    sections.append("")
    sections.append(meta.get("title", "TBD"))
    sections.append("")

    # 2. Original language title
    sections.append("## 2. Original language title")
    sections.append("")
    sections.append(meta.get("title", "TBD"))
    sections.append("")

    # 3. Anticipated or actual start date
    sections.append("## 3. Anticipated or actual start date")
    sections.append("")
    sections.append(meta.get("date_created", "TBD"))
    sections.append("")

    # 4. Anticipated completion date
    sections.append("## 4. Anticipated completion date")
    sections.append("")
    total = timeline.get("total_duration", "TBD")
    sections.append(f"Estimated duration: {total}")
    sections.append("")

    # 5. Stage of review at time of registration
    sections.append("## 5. Stage of review at time of registration")
    sections.append("")
    sections.append(
        "Preliminary searches: No\n"
        "Piloting of the study selection process: No\n"
        "Formal screening against eligibility criteria: No\n"
        "Data extraction: No\n"
        "Risk of bias assessment: No\n"
        "Data analysis: No"
    )
    sections.append("")

    # 6. Named contact
    sections.append("## 6. Named contact")
    sections.append("")
    sections.append(contact.get("lead_investigator", "TBD"))
    sections.append("")

    # 7. Named contact email
    sections.append("## 7. Named contact email")
    sections.append("")
    sections.append(contact.get("email", "TBD"))
    sections.append("")

    # 8. Named contact address
    sections.append("## 8. Named contact address")
    sections.append("")
    sections.append(contact.get("affiliation", "TBD"))
    sections.append("")

    # 9. Named contact affiliation
    sections.append("## 9. Named contact affiliation")
    sections.append("")
    sections.append(contact.get("affiliation", "TBD"))
    sections.append("")

    # 10. Review team members
    sections.append("## 10. Review team members and their affiliations")
    sections.append("")
    sections.append(f"- {contact.get('lead_investigator', 'TBD')}")
    sections.append("")

    # 11. Funding sources
    sections.append("## 11. Funding sources/sponsors")
    sections.append("")
    sections.append(pico.get("funding", "None"))
    sections.append("")

    # 12. Conflicts of interest
    sections.append("## 12. Conflicts of interest")
    sections.append("")
    sections.append(pico.get("conflicts_of_interest", "None declared"))
    sections.append("")

    # 13. Collaborators
    sections.append("## 13. Collaborators")
    sections.append("")
    sections.append("None")
    sections.append("")

    # 14. Review question
    sections.append("## 14. Review question")
    sections.append("")
    pop_desc = pop.get("description", "TBD")
    interv_desc = interv.get("description", "TBD")
    comp_desc = comp.get("description", "TBD")
    primary = outcomes.get("primary", [])
    primary_names = ", ".join(o.get("name", "") for o in primary) if primary else "TBD"
    sections.append(
        f"In {pop_desc.lower()}, what is the comparative efficacy and safety of "
        f"{interv_desc.lower()} vs {comp_desc.lower()}, measured by {primary_names}?"
    )
    sections.append("")

    # 15. Searches
    sections.append("## 15. Searches")
    sections.append("")
    dbs = search.get("databases", [])
    if dbs:
        for db in dbs:
            name = db.get("name", "")
            date_range = db.get("date_range", "")
            sections.append(f"- {name} ({date_range})")
    else:
        sections.append("TBD")
    lang = search.get("language", "English")
    sections.append(f"\nLanguage: {lang}")
    sections.append("")

    # 16. URL to search strategy
    sections.append("## 16. URL to search strategy")
    sections.append("")
    sections.append("Will be made available upon completion.")
    sections.append("")

    # 17. Condition or domain
    sections.append("## 17. Condition or domain being studied")
    sections.append("")
    sections.append(pop_desc)
    sections.append("")

    # 18. Population
    sections.append("## 18. Participants/population")
    sections.append("")
    sections.append("**Inclusion criteria:**")
    for c in pop.get("inclusion_criteria", []):
        sections.append(f"- {c}")
    sections.append("")
    sections.append("**Exclusion criteria:**")
    for c in pop.get("exclusion_criteria", []):
        sections.append(f"- {c}")
    sections.append("")

    # 19. Intervention
    sections.append("## 19. Intervention(s), exposure(s)")
    sections.append("")
    cats = interv.get("treatment_categories", {})
    for key, cat in cats.items():
        name = cat.get("name", key)
        desc = cat.get("description", "")
        agents = cat.get("agents", [])
        sections.append(f"**{name}**: {desc}")
        for a in agents:
            sections.append(f"  - {a}")
    sections.append("")

    # 20. Comparator
    sections.append("## 20. Comparator(s)/control")
    sections.append("")
    direct = comp.get("direct_comparisons", [])
    for d in direct:
        sections.append(f"- {d}")
    soc = comp.get("standard_of_care", [])
    if soc:
        sections.append("\n**Standard of care:**")
        for s in soc:
            sections.append(f"- {s}")
    sections.append("")

    # 21. Types of study
    sections.append("## 21. Types of study to be included")
    sections.append("")
    if isinstance(design, list):
        for e in design:
            sections.append(f"- {e}")
    else:
        eligible = design.get("eligible_designs", [])
        for e in eligible:
            sections.append(f"- {e}")
        sections.append("")
        sections.append("**Excluded study designs:**")
        for e in design.get("exclusion_criteria", []):
            sections.append(f"- {e}")
    sections.append("")

    # 22. Main outcome
    sections.append("## 22. Main outcome(s)")
    sections.append("")
    for o in outcomes.get("primary", []):
        name = o.get("name", "")
        defn = o.get("definition", "")
        measure = o.get("measure", "")
        sections.append(f"**{name}**")
        sections.append(f"- Definition: {defn}")
        sections.append(f"- Measure: {measure}")
    sections.append("")

    # 23. Additional outcomes
    sections.append("## 23. Additional outcome(s)")
    sections.append("")
    for o in outcomes.get("secondary", []):
        name = o.get("name", "")
        defn = o.get("definition", "")
        measure = o.get("measure", "")
        if name:
            sections.append(f"**{name}**")
            if defn:
                sections.append(f"- Definition: {defn}")
            if measure:
                sections.append(f"- Measure: {measure}")
    sections.append("")

    # 24. Data extraction
    sections.append("## 24. Data extraction (selection and coding)")
    sections.append("")
    sections.append(
        "Data will be extracted independently by two reviewers using a "
        "standardized extraction form. Discrepancies will be resolved by "
        "consensus or a third reviewer."
    )
    sections.append("")

    # 25. Risk of bias
    sections.append("## 25. Risk of bias (quality) assessment")
    sections.append("")
    rob_tool = rob.get("tool", "TBD")
    sections.append(f"**Tool:** {rob_tool}")
    sections.append("")
    sections.append("**Domains assessed:**")
    for d in rob.get("domains", []):
        sections.append(f"- {d}")
    sections.append("")
    levels = rob.get("assessment_levels", [])
    if levels:
        sections.append(f"**Judgment levels:** {', '.join(levels)}")
    sections.append("")
    reviewers = rob.get("reviewers", "")
    if reviewers:
        sections.append(f"**Review process:** {reviewers}")
    sections.append("")

    # 26. Strategy for data synthesis
    sections.append("## 26. Strategy for data synthesis")
    sections.append("")
    primary_analysis = synth.get("primary_analysis", "TBD")
    sections.append(f"**Primary analysis:** {primary_analysis}")
    stats = synth.get("statistical_methods", {})
    if stats:
        sections.append(f"- Approach: {stats.get('approach', 'TBD')}")
        sections.append(f"- Software: {stats.get('software', 'TBD')}")
        sections.append(f"- Ranking: {stats.get('ranking', 'TBD')}")
        sections.append(f"- Consistency: {stats.get('consistency', 'TBD')}")
    sections.append("")

    het = synth.get("heterogeneity", {})
    if het:
        sections.append("**Heterogeneity assessment:**")
        for m in het.get("measures", []):
            sections.append(f"- {m}")
    sections.append("")

    # 27. Analysis of subgroups
    sections.append("## 27. Analysis of subgroups or subsets")
    sections.append("")
    for sg in synth.get("subgroup_analyses", []):
        sections.append(f"- {sg}")
    sections.append("")

    # 28. Type and method of review
    sections.append("## 28. Type and method of review")
    sections.append("")
    sections.append(meta.get("study_type", "Systematic review and meta-analysis"))
    sections.append("")

    # 29. Language
    sections.append("## 29. Language")
    sections.append("")
    sections.append("English")
    sections.append("")

    # 30. Country
    sections.append("## 30. Country")
    sections.append("")
    sections.append("TBD")
    sections.append("")

    # 31. Other registration details
    sections.append("## 31. Other registration details")
    sections.append("")
    guidelines = reporting.get("guidelines", [])
    if guidelines:
        sections.append("**Reporting guidelines:**")
        for g in guidelines:
            sections.append(f"- {g}")
    sections.append("")

    # GRADE section
    if grade:
        sections.append("## 32. GRADE assessment")
        sections.append("")
        sections.append(f"**Tool:** {grade.get('tool', 'GRADE')}")
        sections.append("")
        sections.append("**Domains:**")
        for d in grade.get("domains", []):
            name = d.get("name", d) if isinstance(d, dict) else d
            direction = d.get("direction", "") if isinstance(d, dict) else ""
            if direction:
                sections.append(f"- {name} ({direction})")
            else:
                sections.append(f"- {name}")
        sections.append("")
        levels = grade.get("certainty_levels", [])
        if levels:
            sections.append(f"**Certainty levels:** {', '.join(levels)}")
        sections.append("")

    # Footer
    sections.append("---")
    sections.append("")
    sections.append(
        "*This document was auto-generated from `01_protocol/pico.yaml`. "
        "Review and edit before submitting to PROSPERO.*"
    )
    sections.append("")

    return "\n".join(sections)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a PROSPERO registration document from pico.yaml."
    )
    parser.add_argument(
        "--pico",
        required=True,
        help="Path to pico.yaml",
    )
    parser.add_argument(
        "--out",
        required=True,
        help="Output markdown path (e.g., 01_protocol/prospero_registration.md)",
    )
    args = parser.parse_args()

    pico_path = Path(args.pico)
    if not pico_path.exists():
        raise SystemExit(f"pico.yaml not found: {pico_path}")

    pico = load_pico(pico_path)
    doc = build_prospero(pico)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(doc)
    print(f"PROSPERO registration draft written to {out_path}")


if __name__ == "__main__":
    main()
