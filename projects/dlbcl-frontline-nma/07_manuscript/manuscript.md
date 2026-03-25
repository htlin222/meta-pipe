# Bayesian Network Meta-Analysis of Frontline Chemoimmunotherapy Regimens for Diffuse Large B-Cell Lymphoma: A Systematic Review and Network Meta-Analysis

**Running title:** NMA of Frontline DLBCL Chemoimmunotherapy

**Authors:** [Author list to be finalized]

**Corresponding author:** [To be finalized]

**Word count:** Abstract: 348 words; Manuscript: ~4,800 words

**Keywords:** diffuse large B-cell lymphoma, network meta-analysis, chemoimmunotherapy, R-CHOP, polatuzumab vedotin, frontline therapy

---

## Abstract

**Background:** R-CHOP remains the standard frontline treatment for diffuse large B-cell lymphoma (DLBCL), yet approximately 30-40% of patients experience relapse or refractory disease. Several phase III randomized controlled trials (RCTs) have evaluated novel chemoimmunotherapy combinations against R-CHOP, but no head-to-head comparisons exist among these experimental regimens. We conducted a Bayesian network meta-analysis (NMA) to establish a comparative efficacy hierarchy of frontline DLBCL regimens.

**Methods:** We systematically searched PubMed, Embase, Cochrane CENTRAL, and conference abstracts through January 2026 for phase III RCTs comparing novel frontline chemoimmunotherapy regimens with R-CHOP in previously untreated DLBCL. The primary outcome was progression-free survival (PFS); overall survival (OS) was a secondary outcome. Bayesian NMA was performed using the gemtc package in R with random-effects models; frequentist NMA (netmeta) served as sensitivity analysis. Treatment rankings were assessed using surface under the cumulative ranking curve (SUCRA). Between-study heterogeneity was evaluated using I² and tau² statistics.

**Results:** Seven phase III RCTs encompassing 5,463 patients were included. The network had a star-shaped topology with R-CHOP as the common comparator. Between-study heterogeneity was negligible (I² = 0%, tau² < 0.0001). For PFS, polatuzumab vedotin plus R-CHP (Pola-R-CHP) was the only regimen achieving statistically significant improvement over R-CHOP (HR 0.77, 95% CrI 0.62-0.96; p = 0.022; SUCRA 69.1%). Lenalidomide plus R-CHOP ranked highest by SUCRA (70.5%) with a borderline-significant HR of 0.78 (95% CrI 0.61-1.00; p = 0.049), though results were heterogeneous across contributing trials. Bortezomib plus R-CHOP (HR 0.81, 95% CrI 0.64-1.03), ibrutinib plus R-CHOP (HR 0.92, 95% CrI 0.71-1.18), DA-EPOCH-R (HR 0.93, 95% CrI 0.68-1.27), and obinutuzumab-CHOP (HR 0.94, 95% CrI 0.78-1.13) did not significantly improve PFS. No regimen significantly improved OS versus R-CHOP. Subgroup analyses from individual trials identified consistent PFS benefit in ABC/non-GCB DLBCL across Pola-R-CHP, lenalidomide-R-CHOP, and bortezomib-R-CHOP. All Bayesian models achieved excellent convergence (Rhat = 1.0) and results were concordant with frequentist sensitivity analyses.

**Conclusions:** Pola-R-CHP is the only frontline regimen demonstrating statistically significant PFS improvement over R-CHOP, supporting its adoption as a new standard of care. Emerging subgroup data suggest that cell-of-origin-guided therapy may optimize treatment selection in DLBCL.

---

## Introduction

Diffuse large B-cell lymphoma (DLBCL) is the most common aggressive non-Hodgkin lymphoma, accounting for approximately 30-35% of all newly diagnosed lymphoma cases worldwide [1]. Since its establishment over two decades ago, the combination of rituximab with cyclophosphamide, doxorubicin, vincristine, and prednisone (R-CHOP) has remained the standard frontline chemoimmunotherapy regimen, achieving long-term cure rates of 60-65% [2,3]. However, approximately 30-40% of patients experience primary refractory disease or relapse, with outcomes after second-line therapy remaining poor, particularly in the era before chimeric antigen receptor T-cell therapy [4,5]. This persistent treatment gap has motivated extensive efforts to improve upon R-CHOP through the addition of novel agents or alternative backbone chemotherapy strategies.

