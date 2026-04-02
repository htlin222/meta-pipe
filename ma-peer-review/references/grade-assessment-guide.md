# GRADE Assessment Guide

**Time**: 30-45 minutes per outcome
**Standard**: GRADE Working Group (Guyatt et al., 2011-2013)
**Output**: GRADE Summary of Findings (SoF) table

---

## Overview

GRADE (Grading of Recommendations Assessment, Development and Evaluation) provides a systematic approach to rating the **certainty of evidence** for each outcome in your meta-analysis.

**Certainty levels**:
- ⊕⊕⊕⊕ **HIGH**: Very confident the true effect is close to the estimate
- ⊕⊕⊕⊖ **MODERATE**: Moderately confident; true effect likely close but could be substantially different
- ⊕⊕⊖⊖ **LOW**: Limited confidence; true effect may be substantially different
- ⊕⊖⊖⊖ **VERY LOW**: Very little confidence; true effect likely substantially different

---

## Starting Point

**For RCTs**: Start at HIGH (⊕⊕⊕⊕)
**For observational studies**: Start at LOW (⊕⊕⊖⊖)

Then apply **downgrade** and **upgrade** factors.

---

## 5 Downgrade Factors (Each -1 or -2 levels)

### 1. **Risk of Bias** (Study Limitations)

**Downgrade -1** if:
- >25% weight from studies at high risk of bias
- Unclear allocation concealment in most studies
- Lack of blinding affecting subjective outcomes
- High attrition (>20%) with differential dropout

**Downgrade -2** if:
- >50% weight from high-risk studies
- Severe methodological flaws (e.g., no randomization despite claiming RCT)

**Pipeline check**:
```bash
# Check RoB distribution
cat 05_extraction/round-01/quality_rob2.csv | awk -F',' '{print $NF}' | sort | uniq -c
```

**Example**:
- 3/6 studies high risk → **-1** (MODERATE)
- 5/6 studies high risk → **-2** (LOW)

---

### 2. **Inconsistency** (Heterogeneity)

**Downgrade -1** if:
- I² > 50% AND p < 0.10 for heterogeneity
- Effect estimates vary widely (some benefit, some harm)
- 95% prediction interval crosses null AND includes clinically important harm

**Downgrade -2** if:
- I² > 75% with unexplained heterogeneity
- Contradictory results across studies

**Pipeline check**:
```r
# From 06_analysis/nma_04_models.R or 03_models.R
summary(res)$I2  # Check I² value
```

**Example**:
- I² = 65%, p = 0.03 → **-1** (MODERATE)
- I² = 82%, no subgroup explanation → **-2** (LOW)

**NMA-specific**: Also consider **incoherence** (inconsistency between direct and indirect evidence). If node-splitting p < 0.05 → downgrade -1.

---

### 3. **Indirectness** (Population, Intervention, Comparator, Outcome)

**Downgrade -1** if:
- Population differs from target (e.g., mostly Asian patients but applying to Western populations)
- Intervention differs (e.g., different doses/regimens than clinical practice)
- Surrogate outcomes used (e.g., tumor response instead of survival)
- Indirect comparisons in NMA with limited transitivity

**Downgrade -2** if:
- Severe mismatch (e.g., animal studies for human question)

**Example**:
- Meta-analysis on PD-L1 ≥50% but applying to all-comers → **-1** (MODERATE)
- Using PFS instead of OS → **-1** (MODERATE)

---

### 4. **Imprecision** (Wide Confidence Intervals)

**Downgrade -1** if:
- 95% CI crosses clinically important thresholds (e.g., HR 0.75-1.25)
- Total events <300 (for dichotomous outcomes)
- Total sample size <400 (for continuous outcomes)
- Optimal information size (OIS) not met

**Downgrade -2** if:
- Very wide CI crossing both benefit and harm
- <100 total events

**Pipeline check**:
```r
# From forest plot
res$ci.lb  # Lower bound
res$ci.ub  # Upper bound
sum(dat$events_intervention) + sum(dat$events_control)  # Total events
```

