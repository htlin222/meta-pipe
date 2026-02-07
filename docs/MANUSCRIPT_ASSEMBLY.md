# Manuscript Assembly Guide

**Reference**: This file is referenced from CLAUDE.md
**When to use**: After Stage 06 analysis complete

---

## When User Says "Complete Manuscript" or "Prepare for Submission"

Use the **meta-manuscript-assembly** skill (`~/.claude/skills/meta-manuscript-assembly/SKILL.md`):

**Triggers**:

- "complete the manuscript"
- "prepare for journal submission"
- "create publication tables"
- "assemble figures for submission"
- "ready to submit"

**5-Phase Workflow**:

1. **Quarto Manuscript Setup** (30 min)
   - Create Quarto document structure (`index.qmd`)
   - Configure YAML frontmatter with bibliography
   - Set output formats: HTML, PDF, DOCX
   - Output directory: `07_manuscript/output/`

2. **Content Writing with Citation Keys** (2-3 hours)
   - Write sections in Quarto markdown
   - Use citation keys: `[@smith2020]` or `@smith2020`
   - Embed figures: `![Caption](figures/figure1.png){#fig-pcr}`
   - Embed tables: `@tbl-characteristics` with Quarto tables
   - Cross-reference: `@fig-pcr`, `@tbl-efficacy`

3. **Figure Assembly** (1-2 hours)
   - Use Python PIL/Pillow for multi-panel figures
   - Export to `07_manuscript/figures/` at 300 DPI
   - Add professional panel labels (A, B, C)
   - Reference in Quarto: `![Figure 1](figures/figure1.png){#fig-1}`

4. **Tables Integration** (1-2 hours)
   - Create tables in Quarto markdown format
   - Or include external files: `{{< include tables/table1.md >}}`
   - Use `kable()` or `gt()` for dynamic tables
   - Caption and label: `{#tbl-characteristics}`

5. **References & Rendering** (1-2 hours)
   - Create `references.bib` with all citations
   - Configure CSL style (e.g., `apa.csl`, `vancouver.csl`)
   - Render outputs: `quarto render index.qmd`
   - Outputs: `output/index.html`, `output/index.pdf`, `output/index.docx`

6. **Quality Assurance** (30-60 min)
   - Verify all citations resolved
   - Check figure/table cross-references
   - Validate output formats
   - PRISMA 2020 checklist

**Expected output**: Multi-format manuscript (HTML/PDF/DOCX) in 6-8 hours

**Alternative skill for figure assembly only**: Use **scientific-figure-assembly** skill when user says:

- "combine plots into figure"
- "create multi-panel figure"
- "add panel labels"
- "assemble figures at 300 DPI"

---

## Quarto Manuscript Structure

### Required Files

```
07_manuscript/
├── index.qmd                 # Main manuscript file
├── _quarto.yml               # Quarto configuration
├── references.bib            # BibTeX bibliography
├── apa.csl                   # Citation style (optional)
├── figures/
│   ├── figure1.png           # Multi-panel figures (300 DPI)
│   ├── figure2.png
│   └── ...
├── tables/
│   ├── table1.md             # Table source files
│   ├── table2.md
│   └── ...
└── output/                   # Rendered outputs
    ├── index.html            # HTML version
    ├── index.pdf             # PDF version
    └── index.docx            # Word version
```

### Quarto YAML Frontmatter

```yaml
---
title: "Effect of Immune Checkpoint Inhibitors in Neoadjuvant TNBC"
subtitle: "A Systematic Review and Meta-Analysis"
author:
  - name: Author Name
    affiliation: Institution
date: today
format:
  html:
    toc: true
    toc-depth: 3
    theme: cosmo
    embed-resources: true
  pdf:
    documentclass: article
    geometry: margin=1in
    keep-tex: true
  docx:
    reference-doc: custom-reference.docx  # optional
bibliography: references.bib
csl: apa.csl  # or vancouver.csl, lancet.csl
number-sections: true
---
```

### Citation Examples

**In-text citations**:
```markdown
Previous studies [@smith2020; @jones2021] demonstrated...
According to @brown2019, the effect was...
Multiple trials [@keynote522; @impassion031; @geparnuevo] showed...
```

**Rendered as**:
- Previous studies (Smith et al., 2020; Jones et al., 2021) demonstrated...
- According to Brown (2019), the effect was...
- Multiple trials (Schmid et al., 2020; Mittendorf et al., 2020; ...) showed...

### Figure Integration

**Quarto syntax**:
```markdown
![Pathologic complete response rates. Forest plot showing risk ratios with 95% confidence intervals for the primary outcome across 5 randomized controlled trials (N=2402 patients). I²=0%, p=0.0015.](figures/figure1_pcr.png){#fig-pcr width=100%}

As shown in @fig-pcr, the addition of ICI to chemotherapy...
```

