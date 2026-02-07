# Time Investment Guidance

**Reference**: This file is referenced from CLAUDE.md
**Purpose**: Set realistic expectations for meta-analysis timeline

---

## Typical Meta-Analysis Timeline

Based on actual completion (N=2402 patients, 5 RCTs):

| Phase     | Task                    | Time Investment |
| --------- | ----------------------- | --------------- |
| 01        | Protocol & PICO         | 1-2 hours       |
| 02        | Literature Search       | 2-3 hours       |
| 03        | Screening               | 3-4 hours       |
| 04        | Fulltext Retrieval      | 2-4 hours       |
| 05        | Data Extraction         | 4-6 hours\*     |
| 06        | Meta-Analysis           | 4-5 hours       |
| **07**    | **Manuscript Assembly** | **6-8 hours**   |
| **Total** | **End-to-end**          | **22-32 hours** |

\*With LLM assistance: 2-3 hours (65% time savings)

**Critical path**: Stages 05-07 (analysis → manuscript) can be completed in **10-14 hours**

---

## Efficiency Tips

### From Recent Project Experience

1. **Use skills proactively**
   - Don't wait for user to ask - invoke `/meta-manuscript-assembly` when Stage 06 complete
   - Suggest figure assembly when individual PNGs are generated

2. **Batch figure creation**
   - Create all 9+ individual plots first
   - Then assemble all multi-panel figures in one session
   - Saves context switching

3. **References workflow**
   - Extract citations AFTER manuscript text complete
   - Use BibTeX format from the start
   - Map citations once (superscripts → keys)

4. **Validation timing**
   - Run PRISMA checklist BEFORE creating tables
   - Ensures no missing data points
   - Prevents rework

5. **Version control**
   - Commit after each major section (Tables → Figures → References)
   - Enables rollback if journal requires different format

---

## AI-Assisted Workflow Optimization

### When to Use Claude Skills vs Manual Work

**Use skills** (60-80% time savings):

- Manuscript structure creation
- Table template generation
- Figure assembly automation
- Reference management
- PRISMA checklist filling

**Do manually** (requires domain expertise):

- Clinical interpretation
- Discussion points selection
- Figure legend scientific details
- Author contribution statements
- Conflict of interest disclosures

### LLM-Assisted Data Extraction

**Prerequisite**: Claude CLI or similar LLM with PDF processing

**Workflow** (Stage 05):

1. Extract PDF text: `extract_pdf_text.py`
2. LLM extraction: `llm_extract_cli.py --cli claude`
3. Manual review: Edit extraction.csv
4. Validation: `validate_extraction.py`

**Results**:

- 100% success rate (all PDFs processed)
- 65-70% time savings vs manual
- Some fields need manual correction
- Cost: ~$0-5 per meta-analysis