**Example**:
- HR 0.75 (95% CI 0.55-1.02), 250 events → **-1** (MODERATE)
- HR 0.80 (95% CI 0.50-1.30), 80 events → **-2** (LOW)

**Rule of thumb**:
- CI crosses null (1.0 for RR/HR, 0 for MD) AND includes clinically important effect → downgrade

---

### 5. **Publication Bias**

**Downgrade -1** if:
- Funnel plot asymmetry with Egger's test p < 0.10
- <10 studies but strong suspicion (e.g., all industry-funded, no negative trials)
- Evidence of selective outcome reporting

**Pipeline check**:
```r
# From 06_analysis/08_bias.R or nma_08_funnel.R
regtest(res)  # Egger's test
```

**Example**:
- Egger p = 0.03, 12 studies → **-1** (MODERATE)
- Only 6 studies, no clear asymmetry → **No downgrade**

---

## 3 Upgrade Factors (Observational Studies Only)

### 1. **Large Effect**

**Upgrade +1** if:
- RR > 2 or < 0.5 with no plausible confounders

**Upgrade +2** if:
- RR > 5 or < 0.2 with no serious concerns

**Example**:
- Smoking and lung cancer: RR = 10 → **+2**

---

### 2. **Dose-Response Gradient**

**Upgrade +1** if:
- Clear dose-response relationship strengthens causal inference

**Example**:
- Higher PD-L1 expression → better ICI response → **+1**

---

### 3. **All Plausible Confounders Would Reduce Effect**

**Upgrade +1** if:
- Observed effect despite confounders working against it

**Example**:
- ICI benefit despite patients with worse performance status → **+1**

---

## GRADE for Network Meta-Analysis (NMA)

**Framework**: CINeMA (Confidence in Network Meta-Analysis) — adapted from GRADE for NMA

**Reference**: Nikolakopoulou et al. (2020). BMJ 2020;371:m3983. https://doi.org/10.1136/bmj.m3983

### **CINeMA 6 Domains** (instead of GRADE 5)

| Domain | GRADE Equivalent | NMA-Specific Consideration |
|--------|------------------|----------------------------|
| 1. Within-study bias | Risk of bias | Same as GRADE |
| 2. Reporting bias | Publication bias | Same as GRADE |
| 3. Indirectness | Indirectness | **+ Intransitivity** (effect modifiers across comparisons) |
| 4. Imprecision | Imprecision | **+ Contribution matrix** (how studies contribute to indirect estimates) |
| 5. Heterogeneity | Inconsistency | Same as GRADE (but per comparison, not overall) |
| 6. **Incoherence** | *(New for NMA)* | **Direct vs indirect evidence agreement** |

### **Key Differences from Standard GRADE**:

1. **Assessment is per comparison** (not per outcome)
   - Example: Pembrolizumab vs Nivolumab, Pembrolizumab vs Chemotherapy (separate ratings)

2. **Incoherence is a 6th domain** (unique to NMA)
   - **Local approach**: Node-splitting (SIDE) for specific comparisons
   - **Global approach**: Design-by-treatment interaction test
   - **Judgment**: p > 0.10 = no concerns, p < 0.05 = major concerns

3. **Intransitivity assessment is mandatory**
   - Check if effect modifiers (age, disease severity, treatment dose) differ across comparisons
   - If uneven distribution → downgrade for indirectness

4. **Contribution matrix informs judgments**
   - Shows % contribution of each study to each network estimate
   - If indirect estimate relies on high-risk studies → downgrade

### **Staged Assessment Workflow (Brignardello-Petersen 2018)**

The GRADE Working Group recommends a **sequential 4-stage process** for rating NMA certainty:
1. Assess direct evidence (without imprecision)
2. Check efficiency shortcut (high certainty + dominant contribution → skip indirect)
3. Assess indirect evidence (starting from lowest certainty in first-order loop)
4. Derive network estimate (higher of direct/indirect → coherence → imprecision)

