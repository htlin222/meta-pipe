#!/usr/bin/env Rscript
# pCR Meta-Analysis for TNBC Neoadjuvant Immunotherapy
# Generated: 2026-02-07
# Data source: Web search extraction (Claude AI)

# Load required packages
library(meta)
library(metafor)
library(dplyr)
library(readr)
library(ggplot2)

# Set working directory to project root
setwd("/Users/htlin/meta-pipe")

# Create output directories
dir.create("06_analysis/figures", showWarnings = FALSE, recursive = TRUE)
dir.create("06_analysis/tables", showWarnings = FALSE, recursive = TRUE)

# ============================================================================
# 1. LOAD AND PREPARE DATA
# ============================================================================

cat("\n=== Loading extraction data ===\n")
data <- read_csv("05_extraction/round-01/extraction.csv",
                 show_col_types = FALSE)

# Display loaded data
cat("\nLoaded", nrow(data), "trials:\n")
print(data[, c("trial_name", "n_randomized_total", "pCR_rate_intervention_pct",
               "pCR_rate_control_pct")])

# ============================================================================
# 2. CALCULATE pCR EVENTS FROM PERCENTAGES (where missing)
# ============================================================================

cat("\n=== Calculating pCR events ===\n")

# Convert "NR" to NA and ensure numeric types
data <- data %>%
  mutate(
    pCR_intervention_n = ifelse(pCR_intervention_n == "NR", NA, pCR_intervention_n),
    pCR_control_n = ifelse(pCR_control_n == "NR", NA, pCR_control_n),
    pCR_intervention_n = as.numeric(pCR_intervention_n),
    pCR_control_n = as.numeric(pCR_control_n)
  )

# For GeparNuevo: calculate events from percentages
data <- data %>%
  mutate(
    pCR_intervention_n = ifelse(
      is.na(pCR_intervention_n) & !is.na(pCR_rate_intervention_pct),
      round(n_intervention * pCR_rate_intervention_pct / 100),
      pCR_intervention_n
    ),
    pCR_control_n = ifelse(
      is.na(pCR_control_n) & !is.na(pCR_rate_control_pct),
      round(n_control * pCR_rate_control_pct / 100),
      pCR_control_n
    )
  )

# Verify completeness
cat("\npCR data completeness:\n")
print(data %>%
  select(trial_name, pCR_intervention_n, n_intervention,
         pCR_control_n, n_control) %>%
  mutate(complete = !is.na(pCR_intervention_n) & !is.na(pCR_control_n)))

# ============================================================================
# 3. META-ANALYSIS: pCR RISK RATIO
# ============================================================================

cat("\n=== Performing pCR meta-analysis ===\n")

# Prepare data for meta-analysis
ma_data <- data %>%
  filter(!is.na(pCR_intervention_n) & !is.na(pCR_control_n)) %>%
  mutate(
    # Calculate non-events
    no_pCR_intervention = n_intervention - pCR_intervention_n,
    no_pCR_control = n_control - pCR_control_n
  )

cat("\nTrials included in meta-analysis:", nrow(ma_data), "\n")

# Perform random-effects meta-analysis (Risk Ratio)
meta_pcr <- metabin(
  event.e = pCR_intervention_n,
  n.e = n_intervention,
  event.c = pCR_control_n,
  n.c = n_control,
  studlab = trial_name,
  data = ma_data,
  sm = "RR",  # Risk Ratio
  method = "MH",  # Mantel-Haenszel
  random = TRUE,  # Random-effects model
  fixed = FALSE,
  hakn = TRUE,  # Hartung-Knapp adjustment
  title = "pCR: ICI+Chemo vs Chemo Alone in TNBC"
)

# Print results
cat("\n=== META-ANALYSIS RESULTS ===\n")
print(summary(meta_pcr))

# ============================================================================
# 4. FOREST PLOT
# ============================================================================

cat("\n=== Generating forest plot ===\n")

# Create high-quality forest plot
png("06_analysis/figures/forest_plot_pCR.png",
    width = 3000, height = 2000, res = 300)

forest(meta_pcr,
       sortvar = -TE,  # Sort by effect size
       prediction = TRUE,  # Add prediction interval
       print.tau2 = TRUE,
       print.I2 = TRUE,
       print.pval.Q = TRUE,
       col.diamond = "blue",
       col.diamond.lines = "blue",
       col.predict = "red",
       print.I2.ci = TRUE,
       digits = 2,
       smlab = "Risk Ratio (95% CI)",
       leftcols = c("studlab", "event.e", "n.e", "event.c", "n.c"),
       leftlabs = c("Trial", "Events\n(ICI)", "Total\n(ICI)",
                    "Events\n(Control)", "Total\n(Control)"),
       rightcols = c("effect", "ci", "w.random"),
       rightlabs = c("RR", "95% CI", "Weight"),
       xlab = "Favors Control    Favors ICI+Chemo",
       test.overall.random = TRUE,
       test.subgroup.random = FALSE,
       colgap.forest.left = "1cm",
       colgap.forest.right = "1cm"
)

dev.off()
cat("Forest plot saved to: 06_analysis/figures/forest_plot_pCR.png\n")

