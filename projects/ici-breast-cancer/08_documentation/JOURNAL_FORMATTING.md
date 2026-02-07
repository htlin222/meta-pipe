# Journal-Specific Formatting Guide

**Reference**: This file is referenced from CLAUDE.md
**Purpose**: Target journal requirements for meta-analyses

---

## Priority Targets for Meta-Analysis

### 1. Lancet Oncology (IF ~50) ⭐ RECOMMENDED

**Why recommended**: Most generous word limit, well-suited for meta-analyses

- **Abstract**: 250-400 words
- **Main text**: 3,500-5,000 words
- **References**: Maximum 40
- **Figures**: Maximum 6
- **Tables**: Maximum 5

**Submission requirements**:

- Structured abstract (Background, Methods, Findings, Interpretation)
- PRISMA 2020 checklist mandatory
- PRISMA flow diagram required
- Trial registration number (PROSPERO)
- Data sharing statement required

---

### 2. JAMA Oncology (IF ~33)

- **Abstract**: 350 words (structured)
- **Main text**: 3,500 words
- **References**: Maximum 50
- **Figures**: Maximum 5
- **Tables**: Maximum 4

**Submission requirements**:

- Structured abstract (Importance, Objective, Data Sources, Study Selection, Data Extraction and Synthesis, Main Outcomes and Measures, Results, Conclusions and Relevance)
- PRISMA checklist mandatory
- Trial registration required
- Statistical analysis plan preferred

---

### 3. Nature Medicine (IF ~82)

- **Abstract**: 150-200 words (unstructured)
- **Main text**: 3,000 words
- **References**: Maximum 50
- **Figures**: Maximum 6
- **Emphasis**: Clinical impact, translational relevance

**Submission requirements**:

- Brief abstract (no subheadings)
- Extended Data figures allowed (beyond 6 main figures)
- Data deposition required
- High bar for novelty and clinical impact

---

## Format Compliance Checklist

Use this before submission:

- [ ] Word count within ±10% of target
- [ ] Abstract follows journal structure
- [ ] Figure count ≤ maximum
- [ ] Table count ≤ maximum
- [ ] Reference count ≤ maximum
- [ ] All figures at 300+ DPI
- [ ] PRISMA checklist complete (27/27)
- [ ] Trial registration number included
- [ ] Conflicts of interest disclosed
- [ ] Author contributions statement
- [ ] Data availability statement

---

## Quick Format Converter

If journal rejects, use these commands to reformat:

```bash
# Reduce word count by 10%
# (Manual editing required - focus on Discussion section)

# Convert abstract structure
# Lancet → JAMA: Add "Importance" section
# JAMA → Lancet: Merge into Background/Methods/Findings/Interpretation
# Nature Medicine: Remove all subheadings, condense to 150-200 words

# Reduce figures (if needed)
# Move main figures to supplementary
# Priority: Keep efficacy > safety > bias assessment

# Reduce references (if needed)
# Remove older references (pre-2015)
# Keep only primary sources and recent guidelines
```

---

## Typical Manuscript Metrics

Based on completed TNBC meta-analysis:

- **Word count**: 4,921 words
  - Abstract: 396 words
  - Introduction: 689 words
  - Methods: 1,141 words
  - Results: 1,247 words
  - Discussion: 1,448 words

- **Figures**: 5 main + 2 supplementary
- **Tables**: 3 main + 4 supplementary
- **References**: 31 citations

**Status**: ✅ Compliant with Lancet Oncology, ✅ JAMA Oncology
**Issue**: ❌ Over word limit for Nature Medicine (4,921 vs 3,000)
