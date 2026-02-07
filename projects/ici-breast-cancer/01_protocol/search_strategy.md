# Search Strategy

## Early TNBC Neoadjuvant Immunotherapy Meta-Analysis

**Date**: 2026-02-07
**Version**: 1.0
**Based on**: pico.yaml v1.0

---

## Search Overview

**Objective**: Identify all randomized controlled trials evaluating immune checkpoint inhibitors plus neoadjuvant chemotherapy versus chemotherapy alone in early or locally advanced triple-negative breast cancer.

**Databases**: PubMed/MEDLINE, Embase, Cochrane CENTRAL, ClinicalTrials.gov, conference abstracts
**Date range**: 2015-01-01 to present (2026-02-07)
**Language**: No restrictions

---

## PubMed/MEDLINE Search Strategy

### Search Date

2026-02-07

### Search Components

#### Population: Triple-Negative Breast Cancer

```
("triple negative breast"[Title/Abstract] OR
 "triple-negative breast"[Title/Abstract] OR
 "triple negative breast neoplasm"[Title/Abstract] OR
 "TNBC"[Title/Abstract] OR
 ("breast neoplasms"[MeSH Terms] AND
  "ER negative"[Title/Abstract] AND
  "PR negative"[Title/Abstract] AND
  "HER2 negative"[Title/Abstract]))
```

#### Intervention: Immune Checkpoint Inhibitors

```
("immune checkpoint inhibitor"[Title/Abstract] OR
 "immune checkpoint inhibitors"[MeSH Terms] OR
 "immunotherapy"[Title/Abstract] OR
 "immunotherapy"[MeSH Terms] OR
 "PD-1 inhibitor"[Title/Abstract] OR
 "PD-L1 inhibitor"[Title/Abstract] OR
 "PD-1 blockade"[Title/Abstract] OR
 "PD-L1 blockade"[Title/Abstract] OR
 "programmed death-1"[Title/Abstract] OR
 "programmed death-ligand 1"[Title/Abstract] OR
 "pembrolizumab"[Title/Abstract] OR
 "pembrolizumab"[Supplementary Concept] OR
 "atezolizumab"[Title/Abstract] OR
 "atezolizumab"[Supplementary Concept] OR
 "durvalumab"[Title/Abstract] OR
 "durvalumab"[Supplementary Concept] OR
 "nivolumab"[Title/Abstract] OR
 "nivolumab"[Supplementary Concept] OR
 "camrelizumab"[Title/Abstract] OR
 "avelumab"[Title/Abstract] OR
 "cemiplimab"[Title/Abstract])
```

#### Setting: Neoadjuvant/Preoperative

```
("neoadjuvant"[Title/Abstract] OR
 "neoadjuvant therapy"[MeSH Terms] OR
 "preoperative"[Title/Abstract] OR
 "pre-operative"[Title/Abstract] OR
 "presurgical"[Title/Abstract] OR
 "pre-surgical"[Title/Abstract] OR
 "primary systemic"[Title/Abstract])
```

#### Study Design: Randomized Controlled Trials

```
("randomized controlled trial"[Publication Type] OR
 "randomized"[Title/Abstract] OR
 "randomised"[Title/Abstract] OR
 "randomly"[Title/Abstract] OR
 "random allocation"[MeSH Terms] OR
 "clinical trial"[Publication Type] OR
 "RCT"[Title/Abstract])
```

### Combined PubMed Search Query

