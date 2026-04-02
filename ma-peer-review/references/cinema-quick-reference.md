# CINeMA Quick Reference Card

**CINeMA**: Confidence in Network Meta-Analysis
**Reference**: Nikolakopoulou et al. BMJ 2020;371:m3983
**Tool**: https://cinema.ispm.unibe.ch/

---

## 🎯 **When to Use**

- ✅ Network meta-analysis with ≥3 treatments
- ✅ Submitting to high-impact journals (Lancet, JAMA, BMJ)
- ✅ Cochrane NMA reviews
- ✅ HTA submissions (NICE, CADTH)

**NOT for pairwise MA** (use standard GRADE instead)

---

## 📊 **CINeMA vs Standard GRADE**

| Feature | Standard GRADE | CINeMA (NMA) |
|---------|---------------|--------------|
| **Domains** | 5 | **6** (adds Incoherence) |
| **Assessment unit** | Per outcome | **Per comparison** |
| **Indirectness** | PICO mismatch | PICO + **Intransitivity** |
| **Imprecision** | CI width | CI width + **Contribution matrix** |
| **Judgment levels** | 4 (High/Mod/Low/VLow) | **3** (No/Some/Major concerns) |
| **New domain** | N/A | **Incoherence** (direct vs indirect) |

---

## 🔍 **6 Domains (Per Comparison)**

### **1. Within-Study Bias** (= Risk of Bias)

**Same as GRADE**:
- Review RoB 2 or ROBINS-I assessments
- Check % contribution from high-risk studies (via contribution matrix)

**Judgment**:
- <25% high-risk weight → **No concerns**
- 25-50% high-risk weight → **Some concerns (-1)**
- >50% high-risk weight → **Major concerns (-2)**

---

### **2. Reporting Bias** (= Publication Bias)

**Same as GRADE**:
- Funnel plot asymmetry (if ≥10 studies)
- Comparison-adjusted funnel plot (NMA-specific)

**Judgment**:
- No asymmetry → **No concerns**
- Some asymmetry → **Some concerns (-1)**
- Clear asymmetry → **Major concerns (-2)**

---

### **3. Indirectness** (+ Intransitivity)

**Standard GRADE**: PICO mismatch

**NMA-specific**: **Intransitivity** (effect modifiers differ across comparisons)

**Check**:
- Age distribution across comparisons
- Disease severity (early-stage vs metastatic)
- Treatment dose/duration
- Follow-up time

**Example**:
- Comparison A: Median age 55, early-stage
- Comparison B: Median age 70, metastatic
- → **Intransitivity concern** (effect modifiers differ)

**Judgment**:
- Similar characteristics → **No concerns**
- Some differences (e.g., age 55 vs 65) → **Some concerns (-1)**
- Major differences (e.g., early vs metastatic) → **Major concerns (-2)**

---

### **4. Imprecision** (+ Contribution Matrix)

**Standard GRADE**: CI width crosses clinical decision threshold

**NMA-specific**: **Contribution of indirect evidence**

**CINeMA approach**:
1. Check CI width (standard GRADE)
2. Check **% contribution from direct evidence**:
   - >70% direct → Apply standard imprecision rules
   - <30% direct (mostly indirect) → Usually downgrade **-1**
   - 30-70% mixed → Consider both CI + contribution

**Judgment**:
- Narrow CI + direct evidence → **No concerns**
- Wide CI OR mostly indirect → **Some concerns (-1)**
- Very wide CI AND mostly indirect → **Major concerns (-2)**

---

### **5. Heterogeneity** (= Inconsistency in GRADE)

**Same as GRADE, but per comparison**:

**Judgment**:
- I² < 50% → **No concerns**
- I² 50-75% → **Some concerns (-1)**
- I² > 75% → **Major concerns (-2)**

**Note**: In NMA, heterogeneity is assessed separately for each comparison (not network-wide)

---

### **6. Incoherence** (NEW for NMA)

**Definition**: Disagreement between direct and indirect evidence

**Methods**:

1. **Local approach**: **Node-splitting** (per comparison)
   - Tests direct vs indirect for specific comparison
   - Example: Pembrolizumab vs Chemotherapy
     - Direct RR: 0.72
     - Indirect RR: 0.85
     - p = 0.18 → **No incoherence**

2. **Global approach**: **Design-by-treatment interaction**
   - Tests overall network coherence
   - p > 0.10 → **No concerns**

**Judgment**:
- p > 0.10 → **No concerns**
- 0.05 < p < 0.10 → **Some concerns (-1)**
- p < 0.05 → **Major concerns (-2)**

**Pipeline**:
```r
# In nma_05_inconsistency.R
library(netmeta)
netsplit(nma_model)  # Node-splitting

library(gemtc)
mtc.nodesplit(nma_model)  # Bayesian node-splitting
```

---

## 🎯 **Final Rating (Per Comparison)**

**Start**: HIGH (⊕⊕⊕⊕) for RCTs

**Downgrade**:
- **Some concerns** in any domain → **-1 level**
- **Major concerns** in any domain → **-2 levels**