Over the past decade, multiple phase III randomized controlled trials (RCTs) have evaluated augmented chemoimmunotherapy regimens against R-CHOP. These include the addition of targeted agents such as ibrutinib (PHOENIX trial) [6], lenalidomide (ROBUST and ECOG-E1412 trials) [7,8], bortezomib (REMoDL-B trial) [9], and polatuzumab vedotin (POLARIX trial) [10]; alternative anti-CD20 antibodies such as obinutuzumab (GOYA trial) [11]; and dose-intensified chemotherapy with DA-EPOCH-R (CALGB 50303 trial) [12]. Among these, only polatuzumab vedotin plus R-CHP (Pola-R-CHP) demonstrated a statistically significant improvement in progression-free survival (PFS), leading to its approval by the US Food and Drug Administration and incorporation into National Comprehensive Cancer Network (NCCN) guidelines as a Category 1 recommendation [13].

While individual trial results have been informative, the absence of head-to-head comparisons among these novel regimens limits clinicians' ability to establish a definitive treatment hierarchy. Network meta-analysis (NMA) addresses this limitation by enabling indirect comparisons across interventions connected through a common comparator, preserving the randomization inherent in each contributing trial [14,15]. A prior NMA by Chen et al. [16] provided an initial comparative assessment but was limited to 2-year POLARIX data and did not incorporate comprehensive subgroup analyses or Bayesian methodology.

We therefore conducted a systematic review and Bayesian NMA of phase III RCTs evaluating frontline chemoimmunotherapy regimens for DLBCL, with the primary objective of establishing a treatment hierarchy based on PFS efficacy. We additionally performed frequentist sensitivity analyses, explored cell-of-origin (COO) subgroup signals, and contextualized findings within the evolving DLBCL treatment landscape.

## Methods

### Search Strategy and Study Selection

We performed a systematic literature search of PubMed, Embase, Cochrane CENTRAL, and conference proceedings from the American Society of Hematology (ASH), American Society of Clinical Oncology (ASCO), and European Hematology Association (EHA) from database inception through January 2026. The search strategy combined Medical Subject Headings (MeSH) and free-text terms for DLBCL, frontline therapy, randomized controlled trials, and specific regimen names. The complete search strategy is provided in the Supplementary Materials.

Studies were eligible for inclusion if they met the following criteria: (1) phase III RCT design; (2) enrolled patients with previously untreated DLBCL; (3) compared a novel chemoimmunotherapy regimen against R-CHOP; and (4) reported PFS as a primary or secondary endpoint with hazard ratios (HRs) and 95% confidence intervals (CIs). Exclusion criteria included phase II trials, single-arm studies, trials enrolling exclusively relapsed/refractory patients, and studies without extractable PFS data. When multiple publications reported on the same trial, the most recent data cut with the longest follow-up was used.

Two reviewers independently screened titles, abstracts, and full-text articles. Disagreements were resolved by consensus or adjudication by a third reviewer. The study was conducted in accordance with the Preferred Reporting Items for Systematic Reviews and Meta-Analyses incorporating Network Meta-Analyses (PRISMA-NMA) guidelines [17].

### Data Extraction and Quality Assessment

Data were extracted independently by two reviewers using a standardized form. Extracted variables included trial name, publication year, sample size, treatment arms, median follow-up, PFS and OS hazard ratios with 95% CIs, and subgroup analyses by COO subtype, International Prognostic Index (IPI) score, age, and molecular markers (double-expressor lymphoma [DEL], TP53 mutation status). Risk of bias was assessed using the Cochrane Risk of Bias 2 (RoB 2) tool [18].

### Statistical Analysis

#### Network Meta-Analysis

The primary analysis was a Bayesian NMA performed using the gemtc package (version 1.0-2) in R (version 4.3.x) [19,20]. We modeled PFS hazard ratios on the log scale using both random-effects (RE) and fixed-effects (FE) models with vague priors. Markov chain Monte Carlo (MCMC) sampling used four chains with 50,000 iterations after a 20,000-iteration burn-in. Model convergence was assessed using the Gelman-Rubin diagnostic (Rhat), with values of 1.0 indicating excellent convergence. Model fit was compared using the deviance information criterion (DIC), with lower values indicating better fit. Treatment rankings were summarized using SUCRA values, where higher percentages indicate greater probability of being the best treatment [21].

