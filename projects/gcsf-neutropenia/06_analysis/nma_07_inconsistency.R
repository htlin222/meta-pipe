#!/usr/bin/env Rscript
# =============================================================================
# NMA Step 07: Inconsistency Assessment (Node-Splitting)
# Project: G-CSF Prophylaxis in Chemotherapy-Induced Neutropenia
# =============================================================================

library(netmeta)
library(readr)

analysis_dir <- "projects/gcsf-neutropenia/06_analysis"
load(file.path(analysis_dir, "nma_model.RData"))

# --- Global inconsistency test (Q decomposition) ---
cat("=== Global Inconsistency Test ===\n")
cat("Q total:", round(nma$Q, 2), "\n")
cat("df:", nma$df.Q, "\n")
cat("p-value:", round(nma$pval.Q, 4), "\n\n")

cat("Q within-designs:", round(nma$Q.heterogeneity, 2), "\n")
cat("Q between-designs:", round(nma$Q.inconsistency, 2), "\n")
cat("p-value (inconsistency):", round(nma$pval.Q.inconsistency, 4), "\n\n")

# --- Node-splitting (local inconsistency) ---
cat("=== Node-Splitting Test ===\n")
ns <- netsplit(nma)
print(ns)

# --- Extract node-splitting results ---
ns_df <- data.frame(
  comparison = ns$comparison,
  k_direct = ns$k,
  RR_direct = round(exp(ns$direct.random$TE), 2),
  lower_direct = round(exp(ns$direct.random$lower), 2),
  upper_direct = round(exp(ns$direct.random$upper), 2),
  RR_indirect = round(exp(ns$indirect.random$TE), 2),
  lower_indirect = round(exp(ns$indirect.random$lower), 2),
  upper_indirect = round(exp(ns$indirect.random$upper), 2),
  RR_nma = round(exp(ns$random$TE), 2),
  lower_nma = round(exp(ns$random$lower), 2),
  upper_nma = round(exp(ns$random$upper), 2),
  p_interaction = round(ns$compare.random$p, 4),
  stringsAsFactors = FALSE
)

cat("\n=== Node-Splitting Results ===\n")
print(ns_df)

# --- Check for significant inconsistency ---
sig_incon <- ns_df[ns_df$p_interaction < 0.05, ]
if (nrow(sig_incon) > 0) {
  cat("\n*** WARNING: Significant inconsistency detected in:\n")
  print(sig_incon)
} else {
  cat("\nNo significant inconsistency detected (all p > 0.05)\n")
  cat("Direct and indirect evidence are consistent.\n")
}

# --- Save results ---
write_csv(ns_df, file.path(analysis_dir, "tables", "inconsistency_test.csv"))
cat("Inconsistency results saved to tables/inconsistency_test.csv\n")

# --- Net heat plot (if available) ---
tryCatch({
  png(
    file.path(analysis_dir, "figures", "netheat_plot.png"),
    width = 8, height = 8, units = "in", res = 300
  )
  netheat(nma)
  dev.off()
  cat("Net heat plot saved to figures/netheat_plot.png\n")
}, error = function(e) {
  cat("Net heat plot could not be generated:", e$message, "\n")
})
