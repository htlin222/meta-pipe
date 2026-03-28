<div align="center">

# Meta-Analysis Pipeline

[![GitHub stars](https://img.shields.io/github/stars/htlin222/meta-pipe?style=flat-square)](https://github.com/htlin222/meta-pipe/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/htlin222/meta-pipe?style=flat-square)](https://github.com/htlin222/meta-pipe/commits/main)
[![License](https://img.shields.io/badge/license-Academic%20%26%20Non--Commercial-blue?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/python-%E2%89%A53.12-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org)

**AI-assisted, end-to-end meta-analysis with reproducible tooling.**

*From research question to manuscript-ready output -- powered by Claude Code.*

</div>

---

## Quick Start

```bash
# 1. Setup (one-time)
cp .env.example .env        # Add your API keys
cd tooling/python && uv init

# 2. Create a new project
uv run tooling/python/init_project.py --name my-meta-analysis

# 3. Edit your research question
# Open projects/my-meta-analysis/TOPIC.txt and paste your topic

# 4. Launch Claude Code and say:
```

> **"Start project my-meta-analysis"** or **"See projects/my-meta-analysis/TOPIC.txt and start"**

That's it. Claude will handle the rest.

**Don't have a topic yet?** Say:

> **"Help me brainstorm a topic"**

Claude will guide you through an interactive session to develop your research question and create the project for you.

---

## What Claude Does

1. Creates your project in `projects/<your-project-name>/`
2. Reads your topic from `projects/<your-project-name>/TOPIC.txt`
3. Asks clarifying questions (databases, outcomes, dates)
4. Runs the 9-stage pipeline automatically
5. Generates manuscript-ready outputs

## Pipeline Overview

All stages are created inside `projects/<your-project-name>/`:

| Stage         | Output                    |
| ------------- | ------------------------- |
| 01_protocol   | pico.yaml, eligibility.md |
| 02_search     | dedupe.bib                |
| 03_screening  | decisions.csv             |
| 04_fulltext   | manifest.csv              |
| 05_extraction | extraction.csv            |
| 06_analysis   | figures/, tables/         |
| 07_manuscript | manuscript.pdf            |
| 08_reviews    | grade_summary.md          |
| 09_qa         | final_qa_report.md        |

---

## Example: Completed Project

**See a real meta-analysis** → `projects/ici-breast-cancer/`

This is a **99% complete meta-analysis** on immune checkpoint inhibitors in triple-negative breast cancer:

- **5 RCTs, N=2,402 patients**
- **Primary outcome**: RR 1.26 (95% CI 1.16-1.37), p=0.0015, ⊕⊕⊕⊕ HIGH quality
- **Manuscript**: 4,921 words (Lancet Oncology compliant)
- **Time invested**: ~14 hours (vs 100+ hours manual)

**Quick tour**:

1. `projects/ici-breast-cancer/README.md` - Project overview
2. `projects/ici-breast-cancer/00_overview/FINAL_PROJECT_SUMMARY.md` - Key findings
3. `projects/ici-breast-cancer/07_manuscript/` - Complete manuscript (5 sections)

**Use as template** for your own meta-analysis workflow.

## Project Structure

```
meta-pipe/
├── ma-*/                    # Framework code modules
├── docs/archive/            # Archived documentation
├── tooling/                 # Shared tools and scripts
└── projects/                # All your meta-analysis projects
    ├── ici-breast-cancer/   # Example: complete meta-analysis
    ├── legacy/              # Historical data (pre-2026-02-08)
    └── your-project/        # Your new projects
        ├── 01_protocol/
        ├── 02_search/
        ├── ...
        ├── 09_qa/
        └── TOPIC.txt
```

**Note**: Projects are isolated and NOT tracked by Git (see `.gitignore`). Only the example project `ici-breast-cancer/` is tracked for reference.

---

## Documentation

| Doc                                                         | Purpose                      |
| ----------------------------------------------------------- | ---------------------------- |
| [GETTING_STARTED.md](GETTING_STARTED.md)                    | Manual step-by-step guide    |
| [API Setup](ma-search-bibliography/references/api-setup.md) | Database API keys            |
| [CLAUDE.md](CLAUDE.md)                                      | Agent behavior (auto-loaded) |
| [tooling/scripts/](tooling/scripts/)                        | Utility scripts              |

## Citation

If you use meta-pipe in your research, please cite it:

**AMA Format**:

> Lin HT, Yeh JT. meta-pipe: AI-assisted, end-to-end meta-analysis pipeline with reproducible tooling. GitHub; 2025. Accessed 2026. https://github.com/htlin222/meta-pipe

**BibTeX**:

```bibtex
@software{lin_metapipe_2025,
  author       = {Lin, Hsieh-Ting and Yeh, Jiunn-Tyng},
  title        = {meta-pipe: AI-assisted, end-to-end meta-analysis pipeline with reproducible tooling},
  year         = {2025},
  url          = {https://github.com/htlin222/meta-pipe},
  note         = {Accessed: 2026}
}
```

## Requirements

- `uv` (Python)
- R ≥ 4.2 + `renv`
- `cmake` (required for building R packages like `fs` on macOS ARM)
- Quarto
- API keys in `.env`

---

## Citation

If you use meta-pipe in your research, please cite it.

**AMA format**:

> Lin HT, Yeh JT. meta-pipe: AI-assisted, end-to-end meta-analysis pipeline with reproducible tooling. GitHub; 2026. Accessed March 22, 2026. https://github.com/htlin222/meta-pipe

**BibTeX**:

```bibtex
@software{lin2026metapipe,
  author    = {Lin, Hsieh-Ting and Yeh, Jiunn-Tyng},
  title     = {meta-pipe: AI-Assisted, End-to-End Meta-Analysis Pipeline with Reproducible Tooling},
  year      = {2026},
  url       = {https://github.com/htlin222/meta-pipe},
  note      = {Software}
}
```