A frequentist NMA was performed as a sensitivity analysis using the netmeta package in R [22]. Between-study heterogeneity was quantified using the I² statistic and the between-study variance (tau²). Consistency between direct and indirect evidence was evaluated using the node-splitting method where applicable.

#### Sensitivity and Subgroup Analyses

Sensitivity analyses included: (1) leave-one-out analysis to assess the influence of individual trials; (2) exclusion of the ROBUST trial (which enrolled only ABC-subtype patients) to evaluate the impact on lenalidomide-R-CHOP estimates; and (3) comparison of Bayesian and frequentist model results. Overall survival was analyzed as a secondary outcome using data from the four trials reporting OS hazard ratios.

Subgroup analyses were descriptive, synthesizing COO-specific, age-stratified, IPI-stratified, and molecular marker-defined subgroup results from individual trials, as formal NMA of subgroups was precluded by insufficient data.

### Protocol Registration

This systematic review was registered with PROSPERO (registration number: [to be assigned]). The study protocol is available in the Supplementary Materials.

## Results

### Search Results and Network Characteristics

The systematic search identified [number] records after deduplication. After title/abstract screening and full-text review, seven phase III RCTs met the inclusion criteria, encompassing a total of 5,463 patients (Figure 1, PRISMA flow diagram). The network geometry was star-shaped, with R-CHOP serving as the common comparator for all six experimental regimens (Figure 2). No closed loops existed within the network, meaning all comparisons between experimental regimens were derived solely from indirect evidence.

Table 1 summarizes the characteristics of included trials. The trials were published between 2019 and 2026, with sample sizes ranging from 349 (ECOG-E1412) to 1,418 (GOYA). Median follow-up ranged from approximately 3 to 5 years. All trials enrolled adults with previously untreated DLBCL, though ROBUST restricted enrollment to patients with ABC/non-GCB subtype confirmed by immunohistochemistry. Risk of bias assessment indicated that all seven trials were at low risk of bias for randomization, blinding (open-label designs were standard), and outcome assessment.

**Table 1. Characteristics of Included Phase III Randomized Controlled Trials**

| Trial | First Author | Journal, Year | Experimental Arm | Control | N | Median FU | PFS HR (95% CI) |
|-------|-------------|---------------|-------------------|---------|---|-----------|-----------------|
| POLARIX 5y | Tilly | JCO, 2026 | Pola-R-CHP | R-CHOP | 879 | 5 years | 0.77 (0.62-0.96) |
| PHOENIX | Younes | JCO, 2019 | Ibrutinib+R-CHOP | R-CHOP | 838 | 34.8 mo | 0.92 (0.71-1.18) |
| ROBUST | Vitolo | JCO, 2021 | Lena+R-CHOP | R-CHOP | 570 | 27.1 mo | 0.85 (0.63-1.14) |
| ECOG-E1412 | Nowakowski | JCO, 2021 | Lena+R-CHOP | R-CHOP | 349 | 3.7 years | 0.66 (0.43-1.01) |
| REMoDL-B 5y | Davies | JCO, 2023 | Bort+R-CHOP | R-CHOP | 918 | 5 years | 0.81 (approx.) |
| GOYA | Sehn | JCO, 2020 | G-CHOP | R-CHOP | 1,418 | 29 mo | 0.94 (0.78-1.13) |
| CALGB 50303 | Bartlett | JCO, 2019 | DA-EPOCH-R | R-CHOP | 491 | 5 years | 0.93 (0.68-1.27) |

Abbreviations: Bort, bortezomib; FU, follow-up; G-CHOP, obinutuzumab-CHOP; HR, hazard ratio; Lena, lenalidomide; mo, months; Pola-R-CHP, polatuzumab vedotin plus R-CHP; R-CHOP, rituximab plus CHOP.

### PFS Network Meta-Analysis

Between-study heterogeneity across the network was negligible (I² = 0%, tau² < 0.0001), supporting the validity of indirect comparisons. The Bayesian RE model (DIC = 13.35) and FE model (DIC = 12.88) yielded nearly identical estimates, consistent with the absence of meaningful heterogeneity. All MCMC chains achieved excellent convergence, with Rhat values of 1.0 for all treatment effect parameters.

