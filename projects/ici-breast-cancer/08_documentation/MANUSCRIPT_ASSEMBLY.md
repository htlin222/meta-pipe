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

1. **Tables Creation** (2-3 hours)
   - Main text tables (Trial Characteristics, Efficacy, Safety)
   - Supplementary tables (RoB 2, GRADE, detailed results)

2. **Figure Assembly** (1-2 hours)
   - Use Python PIL/Pillow for multi-panel figures
   - Add professional panel labels (A, B, C)
   - Maintain 300 DPI publication quality

3. **References Management** (1-2 hours)
   - Create BibTeX file from citations
   - Map superscripts to BibTeX keys
   - Provide Pandoc/Zotero usage guide

4. **Figure Legends** (30-60 min)
   - Comprehensive figure descriptions
   - Statistical details included
   - Journal-specific formatting

5. **Quality Assurance** (30-60 min)
   - PRISMA 2020 checklist
   - Journal submission requirements
   - Cross-reference validation

**Expected output**: Complete submission-ready package in 6-8 hours

**Alternative skill for figure assembly only**: Use **scientific-figure-assembly** skill when user says:

- "combine plots into figure"
- "create multi-panel figure"
- "add panel labels"
- "assemble figures at 300 DPI"

---

## Success Metrics

### Publication-Ready Manuscript Definition

A manuscript is "publication-ready" when:

- ✅ All sections complete (Abstract through Discussion)
- ✅ Word count within journal target ±10%
- ✅ All tables formatted (main + supplementary)
- ✅ All figures assembled at 300 DPI with legends
- ✅ All references in BibTeX with DOIs
- ✅ PRISMA 2020 checklist 27/27 items
- ✅ No placeholders (TBD, TODO, [ref needed])
- ✅ Citation mapping document exists
- ✅ Submission checklist complete

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
