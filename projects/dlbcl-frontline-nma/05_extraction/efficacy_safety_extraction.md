# Data Extraction: Frontline DLBCL Phase III RCTs for Network Meta-Analysis

**Extracted**: 2026-03-25
**Sources**: PubMed, NEJM, JCO, Lancet Oncology, Blood Advances, FDA Clinical Review
**Extractor**: Claude Code (web search-assisted)

> **IMPORTANT**: Values marked with `*` require verification against the full-text publication.
> Values marked `NR` = Not Reported in publicly available sources.
> All HRs are for intervention vs R-CHOP (HR <1 favors intervention).

---

## Table 1: Primary Efficacy Outcomes

| Trial | Intervention | N (ITT) | Arms (n/n) | Median F/U (mo) | PFS HR (95% CI) | P-value | OS HR (95% CI) | P-value |
|-------|-------------|---------|-------------|-----------------|-----------------|---------|----------------|---------|
| **POLARIX 5y** | Pola-R-CHP | 879 | 440/439 | 64.1 | **0.77** (0.62-0.97) | NR (5y) | **0.85** (0.63-1.15) | NR (5y) |
| POLARIX 2y (primary) | Pola-R-CHP | 879 | 440/439 | 28.2 | **0.73** (0.57-0.95) | 0.0177 | **0.94** (0.65-1.37) | 0.75 |
| **PHOENIX** | R-CHOP+ibrutinib | 838 | 419/419 | 34.8 | **0.917** (0.710-1.183) | 0.5027 | **0.991** (0.712-1.380) | 0.9593 |
| **ROBUST** | R2-CHOP (len) | 570 | 285/285 | 27.1 | **0.85** (0.63-1.14) | 0.29 | NR (immature) | NR |
| **ECOG-E1412** | R2CHOP (len) | 349* | 145/135 (eval) | 36.0 | **0.66** (0.43-1.01) | 0.03 (1-sided) | **0.67** (NR) | 0.05 (1-sided) |
| **REMoDL-B** (primary) | RB-CHOP (bort) | 918 | 459/459 | 29.7 | **0.86** (0.65-1.13) | 0.28 | **0.89** (0.62-1.28) | 0.52 |
| **REMoDL-B 5y** | RB-CHOP (bort) | 918 | 459/459 | 64.0 | **0.81** (NR) | 0.085 | **0.86** (NR) | 0.32 |
| **GOYA** (final) | G-CHOP (obi) | 1418 | 704/710 (4 excluded) | 48.0 | **0.94** (0.78-1.12) | 0.48 | **1.02** (0.81-1.29) | 0.84 |
| **CALGB 50303** | DA-EPOCH-R | 491 | 241/250 | 62.4 | **0.93** (0.68-1.27) | 0.65 | **1.09** (0.75-1.59) | 0.64 |

**Notes**:
- POLARIX: Use 5-year data (HR 0.77) as primary for NMA; 2-year data (HR 0.73) for sensitivity analysis
- PHOENIX: Enrolled non-GCB DLBCL only (75.9% ABC by GEP)
- ROBUST: Enrolled ABC-type DLBCL only; OS immature at publication
- ECOG-E1412: Randomized phase II (not phase III); 349 randomized, 280 evaluable for efficacy; one-sided p-values
- REMoDL-B: Use 5-year data (HR 0.81) for NMA; primary 30-month data (HR 0.86) for sensitivity
- GOYA: Final analysis published 2020 (J Hematol Oncol)

---

## Table 2: Response Rates

| Trial | CR (Intervention) | CR (R-CHOP) | ORR (Intervention) | ORR (R-CHOP) |
|-------|-------------------|-------------|---------------------|--------------|
| **POLARIX** | 78.0% | 74.0% | NR | NR |
| **PHOENIX** | 67.3% | 68.0% | NR | NR |
| **ROBUST** | 69% | 65% | 91% | 91% |
| **ECOG-E1412** | 73% | 68% | 97% | 92% |
| **REMoDL-B** | NR* | NR* | NR | NR |
| **GOYA** | 56.5% | 59.1% | NR | NR |
| **CALGB 50303** | 58.5% | 59.6% | 86.7% | 88.0% |

