# Rayyan Setup Guide

## TNBC Neoadjuvant Immunotherapy Meta-Analysis Screening

**Purpose**: Set up Rayyan for dual independent title/abstract screening
**Time**: 30 minutes
**Date**: 2026-02-07

---

## Step 1: Create Rayyan Account

1. Go to https://www.rayyan.ai/
2. Click "Sign Up Free"
3. Choose "Academic/Researcher" account type
4. Verify email address
5. Complete profile:
   - Affiliation: [Your institution]
   - ORCID ID: [If available]
   - Research interests: Systematic reviews, Oncology, Breast cancer

---

## Step 2: Create New Review

1. Click "New Review" from dashboard
2. Fill in review details:

   **Review Title**: Early TNBC Neoadjuvant Immunotherapy: Systematic Review and Meta-Analysis

   **Description**: Systematic review of randomized controlled trials comparing immune checkpoint inhibitors + chemotherapy vs chemotherapy alone in neoadjuvant treatment of early or locally advanced triple-negative breast cancer (TNBC). Primary outcome: pathologic complete response (pCR).

   **Review Type**: Systematic Review

   **PROSPERO ID**: CRD42026XXXXX (add after registration)

   **Keywords**: TNBC, triple-negative breast cancer, neoadjuvant, immunotherapy, checkpoint inhibitors, pembrolizumab, atezolizumab, pCR

3. Click "Create Review"

---

## Step 3: Configure Screening Settings

### 3.1 Inclusion/Exclusion Criteria

Click "Settings" → "Inclusion/Exclusion Criteria" and add:

**Inclusion Criteria:**

1. Randomized controlled trial (Phase I/II, II, or III)
2. Adults (≥18 years) with early or locally advanced TNBC
3. Neoadjuvant setting (pre-surgery treatment)
4. Intervention: ICI + chemotherapy vs chemotherapy alone
5. Reports pCR, EFS, OS, or safety outcomes
6. Minimum 20 patients per arm

**Exclusion Criteria:**

1. Not a randomized controlled trial (observational, single-arm)
2. Metastatic breast cancer (Stage IV)
3. Non-TNBC or mixed subtypes (unless TNBC subgroup reported)
4. Adjuvant or metastatic setting only
5. No control arm (single-arm trials)
6. Conference abstracts if full publication available
7. Non-human studies
8. Reviews, editorials, commentaries

### 3.2 Blinding Settings

1. Enable **Blind Mode**: Yes
   - Reviewers cannot see each other's decisions until conflicts are resolved
   - Reduces bias

2. Enable **Hide Author Names**: Optional
   - Hides author/journal information during screening
   - Recommended for unbiased screening

---

## Step 4: Upload References

### Option A: Import from BibTeX (Recommended)

1. Go to your review
2. Click "Import"
3. Select "BibTeX" format
4. Upload `02_search/round-01/dedupe.bib`
5. Review import summary
6. Click "Confirm Import"

### Option B: Import from RIS

1. Convert BibTeX to RIS first (if needed)
2. Upload RIS file

### Option C: Direct PubMed Import

1. Click "Import" → "PubMed"
2. Enter PMIDs (comma-separated)
3. Import

**Expected**: ~150-180 records imported

---

## Step 5: Invite Co-Reviewer

1. Click "Team" → "Invite Members"
2. Enter co-reviewer email address
3. Assign role: **Reviewer** (not Owner)
4. Add custom message:

   > Hi [Name],
   >
   > I've invited you to collaborate on our TNBC neoadjuvant immunotherapy systematic review. We'll be screening ~150-180 title/abstracts independently.
   >
   > Please use the inclusion/exclusion criteria in the "Criteria" tab. Mark each reference as:
   >
   > - **Include**: Clearly meets all criteria
   > - **Maybe**: Uncertain, needs full text
   > - **Exclude**: Select reason from dropdown
   >
   > Let's aim to complete screening within 2 weeks.
   >
   > Thanks!

5. Click "Send Invitation"

---

## Step 6: Configure Decision Labels

1. Go to "Settings" → "Labels"
2. Create custom labels (optional):

   **Primary Decision:**
   - Include (green)
   - Maybe (yellow)
   - Exclude (red)

   **Exclusion Reasons:**
   - Wrong population (not TNBC)
   - Wrong intervention (no ICI, or not neoadjuvant)
   - Wrong comparator (no control arm)
   - Wrong study design (not RCT)
   - Wrong setting (metastatic, adjuvant only)
   - Duplicate (already included)
   - Wrong publication type (review, editorial)

3. Save labels

---

## Step 7: Create Screening Instructions Document

Save this in Rayyan "Notes" section:

```markdown
# SCREENING INSTRUCTIONS

## Process

1. Read title and abstract carefully
2. Apply inclusion/exclusion criteria
3. When in doubt, mark as "Maybe" (proceed to full text)
4. Select exclusion reason if excluding

## Quick Decision Tree

### Is it a randomized trial?

- No → Exclude (Wrong study design)
- Unclear → Maybe

### Is it neoadjuvant TNBC?

- No (metastatic) → Exclude (Wrong setting)
- No (other breast cancer subtype) → Exclude (Wrong population)
- Mixed subtypes but TNBC subgroup reported → Include
- Unclear → Maybe

### Does it compare ICI+chemo vs chemo?

- No (single arm) → Exclude (Wrong comparator)
- No (ICI+chemo vs ICI alone) → Exclude (Wrong comparator)
- Yes → Include (if other criteria met)
- Unclear → Maybe

### Does it report relevant outcomes?

- Reports pCR, EFS, OS, or AEs → Include
- No outcomes reported (protocol only) → Exclude (unless updated analysis expected)
- Unclear → Maybe

## Known Key Trials (should be INCLUDED):

- KEYNOTE-522 (Schmid et al.)
- IMpassion031 (Mittendorf et al.)
- GeparNuevo (Loibl et al.)
- NeoTRIPaPDL1 (Gianni et al.)
- CamRelief (Huang et al.)
- NeoPACT (Pusztai et al.)

If you accidentally exclude one of these, please review!

## Edge Cases

- Conference abstract + full publication: Include full publication only (exclude abstract as duplicate)
- Multiple follow-up reports: Include most recent/comprehensive
- Post-hoc analyses: Include if report new outcomes or subgroups
```

