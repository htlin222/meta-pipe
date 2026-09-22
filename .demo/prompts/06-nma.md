Stage 06 — the network meta-analysis. Same standing rules.

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
   - `nma_10_tables.R` — league table, with both directions unambiguous
   - `nma_13_transitivity_tests.R` — always, for an NMA
   - `nma_11_cnma.R` if the combination regimens support a component analysis (trastuzumab / pertuzumab / lapatinib / chemotherapy as components — this network is a good candidate)
   - `nma_12_meta_regression.R` if you extracted enough study-level covariates (HR+ proportion, node-positive proportion)
4. Repeat the primary model for EFS and OS on the HR scale, and for the three safety outcomes on the RR scale, wherever the network supports it. Where it does not, say which outcome had too few connected trials.
5. Validate: `uv run ma-network-meta-analysis/scripts/validate_nma_outputs.py --root projects/neo-her2-ebc`.
6. Write everything to `06_analysis/` — scripts, `figures/`, `tables/`, and `renv.lock`. Figures at ≥300 DPI.

Finish with: the pCR effect estimate and credible interval for each node versus trastuzumab + chemotherapy, τ, the inconsistency verdict, the SUCRA order with a one-line caveat on which ranks rest on thin evidence, and what the safety picture does to the pCR ranking.