**Notes**:
- POLARIX CR: End-of-treatment, blinded independent central review
- GOYA CR: CT with PET assessment
- REMoDL-B: CR rates not prominently reported in available sources -- verify in full Lancet Oncology publication
- CALGB 50303: CR/CRu (unconfirmed) rates reported

---

## Table 3: Safety (Grade >=3 AEs & Treatment-Related Mortality)

| Trial | Gr>=3 AE (Intervention) | Gr>=3 AE (R-CHOP) | TRM (Intervention) | TRM (R-CHOP) |
|-------|-------------------------|--------------------|---------------------|---------------|
| **POLARIX** | 60.7% | 59.8% | 3.0% (13/435) | 2.3% (10/438) |
| **PHOENIX** | 89.9% | 87.1% | 4.3% | 2.9% |
| **ROBUST** | 78%* | 71%* | NR (57 deaths total) | NR (62 deaths total) |
| **ECOG-E1412** | NR (total) | NR (total) | 1.2% (2/166) | 4.1% (7/171)* |
| **REMoDL-B** | 50.2% (SAE) / 42.1% (heme Gr3+) | 42.5% (SAE) / 39.8% (heme Gr3+) | 0.9% (4/444) | 1.1% (5/447) |
| **GOYA** | 75.1% | 65.8% | 6.1% (43/702) | 4.4% (31/701) |
| **CALGB 50303** | 98.3% | 78.2% | 2.1% (5/241) | 2.1% (5/250) |

**Notes**:
- ROBUST: Grade 3-4 AE rates (78% vs 71%) from ASCO Post summary; verify against JCO publication
- ECOG-E1412: Individual Gr3+ AEs reported (febrile neutropenia 25% vs 14%, thrombocytopenia 34% vs 13%); total rate NR; TRM: 2 vs 7 grade V events (note: R2CHOP had FEWER treatment deaths)
- REMoDL-B: Hematologic Gr3+ (42.1% vs 39.8%); SAE rate (50.2% vs 42.5%); TRM from safety population
- GOYA: Fatal AEs 6.1% vs 4.4%, primarily infections
- CALGB 50303: DA-EPOCH-R substantially more toxic (98.3% Gr3-5) but equal TRM (2.1% each)

---

## Table 4: POLARIX Subgroup PFS HRs (Exploratory)

### From 2-year primary analysis (NEJM 2022, FDA Clinical Review)

| Subgroup | HR | 95% CI | Note |
|----------|-----|--------|------|
| **Overall ITT** | 0.73 | 0.57-0.95 | Primary endpoint |
| **IPI 3-5** | 0.71 | 0.53-0.95 | Favors Pola-R-CHP |
| **IPI 2** | NR | NR | Subgroup too small for separate reporting |
| **ABC (by GEP)** | 0.34 | 0.21-0.56 | Strong benefit |
| **GCB (by GEP)** | 1.18 | 0.75-1.84 | No benefit (crosses 1) |
| **DEL (IHC)** | 0.63 | 0.42-0.94 | Favors Pola-R-CHP |
| **Non-DEL** | NR | NR | NR |
| **Age >=70** | 0.63 | 0.41-0.96 | 5y analysis; benefit in elderly |
| **Age <60** | NR | NR | No clear benefit per NEJM commentary |
| **No bulky disease** | 0.59 | 0.42-0.83 | |
| **IPI 3-5 + no bulky** | 0.40 | 0.25-0.63 | Strongest benefit subgroup |

### From 5-year update (JCO 2025/2026)

