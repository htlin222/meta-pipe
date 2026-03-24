#!/bin/bash
# TaskCompleted hook for meta-pipe agent teams
#
# Runs when a task is being marked complete.
# Exit 2 = reject completion and send feedback
# Exit 0 = accept completion
#
# Validates that expected output files exist for stage-completion tasks.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

# The task description is passed via environment or stdin
TASK_DESC="${CLAUDE_TASK_DESCRIPTION:-}"

# Try to extract project name from task description or working directory
# Look for pattern: projects/<name>/
PROJECT_NAME=""
if [[ "$TASK_DESC" =~ projects/([a-zA-Z0-9_-]+)/ ]]; then
    PROJECT_NAME="${BASH_REMATCH[1]}"
fi

# If no project found in task, try to find it from existing projects
if [[ -z "$PROJECT_NAME" ]]; then
    # Look for the most recently modified project
    PROJECT_NAME=$(ls -t "$REPO_ROOT/projects/" 2>/dev/null | head -1 || true)
fi

# If still no project, accept the completion (can't validate)
if [[ -z "$PROJECT_NAME" || "$PROJECT_NAME" == "legacy" ]]; then
    exit 0
fi

PROJECT_DIR="$REPO_ROOT/projects/$PROJECT_NAME"

# If project directory doesn't exist, accept
if [[ ! -d "$PROJECT_DIR" ]]; then
    exit 0
fi

# Validate based on task keywords
validate_stage() {
    local stage="$1"
    case "$stage" in
        "protocol"|"01")
            if [[ ! -f "$PROJECT_DIR/01_protocol/pico.yaml" ]]; then
                echo "Task incomplete: 01_protocol/pico.yaml not found. Protocol must include PICO framework."
                exit 2
            fi
            if [[ ! -f "$PROJECT_DIR/01_protocol/eligibility.md" ]]; then
                echo "Task incomplete: 01_protocol/eligibility.md not found. Eligibility criteria required."
                exit 2
            fi
            ;;
        "search"|"02")
            if [[ ! -f "$PROJECT_DIR/02_search/round-01/dedupe.bib" ]]; then
                echo "Task incomplete: 02_search/round-01/dedupe.bib not found. Deduplicated bibliography required."
                exit 2
            fi
            ;;
        "screening"|"03")
            if [[ ! -f "$PROJECT_DIR/03_screening/round-01/decisions.csv" ]]; then
                echo "Task incomplete: 03_screening/round-01/decisions.csv not found. Screening decisions required."
                exit 2
            fi
            ;;
        "fulltext"|"04")
            if [[ ! -f "$PROJECT_DIR/04_fulltext/manifest.csv" ]]; then
                echo "Task incomplete: 04_fulltext/manifest.csv not found. PDF manifest required."
                exit 2
            fi
            ;;
        "extraction"|"05")
            if [[ ! -f "$PROJECT_DIR/05_extraction/round-01/extraction.csv" ]]; then
                echo "Task incomplete: 05_extraction/round-01/extraction.csv not found. Extraction data required."
                exit 2
            fi
            ;;
        "analysis"|"meta-analysis"|"06")
            if [[ ! -d "$PROJECT_DIR/06_analysis/figures" ]]; then
                echo "Task incomplete: 06_analysis/figures/ not found. Analysis figures required."
                exit 2
            fi
            if [[ ! -d "$PROJECT_DIR/06_analysis/tables" ]]; then
                echo "Task incomplete: 06_analysis/tables/ not found. Analysis tables required."
                exit 2
            fi
            ;;
        "manuscript"|"07")
            if [[ ! -f "$PROJECT_DIR/07_manuscript/index.qmd" ]]; then
                echo "Task incomplete: 07_manuscript/index.qmd not found. Manuscript required."
                exit 2
            fi
            ;;
        "grade"|"review"|"08")
            if [[ ! -f "$PROJECT_DIR/08_reviews/grade_summary.csv" ]]; then
                echo "Task incomplete: 08_reviews/grade_summary.csv not found. GRADE assessment required."
                exit 2
            fi
            ;;
        "qa"|"09")
            if [[ ! -f "$PROJECT_DIR/09_qa/pipeline-checklist.md" ]]; then
                echo "Task incomplete: 09_qa/pipeline-checklist.md not found. PRISMA checklist required."
                exit 2
            fi
            ;;
        *)
            # Unknown stage, accept completion
            ;;
    esac
}

# Try to detect which stage this task is about
TASK_LOWER=$(echo "$TASK_DESC" | tr '[:upper:]' '[:lower:]')

for keyword in protocol search screening fulltext extraction analysis manuscript grade review qa; do
    if echo "$TASK_LOWER" | grep -q "$keyword"; then
        validate_stage "$keyword"
    fi
done

# If we get here, all validations passed (or no stage detected)
exit 0
