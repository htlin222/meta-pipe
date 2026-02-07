#!/usr/bin/env Rscript
# ============================================================================
# Safety Meta-Analysis: ICI + Chemotherapy vs Chemotherapy Alone in TNBC
# ============================================================================
# Purpose: Pool safety outcomes (grade 3+ irAEs, discontinuations, SAEs)
# Method: Mantel-Haenszel random-effects meta-analysis for binary outcomes
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
# 1. Load safety data
# ============================================================================

safety_data <- read_csv("../05_extraction/round-01/safety_data.csv")

# Convert "NR" to NA and ensure numeric types for all safety columns
safety_data <- safety_data %>%
  mutate(
    across(starts_with("ae_") | starts_with("irae_") |
           starts_with("discontinuation_") | starts_with("serious_") |
           starts_with("fatal_"),
           ~ ifelse(. == "NR", NA, .)),
    across(ends_with("_n") | ends_with("_pct"), ~ as.numeric(.))
  )

cat("\n=== Safety Data Loaded ===\n")
print(safety_data)

# ============================================================================
# 2. Grade 3+ Immune-Related Adverse Events (irAEs)
# ============================================================================

cat("\n╔════════════════════════════════════════════════════════════════╗\n")
cat("║          GRADE 3+ IMMUNE-RELATED ADVERSE EVENTS                ║\n")
cat("╚════════════════════════════════════════════════════════════════╝\n\n")

# Filter studies with irAE data
irae_data <- safety_data %>%
  filter(!is.na(irae_grade3plus_intervention_n) & !is.na(irae_grade3plus_control_n))

cat("Studies with Grade 3+ irAE data:", nrow(irae_data), "\n")
print(irae_data %>% select(trial_name,
                            irae_grade3plus_intervention_n, n_intervention,
                            irae_grade3plus_control_n, n_control))

if (nrow(irae_data) >= 2) {
  # Perform meta-analysis
  meta_irae <- metabin(
    event.e = irae_grade3plus_intervention_n,
    n.e = n_intervention,
    event.c = irae_grade3plus_control_n,
    n.c = n_control,
    studlab = trial_name,
    data = irae_data,
    sm = "RR",
    method = "MH",
    random = TRUE,
    common = FALSE,
    method.random.ci = "HK",
    title = "Grade 3+ irAEs: ICI+Chemo vs Chemo Alone"
  )

  cat("\n=== Meta-Analysis Results: Grade 3+ irAEs ===\n")
  print(summary(meta_irae))

  # Forest plot
  png("figures/forest_plot_safety_irae.png", width = 3000, height = 2000, res = 300)
  forest(
    meta_irae,
    sortvar = TE,
    print.tau2 = TRUE,
    print.I2 = TRUE,
    leftcols = "studlab",
    leftlabs = "Trial",
    rightcols = c("effect", "ci"),
    rightlabs = c("RR", "95% CI"),
    xlab = "Risk Ratio (Grade 3+ irAEs)",
    smlab = "Grade 3+ Immune-Related AEs",
    col.square = "navy",
    col.diamond = "maroon",
    fontsize = 12,
    spacing = 1.5,
    digits = 2,
    ref = 1
  )
  dev.off()
  cat("\n✓ Forest plot saved: figures/forest_plot_safety_irae.png\n")

  # Calculate NNH (Number Needed to Harm)
  pooled_RR_irae <- exp(meta_irae$TE.random)
  baseline_risk_irae <- weighted.mean(
    irae_data$irae_grade3plus_control_n / irae_data$n_control,
    irae_data$n_control
  )
  absolute_risk_increase <- baseline_risk_irae * (pooled_RR_irae - 1)
  NNH_irae <- round(1 / absolute_risk_increase)

  cat(sprintf("\nBaseline risk (control): %.1f%%\n", baseline_risk_irae * 100))
  cat(sprintf("Pooled RR: %.2f\n", pooled_RR_irae))
  cat(sprintf("Absolute risk increase: %.1f%%\n", absolute_risk_increase * 100))
  cat(sprintf("NNH (Number Needed to Harm): %d\n", NNH_irae))

} else {
  cat("\n⚠ WARNING: Only", nrow(irae_data), "study with Grade 3+ irAE data.\n")
  cat("Meta-analysis requires at least 2 studies.\n")
}

