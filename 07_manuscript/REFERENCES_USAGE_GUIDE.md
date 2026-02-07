# References Usage Guide

## Quick Start

✅ **BibTeX file created**: `references.bib` (31 entries)
✅ **Citation mapping**: See `CITATION_MAPPING.md` for superscript → BibTeX key mapping

---

## Converting Manuscript to Submission-Ready Format

### Option 1: Using Pandoc (Recommended)

#### Step 1: Download Lancet CSL Style

```bash
cd /Users/htlin/meta-pipe/07_manuscript
wget https://www.zotero.org/styles/the-lancet -O lancet.csl
```

#### Step 2: Convert Markdown to Word

```bash
# Combine all sections into single markdown file
cat 00_abstract.md 01_introduction.md 02_methods.md 03_results.md 04_discussion.md > manuscript_full.md

# Convert to Word with citations
pandoc manuscript_full.md \
  --bibliography=references.bib \
  --csl=lancet.csl \
  --reference-doc=lancet_template.docx \
  -o manuscript_lancet.docx
```

#### Step 3: Manual Cleanup

- Insert tables (from `tables/` folder)
- Insert figures (from `06_analysis/figures/` or assembled multi-panel figures)
- Verify citation numbers are sequential
- Add cover letter

---

### Option 2: Using Zotero (GUI Method)

#### Step 1: Import BibTeX to Zotero

1. Open Zotero
2. File → Import → Select `references.bib`
3. Create collection "TNBC Meta-Analysis"

#### Step 2: Use Word Plugin

1. Open Word
2. Zotero → Set Document Preferences → Style: "The Lancet"
3. Manually copy manuscript text into Word
4. Use Zotero "Add/Edit Citation" for each reference
5. Zotero → Refresh to generate bibliography

---

### Option 3: Manual Reference Formatting (Lancet Style)

**Lancet reference format**:

```
1. Dent R, Trudeau M, Pritchard KI, et al. Triple-negative breast cancer: clinical features and patterns of recurrence. Clin Cancer Res 2007; 13: 4429–34.
```

**Key formatting rules**:

- Author names: Surname + initials (no periods after initials)
- Use "et al" if >6 authors
- Journal abbreviation: standard Index Medicus abbreviations
- Year; volume: pages
- DOI at end (optional for Lancet)

---

## Citation Examples in Text

### Current Format (Manuscript Markdown)

```markdown
TNBC accounts for approximately 15–20% of all breast cancers.¹
```

### Lancet Oncology Format

```
TNBC accounts for approximately 15–20% of all breast cancers.1
```

### Multiple Citations

**Current**: "pCR is a validated surrogate endpoint.⁵⁻⁷"
**Lancet**: "pCR is a validated surrogate endpoint.5-7"

### Combined with Text

**Current**: "Schmid and colleagues¹⁷ reported..."
**Lancet**: "Schmid and colleagues17 reported..."

---

## Formatted Reference Examples

### Journal Article (Standard)

```
1. Dent R, Trudeau M, Pritchard KI, et al. Triple-negative breast cancer: clinical features and patterns of recurrence. Clin Cancer Res 2007; 13: 4429–34.
```

### Journal Article (>6 Authors)

```
5. Cortazar P, Zhang L, Untch M, et al. Pathological complete response and long-term clinical benefit in breast cancer: the CTNeoBC pooled analysis. Lancet 2014; 384: 164–72.
```

### Guideline/Report

```
9. U.S. Food and Drug Administration. Pathologic complete response in neoadjuvant treatment of high-risk early-stage breast cancer: use as an endpoint to support accelerated approval. Guidance for Industry. 2020. https://www.fda.gov/regulatory-information/search-fda-guidance-documents/pathologic-complete-response-neoadjuvant-treatment-high-risk-early-stage-breast-cancer-use-endpoint (accessed Feb 7, 2026).
```

### Software/R Package

```
29. Schwarzer G. meta: general package for meta-analysis. R package version 8.2-1. https://CRAN.R-project.org/package=meta (accessed Feb 7, 2026).
```

---

## Full Formatted Reference List (Lancet Style)

