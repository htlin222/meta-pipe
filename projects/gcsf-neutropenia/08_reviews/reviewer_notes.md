# Reviewer Notes: G-CSF Prophylaxis in Chemotherapy-Induced Neutropenia (NMA)

**Project**: gcsf-neutropenia
**Date**: 2026-03-24
**Reviewer**: QA Auditor (systematic review)

---

## 1. Overall Methodology Assessment

### Strengths

- **Comprehensive network**: The NMA includes all three commercially available G-CSF formulations (filgrastim, pegfilgrastim, lipegfilgrastim) and placebo, enabling both direct and indirect comparisons within a single analytical framework.
- **Adequate sample size**: 18 RCTs with 4,666 patients provides reasonable statistical power for the primary outcome.
- **Rigorous risk-of-bias assessment**: RoB 2.0 applied to all studies; 9/18 rated low risk, consistent with the predominantly double-blind, placebo-controlled study designs.
- **Sensitivity analyses**: Multiple pre-specified sensitivity analyses (excluding high-RoB, dose-finding, and co-intervention studies) confirm robustness of primary findings with negligible change in point estimates (RR range 0.27-0.51 across all sensitivity scenarios).
- **Consistency**: Node-splitting analysis shows no significant inconsistency between direct and indirect evidence at any comparison (all p-interaction > 0.40), supporting the validity of the NMA.
- **Heterogeneity**: tau-squared = 0.031 and I-squared values are low to moderate (0-49%), acceptable for clinical meta-analysis.

### Limitations

- **Lipegfilgrastim evidence is thin**: Only 2 direct studies (Bondarenko 2013, Buchner 2014), both against pegfilgrastim, both in breast cancer. No direct placebo-controlled data for lipegfilgrastim. All lipegfilgrastim-vs-placebo estimates are entirely indirect.
- **Open-label bias**: 5/18 studies are open-label (Timmer-Bonte 2005, Doorduijn 2003, Balducci 2007, Romieu 2007, Hegg 2016). Although FN has a partly objective definition (ANC threshold), fever reporting and decision to hospitalize can be influenced by unblinded clinicians.
- **Cancer type heterogeneity**: Studies span breast cancer, SCLC, NHL, colorectal cancer, and multiple myeloma. While G-CSF mechanism is cancer-agnostic, baseline FN risk varies by regimen and tumor type. Formal subgroup analysis by cancer type is warranted.
- **Pegfilgrastim dosing variability**: Kosaka 2015 used 3.6 mg (Japan-approved dose) rather than the standard 6 mg. This was retained in the main analysis but should be acknowledged.
- **Buchner 2014 is a dose-finding study**: Three lipegfilgrastim dose arms (3, 6, 12 mg) were pooled against pegfilgrastim. This may introduce heterogeneity within the lipeg node. Sensitivity analysis excluding this study shows minimal impact.
- **Secondary outcomes**: OS and infection-related mortality data are sparse. Only 2 studies report OS hazard ratios. This limits the ability to assess whether FN reduction translates to survival benefit.

---

## 2. Study-Specific Concerns

### High Risk of Bias

| Study | Concern | Impact |
|-------|---------|--------|
| Doorduijn 2003 | Open-label; high RoB for measurement domain; per-protocol reporting for some outcomes | May overestimate filgrastim effect; sensitivity analysis excluding this study shows stable results |

### Some Concerns

| Study | Key Issue |
|-------|-----------|
| Crawford 1991 | Randomization sequence generation not fully described (early trial, 1991) |
| Trillet-Lenoir 1993 | Limited sequence generation details; however, double-blind placebo-controlled |
| Pettengell 1992 | Small single-center (N=80); 2 patients lost to follow-up |
| Timmer-Bonte 2005 | Open-label; co-intervention with antibiotics in G-CSF arm complicates attribution |
| Balducci 2007 | Open-label; pegfilgrastim vs no G-CSF; large sample mitigates but does not eliminate bias |
| Romieu 2007 | Open-label; small (N=60); phase II |
| Hegg 2016 | Open-label; small (N=65); phase II |
| Bozzoli 2015 | Open-label; conference abstract only; multiple myeloma (different population) |

### Low Risk of Bias (No Specific Concerns)

