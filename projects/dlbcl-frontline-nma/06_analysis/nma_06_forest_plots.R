# =============================================================================
# nma_06_forest_plots.R — Forest Plots for DLBCL NMA
# =============================================================================

source("nma_04_models.R")

# --- 1. Main forest plot: all treatments vs R-CHOP ---
cat("Generating forest plots...\n")

png(file.path(FIG_DIR, "nma_forest_vs_RCHOP.png"),
    width = 12, height = 8, units = "in", res = FIG_DPI)

forest(net_re,
       reference.group = "RCHOP",
       sortvar = TE,
       smlab = "HR for PFS\n(vs R-CHOP)",
       drop.reference.group = TRUE,
       label.left = "Favours treatment",
       label.right = "Favours R-CHOP",
       xlim = c(0.5, 1.5))

dev.off()
cat("Main forest plot saved.\n")

# --- 2. Fixed vs random comparison ---
png(file.path(FIG_DIR, "nma_forest_fixed_vs_random.png"),
    width = 14, height = 8, units = "in", res = FIG_DPI)

net_both <- netmeta(TE, seTE, treat1, treat2, studlab,
                    data = nma_data, sm = "HR",
                    random = TRUE, fixed = TRUE,
                    method.tau = "REML",
                    reference.group = "RCHOP")

forest(net_both,
       reference.group = "RCHOP",
       sortvar = TE,
       drop.reference.group = TRUE,
       xlim = c(0.4, 1.6))

dev.off()
cat("Fixed vs random forest plot saved.\n")

# --- 3. Bayesian forest plot ---
# Extract posterior medians and CrIs for forest plot
cat("\nBayesian posterior estimates (HR scale):\n")
bayes_summary <- summary(bayes_re)
print(bayes_summary)

cat("\nAll forest plots generated.\n")
