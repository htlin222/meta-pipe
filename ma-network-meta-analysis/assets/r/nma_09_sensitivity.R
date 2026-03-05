# =============================================================================
# nma_09_sensitivity.R — Sensitivity Analyses & CINeMA (GRADE for NMA)
# =============================================================================
# Purpose: Frequentist sensitivity (netmeta), leave-one-out, CINeMA assessment
# Input: bayes_re, net_re, nma_data from previous scripts
# Output: sensitivity report, CINeMA framework summary
# =============================================================================

source("nma_04_models.R")

# =============================================================================
# SECTION A: FREQUENTIST vs BAYESIAN CONCORDANCE
# =============================================================================

cat("=== Frequentist vs Bayesian Concordance ===\n")
cat("Primary: Bayesian (gemtc) | Sensitivity: Frequentist (netmeta)\n\n")

# Compare key results
cat("Bayesian results (posterior medians):\n")
summary(bayes_re)

cat("\nFrequentist results (REML):\n")
summary(net_re)

cat("\nIf results are concordant, report in manuscript:\n")
cat("'Frequentist sensitivity analysis using netmeta (REML) yielded\n")
cat(" consistent results (Supplement Table SX), supporting robustness.'\n")

# =============================================================================
# SECTION B: LEAVE-ONE-OUT ANALYSIS
# =============================================================================

cat("\n=== Leave-One-Out Analysis ===\n")
studies <- unique(nma_data$studlab)
loo_results <- list()

for (s in studies) {
  data_loo <- nma_data[nma_data$studlab != s, ]

  # Check connectivity after removal
  nc_loo <- tryCatch(
    netconnection(data_loo$treat1, data_loo$treat2, data_loo$studlab),
    error = function(e) NULL
  )

  if (is.null(nc_loo) || nc_loo$n.subnets > 1) {
    cat("Skipping", s, "- removal disconnects network\n")
    next
  }

  # Use frequentist for speed in leave-one-out
  net_loo <- tryCatch(
    netmeta(TE, seTE, treat1, treat2, studlab,
            data = data_loo, sm = "RR",
            random = TRUE, method.tau = "REML"),
    error = function(e) NULL
  )

  if (!is.null(net_loo)) {
    loo_results[[s]] <- list(
      excluded = s,
      tau2     = net_loo$tau2,
      I2       = net_loo$I2
    )
  }
}

# Summarize leave-one-out
loo_df <- do.call(rbind, lapply(loo_results, function(x) {
  data.frame(Excluded = x$excluded,
             tau2 = round(x$tau2, 4),
             I2_pct = round(x$I2 * 100, 1),
             stringsAsFactors = FALSE)
}))

if (nrow(loo_df) > 0) {
  cat("\n--- Leave-One-Out Results ---\n")
  cat("Full model tau² (frequentist):", round(net_re$tau2, 4), "\n")
  cat("Full model I²:", round(net_re$I2 * 100, 1), "%\n\n")
  print(loo_df)
  write_csv(loo_df, file.path(TBL_DIR, "nma_leave_one_out.csv"))
}

# =============================================================================
# SECTION C: EXCLUDE HIGH RISK-OF-BIAS STUDIES
# =============================================================================

cat("\n=== High RoB Sensitivity ===\n")
# Uncomment and adapt when RoB data available:
# high_rob_studies <- c("Study1", "Study2")
# data_low_rob <- nma_data[!nma_data$studlab %in% high_rob_studies, ]
#
# # Bayesian sensitivity on low-RoB subset
# gemtc_low_rob <- data.frame(
#   study = data_low_rob$studlab,
#   treatment = data_low_rob$treat1,
#   diff = data_low_rob$TE,
#   std.err = data_low_rob$seTE
# )
# network_low_rob <- mtc.network(data.re = gemtc_low_rob)
# model_low_rob <- mtc.model(network_low_rob, type = "consistency",
#                             linearModel = "random", n.chain = MCMC_N_CHAINS)
# bayes_low_rob <- mtc.run(model_low_rob, n.adapt = MCMC_N_ADAPT,
#                           n.iter = MCMC_N_ITER, thin = MCMC_THIN)
# summary(bayes_low_rob)
cat("Adapt this section with your risk-of-bias classifications.\n")

# =============================================================================
# SECTION D: CONTRIBUTION MATRIX
# =============================================================================

cat("\n=== Contribution Matrix ===\n")
cat("Shows how much each direct comparison contributes to each NMA estimate.\n\n")

