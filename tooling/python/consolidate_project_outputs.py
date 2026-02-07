#!/usr/bin/env python3
"""
Consolidate all project outputs into organized directory structure.

This script copies all project-related files into a centralized location
organized by type for easy review and archival.

Usage:
    uv run consolidate_project_outputs.py --project-name ici-breast-cancer
"""

import argparse
import shutil
from pathlib import Path
from datetime import datetime


def consolidate_outputs(root_dir: Path, project_name: str, output_dir: Path = None):
    """
    Consolidate all project outputs into organized directory structure.

    Args:
        root_dir: Root directory of the meta-analysis project
        project_name: Name of the project (e.g., 'ici-breast-cancer')
        output_dir: Optional output directory (defaults to projects/{project_name})
    """

    # Default output directory
    if output_dir is None:
        output_dir = root_dir / "projects" / project_name

    # Create output directory structure
    structure = {
        "00_overview": "Project overview and summary reports",
        "01_protocol": "Study protocol and registration",
        "02_search": "Literature search results",
        "03_screening": "Title/abstract screening",
        "04_fulltext": "Full-text retrieval",
        "05_extraction": "Data extraction",
        "06_analysis": "Statistical analysis and results",
        "07_manuscript": "Manuscript drafts and tables",
        "08_documentation": "Project documentation and guides",
        "09_scripts": "Analysis and utility scripts",
    }

    print(f"📦 Consolidating project outputs to: {output_dir}")
    print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Create all directories
    for dir_name, description in structure.items():
        dir_path = output_dir / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)

        # Create README in each directory
        readme = dir_path / "README.md"
        readme.write_text(f"# {dir_name.split('_', 1)[1].title()}\n\n{description}\n")

    # Define file mappings
    file_mappings = {
        # Overview files
        "00_overview": [
            "FINAL_PROJECT_SUMMARY.md",
            "PROJECT_STATUS_FINAL.md",
            "CURRENT_STATUS.md",
            "FEASIBILITY_REPORT.md",
            "PARALLEL_WORK_SUMMARY.md",
            "SKILLS_GENERALIZATION_REPORT.md",
            "CLAUDE_MD_UPDATE_SUMMARY.md",
            "PROGRESS_TRACKING_SUMMARY.md",
            "feasibility_abstracts.json",
            "feasibility_hour1_analysis.md",
            "feasibility_hour2_pilot_extraction.md",
            "feasibility_hour3_scoring.md",
        ],

        # Protocol files
        "01_protocol": [
            "01_protocol/pico.yaml",
            "01_protocol/eligibility.md",
            "01_protocol/search_strategy.md",
            "01_protocol/prospero_registration.md",
            "TOPIC.txt",
        ],

        # Search files
        "02_search": [
            "02_search/SEARCH_COMPLETION_REPORT.md",
            "02_search/round-01/dedupe.bib",
            "02_search/round-01/pubmed.bib",
            "02_search/round-01/pubmed_log.md",
        ],

        # Screening files
        "03_screening": [
            "03_screening/AI_SCREENING_REPORT.md",
            "03_screening/SCREENING_COMPLETE.md",
            "03_screening/SCREENING_QUICKSTART.md",
            "03_screening/round-01/decisions.csv",
            "03_screening/round-01/decisions_ai_screened.csv",
            "03_screening/round-01/decisions_screened.csv",
        ],

        # Fulltext files
        "04_fulltext": [
            "04_fulltext/PHASE4_QUICKSTART.md",
            "04_fulltext/PHASE4_SUMMARY.md",
            "04_fulltext/round-01/fulltext_subset.bib",
            "04_fulltext/round-01/include_list.txt",
        ],

        # Extraction files
        "05_extraction": [
            "05_extraction/data-dictionary.md",
            "05_extraction/round-01/EXTRACTION_SUMMARY.md",
            "05_extraction/round-01/QUICK_STATS.md",
            "05_extraction/round-01/extraction.csv",
            "05_extraction/round-01/safety_data.csv",
        ],

        # Analysis files
        "06_analysis": [
            "06_analysis/META_ANALYSIS_SUMMARY.md",
            "06_analysis/ANALYSIS_PROGRESS_SUMMARY.md",
            "06_analysis/PDL1_SUBGROUP_REPORT.md",
            "06_analysis/EFS_META_ANALYSIS_REPORT.md",
            "06_analysis/OS_META_ANALYSIS_REPORT.md",
            "06_analysis/SAFETY_META_ANALYSIS_REPORT.md",
            "06_analysis/01_pCR_meta_analysis.R",
            "06_analysis/02_PDL1_subgroup_analysis.R",
            "06_analysis/03_EFS_meta_analysis.R",
            "06_analysis/04_OS_meta_analysis.R",
            "06_analysis/05_safety_meta_analysis.R",
            "06_analysis/tables/pCR_meta_analysis_results.csv",
            "06_analysis/tables/PDL1_subgroup_comparison.csv",
            "06_analysis/tables/EFS_meta_analysis_results.csv",
            "06_analysis/tables/OS_meta_analysis_results.csv",
            "06_analysis/tables/safety_meta_analysis_summary.csv",
        ],

        # Manuscript files
        "07_manuscript": [
            "07_manuscript/00_abstract.md",
            "07_manuscript/01_introduction.md",
            "07_manuscript/02_methods.md",
            "07_manuscript/03_results.md",
            "07_manuscript/04_discussion.md",
            "07_manuscript/references.bib",
            "07_manuscript/COMPLETION_SUMMARY.md",
            "07_manuscript/CITATION_MAPPING.md",
            "07_manuscript/REFERENCES_USAGE_GUIDE.md",
            "07_manuscript/REFERENCES_COMPLETION_SUMMARY.md",
            "07_manuscript/FIGURE_LEGENDS.md",
            "07_manuscript/FIGURES_ASSEMBLY_SUMMARY.md",
            "07_manuscript/TABLES_FIGURES_PLAN.md",
            "07_manuscript/TABLES_FIGURES_STATUS.md",
            "07_manuscript/tables/Table1_Trial_Characteristics.md",
            "07_manuscript/tables/Table2_Efficacy_Summary.md",
            "07_manuscript/tables/Table3_Safety_Summary.md",
            "07_manuscript/tables/SupplementaryTable1_RiskOfBias.md",
            "07_manuscript/tables/SupplementaryTable2_PDL1_Subgroup.md",
            "07_manuscript/tables/SupplementaryTable3_Individual_pCR_Results.md",
            "07_manuscript/tables/SupplementaryTable4_GRADE_Profile.md",
        ],

        # Documentation files
        "08_documentation": [
            "CLAUDE.md",
            "CLAUDE_MD_ADDITIONS.md",
            "GETTING_STARTED.md",
            "FEASIBILITY_CHECKLIST.md",
            "docs/MANUSCRIPT_ASSEMBLY.md",
            "docs/TIME_GUIDANCE.md",
            "docs/JOURNAL_FORMATTING.md",
            "docs/SKILL_GENERALIZATION.md",
            "docs/API_SETUP.md",
            "docs/RAYYAN_SETUP.md",
            "docs/ZOTERO_SETUP.md",
        ],

        # Scripts
        "09_scripts": [
            "tooling/python/ai_screen_titles.py",
            "tooling/python/assemble_figures.py",
        ],
    }

    # Copy files
    total_copied = 0
    total_missing = 0

    for target_dir, file_list in file_mappings.items():
        target_path = output_dir / target_dir
        print(f"📂 {target_dir}")

        copied_count = 0
        for rel_path in file_list:
            source = root_dir / rel_path

            if source.exists():
                # Preserve directory structure for nested files
                if "/" in rel_path:
                    # Extract filename and parent directory
                    parts = Path(rel_path).parts
                    if len(parts) > 2:
                        # Keep one level of parent directory
                        dest_name = f"{parts[-2]}_{parts[-1]}"
                    else:
                        dest_name = parts[-1]
                else:
                    dest_name = source.name

                dest = target_path / dest_name

                try:
                    shutil.copy2(source, dest)
                    copied_count += 1
                    total_copied += 1
                    print(f"  ✅ {rel_path} → {dest_name}")
                except Exception as e:
                    print(f"  ❌ Failed to copy {rel_path}: {e}")
            else:
                print(f"  ⚠️  Missing: {rel_path}")
                total_missing += 1

        if copied_count == 0:
            print(f"  ℹ️  No files copied to this directory")
        print()

    # Create project index
    create_project_index(output_dir, project_name, total_copied, total_missing)

    # Summary
    print("=" * 70)
    print(f"✅ Consolidation complete!")
    print(f"📊 Total files copied: {total_copied}")
    print(f"⚠️  Missing files: {total_missing}")
    print(f"📁 Output directory: {output_dir}")
    print(f"📄 See INDEX.md for complete file listing")
    print("=" * 70)