| Subgroup | HR | 95% CI | 5y rate (Pola/R-CHOP) |
|----------|-----|--------|-----------------------|
| **Overall ITT** | 0.77 | 0.62-0.97 | 64.9% / 59.1% |
| **ABC (by GEP)** | NR (5y) | NR | OS: 84.6% / 69.9% |
| **ABC OS** | 0.49 | 0.28-0.88 | Dramatic OS benefit |
| **IPI 3-5 OS** | 0.81 | 0.57-1.15 | 79.2% / 74.7% |

**Notes**:
- COO subgroup HRs (ABC 0.34, GCB 1.18) are from the 2-year analysis by GEP (gene expression profiling); different from IHC-based classification
- The ABC benefit is the most striking subgroup finding across POLARIX
- DEL HR 0.64 (from some sources) vs 0.63 (FDA review) -- slight variation by data source; use FDA review value
- No age <60 vs >=60 HR explicitly published; >=70 HR available from dedicated age subgroup analysis

---

## Table 5: PHOENIX Subgroup Data

### ITT Population (non-GCB only, N=838)

| Subgroup | EFS HR | 95% CI | PFS HR | 95% CI | OS HR | 95% CI |
|----------|--------|--------|--------|--------|-------|--------|
| **All (ITT)** | 0.934 | 0.726-1.200 | 0.917 | 0.710-1.183 | 0.991 | 0.712-1.380 |
| **Age <60** | 0.579 | 0.380-0.881 | 0.556 | 0.359-0.860 | 0.330 | 0.162-0.673 |
| **Age >=60** | 1.228 | 0.887-1.699 | 1.200 | 0.866-1.664 | 1.440 | 0.963-2.152 |
| **ABC (by GEP)** | 0.949 | 0.704-1.279 | NR | NR | NR | NR |

### Double-Expressor Subgroup (from Blood Advances 2023, PMID 36696540)

| Subgroup | N | EFS HR | 95% CI | P | OS HR | 95% CI | P |
|----------|---|--------|--------|---|-------|--------|---|
| **All DE patients** | 234 | 0.646 | 0.424-0.984 | 0.040 | 0.682 | 0.400-1.163 | 0.16 |
| **DE + Age <60** | 97 | 0.381 | 0.193-0.752 | 0.004 | 0.234 | 0.078-0.707 | 0.005 |
| **DE + Age >=60** | 137 | 0.924 | 0.530-1.609 | 0.78 | 1.085 | 0.562-2.095 | 0.81 |

**DE Response Rates**: Ibrutinib+R-CHOP CR 67.5% vs R-CHOP CR 64.9%

**Critical note**: PHOENIX benefit is entirely driven by age <60 subgroup. In age >=60, ibrutinib addition WORSENED outcomes due to toxicity (SAE 63.4% vs 38.2%).

---

## Table 6: REMoDL-B Subgroup Data (5-year update, JCO 2023)

| Subgroup | N | 5y PFS HR | 95% CI | P | 5y OS HR | 95% CI | P |
|----------|---|-----------|--------|---|----------|--------|---|
| **Overall** | 801 (profiled) | 0.81 | NR | 0.085 | 0.86 | NR | 0.32 |
| **ABC** | 249 | 0.65 | 0.43-0.98 | 0.041 | 0.58 | 0.35-0.95 | 0.032 |
| **GCB** | 469 | 1.05 | 0.74-1.50 | 0.77 | 1.27 | 0.81-1.98 | 0.30 |
| **MHG** | 83 | 0.46 | 0.26-0.84 | 0.011 | 0.62 | 0.32-1.20 | 0.16 |
| **Unclassified** | NR | NR | NR | NR | NR | NR | NR |

---

## Table 7: GOYA Subgroup PFS HRs (Final Analysis)

| Subgroup | PFS HR | 95% CI | 5y PFS (G-CHOP/R-CHOP) |
|----------|--------|--------|-------------------------|
| **Overall** | 0.94 | 0.78-1.12 | 63.8% / 62.6% |
| **GCB** | 0.80 | 0.58-1.12 | 71.0% / 65.5% |
| **ABC** | 0.91 | 0.61-1.36 | 54.3% / 55.7% |
| **Unclassified** | 1.10 | 0.65-1.88 | 57.9% / 62.7% |
| **IPI low-intermediate** | 0.93 | 0.71-1.23 | NR |
| **IPI high-intermediate** | 0.73 | 0.53-1.01 | NR |
| **IPI high** | 1.27 | 0.87-1.86 | NR |

