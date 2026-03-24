# Search Plan

**Project**: gcsf-neutropenia
**Date**: 2026-03-24

---

## Databases

| Database | Priority | Rationale |
|----------|----------|-----------|
| **PubMed/MEDLINE** | Mandatory | Primary biomedical database; best coverage of clinical trials |
| **Scopus** | Mandatory | Broad interdisciplinary coverage; complements PubMed for non-indexed journals |
| **Embase** | Recommended | Strong coverage of European trials and conference abstracts; captures drug-focused literature |
| **Cochrane CENTRAL** | Recommended | Curated RCT registry; may identify trials missed by other databases |

---

## Search Strategy

### Core Concepts

The search strategy uses a 3-concept Boolean structure:

1. **Population**: Cancer patients receiving chemotherapy
2. **Intervention**: G-CSF (filgrastim, pegfilgrastim, lipegfilgrastim)
3. **Outcome**: Neutropenia / febrile neutropenia
4. **Filter**: Randomized controlled trials

### PubMed Search String (Draft)

```
("Granulocyte Colony-Stimulating Factor"[MeSH] OR "G-CSF" OR "filgrastim" OR
"Neupogen" OR "pegfilgrastim" OR "Neulasta" OR "lipegfilgrastim" OR "Lonquex" OR
"granulocyte colony stimulating factor" OR "G CSF" OR "Zarxio" OR "Nivestym" OR
"Udenyca" OR "Fulphila" OR "Nyvepria")
AND
("Neutropenia"[MeSH] OR "neutropenia" OR "febrile neutropenia" OR "FN" OR
"granulocytopenia" OR "neutropenic fever" OR "chemotherapy-induced neutropenia")
AND
("Neoplasms"[MeSH] OR "cancer" OR "tumor" OR "tumour" OR "malignancy" OR
"chemotherapy" OR "antineoplastic" OR "myelosuppressive")
AND
("randomized controlled trial"[pt] OR "controlled clinical trial"[pt] OR
"randomized"[tiab] OR "randomised"[tiab] OR "placebo"[tiab] OR "randomly"[tiab] OR
"trial"[tiab])
```

### Scopus Search String (Draft)

```
TITLE-ABS-KEY(("G-CSF" OR "filgrastim" OR "pegfilgrastim" OR "lipegfilgrastim" OR
"granulocyte colony-stimulating factor" OR "Neupogen" OR "Neulasta" OR "Lonquex")
AND ("neutropenia" OR "febrile neutropenia" OR "granulocytopenia")
AND ("cancer" OR "neoplasm" OR "chemotherapy" OR "malignancy")
AND ("randomized" OR "randomised" OR "RCT" OR "placebo" OR "trial"))
```

---

## Search Limits

| Parameter | Setting | Rationale |
|-----------|---------|-----------|
| Date range | No restriction (inception to 2026-03-24) | Comprehensive capture; filgrastim approved 1991 |
| Language | No restriction | Non-English studies will be assessed with translation tools |
| Publication type | No filter beyond RCT terms in strategy | Conference abstracts eligible if sufficient data |
| Species | Human only | Exclude animal studies |

---

## Supplementary Searches

| Source | Method | Purpose |
|--------|--------|---------|
| ClinicalTrials.gov | Keyword search: "G-CSF" AND "neutropenia" AND "cancer" | Identify unpublished or ongoing trials |
| WHO ICTRP | Same keywords | International trial registry coverage |
| Reference lists | Backward citation search of included studies and recent systematic reviews | Capture studies missed by database searches |
| Related systematic reviews | Hand-search reference lists of Cochrane reviews and recent meta-analyses on G-CSF | Ensure completeness |
| Key authors | Forward citation search of seminal G-CSF prophylaxis trials (e.g., Crawford 1991, Vogel 2005, Holmes 2002) | Identify follow-up analyses |

---

## Deduplication Plan

1. Export all results to RIS/BibTeX format
2. Import into a single reference manager
3. Use automated deduplication (ASySD or Endnote)
4. Manual review of suspected duplicates (same first author, year, sample size)
5. Document deduplication results in PRISMA flow diagram

---

## Expected Yield

Based on prior systematic reviews on this topic (e.g., Kuderer et al. 2007, Cooper et al. 2011, Mhaskar et al. 2014, Wang et al. 2015):

- **Estimated total hits**: 1,500-3,000 across all databases
- **After deduplication**: 800-1,500
- **After title/abstract screening**: 80-150
- **After full-text review**: 30-60 RCTs
- **Note**: The literature is mature; the first G-CSF (filgrastim) was approved in 1991

---

## Timeline

| Step | Estimated Time |
|------|---------------|
| Finalize search strings | 1-2 hours |
| Run database searches | 1-2 hours |
| Export and deduplicate | 1 hour |
| Title/abstract screening | 3-5 hours |
| Full-text retrieval | 2-3 hours |
| Full-text screening | 2-3 hours |
| **Total search phase** | **10-16 hours** |

---

## PRISMA-S Checklist Notes

- Search strategy will be reported in full for all databases
- Date of each search will be recorded
- Search filters (RCT) documented with source
- Platform/interface noted (e.g., PubMed via NLM)
- Supplementary search methods documented
