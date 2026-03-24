#!/usr/bin/env Rscript
# =============================================================================
# NMA Step 03: Frequentist NMA Model (Random Effects, REML)
# Project: G-CSF Prophylaxis in Chemotherapy-Induced Neutropenia
# Primary outcome: Febrile neutropenia incidence (RR)
# =============================================================================

library(netmeta)
library(meta)
library(readr)

analysis_dir <- "projects/gcsf-neutropenia/06_analysis"
load(file.path(analysis_dir, "nma_data.RData"))

# --- Fit NMA model ---
# Random-effects model with REML estimator for between-study heterogeneity
nma <- netmeta(
  TE = TE,
  seTE = seTE,
  treat1 = treat1,
  treat2 = treat2,
  studlab = studlab,
  data = pw_meta,
  sm = "RR",
  reference.group = "placebo",
  comb.fixed = FALSE,
  comb.random = TRUE,
  method.tau = "REML",
  tol.multiarm = 0.1
)

# --- Print NMA summary ---
cat("=== NMA Summary ===\n")
summary(nma)

# --- Key results vs placebo ---
cat("\n=== Treatment Effects vs Placebo (Random Effects) ===\n")
cat("Reference: placebo/no G-CSF\n\n")

# Extract results
res <- data.frame(
  treatment = nma$trts[nma$trts != "placebo"],
  RR = exp(nma$TE.random["placebo", nma$trts[nma$trts != "placebo"]]),
  lower = exp(nma$lower.random["placebo", nma$trts[nma$trts != "placebo"]]),
  upper = exp(nma$upper.random["placebo", nma$trts[nma$trts != "placebo"]]),
  pval = nma$pval.random["placebo", nma$trts[nma$trts != "placebo"]]
)

# Note: netmeta stores comparisons as treat2 vs treat1, so we need
# to invert (multiply by -1 on log scale) for "treatment vs placebo"
# when placebo is treat1
res <- data.frame(
  treatment = nma$trts[nma$trts != "placebo"],
  stringsAsFactors = FALSE
)

for (trt in res$treatment) {
  idx <- which(nma$trts == trt)
  ref_idx <- which(nma$trts == "placebo")
  res$RR[res$treatment == trt] <- exp(nma$TE.random[trt, "placebo"])
  res$lower[res$treatment == trt] <- exp(nma$lower.random[trt, "placebo"])
  res$upper[res$treatment == trt] <- exp(nma$upper.random[trt, "placebo"])
  res$pval[res$treatment == trt] <- nma$pval.random[trt, "placebo"]
}

print(res)

# --- Heterogeneity ---
cat("\n=== Heterogeneity ===\n")
cat("tau^2 =", nma$tau^2, "\n")
cat("tau =", nma$tau, "\n")
cat("I^2 =", round(nma$I2 * 100, 1), "%\n")

# --- League table ---
cat("\n=== League Table (Random Effects) ===\n")
league <- netleague(nma, random = TRUE, digits = 2)
print(league)

# --- Forest plot (all vs placebo) ---
png(
  file.path(analysis_dir, "figures", "forest_nma.png"),
  width = 10, height = 6, units = "in", res = 300
)
forest(
  nma,
  reference.group = "placebo",
  sortvar = TE,
  smlab = "RR vs Placebo\n(Random Effects NMA)",
  label.left = "Favours G-CSF",
  label.right = "Favours Placebo",
  drop.reference.group = TRUE
)
dev.off()
cat("Forest plot saved to figures/forest_nma.png\n")

# --- Save model object ---
save(nma, file = file.path(analysis_dir, "nma_model.RData"))
cat("NMA model saved to nma_model.RData\n")
