Stage 04 — full-text retrieval and full-text eligibility screening. Same standing rules.

1. Invoke the `ma-fulltext-management` skill.
2. Retrieve full texts for everything in `03_screening/round-01/included.bib`. Use the repo's retrieval path (Unpaywall / open-access resolution, `create_pdf_manifest.py`, `extract_pdf_text.py`). Many of these trials — NeoSphere, NeoALTTO, TRYPHAENA, KRISTINE, CALGB 40601, NSABP B-41, PHERGain, IMpassion050 — have accessible primary publications, so a substantial fraction should resolve.
3. Record every record in `04_fulltext/manifest.csv` with an honest retrieval status. A paywalled paper is `unavailable`, not a guess. Where the PDF is unavailable but a registry entry or a published abstract carries the arm-level pCR numbers, record that as the source and mark it as such — the provenance has to survive into the extraction table.
4. Stage 04b — full-text eligibility screening (PRISMA 2020 item 16, mandatory):
   - `uv run tooling/python/ai_screen.py --project neo-her2-ebc --stage fulltext --reviewer 1`
   - the same with `--reviewer 2`
   - `uv run ma-end-to-end/scripts/audit_screening_quality.py --project neo-her2-ebc`
   - kappa via `dual_review_agreement.py` on `04_fulltext/fulltext_decisions.csv` (cols `FT_Reviewer1_Decision` / `FT_Reviewer2_Decision`) into `04_fulltext/ft_agreement.md`
   - resolve conflicts; **every exclusion at this stage needs a stated reason**, because PRISMA requires the reason list in the flow diagram
5. Only rows with `FT_Final_Decision = include` go forward to Stage 05.

If retrieval leaves the network too thin to answer the question, say so now rather than at Stage 06 — that is the cheap moment to find out.

Finish with: attempted / retrieved / unavailable counts, full-text kappa, final included studies, exclusion reasons with counts, and whether the network still holds together.
