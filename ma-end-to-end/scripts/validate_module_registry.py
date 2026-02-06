#!/usr/bin/env python3
"""Validate that all scripts are properly registered in documentation.

Checks for:
  1. Orphan scripts  - scripts that exist but aren't documented
  2. Ghost references - docs referencing scripts that don't exist
  3. SKILL.md coverage - each module's SKILL.md mentions its scripts
  4. CLAUDE.md coverage - main agent instructions reference the scripts
  5. GETTING_STARTED.md coverage - user-facing docs reference the scripts
  6. tests/README.md coverage - test instructions exist

Exit codes:
  0 = all checks pass
  1 = warnings only (missing test docs)
  2 = errors found (orphan scripts or ghost references)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


# Patterns to scan for script references in documentation
SCRIPT_REF_RE = re.compile(r"[\w/.-]*scripts/[\w_-]+\.py|[\w_-]+\.py")

# Scripts to always skip (utility modules, not user-facing)
SKIP_SCRIPTS = {
    "env_utils.py",
    "main.py",
    "__init__.py",
}

# Documentation files to check
DOC_FILES = {
    "skill": "{module}/SKILL.md",
    "claude": "CLAUDE.md",
    "getting_started": "GETTING_STARTED.md",
    "tests": "tests/README.md",
}


def discover_scripts(root: Path) -> dict[str, list[Path]]:
    """Discover all Python scripts grouped by module.

    Returns: {"ma-peer-review": [Path(...), ...], "tooling/python": [...]}
    """
    modules: dict[str, list[Path]] = {}

    # ma-*/scripts/*.py
    for script in sorted(root.glob("ma-*/scripts/*.py")):
        if script.name in SKIP_SCRIPTS:
            continue
        module = script.parent.parent.name
        modules.setdefault(module, []).append(script)

    # tooling/python/*.py
    for script in sorted(root.glob("tooling/python/*.py")):
        if script.name in SKIP_SCRIPTS:
            continue
        modules.setdefault("tooling/python", []).append(script)

    # tests/*.py (test runners - tracked but not required in SKILL.md)
    for script in sorted(root.glob("tests/*.py")):
        if script.name in SKIP_SCRIPTS:
            continue
        modules.setdefault("tests", []).append(script)

    return modules


def extract_script_refs(text: str) -> set[str]:
    """Extract script filenames referenced in a doc."""
    refs = set()
    for match in SCRIPT_REF_RE.finditer(text):
        ref = match.group(0)
        # Normalize: extract just the filename
        basename = Path(ref).name
        if basename.endswith(".py"):
            refs.add(basename)
    return refs


def check_doc_coverage(
    doc_path: Path,
    scripts: list[Path],
    label: str,
) -> tuple[list[str], list[str]]:
    """Check if scripts are referenced in a documentation file.

    Returns: (orphans, ghosts) where orphans are undocumented scripts
    and ghosts are referenced but nonexistent scripts.
    """
    orphans: list[str] = []
    ghosts: list[str] = []

    if not doc_path.exists():
        for s in scripts:
            orphans.append(f"[{label}] {s.name} - doc file missing: {doc_path}")
        return orphans, ghosts

    text = doc_path.read_text()
    refs = extract_script_refs(text)

    # Check orphans (scripts not referenced)
    for script in scripts:
        if script.name not in refs:
            orphans.append(f"[{label}] {script.name} not referenced in {doc_path.name}")

    return orphans, ghosts


def check_ghost_references(root: Path, all_scripts: set[str]) -> list[str]:
    """Find documentation references to scripts that don't exist."""
    ghosts: list[str] = []

    for doc_key, doc_pattern in DOC_FILES.items():
        if "{module}" in doc_pattern:
            # Check each module's SKILL.md
            for module_dir in sorted(root.glob("ma-*")):
                doc_path = module_dir / "SKILL.md"
                if not doc_path.exists():
                    continue
                refs = extract_script_refs(doc_path.read_text())
                for ref in refs:
                    if ref not in all_scripts and ref not in SKIP_SCRIPTS:
                        ghosts.append(
                            f"[ghost] {doc_path.name} ({module_dir.name}) "
                            f"references {ref} which doesn't exist"
                        )
        else:
            doc_path = root / doc_pattern
            if not doc_path.exists():
                continue
            refs = extract_script_refs(doc_path.read_text())
            for ref in refs:
                if ref not in all_scripts and ref not in SKIP_SCRIPTS:
                    ghosts.append(
                        f"[ghost] {doc_path.name} references {ref} which doesn't exist"
                    )

    return ghosts


