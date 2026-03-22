# Data Dictionary — Scoping Review Charting Table

## Variables

| Variable | Type | Description |
|----------|------|-------------|
| study_id | string | BibTeX record ID |
| authors | string | Author list (first author et al. for >3 authors) |
| year | integer | Publication year |
| title | string | Full article title |
| doi | string | Digital Object Identifier |
| pmid | string | PubMed ID (if available) |
| journal | string | Journal name |
| layer | string | Primary literature layer (L1-L5, may be multiple separated by ;) |
| study_design | string | RCT, within-subjects, between-subjects, observational, review, theoretical, neuroimaging |
| population | string | healthy adults, TTH patients, mixed, N/A (for theoretical) |
| sample_size | integer | N participants (blank for theoretical papers) |
| cognitive_task | string | Task used (N-back, Stroop, simulated workday, etc.) |
| task_duration | string | Duration of cognitive task |
| outcome_measures | string | What was measured (VAS, effort discounting, fMRI, MRS, etc.) |
| discomfort_type | string | general fatigue, head-localized, somatic, motivational, N/A |
| key_finding | string | 1-2 sentence summary of main result |
| theoretical_framework | string | opportunity cost, EVC, predictive processing, metabolic, peripheral, multiple |
| limitations | string | Key methodological limitations |

## Layer Definitions

- **L1**: Why effort is aversive (opportunity cost, effort paradox, EVC theory)
- **L2**: Neural metabolic cost (glutamate, glycogen, lPFC fatigue)
- **L3**: Effort as aversive signal (dACC, effort meter, aversive motivation)
- **L4**: Predictive processing / allostatic (interoception, prediction error, active inference)
- **L5**: Pain/headache bridging (TTH, stress-hyperalgesia, pericranial)
