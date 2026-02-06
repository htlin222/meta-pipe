# Git Branch Structure

**Date**: 2026-02-06

---

## Branch Overview

This repository uses a dual-branch structure to separate **reusable tools** from **project-specific work**.

```
main
├── [通用工具] Generalized scripts for any systematic review
│
projects/cdk46-breast
├── [專案資料] CDK4/6 inhibitor meta-analysis specific data
```

---

## Branch: `main`

**Purpose**: Reusable tools and infrastructure for systematic reviews

**Contains**:
- ✅ Generalized scripts in `ma-*` modules
- ✅ Comprehensive documentation
- ✅ CLAUDE.md with Stage 04 workflow
- ✅ Tool integration reports

**Latest commit**: `614fab0` - Add generalized PDF retrieval tools

**Files** (8 files, 2,498 lines):
```
ma-search-bibliography/scripts/
└── bib_subset_by_ids.py                    (198 lines)

ma-fulltext-management/scripts/
├── download_oa_pdfs.py                     (257 lines)
├── analyze_unpaywall.py                    (219 lines)
└── README.md                               (431 lines)

Documentation:
├── REUSABLE_TOOLS_SUMMARY.md              (407 lines)
├── TOOL_INTEGRATION_REPORT.md             (345 lines)
├── tooling/python/MIGRATION_SUMMARY.md    (331 lines)
└── tooling/python/SCRIPT_ANALYSIS.md      (310 lines)
```

**Use cases**:
- Any future systematic review project
- Stage 04 full-text retrieval workflows
- PDF automation and OA analysis

---

## Branch: `projects/cdk46-breast`

**Purpose**: CDK4/6 inhibitor post-progression meta-analysis project data

**Contains**:
- ✅ All stage data (01-04)
- ✅ Search results (447 records)
- ✅ Screening results (52 for full-text)
- ✅ Project-specific scripts
- ✅ Retrieval guides and manifests

**Latest commit**: `418fb25` - CDK4/6 inhibitor project progress

**Files** (40 files, 24,906 lines):
```
01_protocol/
├── pico.yaml                               # Structured PICO
└── eligibility.md                          # Screening criteria

02_search/round-01/
├── dedupe.bib                              # 447 records
├── pubmed.bib                              # 54 records
├── scopus.bib                              # 440 records
├── manual_additions.bib                    # 6 key trials
└── queries_refined.txt                     # Search strategies

03_screening/round-01/
├── decisions_screened_r1.csv              # 52 for full-text
├── screening_summary.md                    # Results report
└── screening_guide.md                      # Screening instructions

04_fulltext/round-01/
├── fulltext_subset.bib                     # 52 records
├── unpaywall_results.csv                   # OA status (51/52)
├── pdf_retrieval_manifest_updated.csv      # Retrieval tracking
├── PDF_RETRIEVAL_REPORT.md                 # Comprehensive analysis
├── PRIORITY_RETRIEVAL_LIST.md              # Manual retrieval guide
└── pdfs/ (10 PDFs downloaded)

tooling/python/
├── auto_screening.py                       # AI screening (CDK4/6 keywords)
├── bib_to_csv.py                          # BibTeX converter
├── check_key_trials_oa.py                 # Key trial checker
├── prepare_fulltext_review.py             # Full-text prep
└── [Original versions before generalization]
```

**Project Status**:
- Stage 01-04: ✅ COMPLETE
- Stage 05-09: ⏳ PENDING
- PDFs retrieved: 10/52 (19.2%)
- Key trials: 10/10 identified (100%)

---

## Branching Strategy

### Main Branch (`main`)

**What to commit here**:
- ✅ Generalized, reusable scripts
- ✅ Tool documentation (README.md)
- ✅ Workflow updates (CLAUDE.md)
- ✅ Infrastructure improvements

**What NOT to commit here**:
- ❌ Project-specific data files
- ❌ Search results (.bib, .csv)
- ❌ Study-specific documentation
- ❌ Hardcoded project scripts

### Project Branch (`projects/cdk46-breast`)

**What to commit here**:
- ✅ All stage data (01-09)
- ✅ Search and screening results
- ✅ Project-specific scripts
- ✅ Retrieval manifests and guides
- ✅ Study-specific documentation

**What NOT to commit here**:
- ❌ Changes to reusable tools (put in main)
- ❌ CLAUDE.md updates (unless project-specific)

---

## Switching Between Branches

### Work on Reusable Tools

```bash
git checkout main
# Make changes to ma-* scripts or documentation
git add <changed files>
git commit -m "Description of tool improvements"
```

### Work on Project Data

```bash
git checkout projects/cdk46-breast
# Work on stage data, screening, retrieval
git add <project files>
git commit -m "Project progress update"
```

### Sync Changes

If you make tool improvements in `main`, merge them into project branch:

```bash
git checkout projects/cdk46-breast
git merge main
```

---

## Commit History

### Main Branch

```
614fab0 - Add generalized PDF retrieval tools for systematic reviews
          * 3 new scripts (bib_subset_by_ids, download_oa_pdfs, analyze_unpaywall)
          * Comprehensive documentation (800+ lines)
          * CLAUDE.md Stage 04 updates

601d7ad - Add environment variables for study characteristics
5b208a0 - polish
7147a84 - INIT
```

### Project Branch

```
418fb25 - CDK4/6 inhibitor post-progression meta-analysis - Project progress
          * Stage 01-04 data
          * 447 search records
          * 52 full-text candidates
          * 10 PDFs retrieved
          * Comprehensive retrieval guides

[Includes all commits from main branch]
```

---

## File Organization

### Shared Across Both Branches

- `ma-*` modules (reusable infrastructure)
- `CLAUDE.md` (workflow documentation)
- `.env.example` (configuration template)
- Basic documentation

### Only in Project Branch

- `01_protocol/` through `09_qa/`
- `TOPIC.txt`
- Project-specific entries in `AGENTS.md`
- All `.bib`, `.csv` data files

---

## Benefits of This Structure

### Separation of Concerns

- **Tools** (main): Can be used by any project
- **Data** (project branches): Isolated per study

### Clean Repository

- Main branch stays lean (only infrastructure)
- Project branches contain full workflow data
- Easy to archive completed projects

### Reusability

- Other researchers can fork `main` for tools only
- Project branches serve as workflow templates
- Clear examples of tool usage in real projects

---

## Future Projects

To start a new systematic review:

```bash
# Start from main (clean tools)
git checkout main

# Create new project branch
git checkout -b projects/new-study-name

# Work on new project
# (All stage data goes here)
```

---

## Summary

| Aspect | Main Branch | Project Branch |
|--------|-------------|----------------|
| **Purpose** | Reusable tools | CDK4/6 study data |
| **Files** | 8 (infrastructure) | 40 (data) |
| **Size** | 2,498 lines | 24,906 lines |
| **Updates** | Tool improvements | Project progress |
| **Audience** | Future projects | This study only |

---

**Current active branch**: `projects/cdk46-breast`
**Next action**: Manual PDF retrieval (42 remaining)