---

## Table 8: ECOG-E1412 Subgroup PFS HRs

| Subgroup | PFS HR | 95% CI | Note |
|----------|--------|--------|------|
| **Overall** | 0.66 | 0.43-1.01 | 3y PFS: 73% vs 61% |
| **ABC** | 0.68 | NR | Co-primary endpoint |
| **GCB** | 0.82 | NR | |
| **Unclassified** | 0.83 | NR | |
| **Unknown** | 0.61 | NR | |

---

## Table 9: CALGB 50303 Subgroup PFS Data

| Subgroup | PFS HR | 95% CI | Note |
|----------|--------|--------|------|
| **Overall** | 0.93 | 0.68-1.27 | No difference |
| **IPI 4-5** | 0.46 | 0.21-1.01 | P=0.052 (trend, post hoc) |
| **ABC** | NR | NR | No significant interaction |
| **GCB** | NR | NR | No significant interaction |

---

## Summary Table for NMA Input (Primary Analysis)

Use these values for the Bayesian NMA:

| Trial | Comparison | PFS HR | 95% CI | Data Maturity | Population |
|-------|-----------|--------|--------|---------------|------------|
| POLARIX | Pola-R-CHP vs R-CHOP | 0.77 | 0.62-0.97 | 5-year | All DLBCL (IPI 2-5) |
| PHOENIX | Ibrutinib+R-CHOP vs R-CHOP | 0.917 | 0.710-1.183 | ~3-year | Non-GCB only |
| ROBUST | R2-CHOP vs R-CHOP | 0.85 | 0.63-1.14 | ~2-year | ABC only |
| ECOG-E1412 | R2CHOP vs R-CHOP | 0.66 | 0.43-1.01 | 3-year | All DLBCL (IPI >=2) |
| REMoDL-B | RB-CHOP vs R-CHOP | 0.81 | NR* | 5-year | All DLBCL |
| GOYA | G-CHOP vs R-CHOP | 0.94 | 0.78-1.12 | ~4-year | All DLBCL |
| CALGB 50303 | DA-EPOCH-R vs R-CHOP | 0.93 | 0.68-1.27 | 5-year | All DLBCL |

### NMA Considerations

1. **Population heterogeneity**: PHOENIX (non-GCB only) and ROBUST (ABC only) enrolled restricted populations. For the overall NMA, consider:
   - Using these in the overall network with a note on transitivity
   - Alternatively, restricting PHOENIX and ROBUST data to ABC/non-GCB subgroup NMA only

2. **REMoDL-B 5y CI**: The 95% CI for the 5-year overall HR (0.81) was not published in the available sources. Use the primary 30-month data (HR 0.86, 95% CI 0.65-1.13) if the 5y CI cannot be obtained.

3. **ECOG-E1412**: Phase II trial (smaller, IPI >=2 only). Consider sensitivity analysis including/excluding this trial.

4. **Follow-up disparity**: Ranges from 27 months (ROBUST) to 64 months (POLARIX, REMoDL-B). Use most mature data per trial but note in evidence table.

5. **PFS definition**: Verify IRC vs investigator-assessed PFS across trials for consistency.

---

## Items Requiring Verification Against Full-Text Publications