# netcontrib() requires netmeta >= 2.5.0
if (packageVersion("netmeta") >= "2.5.0") {
  nc <- netcontrib(net_re)
  contrib_df <- as.data.frame(nc$random)
  write.csv(contrib_df, file.path(TBL_DIR, "contribution_matrix.csv"), row.names = TRUE)
  cat("Contribution matrix saved to", file.path(TBL_DIR, "contribution_matrix.csv"), "\n")

  # Heatmap of contributions
  png(file.path(FIG_DIR, "nma_contribution_heatmap.png"),
      width = FIG_WIDTH + 2, height = FIG_HEIGHT + 2, units = "in", res = FIG_DPI)
  netheat(net_re, random = TRUE)
  dev.off()
  cat("Contribution heatmap saved to", file.path(FIG_DIR, "nma_contribution_heatmap.png"), "\n")
} else {
  cat("netcontrib() requires netmeta >= 2.5.0. Skipping contribution matrix.\n")
  cat("Update with: install.packages('netmeta')\n")
}

# =============================================================================
# SECTION E: CINeMA (GRADE FOR NMA) — FRAMEWORK
# =============================================================================

cat("\n=== CINeMA Assessment Framework (GRADE for NMA) ===\n")
cat("CINeMA evaluates certainty of evidence for each comparison in NMA.\n\n")

cat("The 6 CINeMA domains:\n")
cat("1. Within-study bias (from RoB assessments)\n")
cat("2. Across-study bias (reporting bias, comparison-adjusted funnel)\n")
cat("3. Indirectness (transitivity concerns)\n")
cat("4. Imprecision (width of credible intervals)\n")
cat("5. Heterogeneity (between-study variance)\n")
cat("6. Incoherence (inconsistency between direct and indirect)\n")

cat("\nRating scale: No concerns | Some concerns | Major concerns\n")
cat("Overall: High | Moderate | Low | Very low\n\n")

cat("IMPORTANT: CINeMA is the #3 reviewer rejection reason (after\n")
cat("inconsistency handling and transitivity assessment).\n\n")

cat("Tools for CINeMA:\n")
cat("- Web app: https://cinema.ispm.unibe.ch/\n")
cat("- R package: Not yet available as standalone (use web app)\n")
cat("- Input: netmeta or gemtc results + RoB assessments\n\n")

# Generate CINeMA input template
cinema_treatments <- sort(unique(c(nma_data$treat1, nma_data$treat2)))
n_treat <- length(cinema_treatments)
n_comparisons <- n_treat * (n_treat - 1) / 2

cat("Your network has", n_treat, "treatments and", n_comparisons, "pairwise comparisons.\n")
cat("Prepare CINeMA assessment for all", n_comparisons, "comparisons.\n")

# Create CINeMA template
cinema_template <- expand.grid(
  treat1 = cinema_treatments,
  treat2 = cinema_treatments,
  stringsAsFactors = FALSE
) %>%
  filter(treat1 < treat2) %>%
  mutate(
    within_study_bias = NA_character_,
    across_study_bias = NA_character_,
    indirectness      = NA_character_,
    imprecision       = NA_character_,
    heterogeneity     = NA_character_,
    incoherence       = NA_character_,
    overall_certainty = NA_character_
  )

write_csv(cinema_template, file.path(TBL_DIR, "cinema_template.csv"))
cat("CINeMA template saved to", file.path(TBL_DIR, "cinema_template.csv"), "\n")
cat("Fill in each domain rating and overall certainty.\n")

# =============================================================================
# SECTION F: SAVE SENSITIVITY REPORT
# =============================================================================

sink("nma_sensitivity_report.txt")
cat("=== NMA Sensitivity Analysis Report ===\n\n")

cat("--- Bayesian vs Frequentist Concordance ---\n")
cat("Primary: gemtc (Bayesian, random-effects)\n")
cat("Sensitivity: netmeta (frequentist, REML)\n\n")

cat("--- Leave-One-Out ---\n")
if (exists("loo_df") && nrow(loo_df) > 0) print(loo_df)

cat("\n--- CINeMA Status ---\n")
cat("Template generated:", file.path(TBL_DIR, "cinema_template.csv"), "\n")
cat("Comparisons to rate:", n_comparisons, "\n")
sink()
cat("\nSensitivity report saved to nma_sensitivity_report.txt\n")