```
(("triple negative breast"[Title/Abstract] OR
  "triple-negative breast"[Title/Abstract] OR
  "triple negative breast neoplasm"[Title/Abstract] OR
  "TNBC"[Title/Abstract] OR
  ("breast neoplasms"[MeSH Terms] AND
   "ER negative"[Title/Abstract] AND
   "PR negative"[Title/Abstract] AND
   "HER2 negative"[Title/Abstract]))
 AND
 ("immune checkpoint inhibitor"[Title/Abstract] OR
  "immune checkpoint inhibitors"[MeSH Terms] OR
  "immunotherapy"[Title/Abstract] OR
  "immunotherapy"[MeSH Terms] OR
  "PD-1 inhibitor"[Title/Abstract] OR
  "PD-L1 inhibitor"[Title/Abstract] OR
  "PD-1 blockade"[Title/Abstract] OR
  "PD-L1 blockade"[Title/Abstract] OR
  "programmed death-1"[Title/Abstract] OR
  "programmed death-ligand 1"[Title/Abstract] OR
  "pembrolizumab"[Title/Abstract] OR
  "atezolizumab"[Title/Abstract] OR
  "durvalumab"[Title/Abstract] OR
  "nivolumab"[Title/Abstract] OR
  "camrelizumab"[Title/Abstract] OR
  "avelumab"[Title/Abstract] OR
  "cemiplimab"[Title/Abstract])
 AND
 ("neoadjuvant"[Title/Abstract] OR
  "neoadjuvant therapy"[MeSH Terms] OR
  "preoperative"[Title/Abstract] OR
  "pre-operative"[Title/Abstract] OR
  "presurgical"[Title/Abstract] OR
  "pre-surgical"[Title/Abstract] OR
  "primary systemic"[Title/Abstract])
 AND
 ("randomized controlled trial"[Publication Type] OR
  "randomized"[Title/Abstract] OR
  "randomised"[Title/Abstract] OR
  "randomly"[Title/Abstract] OR
  "random allocation"[MeSH Terms] OR
  "clinical trial"[Publication Type] OR
  "RCT"[Title/Abstract])
 AND
 ("2015/01/01"[Date - Publication] : "2026/12/31"[Date - Publication]))
```

### Expected Results

Approximately 95-120 records

---

## Embase Search Strategy (Ovid Syntax)

### Search Components

```
1. exp *triple negative breast cancer/
2. (triple negative breast or triple-negative breast or TNBC).ti,ab.
3. (breast cancer/ and (ER negative or PR negative or HER2 negative).ti,ab.)
4. 1 or 2 or 3

5. exp *immune checkpoint inhibitor/
6. exp *immunotherapy/
7. (immune checkpoint inhibitor* or immunotherap* or PD-1 inhibitor* or PD-L1 inhibitor*).ti,ab.
8. (pembrolizumab or atezolizumab or durvalumab or nivolumab or camrelizumab or avelumab or cemiplimab).ti,ab,tn.
9. (PD-1 blockade or PD-L1 blockade or programmed death-1 or programmed death-ligand 1).ti,ab.
10. 5 or 6 or 7 or 8 or 9

11. exp *neoadjuvant therapy/
12. (neoadjuvant or preoperative or pre-operative or presurgical or pre-surgical or primary systemic).ti,ab.
13. 11 or 12

14. exp *randomized controlled trial/
15. (randomized or randomised or randomly or random allocation).ti,ab.
16. (clinical trial or RCT).ti,ab.
17. 14 or 15 or 16

18. 4 and 10 and 13 and 17
19. limit 18 to yr="2015 -Current"
20. limit 19 to (human and (english or chinese or japanese or korean or spanish or french or german))
```

### Expected Results

Approximately 120-150 records

---

## Cochrane CENTRAL Search Strategy

### Search in Cochrane Library

```
#1 MeSH descriptor: [Triple Negative Breast Neoplasms] explode all trees
#2 (triple negative breast or triple-negative breast or TNBC):ti,ab,kw
#3 #1 or #2

#4 MeSH descriptor: [Immune Checkpoint Inhibitors] explode all trees
#5 MeSH descriptor: [Immunotherapy] explode all trees
#6 (immune checkpoint inhibitor* or immunotherap* or PD-1 inhibitor* or PD-L1 inhibitor*):ti,ab,kw
#7 (pembrolizumab or atezolizumab or durvalumab or nivolumab or camrelizumab or avelumab):ti,ab,kw
#8 #4 or #5 or #6 or #7

#9 MeSH descriptor: [Neoadjuvant Therapy] explode all trees
#10 (neoadjuvant or preoperative or pre-operative or presurgical or primary systemic):ti,ab,kw
#11 #9 or #10

#12 #3 and #8 and #11
#13 #12 with Cochrane Library publication date Between Jan 2015 and Dec 2026, in Trials
```

### Expected Results

Approximately 20-30 records

---

## ClinicalTrials.gov Search Strategy

### Advanced Search

**Condition or Disease**: Triple-Negative Breast Cancer OR TNBC

