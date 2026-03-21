# Dual-Review Schema

## Title/Abstract Screening (`03_screening/round-01/decisions.csv`)

Recommended columns:
- `record_id`
- `title`
- `decision_r1`
- `decision_r2`
- `final_decision`
- `exclusion_reason`

Valid decision labels should match `references/screening-labels.md`.

## Full-Text Eligibility Screening (`04_fulltext/fulltext_decisions.csv`)

Recommended columns:
- `record_id`
- `title`
- `doi`
- `pmid`
- `FT_Reviewer1_Decision` — include / exclude (no "maybe" at this stage)
- `FT_Reviewer1_Reason`
- `FT_Reviewer2_Decision` — include / exclude
- `FT_Reviewer2_Reason`
- `FT_Final_Decision` — include / exclude (resolved)
- `FT_Exclusion_Code` — code from screening-labels.md or NONE

Valid decision labels: `include`, `exclude` only. Valid exclusion codes match `references/screening-labels.md`.

Only studies with `FT_Final_Decision = include` proceed to Stage 05 (data extraction).
Excluded studies with reasons feed into PRISMA 2020 flow diagram item 16.