**Full guide**: `ma-network-meta-analysis/references/nma-grade-certainty-workflow.md`

**Reference**: Brignardello-Petersen R, et al. *J Clin Epidemiol*. 2018;93:36-44. PMID: 29051107.

### **CINeMA Judgment Levels** (3 levels, not GRADE's 4)

- **No concerns**: No downgrade
- **Some concerns**: Downgrade **-1 level**
- **Major concerns**: Downgrade **-2 levels**

**Final rating**: Very Low / Low / Moderate / High (same as GRADE)

### **CINeMA Tool** (Web Application)

**URL**: https://cinema.ispm.unibe.ch/

**Features**:
- Upload study data (standard meta-analysis format)
- Automatic network plots
- Contribution matrices (per comparison)
- Heterogeneity estimates (per comparison)
- Incoherence tests (node-splitting + global)
- Guided GRADE assessment (6 domains)
- Export Summary of Findings table

**Required for**:
- High-impact journals (Lancet, JAMA, BMJ)
- Cochrane NMA reviews
- HTA submissions (NICE, CADTH)

### **Incoherence Assessment** (Domain 6)

**Methods**:

1. **Node-splitting** (local inconsistency)
   - Tests direct vs indirect evidence for each comparison
   - **p > 0.10**: No concerns
   - **0.05 < p < 0.10**: Some concerns → **-1**
   - **p < 0.05**: Major concerns → **-2**

2. **Design-by-treatment interaction** (global inconsistency)
   - Tests overall network coherence
   - Same p-value thresholds

**WARNING**: Do NOT rely solely on global incoherence tests (Lu-Ades model, design-by-treatment interaction) — these are **frequently underpowered**. A non-significant global p-value does NOT mean no incoherence exists. Always perform **local node-splitting** for each comparison as the primary assessment. See `ma-network-meta-analysis/references/nma-grade-certainty-workflow.md` (Stage 4b).

**Pipeline check**:
```bash
# Check node-splitting results
grep -i "p-value" 06_analysis/nma_05_inconsistency_output.txt

# Or from R:
# netsplit() in netmeta package
# or mtc.nodesplit() in gemtc package
```

**Example**:
- Pembrolizumab vs Chemotherapy: Direct RR 0.72, Indirect RR 0.85, p = 0.18 → **No concerns**
- Nivolumab vs Atezolizumab: No direct evidence, indirect RR 1.05, p = 0.02 → **Major concerns (-2)**

### **Intransitivity Assessment** (Domain 3)

**Definition**: Violation of the similarity assumption (all studies can be jointly analyzed)

**Check**:
1. **Effect modifiers** across comparisons:
   - Age (elderly vs young)
   - Disease severity (early vs advanced stage)
   - Treatment dose/duration
   - Follow-up time

2. **Baseline characteristics** in study characteristics table

**Judgment**:
- **Similar across comparisons** → No concerns
- **Some differences** (e.g., median age 55 vs 65) → Some concerns → **-1**
- **Major differences** (e.g., early-stage vs metastatic) → Major concerns → **-2**

**Pipeline check**:
```bash
# Compare study characteristics across comparisons
cat 05_extraction/round-01/extraction.csv | awk -F',' '{print $3,$5,$8}' # intervention, age, stage
```

### **Imprecision in NMA** (Domain 4)

**Additional consideration**: **Contribution of indirect evidence**

**Judgment**:
- **Direct evidence dominates** (>70% contribution) → Apply standard GRADE imprecision
- **Indirect evidence dominates** (>70% contribution) → Usually downgrade **-1**
- **Mixed** (30-70% each) → Consider CI width + contribution matrix

**Pipeline check**:
```r
# From CINeMA web app or netmeta package
netcontrib(nma_model)  # Shows contribution matrix
```

### **Pipeline Integration**

