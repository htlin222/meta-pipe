Stage 06 — the network meta-analysis. Same standing rules.

**Scope: pCR is the only outcome that gets a network.** EFS, OS and the safety outcomes were extracted where they genuinely appeared, but abstract-only sourcing left them at 2–13% coverage. Report that coverage honestly in `06_analysis/tables/` and say which outcome failed for want of how many connected trials. Do not build a network on them, and do not describe the absence as "insufficient data" as though it were a property of the literature — it is a property of this run's retrieval.

Confirm `analysis_type.confirmed` in `01_protocol/pico.yaml` before you begin. If it says anything other than `nma`, follow that route instead and tell me — the honest answer beats the impressive one.

1. Invoke the `ma-network-meta-analysis` skill and read `references/nma-r-guide.md`.
2. Set up R with `renv` inside `06_analysis/`. Copy the script templates from `ma-network-meta-analysis/assets/r/` and adapt them; `projects/dlbcl-frontline-nma/06_analysis/` is a worked precedent in this repo — read it before writing your own.
3. Run the sequence:
   - `nma_01_setup.R`, `nma_02_data_prep.R` — long/wide arm-level data keyed to the Stage 03b node names
   - `nma_03_network_graph.R` — network geometry, node size by sample size, edge width by number of trials
   - `nma_04_models.R` — **Bayesian random-effects NMA as the primary analysis** (RR for pCR), frequentist NMA as the sensitivity analysis. Report the between-study heterogeneity τ with its interval.
   - `nma_05_inconsistency.R` — node-splitting and design-by-treatment interaction. If any loop is inconsistent, investigate it rather than reporting the p-value and moving on.
   - `nma_06_forest_plots.R` — every treatment against trastuzumab + chemotherapy
   - `nma_07_ranking.R` — SUCRA and rankograms. State plainly in the text that a rank is not an effect size: a sparse node can rank first on almost no evidence, and the reader must be able to see that.
   - `nma_08_funnel.R` — comparison-adjusted funnel plot
   - `nma_09_sensitivity.R` — at minimum: the alternative pCR definition, anthracycline-free trials only, and low-risk-of-bias trials only
   - `nma_10_tables.R` — league table. **Assert the orientation at runtime; do not trust the comment or the transpose.** `netmeta::netleague()` returns the lower triangle as *column versus row* and the upper as the *direct* estimate, so a table read with the natural "this row versus that column" instinct comes out inverted — and an inverted league table is invisible, because every cell is still a plausible risk ratio. Tested on synthetic data where THP is decisively better than chemotherapy alone (event rates 0.52 vs 0.17), `netmeta` holds `TE.random[THP, CT] = 1.246` (RR 3.48, correct) while the raw `netleague()` cell at row THP, column CT reads `0.29` — the exact reversal.

     So: after building the table, pick the node pair with the largest separation in the network, recompute its effect directly from the model object, and check the sign agrees with the league cell. Abort with a loud error if it does not. Put that assertion in the script, not in a comment, and state the orientation in the table's own caption and column header — not only in the file header — because the CSV outlives the script that made it.
   - `nma_13_transitivity_tests.R` — always, for an NMA
   - `nma_11_cnma.R` if the combination regimens support a component analysis (trastuzumab / pertuzumab / lapatinib / chemotherapy as components — this network is a good candidate)
   - `nma_12_meta_regression.R` if you extracted enough study-level covariates (HR+ proportion, node-positive proportion)
4. **Honour the four binding conditions pre-committed at the Stage 03b gate** (`01_protocol/analysis-type-decision.md` §2e). They were fixed before any result was seen, precisely so they could not be renegotiated afterwards:
   - every NMA estimate is reported beside its direct pairwise estimate; where they disagree, both are shown and the network estimate never stands alone
   - `N8` and `N9` are single-trial nodes: CINeMA no higher than Low for imprecision, SUCRA rank stated only with the instability caveat in the same sentence, and neither may be called "best" anywhere, least of all in the abstract
   - the era-restricted sensitivity network (pertuzumab era, 2013+) is required, not optional — it is the main defence against the backbone/era confound
   - backbone enters as a meta-regression covariate, and CNMA is run

   Condition 4 depends on covariates that abstract-only sourcing may not supply. If the covariate coverage is too thin to fit, say so and report the coverage — do not quietly drop the condition, and do not fit it on a handful of studies and present it as though it were powered.

5. **Sensitivity analysis on derived data**: refit the primary model excluding every arm whose pCR count carries `pcr_derivation = derived_from_pct_and_n`. If the ranking moves, that is a headline finding about the method, not a footnote.
6. Validate: `uv run ma-network-meta-analysis/scripts/validate_nma_outputs.py --root projects/neo-her2-ebc`.
7. Write everything to `06_analysis/` — scripts, `figures/`, `tables/`, and `renv.lock`. Figures at ≥300 DPI.

Finish with: the pCR coverage (how many trials, arms and patients actually entered the network), the pCR effect estimate and credible interval for each node versus trastuzumab + chemotherapy, τ, the inconsistency verdict, the SUCRA order with a one-line caveat on which ranks rest on thin evidence, and what the safety picture does to the pCR ranking.
