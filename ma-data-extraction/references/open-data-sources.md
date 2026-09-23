# Getting primary trial data without institutional access

A meta-analysis run outside a university network loses most publisher full text.
That is a retrieval problem, not an evidence problem: a large share of what a
reviewer needs — per-arm event counts, adverse events, arm sizes, population
characteristics — exists in sources that are free, structured, and often closer
to the primary record than the paper is.

This is the order to work through them, strongest provenance first. Every
extracted cell records which tier it came from, so a sensitivity analysis can
drop the weaker tiers and show whether the conclusion moves.

## Tier 1 — trial registry results

**ClinicalTrials.gov results database.** For trials that posted results, the
API returns per-arm outcome measures and per-arm adverse-event counts. This is
sponsor-reported primary data, not a secondary account of it, and it is often
more complete than the paper: papers summarise safety, the registry tabulates
every term.

```
https://clinicaltrials.gov/api/v2/studies/<NCT>          # full record incl. resultsSection
https://clinicaltrials.gov/api/v2/studies/<NCT>?fields=hasResults
```

What NeoSphere (NCT00545688) yields: the primary outcome as four arm-level pCR
percentages (29.0 / 45.8 / 16.8 / 24.0), plus 4 adverse-event groups, 43 serious
and 72 non-serious event terms — including `Left ventricular dysfunction` and
`Cardiac failure congestive` with numerator and denominator per arm.

**Coverage is the catch.** Posting results is driven by FDAAA, so it tracks
US-registered industry trials. Measured on one HER2 neoadjuvant review: of 27
distinct registered trials among the included studies, **8 had a results
section**. Investigator-initiated, Chinese and European academic trials mostly
do not. Treat Tier 1 as deep rather than broad: the trials it covers are usually
the large ones anchoring the network.

**EU CTR / EudraCT** carries results for European trials that ClinicalTrials.gov
misses, under the same obligation-to-post logic. **WHO ICTRP** federates the
national registries (ChiCTR, jRCT, CTRI) that matter for the Asian trials.

## Tier 2 — registry protocol records

Even without a results section, the protocol record gives arm definitions,
planned and actual enrolment per arm, eligibility, and often baseline
characteristics. This is what converts a reported percentage into an event
count: `round(pct × N_arm)` is defensible when `N_arm` comes from the registry,
and indefensible when it comes from a guess.

NCT ids are frequently absent from a bibliographic manifest but present in the
abstract text. Mine them — in the same review, the manifest column was empty for
every record while **41% of included studies carried an NCT id in their title or
abstract**.

## Tier 3 — open full text

**Europe PMC** is the workhorse. Its REST API searches by PMID or DOI, reports
whether a record is open access, and serves complete JATS full text:

```
https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=EXT_ID:<pmid>&resultType=core&format=json
https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML
```

Full text matters beyond the numbers: risk-of-bias assessment needs the methods
section, and an abstract cannot support a RoB 2 judgement. Supplementary
material, where `hasSuppl=Y`, often holds the per-arm tables the main text
compresses.

**PubMed Central** via efetch, **Unpaywall** for the OA location of a given DOI,
and **OpenAlex** for locations Unpaywall misses, cover the rest. Unpaywall's
`best_oa_pdf_url` is null for a meaningful share of `is_oa=true` records —
bronze and some hybrid articles have a landing page but no direct PDF link, so a
retriever that only follows `best_oa_pdf_url` will under-report what is
reachable. Resolve the landing page before recording `unavailable`.

## Tier 4 — regulatory assessment documents

**EMA European Public Assessment Reports** and **FDA drug approval packages**
are free and contain the efficacy and safety tables the regulator saw, at arm
level, for the registration trials. For a review of licensed agents this is an
underused Tier-1-quality source in a Tier-4 wrapper: it is primary data, but it
is organised by drug rather than by trial, so it takes work to map back.

## Tier 5 — conference abstracts

ASCO, SABCS and ESMO abstracts are free and carry arm-level primary endpoints
for trials not yet published. They are also where the newest agents live. Record
them as abstracts, never as full reports, and never assign a risk-of-bias
judgement from one.

## What not to do

Do not harvest numbers from review articles, news coverage, or discussion posts
that restate a trial's results. They introduce transcription error, frequently
use a different outcome definition than the one you are pooling, and sometimes
report an interim analysis as if it were final. A number whose provenance is
"a review said so" cannot be defended to a reviewer, and one wrong cell
contaminates the audit trail that makes the rest credible.

## Recording provenance

Each extracted value carries its tier and its locator, for example:

| field | value | source_tier | source |
|---|---|---|---|
| pCR events, arm B | 45/107 | `ctgov_results` | NCT00545688 outcome 1 |
| pCR events, arm B | 49 (derived) | `abstract+ctgov_protocol` | 45.8% × N=107 |
| LVEF decline, arm B | 4/107 | `ctgov_results` | NCT00545688 AE, cardiac disorders |
| EFS HR | — | `unavailable` | not in abstract; no full text |

`derived` values must be separable, because the honest sensitivity analysis is
to refit without them and report whether the ranking moved.