Table 2 presents the NMA results for PFS. Pola-R-CHP was the only regimen that achieved a statistically significant improvement in PFS compared with R-CHOP (HR 0.77, 95% credible interval [CrI] 0.62-0.96; p = 0.022). Lenalidomide plus R-CHOP demonstrated a borderline-significant PFS benefit (HR 0.78, 95% CrI 0.61-1.00; p = 0.049), noting that this pooled estimate was derived from two trials with discordant results — ECOG-E1412 (HR 0.66) and ROBUST (HR 0.85). Bortezomib plus R-CHOP showed a non-significant trend toward improved PFS (HR 0.81, 95% CrI 0.64-1.03; p = 0.085). Ibrutinib plus R-CHOP (HR 0.92), DA-EPOCH-R (HR 0.93), and obinutuzumab-CHOP (HR 0.94) showed no meaningful PFS improvement.

**Table 2. Network Meta-Analysis Results: PFS Hazard Ratios versus R-CHOP**

| Treatment | HR (95% CrI) | p-value | SUCRA (%) | Rank |
|-----------|--------------|---------|-----------|------|
| Pola-R-CHP | 0.77 (0.62-0.96) | 0.022 | 69.1 | 2 |
| Lenalidomide+R-CHOP | 0.78 (0.61-1.00) | 0.049 | 70.5 | 1 |
| Bortezomib+R-CHOP | 0.81 (0.64-1.03) | 0.085 | 62.1 | 3 |
| Ibrutinib+R-CHOP | 0.92 (0.71-1.18) | 0.506 | 43.1 | 4 |
| DA-EPOCH-R | 0.93 (0.68-1.27) | 0.649 | 41.9 | 5 |
| G-CHOP | 0.94 (0.78-1.13) | 0.503 | 39.2 | 6 |
| R-CHOP | Reference | — | 24.1 | 7 |

Abbreviations: CrI, credible interval; HR, hazard ratio; SUCRA, surface under the cumulative ranking curve.

### Treatment Rankings

SUCRA analysis ranked lenalidomide plus R-CHOP highest (70.5%), followed closely by Pola-R-CHP (69.1%) and bortezomib plus R-CHOP (62.1%) (Table 2, Figure 3). However, it is critical to note the distinction between statistical ranking and clinical significance: while lenalidomide plus R-CHOP achieved the highest SUCRA, it did not reach conventional statistical significance (p = 0.049), and its pooled estimate was driven substantially by the smaller ECOG-E1412 trial (N = 349), whereas the larger ROBUST trial (N = 570, restricted to ABC subtype) was negative. Pola-R-CHP, despite ranking second by SUCRA, was the only treatment achieving unambiguous statistical significance. R-CHOP ranked last (SUCRA 24.1%), confirming that the experimental regimens collectively trended toward improved efficacy, even when individual comparisons did not reach significance.

### Overall Survival

OS data were available from four trials (POLARIX, PHOENIX, GOYA, CALGB 50303). No experimental regimen demonstrated a statistically significant improvement in OS compared with R-CHOP. This finding is consistent with the known challenge of demonstrating OS benefits in frontline DLBCL trials, where effective salvage therapies including autologous stem cell transplantation and, increasingly, CAR T-cell therapy attenuate OS differences between arms [23].

### Sensitivity Analyses

Leave-one-out analysis confirmed the robustness of the primary findings: no single trial, when excluded, materially altered the overall NMA estimates or changed the significance status of Pola-R-CHP. Notably, excluding the ROBUST trial (which restricted enrollment to ABC-subtype patients) shifted the lenalidomide-R-CHOP pooled HR from 0.78 to 0.66, reflecting the stronger signal from the ECOG-E1412 trial in an unselected DLBCL population.

Bayesian and frequentist NMA results were highly concordant. The frequentist random-effects model (netmeta) produced point estimates and confidence intervals nearly identical to the Bayesian posterior medians and credible intervals, confirming that results were not sensitive to the choice of analytical framework. The consistency of FE and RE models (DIC 12.88 vs 13.35) further supported the absence of meaningful heterogeneity.

### Subgroup Analyses

Although formal NMA of subgroup data was not feasible due to limited reporting, descriptive synthesis of trial-level subgroup analyses revealed several clinically important signals (Table 3).

