# NMA Completion Checklist (Pre-Submission)

**Purpose**: Systematic checklist for Network Meta-Analysis manuscripts before journal submission.

**Use when**: You're at Stage 09 (QA) and preparing final submission package.

**Time**: 30-45 min to review all items

---

## 📊 **Data & Analysis (7 items)**

- [ ] **01. Network graph generated**
  - File: `06_analysis/figures/network_graph.png`
  - Shows all treatments as nodes, studies as edges
  - 300 DPI, clear labels
  - **Missing?** Run `nma_03_network_graph.R`

- [ ] **02. Network connectivity verified**
  - All treatments connected (no isolated nodes)
  - Sufficient direct comparisons (≥2 studies per comparison ideal)
  - **Tool**: `uv run validate_nma_outputs.py --root projects/<name>`

- [ ] **03. League table complete**
  - File: `06_analysis/tables/league_table.png` or `.csv`
  - Heatmap: `06_analysis/tables/league_table_heatmap.png`
  - All n*(n-1)/2 pairwise comparisons present
  - Upper triangle: effect estimates (RR/OR/HR)
  - Lower triangle: credible/confidence intervals
  - Heatmap: color-coded by effect direction/magnitude, bold = significant
  - **Missing?** Run `nma_10_tables.R`

- [ ] **04. Treatment rankings generated**
  - Files: `06_analysis/tables/sucra_rankings.csv`, `figures/rankograms.png`
  - **Bayesian**: SUCRA scores (0-100%) with uncertainty intervals
  - **Frequentist**: P-scores (sensitivity analysis)
  - All treatments ranked
  - **Missing?** Run `nma_07_ranking.R`

- [ ] **05. Inconsistency assessment performed**
  - **Node-splitting** analysis (gemtc or netmeta)
  - **Design-by-treatment interaction** test
  - Net heat plot (inconsistency visualization)
  - Results reported in manuscript
  - **Missing?** Run `nma_05_inconsistency.R`

- [ ] **06. Bayesian convergence diagnostics**
  - **Gelman-Rubin** diagnostic (R̂ < 1.05)
  - **Trace plots** (good mixing)
  - **Autocorrelation** plots (<0.1 after lag 10)
  - **Iterations**: ≥10,000 (20,000 ideal)
  - **Burn-in**: ≥5,000
  - Documented in supplementary materials
  - **Tool**: Check `nma_04_models.R` output

- [ ] **07. Sensitivity analysis complete**
  - **Frequentist concordance** (netmeta vs gemtc)
  - **Leave-one-out** analysis (influential studies)
  - **Subgroup analysis** (if applicable)
  - Results concordant with primary Bayesian analysis
  - **Missing?** Run `nma_09_sensitivity.R`

---

## 📝 **Reporting (10 items)**

- [ ] **08. PRISMA-NMA checklist filled**
  - File: `09_qa/prisma_nma_checklist.md`
  - **32 items** (27 standard + 5 NMA-specific)
  - All items addressed or marked NA with justification
  - **Tool**: `uv run init_reporting_checklists.py --type prisma-nma`

- [ ] **09. Methods section describes NMA approach**
  - **Software**: gemtc (primary), netmeta (sensitivity)
  - **Model**: Random-effects consistency model
  - **Priors**: Vague/non-informative (gemtc)
  - **Iterations**: n.iter, burn-in, thin reported
  - **Convergence criteria**: R̂, ESS described

- [ ] **10. Transitivity assessment documented**
  - **Assumption**: Studies are similar enough to mix direct/indirect evidence
  - **Check**: Study characteristics table compared across comparisons
  - **Risk factors**: Age, disease severity, treatment dose, follow-up
  - Reported in Methods + Results
  - **Reference**: `ma-network-meta-analysis/references/nma-assumptions.md`

- [ ] **11. Consistency assessment reported**
  - **Method**: Node-splitting + design-by-treatment
  - **Results**: No significant inconsistency detected (or acknowledged)
  - **Interpretation**: Can we trust indirect evidence?
  - Reported in Results + Table S9

- [ ] **12. Treatment rankings interpreted cautiously**
  - **SUCRA scores** reported with uncertainty
  - **Avoid overclaims**: "Treatment X ranked highest (SUCRA 0.85, 95% CrI 0.62-0.97)"
  - **Not**: "Treatment X is definitively best"
  - Acknowledge ranking uncertainty in Discussion