**Final**:
- ⊕⊕⊕⊕ **HIGH**: No concerns across all 6 domains
- ⊕⊕⊕⊖ **MODERATE**: Some concerns in 1 domain OR major in 1 domain
- ⊕⊕⊖⊖ **LOW**: Some concerns in 2+ domains OR major in 1-2 domains
- ⊕⊖⊖⊖ **VERY LOW**: Major concerns in 3+ domains

---

## 🔧 **CINeMA Web Tool Workflow**

### **Step 1: Prepare Data**

Upload to https://cinema.ispm.unibe.ch/:
- Study-level data (treatment arms, outcomes, sample sizes)
- Risk of bias assessments (per study)
- Indirectness judgments (per study)

**Format**: CSV or Excel (template provided on website)

---

### **Step 2: Generate Network Plot**

Tool automatically creates:
- Network graph (treatments as nodes, studies as edges)
- Contribution matrix (% contribution per study to each estimate)
- Heterogeneity estimates (per comparison)

---

### **Step 3: Assess 6 Domains**

For **each pairwise comparison** (e.g., Pembrolizumab vs Nivolumab):

1. **Within-study bias**: Check contribution matrix → weight from high-risk studies
2. **Reporting bias**: Review funnel plot
3. **Indirectness**: Check intransitivity (study characteristics)
4. **Imprecision**: Check CI width + % direct contribution
5. **Heterogeneity**: Check I² per comparison
6. **Incoherence**: Review node-splitting p-values

Tool guides you through each domain with pre-specified rules.

---

### **Step 4: Export Results**

Download:
- **Summary of Findings table** (per comparison)
- **Confidence ratings** (High/Moderate/Low/Very Low)
- **Contribution matrices**
- **Incoherence tests**

Save as: `08_reviews/cinema_assessment.csv`

---

## 📋 **Common Mistakes**

❌ **Using standard GRADE for NMA** (missing incoherence assessment)

❌ **Rating per outcome instead of per comparison**
- ❌ Wrong: "Overall Survival → MODERATE"
- ✅ Right: "Pembrolizumab vs Nivolumab for OS → MODERATE"

❌ **Ignoring intransitivity** (just checking PICO)

❌ **Not using contribution matrix** (treating all comparisons equally)

❌ **Downgrading twice for related issues**
- Example: Imprecision AND heterogeneity (if wide CI due to I²) → **only downgrade once**

❌ **Forgetting to assess incoherence** (6th domain unique to NMA)

❌ **Relying on global incoherence test alone** (Lu-Ades, design-by-treatment — frequently underpowered; always do local node-splitting per comparison)

❌ **Assessing imprecision before combining direct + indirect evidence** (imprecision applies to network estimate, not to direct/indirect components separately — see staged workflow)

---

## 🕒 **Time Budget**

| Task | Time |
|------|------|
| Prepare data for CINeMA | 30 min |
| Upload + generate network plots | 10 min |
| Assess 6 domains per comparison | 15 min × N comparisons |
| Export + integrate into manuscript | 20 min |
| **Total for N=5 comparisons** | **~2 hours** |

**Example**: 5 treatments = 10 comparisons = **2.5 hours**

---

## 📖 **Staged Workflow (Brignardello-Petersen 2018)**

For the sequential 4-stage process of combining direct → indirect → network certainty:

See `ma-network-meta-analysis/references/nma-grade-certainty-workflow.md`

Key additions beyond CINeMA:
- Imprecision deferred to network estimate stage only
- Efficiency shortcut for high-certainty direct evidence
- Indirect evidence starts from lowest certainty in first-order loop
- Network estimate = higher of direct/indirect as starting point
- Explicit warning about underpowered global incoherence tests

**Reference**: Brignardello-Petersen R, et al. *J Clin Epidemiol*. 2018;93:36-44. PMID: 29051107.

---

## 📚 **Resources**

- **CINeMA Paper**: Nikolakopoulou et al. BMJ 2020;371:m3983 (https://doi.org/10.1136/bmj.m3983)
- **CINeMA Tool**: https://cinema.ispm.unibe.ch/
- **Tutorial**: Available on CINeMA website (demo datasets included)
- **GRADE Guide**: `ma-peer-review/references/grade-assessment-guide.md`
- **NMA Checklist**: `ma-network-meta-analysis/references/nma-completion-checklist.md`

---

## ✅ **Quick Checklist**

Before submission, ensure:

- [ ] CINeMA assessment completed for **all key comparisons** (not just primary)
- [ ] **6 domains** assessed per comparison (not 5)
- [ ] **Incoherence** assessed via node-splitting (not just heterogeneity)
- [ ] **Intransitivity** checked (effect modifiers across comparisons)
- [ ] **Contribution matrix** reviewed (% direct vs indirect)
- [ ] Results exported to `08_reviews/cinema_assessment.csv`
- [ ] Table S10 (CINeMA results) included in supplementary materials
- [ ] Methods section describes CINeMA approach

---

**Last updated**: 2026-02-17 (Phase 2 enhancements)
