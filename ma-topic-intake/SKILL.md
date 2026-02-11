---
name: ma-topic-intake
description: Intake a meta-analysis topic from TOPIC.txt, translate it into a PICO or PECO protocol, and define eligibility, outcomes, and search scope. Use when starting a new meta-analysis project or refining a research question.
---

# Ma Topic Intake

## Overview

Turn the raw topic into a formal protocol and a search-ready research question.

## Inputs

- `TOPIC.txt`
- Any user constraints or preferences

## Outputs

- `01_protocol/pico.yaml`
- `01_protocol/eligibility.md`
- `01_protocol/outcomes.md`
- `01_protocol/search-plan.md`
- `01_protocol/decision-log.md`

## Workflow

1. Read `TOPIC.txt` and restate the question in PICO or PECO form.
2. Define primary and secondary outcomes, time horizon, and effect measures.
3. Specify inclusion and exclusion criteria, including study types and populations.
4. Define the search scope: databases, years, languages, and gray literature policy.
5. Write a concise protocol summary and log assumptions or unresolved items.
6. Ask targeted clarifying questions only if missing data blocks downstream steps.

## Resources

- `references/pico-template.yaml` provides a structured PICO scaffold.

## Validation

- Ensure each protocol file is consistent and non-contradictory.
- Record all assumptions in `01_protocol/decision-log.md`.

## Pipeline Navigation

| Step | Skill                     | Stage                          |
| ---- | ------------------------- | ------------------------------ |
| Prev | `/brainstorm-topic`       | Pre-pipeline topic development |
| Next | `/ma-search-bibliography` | 02 Search & Bibliography       |
| All  | `/ma-end-to-end`          | Full pipeline orchestration    |