# ============================================================================
# 5. HETEROGENEITY ASSESSMENT
# ============================================================================

cat("\n=== HETEROGENEITY ASSESSMENT ===\n")

# Extract heterogeneity statistics
het_stats <- data.frame(
  Statistic = c("Cochran's Q", "df", "p-value (Q)",
                "I² (%)", "I² 95% CI", "τ²", "τ"),
  Value = c(
    round(meta_pcr$Q, 2),
    meta_pcr$df.Q,
    format.pval(meta_pcr$pval.Q, digits = 4),
    paste0(round(meta_pcr$I2 * 100, 1), "%"),
    paste0("[", round(meta_pcr$lower.I2 * 100, 1), "%, ",
           round(meta_pcr$upper.I2 * 100, 1), "%]"),
    round(meta_pcr$tau2, 4),
    round(meta_pcr$tau, 4)
  )
)

print(het_stats)

# Interpretation
cat("\n=== HETEROGENEITY INTERPRETATION ===\n")
i2_value <- meta_pcr$I2 * 100
if (i2_value < 25) {
  cat("Low heterogeneity (I² <25%): Trials are relatively homogeneous\n")
} else if (i2_value < 50) {
  cat("Moderate heterogeneity (I² 25-50%): Some variation between trials\n")
} else if (i2_value < 75) {
  cat("Substantial heterogeneity (I² 50-75%): Considerable variation\n")
} else {
  cat("High heterogeneity (I² >75%): Large variation between trials\n")
}

# ============================================================================
# 6. RESULTS TABLE
# ============================================================================

cat("\n=== Generating results table ===\n")

results_table <- data.frame(
  Trial = ma_data$trial_name,
  N_Total = ma_data$n_randomized_total,
  pCR_ICI = paste0(ma_data$pCR_intervention_n, "/", ma_data$n_intervention,
                   " (", round(ma_data$pCR_rate_intervention_pct, 1), "%)"),
  pCR_Control = paste0(ma_data$pCR_control_n, "/", ma_data$n_control,
                       " (", round(ma_data$pCR_rate_control_pct, 1), "%)"),
  RR = round(exp(meta_pcr$TE), 2),
  CI_95 = paste0("[", round(exp(meta_pcr$lower), 2), ", ",
                 round(exp(meta_pcr$upper), 2), "]"),
  Weight = paste0(round(meta_pcr$w.random, 1), "%"),
  P_value = ifelse(ma_data$pCR_p_value == "<0.001", "<0.001",
                   format.pval(as.numeric(gsub("<", "", ma_data$pCR_p_value)),
                              digits = 4))
)

# Add pooled estimate row
pooled_row <- data.frame(
  Trial = "POOLED (Random-effects)",
  N_Total = sum(ma_data$n_randomized_total),
  pCR_ICI = paste0(sum(ma_data$pCR_intervention_n), "/",
                   sum(ma_data$n_intervention)),
  pCR_Control = paste0(sum(ma_data$pCR_control_n), "/",
                       sum(ma_data$n_control)),
  RR = round(exp(meta_pcr$TE.random), 2),
  CI_95 = paste0("[", round(exp(meta_pcr$lower.random), 2), ", ",
                 round(exp(meta_pcr$upper.random), 2), "]"),
  Weight = "100.0%",
  P_value = format.pval(meta_pcr$pval.random, digits = 4)
)

results_table <- rbind(results_table, pooled_row)

cat("\n=== RESULTS TABLE ===\n")
print(results_table)

# Save to CSV
write_csv(results_table, "06_analysis/tables/pCR_meta_analysis_results.csv")
cat("\nResults table saved to: 06_analysis/tables/pCR_meta_analysis_results.csv\n")

# ============================================================================
# 7. SENSITIVITY ANALYSIS
# ============================================================================

cat("\n=== SENSITIVITY ANALYSES ===\n")

# 7.1 Exclude Phase II trial (GeparNuevo)
cat("\n--- Excluding Phase II trial (GeparNuevo) ---\n")
ma_phase3_only <- ma_data %>% filter(study_design == "RCT_phase3")

if (nrow(ma_phase3_only) >= 2) {
  meta_phase3 <- metabin(
    event.e = pCR_intervention_n,
    n.e = n_intervention,
    event.c = pCR_control_n,
    n.c = n_control,
    studlab = trial_name,
    data = ma_phase3_only,
    sm = "RR",
    method = "MH",
    random = TRUE,
    fixed = FALSE,
    hakn = TRUE
  )
  cat("Pooled RR (Phase III only):", round(exp(meta_phase3$TE.random), 2),
      "  95% CI:", round(exp(meta_phase3$lower.random), 2), "-",
      round(exp(meta_phase3$upper.random), 2), "\n")
  cat("I² =", round(meta_phase3$I2 * 100, 1), "%\n")
}

# 7.2 Exclude negative trial (NeoTRIPaPDL1)
cat("\n--- Excluding negative trial (NeoTRIPaPDL1) ---\n")
ma_positive_only <- ma_data %>% filter(trial_name != "NeoTRIPaPDL1")

