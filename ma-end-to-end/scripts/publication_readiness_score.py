#!/usr/bin/env python3
"""
Publication Readiness Score Calculator
=======================================

Calculates an objective 0-100% readiness score for meta-analysis manuscripts.

Components:
- PRISMA checklist completion (20%)
- GRADE assessment quality (15%)
- Supplementary materials (15%)
- Author statements (10%)
- Claim audit (15%)
- Cross-reference validation (10%)
- Figure quality (10%)
- Reference completeness (5%)

Usage:
    uv run publication_readiness_score.py --root projects/ici-nsclc
    uv run publication_readiness_score.py --root projects/ici-nsclc --verbose
    uv run publication_readiness_score.py --root projects/ici-nsclc --out 09_qa/readiness_score.md

Author: AI-assisted meta-analysis pipeline
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional


def check_prisma_checklist(
    project_root: Path, analysis_type: str
) -> Tuple[int, int, List[str]]:
    """Check PRISMA checklist completion."""
    if analysis_type == "nma":
        checklist_path = project_root / "09_qa" / "prisma_nma_checklist.md"
        total_items = 32
    else:
        checklist_path = project_root / "09_qa" / "prisma_checklist.md"
        total_items = 27

    if not checklist_path.exists():
        return 0, total_items, [f"PRISMA checklist not found: {checklist_path}"]

    content = checklist_path.read_text()
    issues = []

    # Count completed items (lines with ✅ or checkmark)
    completed = len(re.findall(r"[✅✓]", content))

    # Count NA items (not applicable)
    na_count = len(re.findall(r"\bNA\b", content))

    # Count incomplete items (lines with ❌ or ⬜)
    incomplete = len(re.findall(r"[❌⬜]", content))

    if na_count > 5:
        issues.append(f"Too many NA items ({na_count}) - review applicability")

    if incomplete > 0:
        issues.append(f"{incomplete} PRISMA items incomplete")

    return completed, total_items, issues


def check_grade_assessment(project_root: Path) -> Tuple[int, int, List[str]]:
    """Check GRADE assessment quality."""
    grade_path = project_root / "08_reviews" / "grade_summary.csv"

    if not grade_path.exists():
        return 0, 15, ["GRADE assessment not found"]

    issues = []
    score = 15

    with open(grade_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return 0, 15, ["GRADE CSV is empty"]

    # Check for missing quality ratings
    missing_quality = sum(1 for row in rows if not row.get("quality_rating"))
    if missing_quality > 0:
        issues.append(f"{missing_quality} outcomes missing quality rating")
        score -= 5

    # Check for missing explanations
    missing_explanation = sum(1 for row in rows if not row.get("explanation"))
    if missing_explanation > 0:
        issues.append(f"{missing_explanation} outcomes missing downgrade explanation")
        score -= 3

    # Check for inappropriate ratings (e.g., HIGH for observational)
    for row in rows:
        if (
            row.get("study_design") == "observational"
            and row.get("quality_rating") == "HIGH"
        ):
            issues.append(f"Observational study rated HIGH (should start at LOW)")
            score -= 2
            break

    return max(0, score), 15, issues


def check_supplementary_materials(
    project_root: Path, analysis_type: str
) -> Tuple[int, int, List[str]]:
    """Check supplementary materials completeness."""
    supp_dir = project_root / "07_manuscript" / "supplementary"

    if not supp_dir.exists():
        return 0, 15, ["Supplementary materials directory not found"]

    issues = []
    score = 15

    # Standard tables/figures for all MA
    required_standard = [
        "table_s1_search_strategies",
        "table_s2_excluded_studies",
        "table_s3_study_characteristics",
        "table_s4_risk_of_bias",
        "figure_s1_rob_summary",
        "figure_s2_funnel_plot",
        "figure_s3_sensitivity",
    ]

    # Additional for NMA
    required_nma = [
        "table_s6_network_geometry",
        "table_s7_league_table",
        "table_s8_rankings",
        "figure_s4_network_graph",
        "figure_s5_rankograms",
    ]

    required = required_standard
    if analysis_type == "nma":
        required.extend(required_nma)

    missing = []
    for item in required:
        # Check for file with this prefix (any extension)
        matches = list(supp_dir.glob(f"{item}.*"))
        if not matches:
            missing.append(item)

    if missing:
        issues.append(
            f"Missing {len(missing)} supplementary items: {', '.join(missing[:3])}"
        )
        score -= min(len(missing) * 1, 10)

    return max(0, score), 15, issues


def check_author_statements(project_root: Path) -> Tuple[int, int, List[str]]:
    """Check author statements completeness."""
    statements_path = project_root / "07_manuscript" / "author_statements.md"

    if not statements_path.exists():
        return 0, 10, ["Author statements file not found"]

    content = statements_path.read_text()
    issues = []
    score = 10

    required_sections = [
        "Author Contributions",
        "Funding",
        "Conflicts of Interest",
        "Data Availability",
    ]

    for section in required_sections:
        if section not in content:
            issues.append(f"Missing section: {section}")
            score -= 2.5

    # Check for boilerplate text (not filled in)
    if "[TBD]" in content or "TODO" in content or "FILL" in content:
        issues.append("Contains placeholder text - needs completion")
        score -= 3

    return max(0, int(score)), 10, issues


def check_claim_audit(project_root: Path) -> Tuple[int, int, List[str]]:
    """Check claim audit results."""
    audit_path = project_root / "09_qa" / "claim_audit.md"

    if not audit_path.exists():
        return 0, 15, ["Claim audit not found - run claim_audit.py"]

    content = audit_path.read_text()
    issues = []
    score = 15

    # Check for flagged overclaims
    if "⚠️" in content or "WARNING" in content:
        overclaim_count = content.count("⚠️") + content.count("WARNING")
        issues.append(f"{overclaim_count} potential overclaims detected")
        score -= min(overclaim_count * 2, 10)

    # Check for evidence-claim mismatches
    if "MISMATCH" in content or "inconsistent" in content.lower():
        issues.append("Evidence-claim inconsistencies detected")
        score -= 5

    return max(0, score), 15, issues


def check_crossreference_validation(project_root: Path) -> Tuple[int, int, List[str]]:
    """Check cross-reference validation."""
    crossref_path = project_root / "09_qa" / "crossref_report.md"

    if not crossref_path.exists():
        return 0, 10, ["Cross-reference validation not found - run crossref_check.py"]

    content = crossref_path.read_text()
    issues = []
    score = 10

    # Check for orphaned figures
    if "orphaned" in content.lower():
        issues.append("Orphaned figures/tables detected")
        score -= 5

    # Check for missing citations
    if "missing" in content.lower() or "not found" in content.lower():
        issues.append("Missing figure/table citations")
        score -= 5

    return max(0, score), 10, issues


def png_dpi(path: Path) -> Optional[int]:
    """Resolution a PNG declares in its pHYs chunk, or None if it declares none.

    A PNG with no pHYs chunk is rendered at the viewer's default, conventionally
    72 dpi, however many pixels it contains. Journals that check resolution read
    this chunk, so "2400 pixels wide" is not the same as "300 dpi".
    """
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    offset = 8
    while offset + 8 <= len(data):
        length = int.from_bytes(data[offset : offset + 4], "big")
        chunk = data[offset + 4 : offset + 8]
        if chunk == b"pHYs" and offset + 17 <= len(data):
            px_per_unit = int.from_bytes(data[offset + 8 : offset + 12], "big")
            unit = data[offset + 16]
            if unit != 1:  # not metres; resolution is a ratio only
                return None
            return round(px_per_unit * 0.0254)
        if chunk == b"IDAT":
            return None  # pHYs must precede IDAT
        offset += 12 + length
    return None


def check_figure_quality(project_root: Path) -> Tuple[int, int, List[str]]:
    """Check figure quality (DPI, labels)."""
    figures_dir = project_root / "06_analysis" / "figures"

    if not figures_dir.exists():
        return 0, 10, ["Figures directory not found"]

    issues = []
    score = 10

    png_files = list(figures_dir.glob("*.png"))
    if not png_files:
        return 0, 10, ["No PNG figures found"]

    # Check for common naming patterns indicating panel labels
    multi_panel_files = [
        f
        for f in png_files
        if any(x in f.name.lower() for x in ["combined", "multi", "panel", "composite"])
    ]

    if multi_panel_files:
        # Assume multi-panel figures need labels (can't check DPI without image library)
        issues.append(
            f"{len(multi_panel_files)} multi-panel figures - verify A/B/C labels present"
        )
        score -= 2

    # Read the declared resolution instead of guessing from file size. File size
    # is not a DPI proxy and in practice points the wrong way: R's png(res=300)
    # writes no pHYs chunk at all (so the file declares 72 dpi) while producing a
    # LARGER file than ragg::agg_png, which does declare 300.
    undeclared = [f for f in png_files if png_dpi(f) is None]
    low_dpi = [f for f in png_files if (d := png_dpi(f)) is not None and d < 300]

    if undeclared:
        issues.append(
            f"{len(undeclared)} figures declare no resolution (no pHYs chunk) - "
            "re-render with ragg::agg_png(res=300), png(type='cairo', res=300) "
            "or ggsave(dpi=300)"
        )
        score -= 3
    if low_dpi:
        issues.append(
            f"{len(low_dpi)} figures below 300 DPI "
            f"(lowest {min(png_dpi(f) for f in low_dpi)})"
        )
        score -= 3

    return max(0, score), 10, issues


def check_reference_completeness(project_root: Path) -> Tuple[int, int, List[str]]:
    """Check reference completeness (DOI coverage)."""
    bib_path = project_root / "07_manuscript" / "references.bib"

    if not bib_path.exists():
        return 0, 5, ["References file not found"]

    content = bib_path.read_text()
    issues = []
    score = 5

    # Count entries
    entries = len(re.findall(r"@\w+\{", content))
    if entries == 0:
        return 0, 5, ["No references found in BibTeX"]

    # Count DOIs
    dois = len(re.findall(r"doi\s*=", content, re.IGNORECASE))
    coverage = dois / entries if entries > 0 else 0

    if coverage < 0.9:
        issues.append(f"DOI coverage {coverage * 100:.0f}% (target ≥90%)")
        score -= 3

    return max(0, score), 5, issues


def detect_analysis_type(project_root: Path) -> str:
    """Detect if project is NMA or pairwise."""
    pico_path = project_root / "01_protocol" / "pico.yaml"

    if pico_path.exists():
        content = pico_path.read_text()
        if "analysis_type: nma" in content:
            return "nma"

    # Fallback: check for NMA-specific files
    if (project_root / "06_analysis" / "nma_04_models.R").exists():
        return "nma"

    return "pairwise"


def calculate_readiness_score(project_root: Path, verbose: bool = False) -> Dict:
    """Calculate overall publication readiness score."""

    analysis_type = detect_analysis_type(project_root)

    results = {
        "analysis_type": analysis_type,
        "components": {},
        "total_score": 0,
        "total_possible": 100,
        "grade": "",
        "all_issues": [],
    }

    # Run all checks
    checks = [
        ("PRISMA checklist", check_prisma_checklist, [project_root, analysis_type]),
        ("GRADE assessment", check_grade_assessment, [project_root]),
        (
            "Supplementary materials",
            check_supplementary_materials,
            [project_root, analysis_type],
        ),
        ("Author statements", check_author_statements, [project_root]),
        ("Claim audit", check_claim_audit, [project_root]),
        ("Cross-reference validation", check_crossreference_validation, [project_root]),
        ("Figure quality", check_figure_quality, [project_root]),
        ("Reference completeness", check_reference_completeness, [project_root]),
    ]

    for name, check_func, args in checks:
        score, max_score, issues = check_func(*args)
        results["components"][name] = {
            "score": score,
            "max_score": max_score,
            "percentage": (score / max_score * 100) if max_score > 0 else 0,
            "issues": issues,
        }
        results["total_score"] += score
        results["all_issues"].extend(issues)

    # Assign grade
    percentage = (results["total_score"] / results["total_possible"]) * 100
    if percentage >= 95:
        results["grade"] = "Ready to Submit ✅"
    elif percentage >= 85:
        results["grade"] = "Almost Ready ⚠️"
    elif percentage >= 70:
        results["grade"] = "Needs Work 🔧"
    else:
        results["grade"] = "Major Gaps ❌"

    return results


def format_report(results: Dict, verbose: bool = False) -> str:
    """Format results as markdown report."""

    lines = [
        "# Publication Readiness Score",
        "",
        f"**Analysis Type**: {results['analysis_type'].upper()}",
        f"**Overall Score**: {results['total_score']}/{results['total_possible']} ({results['total_score'] / results['total_possible'] * 100:.0f}%)",
        f"**Grade**: {results['grade']}",
        "",
        "---",
        "",
        "## Component Scores",
        "",
    ]

    for component, data in results["components"].items():
        status = (
            "✅"
            if data["percentage"] >= 90
            else "⚠️"
            if data["percentage"] >= 70
            else "❌"
        )
        lines.append(
            f"### {status} {component}: {data['score']}/{data['max_score']} ({data['percentage']:.0f}%)"
        )

        if data["issues"]:
            lines.append("")
            lines.append("**Issues**:")
            for issue in data["issues"]:
                lines.append(f"- {issue}")
        lines.append("")

    # Priority actions
    lines.extend(["---", "", "## 🎯 Next Steps (Priority Order)", ""])

    # Sort components by percentage (lowest first)
    sorted_components = sorted(
        results["components"].items(), key=lambda x: x[1]["percentage"]
    )

    priority_count = 0
    for component, data in sorted_components:
        if data["percentage"] < 90 and data["issues"]:
            priority_count += 1
            lines.append(
                f"{priority_count}. **Fix {component}** ({data['percentage']:.0f}%)"
            )
            for issue in data["issues"][:2]:  # Top 2 issues
                lines.append(f"   - {issue}")
            lines.append("")

    if not priority_count:
        lines.append("✅ All components meet quality thresholds!")

    # Interpretation guide
    lines.extend(
        [
            "---",
            "",
            "## 📊 Interpretation",
            "",
            "- **≥95%**: Ready to submit to target journal",
            "- **85-94%**: Almost ready - address flagged issues (1-2 days)",
            "- **70-84%**: Needs work - systematic improvements needed (3-5 days)",
            "- **<70%**: Major gaps - review pipeline completion",
            "",
        ]
    )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Calculate publication readiness score (0-100%)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run publication_readiness_score.py --root projects/ici-nsclc
  uv run publication_readiness_score.py --root projects/ici-nsclc --verbose
  uv run publication_readiness_score.py --root projects/ici-nsclc --out 09_qa/readiness.md
        """,
    )

    parser.add_argument("--root", required=True, help="Project root directory")
    parser.add_argument("--out", help="Output markdown file (default: stdout)")
    parser.add_argument(
        "--verbose", action="store_true", help="Show detailed diagnostics"
    )
    parser.add_argument("--json", help="Also output JSON results to this file")

    args = parser.parse_args()

    project_root = Path(args.root)
    if not project_root.exists():
        print(f"Error: Project root not found: {project_root}", file=sys.stderr)
        sys.exit(1)

    # Calculate score
    results = calculate_readiness_score(project_root, args.verbose)

    # Format report
    report = format_report(results, args.verbose)

    # Output
    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report)
        print(f"✅ Readiness report written to: {out_path}")
    else:
        print(report)

    # JSON output
    if args.json:
        json_path = Path(args.json)
        json_path.parent.mkdir(parents=True, exist_ok=True)
        with open(json_path, "w") as f:
            json.dump(results, f, indent=2)
        print(f"✅ JSON results written to: {json_path}")

    # Exit code based on score
    percentage = (results["total_score"] / results["total_possible"]) * 100
    if percentage < 70:
        sys.exit(1)  # Major gaps


if __name__ == "__main__":
    main()