**Other Terms**: (pembrolizumab OR atezolizumab OR durvalumab OR nivolumab OR camrelizumab OR immune checkpoint inhibitor OR immunotherapy) AND (neoadjuvant OR preoperative)

**Study Type**: Interventional Studies (Clinical Trials)

**Study Results**: All Studies (with or without results)

**Phase**: Phase 2, Phase 3

**First Posted**: From 01/01/2015 to 12/31/2026

### Search URL Template

```
https://clinicaltrials.gov/search?cond=Triple-Negative+Breast+Cancer&term=pembrolizumab+OR+atezolizumab+OR+durvalumab+OR+nivolumab+OR+camrelizumab+OR+immune+checkpoint+inhibitor&term=neoadjuvant+OR+preoperative&type=Intr&phase=1&phase=2&aggFilters=phase:2%203,results:with%20without&firstPost=01%2F01%2F2015_12%2F31%2F2026
```

### Expected Results

Approximately 15-25 trials

---

## WHO International Clinical Trials Registry Platform (ICTRP)

### Search Terms

```
Condition: triple-negative breast cancer OR TNBC
Intervention: pembrolizumab OR atezolizumab OR durvalumab OR nivolumab OR camrelizumab OR immune checkpoint inhibitor
Recruitment Status: ALL
```

### Expected Results

Approximately 10-20 trials

---

## Conference Abstracts

### ASCO (American Society of Clinical Oncology)