```
1. Dent R, Trudeau M, Pritchard KI, et al. Triple-negative breast cancer: clinical features and patterns of recurrence. Clin Cancer Res 2007; 13: 4429–34.

2. Foulkes WD, Smith IE, Reis-Filho JS. Triple-negative breast cancer. N Engl J Med 2010; 363: 1938–48.

3. Bianchini G, Balko JM, Mayer IA, Sanders ME, Gianni L. Triple-negative breast cancer: challenges and opportunities of a heterogeneous disease. Nat Rev Clin Oncol 2016; 13: 674–90.

4. Mieog JSD, van der Hage JA, van de Velde CJH. Preoperative chemotherapy for women with operable breast cancer. Cochrane Database Syst Rev 2007; (2): CD005002.

5. Cortazar P, Zhang L, Untch M, et al. Pathological complete response and long-term clinical benefit in breast cancer: the CTNeoBC pooled analysis. Lancet 2014; 384: 164–72.

6. Spring LM, Fell G, Arfe A, et al. Pathologic complete response after neoadjuvant chemotherapy and impact on breast cancer recurrence and survival: a comprehensive meta-analysis. Clin Cancer Res 2020; 26: 2838–48.

7. von Minckwitz G, Untch M, Blohmer JU, et al. Definition and impact of pathologic complete response on prognosis after neoadjuvant chemotherapy in various intrinsic breast cancer subtypes. J Clin Oncol 2012; 30: 1796–804.

8. Symmans WF, Wei C, Gould R, et al. Long-term prognostic risk after neoadjuvant chemotherapy associated with residual cancer burden and breast cancer subtype. J Clin Oncol 2017; 35: 1049–60.

9. U.S. Food and Drug Administration. Pathologic complete response in neoadjuvant treatment of high-risk early-stage breast cancer: use as an endpoint to support accelerated approval. Guidance for Industry. 2020.

10. Adams S, Gray RJ, Demaria S, et al. Prognostic value of tumor-infiltrating lymphocytes in triple-negative breast cancers from two phase III randomized adjuvant breast cancer trials: ECOG 2197 and ECOG 1199. J Clin Oncol 2014; 32: 2959–66.

11. Mittendorf EA, Philips AV, Meric-Bernstam F, et al. PD-L1 expression in triple-negative breast cancer. Cancer Immunol Res 2014; 2: 361–70.

12. Safonov A, Jiang T, Bianchini G, et al. Immune gene expression is associated with genomic aberrations in breast cancer. Cancer Res 2017; 77: 3317–24.

13. Schmid P, Adams S, Rugo HS, et al. Atezolizumab and nab-paclitaxel in advanced triple-negative breast cancer. N Engl J Med 2018; 379: 2108–21.

14. Cortes J, Cescon DW, Rugo HS, et al. Pembrolizumab plus chemotherapy versus placebo plus chemotherapy for previously untreated locally recurrent inoperable or metastatic triple-negative breast cancer (KEYNOTE-355): a randomised, placebo-controlled, double-blind, phase 3 clinical trial. Lancet 2020; 396: 1817–28.

15. Miles D, Gligorov J, André F, et al. Primary results from IMpassion131, a double-blind, placebo-controlled, randomised phase III trial of first-line paclitaxel with or without atezolizumab for unresectable locally advanced or metastatic triple-negative breast cancer. Ann Oncol 2021; 32: 994–1004.

16. Kwa MJ, Adams S. Checkpoint inhibitors in triple-negative breast cancer (TNBC): where to go from here. Cancer 2018; 124: 2086–103.

17. Schmid P, Cortes J, Dent R, et al. Event-free survival with pembrolizumab in early triple-negative breast cancer. N Engl J Med 2022; 386: 556–67. [Updated: Schmid P, et al. N Engl J Med 2024; 391: 515–25.]

18. Mittendorf EA, Zhang H, Barrios CH, et al. Neoadjuvant atezolizumab in combination with sequential nab-paclitaxel and anthracycline-based chemotherapy versus placebo and chemotherapy in patients with early-stage triple-negative breast cancer (IMpassion031): a randomised, double-blind, phase 3 trial. Lancet 2020; 396: 1090–100.

19. Loibl S, Untch M, Burchardi N, et al. A randomised phase II study investigating durvalumab in addition to an anthracycline taxane-based neoadjuvant therapy in early triple-negative breast cancer: clinical results and biomarker analysis of GeparNuevo study. Ann Oncol 2019; 30: 1279–88. [Updated: Loibl S, et al. Ann Oncol 2022; 33: 382–90.]

20. Gianni L, Huang CS, Egle D, et al. Pathologic complete response (pCR) to neoadjuvant treatment with or without atezolizumab in triple-negative, early high-risk and locally advanced breast cancer: NeoTRIP Michelangelo randomized study. Ann Oncol 2022; 33: 534–43.

21. Chen X, Qin Y, Li H, et al. Neoadjuvant camrelizumab plus chemotherapy versus chemotherapy alone for early triple-negative breast cancer (CamRelief): a multicentre, randomised, double-blind, phase 3 trial. Lancet 2024; 403: 2371–83.

22. Postow MA, Sidlow R, Hellmann MD. Immune-related adverse events associated with immune checkpoint blockade. N Engl J Med 2018; 378: 158–68.

23. Page MJ, McKenzie JE, Bossuyt PM, et al. The PRISMA 2020 statement: an updated guideline for reporting systematic reviews. BMJ 2021; 372: n71.

24. Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. BMJ 2019; 366: l4898.

25. Hartung J, Knapp G. A refined method for the meta-analysis of controlled clinical trials with binary outcome. Stat Med 2001; 20: 3875–89.

26. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. BMJ 2003; 327: 557–60.

27. Viechtbauer W, Cheung MW. Outlier and influence diagnostics for meta-analysis. Res Synth Methods 2010; 1: 112–25.

28. Sterne JAC, Sutton AJ, Ioannidis JPA, et al. Recommendations for examining and interpreting funnel plot asymmetry in meta-analyses of randomised controlled trials. BMJ 2011; 343: d4002.

29. Schwarzer G. meta: general package for meta-analysis. R package version 8.2-1. https://CRAN.R-project.org/package=meta (accessed Feb 7, 2026).

30. Viechtbauer W. Conducting meta-analyses in R with the metafor package. J Stat Softw 2010; 36: 1–48.

31. Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. BMJ 2008; 336: 924–6.
```