if (nrow(ma_positive_only) >= 2) {
  meta_positive <- metabin(
    event.e = pCR_intervention_n,
    n.e = n_intervention,
    event.c = pCR_control_n,
    n.c = n_control,
    studlab = trial_name,
    data = ma_positive_only,
    sm = "RR",
    method = "MH",
    random = TRUE,
    fixed = FALSE,
    hakn = TRUE
  )
  cat("Pooled RR (excl. negative trial):", round(exp(meta_positive$TE.random), 2),
      "  95% CI:", round(exp(meta_positive$lower.random), 2), "-",
      round(exp(meta_positive$upper.random), 2), "\n")
  cat("I² =", round(meta_positive$I2 * 100, 1), "%\n")
}

# ============================================================================
# 8. PUBLICATION BIAS
# ============================================================================

cat("\n=== PUBLICATION BIAS ASSESSMENT ===\n")

# Funnel plot
png("06_analysis/figures/funnel_plot_pCR.png",
    width = 2400, height = 2000, res = 300)
funnel(meta_pcr,
       xlab = "Risk Ratio (log scale)",
       studlab = TRUE,
       contour = c(0.95, 0.99),
       col.contour = c("gray75", "gray90"))
legend("topright",
       legend = c("p < 0.05", "p < 0.01"),
       fill = c("gray75", "gray90"))
dev.off()
cat("\nFunnel plot saved to: 06_analysis/figures/funnel_plot_pCR.png\n")

# Egger's test (if ≥3 studies)
if (nrow(ma_data) >= 3) {
  egger_test <- metabias(meta_pcr, method.bias = "linreg", k.min = 3)
  cat("\nEgger's test for funnel plot asymmetry:\n")
  cat("  Intercept:", round(egger_test$estimate[1], 4), "\n")
  cat("  p-value:", format.pval(egger_test$pval, digits = 4), "\n")
  if (egger_test$pval < 0.05) {
    cat("  WARNING: Significant asymmetry detected (possible publication bias)\n")
  } else {
    cat("  No significant asymmetry detected\n")
  }
}

# ============================================================================
# 9. SUMMARY FOR MANUSCRIPT
# ============================================================================

cat("\n" , paste(rep("=", 70), collapse = ""), "\n")
cat("=== SUMMARY FOR MANUSCRIPT ===\n")
cat(paste(rep("=", 70), collapse = ""), "\n\n")

cat("METHODS:\n")
cat("We performed a random-effects meta-analysis using the Mantel-Haenszel\n")
cat("method with Hartung-Knapp adjustment. Risk ratios (RR) and 95% confidence\n")
cat("intervals were calculated for pathologic complete response (pCR).\n")
cat("Heterogeneity was assessed using Cochran's Q test and I² statistic.\n\n")

cat("RESULTS:\n")
cat(sprintf("Five trials (N=%d) reported pCR outcomes. The pooled risk ratio for\n",
            sum(ma_data$n_randomized_total)))
cat(sprintf("pCR was %.2f (95%% CI %.2f-%.2f, p%s), favoring ICI plus chemotherapy.\n",
            exp(meta_pcr$TE.random),
            exp(meta_pcr$lower.random),
            exp(meta_pcr$upper.random),
            ifelse(meta_pcr$pval.random < 0.001, "<0.001",
                   paste0("=", format.pval(meta_pcr$pval.random, digits = 3)))))
cat(sprintf("Heterogeneity was %s (I² = %.1f%%, 95%% CI %.1f%%-%.1f%%, p%s).\n",
            ifelse(i2_value < 50, "moderate", "substantial"),
            meta_pcr$I2 * 100,
            meta_pcr$lower.I2 * 100,
            meta_pcr$upper.I2 * 100,
            ifelse(meta_pcr$pval.Q < 0.001, "<0.001",
                   paste0("=", format.pval(meta_pcr$pval.Q, digits = 3)))))

cat("\nABSOLUTE BENEFIT:\n")
pooled_pCR_ICI <- sum(ma_data$pCR_intervention_n) / sum(ma_data$n_intervention) * 100
pooled_pCR_Control <- sum(ma_data$pCR_control_n) / sum(ma_data$n_control) * 100
absolute_diff <- pooled_pCR_ICI - pooled_pCR_Control
cat(sprintf("Pooled pCR rates: %.1f%% (ICI+Chemo) vs %.1f%% (Chemo alone)\n",
            pooled_pCR_ICI, pooled_pCR_Control))
cat(sprintf("Absolute difference: +%.1f%% (95%% CI calculated from RR)\n", absolute_diff))
cat(sprintf("Number Needed to Treat (NNT): %.0f patients\n", 100 / absolute_diff))

cat("\n" , paste(rep("=", 70), collapse = ""), "\n")
cat("Analysis complete! Check:\n")
cat("  - 06_analysis/figures/forest_plot_pCR.png\n")
cat("  - 06_analysis/figures/funnel_plot_pCR.png\n")
cat("  - 06_analysis/tables/pCR_meta_analysis_results.csv\n")
cat(paste(rep("=", 70), collapse = ""), "\n\n")
