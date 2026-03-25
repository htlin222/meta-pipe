# =============================================================================
# nma_09_sensitivity.R — Sensitivity Analyses + Leave-One-Out
# =============================================================================

source("nma_04_models.R")

# =============================================================================
# A: LEAVE-ONE-OUT
# =============================================================================

cat("=== Leave-One-Out Analysis ===\n")
studies <- unique(nma_data$studlab)
loo_results <- list()

for (s in studies) {
  data_loo <- nma_data[nma_data$studlab != s, ]
  nc_loo <- tryCatch(
    netconnection(data_loo$treat1, data_loo$treat2, data_loo$studlab),
    error = function(e) NULL)

  if (is.null(nc_loo) || nc_loo$n.subnets > 1) {
    cat("Excluding", s, "disconnects network — skipping\n")
    next
  }

  net_loo <- tryCatch(
    netmeta(TE, seTE, treat1, treat2, studlab, data = data_loo,
            sm = "HR", random = TRUE, method.tau = "REML",
            reference.group = "RCHOP"),
    error = function(e) NULL)

  if (!is.null(net_loo)) {
    loo_results[[s]] <- list(
      excluded = s,
      tau2     = net_loo$tau2,
      I2       = net_loo$I2
    )
  }
}

loo_df <- do.call(rbind, lapply(loo_results, function(x) {
  data.frame(Excluded = x$excluded,
             tau2 = round(x$tau2, 4),
             I2_pct = round(x$I2 * 100, 1))
}))

cat("\nFull model tau²:", round(net_re$tau2, 4), "\n")
cat("Full model I²:", round(net_re$I2 * 100, 1), "%\n\n")
print(loo_df)
write_csv(loo_df, file.path(TBL_DIR, "nma_leave_one_out.csv"))

# =============================================================================
# B: SENSITIVITY — EXCLUDE ROBUST (ABC-only population)
# =============================================================================

cat("\n=== Sensitivity: Exclude ROBUST (ABC-only) ===\n")
data_no_robust <- nma_data %>% filter(studlab != "ROBUST")

net_no_robust <- netmeta(TE, seTE, treat1, treat2, studlab,
                         data = data_no_robust, sm = "HR",
                         random = TRUE, method.tau = "REML",
                         reference.group = "RCHOP")

cat("Without ROBUST:\n")
summary(net_no_robust)

# =============================================================================
# C: OS NMA (SECONDARY OUTCOME)
# =============================================================================

cat("\n=== OS NMA (Secondary) ===\n")
if (nrow(nma_os) >= 3) {
  net_os <- netmeta(TE, seTE, treat1, treat2, studlab,
                    data = nma_os, sm = "HR",
                    random = TRUE, method.tau = "REML",
                    reference.group = "RCHOP")
  cat("OS NMA:\n")
  summary(net_os)

  png(file.path(FIG_DIR, "nma_forest_os.png"),
      width = 12, height = 8, units = "in", res = FIG_DPI)
  forest(net_os, reference.group = "RCHOP", sortvar = TE,
         smlab = "HR for OS\n(vs R-CHOP)",
         drop.reference.group = TRUE,
         label.left = "Favours treatment",
         label.right = "Favours R-CHOP")
  dev.off()
} else {
  cat("Insufficient OS data for NMA (need ≥3 trials with HR + CI).\n")
}

# =============================================================================
# D: FUNNEL PLOT
# =============================================================================

cat("\n=== Comparison-Adjusted Funnel Plot ===\n")
png(file.path(FIG_DIR, "nma_funnel.png"),
    width = 10, height = 8, units = "in", res = FIG_DPI)
tryCatch({
  funnel(net_re, pch = 16, col = "steelblue", legend = TRUE)
}, error = function(e) {
  cat("Funnel plot error:", e$message, "\n")
  plot.new()
  text(0.5, 0.5, "Funnel plot: insufficient data points\nfor comparison-adjusted funnel")
})
dev.off()

# =============================================================================
# E: CINeMA TEMPLATE
# =============================================================================

cinema_treatments <- sort(unique(c(nma_data$treat1, nma_data$treat2)))
cinema_template <- expand.grid(
  treat1 = cinema_treatments,
  treat2 = cinema_treatments,
  stringsAsFactors = FALSE
) %>%
  filter(treat1 < treat2) %>%
  mutate(within_study_bias = NA, across_study_bias = NA,
         indirectness = NA, imprecision = NA,
         heterogeneity = NA, incoherence = NA,
         overall_certainty = NA)

write_csv(cinema_template, file.path(TBL_DIR, "cinema_template.csv"))

# =============================================================================
# F: REPORT
# =============================================================================

sink("nma_sensitivity_report.txt")
cat("=== Sensitivity Analysis Report ===\n\n")
cat("Leave-One-Out:\n")
if (nrow(loo_df) > 0) print(loo_df)
cat("\nExclude ROBUST (ABC-only):\n")
summary(net_no_robust)
cat("\nOS NMA:\n")
if (exists("net_os")) summary(net_os) else cat("Insufficient data.\n")
sink()
cat("Sensitivity report saved.\n")
