# Reporting Checklist Compliance Audit

**Project**: gcsf-neutropenia
**Date**: 2026-03-24
**Auditor**: QA Auditor

---

## Guidelines Assessed

1. **PRISMA 2020** (Page et al., BMJ 2021) -- 27 items
2. **PRISMA-NMA Extension** (Hutton et al., Ann Intern Med 2015) -- 5 additional items (32 total)
3. **GRADE NMA** (Puhan et al., J Clin Epidemiol 2014)

---

## PRISMA 2020 Compliance (27 Core Items)

| # | Item | Status | Location/Notes |
|---|------|--------|----------------|
| 1 | Title: identify as systematic review | VERIFY | Must state "network meta-analysis" in title |
| 2 | Abstract: structured summary | VERIFY | Awaiting manuscript |
| 3 | Rationale | COMPLETE | 01_protocol/pico.yaml; clinical rationale for comparing G-CSF formulations |
| 4 | Objectives | COMPLETE | 01_protocol/pico.yaml; PICO clearly defined |
| 5 | Eligibility criteria | COMPLETE | 01_protocol/eligibility.md |
| 6 | Information sources | COMPLETE | 01_protocol/search-plan.md |
| 7 | Search strategy | COMPLETE | 02_search/ |
| 8 | Selection process | COMPLETE | 03_screening/ |
| 9 | Data collection process | COMPLETE | 05_extraction/ |
| 10 | Data items | COMPLETE | 01_protocol/outcomes.md; 05_extraction/extraction.csv |
| 11 | Study risk of bias | COMPLETE | 05_extraction/rob_assessment.csv; RoB 2.0 applied |
| 12 | Effect measures | COMPLETE | RR for dichotomous; HR for time-to-event; MD for continuous |
| 13 | Synthesis methods | COMPLETE | 06_analysis/; frequentist NMA via netmeta |
| 14 | Reporting bias assessment | PARTIAL | Egger test feasible for FN (>=10 studies); not yet confirmed in manuscript |
| 15 | Certainty assessment | COMPLETE | 08_reviews/grade_summary.csv |
| 16 | Study selection results | COMPLETE | 03_screening/ |
| 17 | Study characteristics | COMPLETE | 06_analysis/tables/study_characteristics.csv |
| 18 | Risk of bias in studies | COMPLETE | 05_extraction/rob_assessment.csv |
| 19 | Results of individual studies | COMPLETE | 05_extraction/round-01/extraction.csv |
| 20 | Results of syntheses | COMPLETE | 06_analysis/tables/nma_summary.csv; league_table.csv |
| 21 | Reporting biases | PARTIAL | Funnel plot not confirmed in manuscript outputs |
| 22 | Certainty of evidence | COMPLETE | 08_reviews/grade_summary.csv; 08_reviews/sof_table.csv |
| 23 | Discussion: summary | VERIFY | Awaiting manuscript |
| 24 | Discussion: limitations | VERIFY | See claim_audit.md for required limitations |
| 25 | Discussion: interpretation | VERIFY | Awaiting manuscript |
| 26 | Registration and protocol | VERIFY | PROSPERO registration status to confirm |
| 27 | Funding and COI | VERIFY | Awaiting manuscript |

**Core PRISMA Score**: 19/27 COMPLETE, 2/27 PARTIAL, 6/27 VERIFY (awaiting manuscript)

---

## PRISMA-NMA Extension Items (5 Additional)

| # | Item | Status | Location/Notes |
|---|------|--------|----------------|
| S1 | Network geometry: describe and present network plot | PARTIAL | Network structure described; network plot awaiting manuscript figures |
| S2 | Assessment of inconsistency | COMPLETE | 06_analysis/tables/inconsistency_test.csv; node-splitting with all p>0.40 |
| S3 | Treatment ranking | COMPLETE | 06_analysis/tables/ranking_table.csv; P-scores reported |
| S4 | Assessment of transitivity | PARTIAL | Discussed in reviewer_notes.md; formal assessment needed in manuscript |
| S5 | Additional analyses (sensitivity, subgroup) | COMPLETE | 06_analysis/tables/sensitivity_analyses.csv |

**NMA Extension Score**: 3/5 COMPLETE, 2/5 PARTIAL

---

## GRADE-NMA Compliance

| Domain | Status | Notes |
|--------|--------|-------|
| Within-study bias (RoB) | COMPLETE | RoB 2.0 applied to all 18 studies |
| Reporting bias | PARTIAL | Funnel plot needed for >=10-study comparisons |
| Indirectness | COMPLETE | Assessed per comparison in GRADE table |
| Imprecision | COMPLETE | OIS and CI width evaluated |
| Heterogeneity | COMPLETE | I-squared and tau-squared reported |
| Incoherence (inconsistency) | COMPLETE | Node-splitting performed |
| Overall certainty per comparison | COMPLETE | 08_reviews/grade_summary.csv |

---

## Compliance Summary

| Guideline | Complete | Partial | Pending | Total |
|-----------|----------|---------|---------|-------|
| PRISMA 2020 | 19 | 2 | 6 | 27 |
| PRISMA-NMA | 3 | 2 | 0 | 5 |
| GRADE-NMA | 5 | 1 | 0 | 6 |
| **Total** | **27** | **5** | **6** | **38** |

---

## Action Items

1. **Manuscript required**: 6 PRISMA items cannot be verified until the manuscript is drafted (items 1, 2, 23-27)
2. **Funnel plot / Egger test**: Must be generated and reported for the all-G-CSF-vs-placebo FN comparison (>=13 studies)
3. **Network plot**: Required for PRISMA-NMA S1; should show node sizes proportional to sample and edge widths proportional to number of direct studies
4. **Transitivity assessment**: Formal discussion of effect modifier distribution across comparisons needed in manuscript
5. **PROSPERO**: Confirm registration number and report any deviations from registered protocol

**Overall Readiness**: The analysis-stage deliverables are substantially complete (27/38 items verified). Remaining gaps are manuscript-dependent and expected to be resolved during Stage 07.
