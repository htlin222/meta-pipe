You are the worker session for an end-to-end demonstration of the meta-pipe pipeline in /Users/htlin/meta-pipe. Another Claude Code session is orchestrating you over the herdr socket API: it reads `projects/neo-her2-ebc/.progress/PROGRESS.md` (written by this repo's Stop hook) after each of your turns and then sends the next step. So: do the step you are given, completely, then stop. Do not ask me questions — every decision you need has been made below or in TOPIC.txt. When a decision is genuinely missing, pick the option that the repo's own SKILL.md documents as the default, write the choice and your reasoning into `01_protocol/decision-log.md`, and continue.

Two rules that hold for the whole project and override any instinct to be helpful:

1. **Never invent study data.** Every number that ends up in the extraction database or the manuscript must be traceable to a source you actually retrieved. If a full text or an arm-level number cannot be obtained, record it as missing and say so in the artifacts. A demo with honest gaps is the deliverable; a demo with fabricated trial results is a failure.
2. **Keep the audit trail.** Never overwrite a `round-XX` directory, use `rip` instead of `rm`, run Python through `uv run`, and use absolute paths.

## This step: Stage 00–01 (feasibility + protocol)

Project: `neo-her2-ebc` — already initialized at `projects/neo-her2-ebc/`, with `TOPIC.txt` filled in. Read it first.

1. Read `CLAUDE.md`, then invoke the `ma-topic-intake` skill and run the mandatory feasibility assessment (`ma-topic-intake/references/feasibility-checklist.md`). Write the result to `01_protocol/feasibility-assessment.md`. This topic is expected to pass — the point is to show the gate running and to surface the real risks (heterogeneous pCR definitions, chemotherapy-backbone variation across trials, sparse nodes for the newest agents).
2. Invoke the `ma-end-to-end` skill so you have the stage map, then produce the Stage 01 artifacts:
   - `01_protocol/pico.yaml` — including `analysis_type.preliminary: nma_candidate` (TOPIC.txt lists well over three competing regimens with trastuzumab + chemotherapy as the common node). Leave `analysis_type.confirmed` unset; it is decided at the Stage 03b gate.
   - `01_protocol/eligibility.md` — inclusion/exclusion criteria operational enough that a screener can apply them without asking you anything.
   - `01_protocol/outcomes.md` — outcome definitions, effect measures (RR for pCR and the binary safety outcomes, HR for EFS/OS), and how you will handle the two competing pCR definitions.
   - `01_protocol/search-plan.md` — databases, the concept blocks, and the date window.
   - `01_protocol/decision-log.md` — start it now and keep appending for the rest of the project.
   - `01_protocol/analysis-type-decision.md` — copy the repo's template and fill in Stage 1 only.
3. Generate the PROSPERO-style protocol with `uv run tooling/python/generate_prospero_protocol.py` if the script supports this project layout; if it does not, write the protocol by hand into `01_protocol/` and note the deviation in the decision log.

Stop when those files exist. Finish your turn with a 5-line summary: feasibility verdict, the preliminary analysis type, the number of treatment nodes you expect, the biggest threat to transitivity, and what Stage 02 should search.
