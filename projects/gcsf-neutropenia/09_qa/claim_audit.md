# Claim Audit: G-CSF Prophylaxis NMA

**Project**: gcsf-neutropenia
**Date**: 2026-03-24
**Auditor**: QA Auditor

---

## Purpose

Systematic check for overclaiming, unsupported assertions, and mismatches between evidence strength and conclusions.

---

## 1. GRADE-Conclusion Concordance

| Claim | GRADE Certainty | Supported? | Notes |
|-------|----------------|------------|-------|
| All G-CSFs reduce FN vs placebo | HIGH | YES | Large, consistent, statistically significant effects across all formulations. Language such as "substantially reduces" or "strongly reduces" is appropriate. |
| Pegfilgrastim is superior to filgrastim for FN prevention | MODERATE | CONDITIONAL | RR 0.61 (0.41-0.90, p=0.013) is statistically significant but limited to 3 breast cancer RCTs. Claims should be qualified: "Pegfilgrastim was associated with a lower FN incidence compared with filgrastim in head-to-head trials, although evidence is limited to breast cancer populations." |
| Lipegfilgrastim is comparable/non-inferior to pegfilgrastim | LOW | CAUTION | RR 0.93 (0.51-1.68, p=0.80) is non-significant but with a wide CI. The evidence cannot confirm equivalence. Appropriate language: "Limited evidence from 2 RCTs suggests similar efficacy, but the comparison is imprecise and restricted to breast cancer." |
| G-CSF improves overall survival | LOW | OVERCLAIM RISK | Only 2 studies report OS; HR 0.85 (0.60-1.20) is non-significant. Must NOT claim survival benefit. Appropriate: "Evidence is insufficient to determine whether G-CSF prophylaxis improves overall survival." |
| G-CSF reduces infection-related mortality | MODERATE | CONDITIONAL | RR 0.55 (0.30-1.01) is borderline non-significant. Must hedge: "G-CSF prophylaxis may reduce infection-related mortality, but the evidence is imprecise due to the rarity of events." |
| G-CSF reduces hospitalization | MODERATE | YES (with qualification) | RR 0.35 (0.26-0.48) is significant and consistent. Note open-label bias: "G-CSF prophylaxis was associated with substantially fewer hospitalizations, although some studies were open-label." |

---

## 2. Comparative Claims Audit

### 2.1 Lipegfilgrastim Claims (Highest Overclaim Risk)

**Red flags to check for**:
- Claiming lipegfilgrastim is "equivalent" or "non-inferior" to pegfilgrastim without acknowledging that this was not formally tested and the CI is very wide
- Citing lipegfilgrastim P-score ranking (0.90, rank 1) without noting this is driven largely by indirect evidence
- Presenting lipegfilgrastim-vs-placebo RR 0.28 without stating this is an entirely indirect estimate with no direct supporting trials
- Claiming lipegfilgrastim is "the most effective G-CSF" based on rankings alone

**Required hedging language**: "Lipegfilgrastim had the highest probability of being the most effective agent (P-score 0.90), but this ranking is based on only 2 direct head-to-head trials against pegfilgrastim and should be interpreted with caution."

### 2.2 Pegfilgrastim vs Filgrastim

**Check for**:
- Stating superiority without noting all 3 direct studies were in breast cancer with doxorubicin/docetaxel
- Overgeneralizing to all cancer types and chemotherapy regimens
- Failing to mention that the direct estimate (RR 0.70, 0.47-1.04) crosses 1.0, while the NMA estimate (RR 0.61, 0.41-0.90) achieves significance partly through indirect evidence

**Required context**: "The NMA estimate incorporating indirect evidence suggests pegfilgrastim superiority (RR 0.61, p=0.013), while the direct-only estimate shows a non-significant trend (RR 0.70, p=0.08)."

---

## 3. Statistical Reporting Checks

| Check | Status | Detail |
|-------|--------|--------|
| All CIs reported alongside point estimates | VERIFY | Every RR/HR must include 95% CI |
| P-values consistent with CI | OK | Checked: all p-values concordant with CI crossing/not crossing 1.0 |
| I-squared reported for heterogeneity | OK | Reported for all comparisons with direct evidence |
| Non-significant results not described as "no effect" | VERIFY | Non-significance means insufficient evidence, not absence of effect |
| NMA-specific: node-splitting reported | OK | All comparisons tested; no significant inconsistency |
| NMA-specific: SUCRA/P-scores with uncertainty | VERIFY | Rankings should include CrI or note uncertainty |

---

## 4. Limitations Acknowledgement Checklist

The manuscript must acknowledge:

- [ ] Open-label bias in 5/18 studies
- [ ] Cancer type heterogeneity across treatment nodes
- [ ] Lipegfilgrastim evidence limited to 2 studies in breast cancer only
- [ ] Temporal heterogeneity (1991-2016) and evolving supportive care standards
- [ ] Pegfilgrastim dosing variation (3.6 mg vs 6 mg)
- [ ] Buchner 2014 dose-finding design (3 lipeg dose arms pooled)
- [ ] Sparse data for OS and infection-related mortality
- [ ] Single high-RoB study (Doorduijn 2003)
- [ ] Potential transitivity concerns due to different cancer types per node
- [ ] No direct lipegfilgrastim-vs-placebo or lipegfilgrastim-vs-filgrastim trials

---

## 5. Specific Overclaim Patterns to Flag

### Pattern 1: Causal Language

- AVOID: "G-CSF prevents febrile neutropenia"
- USE: "G-CSF prophylaxis was associated with a substantially lower incidence of febrile neutropenia"
- EXCEPTION: Given the RCT design, "reduces" is acceptable for HIGH certainty outcomes

### Pattern 2: Ranking as Definitive

- AVOID: "Lipegfilgrastim is the most effective G-CSF"
- USE: "Lipegfilgrastim had the highest P-score (0.90), suggesting it may be the most effective, though this finding is based on limited evidence and should be interpreted cautiously"

### Pattern 3: Absence of Evidence as Evidence of Absence

- AVOID: "G-CSF has no effect on overall survival"
- USE: "The available evidence was insufficient to detect a survival benefit"

### Pattern 4: Overextension Beyond Study Populations

- AVOID: "Our findings apply to all cancer patients receiving chemotherapy"
- USE: "Our findings are most directly applicable to patients with solid tumors or aggressive lymphomas receiving moderately to highly myelosuppressive chemotherapy regimens"

---

## 6. Audit Summary

| Category | Count | Details |
|----------|-------|---------|
| High overclaim risk | 2 | Lipegfilgrastim efficacy claims; OS benefit claims |
| Moderate overclaim risk | 2 | Peg vs fil generalizability; infection mortality |
| Low overclaim risk | 2 | G-CSF vs placebo FN; hospitalization reduction |
| Required hedging additions | 4 | Lipeg ranking, peg vs fil population, OS, direct vs NMA estimates |
| Limitations to verify in manuscript | 10 | See checklist above |

**Overall Assessment**: The core finding (G-CSFs reduce FN) is well-supported. The principal overclaim risks center on (a) lipegfilgrastim conclusions drawn from sparse indirect evidence, and (b) generalization of breast cancer-specific head-to-head data to broader populations. These must be explicitly addressed in the Discussion section.