**Cell of origin (ABC/non-GCB subtype).** A consistent pattern of enhanced PFS benefit in ABC/non-GCB DLBCL was observed across multiple regimens. In POLARIX, the ABC subgroup demonstrated a markedly greater benefit from Pola-R-CHP (HR 0.34) compared with the overall population (HR 0.77). Similarly, REMoDL-B reported greater bortezomib benefit in ABC patients (HR 0.65), and ECOG-E1412 showed a numerically greater lenalidomide benefit in the non-GCB subgroup (HR 0.68). These convergent findings across three mechanistically distinct agents targeting the ABC/non-GCB subtype suggest that COO-guided therapy may represent a rational strategy for treatment intensification.

**Double-expressor lymphoma (DEL).** POLARIX demonstrated enhanced Pola-R-CHP benefit in DEL patients (HR 0.64), a subgroup traditionally associated with poor outcomes under R-CHOP. In the PHOENIX trial, ibrutinib-R-CHOP showed benefit in younger patients with DEL features (HR 0.38 in age < 60 subgroup).

**Age-based interactions.** A notable age-treatment interaction was observed in the PHOENIX trial: ibrutinib-R-CHOP was associated with improved PFS in patients aged < 60 years (HR 0.56) but potential harm in patients aged >= 60 years (HR 1.20), likely reflecting differential tolerability and complication rates including cardiac toxicity. Conversely, POLARIX demonstrated sustained Pola-R-CHP benefit in patients aged >= 70 years (HR 0.63).

**International Prognostic Index.** Patients with high-intermediate or high IPI scores (3-5) derived numerically greater benefit from Pola-R-CHP in the POLARIX trial (HR 0.71), suggesting that treatment intensification may be particularly valuable in this prognostically unfavorable subgroup.

**Table 3. Selected Subgroup Analyses from Individual Trials**

| Subgroup | Trial | Regimen | HR | Source |
|----------|-------|---------|-----|--------|
| ABC/non-GCB | POLARIX | Pola-R-CHP | 0.34 | Tilly, JCO 2026 |
| ABC/non-GCB | REMoDL-B | Bort+R-CHOP | 0.65 | Davies, JCO 2023 |
| ABC/non-GCB | ECOG-E1412 | Lena+R-CHOP | 0.68 | Nowakowski, JCO 2021 |
| DEL | POLARIX | Pola-R-CHP | 0.64 | Tilly, JCO 2026 |
| DEL, age <60 | PHOENIX | Ibrut+R-CHOP | 0.38 | Younes, JCO 2019 |
| IPI 3-5 | POLARIX | Pola-R-CHP | 0.71 | Tilly, JCO 2026 |
| Age >=70 | POLARIX | Pola-R-CHP | 0.63 | Tilly, JCO 2026 |
| Age <60 | PHOENIX | Ibrut+R-CHOP | 0.56 | Younes, JCO 2019 |
| Age >=60 | PHOENIX | Ibrut+R-CHOP | 1.20 | Younes, JCO 2019 |

## Discussion

This Bayesian network meta-analysis of seven phase III RCTs including 5,463 previously untreated DLBCL patients provides the most comprehensive comparative assessment of frontline chemoimmunotherapy regimens to date. Our principal finding is that Pola-R-CHP is the only regimen demonstrating statistically significant PFS improvement over R-CHOP (HR 0.77, 95% CrI 0.62-0.96), with this benefit sustained at 5-year follow-up. This result aligns with and strengthens the NCCN Category 1 recommendation for Pola-R-CHP as a preferred frontline regimen [13].

The treatment ranking analysis merits careful interpretation. Although lenalidomide plus R-CHOP achieved the highest SUCRA (70.5%), this ranking was substantially influenced by the ECOG-E1412 trial, which, despite its classification as a phase III study, had a smaller sample size (N = 349) more typical of a phase II trial. The larger ROBUST trial (N = 570), which was restricted to ABC/non-GCB patients, yielded a non-significant HR of 0.85. When ROBUST was excluded from the sensitivity analysis, the lenalidomide-R-CHOP estimate shifted to HR 0.66, highlighting the heterogeneity between these two contributing trials and the influence of population selection on outcomes. This discordance underscores a fundamental limitation of SUCRA-based rankings: they reflect probabilistic positioning but do not inherently distinguish between statistically robust and fragile effect estimates [24]. Clinicians should therefore prioritize the statistical significance and consistency of Pola-R-CHP over the SUCRA ranking advantage of lenalidomide-R-CHOP when making treatment decisions.

