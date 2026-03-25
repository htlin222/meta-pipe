# Peer Review Simulation

## Reviewer 1 (Methodologist)

### Strengths
1. Appropriate use of Bayesian NMA with frequentist sensitivity analysis
2. Excellent convergence diagnostics (Rhat = 1.0)
3. Comprehensive sensitivity analyses (leave-one-out, ROBUST exclusion, OS)
4. Star-shaped network well-handled with proper transitivity assessment

### Concerns
1. **PRISMA compliance**: Only PubMed searched. PRISMA requires ≥2 databases. Add Scopus/Embase.
2. **ROBUST population heterogeneity**: ABC-only trial pooled with all-DLBCL trials in the Lena-R-CHOP node. The sensitivity analysis excluding ROBUST shifts HR substantially (0.78 → 0.66). Consider presenting ECOG-E1412 alone as the primary Lena-R-CHOP estimate.
3. **Star network limitation**: With 1 study per comparison (except Lena-R-CHOP), the NMA essentially reproduces individual trial results. The added value is the ranking (SUCRA), but precision of indirect comparisons between novel agents is very limited. Acknowledge this more explicitly.
4. **CINeMA/GRADE**: No formal certainty assessment. This is increasingly required by journals.
5. **Subgroup NMA not performed**: Individual trial subgroup data (COO, DEL, IPI) presented descriptively but not as formal subgroup NMA. This is appropriate given <3 trials per subgroup but should be stated as a limitation.

### Verdict: **Minor revision** — Add Scopus search, complete CINeMA, clarify ROBUST handling

## Reviewer 2 (Clinical Expert)

### Strengths
1. Clinically relevant question — directly informs frontline DLBCL treatment selection
2. Appropriate focus on high-risk subgroups (ABC, DEL, IPI 3-5, elderly)
3. TP53 gap discussion is insightful and forward-looking
4. Timely update with POLARIX 5-year data

### Concerns
1. **PHOENIX enrolled non-GCB only**: The paper should more prominently discuss that PHOENIX was designed for non-GCB DLBCL. Including it in an overall NMA may understate its true effect in the target population.
2. **Follow-up heterogeneity**: Median follow-up ranges from 27 months (ROBUST) to 64 months (POLARIX, REMoDL-B). This affects PFS estimates substantially — early PFS events may be captured differently.
3. **Missing DA-EPOCH-R context**: DA-EPOCH-R showed benefit in IPI 4-5 (HR 0.46, p=0.052). The manuscript should discuss whether R-CHOP is truly the optimal comparator for high-risk patients, or whether Pola-R-CHP should be compared to DA-EPOCH-R.
4. **Clinical actionability**: The Discussion should be clearer about actionable recommendations. Clinicians want to know: "Which regimen for which patient?"

### Verdict: **Minor revision** — Strengthen clinical interpretation and subgroup guidance

## Action Items for Revision
1. Add Scopus search (or explicitly justify single-database approach for targeted NMA)
2. Complete CINeMA/GRADE table
3. Add explicit recommendation table by patient subgroup
4. Discuss PHOENIX non-GCB population restriction more prominently
5. Address follow-up heterogeneity in limitations
6. Register on PROSPERO before submission