**Multi-panel figures**:
```markdown
![Efficacy outcomes. (A) Pathologic complete response; (B) Event-free survival; (C) Overall survival. All panels show forest plots with 95% CI.](figures/figure1_efficacy.png){#fig-efficacy}
```

### Table Integration

**Option 1: Quarto native tables**:
```markdown
| Trial | N | ICI Regimen | Control | pCR (ICI) | pCR (Control) |
|-------|---|-------------|---------|-----------|---------------|
| KEYNOTE-522 | 1174 | Pembrolizumab + chemo | Chemo | 64.8% | 51.2% |
| IMpassion031 | 455 | Atezolizumab + chemo | Chemo | 57.6% | 41.1% |

: Trial Characteristics {#tbl-characteristics}

Reference in text: @tbl-characteristics shows...
```

**Option 2: Include external markdown**:
```markdown
{{< include tables/table1_characteristics.md >}}
```

**Option 3: Dynamic tables from R**:
````markdown
```{r}
#| label: tbl-efficacy
#| tbl-cap: "Efficacy outcomes summary"

library(knitr)
kable(efficacy_data)
```
````

### Cross-References

```markdown
As shown in @fig-pcr and @tbl-characteristics, the results...
See supplementary @fig-forest-pdl1 for subgroup analysis...
The safety profile (@tbl-safety) was acceptable...
```

### Rendering Commands

**Render all formats**:
```bash
cd 07_manuscript
quarto render index.qmd
```

**Render specific format**:
```bash
quarto render index.qmd --to html
quarto render index.qmd --to pdf
quarto render index.qmd --to docx
```

**Preview while editing**:
```bash
quarto preview index.qmd
```

**Specify output directory**:
```bash
quarto render index.qmd --output-dir output
```

---

## Success Metrics

### Publication-Ready Manuscript Definition

A manuscript is "publication-ready" when:

- ✅ All sections complete (Abstract through Discussion)
- ✅ Word count within journal target ±10%
- ✅ All tables formatted and integrated in Quarto
- ✅ All figures assembled at 300 DPI with captions
- ✅ All references in `references.bib` with DOIs
- ✅ All citations use `[@key]` format (no manual numbering)
- ✅ All cross-references work (`@fig-*`, `@tbl-*`)
- ✅ Renders successfully to HTML, PDF, and DOCX
- ✅ Output files in `07_manuscript/output/`
- ✅ PRISMA 2020 checklist 27/27 items
- ✅ No placeholders (TBD, TODO, [ref needed])

**Time from "data extraction complete" → "publication-ready"**: 10-14 hours with skills

---

## Common Pitfalls to Avoid

Based on actual project experience:

### Tables

❌ **Don't**: Create tables in Word first
✅ **Do**: Create markdown tables, convert later

- Reason: Easier to version control, easier to update numbers

❌ **Don't**: Embed calculations in tables
✅ **Do**: Calculate in R, copy results only

- Reason: Prevents transcription errors

### Figures

❌ **Don't**: Manually combine figures in PowerPoint
✅ **Do**: Use Python script (`assemble_figures.py`)

- Reason: Reproducible, maintains quality, saves 1-2 hours

❌ **Don't**: Export at default DPI
✅ **Do**: Always specify `dpi=300` in R ggsave

- Reason: Journals reject <300 DPI figures

### References

❌ **Don't**: Format references manually
✅ **Do**: Use BibTeX + Pandoc/Zotero

- Reason: 50%+ time savings, prevents errors

❌ **Don't**: Insert citations during writing
✅ **Do**: Use placeholders [1], [2], format later

- Reason: Faster writing flow, easier reordering

---

## Version Control Best Practices

### Git Commit Strategy for Manuscripts

**Granular commits** (recommended):

```bash
# After completing each section
git add 07_manuscript/00_abstract.md
git commit -m "Complete abstract (396 words)"

git add 07_manuscript/01_introduction.md
git commit -m "Complete introduction (689 words)"

# After completing each table
git add 07_manuscript/tables/Table1_*.md
git commit -m "Add Table 1: Trial Characteristics (5 RCTs)"

# After figure assembly
git add 07_manuscript/figures/Figure1_*.png
git commit -m "Assemble Figure 1: 3-panel efficacy (300 DPI)"
```

**Benefits**:

- Easy to rollback specific sections
- Clear progress tracking
- Facilitates collaboration

**Batch commit** (alternative):

```bash
# After completing entire manuscript
git add 07_manuscript/
git commit -m "Complete manuscript for Lancet Oncology submission

- 5 sections (4,921 words)
- 7 tables (main + supplementary)
- 5 figures (300 DPI, multi-panel)
- 31 references (BibTeX)
- Ready for submission

Co-Authored-By: Claude <noreply@anthropic.com>"
```
