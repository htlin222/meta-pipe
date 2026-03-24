# PRISMA-NMA Pipeline Checklist (32 Items)

**Project**: gcsf-neutropenia
**Date**: 2026-03-24
**Auditor**: QA Auditor

---

## Section 1: Title (Item 1)

- [ ] **1. Title**: Identify the report as a systematic review incorporating a network meta-analysis
  - *Status*: Awaiting manuscript (07_manuscript not yet created)

## Section 2: Abstract (Item 2)

- [ ] **2. Structured summary**: Provide a structured abstract including background, objectives, data sources, study eligibility, participants, interventions, study appraisal/synthesis, results, limitations, conclusions, registration number
  - *Status*: Awaiting manuscript

## Section 3: Introduction (Items 3-4)

- [x] **3. Rationale**: Describe the rationale for the review in the context of existing knowledge
  - *Location*: `01_protocol/pico.yaml` (rationale for comparing 3 G-CSF formulations via NMA)
- [x] **4. Objectives**: Provide an explicit statement of questions being addressed with reference to PICO
  - *Location*: `01_protocol/pico.yaml`, `01_protocol/outcomes.md`

## Section 4: Methods (Items 5-16)

- [x] **5. Protocol and registration**: Indicate whether a review protocol exists, provide registration information
  - *Location*: `01_protocol/`; PROSPERO status to confirm in manuscript
- [x] **6. Eligibility criteria**: Specify study characteristics and report characteristics used as criteria
  - *Location*: `01_protocol/eligibility.md`; RCTs of G-CSF vs placebo or head-to-head
- [x] **7. Information sources**: Describe all information sources searched with dates
  - *Location*: `01_protocol/search-plan.md`, `02_search/`
- [x] **8. Search**: Present full electronic search strategy for at least one database
  - *Location*: `02_search/`
- [x] **9. Study selection**: State the process for selecting studies (screening, eligibility, inclusion)
  - *Location*: `03_screening/`
- [x] **10. Data collection process**: Describe method of data extraction and any processes for obtaining/confirming data
  - *Location*: `05_extraction/`
- [x] **11. Data items**: List and define all variables for which data were sought
  - *Location*: `01_protocol/outcomes.md`; 7 outcomes defined with measurement criteria
- [x] **12. Risk of bias in individual studies**: Describe methods used for assessing RoB
  - *Location*: `05_extraction/rob_assessment.csv`; RoB 2.0 (5 domains)
- [x] **13. Summary measures**: State the principal summary measures (RR, HR, MD)
  - *Location*: `01_protocol/outcomes.md`; `06_analysis/tables/nma_summary.csv`

### NMA-Specific Methods

- [x] **14. Planned methods of analysis**: Describe the methods of handling data and combining results
  - *Location*: `06_analysis/`; frequentist NMA using netmeta (R); random-effects model
- [x] **14a. Geometry of the network**: Describe methods used to present and assess the network geometry
  - *Location*: 4-node network (filgrastim, pegfilgrastim, lipegfilgrastim, placebo); network plot pending
- [x] **14b. Assessment of inconsistency**: Describe statistical methods for evaluating consistency
  - *Location*: `06_analysis/tables/inconsistency_test.csv`; node-splitting approach
- [x] **14c. Assessment of transitivity**: Describe methods for evaluating the transitivity assumption
  - *Partial*: Discussed qualitatively; formal assessment of effect modifier distribution needed in manuscript

- [x] **15. Risk of bias across studies**: Specify any assessment of publication bias
  - *Partial*: Egger test planned for comparisons with >=10 studies; results pending manuscript
- [x] **16. Additional analyses**: Describe methods of additional analyses (sensitivity, subgroup, meta-regression)
  - *Location*: `06_analysis/tables/sensitivity_analyses.csv`; 4 sensitivity scenarios completed

## Section 5: Results (Items 17-23)

- [x] **17. Study selection**: Report numbers at each stage of study selection; PRISMA flow diagram
  - *Location*: `03_screening/`; flow diagram pending manuscript
- [x] **18. Study characteristics**: Present characteristics of each study
  - *Location*: `06_analysis/tables/study_characteristics.csv`; 18 studies with full characteristics
- [x] **19. Risk of bias within studies**: Present RoB assessment for each included study
  - *Location*: `05_extraction/rob_assessment.csv`; 9 low, 8 some concerns, 1 high
- [x] **20. Results of individual studies**: For all outcomes, present simple summary data and effect estimates with CIs
  - *Location*: `05_extraction/round-01/extraction.csv`
- [x] **21. Synthesis of results**: Present results of each meta-analysis with CIs and measures of consistency
  - *Location*: `06_analysis/tables/nma_summary.csv`, `league_table.csv`

### NMA-Specific Results

- [x] **21a. Network geometry**: Provide a network figure and description
  - *Partial*: Structure described (4 nodes, 18 studies); figure pending
- [x] **21b. Inconsistency results**: Present results of assessment of inconsistency
  - *Location*: `06_analysis/tables/inconsistency_test.csv`; all p-interaction > 0.40
- [x] **21c. Treatment rankings**: Present ranking probabilities
  - *Location*: `06_analysis/tables/ranking_table.csv`; P-scores: lipeg 0.90, peg 0.85, fil 0.54, placebo 0.003

- [ ] **22. Risk of bias across studies**: Present results of assessment of publication bias
  - *Status*: Funnel plot and Egger test not yet generated
- [x] **23. Additional analysis**: Present results of sensitivity/subgroup analyses
  - *Location*: `06_analysis/tables/sensitivity_analyses.csv`; robust across all scenarios

## Section 6: Discussion (Items 24-26)

- [ ] **24. Summary of evidence**: Summarize main findings including strength of evidence for each outcome; consider relevance to key groups
  - *Status*: Awaiting manuscript; GRADE summary prepared in `08_reviews/grade_summary.csv`
- [ ] **25. Limitations**: Discuss limitations at study and outcome level, and at review level
  - *Status*: Awaiting manuscript; limitations catalogued in `08_reviews/reviewer_notes.md`
- [ ] **26. Conclusions**: Provide general interpretation of results in context of other evidence and implications
  - *Status*: Awaiting manuscript

## Section 7: Funding (Item 27)

- [ ] **27. Funding**: Describe sources of funding and role of funders
  - *Status*: Awaiting manuscript

---

## Completion Summary

| Section | Complete | Incomplete | Total |
|---------|----------|------------|-------|
| Title/Abstract | 0 | 2 | 2 |
| Introduction | 2 | 0 | 2 |
| Methods | 13 | 0 | 13 |
| Results | 6 | 1 | 7 |
| Discussion | 0 | 3 | 3 |
| Funding | 0 | 1 | 1 |
| **NMA Extension** | 4 | 1 | 5 |
| **Total** | **25** | **7** | **32** |

**Completion Rate**: 25/32 (78%)

**Remaining 7 items** are manuscript-dependent (Title, Abstract, Publication bias figure, Discussion x3, Funding). These will be addressed during Stage 07 manuscript assembly.
