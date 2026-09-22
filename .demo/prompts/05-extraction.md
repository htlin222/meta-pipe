Stage 05 — data extraction and risk of bias. This is the stage where a demo is most tempted to invent numbers. Do not. Same standing rules, and this one especially: **every cell traces to a retrieved source, or it is blank.**

1. Invoke the `ma-data-extraction` skill.
2. Build the extraction template (`create_extraction_template.py`), then extract, for each included trial and **each arm separately**:
   - trial name, registration number, publication year, design, country/region
   - arm label mapped to one of the treatment nodes fixed at Stage 03b — the node mapping is what makes the network work, so make it explicit and consistent
   - chemotherapy backbone, anthracycline yes/no, number of cycles
   - N randomized and N evaluable per arm
   - pCR events per arm **and the pCR definition the trial used** (ypT0/is ypN0 vs ypT0 ypN0)
   - EFS and OS: HR with 95% CI, plus the comparison it refers to and the median follow-up
   - symptomatic cardiac dysfunction / LVEF decline events per arm, grade ≥3 AE events per arm, discontinuation-for-AE events per arm
   - hormone-receptor-positive proportion and node-positive proportion per arm (these are the transitivity variables — without them Stage 06's transitivity tests cannot run)
   - a `source` field: file or URL, and page or table number
3. Run `validate_extraction.py` and `flag_low_confidence.py`. Anything flagged gets verified against the source by hand.
4. Risk of bias: RoB 2 for every randomized trial, into `08_reviews/rob2_assessment.csv`. Judge each domain with a written rationale — an open-label neoadjuvant trial with a pathology endpoint has a real and specific bias profile, so do not paste the same rationale into every row.
5. Write `05_extraction/extraction.sqlite`, `extraction.csv`, and `data-dictionary.md`.

Finish with: trials extracted, arms extracted, total N, how many trials contributed each outcome, which cells are missing and why, and the RoB distribution.
