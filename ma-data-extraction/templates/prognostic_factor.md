# Prognostic factor 2×2 data dictionary

This is the markdown data dictionary paired with `prognostic_factor.yaml`.
Pass it to `create_extraction_template.py` to scaffold an extraction CSV
with the correct columns:

```bash
uv run tooling/python/create_extraction_template.py \
  --pdf-jsonl projects/<name>/05_extraction/pdf_texts.jsonl \
  --data-dict ma-data-extraction/templates/prognostic_factor.md \
  --out-csv projects/<name>/05_extraction/extraction.csv
```

Use this template when extracting binary exposure → binary outcome
contingencies from observational studies (cohort, case-control, registry).
It covers unadjusted counts, the reported effect estimate with confidence
interval, and the adjustment set.

## Critical Fields (Must Not Be Missing)

1. record_id
2. study_id
3. n_total
4. n_exposed
5. n_unexposed
6. events_exposed
7. events_unexposed
8. effect_estimate
9. ci_lower
10. ci_upper
11. outcome_name

## Field definitions

### Identification

- `record_id` — upstream record identifier (matches screening/manifest CSV).
- `study_id` — first author + year, e.g. `Smith2020`.

### Sample sizes

- `n_total` — total analytic sample size for the 2×2.
- `n_exposed` — participants with the prognostic factor present.
- `n_unexposed` — participants without the prognostic factor.

### Event counts

- `events_exposed` — outcome events among exposed.
- `events_unexposed` — outcome events among unexposed.

### Effect estimate

- `effect_measure` — one of: OR, RR, HR, IRR.
- `effect_estimate` — point estimate (adjusted if available).
- `ci_lower` — lower bound of the 95% confidence interval.
- `ci_upper` — upper bound of the 95% confidence interval.
- `estimate_type` — either unadjusted or adjusted.

### Adjustment set

- `adjustment_set` — comma-separated covariates adjusted for
  (e.g., `age, sex, stage, ECOG`). Empty if the estimate is unadjusted.
- `confounders_considered` — confounders the authors discussed but
  did not adjust for (feeds ROBINS-I D1 judgment).

### Outcome definition

- `outcome_name` — short label, e.g. `overall mortality`.
- `outcome_definition` — how the outcome was ascertained (chart review,
  registry, death certificate).
- `follow_up_months` — median follow-up in months.

### Metadata

- `data_source_page` — where in the paper the 2×2 came from
  (e.g., `Table 2`).
- `extractor_notes` — free-text notes for the reviewer.