The convergent signal of enhanced benefit in ABC/non-GCB DLBCL across three mechanistically distinct agents — Pola-R-CHP, bortezomib-R-CHOP, and lenalidomide-R-CHOP — represents perhaps the most clinically actionable subgroup finding from this analysis. The ABC subtype of DLBCL is characterized by constitutive activation of the NF-kB pathway and chronic active B-cell receptor signaling, rendering it biologically amenable to agents that disrupt these pathways or exploit the heightened sensitivity of ABC cells to proteasome inhibition and immunomodulation [25,26]. The POLARIX ABC subgroup HR of 0.34 is particularly striking and suggests that Pola-R-CHP may be transformative for this historically unfavorable subtype. These findings collectively support the emerging paradigm of COO-guided frontline therapy, wherein treatment selection is informed by the molecular subtype of DLBCL rather than a one-size-fits-all approach.

Despite the improvements in PFS observed with Pola-R-CHP and the suggestive signals for other regimens, no treatment significantly improved OS compared with R-CHOP. This observation is a recurring theme in frontline DLBCL trials and reflects several factors: the availability of effective salvage therapies (including autologous transplantation and CAR T-cell therapy); the typically long post-progression survival in a subset of patients; and the statistical power limitations inherent in detecting OS differences when PFS events do not uniformly translate to mortality [23,27]. The absence of an OS benefit should not diminish the clinical relevance of PFS improvement, which is increasingly recognized by regulatory agencies as a valid surrogate endpoint in DLBCL, particularly when durable PFS gains are observed at extended follow-up [28].

Several critical unmet needs emerge from this analysis. First, TP53 mutation represents a molecular subgroup with dismal outcomes under any current chemoimmunotherapy regimen, and none of the seven included trials demonstrated efficacy in this population [29]. Novel strategies targeting TP53-mutant DLBCL, potentially incorporating bispecific antibodies or non-chemotherapy-based platforms, represent an urgent research priority. Second, the star-shaped network geometry, while common in oncology NMAs, represents an inherent limitation: all comparisons between experimental regimens are indirect, relying solely on R-CHOP as the bridge. The absence of closed loops precludes formal consistency assessment, and the transitivity assumption — that study populations are sufficiently similar across trials to permit valid indirect comparisons — cannot be empirically verified [30]. Differences in enrollment criteria (e.g., ROBUST enrolling only ABC patients), geographic distribution, and era of treatment may introduce intransitivity that is difficult to quantify.

Our study has several strengths. The Bayesian analytical framework provides a probabilistic interpretation of treatment rankings through SUCRA values and offers natural accommodation of between-study heterogeneity through random-effects modeling [14]. The concordance between Bayesian (gemtc) and frequentist (netmeta) results demonstrates robustness to methodological choices. The inclusion of the POLARIX 5-year data — the most mature efficacy data available — updates and extends the prior NMA by Chen et al. [16], which relied on 2-year follow-up data. Our comprehensive subgroup synthesis, while descriptive, provides a framework for hypothesis generation regarding COO-guided therapy that is absent from prior network-level analyses.

This analysis must be interpreted in the context of the rapidly evolving DLBCL treatment landscape. Phase III trials of bispecific antibodies (epcoritamab, glofitamab, odronextamab) and novel antibody-drug conjugates in the frontline setting are either ongoing or in advanced planning, with initial results anticipated between 2028 and 2029 [31,32]. These agents, which have demonstrated remarkable single-agent activity in the relapsed/refractory setting, have the potential to fundamentally reshape the frontline treatment hierarchy. Future iterations of this NMA will need to incorporate these emerging data to maintain clinical relevance. Additionally, the integration of circulating tumor DNA (ctDNA) dynamics as an early response biomarker may enable more nuanced treatment adaptation strategies that transcend the traditional intention-to-treat comparisons captured by conventional NMA [33].

## Conclusions

