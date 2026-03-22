# Search Plan — Scoping Review

## Databases
1. **PubMed** (primary) — biomedical literature, MeSH indexing
2. **CrossRef** (supplementary) — broad scholarly coverage, captures non-indexed journals
3. **Semantic Scholar** (supplementary) — AI-curated, citation graph for chaining

## Search Strategy

### Layered approach
Five separate queries targeting each literature layer, then merged and deduplicated.

### Layer 1: Why effort is aversive
**PubMed**: `("cognitive effort"[tiab] OR "mental effort"[tiab] OR "effort cost"[tiab]) AND ("aversive"[tiab] OR "opportunity cost"[tiab] OR "fatigue"[tiab] OR "discomfort"[tiab])`

### Layer 2: Neural metabolic cost
**PubMed**: `("glutamate"[tiab] OR "glycogen"[tiab] OR "metabolic cost"[tiab] OR "neuro-metabolic"[tiab]) AND ("cognitive"[tiab] OR "prefrontal"[tiab] OR "working memory"[tiab]) AND ("fatigue"[tiab] OR "effort"[tiab] OR "depletion"[tiab])`

### Layer 3: Expected value of control / dACC
**PubMed**: `("expected value of control"[tiab] OR "dorsal anterior cingulate"[tiab] OR "dACC"[tiab]) AND ("effort"[tiab] OR "cognitive control"[tiab] OR "cost"[tiab])`

### Layer 4: Predictive processing / interoception
**PubMed**: `("interoceptive"[tiab] OR "prediction error"[tiab] OR "allostatic"[tiab] OR "active inference"[tiab]) AND ("fatigue"[tiab] OR "discomfort"[tiab] OR "effort"[tiab] OR "cognitive"[tiab])`

### Layer 5: Cognitive stress & headache in healthy populations
**PubMed**: `("cognitive"[tiab] OR "mental"[tiab]) AND ("stress"[tiab] OR "fatigue"[tiab]) AND ("headache"[tiab] OR "head pain"[tiab] OR "discomfort"[tiab]) AND ("healthy"[tiab] OR "non-clinical"[tiab] OR "normal"[tiab])`

### Supplementary: Citation chaining
Seed DOIs for forward/backward citation chaining via Semantic Scholar:
- 10.1016/j.cub.2022.07.010 (Wiehler 2022)
- 10.3389/fnins.2015.00289 (Christie 2015)
- 10.1371/journal.pone.0198204 (Otto 2018)
- 10.1016/j.neubiorev.2021.12.016 (Yee 2022)

## Deduplication
- By DOI (primary)
- By PMID (secondary)
- By normalized title (tertiary)

## Expected Results
- PubMed: 200-500 records across 5 layers
- CrossRef: 100-300 additional records
- Semantic Scholar: 100-400 from search + citation chaining
- After deduplication: estimated 300-800 unique records for screening
- After screening: estimated 20-60 included studies
