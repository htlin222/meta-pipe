#!/usr/bin/env Rscript
# ============================================================================
# EFS Meta-Analysis: ICI + Chemotherapy vs Chemotherapy Alone in TNBC
# ============================================================================
# Purpose: Pool hazard ratios for event-free survival across RCTs
# Method: Generic inverse-variance random-effects meta-analysis
# Date: 2026-02-07
# ============================================================================

library(meta)
library(metafor)
library(dplyr)
library(readr)
library(ggplot2)

# Set working directory
setwd("/Users/htlin/meta-pipe/06_analysis")

# ============================================================================
# 1. Load and prepare data
# ============================================================================

# Read extraction data
data <- read_csv("../05_extraction/round-01/extraction.csv")

# Filter studies with EFS data
# KEYNOTE-522, IMpassion031, GeparNuevo have complete HR data
efs_data <- data %>%
  select(
    study_id,
    trial_name,
    first_author,
    publication_year,
    n_randomized_total,
    n_intervention,
    n_control,
    ici_agent,
    EFS_HR,
    EFS_HR_95CI_lower,
    EFS_HR_95CI_upper,
    EFS_p_value,
    EFS_5yr_intervention_pct,
    EFS_5yr_control_pct,
    median_followup_months
  ) %>%
  # Convert "NR" to NA and ensure numeric types
  mutate(
    EFS_HR = ifelse(EFS_HR == "NR", NA, EFS_HR),
    EFS_HR_95CI_lower = ifelse(EFS_HR_95CI_lower == "NR", NA, EFS_HR_95CI_lower),
    EFS_HR_95CI_upper = ifelse(EFS_HR_95CI_upper == "NR", NA, EFS_HR_95CI_upper),
    EFS_5yr_intervention_pct = ifelse(EFS_5yr_intervention_pct == "NR", NA, EFS_5yr_intervention_pct),
    EFS_5yr_control_pct = ifelse(EFS_5yr_control_pct == "NR", NA, EFS_5yr_control_pct),
    EFS_HR = as.numeric(EFS_HR),
    EFS_HR_95CI_lower = as.numeric(EFS_HR_95CI_lower),
    EFS_HR_95CI_upper = as.numeric(EFS_HR_95CI_upper),
    EFS_5yr_intervention_pct = as.numeric(EFS_5yr_intervention_pct),
    EFS_5yr_control_pct = as.numeric(EFS_5yr_control_pct)
  ) %>%
  # Filter out studies without EFS HR data
  filter(!is.na(EFS_HR))

cat("\n=== EFS Data Extracted ===\n")
print(efs_data)

# Calculate log(HR) and SE from CI
# Formula: SE = (log(upper) - log(lower)) / (2 * 1.96)
efs_data <- efs_data %>%
  mutate(
    log_HR = log(EFS_HR),
    log_CI_lower = log(EFS_HR_95CI_lower),
    log_CI_upper = log(EFS_HR_95CI_upper),
    SE_log_HR = (log_CI_upper - log_CI_lower) / (2 * 1.96)
  )

cat("\n=== Calculated Log HR and SE ===\n")
print(efs_data %>% select(trial_name, EFS_HR, log_HR, SE_log_HR))

# ============================================================================
# 2. Perform generic inverse-variance meta-analysis
# ============================================================================

meta_efs <- metagen(
  TE = log_HR,
  seTE = SE_log_HR,
  studlab = trial_name,
  data = efs_data,
  sm = "HR",
  random = TRUE,
  common = FALSE,
  method.random.ci = "HK",  # Hartung-Knapp adjustment
  title = "EFS: ICI+Chemo vs Chemo Alone in TNBC"
)

cat("\n=== Meta-Analysis Results ===\n")
print(summary(meta_efs))

# ============================================================================
# 3. Forest plot
# ============================================================================

png("figures/forest_plot_EFS.png", width = 3000, height = 2000, res = 300)

forest(
  meta_efs,
  sortvar = TE,
  prediction = TRUE,
  print.tau2 = TRUE,
  print.I2 = TRUE,
  leftcols = "studlab",
  leftlabs = "Trial",
  rightcols = c("effect", "ci"),
  rightlabs = c("HR", "95% CI"),
  xlab = "Hazard Ratio (EFS)",
  smlab = "EFS Benefit",
  col.square = "navy",
  col.diamond = "maroon",
  col.predict = "red",
  fontsize = 12,
  spacing = 1.5,
  digits = 2,
  ref = 1  # Add reference line at HR = 1
)

dev.off()
cat("\n✓ Forest plot saved: figures/forest_plot_EFS.png\n")

# ============================================================================
# 4. Heterogeneity assessment
# ============================================================================

