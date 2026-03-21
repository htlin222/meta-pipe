#!/usr/bin/env python3
"""Check and report meta-analysis project status."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Stage definitions with expected outputs
STAGES = {
    "01_protocol": {
        "name": "Protocol Development",
        "key_files": ["pico.yaml", "eligibility.md"],
        "optional_files": ["prospero_registration.md"],
        "validation": lambda p: (p / "pico.yaml").exists(),
    },
    "02_search": {
        "name": "Literature Search",
        "key_files": ["round-01/dedupe.bib", "round-01/queries.txt"],
        "validation": lambda p: (p / "round-01" / "dedupe.bib").exists(),
    },
    "03_screening": {
        "name": "Title/Abstract Screening",
        "key_files": ["round-01/decisions.csv", "round-01/agreement.md"],
        "validation": lambda p: (p / "round-01" / "decisions.csv").exists(),
    },
    "04_fulltext": {
        "name": "Full-text Retrieval & Screening",
        "key_files": ["manifest.csv", "fulltext_decisions.csv", "ft_agreement.md"],
        "validation": lambda p: (p / "manifest.csv").exists(),
    },
    "05_extraction": {
        "name": "Data Extraction",
        "key_files": ["round-01/extraction.csv", "data-dictionary.md"],
        "validation": lambda p: (p / "round-01" / "extraction.csv").exists(),
    },
    "06_analysis": {
        "name": "Meta-Analysis",
        "key_files": ["figures/", "tables/"],
        "validation": lambda p: (p / "figures").exists() and (p / "tables").exists(),
    },
    "07_manuscript": {
        "name": "Manuscript Assembly",
        "key_files": ["index.qmd", "manuscript_outline.md"],
        "validation": lambda p: (p / "index.qmd").exists(),
    },
    "08_reviews": {
        "name": "GRADE Assessment",
        "key_files": ["grade_summary.csv"],
        "validation": lambda p: (p / "grade_summary.csv").exists(),
    },
    "09_qa": {
        "name": "Quality Assurance",
        "key_files": ["pipeline-checklist.md"],
        "validation": lambda p: True,  # Always exists
    },
}


def check_stage_status(project_root: Path, stage: str) -> Dict:
    """Check completion status of a single stage."""
    stage_dir = project_root / stage
    stage_info = STAGES[stage]

    status = {
        "stage": stage,
        "name": stage_info["name"],
        "exists": stage_dir.exists(),
        "validated": False,
        "key_files_present": [],
        "key_files_missing": [],
        "file_count": 0,
        "last_modified": None,
    }

    if not stage_dir.exists():
        return status

    # Check validation
    status["validated"] = stage_info["validation"](stage_dir)

    # Check key files
    for key_file in stage_info["key_files"]:
        file_path = stage_dir / key_file
        if file_path.exists():
            status["key_files_present"].append(key_file)
        else:
            status["key_files_missing"].append(key_file)

    # Count files (excluding hidden files)
    status["file_count"] = sum(
        1 for f in stage_dir.rglob("*")
        if f.is_file() and not f.name.startswith(".")
    )

    # Last modified time
    all_files = [f for f in stage_dir.rglob("*") if f.is_file()]
    if all_files:
        latest_file = max(all_files, key=lambda f: f.stat().st_mtime)
        status["last_modified"] = datetime.fromtimestamp(
            latest_file.stat().st_mtime
        ).isoformat()

    return status


def get_project_status(project_root: Path) -> Dict:
    """Get comprehensive project status."""
    status = {
        "project_name": project_root.name,
        "project_root": str(project_root),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "stages": {},
        "current_stage": None,
        "completion_percentage": 0,
        "next_action": None,
    }

    # Check all stages
    completed_stages = 0
    last_completed_stage = None

    for stage in STAGES.keys():
        stage_status = check_stage_status(project_root, stage)
        status["stages"][stage] = stage_status

        if stage_status["validated"]:
            completed_stages += 1
            last_completed_stage = stage

    # Calculate completion percentage
    status["completion_percentage"] = int((completed_stages / len(STAGES)) * 100)

    # Determine current stage (next incomplete stage)
    for stage in STAGES.keys():
        if not status["stages"][stage]["validated"]:
            status["current_stage"] = stage
            break

    # If all complete
    if not status["current_stage"]:
        status["current_stage"] = "09_qa"
        status["next_action"] = "Project complete! Run final QA report."
    else:
        stage_name = STAGES[status["current_stage"]]["name"]
        status["next_action"] = f"Complete {status['current_stage']} ({stage_name})"

    return status


def print_status_report(status: Dict, verbose: bool = False) -> None:
    """Print human-readable status report."""
    print(f"\n{'='*60}")
    print(f"📊 PROJECT STATUS: {status['project_name']}")
    print(f"{'='*60}\n")

    print(f"📁 Location: {status['project_root']}")
    print(f"⏰ Checked: {status['timestamp']}")
    print(f"✅ Completion: {status['completion_percentage']}%")
    print(f"🎯 Current Stage: {status['current_stage']}")
    print(f"➡️  Next Action: {status['next_action']}\n")

    print(f"{'─'*60}")
    print("STAGE PROGRESS:")
    print(f"{'─'*60}\n")

    for stage, stage_status in status["stages"].items():
        stage_name = stage_status["name"]

        if stage_status["validated"]:
            icon = "✅"
        elif stage_status["exists"]:
            icon = "🔄"
        else:
            icon = "⬜"

        print(f"{icon} {stage} - {stage_name}")

        if verbose and stage_status["exists"]:
            print(f"   Files: {stage_status['file_count']}")
            if stage_status["last_modified"]:
                print(f"   Last Modified: {stage_status['last_modified']}")
            if stage_status["key_files_present"]:
                print(f"   ✓ Present: {', '.join(stage_status['key_files_present'])}")
            if stage_status["key_files_missing"]:
                print(f"   ✗ Missing: {', '.join(stage_status['key_files_missing'])}")
        print()

    print(f"{'─'*60}\n")


def save_status_json(status: Dict, output_path: Path) -> None:
    """Save status as JSON for programmatic access."""
    output_path.write_text(json.dumps(status, indent=2))
    print(f"💾 Status saved to: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check meta-analysis project status."
    )
    parser.add_argument(
        "--project",
        required=True,
        help="Project name (in projects/<name>/) or full path",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed file information",
    )
    parser.add_argument(
        "--json",
        help="Save status as JSON to this path",
    )
    args = parser.parse_args()

    # Determine project root
    project_path = Path(args.project)
    if not project_path.is_absolute():
        # Assume it's a project name in projects/
        script_dir = Path(__file__).resolve().parent
        repo_root = script_dir.parent.parent
        project_path = repo_root / "projects" / args.project

    if not project_path.exists():
        print(f"❌ Error: Project not found at {project_path}")
        return

    # Get status
    status = get_project_status(project_path)

    # Print report
    print_status_report(status, verbose=args.verbose)

    # Save JSON if requested
    if args.json:
        json_path = Path(args.json)
        save_status_json(status, json_path)


if __name__ == "__main__":
    main()