Holmes 2002, Green 2003, Vogel 2005, del Giglio 2008, Hecht 2010, Kosaka 2015, Grigg 2003, Bondarenko 2013, Buchner 2014 -- all double-blind with adequate methodology.

---

## 3. Network Geometry and Transitivity

- **Network connectivity**: The network is connected but relies on filgrastim-vs-placebo and pegfilgrastim-vs-placebo comparisons as the primary backbone. The lipegfilgrastim node connects only via pegfilgrastim (2 studies).
- **Transitivity assumption**: Studies span 1991-2016. Supportive care standards have evolved (e.g., antibiotic prophylaxis, growth factor guidelines). Earlier filgrastim trials may have higher baseline FN rates. This temporal heterogeneity should be discussed as a potential threat to transitivity.
- **Effect modifier distribution**: Most studies use primary prophylaxis in intermediate-to-high risk chemotherapy regimens. Cancer type distribution differs across nodes (filgrastim: predominantly SCLC/NHL; pegfilgrastim: predominantly breast cancer; lipegfilgrastim: exclusively breast cancer).

---

## 4. Recommendations for Manuscript

### Critical (Must Address)

1. **Acknowledge lipegfilgrastim limitations explicitly**: State that all lipeg-vs-placebo estimates are indirect, based on only 2 studies, and limited to breast cancer. Avoid claiming equivalence or superiority -- the evidence supports non-inferiority to pegfilgrastim at best, and even this is imprecise.
2. **Qualify the pegfilgrastim vs filgrastim comparison**: The statistically significant RR 0.61 (p=0.013) comes from 3 head-to-head RCTs all in breast cancer with doxorubicin/docetaxel. Generalizability to other regimens and cancer types should be explicitly noted.
3. **Discuss open-label bias impact**: 5 open-label studies contribute to the pegfilgrastim-vs-placebo and filgrastim-vs-placebo nodes. Report the sensitivity analysis excluding open-label studies to address this concern.
4. **Report GRADE certainty alongside all effect estimates**: The Abstract and Discussion should reference certainty levels (HIGH for G-CSF vs placebo FN; LOW for lipeg comparisons).

### Important (Should Address)

5. **Temporal trends in FN management**: Discuss whether evolving supportive care practices (antibiotic prophylaxis, earlier hospitalization protocols) may affect the NMA validity.
6. **Subgroup analysis by cancer type**: The heterogeneous cancer populations warrant at least exploratory subgroup analysis to assess consistency.
7. **Cost-effectiveness implications**: The ranking (lipeg > peg > filgrastim > placebo) has direct cost implications. Even a brief note on cost considerations would strengthen clinical relevance.
8. **Pegfilgrastim 3.6 mg vs 6 mg**: Acknowledge Kosaka 2015 dosing difference.

### Minor (Consider)

9. **Funnel plot / small-study effects**: With 13+ studies for the G-CSF-vs-placebo comparison, formal assessment of publication bias is feasible and should be reported.
10. **Protocol registration**: Confirm PROSPERO registration status and report any protocol deviations.

---

## 5. Data Integrity Checks

- [x] Extraction data matches published study reports (spot-checked Crawford 1991, Vogel 2005, Bondarenko 2013)
- [x] RR calculations are internally consistent (events/N match reported RRs)
- [x] NMA summary estimates are consistent with league table values
- [x] Sensitivity analyses show stable results (all RR point estimates within 0.02 of main analysis)
- [x] Node-splitting p-values indicate no significant inconsistency
- [x] P-scores are concordant with effect estimates (lipeg 0.90 > peg 0.85 > filgrastim 0.54 > placebo 0.003)
- [ ] Forest plots and network plot -- not yet reviewed (awaiting 07_manuscript)

---

## 6. Summary Judgement

This NMA is methodologically sound with robust primary findings. The evidence that all G-CSF formulations substantially reduce FN incidence compared to placebo is HIGH certainty and clinically actionable. The pegfilgrastim advantage over filgrastim is supported by direct evidence but limited to breast cancer. The lipegfilgrastim evidence is the weakest link -- conclusions about this agent must be carefully hedged. The manuscript should be transparent about these gradations in evidence quality. With the recommended revisions addressed, this work meets the standards for a high-impact journal submission.
