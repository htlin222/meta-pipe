# ICI-BREAST-CANCER Project Outputs

**Consolidated Date**: 2026-02-07 16:34:23
**Total Files**: 86 copied, 0 missing

---

## 📊 Project Overview

This directory contains all outputs from the ici-breast-cancer meta-analysis project,
organized by pipeline stage for easy review and archival.

### Directory Structure

```
projects/ici-breast-cancer/
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


### 00_overview

- `CLAUDE_MD_UPDATE_SUMMARY.md` (12.6 KB)
- `CURRENT_STATUS.md` (10.0 KB)
- `FEASIBILITY_REPORT.md` (17.6 KB)
- `FINAL_PROJECT_SUMMARY.md` (13.7 KB)
- `PARALLEL_WORK_SUMMARY.md` (8.9 KB)
- `PROGRESS_TRACKING_SUMMARY.md` (5.9 KB)
- `PROJECT_STATUS_FINAL.md` (11.9 KB)
- `SKILLS_GENERALIZATION_REPORT.md` (11.1 KB)
- `feasibility_abstracts.json` (42.0 KB)
- `feasibility_hour1_analysis.md` (6.5 KB)
- `feasibility_hour2_pilot_extraction.md` (12.1 KB)
- `feasibility_hour3_scoring.md` (13.7 KB)

### 01_protocol

- `TOPIC.txt` (7.2 KB)
- `eligibility.md` (10.4 KB)
- `pico.yaml` (20.3 KB)
- `prospero_registration.md` (15.9 KB)
- `search_strategy.md` (14.3 KB)

### 02_search

- `SEARCH_COMPLETION_REPORT.md` (9.2 KB)
- `round-01_dedupe.bib` (77.4 KB)
- `round-01_pubmed.bib` (77.6 KB)
- `round-01_pubmed_log.md` (1.6 KB)

### 03_screening

- `AI_SCREENING_REPORT.md` (8.6 KB)
- `SCREENING_COMPLETE.md` (8.9 KB)
- `SCREENING_QUICKSTART.md` (11.6 KB)
- `round-01_decisions.csv` (61.0 KB)
- `round-01_decisions_ai_screened.csv` (72.2 KB)
- `round-01_decisions_screened.csv` (72.2 KB)

### 04_fulltext

- `PHASE4_QUICKSTART.md` (9.6 KB)
- `PHASE4_SUMMARY.md` (7.7 KB)
- `round-01_fulltext_subset.bib` (59.2 KB)
- `round-01_include_list.txt` (2.0 KB)

### 05_extraction

- `data-dictionary.md` (18.4 KB)
- `round-01_EXTRACTION_SUMMARY.md` (11.3 KB)
- `round-01_QUICK_STATS.md` (5.6 KB)
- `round-01_extraction.csv` (3.3 KB)
- `round-01_safety_data.csv` (2.1 KB)

### 06_analysis

- `01_pCR_meta_analysis.R` (12.8 KB)
- `02_PDL1_subgroup_analysis.R` (12.4 KB)
- `03_EFS_meta_analysis.R` (12.7 KB)
- `04_OS_meta_analysis.R` (14.9 KB)
- `05_safety_meta_analysis.R` (18.9 KB)
- `ANALYSIS_PROGRESS_SUMMARY.md` (11.6 KB)
- `EFS_META_ANALYSIS_REPORT.md` (13.4 KB)
- `META_ANALYSIS_SUMMARY.md` (8.8 KB)
- `OS_META_ANALYSIS_REPORT.md` (18.0 KB)
- `PDL1_SUBGROUP_REPORT.md` (10.7 KB)
- `SAFETY_META_ANALYSIS_REPORT.md` (13.3 KB)
- `tables_EFS_meta_analysis_results.csv` (0.4 KB)
- `tables_OS_meta_analysis_results.csv` (0.4 KB)
- `tables_PDL1_subgroup_comparison.csv` (0.2 KB)
- `tables_pCR_meta_analysis_results.csv` (0.5 KB)
- `tables_safety_meta_analysis_summary.csv` (0.3 KB)

### 07_manuscript

- `00_abstract.md` (3.1 KB)
- `01_introduction.md` (5.3 KB)
- `02_methods.md` (8.5 KB)
- `03_results.md` (8.8 KB)
- `04_discussion.md` (10.5 KB)
- `CITATION_MAPPING.md` (9.0 KB)
- `COMPLETION_SUMMARY.md` (6.0 KB)
- `FIGURES_ASSEMBLY_SUMMARY.md` (9.0 KB)
- `FIGURE_LEGENDS.md` (10.4 KB)
- `REFERENCES_COMPLETION_SUMMARY.md` (7.2 KB)
- `REFERENCES_USAGE_GUIDE.md` (11.0 KB)
- `TABLES_FIGURES_PLAN.md` (6.7 KB)
- `TABLES_FIGURES_STATUS.md` (9.8 KB)
- `references.bib` (17.6 KB)
- `tables_SupplementaryTable1_RiskOfBias.md` (7.8 KB)
- `tables_SupplementaryTable2_PDL1_Subgroup.md` (7.6 KB)
- `tables_SupplementaryTable3_Individual_pCR_Results.md` (11.2 KB)
- `tables_SupplementaryTable4_GRADE_Profile.md` (21.1 KB)
- `tables_Table1_Trial_Characteristics.md` (2.6 KB)
- `tables_Table2_Efficacy_Summary.md` (3.1 KB)
- `tables_Table3_Safety_Summary.md` (3.9 KB)

### 08_documentation

- `API_SETUP.md` (2.6 KB)
- `CLAUDE.md` (18.5 KB)
- `CLAUDE_MD_ADDITIONS.md` (11.0 KB)
- `FEASIBILITY_CHECKLIST.md` (13.7 KB)
- `GETTING_STARTED.md` (9.9 KB)
- `JOURNAL_FORMATTING.md` (3.1 KB)
- `MANUSCRIPT_ASSEMBLY.md` (4.1 KB)
- `RAYYAN_SETUP.md` (9.8 KB)
- `SKILL_GENERALIZATION.md` (4.0 KB)
- `TIME_GUIDANCE.md` (2.7 KB)
- `ZOTERO_SETUP.md` (15.3 KB)

### 09_scripts

- `python_ai_screen_titles.py` (8.6 KB)
- `python_assemble_figures.py` (11.4 KB)

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
**Last updated**: 2026-02-07 16:34:23
