Stage 02, round 02 — the Scopus credentials you were missing now exist. Same standing rules: no invented data, `round-01/` stays untouched, `uv run` for Python, finish the step then stop.

A `.env` file now exists in the repo root with `PUBMED_API_KEY` and `SCOPUS_API_KEY` set. `EMBASE_*` and `COCHRANE_*` are still empty. This is the remediation path you yourself wrote into `02_search/round-01/log.md` §5, so take it.

1. Confirm what the keys actually unlock — load `.env` and make a live call to each. A key present in the file is not the same as a key that authenticates; report what each one really returns. Note that `SCOPUS_INST_TOKEN` is empty, which limits Scopus to whatever the key alone authorises.
2. Fix the bug you found before you use it: `build_queries.py` emits PubMed field tags into the Scopus query string (`TITLE-ABS-KEY("Breast Neoplasms"[MeSH])` is not valid Scopus syntax). Correct it in `ma-search-bibliography/scripts/build_queries.py` so the Scopus block is syntactically valid Scopus, keep the PubMed behaviour unchanged, and record the fix in `01_protocol/decision-log.md`. This is a real repo bug the demo surfaced — fixing it is part of the deliverable.
3. Re-run the search into a **new** `02_search/round-02/` directory: PubMed (now keyed, so higher rate limit) + Scopus, plus ClinicalTrials.gov again for registry coverage. Do not touch `round-01/`.
4. Dedupe across all sources, then dedupe round-02 against round-01 so you can report what Scopus added that PubMed alone missed — that delta is the honest measure of what the missing credential was costing.
5. Update `02_search/round-02/log.md`, `queries.txt`, `db_counts`, `search_audit`, `search_report`, and revise the protocol-deviation section: Scopus is no longer a deviation, Embase and Cochrane CENTRAL still are.
6. `round-02/dedupe.bib` becomes the input to screening. Say so explicitly in the log so Stage 03 picks up the right file.

Finish with: records per source, unique records added by Scopus over round-01, the total going into screening, which databases remain unavailable, and confirmation that round-01 is unmodified.