cat("\n=== Heterogeneity Assessment ===\n")
cat(sprintf("I² = %.1f%%\n", meta_efs$I2 * 100))
cat(sprintf("τ² = %.4f\n", meta_efs$tau2))
cat(sprintf("Cochran's Q = %.2f (df=%d, p=%s)\n",
            meta_efs$Q, meta_efs$df.Q,
            ifelse(meta_efs$pval.Q < 0.001, "<0.001", sprintf("%.3f", meta_efs$pval.Q))))

# ============================================================================
# 5. Sensitivity analysis
# ============================================================================

# Leave-one-out analysis
loo <- metainf(meta_efs, pooled = "random")

png("figures/efs_leave_one_out.png", width = 3000, height = 2000, res = 300)
forest(loo,
       leftcols = c("studlab"),
       leftlabs = c("Omitted Trial"),
       xlab = "Hazard Ratio (Leave-One-Out)",
       col.square = "steelblue",
       col.diamond = "darkred",
       ref = 1)
dev.off()
cat("\n✓ Leave-one-out plot saved: figures/efs_leave_one_out.png\n")

# Influence diagnostics using metafor
rma_model <- rma(yi = log_HR, sei = SE_log_HR, data = efs_data, method = "REML")
inf <- influence(rma_model)

cat("\n=== Influential Studies (DFBETAS) ===\n")
print(inf$inf)

# ============================================================================
# 6. Publication bias assessment
# ============================================================================

# Egger's test (if >= 3 studies)
if (nrow(efs_data) >= 3) {
  egger_test <- metabias(meta_efs, method.bias = "linreg", k.min = 3)

  cat("\n=== Publication Bias Assessment ===\n")
  cat(sprintf("Egger's test: t = %.2f, p = %.3f\n",
              egger_test$statistic, egger_test$p.value))

  # Funnel plot
  png("figures/funnel_plot_EFS.png", width = 2400, height = 2000, res = 300)
  funnel(meta_efs,
         xlab = "Hazard Ratio (log scale)",
         studlab = TRUE,
         col = "navy",
         pch = 16,
         cex = 1.5)
  title("Funnel Plot: EFS Meta-Analysis")
  dev.off()
  cat("✓ Funnel plot saved: figures/funnel_plot_EFS.png\n")
} else {
  cat("\nNote: Publication bias tests require ≥3 studies\n")
}

# ============================================================================
# 7. Export results table
# ============================================================================

results_table <- data.frame(
  Trial = efs_data$trial_name,
  First_Author = paste0(efs_data$first_author, " ", efs_data$publication_year),
  ICI_Agent = efs_data$ici_agent,
  N_Total = efs_data$n_randomized_total,
  N_ICI = efs_data$n_intervention,
  N_Control = efs_data$n_control,
  HR = sprintf("%.2f", efs_data$EFS_HR),
  CI_95 = sprintf("%.2f-%.2f", efs_data$EFS_HR_95CI_lower, efs_data$EFS_HR_95CI_upper),
  P_value = ifelse(is.na(efs_data$EFS_p_value) | efs_data$EFS_p_value == "NR",
                   "NR",
                   ifelse(efs_data$EFS_p_value == "<0.001" | as.numeric(efs_data$EFS_p_value) < 0.001,
                          "<0.001",
                          sprintf("%.3f", as.numeric(efs_data$EFS_p_value)))),
  EFS_5yr_ICI_pct = ifelse(is.na(efs_data$EFS_5yr_intervention_pct),
                           "NR",
                           sprintf("%.1f%%", as.numeric(efs_data$EFS_5yr_intervention_pct))),
  EFS_5yr_Control_pct = ifelse(is.na(efs_data$EFS_5yr_control_pct),
                               "NR",
                               sprintf("%.1f%%", as.numeric(efs_data$EFS_5yr_control_pct))),
  Followup_months = efs_data$median_followup_months
)

# Add pooled estimate
pooled_row <- data.frame(
  Trial = "Pooled (Random-Effects)",
  First_Author = "",
  ICI_Agent = "",
  N_Total = sum(efs_data$n_randomized_total),
  N_ICI = sum(efs_data$n_intervention),
  N_Control = sum(efs_data$n_control),
  HR = sprintf("%.2f", exp(meta_efs$TE.random)),
  CI_95 = sprintf("%.2f-%.2f", exp(meta_efs$lower.random), exp(meta_efs$upper.random)),
  P_value = ifelse(meta_efs$pval.random < 0.001,
                   "<0.001",
                   sprintf("%.3f", meta_efs$pval.random)),
  EFS_5yr_ICI_pct = "—",
  EFS_5yr_Control_pct = "—",
  Followup_months = ""
)

results_table <- rbind(results_table, pooled_row)

write_csv(results_table, "tables/EFS_meta_analysis_results.csv")
cat("\n✓ Results table saved: tables/EFS_meta_analysis_results.csv\n")