1. [ ] POLARIX 5y: p-value for PFS HR; age <60 subgroup HR; IPI 2 subgroup HR
2. [ ] POLARIX 5y: Confirm GCB subgroup PFS HR at 5 years (only ABC OS HR available from searches)
3. [ ] PHOENIX: 95% CI for age <60 PFS HR (0.556; CI 0.359-0.860 -- confirm)
4. [ ] ROBUST: OS HR with 95% CI (data were immature at publication; check for any update)
5. [ ] ROBUST: Grade >=3 AE total rate -- confirm 78% vs 71% from ASCO Post vs JCO
6. [ ] ECOG-E1412: Total Grade >=3 AE rate for both arms (individual AEs reported, total NR)
7. [ ] ECOG-E1412: OS HR 95% CI (HR 0.67, CI NR in available sources)
8. [ ] REMoDL-B primary: CR rates for both arms (NR in available sources)
9. [ ] REMoDL-B 5y: 95% CI for overall PFS HR 0.81 and OS HR 0.86
10. [ ] GOYA: OS HR with 95% CI (1.02, 0.81-1.29 -- confirmed from PMC)
11. [ ] CALGB 50303: COO-specific subgroup HRs (no formal interaction reported)
12. [ ] All trials: Confirm PFS assessment method (IRC vs investigator)

---

## References

### Primary Publications
1. POLARIX 5y: Tilly H et al. JCO 2025/2026. DOI: 10.1200/JCO-25-00925. PMID: 40991874
2. POLARIX 2y: Tilly H et al. NEJM 2022;386:351-363. PMID: 34904799
3. PHOENIX: Younes A et al. JCO 2019;37:1285-1295. PMID: 30901302
4. ROBUST: Vitolo U et al. JCO 2021;39:1295-1306. PMID: 33621109
5. ECOG-E1412: Nowakowski GS et al. JCO 2021;39:1329-1338. PMID: 33555941
6. REMoDL-B: Davies A et al. Lancet Oncol 2019;20:649-662. PMID: 30948276
7. GOYA (final): Sehn LH et al. J Hematol Oncol 2020;13:71. PMID: 32505213
8. CALGB 50303: Bartlett NL et al. JCO 2019;37:1790-1799. PMID: 30939090

### Supplementary Publications
9. REMoDL-B 5y: Davies A et al. JCO 2023;41:2718-2723. PMID: 36972491
10. PHOENIX DEL: Bartlett NL et al. Blood Adv 2023;7:2008-2017. PMID: 36696540
11. GOYA primary: Vitolo U et al. JCO 2017;35:3529-3537. PMID: 28796588
12. POLARIX age >=60: Kuhnl A et al. Haematologica 2025. PMID: 40085955
13. POLARIX COO commentary: Nowakowski GS. Blood 2023;142:2216-2217.

### Sources Used for This Extraction
- [POLARIX 5y - ASCO Post](https://ascopost.com/news/october-2025/combination-therapies-for-diffuse-large-b-cell-lymphoma-5-year-outcomes-of-polarix-trial/)
- [POLARIX 5y - JCO](https://ascopubs.org/doi/10.1200/JCO-25-00925)
- [PHOENIX - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6553835/)
- [PHOENIX DEL - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10188634/)
- [ROBUST - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8078325/)
- [ECOG-E1412 - ASCO Post](https://ascopost.com/news/february-2021/addition-of-lenalidomide-to-r-chop-in-newly-diagnosed-patients-with-dlbcl/)
- [REMoDL-B - Lymphoma Hub](https://lymphomahub.com/medical-information/bortezomib-plus-r-chop-for-distinct-molecular-dlbcl-subtypes-results-from-the-phase-iii-trial-remodl-b)
- [REMoDL-B 5y - ASCO Post](https://ascopost.com/news/april-2023/addition-of-bortezomib-to-r-chop-in-patients-with-dlbcl-according-to-molecular-subgroups/)
- [GOYA final - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC7276080/)
- [CALGB 50303 - Lymphoma Hub](https://lymphomahub.com/medical-information/r-chop-versus-da-epoch-r-as-frontline-therapy-for-dlbcl-results-from-a-phase-iii-trial)
- [FDA Clinical Review - NCBI Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK602516/)
- [POLARIX primary - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11702892/)
- [Polivy HCP](https://www.polivy-hcp.com/newly-diagnosed/rchp/efficacy/trial-results.html)
