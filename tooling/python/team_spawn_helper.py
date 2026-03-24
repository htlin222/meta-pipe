#!/usr/bin/env python3
"""Generate filled spawn prompts for agent team teammates.

Reads a spawn prompt template from ma-agent-teams/prompts/ and substitutes
project-specific placeholders. The output can be used as the spawn prompt
when the lead creates a teammate.

Usage:
    uv run tooling/python/team_spawn_helper.py --project gcsf-neutropenia --role statistician
    uv run tooling/python/team_spawn_helper.py --project gcsf-neutropenia --role screening-reviewer --list
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
PROMPTS_DIR = REPO_ROOT / "ma-agent-teams" / "prompts"

AVAILABLE_ROLES = [
    "protocol-architect",
    "search-specialist",
    "screening-reviewer",
    "fulltext-manager",
    "data-extractor",
    "statistician",
    "manuscript-writer",
    "qa-auditor",
]


def get_prompt(role: str, project_name: str) -> str:
    """Read and fill a spawn prompt template."""
    template_path = PROMPTS_DIR / f"{role}.md"
    if not template_path.exists():
        print(f"Error: No prompt template found at {template_path}", file=sys.stderr)
        print(f"Available roles: {', '.join(AVAILABLE_ROLES)}", file=sys.stderr)
        sys.exit(1)

    template = template_path.read_text()

    project_root = REPO_ROOT / "projects" / project_name
    filled = template.replace("{{project-name}}", project_name)
    filled = filled.replace("{{project-root}}", str(project_root))

    return filled


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate spawn prompts for agent team teammates"
    )
    parser.add_argument(
        "--project",
        required=True,
        help="Project name (e.g., gcsf-neutropenia)",
    )
    parser.add_argument(
        "--role",
        help="Teammate role (e.g., statistician)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available roles and exit",
    )

    args = parser.parse_args()

    if args.list:
        print("Available roles:")
        for role in AVAILABLE_ROLES:
            template_path = PROMPTS_DIR / f"{role}.md"
            status = "✓" if template_path.exists() else "✗ (missing)"
            print(f"  {role} {status}")
        return

    if not args.role:
        parser.error("--role is required (or use --list to see available roles)")

    if args.role not in AVAILABLE_ROLES:
        print(f"Error: Unknown role '{args.role}'", file=sys.stderr)
        print(f"Available roles: {', '.join(AVAILABLE_ROLES)}", file=sys.stderr)
        sys.exit(1)

    prompt = get_prompt(args.role, args.project)
    print(prompt)


if __name__ == "__main__":
    main()
