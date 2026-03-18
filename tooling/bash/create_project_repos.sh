#!/usr/bin/env bash
# Create GitHub private repositories for meta-pipe projects
# Usage: bash create_project_repos.sh

set -euo pipefail

# Project root
PROJECT_ROOT="/Users/htlin/meta-pipe/projects"

# Define projects and descriptions
declare -A PROJECTS
PROJECTS["btk-wm"]="Network meta-analysis comparing BTK inhibitors (zanubrutinib, acalabrutinib, ibrutinib) in Waldenström macroglobulinemia"
PROJECTS["caffeine-endurance"]="Meta-analysis of caffeine supplementation effects on endurance exercise performance in healthy adults"
PROJECTS["early-immuno-timing"]="Meta-analysis comparing neoadjuvant vs perioperative vs adjuvant immune checkpoint inhibitor timing in resectable early-stage NSCLC"
PROJECTS["early-immuno-timing-nma"]="Network meta-analysis of optimal immunotherapy timing strategies (neoadjuvant/perioperative/adjuvant) in early-stage NSCLC Stage II-III"
PROJECTS["hrd-parp-inhibitors"]="Network meta-analysis of PARP inhibitors (olaparib, talazoparib, niraparib) in BRCA-mutated breast cancer"
PROJECTS["ici-breast-cancer"]="Meta-analysis of immune checkpoint inhibitors in neoadjuvant triple-negative breast cancer (5 RCTs, N=2402)"

echo "🚀 Creating GitHub private repositories for meta-pipe projects..."
echo ""

# Function to create README.md
create_readme() {
    local project_name="$1"
    local description="$2"
    local readme_file="$PROJECT_ROOT/$project_name/README.md"

    # Check if README already exists
    if [[ -f "$readme_file" ]]; then
        echo "  ℹ️  README.md already exists for $project_name, skipping creation"
        return 0
    fi

    cat > "$readme_file" <<EOF
# ${project_name}

**Meta-Analysis Project**

## Description

${description}

## Project Structure

This is a meta-analysis project created using the [meta-pipe](https://github.com/htlin/meta-pipe) framework.

\`\`\`
${project_name}/
├── 01_protocol/       # Research protocol, PICO, eligibility criteria
├── 02_search/         # Literature search results
├── 03_screening/      # Title/abstract screening
├── 04_fulltext/       # Full-text PDF collection
├── 05_extraction/     # Data extraction
├── 06_analysis/       # Statistical analysis (R scripts)
├── 07_manuscript/     # Manuscript sections
├── 08_documentation/  # QA and documentation
└── TOPIC.txt          # Research question definition
\`\`\`

## Status

See \`TOPIC.txt\` for research question and \`00_overview/\` (if exists) for progress summary.

## Framework

This project uses [meta-pipe](https://github.com/htlin/meta-pipe), an AI-assisted meta-analysis pipeline.

**Time saved**: 80-100 hours compared to manual meta-analysis.

## License

Private research project.

---

**Generated**: $(date +%Y-%m-%d)
EOF

    echo "  ✅ Created README.md for $project_name"
}

# Function to create .gitignore
create_gitignore() {
    local project_name="$1"
    local gitignore_file="$PROJECT_ROOT/$project_name/.gitignore"

    if [[ -f "$gitignore_file" ]]; then
        echo "  ℹ️  .gitignore already exists for $project_name, skipping"
        return 0
    fi

    if [[ -f "$PROJECT_ROOT/.gitignore.template" ]]; then
        cp "$PROJECT_ROOT/.gitignore.template" "$gitignore_file"
        echo "  ✅ Created .gitignore for $project_name"
    else
        echo "  ⚠️  .gitignore.template not found, skipping"
    fi
}

# Function to initialize git and create GitHub repo
create_github_repo() {
    local project_name="$1"
    local description="$2"
    local project_dir="$PROJECT_ROOT/$project_name"

    cd "$project_dir" || exit 1

    echo "📦 Processing: $project_name"

    # Create README and .gitignore
    create_readme "$project_name" "$description"
    create_gitignore "$project_name"

    # Initialize git if not already initialized
    if [[ ! -d ".git" ]]; then
        echo "  🔧 Initializing git repository..."
        git init
        git add .
        git commit -m "Initial commit: $description

Co-Authored-By: Claude <noreply@anthropic.com>"
    else
        echo "  ℹ️  Git already initialized, checking for uncommitted changes..."
        if [[ -n $(git status --porcelain) ]]; then
            git add .
            git commit -m "Update project files before GitHub sync

Co-Authored-By: Claude <noreply@anthropic.com>" || true
        fi
    fi

    # Create GitHub private repository
    echo "  🌐 Creating GitHub private repository..."
    if gh repo create "$project_name" --private --description "$description" --source=. 2>/dev/null; then
        echo "  ✅ GitHub repo created: https://github.com/htlin/$project_name"
    else
        echo "  ⚠️  Repo may already exist, attempting to add remote..."
        git remote add origin "https://github.com/htlin/$project_name.git" 2>/dev/null || true
    fi

    # Push to GitHub
    echo "  📤 Pushing to GitHub..."
    git branch -M main
    git push -u origin main --force

    echo "  ✅ Successfully synced $project_name to GitHub"
    echo ""
}

# Main execution
echo "Found ${#PROJECTS[@]} projects to process:"
for project in "${!PROJECTS[@]}"; do
    echo "  - $project"
done
echo ""

# Process each project
for project in "${!PROJECTS[@]}"; do
    create_github_repo "$project" "${PROJECTS[$project]}"
done

echo "🎉 All projects successfully created and pushed to GitHub!"
echo ""
echo "📝 Summary:"
for project in "${!PROJECTS[@]}"; do
    echo "  ✅ https://github.com/htlin/$project"
done
