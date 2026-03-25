# Outcome Definitions

## Primary Outcome

### Progression-Free Survival (PFS)
- **Definition**: Time from randomization to disease progression, relapse, or death from any cause
- **Measure**: Hazard ratio (HR) with 95% confidence interval
- **Assessment**: Per Lugano 2014 criteria (PET-CT based) preferred; Cheson 2007 acceptable
- **Note**: Some trials use investigator-assessed PFS, others use IRC-assessed. Record which; sensitivity analysis by assessment method if >2 trials per type.

## Secondary Outcomes

### Overall Survival (OS)
- **Definition**: Time from randomization to death from any cause
- **Measure**: HR with 95% CI
- **Note**: May be immature in some trials; document median follow-up

### Complete Response Rate (CR)
- **Definition**: Proportion achieving complete metabolic response (Deauville 1-3) at end-of-treatment PET-CT
- **Measure**: Risk ratio (RR) with 95% CI
- **Note**: CR definition varies (Lugano vs Cheson); record criteria used

### Grade ≥3 Adverse Events
- **Definition**: Proportion experiencing any CTCAE Grade 3 or higher adverse event
- **Measure**: RR with 95% CI
- **Specific AEs of interest**: Febrile neutropenia, peripheral neuropathy, infections, CRS (if applicable)

### Treatment-Related Mortality (TRM)
- **Definition**: Death attributed to treatment toxicity (not disease progression)
- **Measure**: RR with 95% CI (if event counts permit) or descriptive summary

## Effect Measures

| Outcome | Data Type | Effect Measure | Pooling Method |
|---------|-----------|----------------|----------------|
| PFS | Time-to-event | HR | Bayesian NMA (gemtc) |
| OS | Time-to-event | HR | Bayesian NMA (gemtc) |
| CR rate | Binary | RR | Bayesian NMA (gemtc) |
| Grade ≥3 AE | Binary | RR | Bayesian NMA (gemtc) |
| TRM | Binary | RR | Pairwise (sparse events) |

## Subgroup Outcome Analyses

Subgroup NMAs will be performed for PFS and OS (if ≥3 trials report subgroup HRs) stratified by:
1. Cell-of-origin: ABC/non-GCB vs GCB
2. IPI risk: 0-2 vs 3-5
3. Double-expressor: DEL+ vs DEL−
4. Age: ≤60 vs >60

## Time Points

- **Primary analysis**: Most mature follow-up available per trial
- **Landmark analysis**: 2-year PFS/OS rates (if reported across ≥5 trials)