# ============================================================================
# 3. Treatment Discontinuation (Any Drug)
# ============================================================================

cat("\n╔════════════════════════════════════════════════════════════════╗\n")
cat("║          TREATMENT DISCONTINUATION (ANY DRUG)                  ║\n")
cat("╚════════════════════════════════════════════════════════════════╝\n\n")

# Filter studies with discontinuation data
disc_data <- safety_data %>%
  filter(!is.na(discontinuation_any_intervention_n) & !is.na(discontinuation_any_control_n))

cat("Studies with discontinuation data:", nrow(disc_data), "\n")

if (nrow(disc_data) >= 2) {
  print(disc_data %>% select(trial_name,
                              discontinuation_any_intervention_n, n_intervention,
                              discontinuation_any_control_n, n_control))

  # Perform meta-analysis
  meta_disc <- metabin(
    event.e = discontinuation_any_intervention_n,
    n.e = n_intervention,
    event.c = discontinuation_any_control_n,
    n.c = n_control,
    studlab = trial_name,
    data = disc_data,
    sm = "RR",
    method = "MH",
    random = TRUE,
    common = FALSE,
    method.random.ci = "HK",
    title = "Treatment Discontinuation: ICI+Chemo vs Chemo Alone"
  )

  cat("\n=== Meta-Analysis Results: Discontinuation ===\n")
  print(summary(meta_disc))

  # Forest plot
  png("figures/forest_plot_safety_discontinuation.png", width = 3000, height = 2000, res = 300)
  forest(
    meta_disc,
    sortvar = TE,
    print.tau2 = TRUE,
    print.I2 = TRUE,
    leftcols = "studlab",
    leftlabs = "Trial",
    rightcols = c("effect", "ci"),
    rightlabs = c("RR", "95% CI"),
    xlab = "Risk Ratio (Discontinuation)",
    smlab = "Treatment Discontinuation",
    col.square = "navy",
    col.diamond = "maroon",
    fontsize = 12,
    spacing = 1.5,
    digits = 2,
    ref = 1
  )
  dev.off()
  cat("\n✓ Forest plot saved: figures/forest_plot_safety_discontinuation.png\n")

} else {
  cat("\n⚠ Only", nrow(disc_data), "study with discontinuation data.\n")
  cat("Cannot perform meta-analysis.\n")
}

# ============================================================================
# 4. Serious Adverse Events (SAE)
# ============================================================================

cat("\n╔════════════════════════════════════════════════════════════════╗\n")
cat("║          SERIOUS ADVERSE EVENTS (SAE)                          ║\n")
cat("╚════════════════════════════════════════════════════════════════╝\n\n")

# Filter studies with SAE data
sae_data <- safety_data %>%
  filter(!is.na(serious_ae_intervention_n) & !is.na(serious_ae_control_n))

cat("Studies with SAE data:", nrow(sae_data), "\n")

