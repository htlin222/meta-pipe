Stage 02, round 03 — close the two gaps you found, then build the screening input. These are decisions, not questions: you raised D-019 and D-021 correctly, and here is how they resolve.

**Decision on D-021 (incomplete intervention terms): expand and re-run.** Pyrotinib is not a rounding error — it anchors several Chinese neoadjuvant HER2 RCTs, and a network missing that node is incomplete rather than merely smaller. Do a `round-03` search adding the anti-HER2 agents the term list omits. At minimum: pyrotinib, tucatinib, margetuximab, inetetamab, disitamab vedotin (RC48), trastuzumab duocarmazine (SYD985), zanidatamab, and any further agent your own term expansion surfaces. Keep the existing terms; this is an addition. `round-01` and `round-02` stay untouched.

**Decision on D-019 (no abstracts): fetch them, and do not screen on titles alone.** The repo already has the tool — you did not find it because it aborts on a missing dependency and because of how `uv` resolves its project:

```
uv run --project tooling/python ma-search-bibliography/scripts/enrich_abstracts.py \
  --in-bib 02_search/round-03/dedupe.bib \
  --out-csv 03_screening/enriched.csv \
  --min-coverage 0.85
```

`bibtexparser` is now installed. Note the `--project tooling/python` — without it `uv` resolves a different environment and the script reports the dependency as missing even though it is present. Record that invocation in `ma-search-bibliography/SKILL.md` so the next person does not lose an hour to it. The script falls back PubMed → CrossRef → OpenAlex, so coverage should be high.

Then:

1. Run the round-03 search (PubMed + Scopus + ClinicalTrials.gov), dedupe within round-03 and against rounds 01–02, and report what the new terms added.
2. Enrich abstracts over the round-03 corpus. Report the coverage you actually achieved. If it lands below 85%, say so rather than proceeding quietly.
3. Build `03_screening/screening-database.csv` with `build_screening_database.py`, from the **enriched CSV** so the abstracts carry through.
4. Records for which no abstract can be obtained anywhere: keep them in the corpus, mark them `abstract_missing = TRUE`, and screen them on title alone — but they resolve to *unclear → advance to full text*, never to exclude. Excluding a study because its abstract could not be fetched is a retrieval artefact masquerading as an eligibility decision. Report that count; it goes in the PRISMA flow and the limitations section.
5. Registry records (`@misc` from ClinicalTrials.gov) have no abstract by nature. Handle them as D-018 anticipated: link them to their publications by NCT id where one exists, and treat unlinked registrations as a separate track rather than as screenable records.

Finish with: new records added by the expanded terms, the round-03 total going into screening, abstract coverage achieved, how many records are title-only, and how many registry records were linked to publications versus left unlinked.