- [ ] **13. Network geometry described**
  - **Number of treatments**: N treatments
  - **Number of comparisons**: Direct vs indirect
  - **Network structure**: Star, loop, fully connected?
  - Reported in Results + Table S6

- [ ] **14. Effect estimates for all comparisons**
  - **Primary outcome**: All pairwise RR/OR/HR in league table
  - **Secondary outcomes**: If multiple outcomes analyzed
  - **Credible intervals**: 95% CrI (Bayesian) or 95% CI (frequentist)
  - Forest plots for key comparisons

- [ ] **15. CINeMA GRADE assessment complete**
  - File: `08_reviews/cinema_assessment.csv`
  - **6 Domains assessed** (per comparison):
    1. Within-study bias (Risk of bias)
    2. Reporting bias (Publication bias)
    3. Indirectness (+ **Intransitivity**)
    4. Imprecision (+ **Contribution matrix**)
    5. Heterogeneity (Inconsistency)
    6. **Incoherence** (Direct vs indirect agreement)
  - **Judgment levels**: No concerns / Some concerns (-1) / Major concerns (-2)
  - **Per comparison**: Rate each pairwise comparison separately
  - **Tool**: https://cinema.ispm.unibe.ch/ (required for Lancet/JAMA/BMJ)
  - Reported in Table S10 (Supplementary)
  - **Reference**: Nikolakopoulou et al. BMJ 2020;371:m3983
  - **Guide**: `ma-peer-review/references/grade-assessment-guide.md`

- [ ] **15b. Staged certainty workflow applied (Brignardello-Petersen 2018)**
  - Direct evidence rated WITHOUT imprecision first (4 domains only)
  - Efficiency shortcut evaluated (high certainty direct + dominant contribution?)
  - Indirect evidence rated from lowest certainty in first-order loop (if applicable)
  - Network estimate certainty = higher of direct/indirect, then coherence + imprecision
  - Local incoherence checked per comparison (not just global test)
  - When incoherence detected, higher-certainty estimate noted for clinical decisions
  - **Guide**: `ma-network-meta-analysis/references/nma-grade-certainty-workflow.md`

- [ ] **16. Limitations acknowledged**
  - **Network structure**: Sparse comparisons, lack of direct evidence
  - **Transitivity**: Potential violations (different populations, doses)
  - **Inconsistency**: If detected, discussed
  - **Publication bias**: Funnel plot asymmetry (if <10 studies, acknowledged)
  - **Study quality**: Risk of bias concerns

- [ ] **17. Reporting checklist items mapped to manuscript**
  - Each PRISMA-NMA item → section/page number
  - No "NA" without justification
  - Reviewer can verify all items addressed

---

## 📁 **Supplementary Materials (8 items)**

- [ ] **18. Table S6: Network geometry**
  - Number of treatments, comparisons (direct/indirect)
  - Network structure description
  - **Tool**: Export from `nma_03_network_graph.R`

- [ ] **19. Table S7: League table**
  - All pairwise comparisons
  - Upper/lower triangle format
  - **Format**: PNG (300 DPI) via `gt` package
  - **Heatmap**: `league_table_heatmap.png` — color-coded version (Figure S9)
  - **Tool**: `nma_10_tables.R`

- [ ] **20. Table S8: Treatment rankings**
  - SUCRA scores (Bayesian primary)
  - P-scores (frequentist sensitivity)
  - Rank probabilities
  - **Tool**: `nma_07_ranking.R`

- [ ] **21. Table S9: Inconsistency assessment**
  - Node-splitting results (direct vs indirect)
  - Design-by-treatment p-values
  - Interpretation
  - **Tool**: `nma_05_inconsistency.R`

- [ ] **22. Table S10: CINeMA GRADE**
  - Per-comparison certainty ratings
  - Downgrade reasons (intransitivity, incoherence)
  - **Source**: https://cinema.ispm.unibe.ch/

- [ ] **23. Figure S4: Network graph**
  - 300 DPI, clear labels
  - Node size ∝ sample size
  - Edge width ∝ number of studies
  - **Tool**: `nma_03_network_graph.R`

- [ ] **24. Figure S5: Rankograms**
  - Probability distribution per treatment rank
  - All treatments shown
  - **Tool**: `nma_07_ranking.R`