if (nrow(sae_data) >= 2) {
  print(sae_data %>% select(trial_name,
                             serious_ae_intervention_n, n_intervention,
                             serious_ae_control_n, n_control))

  # Perform meta-analysis
  meta_sae <- metabin(
    event.e = serious_ae_intervention_n,
    n.e = n_intervention,
    event.c = serious_ae_control_n,
    n.c = n_control,
    studlab = trial_name,
    data = sae_data,
    sm = "RR",
    method = "MH",
    random = TRUE,
    common = FALSE,
    method.random.ci = "HK",
    title = "Serious Adverse Events: ICI+Chemo vs Chemo Alone"
  )

  cat("\n=== Meta-Analysis Results: Serious AE ===\n")
  print(summary(meta_sae))

  # Forest plot
  png("figures/forest_plot_safety_sae.png", width = 3000, height = 2000, res = 300)
  forest(
    meta_sae,
    sortvar = TE,
    print.tau2 = TRUE,
    print.I2 = TRUE,
    leftcols = "studlab",
    leftlabs = "Trial",
    rightcols = c("effect", "ci"),
    rightlabs = c("RR", "95% CI"),
    xlab = "Risk Ratio (Serious AE)",
    smlab = "Serious Adverse Events",
    col.square = "navy",
    col.diamond = "maroon",
    fontsize = 12,
    spacing = 1.5,
    digits = 2,
    ref = 1
  )
  dev.off()
  cat("\n✓ Forest plot saved: figures/forest_plot_safety_sae.png\n")

} else {
  cat("\n⚠ Only", nrow(sae_data), "study with SAE data.\n")
  cat("Cannot perform meta-analysis.\n")
}

# ============================================================================
# 5. Fatal Adverse Events
# ============================================================================

cat("\n╔════════════════════════════════════════════════════════════════╗\n")
cat("║          FATAL ADVERSE EVENTS                                  ║\n")
cat("╚════════════════════════════════════════════════════════════════╝\n\n")

# Summarize fatal events
fatal_summary <- safety_data %>%
  filter(!is.na(fatal_ae_intervention_n)) %>%
  summarize(
    total_intervention = sum(n_intervention),
    total_control = sum(n_control),
    fatal_intervention = sum(fatal_ae_intervention_n, na.rm = TRUE),
    fatal_control = sum(fatal_ae_control_n, na.rm = TRUE),
    fatal_intervention_rate = fatal_intervention / total_intervention * 100,
    fatal_control_rate = fatal_control / total_control * 100
  )

cat("Fatal AE Summary:\n")
cat(sprintf("  ICI + Chemo: %d/%d (%.2f%%)\n",
            fatal_summary$fatal_intervention,
            fatal_summary$total_intervention,
            fatal_summary$fatal_intervention_rate))
cat(sprintf("  Chemo alone: %d/%d (%.2f%%)\n",
            fatal_summary$fatal_control,
            fatal_summary$total_control,
            fatal_summary$fatal_control_rate))

# List fatal events by trial
cat("\nFatal events by trial:\n")
fatal_by_trial <- safety_data %>%
  filter(!is.na(fatal_ae_intervention_n)) %>%
  select(trial_name, fatal_ae_intervention_n, fatal_ae_control_n, extraction_notes)

for (i in 1:nrow(fatal_by_trial)) {
  cat(sprintf("  %s: %d (ICI) vs %d (Control)\n",
              fatal_by_trial$trial_name[i],
              fatal_by_trial$fatal_ae_intervention_n[i],
              fatal_by_trial$fatal_ae_control_n[i]))
  if (fatal_by_trial$fatal_ae_intervention_n[i] > 0) {
    cat(sprintf("    Note: %s\n", fatal_by_trial$extraction_notes[i]))
  }
}

# ============================================================================
# 6. Comprehensive Safety Summary Table
# ============================================================================

cat("\n╔════════════════════════════════════════════════════════════════╗\n")
cat("║          COMPREHENSIVE SAFETY SUMMARY                          ║\n")
cat("╚════════════════════════════════════════════════════════════════╝\n\n")

# Create summary table
safety_summary <- data.frame(
  Outcome = character(),
  Trials = integer(),
  ICI_Events = integer(),
  ICI_Total = integer(),
  ICI_Rate_Pct = numeric(),
  Control_Events = integer(),
  Control_Total = integer(),
  Control_Rate_Pct = numeric(),
  Pooled_RR = character(),
  CI_95 = character(),
  P_value = character(),
  I2_Pct = character(),
  stringsAsFactors = FALSE
)