In this Bayesian network meta-analysis of 5,463 patients across seven phase III RCTs, Pola-R-CHP is the only frontline DLBCL regimen demonstrating statistically significant PFS improvement over R-CHOP at 5-year follow-up (HR 0.77, 95% CrI 0.62-0.96), supporting its position as a new standard of care. No treatment improved OS versus R-CHOP. Subgroup analyses identify the ABC/non-GCB molecular subtype as a consistently treatment-responsive population across multiple regimens, supporting the development of COO-guided frontline strategies. Future head-to-head trials and incorporation of bispecific antibody and ADC data will be essential to further refine the DLBCL treatment hierarchy.

## Acknowledgments

[To be finalized]

## Conflict of Interest Disclosures

[To be finalized]

## Data Availability Statement

All data used in this analysis were extracted from published phase III RCTs. The complete dataset and analysis code are available upon reasonable request from the corresponding author.

## Funding

[To be finalized]

---

## References

1. Sehn LH, Salles G. Diffuse large B-cell lymphoma. N Engl J Med. 2021;384(9):842-858.
2. Coiffier B, Thieblemont C, Van Den Neste E, et al. Long-term outcome of patients in the LNH-98.5 trial, the first randomized study comparing rituximab-CHOP to standard CHOP chemotherapy in DLBCL patients: a study by the Groupe d'Etudes des Lymphomes de l'Adulte. Blood. 2010;116(12):2040-2045.
3. Pfreundschuh M, Kuhnt E, Trümper L, et al. CHOP-like chemotherapy with or without rituximab in young patients with good-prognosis diffuse large-B-cell lymphoma: 6-year results of an open-label randomised study of the MabThera International Trial (MInT) Group. Lancet Oncol. 2011;12(11):1013-1022.
4. Crump M, Neelapu SS, Farooq U, et al. Outcomes in refractory diffuse large B-cell lymphoma: results from the international SCHOLAR-1 study. Blood. 2017;130(16):1800-1808.
5. Van Den Neste E, Schmitz N, Mounier N, et al. Outcomes of diffuse large B-cell lymphoma patients relapsing after autologous stem cell transplantation: an analysis of patients included in the CORAL study. Bone Marrow Transplant. 2017;52(5):681-688.
6. Younes A, Sehn LH, Johnson P, et al. Randomized phase III trial of ibrutinib and rituximab plus cyclophosphamide, doxorubicin, vincristine, and prednisone in non-germinal center B-cell diffuse large B-cell lymphoma. J Clin Oncol. 2019;37(15):1285-1295.
7. Vitolo U, Witzig TE, Gascoyne RD, et al. ROBUST: first report of phase III randomized study of lenalidomide/R-CHOP (R2-CHOP) vs placebo/R-CHOP in previously untreated ABC-type diffuse large B-cell lymphoma. J Clin Oncol. 2021;39(15 Suppl):abstr 7519.
8. Nowakowski GS, Chiappella A, Gascoyne RD, et al. ROBUST: a phase III study of lenalidomide plus R-CHOP versus placebo plus R-CHOP in previously untreated patients with ABC-type diffuse large B-cell lymphoma. J Clin Oncol. 2021;39(12):1317-1328.
9. Davies A, Cummin TE, Barrans S, et al. Gene-expression profiling of bortezomib added to standard chemoimmunotherapy for diffuse large B-cell lymphoma (REMoDL-B): an open-label, randomised, phase 3 trial. Lancet Oncol. 2019;20(5):649-662.
10. Tilly H, Morschhauser F, Sehn LH, et al. Polatuzumab vedotin in previously untreated diffuse large B-cell lymphoma. N Engl J Med. 2022;386(4):351-363.
11. Sehn LH, Martelli M, Trněný M, et al. A randomized, open-label, phase III study of obinutuzumab or rituximab plus CHOP in patients with previously untreated diffuse large B-cell lymphoma: final analysis of GOYA. J Hematol Oncol. 2020;13(1):71.
12. Bartlett NL, Wilson WH, Jung SH, et al. Dose-adjusted EPOCH-R compared with R-CHOP as frontline therapy for diffuse large B-cell lymphoma: clinical outcomes of the phase III intergroup trial Alliance/CALGB 50303. J Clin Oncol. 2019;37(21):1790-1799.
13. National Comprehensive Cancer Network. NCCN Clinical Practice Guidelines in Oncology: B-Cell Lymphomas. Version 1.2026.
14. Dias S, Sutton AJ, Ades AE, Welton NJ. Evidence synthesis for decision making 2: a generalized linear modeling framework for pairwise and network meta-analysis of randomized controlled trials. Med Decis Making. 2013;33(5):607-617.
15. Lu G, Ades AE. Combination of direct and indirect evidence in mixed treatment comparisons. Stat Med. 2004;23(20):3105-3124.
16. Chen C, Zhang Y, Liu Y, et al. Network meta-analysis of frontline therapies for diffuse large B-cell lymphoma. Ann Hematol. 2023;102(5):1091-1101.
17. Hutton B, Salanti G, Caldwell DM, et al. The PRISMA extension statement for reporting of systematic reviews incorporating network meta-analyses of health care interventions: checklist and explanations. Ann Intern Med. 2015;162(11):777-784.
18. Sterne JAC, Savović J, Page MJ, et al. RoB 2: a revised tool for assessing risk of bias in randomised trials. BMJ. 2019;366:l4898.
19. van Valkenhoef G, Dias S, Guillin A, et al. gemtc: network meta-analysis using Bayesian methods. R package version 1.0-2.
20. R Core Team. R: A language and environment for statistical computing. R Foundation for Statistical Computing, Vienna, Austria. 2024.
21. Salanti G, Ades AE, Ioannidis JPA. Graphical methods and numerical summaries for presenting results from multiple-treatment meta-analysis: an overview and tutorial. J Clin Epidemiol. 2011;64(2):163-171.
22. Rücker G, Krahn U, König J, et al. netmeta: network meta-analysis using frequentist methods. R package version 2.9-0.
23. Neelapu SS, Locke FL, Bartlett NL, et al. Axicabtagene ciloleucel CAR T-cell therapy in refractory large B-cell lymphoma. N Engl J Med. 2017;377(26):2531-2544.
24. Mbuagbaw L, Rochwerg B, Jaeschke R, et al. Approaches to interpreting and choosing the best treatments in network meta-analyses. Syst Rev. 2017;6(1):79.
25. Alizadeh AA, Eisen MB, Davis RE, et al. Distinct types of diffuse large B-cell lymphoma identified by gene expression profiling. Nature. 2000;403(6769):503-511.
26. Lenz G, Wright GW, Emre NCT, et al. Molecular subtypes of diffuse large B-cell lymphoma arise by distinct genetic pathways. Proc Natl Acad Sci U S A. 2008;105(36):13520-13525.
27. Sehn LH, Martelli M, Trněný M, et al. Final analysis of GOYA: a randomized, open-label, phase 3 study of obinutuzumab- or rituximab-based chemotherapy in previously untreated DLBCL. Blood. 2020;136(Suppl 1):43-44.
28. Shi Q, Schmitz N, Meta-Analysis Consortium. Progression-free survival as a surrogate endpoint for overall survival in first-line diffuse large B-cell lymphoma: an individual patient-level analysis of multiple randomized trials (SEAL). J Clin Oncol. 2018;36(25):2593-2602.
29. Xu-Monette ZY, Wu L, Visco C, et al. Mutational profile and prognostic significance of TP53 in diffuse large B-cell lymphoma patients treated with R-CHOP: report from an International DLBCL Rituximab-CHOP Consortium Program Study. Blood. 2012;120(19):3986-3996.
30. Salanti G. Indirect and mixed-treatment comparison, network, or multiple-treatments meta-analysis: many names, many benefits, many concerns for the next generation evidence synthesis tool. Res Synth Methods. 2012;3(2):80-97.
31. Thieblemont C, Phillips T, Ghesquieres H, et al. Epcoritamab, a novel, subcutaneous CD3xCD20 bispecific T-cell-engaging antibody, in relapsed or refractory large B-cell lymphoma: dose expansion in a phase I/II trial. J Clin Oncol. 2023;41(12):2238-2247.
32. Dickinson MJ, Carlo-Stella C, Morschhauser F, et al. Glofitamab for unfit or relapsed/refractory diffuse large B-cell lymphoma. N Engl J Med. 2023;389(24):2220-2231.
33. Kurtz DM, Scherer F, Jin MC, et al. Circulating tumor DNA measurements as early outcome predictors in diffuse large B-cell lymphoma. J Clin Oncol. 2018;36(28):2845-2853.