- [ ] **25. Figure S6: Contribution matrix**
  - Shows which direct comparisons inform which network estimates
  - **Tool**: `netcontrib()` in netmeta
  - **Optional but recommended** for transparency

---

## ✅ **Completion Criteria**

**Ready to submit if**:

- ✅ All 25 items checked
- ✅ PRISMA-NMA: 32/32 items addressed
- ✅ CINeMA: All key comparisons assessed
- ✅ Convergence: R̂ < 1.05 for all parameters
- ✅ Inconsistency: Assessed and discussed
- ✅ Supplementary: Tables S6-S10 + Figures S4-S6 present

**Not ready if**:

- ❌ Any convergence issues (R̂ > 1.05)
- ❌ Significant inconsistency without discussion
- ❌ Missing CINeMA assessment
- ❌ PRISMA-NMA <32 items
- ❌ Overclaims detected (use `uv run claim_audit.py`)

---

## 🛠️ **Automated Checks**

Run these scripts to validate completion:

```bash
cd /Users/htlin/meta-pipe/tooling/python

# 1. NMA-specific validation
uv run ../../ma-network-meta-analysis/scripts/validate_nma_outputs.py \
  --root ../../projects/<project-name> \
  --out ../../projects/<project-name>/09_qa/nma_validation.md

# 2. Publication readiness score
uv run ../../ma-end-to-end/scripts/publication_readiness_score.py \
  --root ../../projects/<project-name> \
  --out ../../projects/<project-name>/09_qa/readiness_score.md

# 3. PRISMA-NMA checklist
uv run ../../ma-publication-quality/scripts/init_reporting_checklists.py \
  --root ../../projects/<project-name>/.. --type prisma-nma \
  --out ../../projects/<project-name>/09_qa/prisma_nma_checklist.md

# 4. Claim audit
uv run ../../ma-publication-quality/scripts/claim_audit.py \
  --abstract ../../projects/<project-name>/07_manuscript/00_abstract.qmd \
  --results ../../projects/<project-name>/07_manuscript/03_results.qmd \
  --discussion ../../projects/<project-name>/07_manuscript/04_discussion.qmd \
  --out ../../projects/<project-name>/09_qa/claim_audit.md
```

**Expected output**:

- `nma_validation.md`: All NMA outputs validated
- `readiness_score.md`: Score ≥95% (ready to submit)
- `prisma_nma_checklist.md`: 32/32 items ✅
- `claim_audit.md`: 0 critical/high issues

---

## 📚 **References**

- **PRISMA-NMA**: Hutton et al. (2015) - https://doi.org/10.7326/M14-2385
- **CINeMA**: Nikolakopoulou et al. (2020) - https://doi.org/10.1136/bmj.m3983
- **NMA Guidelines**: NICE DSU TSD series - http://nicedsu.org.uk/
- **gemtc Package**: van Valkenhoef et al. (2016) - https://doi.org/10.18637/jss.v068.i08

---

## 💡 **Common Pitfalls**

1. **Using PRISMA 2020 instead of PRISMA-NMA** (missing 5 NMA-specific items)
2. **Not assessing intransitivity** (just assumed, not checked)
3. **Not reporting Bayesian convergence** (R̂, trace plots)
4. **Ranking overclaims** ("Treatment X is best" vs "ranked highest, SUCRA 0.85")
5. **Missing CINeMA** (GRADE for NMA is mandatory per 2020 guidelines)
6. **Not comparing Bayesian vs frequentist** (no sensitivity analysis)
7. **Ignoring inconsistency** (detected but not discussed)

---

## ⏱️ **Time Budget**

| Task | Time |
|------|------|
| Review checklist items 1-7 (Data) | 10 min |
| Review checklist items 8-17 (Reporting) | 15 min |
| Review checklist items 18-25 (Supplementary) | 10 min |
| Run automated checks | 5 min |
| Fix identified issues | 30-60 min |
| **Total** | **70-100 min** |

---

## 🎯 **Next Steps After Completion**

1. **Final QA**: Run `publication_readiness_score.py` → aim for 95-100%
2. **Cover letter**: Draft highlighting NMA methodology + key findings
3. **Journal selection**: Target NMA-friendly journals (see `ma-publication-quality/references/journal-formatting.md`)
4. **Submission**: Upload manuscript + supplementary + checklist

---

**Last updated**: 2026-02-17 (Phase 2 enhancements)