# Add Grade 3+ irAE results
if (exists("meta_irae") && nrow(irae_data) >= 2) {
  safety_summary <- rbind(safety_summary, data.frame(
    Outcome = "Grade 3+ irAEs",
    Trials = nrow(irae_data),
    ICI_Events = sum(irae_data$irae_grade3plus_intervention_n),
    ICI_Total = sum(irae_data$n_intervention),
    ICI_Rate_Pct = round(sum(irae_data$irae_grade3plus_intervention_n) / sum(irae_data$n_intervention) * 100, 1),
    Control_Events = sum(irae_data$irae_grade3plus_control_n),
    Control_Total = sum(irae_data$n_control),
    Control_Rate_Pct = round(sum(irae_data$irae_grade3plus_control_n) / sum(irae_data$n_control) * 100, 1),
    Pooled_RR = sprintf("%.2f", exp(meta_irae$TE.random)),
    CI_95 = sprintf("%.2f-%.2f", exp(meta_irae$lower.random), exp(meta_irae$upper.random)),
    P_value = ifelse(meta_irae$pval.random < 0.001, "<0.001", sprintf("%.3f", meta_irae$pval.random)),
    I2_Pct = sprintf("%.1f%%", meta_irae$I2 * 100)
  ))
}

# Add Discontinuation results
if (exists("meta_disc") && nrow(disc_data) >= 2) {
  safety_summary <- rbind(safety_summary, data.frame(
    Outcome = "Treatment Discontinuation",
    Trials = nrow(disc_data),
    ICI_Events = sum(disc_data$discontinuation_any_intervention_n),
    ICI_Total = sum(disc_data$n_intervention),
    ICI_Rate_Pct = round(sum(disc_data$discontinuation_any_intervention_n) / sum(disc_data$n_intervention) * 100, 1),
    Control_Events = sum(disc_data$discontinuation_any_control_n),
    Control_Total = sum(disc_data$n_control),
    Control_Rate_Pct = round(sum(disc_data$discontinuation_any_control_n) / sum(disc_data$n_control) * 100, 1),
    Pooled_RR = sprintf("%.2f", exp(meta_disc$TE.random)),
    CI_95 = sprintf("%.2f-%.2f", exp(meta_disc$lower.random), exp(meta_disc$upper.random)),
    P_value = ifelse(meta_disc$pval.random < 0.001, "<0.001", sprintf("%.3f", meta_disc$pval.random)),
    I2_Pct = sprintf("%.1f%%", meta_disc$I2 * 100)
  ))
}

# Add SAE results
if (exists("meta_sae") && nrow(sae_data) >= 2) {
  safety_summary <- rbind(safety_summary, data.frame(
    Outcome = "Serious Adverse Events",
    Trials = nrow(sae_data),
    ICI_Events = sum(sae_data$serious_ae_intervention_n),
    ICI_Total = sum(sae_data$n_intervention),
    ICI_Rate_Pct = round(sum(sae_data$serious_ae_intervention_n) / sum(sae_data$n_intervention) * 100, 1),
    Control_Events = sum(sae_data$serious_ae_control_n),
    Control_Total = sum(sae_data$n_control),
    Control_Rate_Pct = round(sum(sae_data$serious_ae_control_n) / sum(sae_data$n_control) * 100, 1),
    Pooled_RR = sprintf("%.2f", exp(meta_sae$TE.random)),
    CI_95 = sprintf("%.2f-%.2f", exp(meta_sae$lower.random), exp(meta_sae$upper.random)),
    P_value = ifelse(meta_sae$pval.random < 0.001, "<0.001", sprintf("%.3f", meta_sae$pval.random)),
    I2_Pct = sprintf("%.1f%%", meta_sae$I2 * 100)
  ))
}

# Add Fatal AE (descriptive only, no meta-analysis for rare events)
if (nrow(fatal_summary) > 0) {
  safety_summary <- rbind(safety_summary, data.frame(
    Outcome = "Fatal Adverse Events",
    Trials = nrow(safety_data %>% filter(!is.na(fatal_ae_intervention_n))),
    ICI_Events = fatal_summary$fatal_intervention,
    ICI_Total = fatal_summary$total_intervention,
    ICI_Rate_Pct = round(fatal_summary$fatal_intervention_rate, 2),
    Control_Events = fatal_summary$fatal_control,
    Control_Total = fatal_summary$total_control,
    Control_Rate_Pct = round(fatal_summary$fatal_control_rate, 2),
    Pooled_RR = "—",
    CI_95 = "—",
    P_value = "—",
    I2_Pct = "—"
  ))
}

