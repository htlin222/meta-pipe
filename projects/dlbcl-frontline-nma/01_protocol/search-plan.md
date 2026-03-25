# Search Plan

## Databases

| Database | Priority | Rationale |
|----------|----------|-----------|
| PubMed/MEDLINE | Mandatory | Primary biomedical database |
| Scopus | Mandatory | Broader coverage, captures conference proceedings |
| Embase | Recommended | European trials, drug-focused |
| Cochrane CENTRAL | Recommended | Curated RCT registry |
| ClinicalTrials.gov | Supplementary | Verify trial status, find unpublished data |

## Search Strategy

### PubMed Search String

```
("diffuse large B-cell lymphoma"[MeSH] OR "DLBCL"[tiab] OR "diffuse large B cell"[tiab])
AND
("first-line"[tiab] OR "frontline"[tiab] OR "untreated"[tiab] OR "newly diagnosed"[tiab] OR "treatment-naive"[tiab])
AND
("randomized controlled trial"[pt] OR "randomized"[tiab] OR "phase III"[tiab] OR "phase 3"[tiab])
AND
("R-CHOP"[tiab] OR "rituximab"[tiab] OR "chemoimmunotherapy"[tiab])
AND
2010:2026[dp]
```

### Key Trial Names (Supplementary Search)

Search each trial name individually to ensure capture:
- POLARIX
- PHOENIX
- ROBUST
- ECOG-E1412 OR R2-CHOP
- REMoDL-B
- GOYA
- CALGB 50303 OR Alliance 50303

### Filters
- **Date**: 2010-01-01 to 2026-03-25
- **Language**: English
- **Species**: Humans
- **Study type**: RCT / Clinical Trial Phase III

## Search Rounds

- **Round 01**: Initial systematic search (all databases)
- **Round 02**: Trial-name targeted search (supplementary)
- **Round 03**: Reference list screening of included studies and relevant reviews
- **Round 04**: Citation tracking (forward search) of key included trials

## Gray Literature

- Conference abstracts: ASH, ASCO, EHA, ICML (2020-2026)
- Check ClinicalTrials.gov for unpublished results
- Contact corresponding authors if data missing from publications

## Expected Yield

- Estimated unique records after deduplication: 200-500
- Estimated includable Phase III RCTs: 7-10
- Known trials pre-identified: 7 (see TOPIC.txt)