---

## Step 8: Test Run

Before full screening:

1. Screen 10 pilot references together (same room or video call)
2. Discuss discrepancies
3. Clarify borderline cases
4. Refine criteria if needed
5. Document any protocol amendments

---

## Step 9: Start Independent Screening

1. **Reviewer 1 (you)**: Screen independently
2. **Reviewer 2 (co-reviewer)**: Screen independently
3. **Do NOT discuss** decisions until both complete
4. **Target pace**: 20-30 records per hour
5. **Expected time**: 6-8 hours per reviewer

### Screening Tips:

- Block out dedicated time (don't multitask)
- Take breaks every 45-60 minutes
- If fatigued, stop and resume later (fatigue reduces accuracy)
- Use keyboard shortcuts (I = Include, M = Maybe, E = Exclude)

---

## Step 10: Resolve Conflicts

After both reviewers complete screening:

1. Click "Conflicts" tab to see disagreements
2. Schedule 2-hour conflict resolution meeting
3. Review each conflict:
   - Re-read title/abstract together
   - Discuss reasoning
   - Reach consensus
4. Document any patterns (e.g., "we disagreed on phase I/II trials → decided to include if ≥20 patients per arm")
5. Calculate Cohen's kappa (Rayyan shows this automatically)

**Target kappa**: ≥0.60 (moderate agreement)

If kappa <0.60:

- Review inclusion/exclusion criteria
- Identify sources of disagreement
- Consider additional pilot screening
- Document reasons and how resolved

---

## Step 11: Export Results

After conflict resolution:

1. Click "Export"
2. Select format: **CSV** (for use with pipeline scripts)
3. Include fields:
   - Title
   - Authors
   - Year
   - Journal
   - Abstract
   - DOI
   - PMID
   - Decision (Reviewer 1)
   - Decision (Reviewer 2)
   - Final Decision
   - Exclusion Reason
   - Notes
4. Save as `03_screening/round-01/rayyan_export.csv`

---

## Step 12: Update Pipeline CSV

After export from Rayyan:

```bash
cd /Users/htlin/meta-pipe/tooling/python

# Merge Rayyan decisions into pipeline CSV
uv run merge_rayyan_decisions.py \
  --rayyan-csv ../../03_screening/round-01/rayyan_export.csv \
  --pipeline-csv ../../03_screening/round-01/decisions.csv \
  --out-csv ../../03_screening/round-01/decisions_screened.csv
```

---

## Keyboard Shortcuts (Rayyan Desktop/Web)

- **I** or **↑**: Include
- **M** or **→**: Maybe
- **E** or **↓**: Exclude
- **U**: Undo decision
- **N**: Next reference
- **P**: Previous reference
- **F**: Add to favorites (flag for discussion)
- **Ctrl+F**: Search

---

## Quality Checks

Before moving to full-text stage:

- [ ] All ~150-180 references have decisions from both reviewers
- [ ] All conflicts resolved
- [ ] Cohen's kappa ≥0.60
- [ ] Expected inclusions: 15-25 studies
- [ ] Known key trials (KEYNOTE-522, IMpassion031, GeparNuevo) are INCLUDED
- [ ] Export CSV saved and backed up
- [ ] PRISMA flow diagram numbers ready:
  - Records identified
  - Records after deduplication
  - Records screened
  - Records excluded (with reasons)
  - Full texts to retrieve

---

## Troubleshooting

### Issue: Rayyan won't import BibTeX

- **Solution**: Check BibTeX syntax, remove special characters, or use RIS format

### Issue: Co-reviewer can't access review

- **Solution**: Check email spelling, resend invitation, verify they created account

### Issue: Blind mode not working

- **Solution**: Ensure both reviewers have "Reviewer" role (not "Owner"), refresh page

### Issue: Export missing fields

- **Solution**: Check "Include all fields" in export options, use CSV format

### Issue: Many "Maybe" decisions

- **Solution**: Normal for uncertain abstracts - all proceed to full text. If >50%, criteria may be too vague - discuss and clarify.

---

## Timeline

- **Setup**: 30 minutes (today)
- **Pilot screening**: 1 hour (10 references together)
- **Independent screening**: 6-8 hours per reviewer (over 1-2 weeks)
- **Conflict resolution**: 2-3 hours (together)
- **Export and QA**: 30 minutes

**Total**: ~18-24 person-hours (9-12 hours per reviewer)

---

## Resources

- Rayyan Help Center: https://help.rayyan.ai/
- Rayyan Tutorial Videos: https://www.rayyan.ai/tutorials
- PRISMA Screening Guidelines: http://www.prisma-statement.org/

---

**Version**: 1.0
**Date**: 2026-02-07
**Next update**: After pilot screening (add any clarifications)
