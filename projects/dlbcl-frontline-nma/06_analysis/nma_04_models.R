# =============================================================================
# nma_04_models.R — Bayesian NMA (Primary) + Frequentist (Sensitivity)
# =============================================================================
# PFS outcome, HR scale (log-HR internally)
# =============================================================================

source("nma_02_data_prep.R")

# =============================================================================
# SECTION A: BAYESIAN NMA (PRIMARY)
# =============================================================================

cat("=== Bayesian NMA for PFS (Primary) ===\n")

# --- 1. Prepare gemtc data ---
# gemtc data.re format requires TWO rows per study:
#   - baseline arm: diff = NA, std.err = NA
#   - treatment arm: diff = log(HR), std.err = SE(log(HR))

# Treatment arms (with relative effects)
gemtc_treat <- data.frame(
  study     = nma_data$studlab,
  treatment = nma_data$treat1,
  diff      = nma_data$TE,
  std.err   = nma_data$seTE,
  stringsAsFactors = FALSE
)

# Baseline arms (R-CHOP, with NA)
gemtc_base <- data.frame(
  study     = nma_data$studlab,
  treatment = nma_data$treat2,
  diff      = NA_real_,
  std.err   = NA_real_,
  stringsAsFactors = FALSE
)

# Combine: baseline + treatment arms
gemtc_re <- rbind(gemtc_base, gemtc_treat)
gemtc_re <- gemtc_re[order(gemtc_re$study, is.na(gemtc_re$diff)), ]

network <- mtc.network(data.re = gemtc_re)
cat("Network summary:\n")
summary(network)

# --- 2. Fit consistency model (random-effects) ---
cat("\nFitting Bayesian RE consistency model...\n")
model_re <- mtc.model(
  network,
  type        = "consistency",
  linearModel = "random",
  n.chain     = MCMC_N_CHAINS
)

bayes_re <- mtc.run(
  model_re,
  n.adapt = MCMC_N_ADAPT,
  n.iter  = MCMC_N_ITER,
  thin    = MCMC_THIN
)

# --- 3. Convergence diagnostics ---
cat("\n=== Convergence Diagnostics ===\n")
gelman <- gelman.diag(bayes_re)
cat("Gelman-Rubin:\n")
print(gelman)
max_rhat <- max(gelman$psrf[, "Point est."])
cat("Max Rhat:", round(max_rhat, 3), "\n")

ess <- tryCatch(effectiveSize(bayes_re), error = function(e) {
  cat("ESS calculation error (non-critical):", e$message, "\n")
  NULL
})
if (!is.null(ess)) cat("Min ESS:", min(ess), "\n")

# Trace plots
png(file.path(FIG_DIR, "nma_trace_plots.png"),
    width = 12, height = 10, units = "in", res = FIG_DPI)
plot(bayes_re)
dev.off()

# --- 4. Fixed-effect model (for DIC comparison) ---
cat("\nFitting Bayesian FE model...\n")
model_fe <- mtc.model(network, type = "consistency",
                       linearModel = "fixed", n.chain = MCMC_N_CHAINS)
bayes_fe <- mtc.run(model_fe, n.adapt = MCMC_N_ADAPT,
                     n.iter = MCMC_N_ITER, thin = MCMC_THIN)

# --- 5. DIC comparison ---
cat("\n=== DIC Comparison ===\n")
dic_re <- summary(bayes_re)$DIC
dic_fe <- summary(bayes_fe)$DIC
cat("RE DIC:", dic_re, "| FE DIC:", dic_fe, "\n")
cat("Preferred:", ifelse(dic_re < dic_fe, "Random-effects", "Fixed-effect"), "\n")

# --- 6. Model summary ---
cat("\n=== Bayesian NMA Results (log-HR scale) ===\n")
summary(bayes_re)

# =============================================================================
# SECTION B: FREQUENTIST NMA (SENSITIVITY)
# =============================================================================

cat("\n=== Frequentist NMA (Sensitivity) ===\n")
net_re <- netmeta(
  TE, seTE, treat1, treat2, studlab,
  data            = nma_data,
  sm              = "HR",
  random          = TRUE,
  fixed           = TRUE,
  method.tau      = "REML",
  reference.group = "RCHOP"
)

cat("Frequentist summary:\n")
summary(net_re)

# --- 7. Save summaries ---
sink("nma_model_summary.txt")
cat("========================================\n")
cat("FRONTLINE DLBCL NMA - PFS (PRIMARY)\n")
cat("========================================\n\n")
cat("PRIMARY: Bayesian (gemtc)\n\n")
summary(bayes_re)
cat("\n\nConvergence:\n")
print(gelman.diag(bayes_re))
cat("\n\nSENSITIVITY: Frequentist (netmeta)\n\n")
summary(net_re)
sink()
cat("Model summaries saved.\n")
