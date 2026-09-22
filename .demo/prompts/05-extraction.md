Stage 05 — data extraction and risk of bias. This is the stage where a demo is most tempted to invent numbers. Do not. Same standing rules, and this one especially: **every cell traces to a retrieved source, or it is blank.**

## Scope decision, made before you start

Only 18 of the 101 included studies have a full PDF; the other 83 are abstract-only. Measured against those abstracts, what is actually recoverable is lopsided:

| field | present in abstracts |
|---|---|
| pCR percentage | 64% |
| randomized N | 35% |
| grade ≥3 AE | 13% |
| cardiac / LVEF | 10% |
| HR with 95% CI | 2% |
| hormone-receptor-positive proportion | 4% |

**So: pCR is the analysis. It is the only outcome that will be networked at Stage 06.** EFS, OS and the safety outcomes are still extracted wherever they genuinely appear, but they will be reported as coverage, not pooled — there is not enough of them to build a network, and a network built on 2% coverage would be a fiction with a credible interval around it.

This is a scope decision, not a data problem, and it gets stated plainly in the manuscript. Do not compensate by estimating what the abstracts do not report.

## Before extracting anything: harvest the open sources

Read `ma-data-extraction/references/open-data-sources.md` and work the tiers in order. Most of what the missing PDFs would have given you exists in free, structured sources that are often *closer to the primary record than the paper* — a paper summarises safety, a registry tabulates every term with a numerator and denominator per arm.

0a. **Mine NCT ids.** The manifest's `nctid` column is empty for every row, but about 41% of the included studies carry an NCT id in their title or abstract. Extract them with a regex over `03_screening/screening-database.csv` and write them back into the manifest. This is a real gap in `create_pdf_manifest.py` — fix it there too so the next run starts with them.

0b. **Tier 1 — ClinicalTrials.gov results.** For every NCT, fetch `https://clinicaltrials.gov/api/v2/studies/<NCT>` and, where `resultsSection` exists, take the per-arm outcome measures and the per-arm adverse-event counts. Expect roughly 8 of the registered trials to have results, and expect them to be the large ones anchoring the network. This is where per-arm cardiac events and grade ≥3 counts come from — the data the abstracts do not have.

0c. **Tier 2 — ClinicalTrials.gov protocol.** For the rest, take arm definitions and per-arm enrolment. This is what makes `round(pct × N_arm)` defensible rather than a guess.

0d. **Tier 3 — Europe PMC.** Query by PMID or DOI (`resultType=core`); where `isOpenAccess=Y` and a `pmcid` exists, fetch `https://www.ebi.ac.uk/europepmc/webservices/rest/<PMCID>/fullTextXML`. Full text is what makes a RoB 2 judgement possible at all — an abstract cannot support one. Check `hasSuppl` too: the per-arm tables are often in the supplement. Also re-try the Unpaywall `is_oa=true` records whose `best_oa_pdf_url` was null: those have an OA landing page but no direct PDF link, and the Stage 04 retriever recorded 151 of them as unavailable without resolving the page.

0e. **Tier 4 — regulatory documents.** For the licensed agents, EMA EPARs and FDA approval packages carry arm-level efficacy and safety tables for the registration trials, free. Use them where a registration trial is otherwise unreachable.

**Do not** take numbers from review articles, news coverage or discussion threads that restate a trial's results. They introduce transcription error, often use a different outcome definition than the one being pooled, and sometimes report an interim analysis as final. One such cell contaminates the audit trail that makes every other cell credible.

Report the retrieval you achieved per tier, and how much it moved the coverage numbers in the scope table above. If Tier 1 and Tier 3 together bring cardiac and grade ≥3 events up to a usable level for the core nodes, say so — the scope decision above can be revisited on evidence, though only for the nodes where the data genuinely exists, and the manuscript must then say which nodes those are.

1. Invoke the `ma-data-extraction` skill.
2. Build the extraction template (`create_extraction_template.py`), then extract, for each included trial and **each arm separately**:
   - trial name, registration number, publication year, design, country/region
   - arm label mapped to one of the treatment nodes fixed at Stage 03b — the node mapping is what makes the network work, so make it explicit and consistent
   - chemotherapy backbone, anthracycline yes/no, number of cycles
   - N randomized and N evaluable per arm
   - pCR events per arm **and the pCR definition the trial used** (ypT0/is ypN0 vs ypT0 ypN0, or breast-only — a previous stage found three definitions in circulation, not two)

     Most abstracts give a percentage rather than a count. Reconstruct the event count as `round(pct × N_arm)` **only when both the arm percentage and the arm N are reported**, and record in a `pcr_derivation` column which of these you did: `reported_count`, `derived_from_pct_and_n`, or `unavailable`. Where the arm N is missing from the abstract, look for it in the trial's ClinicalTrials.gov record — that is a real, citable source and 207 registry records were retrieved for exactly this purpose — and record `nct_arm_n` as the source. Never infer an arm N from a total, and never carry a derived count without its derivation label: the sensitivity analysis at Stage 06 needs to be able to drop every derived row and see what happens.
   - EFS and OS: HR with 95% CI, plus the comparison it refers to and the median follow-up
   - symptomatic cardiac dysfunction / LVEF decline events per arm, grade ≥3 AE events per arm, discontinuation-for-AE events per arm
   - hormone-receptor-positive proportion and node-positive proportion per arm (these are the transitivity variables — without them Stage 06's transitivity tests cannot run)
   - a `source` field: file or URL, and page or table number
3. Run `validate_extraction.py` and `flag_low_confidence.py`. Anything flagged gets verified against the source by hand.
4. Risk of bias: RoB 2 for every randomized trial, into `08_reviews/rob2_assessment.csv`. Judge each domain with a written rationale — an open-label neoadjuvant trial with a pathology endpoint has a real and specific bias profile, so do not paste the same rationale into every row.
5. Write `05_extraction/extraction.sqlite`, `extraction.csv`, and `data-dictionary.md`.

Finish with: trials extracted, arms extracted, total N, how many trials contributed each outcome, which cells are missing and why, and the RoB distribution.
