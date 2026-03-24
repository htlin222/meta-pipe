# Manuscript Outline

**Title**: Comparative Efficacy of G-CSF Formulations for Prevention of Febrile Neutropenia in Cancer Patients Receiving Myelosuppressive Chemotherapy: A Systematic Review and Network Meta-Analysis

**Target journals**: Lancet Oncology, JAMA Oncology, Annals of Oncology
**Target word count**: 4,000-5,000 words
**Format**: IMRaD with structured abstract

---

## Abstract (~300 words)

- **Background**: FN is a serious complication; multiple G-CSF formulations exist but no NMA has compared all three simultaneously.
- **Methods**: Systematic review and frequentist NMA of RCTs; PubMed, Scopus, Embase, CENTRAL searched; primary outcome FN incidence (RR); random-effects REML; P-scores for ranking.
- **Results**: 18 RCTs (N=4,666). All G-CSFs reduce FN vs placebo. Pegfilgrastim RR 0.30 (0.20-0.46); filgrastim RR 0.50 (0.38-0.66); lipegfilgrastim RR 0.28 (0.15-0.52). Pegfilgrastim superior to filgrastim (RR 0.61, 0.41-0.90). Lipegfilgrastim equivalent to pegfilgrastim (RR 0.93, 0.51-1.68). No inconsistency detected.
- **Conclusions**: Long-acting G-CSFs (pegfilgrastim, lipegfilgrastim) are preferred; pegfilgrastim has the strongest evidence base.

## Introduction (~600 words)

1. Burden of febrile neutropenia: morbidity, mortality (5-11%), cost ($15,000-25,000/episode), chemotherapy dose delays
2. G-CSF prophylaxis as standard of care (ASCO/ESMO/NCCN guidelines recommend primary prophylaxis when FN risk >=20%)
3. Three formulations: filgrastim (daily), pegfilgrastim (single-dose per cycle), lipegfilgrastim (single-dose, glycopegylated)
4. Knowledge gap: prior meta-analyses (Cooper 2011, Mhaskar 2014 Cochrane) used pairwise only; no NMA has simultaneously compared all three
5. Study objective and rationale for NMA

## Methods (~1,000 words)

1. Protocol registration (PROSPERO placeholder)
2. Search strategy: PubMed, Scopus, Embase, CENTRAL; no date restriction
3. Eligibility: PICO criteria (adults, myelosuppressive chemo, G-CSF vs placebo/active, FN incidence)
4. Screening: dual-review, kappa = 0.84 (almost perfect agreement)
5. Data extraction: standardized form, two reviewers
6. Risk of bias: RoB 2.0 tool
7. Statistical analysis:
   - Frequentist NMA using netmeta (R); random-effects REML
   - Effect measure: RR (log scale)
   - Consistency: global Q decomposition + node-splitting
   - Ranking: P-scores
   - Publication bias: comparison-adjusted funnel plot + Egger's test
   - Sensitivity analyses (5 pre-specified)

## Results (~1,500 words)

1. **Study selection**: PRISMA flow — 27 screened, 18 RCTs included (N=4,666)
2. **Study characteristics**: Table 1 — years 1991-2016, breast cancer (11), SCLC (3), NHL (3), CRC (1), MM (1)
3. **Risk of bias**: 9 low, 8 some concerns, 1 high (Doorduijn2003 — open-label with measurement bias)
4. **Network geometry**: 4 nodes (placebo, filgrastim, pegfilgrastim, lipegfilgrastim); fully connected
5. **Primary outcome — FN incidence** (league table + forest plot):
   - All G-CSFs vs placebo: statistically significant reductions
   - Pegfilgrastim vs filgrastim: RR 0.61 (0.41-0.90, p=0.013)
   - Lipegfilgrastim vs pegfilgrastim: RR 0.93 (0.51-1.68, p=0.802)
6. **Rankings**: P-scores — lipegfilgrastim (0.901), pegfilgrastim (0.853), filgrastim (0.542), placebo (0.003)
7. **Heterogeneity**: tau^2=0.0312; I^2 low-to-moderate
8. **Inconsistency**: All node-splitting p>0.05; direct and indirect evidence consistent
9. **Sensitivity analyses**: All 5 confirm main findings
10. **Secondary outcomes**: Narrative summary (OS, infection-related mortality, hospitalization, neutrophil recovery, bone pain, RDI)

## Discussion (~1,200 words)

1. Principal findings: long-acting G-CSFs superior; pegfilgrastim has robust evidence; lipegfilgrastim comparable but limited data
2. Context: findings align with and extend Cooper 2011 and Mhaskar 2014 Cochrane review
3. Clinical implications:
   - Pegfilgrastim preferred first-line (strongest evidence, single-dose convenience)
   - Lipegfilgrastim as equivalent alternative (2 RCTs only)
   - Filgrastim remains effective but requires daily dosing
4. Strengths: NMA framework, comprehensive search, dual-review (kappa 0.84), pre-registered sensitivity analyses, no inconsistency
5. Limitations:
   - 1 high-RoB study, 8 with some concerns
   - Lipegfilgrastim evidence limited (2 RCTs, no direct placebo comparison)
   - Cancer type heterogeneity
   - No individual patient data
   - Open-label studies for some comparisons
6. GRADE certainty: high for G-CSF vs placebo; moderate for pegfilgrastim vs filgrastim; low for lipegfilgrastim comparisons

## Conclusions (~200 words)

- All G-CSF formulations significantly prevent FN
- Pegfilgrastim and lipegfilgrastim are more effective than filgrastim
- Pegfilgrastim has the strongest evidence base
- Lipegfilgrastim is a viable alternative to pegfilgrastim
- These findings support current guideline recommendations for long-acting G-CSF prophylaxis

## Tables and Figures

| Item | Description | Source |
|------|-------------|--------|
| Table 1 | Study characteristics (18 RCTs) | `study_characteristics.csv` |
| Table 2 | League table (all pairwise NMA estimates) | `league_table.csv` |
| Table 3 | Treatment rankings (P-scores) | `ranking_table.csv` |
| Table 4 | Sensitivity analyses summary | `sensitivity_analyses.csv` |
| Figure 1 | PRISMA flow diagram | To be generated |
| Figure 2 | Network geometry plot | `network_plot.png` |
| Figure 3 | NMA forest plot (vs placebo) | `forest_nma.png` |
| Figure 4 | Comparison-adjusted funnel plot | `funnel_plot.png` |
| Figure S1 | Risk of bias summary | Supplementary |
| Figure S2 | Rankogram | `rankogram.png` |
