Stages 08–09 — peer review, GRADE, and quality assurance. Same standing rules. Your job in this step is to be hostile to the work you just produced.

1. Invoke `ma-peer-review`:
   - GRADE for NMA (CINeMA logic) across every comparison that matters: risk of bias, indirectness, inconsistency, imprecision, publication bias — plus the within/between-network incoherence that only an NMA has. Write `08_reviews/grade_summary.csv`.
   - Summary-of-findings table for the primary outcome.
   - Reviewer 1 and Reviewer 2 passes, written as a real reviewer would: the objections most likely to arrive from a journal, and what in the manuscript answers them. Save to `08_reviews/`.
2. Invoke `ma-publication-quality`:
   - `uv run ma-end-to-end/scripts/run_robustness_checks.py --root projects/neo-her2-ebc`
   - PRISMA-NMA checklist — the 32-item version, not the 27-item one
   - `claim_audit.py` for overclaiming. Fix every hit at source in the manuscript instead of arguing with the tool; "X was superior" where the interval crosses the null is exactly what this catches.
   - `crossref_report.py` to verify the citations resolve
   - `uv run ma-end-to-end/scripts/publication_readiness_score.py --root projects/neo-her2-ebc` — **target ≥95%**
   - `uv run ma-network-meta-analysis/scripts/validate_nma_outputs.py --root projects/neo-her2-ebc`
   - the 25-item NMA completion checklist in `ma-network-meta-analysis/references/nma-completion-checklist.md`
3. `uv run ma-end-to-end/scripts/validate_stage_transition.py --root projects/neo-her2-ebc --from-stage 08_reviews --to-stage 09_qa` and write `09_qa/pipeline-checklist.md` and `09_qa/stage_transition_report.md`.

If the readiness score lands below 95%, fix what it names and re-run it. Report the score you actually measured, not the one you were aiming at.

Finish with: the readiness score, PRISMA-NMA items complete out of 32, GRADE ratings per comparison, the claim-audit hits and how you resolved each, and the strongest objection a reviewer will raise that you cannot fully answer.