```bash
cd /Users/htlin/meta-pipe/tooling/python

# Step 1: Run NMA analysis (generates inconsistency tests)
Rscript 06_analysis/nma_05_inconsistency.R

# Step 2: Export data for CINeMA
# (Manual: Upload extraction.csv to https://cinema.ispm.unibe.ch/)

# Step 3: Download CINeMA results
# Save as: 08_reviews/cinema_assessment.csv

# Step 4: Validate CINeMA completion
uv run ../../ma-network-meta-analysis/scripts/validate_nma_outputs.py \
  --root ../../projects/<project-name> \
  --out ../../projects/<project-name>/09_qa/nma_validation.md
```

---

## GRADE Summary of Findings (SoF) Table Format

| Outcome | No. of Studies (Participants) | Effect Estimate (95% CI) | Certainty | Explanation |
|---------|-------------------------------|--------------------------|-----------|-------------|
| Overall Survival (OS) | 6 RCTs (3,819) | HR 0.72 (0.61-0.85) | ⊕⊕⊕⊖ MODERATE | -1 for imprecision (OS data immature, median not reached in 4/6 trials) |
| Event-Free Survival (EFS) | 5 RCTs (3,256) | HR 0.58 (0.49-0.68) | ⊕⊕⊕⊕ HIGH | No serious concerns |
| Grade 3-4 Adverse Events | 6 RCTs (3,819) | RR 1.38 (1.15-1.65) | ⊕⊕⊕⊖ MODERATE | -1 for inconsistency (I² = 58%, p = 0.04) |

---

## Common Mistakes

❌ **Don't downgrade twice for the same issue**
- Example: Don't downgrade for "inconsistency" AND "imprecision" if wide CI is due to heterogeneity

❌ **Don't upgrade RCTs**
- Upgrade factors only apply to observational studies starting at LOW

❌ **Don't ignore NMA-specific issues**
- Incoherence and intransitivity are mandatory checks for NMA

❌ **Don't confuse statistical significance with certainty**
- p < 0.05 ≠ HIGH certainty
- Example: HR 0.80 (0.65-0.98) with I² = 70% → MODERATE at best

---

## Pipeline Integration

### **Step 1: Initialize GRADE Template**
```bash
cd /Users/htlin/meta-pipe/tooling/python
uv run ../../ma-peer-review/scripts/init_grade_summary.py \
  --extraction ../../projects/<project>/05_extraction/extraction.csv \
  --out-csv ../../projects/<project>/08_reviews/grade_summary.csv
```

### **Step 2: Collect Analysis Statistics**
```bash
uv run ../../ma-peer-review/scripts/collect_analysis_stats.py \
  --analysis-dir ../../projects/<project>/06_analysis \
  --rob-csv ../../projects/<project>/08_reviews/quality_rob2.csv \
  --out ../../projects/<project>/08_reviews/analysis_stats.json
```

This parses Stage 06 markdown reports and CSV tables to extract I², Egger's
test p-values, pooled effects, CI bounds, total events, and RoB 2 judgments
into a structured JSON file.

### **Step 3: Auto-Populate Suggestions (Semi-Automated)**
```bash
uv run ../../ma-peer-review/scripts/auto_grade_suggestion.py \
  --grade ../../projects/<project>/08_reviews/grade_summary.csv \
  --stats ../../projects/<project>/08_reviews/analysis_stats.json \
  --out-csv ../../projects/<project>/08_reviews/grade_suggestions.csv \
  --out-md ../../projects/<project>/08_reviews/grade_suggestions.md \
  --out-detailed-md ../../projects/<project>/08_reviews/grade_detailed.md \
  --default-start high
```

This script will compute per-domain suggestions with rationale:

| Domain | Computable input | Suggested logic | Reference |
|--------|-----------------|-----------------|-----------|
| **Inconsistency** | I², prediction interval | I²>50% + PI crossing null → "serious" | Cochrane Handbook §14.4.4 |
| **Imprecision** | Total events, CI width | <300 events → "serious"; CI crosses null → "serious" | Guyatt et al. 2011 (PMID: 21208779) |
| **Publication bias** | Egger's test | Egger p<0.10 → "serious" (caveat if <10 studies) | Sterne et al. 2011 (PMID: 21952616) |
| **Risk of bias** | RoB 2 per-study assessments | >25% high risk → "serious" | Sterne et al. 2019 (PMID: 31462531) |
| **Indirectness** | PICO vs study characteristics | Flag for human review | Guyatt et al. 2011 (PMID: 21208780) |

