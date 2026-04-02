# =============================================================================
# nma_05_inconsistency.R — Transitivity & Consistency Assessment
# =============================================================================
# Purpose: Assess NMA assumptions via design decomposition, heat plot,
#          and node-splitting
# Input: net_re from nma_04_models.R
# Output: figures/netheat.png, inconsistency test results
# =============================================================================

source("nma_04_models.R")

# --- 1. Global inconsistency test (Q decomposition) ---
cat("=== Design Decomposition (Consistency Assessment) ===\n")
dd <- decomp.design(net_re)
print(dd)

cat("\nQ_total:", dd$Q.decomp$Q[1], "(p =", dd$Q.decomp$pval[1], ")\n")
cat("Q_between-designs:", dd$Q.decomp$Q[2], "(p =", dd$Q.decomp$pval[2], ")\n")
cat("Q_within-designs:", dd$Q.decomp$Q[3], "(p =", dd$Q.decomp$pval[3], ")\n")

if (dd$Q.decomp$pval[2] < 0.05) {
  warning("Significant between-designs inconsistency detected (p < 0.05).")
  cat("Consider investigating sources of inconsistency.\n")
} else {
  cat("No significant between-designs inconsistency detected.\n")
}

# NOTE (Brignardello-Petersen et al. 2018): Global inconsistency tests
# (design decomposition, Lu-Ades model) are frequently underpowered.
# A non-significant p-value does NOT confirm coherence across all comparisons.
# Always interpret the node-splitting (local) results below as the primary
# evidence for incoherence assessment per comparison.
# See: ma-network-meta-analysis/references/nma-grade-certainty-workflow.md

# --- 2. Net heat plot ---
cat("\nGenerating net heat plot...\n")
png(file.path(FIG_DIR, "netheat.png"),
    width = FIG_WIDTH, height = FIG_HEIGHT, units = "in", res = FIG_DPI)

netheat(net_re, random = TRUE)

dev.off()
cat("Net heat plot saved to", file.path(FIG_DIR, "netheat.png"), "\n")

# --- 3. Node-splitting (direct vs indirect evidence) ---
cat("\n=== Node-Splitting (Local Inconsistency) ===\n")
ns <- netsplit(net_re)
print(ns)

# Identify comparisons with significant inconsistency
cat("\n--- Comparisons with significant inconsistency (p < 0.10) ---\n")
ns_df <- as.data.frame(ns)
if ("p.value" %in% names(ns_df)) {
  sig_inconsistency <- ns_df[ns_df$p.value < 0.10, ]
  if (nrow(sig_inconsistency) > 0) {
    print(sig_inconsistency)
  } else {
    cat("No comparisons with significant local inconsistency.\n")
  }
}

# --- 4. Forest plot of node-splitting results ---
png(file.path(FIG_DIR, "netsplit_forest.png"),
    width = 12, height = max(8, nrow(ns_df) * 0.5), units = "in", res = FIG_DPI)

forest(ns)

dev.off()
cat("Node-splitting forest plot saved to", file.path(FIG_DIR, "netsplit_forest.png"), "\n")

# --- 5. Save inconsistency report ---
sink("nma_inconsistency_report.txt")
cat("=== NMA Inconsistency Assessment ===\n\n")
cat("--- Design Decomposition ---\n")
print(dd)
cat("\n--- Node-Splitting ---\n")
print(ns)
sink()
cat("\nInconsistency report saved to nma_inconsistency_report.txt\n")
