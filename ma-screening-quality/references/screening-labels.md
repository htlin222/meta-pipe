# Screening Labels

## Decision
- include
- exclude
- maybe

## Exclusion Reasons (free text)
- wrong population
- wrong intervention or exposure
- wrong comparator
- wrong outcomes
- wrong study design
- non-human
- not primary research
- duplicate
- insufficient data

## Exclusion Codes (used by `ai_screen.py`)

| Code | Category | Meaning |
|------|----------|---------|
| P1 | Population | Wrong population |
| P2 | Population | Wrong age group |
| I1 | Intervention | Wrong intervention |
| I2 | Intervention | Intervention for wrong indication |
| C1 | Comparator | Wrong comparator |
| S1 | Study design | Review/meta-analysis/editorial/commentary |
| S2 | Study design | Case report or series below minimum sample size |
| S3 | Study design | Preclinical/in vitro/animal study |
| S4 | Study design | Study protocol without results |
| O1 | Outcomes | No relevant outcomes reported |
| O2 | Outcomes | Insufficient follow-up duration |
| T1 | Time | Outside date range |
| T2 | Time | Conference abstract too old without full publication |
| L1 | Language | Language not meeting criteria |
| D1 | Duplicate | Duplicate or superseded publication |
| NONE | — | No exclusion (include or maybe) |

## Usage by Stage

- **Stage 03 (title/abstract screening)**: All codes apply. Decision can be `include`, `exclude`, or `maybe`.
- **Stage 04b (full-text screening)**: All codes apply. Decision is `include` or `exclude` only (no `maybe` — full text should resolve uncertainty). Excluded studies and their codes feed into PRISMA 2020 flow diagram item 16.