Output format per outcome × domain (in `grade_detailed.md`):
```
### Inconsistency
- Computed: I² = 62%, prediction interval [0.85, 1.92] (crosses null)
- Suggested downgrade: Serious (-1)
- Rationale: I² >50% with prediction interval including no effect (Cochrane Handbook §14.4.4)
- Reviewer decision: [ ] Accept  [ ] Override to: ___
```

> **Note**: Without `--stats`, the script falls back to legacy text-parsing mode.

### **Step 4: Manual Review**
- Open `grade_detailed.md` for per-domain computed suggestions
- Accept or override each domain suggestion
- Flag indirectness concerns (not computable automatically)
- Document rationale for any overrides

### **Step 4: Render SoF Table**
```bash
uv run ../../ma-peer-review/scripts/render_sof_table.py \
  --grade ../../projects/<project>/08_reviews/grade_summary.csv \
  --out ../../projects/<project>/07_manuscript/tables/sof_table.png \
  --dpi 300
```

---

## Decision Tree

```
Start: RCTs = HIGH (⊕⊕⊕⊕), Observational = LOW (⊕⊕⊖⊖)
  ↓
Risk of Bias?
  >25% high risk → -1
  >50% high risk → -2
  ↓
Inconsistency?
  I² >50% + p<0.10 → -1
  I² >75% unexplained → -2
  ↓
Indirectness?
  Population/intervention/outcome mismatch → -1
  Severe mismatch → -2
  ↓
Imprecision?
  CI crosses clinical threshold + <300 events → -1
  CI very wide + <100 events → -2
  ↓
Publication Bias?
  Funnel asymmetry + Egger p<0.10 → -1
  ↓
Final Certainty:
  ⊕⊕⊕⊕ HIGH
  ⊕⊕⊕⊖ MODERATE
  ⊕⊕⊖⊖ LOW
  ⊕⊖⊖⊖ VERY LOW
```

---

## Example: Perioperative ICI for Resectable NSCLC (EFS Outcome)

**Starting point**: RCTs → HIGH (⊕⊕⊕⊕)

**Downgrades**:
1. **Risk of Bias**: 1/5 studies high risk (AEGEAN open-label) → **No downgrade** (<25% weight)
2. **Inconsistency**: I² = 0%, p = 0.92 → **No downgrade**
3. **Indirectness**: All studies in resectable NSCLC, EFS defined consistently → **No downgrade**
4. **Imprecision**: HR 0.58 (0.49-0.68), 856 events, CI excludes null → **No downgrade**
5. **Publication Bias**: 5 studies, no asymmetry → **No downgrade**

**Final**: ⊕⊕⊕⊕ HIGH certainty

**Interpretation**: "We are very confident that perioperative ICI improves EFS in resectable NSCLC."

---

## References

1. Guyatt GH, Oxman AD, Vist GE, et al. GRADE: an emerging consensus on rating quality of evidence and strength of recommendations. *BMJ*. 2008;336:924-926.
2. Guyatt GH, Oxman AD, Kunz R, et al. GRADE guidelines: 7. Rating the quality of evidence—inconsistency. *J Clin Epidemiol*. 2011;64(12):1294-1302.
3. Puhan MA, Schünemann HJ, Murad MH, et al. A GRADE Working Group approach for rating the quality of treatment effect estimates from network meta-analysis. *BMJ*. 2014;349:g5630.
4. Salanti G, Del Giovane C, Chaimani A, Caldwell DM, Higgins JPT. Evaluating the quality of evidence from a network meta-analysis. *PLoS One*. 2014;9(7):e99682.