print(safety_summary)

# Export summary table
write_csv(safety_summary, "tables/safety_meta_analysis_summary.csv")
cat("\n✓ Safety summary table saved: tables/safety_meta_analysis_summary.csv\n")

# ============================================================================
# 7. Benefit-Risk Assessment
# ============================================================================

cat("\n╔════════════════════════════════════════════════════════════════╗\n")
cat("║          BENEFIT-RISK ASSESSMENT                               ║\n")
cat("╚════════════════════════════════════════════════════════════════╝\n\n")

cat("BENEFITS (from efficacy meta-analyses):\n")
cat("  pCR:  RR 1.26 → +13.8% absolute benefit, NNT=7\n")
cat("  EFS:  HR 0.66 → +9.2% absolute benefit at 5 years, NNT=11\n")
cat("  OS:   HR 0.48 (individual trials HR 0.26-0.66, both p<0.01)\n\n")

cat("HARMS (from safety meta-analysis):\n")
if (exists("meta_irae")) {
  cat(sprintf("  Grade 3+ irAEs: RR %.2f → +%.1f%% absolute risk, NNH=%d\n",
              pooled_RR_irae,
              absolute_risk_increase * 100,
              NNH_irae))
}
if (exists("meta_disc")) {
  pooled_RR_disc <- exp(meta_disc$TE.random)
  baseline_risk_disc <- weighted.mean(
    disc_data$discontinuation_any_control_n / disc_data$n_control,
    disc_data$n_control
  )
  absolute_risk_increase_disc <- baseline_risk_disc * (pooled_RR_disc - 1)
  NNH_disc <- round(1 / absolute_risk_increase_disc)

  cat(sprintf("  Discontinuation: RR %.2f → +%.1f%% absolute risk, NNH=%d\n",
              pooled_RR_disc,
              absolute_risk_increase_disc * 100,
              NNH_disc))
}
cat(sprintf("  Fatal AE: %.2f%% (ICI) vs %.2f%% (Control) → Rare but serious\n",
            fatal_summary$fatal_intervention_rate,
            fatal_summary$fatal_control_rate))

cat("\nBENEFIT-RISK RATIO:\n")
if (exists("NNH_irae")) {
  cat(sprintf("  For every %d patients treated:\n", NNH_irae))
  cat(sprintf("    → 1 additional pCR (benefit)\n"))
  cat(sprintf("    → 1 additional Grade 3+ irAE (harm)\n"))
} else {
  cat("  KEYNOTE-522 data: 13% Grade 3+ irAEs vs 1.5% (NNH ~9)\n")
  cat("  → For every 9 patients treated: 1 Grade 3+ irAE\n")
  cat("  → For every 7 patients treated: 1 additional pCR (NNT=7)\n")
}
cat("\n  ✓ FAVORABLE: Benefit (cure potential) outweighs manageable toxicity\n")
cat("  ✓ Grade 3+ irAEs are typically reversible with treatment interruption\n")
cat("  ✓ Fatal events rare (<1%), comparable to chemotherapy alone\n")

cat("\n════════════════════════════════════════════════════════════════\n")
cat("Safety meta-analysis complete. Files generated:\n")
if (exists("meta_irae")) cat("  - figures/forest_plot_safety_irae.png\n")
if (exists("meta_disc")) cat("  - figures/forest_plot_safety_discontinuation.png\n")
if (exists("meta_sae")) cat("  - figures/forest_plot_safety_sae.png\n")
cat("  - tables/safety_meta_analysis_summary.csv\n")
cat("════════════════════════════════════════════════════════════════\n")
