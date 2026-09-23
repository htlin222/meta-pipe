Stage 03 — title/abstract screening, then the Stage 03b analysis-type gate.

The corpus now has abstracts and the sharding you built is in place, so the two things that blocked you are resolved. One more must be fixed before a single record is screened.

**Fix the dual-review defect first.** You found that the reviewer-2 pass re-reads a file whose Reviewer1 columns are empty and overwrites `decisions.csv`, which silently destroys half of an independent dual review — the exact thing the kappa is supposed to measure. Fix it properly in `tooling/python/ai_screen.py`: a reviewer pass must merge into the existing decisions rather than replace them, and must never clear another reviewer's column. Add a guard that refuses to write if it would reduce the number of populated cells in a column it does not own. Record the fix in `01_protocol/decision-log.md` and note it in `ma-screening-quality/SKILL.md`. This is a real repo bug and fixing it is part of the deliverable.

Then:

1. Invoke the `ma-screening-quality` skill.
2. Run genuine dual independent review over `03_screening/screening-database.csv`, sharded so it finishes in reasonable time:
   - reviewer 1: `uv run tooling/python/ai_screen.py --project neo-her2-ebc --stage abstract --reviewer 1 --shard i/16` for i in 1..16, in parallel
   - reviewer 2: the same with `--reviewer 2`
   - merge with `merge_screening_shards.py`, and verify the merged record count equals the input count exactly — a lost record is a corrupted PRISMA flow
   Apply `01_protocol/eligibility.md` as written. The two reviewers must judge independently; if reviewer 2 can see reviewer 1's call, the kappa measures nothing.
3. Compute agreement into `03_screening/round-01/agreement.md`. **Gate: kappa ≥ 0.60.** If it comes in lower, that is a finding, not an obstacle: identify which criterion the disagreements cluster on, sharpen it, record the change, re-screen as `round-02/`, and report both rounds.
4. Resolve conflicts, then write `03_screening/round-01/decisions.csv` and `included.bib`. Records flagged `abstract_missing` resolve to unclear → full text, never to exclude.

### Stage 03b — the analysis-type confirmation gate

The decision the whole project turns on. Do it explicitly.

- Tally the included studies by the treatment arms they contribute, mapped to the `N1`–`N10` nodes fixed at Stage 01. Anything that maps to none of them is an `N_other` escalation — handle it per `eligibility.md` §3 rather than forcing it into a neighbouring node.
- Draw the network: is it connected through trastuzumab + chemotherapy? Which nodes are orphans, reachable only through a single trial with no shared comparator?
- Assess transitivity across the effect modifiers in TOPIC.txt — hormone receptor mix, nodal status, anthracycline vs anthracycline-free backbone, pCR definition. You already identified the sharpest threat at Stage 01: chemotherapy backbone is confounded with both node and trial era, so the "control" arm does not mean the same thing across the network. Say what that does to the transitivity assumption now, in writing.
- If >30% of included records are single-arm, or the network is disconnected, downgrade to pairwise plus pooled proportions and mean it. A forced NMA over a broken network is worse than an honest pairwise analysis, and this pipeline supports that route.

Write the verdict into the Stage 2 section of `01_protocol/analysis-type-decision.md` and set `analysis_type.confirmed` in `01_protocol/pico.yaml`. Stage 06 does not start until that field is set.

Finish with: records screened, kappa, number included, the confirmed analysis type, the node list with trial counts per node, which nodes are sparse or orphaned, and your written transitivity judgement.
