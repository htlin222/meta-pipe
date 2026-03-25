# =============================================================================
# nma_05_inconsistency.R — Consistency Assessment
# =============================================================================
# Note: Star-shaped network (all vs R-CHOP) has NO closed loops for most
# comparisons, so inconsistency testing is limited. Only Lena-R-CHOP has
# 2 studies (ROBUST + ECOG-E1412) but both compare to R-CHOP directly.
# =============================================================================

source("nma_04_models.R")

# --- 1. Global inconsistency (Q decomposition) ---
cat("=== Design Decomposition ===\n")
dd <- decomp.design(net_re)
print(dd)

cat("\nQ_total:", dd$Q.decomp$Q[1], "(p =", dd$Q.decomp$pval[1], ")\n")
cat("Q_between:", dd$Q.decomp$Q[2], "(p =", dd$Q.decomp$pval[2], ")\n")

# --- 2. Net heat plot ---
png(file.path(FIG_DIR, "netheat.png"),
    width = 10, height = 8, units = "in", res = FIG_DPI)
tryCatch(netheat(net_re, random = TRUE), error = function(e) {
  cat("Net heat plot not available (star network):", e$message, "\n")
  plot.new()
  text(0.5, 0.5, "Net heat plot not applicable\n(star-shaped network)")
})
dev.off()

# --- 3. Node-splitting ---
cat("\n=== Node-Splitting ===\n")
cat("Note: Star-shaped network has limited node-splitting applicability.\n")
cat("Only comparisons with both direct and indirect evidence can be split.\n\n")

tryCatch({
  ns <- netsplit(net_re)
  print(ns)

  png(file.path(FIG_DIR, "netsplit_forest.png"),
      width = 12, height = 10, units = "in", res = FIG_DPI)
  forest(ns)
  dev.off()
}, error = function(e) {
  cat("Node-splitting not applicable:", e$message, "\n")
})

# --- 4. Report ---
sink("nma_inconsistency_report.txt")
cat("=== NMA Inconsistency Assessment ===\n")
cat("Network: Star-shaped (all treatments vs R-CHOP)\n")
cat("Closed loops: Limited (only Lena-R-CHOP has 2 studies)\n\n")
cat("Design decomposition:\n")
print(dd)
cat("\nConclusion: Inconsistency testing has limited power in star networks.\n")
cat("Transitivity assessment is the primary validity check.\n")
sink()
cat("Inconsistency report saved.\n")