---

## Verification Checklist

Before submission, verify:

- [ ] All 31 citations appear in order of first mention
- [ ] No citation numbers are skipped
- [ ] All BibTeX keys have matching references
- [ ] All DOIs are valid and resolve correctly
- [ ] Journal abbreviations follow Index Medicus standards
- [ ] Author names are formatted consistently
- [ ] Page ranges use en-dash (–) not hyphen (-)
- [ ] Volume/issue/page format matches journal style
- [ ] URLs work and include access dates
- [ ] Primary trial references (17-21) are most recent publications

---

## Common Issues and Fixes

### Issue 1: Superscripts not converting properly

**Fix**: Use find-and-replace to convert Unicode superscripts (¹²³) to regular numbers (1,2,3)

### Issue 2: Citation order doesn't match reference list

**Fix**: Use Pandoc or Zotero to auto-generate numbered references in order of appearance

### Issue 3: Journal abbreviations inconsistent

**Fix**: Use Index Medicus abbreviations from PubMed

- Example: "New England Journal of Medicine" → "N Engl J Med"
- Example: "Journal of Clinical Oncology" → "J Clin Oncol"

### Issue 4: Page ranges using wrong dash

**Fix**: Use en-dash (–) not hyphen (-)

- Correct: 2838–48
- Incorrect: 2838-48

---

## Next Steps

1. ✅ BibTeX file created (`references.bib`)
2. ✅ Citation mapping documented (`CITATION_MAPPING.md`)
3. ⏳ Convert to journal format (use Pandoc or Zotero)
4. ⏳ Insert tables and figures
5. ⏳ Write cover letter
6. ⏳ Complete submission checklist

---

**Status**: References phase complete. Ready for journal formatting and figure assembly.

**Estimated time for formatting**: 1-2 hours
