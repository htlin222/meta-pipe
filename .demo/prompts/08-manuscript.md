Stage 07 — the manuscript. Same standing rules, plus one that matters most here: **the manuscript may not claim more than Stage 06 measured.** A wide credible interval is a wide credible interval in the abstract too.

1. Invoke the `ma-manuscript-quarto` skill.
   **The scope limitation goes in the abstract, not only the limitations section.** This review networks pCR alone. EFS, OS and safety were pre-specified in the protocol and are not pooled, because full-text retrieval reached only 18 of 101 included studies and the remaining abstracts carry HR with CI in 2% and cardiac outcomes in 10%. A reader who sees only the abstract must still learn that this is a single-outcome network. Say it in the Methods as a scope decision with its reason, restate it in the Discussion, and never let the Results imply a breadth the analysis does not have.

2. **Phase 1 is mandatory**: fill `07_manuscript/manuscript_outline.md` first — section-by-section, with the key numbers slotted in. The repo's workflow asks for user approval here; the orchestrating session is acting as the user, so write the outline, then continue into Phase 2 in the same turn and flag anything in the outline you think a human should overrule.
3. Phase 2 — write the sections as Quarto:
   - Introduction: why regimen choice in neoadjuvant HER2-positive disease is genuinely unsettled, and what a network adds over the existing pairwise meta-analyses
   - Methods: PRISMA-NMA compliant — protocol, eligibility, sources (including the database substitution recorded at Stage 02), screening with kappa, extraction, RoB 2, the Bayesian model and priors, transitivity, inconsistency, ranking
   - Results: study characteristics table, network description, primary pCR results, EFS/OS, safety, inconsistency, sensitivity analyses
   - Discussion: what changes clinical practice, what does not, and an honest limitations section — the pCR-definition heterogeneity, the sparse nodes for the newest agents, the surrogacy gap between pCR and long-term outcome, and the search limitation from Stage 02
   - Abstract last, once the numbers are fixed
4. Target format: Lancet Oncology / JAMA Oncology conventions, roughly 3,500–5,000 words.
5. Assemble the tables (study characteristics, league table, GRADE summary) and reference both the journal and presentation figure sets.
6. Render to `07_manuscript/index.html` and `index.pdf`. If a render fails, fix it — an unrendered manuscript is not a manuscript.
   **Run `quarto render` with the working directory set to `07_manuscript/`, never the repo root.** Quarto's dotenv reads `.env`/`.env.example` from the current directory and treats every key in `.env.example` as required and non-empty; the repo's `.env` is only partly filled, so a render started at the repo root dies before it reads your document. From the manuscript directory neither file is visible and it renders normally.

Finish with: word count, section list, the rendered file paths, and the three sentences you are least confident are supported by the data.