def build_registry(root: Path) -> dict:
    """Build a complete module registry for JSON output."""
    modules = discover_scripts(root)
    registry: dict = {"modules": {}, "total_scripts": 0}

    for module_name, scripts in sorted(modules.items()):
        script_names = [s.name for s in scripts]
        registry["modules"][module_name] = {
            "scripts": script_names,
            "count": len(script_names),
        }

        # Check SKILL.md coverage
        if module_name.startswith("ma-"):
            skill_path = root / module_name / "SKILL.md"
            if skill_path.exists():
                refs = extract_script_refs(skill_path.read_text())
                documented = [s for s in script_names if s in refs]
                registry["modules"][module_name]["skill_documented"] = documented
                registry["modules"][module_name]["skill_missing"] = [
                    s for s in script_names if s not in refs
                ]

        registry["total_scripts"] += len(script_names)

    return registry


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate module registry: check scripts are documented."
    )
    parser.add_argument("--root", default=".", help="Project root directory")
    parser.add_argument(
        "--out-json",
        help="Output registry as JSON (optional)",
    )
    parser.add_argument(
        "--out-md",
        help="Output report as markdown (optional)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings (missing test docs) as errors",
    )
    args = parser.parse_args()

    root = Path(args.root).resolve()
    modules = discover_scripts(root)

    # Collect all script names for ghost detection
    all_script_names = set()
    for scripts in modules.values():
        for s in scripts:
            all_script_names.add(s.name)

    errors: list[str] = []
    warnings: list[str] = []

    # 1. Check SKILL.md coverage (each module documents its own scripts)
    for module_name, scripts in modules.items():
        if module_name.startswith("ma-"):
            skill_path = root / module_name / "SKILL.md"
            orphans, _ = check_doc_coverage(skill_path, scripts, f"SKILL({module_name})")
            errors.extend(orphans)

    # 2. Check CLAUDE.md coverage
    claude_path = root / "CLAUDE.md"
    for module_name, scripts in modules.items():
        orphans, _ = check_doc_coverage(claude_path, scripts, "CLAUDE.md")
        # CLAUDE.md doesn't need to list every script; only user-facing ones
        # So these are warnings, not errors
        warnings.extend(orphans)

    # 3. Check GETTING_STARTED.md coverage
    gs_path = root / "GETTING_STARTED.md"
    for module_name, scripts in modules.items():
        orphans, _ = check_doc_coverage(gs_path, scripts, "GETTING_STARTED.md")
        warnings.extend(orphans)

    # 4. Check tests/README.md coverage
    tests_path = root / "tests" / "README.md"
    for module_name, scripts in modules.items():
        orphans, _ = check_doc_coverage(tests_path, scripts, "tests/README.md")
        warnings.extend(orphans)

    # 5. Ghost reference detection
    ghosts = check_ghost_references(root, all_script_names)
    errors.extend(ghosts)

    # Build registry
    registry = build_registry(root)

    # Output JSON
    if args.out_json:
        out_json = Path(args.out_json)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        registry["validation"] = {
            "errors": errors,
            "warnings": warnings,
            "status": "pass" if not errors else "fail",
        }
        out_json.write_text(json.dumps(registry, indent=2) + "\n")

    # Output markdown report
    report_lines = build_report(modules, errors, warnings, registry)
    report_text = "\n".join(report_lines) + "\n"

    if args.out_md:
        out_md = Path(args.out_md)
        out_md.parent.mkdir(parents=True, exist_ok=True)
        out_md.write_text(report_text)

    # Print summary
    print(f"Module Registry Validation")
    print(f"  Modules: {len(modules)}")
    print(f"  Scripts: {registry['total_scripts']}")
    print(f"  Errors:  {len(errors)}")
    print(f"  Warnings: {len(warnings)}")

    if errors:
        print("\nErrors (scripts not registered):")
        for e in errors:
            print(f"  - {e}")

    if args.strict and warnings:
        print("\nWarnings (treated as errors with --strict):")
        for w in warnings:
            print(f"  - {w}")

    if errors or (args.strict and warnings):
        raise SystemExit(2)

    if warnings:
        print(f"\n{len(warnings)} warnings (use --strict to enforce)")
        raise SystemExit(1)

    print("\nAll checks passed.")


def build_report(
    modules: dict[str, list[Path]],
    errors: list[str],
    warnings: list[str],
    registry: dict,
) -> list[str]:
    """Build a markdown validation report."""
    lines = [
        "# Module Registry Validation Report",
        "",
        "## Summary",
        "",
        f"- **Modules**: {len(modules)}",
        f"- **Total scripts**: {registry['total_scripts']}",
        f"- **Errors**: {len(errors)}",
        f"- **Warnings**: {len(warnings)}",
        f"- **Status**: {'PASS' if not errors else 'FAIL'}",
        "",
    ]

    # Module inventory
    lines.append("## Module Inventory")
    lines.append("")
    lines.append("| Module | Scripts | SKILL.md |")
    lines.append("| --- | --- | --- |")
    for module_name in sorted(registry["modules"]):
        info = registry["modules"][module_name]
        count = info["count"]
        missing = info.get("skill_missing", [])
        status = f"{count - len(missing)}/{count}" if "skill_missing" in info else "N/A"
        lines.append(f"| `{module_name}` | {count} | {status} |")
    lines.append("")

    # Errors
    if errors:
        lines.append("## Errors")
        lines.append("")
        for e in errors:
            lines.append(f"- {e}")
        lines.append("")

    # Warnings
    if warnings:
        lines.append("## Warnings")
        lines.append("")
        for w in warnings:
            lines.append(f"- {w}")
        lines.append("")

    # Full script list
    lines.append("## Full Script Registry")
    lines.append("")
    for module_name, scripts in sorted(modules.items()):
        lines.append(f"### {module_name}")
        lines.append("")
        for s in scripts:
            lines.append(f"- `{s.name}`")
        lines.append("")

    return lines


if __name__ == "__main__":
    main()
