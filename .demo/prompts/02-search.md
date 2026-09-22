Stage 02 — literature search, through to a screening-ready corpus with abstracts. Same standing rules: no invented data, `round-XX` is immutable, `uv run` for Python, finish the step then stop.

This step ends when screening can actually start. A `.bib` file is not a screening corpus.

1. Invoke the `ma-search-bibliography` skill.

2. **Verify credentials before building anything.** Load `.env` and make a live call against each source; a key present in the file is not a key that authenticates. PubMed E-utilities work without a key at a lower rate limit. Scopus needs `SCOPUS_API_KEY`, and without `SCOPUS_INST_TOKEN` the STANDARD view returns no `dc:description` — so Scopus records arrive without abstracts, which matters at step 6. Report what each source really returns. Where a source is unavailable, substitute one you can genuinely reach (ClinicalTrials.gov) and record it as a protocol deviation in both `02_search/round-01/log.md` and `01_protocol/decision-log.md`. Never fake a source you did not query.

3. **Build the query from concept blocks**, per `01_protocol/search-plan.md`: HER2-positive breast cancer × neoadjuvant/preoperative × randomized design. Search from inception through 2026, no language limit. Keep outcome terms out of the query — filtering on pCR at search time loses trials that report it only in a table.

   Name the anti-HER2 agents explicitly as a fourth, OR-ed block, even though the concept blocks already capture most of them: trastuzumab, pertuzumab, lapatinib, neratinib, T-DM1/trastuzumab emtansine, trastuzumab deruxtecan, **pyrotinib**, tucatinib, margetuximab, inetetamab, disitamab vedotin (RC48), trastuzumab duocarmazine (SYD985), zanidatamab. Expect this block to add few records — a previous run measured 2 — but the completeness claim in the manuscript depends on having searched for them by name, and the cost is one OR clause.

4. **Check `build_queries.py` output before running it.** It has emitted PubMed field tags into the Scopus query string (`TITLE-ABS-KEY("Breast Neoplasms"[MeSH])` is not valid Scopus syntax, and Scopus accepts it silently while returning nonsense). Inspect the generated query per database, and fix the generator rather than the output if it is still wrong.

5. Run the searches, dedupe (`dedupe_bib.py`, `multi_db_dedupe.py`), and write `02_search/round-01/` — `queries.txt`, `results.bib`, `dedupe.bib`, `log.md` — plus `db_counts`, `search_audit` and `search_report`.

6. **Enrich abstracts. Screening on titles alone is not acceptable.** Neither PubMed's BibTeX export nor Scopus's STANDARD view carries abstracts, so the deduplicated corpus will have close to zero:

   ```
   uv run --project tooling/python ma-search-bibliography/scripts/enrich_abstracts.py \
     --in-bib 02_search/round-01/dedupe.bib \
     --out-csv 03_screening/enriched.csv \
     --min-coverage 0.85
   ```

   Note `--project tooling/python`. Without it `uv` resolves a different environment and the script reports `bibtexparser` missing even though it is installed. It falls back PubMed → CrossRef → OpenAlex. Report the coverage you actually achieved; if it lands below 85%, say so rather than proceeding quietly.

7. Build `03_screening/screening-database.csv` with `build_screening_database.py`, from the **enriched CSV** so the abstracts carry through. Nothing else in the pipeline bridges BibTeX to the CSV that `ai_screen.py --stage abstract` expects.

8. Records with no obtainable abstract stay in the corpus, marked `abstract_missing = TRUE`. They are screened on title alone and resolve to *unclear → advance to full text*, never to exclude: dropping a study because its abstract could not be fetched is a retrieval artefact wearing the costume of an eligibility decision. Report the count — it belongs in the PRISMA flow and the limitations section.

9. Registry records (`@misc` from ClinicalTrials.gov) have no abstract by nature. Link them to their publications by NCT id where one exists; treat unlinked registrations as a separate track rather than as screenable records.

A realistic yield is one to three thousand records after dedupe. Fewer than a few hundred means the query is too narrow — loosen it, save the revision as `round-02/`, and leave `round-01/` untouched.

Finish with: records per source, records after dedupe, what the named-agent block added, abstract coverage achieved, how many records are title-only, how many registry records were linked, and any protocol deviation you recorded.