**Source**: ASCO Meeting Library (https://meetinglibrary.asco.org/)

**Years**: 2015-2025 (Annual Meeting and Breast Cancer Symposium)

**Search Terms**:

- triple-negative breast cancer neoadjuvant immunotherapy
- TNBC pembrolizumab neoadjuvant
- TNBC atezolizumab neoadjuvant

**Manual screening**: Review breast cancer sessions for relevant abstracts

---

### ESMO (European Society for Medical Oncology)

**Source**: ESMO Meeting Library

**Years**: 2015-2025 (Congress and Breast Cancer sessions)

**Search Terms**: Same as ASCO

---

### SABCS (San Antonio Breast Cancer Symposium)

**Source**: Cancer Research journal supplements

**Years**: 2015-2025

**Search Terms**: Same as ASCO

**Expected abstracts**: 10-20 relevant abstracts across all conferences

---

## Grey Literature and Additional Sources

### Regulatory Documents

- **FDA**: Search Drugs@FDA for pembrolizumab, atezolizumab, durvalumab approval documents
- **EMA**: Search European Medicines Agency database

### Pharmaceutical Company Trial Results

- **Merck** (pembrolizumab): https://www.merck.com/clinical-trials/
- **Roche/Genentech** (atezolizumab): https://forpatients.roche.com/en/trials.html
- **AstraZeneca** (durvalumab): https://astrazenecagrouptrials.pharmacm.com/

### Reference Lists

- Hand-search reference lists of included studies
- Hand-search reference lists of relevant systematic reviews (especially Villacampa et al. 2024)

---

## Search Filters and Limits

### Date Limits

- **From**: January 1, 2015 (earliest immunotherapy trials in TNBC)
- **To**: Present (search date: 2026-02-07)
- **Rationale**: Immune checkpoint inhibitors for TNBC emerged around 2015-2016

### Language Limits

- **No language restrictions**
- Will translate non-English articles if necessary
- Priority languages: English, Chinese, Japanese, Korean, Spanish

### Publication Type

- **Include**:
  - Peer-reviewed journal articles
  - Conference abstracts with sufficient data
  - Trial registry records with results
  - Regulatory documents
- **Exclude**:
  - Editorials, commentaries, letters (unless contain original data)
  - Reviews (but check reference lists)
  - Case reports, case series

---

## Search Execution Plan

### Week 3 - Day 15-16 (Search Execution)

#### Day 15 Morning (3 hours)

1. **PubMed**: Execute search, export to BibTeX (30 min)
2. **Embase**: Execute search via institutional access, export to BibTeX (60 min)
3. **Cochrane CENTRAL**: Execute search, export to BibTeX (30 min)
4. **ClinicalTrials.gov**: Execute search, export results to CSV (30 min)

#### Day 15 Afternoon (2 hours)

5. **WHO ICTRP**: Execute search, export results (30 min)
6. **Conference abstracts**: Search ASCO Meeting Library (45 min)
7. **Conference abstracts**: Search ESMO and SABCS (45 min)

#### Day 16 Morning (2 hours)

8. **Grey literature**: Search FDA, EMA, pharmaceutical websites (60 min)
9. **Citation searching**: Check references of Villacampa et al. 2024 (30 min)
10. **Expert consultation**: Email 2-3 key researchers for unpublished studies (30 min)

#### Day 16 Afternoon (1 hour)

11. **Compile all results**: Merge all exported files (30 min)
12. **Document search process**: Complete search log with dates, terms, results (30 min)

---

## Search Documentation

### Search Log Template

For each database, document:

- **Database name and platform**
- **Search date**
- **Search terms used** (exact syntax)
- **Limits applied** (date, language, study type)
- **Number of results retrieved**
- **File name of exported results**
- **Searcher name**

Example:

```
Database: PubMed/MEDLINE (via Entrez)
Date: 2026-02-07
Search terms: [Full query as above]
Limits: 2015/01/01 to 2026/12/31
Results: 95 records
Export file: pubmed_2026-02-07.bib
Searcher: [Name]
Notes: None
```

---

## Expected Total Yield

| Source                           | Expected Records |
| -------------------------------- | ---------------- |
| PubMed/MEDLINE                   | 95-120           |
| Embase                           | 120-150          |
| Cochrane CENTRAL                 | 20-30            |
| ClinicalTrials.gov               | 15-25            |
| WHO ICTRP                        | 10-20            |
| Conference abstracts             | 10-20            |
| Grey literature                  | 5-10             |
| **Total before deduplication**   | **275-375**      |
| **Expected after deduplication** | **150-200**      |

---

## Deduplication Strategy

### Automated Deduplication

Use `multi_db_dedupe.py` script to remove duplicates based on:

- **Title similarity** (>90% match)
- **Author overlap** (≥2 common authors)
- **DOI match** (exact)
- **PMID match** (exact)

### Manual Deduplication

Review near-duplicates (80-90% title similarity):

- Check if same study with different publication types (abstract vs full text)
- Check if same study with different follow-up durations
- Keep most recent/complete publication

---

## Search Update Strategy

### When to Update Search

1. **Before abstract screening**: If >3 months since initial search
2. **Before manuscript submission**: Final search update
3. **After peer review**: If reviewers request update

### How to Update

- Re-run exact same search strategies
- Add new date limit: [last search date] to [current date]
- Document as "Search Update [N]"
- Screen new records using same criteria

---

## Quality Assurance

### Validation Check

- **Test search**: Run simplified version on known key studies (KEYNOTE-522, IMpassion031) to ensure they are captured
- **Peer review**: Have librarian or second researcher review search strategies
- **PRESS checklist**: Peer Review of Electronic Search Strategies (McGowan et al. 2016)

### Key Studies to Verify Capture

- ✓ KEYNOTE-522 (Schmid et al. 2020, PMID: 32101663)
- ✓ IMpassion031 (Mittendorf et al. 2020, PMID: 32966830)
- ✓ GeparNuevo (Loibl et al. 2022, PMID: 39207778)
- ✓ CamRelief (Chen et al. 2025, PMID: 39671272)

If any key study is NOT captured, revise search strategy.

---

## Reporting in Protocol and Manuscript

### PRISMA-S Checklist Compliance

Document all elements per PRISMA-S (Preferred Reporting Items for Systematic Review and Meta-Analysis literature search extension):

- [ ] Named databases and platforms
- [ ] Search strategy for at least one database
- [ ] Date of search for each database
- [ ] Years covered by search
- [ ] Search strings for all databases (appendix)
- [ ] Limits applied
- [ ] Deduplication method

---

## Search Strategy Validation

### Sensitivity Check

- **Gold standard set**: 5 known key RCTs
- **Sensitivity target**: 100% (must capture all 5)
- **Precision**: Not prioritized (prefer high sensitivity, accept low precision)

### Precision Check

- **Screening burden**: 150-200 unique records is acceptable
- **Expected inclusion rate**: 3-5% (5-10 studies included / 150-200 screened)

---

**Version**: 1.0
**Date**: 2026-02-07
**Next review**: Before executing search (Day 15)
**Approved by**: Meta-analysis team