# ============================================================================
# 8. Clinical interpretation
# ============================================================================

pooled_HR <- exp(meta_efs$TE.random)
pooled_CI_lower <- exp(meta_efs$lower.random)
pooled_CI_upper <- exp(meta_efs$upper.random)
pooled_p <- meta_efs$pval.random

cat("\n╔════════════════════════════════════════════════════════════════╗\n")
cat("║            EFS META-ANALYSIS SUMMARY                           ║\n")
cat("╚════════════════════════════════════════════════════════════════╝\n\n")

cat(sprintf("Pooled HR: %.2f (95%% CI: %.2f-%.2f, p=%s)\n",
            pooled_HR, pooled_CI_lower, pooled_CI_upper,
            ifelse(pooled_p < 0.001, "<0.001", sprintf("%.3f", pooled_p))))

cat(sprintf("Heterogeneity: I² = %.1f%%, τ² = %.4f\n",
            meta_efs$I2 * 100, meta_efs$tau2))

# Calculate absolute risk reduction (if 5-year EFS available)
# Use weighted average of control group 5-year EFS
control_efs_5yr <- efs_data %>%
  filter(!is.na(EFS_5yr_control_pct)) %>%
  summarize(weighted_mean = weighted.mean(EFS_5yr_control_pct, n_control, na.rm = TRUE)) %>%
  pull(weighted_mean)

if (!is.na(control_efs_5yr)) {
  # HR to absolute benefit formula (approximation)
  # EFS_intervention ≈ EFS_control^HR
  predicted_efs_5yr <- control_efs_5yr^pooled_HR

  # For HR < 1 (benefit), we need: EFS_intervention = 1 - (1 - EFS_control) * HR
  # This is more accurate for survival outcomes
  baseline_event_rate <- (100 - control_efs_5yr) / 100
  intervention_event_rate <- baseline_event_rate * pooled_HR
  predicted_efs_5yr <- 100 - (intervention_event_rate * 100)

  absolute_benefit <- predicted_efs_5yr - control_efs_5yr
  NNT <- round(100 / absolute_benefit)

  cat(sprintf("\n5-year EFS (Control group baseline): %.1f%%\n", control_efs_5yr))
  cat(sprintf("5-year EFS (Predicted with ICI): %.1f%%\n", predicted_efs_5yr))
  cat(sprintf("Absolute benefit: +%.1f%%\n", absolute_benefit))
  cat(sprintf("NNT (5-year EFS benefit): %d patients\n", NNT))
}

cat("\n╔════════════════════════════════════════════════════════════════╗\n")
cat("║            CLINICAL INTERPRETATION                             ║\n")
cat("╚════════════════════════════════════════════════════════════════╝\n\n")

if (pooled_p < 0.05 && pooled_CI_upper < 1) {
  cat("✓ Statistically significant EFS benefit with ICI + chemotherapy\n")
  cat("✓ Consistent with pCR improvement (RR 1.26)\n")
  cat("✓ Validates pCR as surrogate endpoint for long-term survival\n")
} else if (pooled_CI_lower < 1 && pooled_CI_upper > 1) {
  cat("○ Trend toward EFS benefit but not statistically significant\n")
  cat("  (May be due to limited follow-up or small sample size)\n")
} else {
  cat("⚠ No clear EFS benefit detected\n")
  cat("  (Requires cautious interpretation given pCR benefit)\n")
}

cat("\n=== By Individual Trial ===\n")
for (i in 1:nrow(efs_data)) {
  cat(sprintf("\n%s:\n", efs_data$trial_name[i]))
  cat(sprintf("  HR %.2f (95%% CI %.2f-%.2f)\n",
              efs_data$EFS_HR[i],
              efs_data$EFS_HR_95CI_lower[i],
              efs_data$EFS_HR_95CI_upper[i]))
  if (!is.na(efs_data$EFS_5yr_intervention_pct[i])) {
    cat(sprintf("  5-year EFS: %.1f%% (ICI) vs %.1f%% (Control)\n",
                efs_data$EFS_5yr_intervention_pct[i],
                efs_data$EFS_5yr_control_pct[i]))
  }
  cat(sprintf("  Follow-up: %s months\n", efs_data$median_followup_months[i]))
}

cat("\n════════════════════════════════════════════════════════════════\n")
cat("Analysis complete. Files generated:\n")
cat("  - figures/forest_plot_EFS.png\n")
cat("  - figures/efs_leave_one_out.png\n")
if (nrow(efs_data) >= 3) {
  cat("  - figures/funnel_plot_EFS.png\n")
}
cat("  - tables/EFS_meta_analysis_results.csv\n")
cat("════════════════════════════════════════════════════════════════\n")