def create_project_index(output_dir: Path, project_name: str, total_copied: int, total_missing: int):
    """Create an index file listing all consolidated outputs."""

    index_path = output_dir / "INDEX.md"

    content = f"""# {project_name.upper()} Project Outputs

**Consolidated Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Files**: {total_copied} copied, {total_missing} missing

---

## 📊 Project Overview

This directory contains all outputs from the {project_name} meta-analysis project,
organized by pipeline stage for easy review and archival.

### Directory Structure

```
projects/{project_name}/
├── 00_overview/          # Project summaries and feasibility reports
├── 01_protocol/          # PICO, eligibility, search strategy
├── 02_search/            # Literature search results (122 records)
├── 03_screening/         # Title/abstract screening (5 RCTs)
├── 04_fulltext/          # Full-text retrieval
├── 05_extraction/        # Data extraction (N=2402 patients)
├── 06_analysis/          # Meta-analysis results and R scripts
├── 07_manuscript/        # Manuscript sections and tables (4,921 words)
├── 08_documentation/     # Project guides and workflows
└── 09_scripts/           # Python utility scripts
```

---

## 🎯 Key Findings (Quick Reference)

### Efficacy Results

| Outcome | Effect | 95% CI | p-value | Quality |
|---------|--------|--------|---------|---------|
| pCR | RR 1.26 | 1.16-1.37 | 0.0015 | ⊕⊕⊕⊕ HIGH |
| EFS | HR 0.66 | 0.51-0.86 | 0.021 | ⊕⊕⊕◯ MODERATE |
| OS | HR 0.48 | (k=2) | 0.346 | ⊕⊕◯◯ LOW |

### Study Characteristics

- **Trials included**: 5 RCTs
- **Total patients**: N=2402
- **Intervention**: ICI + chemotherapy vs chemotherapy alone
- **Population**: Triple-negative breast cancer (TNBC), neoadjuvant setting

---

## 📁 File Listings by Directory

"""

    # List files in each directory
    for subdir in sorted(output_dir.iterdir()):
        if subdir.is_dir() and not subdir.name.startswith('.'):
            content += f"\n### {subdir.name}\n\n"

            files = sorted([f for f in subdir.iterdir() if f.is_file() and f.name != "README.md"])

            if files:
                for file in files:
                    size = file.stat().st_size / 1024  # KB
                    content += f"- `{file.name}` ({size:.1f} KB)\n"
            else:
                content += "*No files in this directory*\n"

    content += f"""
---

## 📖 Recommended Reading Order

For new reviewers or collaborators:

1. **Start here**: `00_overview/FINAL_PROJECT_SUMMARY.md` (415 lines, comprehensive)
2. **Protocol**: `01_protocol/pico.yaml` and `01_protocol/eligibility.md`
3. **Key findings**: `06_analysis/META_ANALYSIS_SUMMARY.md`
4. **Manuscript**: `07_manuscript/00_abstract.md` → `07_manuscript/04_discussion.md`

---

## 🔗 Related Resources

- **Main repository**: `/Users/htlin/meta-pipe/`
- **Git branch**: `projects/ici-breast-cancer`
- **Skills created**: `~/.claude/skills/meta-manuscript-assembly/`
- **Documentation**: `docs/` (modular guides with progressive disclosure)

---

## 📊 Project Status

- **Completion**: 99%
- **Pending**: Figure assembly, journal formatting (1%)
- **Target journal**: Lancet Oncology (recommended)
- **Estimated time to submission**: 1-2 hours remaining

---

**Generated by**: `tooling/python/consolidate_project_outputs.py`
**Last updated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""

    index_path.write_text(content)
    print(f"📄 Created project index: {index_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Consolidate all project outputs into organized directory"
    )
    parser.add_argument(
        "--project-name",
        default="ici-breast-cancer",
        help="Name of the project (default: ici-breast-cancer)"
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Root directory of the project (default: current directory)"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory (default: projects/{project-name})"
    )

    args = parser.parse_args()

    consolidate_outputs(
        root_dir=args.root,
        project_name=args.project_name,
        output_dir=args.output
    )


if __name__ == "__main__":
    main()
