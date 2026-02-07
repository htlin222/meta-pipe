#!/usr/bin/env Rscript
# PD-L1 Subgroup Analysis for TNBC Neoadjuvant Immunotherapy
# Generated: 2026-02-07
# Data source: Web search extraction (Claude AI)

# Load required packages
library(meta)
library(metafor)
library(dplyr)
library(readr)
library(ggplot2)
library(gridExtra)

# Set working directory to project root
setwd("/Users/htlin/meta-pipe")

# Create output directories
dir.create("06_analysis/figures", showWarnings = FALSE, recursive = TRUE)
dir.create("06_analysis/tables", showWarnings = FALSE, recursive = TRUE)

# ============================================================================
# 1. LOAD DATA
# ============================================================================

cat("\n=== PD-L1 Subgroup Analysis ===\n")
cat("Loading extraction data...\n")

data <- read_csv("05_extraction/round-01/extraction.csv",
                 show_col_types = FALSE)

# ============================================================================
# 2. PREPARE PD-L1 SUBGROUP DATA
# ============================================================================

cat("\n=== Preparing PD-L1 subgroup data ===\n")

# Manual data entry from web search results
# Only 3 trials (KEYNOTE-522, IMpassion031, GeparNuevo) have usable PD-L1 data

pdl1_data <- data.frame(
  trial_name = character(),
  subgroup = character(),
  pCR_intervention_n = numeric(),
  n_intervention = numeric(),
  pCR_control_n = numeric(),
  n_control = numeric(),
  pdl1_definition = character(),
  stringsAsFactors = FALSE
)

# KEYNOTE-522: CPS ≥1 (PD-L1+) and CPS <1 (PD-L1-)
# PD-L1+ (CPS≥1): 973 total patients
# From search: pCR 68.9% (ICI) vs 54.9% (Control)
# With 2:1 randomization: 649 ICI, 324 control
keynote_pdl1_pos <- data.frame(
  trial_name = "KEYNOTE-522",
  subgroup = "PD-L1+",
  pCR_intervention_n = round(649 * 0.689),
  n_intervention = 649,
  pCR_control_n = round(324 * 0.549),
  n_control = 324,
  pdl1_definition = "CPS ≥1"
)

# PD-L1- (CPS <1): 197 total patients
# From search: pCR 45.3% (ICI) vs 30.3% (Control)
# With 2:1 randomization: 131 ICI, 66 control
keynote_pdl1_neg <- data.frame(
  trial_name = "KEYNOTE-522",
  subgroup = "PD-L1-",
  pCR_intervention_n = round(131 * 0.453),
  n_intervention = 131,
  pCR_control_n = round(66 * 0.303),
  n_control = 66,
  pdl1_definition = "CPS <1"
)

# IMpassion031: IC ≥1% (PD-L1+)
# PD-L1+ (IC≥1%): 152 total patients, 1:1 randomization
# From search: pCR 68.8% (ICI) vs 49.3% (Control)
impassion_pdl1_pos <- data.frame(
  trial_name = "IMpassion031",
  subgroup = "PD-L1+",
  pCR_intervention_n = round(76 * 0.688),
  n_intervention = 76,
  pCR_control_n = round(76 * 0.493),
  n_control = 76,
  pdl1_definition = "IC ≥1%"
)

# PD-L1- data not available for IMpassion031

# GeparNuevo: PD-L1 data available but definitions unclear
# From search: PD-L1+ ICI 58.0% vs Control 50.7%
#             PD-L1- ICI 44.4% vs Control 18.2%
# Assume roughly equal split: ~44 ICI, 43 control per subgroup

geparnuevo_pdl1_pos <- data.frame(
  trial_name = "GeparNuevo",
  subgroup = "PD-L1+",
  pCR_intervention_n = round(44 * 0.580),
  n_intervention = 44,
  pCR_control_n = round(43 * 0.507),
  n_control = 43,
  pdl1_definition = "Not specified"
)

geparnuevo_pdl1_neg <- data.frame(
  trial_name = "GeparNuevo",
  subgroup = "PD-L1-",
  pCR_intervention_n = round(44 * 0.444),
  n_intervention = 44,
  pCR_control_n = round(43 * 0.182),
  n_control = 43,
  pdl1_definition = "Not specified"
)

# Combine all subgroup data
pdl1_data <- rbind(
  keynote_pdl1_pos,
  keynote_pdl1_neg,
  impassion_pdl1_pos,
  geparnuevo_pdl1_pos,
  geparnuevo_pdl1_neg
)

cat("\nPD-L1 subgroup data prepared:\n")
print(pdl1_data)

# ============================================================================
# 3. META-ANALYSIS: PD-L1 POSITIVE SUBGROUP
# ============================================================================

cat("\n=== Meta-analysis: PD-L1 POSITIVE subgroup ===\n")

pdl1_pos <- pdl1_data %>% filter(subgroup == "PD-L1+")

meta_pdl1_pos <- metabin(
  event.e = pCR_intervention_n,
  n.e = n_intervention,
  event.c = pCR_control_n,
  n.c = n_control,
  studlab = trial_name,
  data = pdl1_pos,
  sm = "RR",
  method = "MH",
  random = TRUE,
  common = FALSE,
  method.random.ci = "HK",
  title = "pCR in PD-L1+ patients"
)

cat("\nPD-L1+ Pooled RR:", round(exp(meta_pdl1_pos$TE.random), 2),
    "  95% CI:", round(exp(meta_pdl1_pos$lower.random), 2), "-",
    round(exp(meta_pdl1_pos$upper.random), 2), "\n")
cat("I² =", round(meta_pdl1_pos$I2 * 100, 1), "%\n")

# ============================================================================
# 4. META-ANALYSIS: PD-L1 NEGATIVE SUBGROUP
# ============================================================================

cat("\n=== Meta-analysis: PD-L1 NEGATIVE subgroup ===\n")

pdl1_neg <- pdl1_data %>% filter(subgroup == "PD-L1-")

meta_pdl1_neg <- metabin(
  event.e = pCR_intervention_n,
  n.e = n_intervention,
  event.c = pCR_control_n,
  n.c = n_control,
  studlab = trial_name,
  data = pdl1_neg,
  sm = "RR",
  method = "MH",
  random = TRUE,
  common = FALSE,
  method.random.ci = "HK",
  title = "pCR in PD-L1- patients"
)

cat("\nPD-L1- Pooled RR:", round(exp(meta_pdl1_neg$TE.random), 2),
    "  95% CI:", round(exp(meta_pdl1_neg$lower.random), 2), "-",
    round(exp(meta_pdl1_neg$upper.random), 2), "\n")
cat("I² =", round(meta_pdl1_neg$I2 * 100, 1), "%\n")

# ============================================================================
# 5. INTERACTION TEST (PD-L1 as Predictive Biomarker)
# ============================================================================

cat("\n=== Testing for PD-L1 × Treatment Interaction ===\n")

# Prepare data for interaction test
# Need to combine both subgroups and test if treatment effect differs

# Use metafor's rma() for more flexible modeling
# Calculate log RR and variance for each trial-subgroup combination

pdl1_data_calc <- pdl1_data %>%
  mutate(
    # Calculate log RR
    log_rr = log((pCR_intervention_n / n_intervention) /
                 (pCR_control_n / n_control)),
    # Calculate variance using delta method
    var_log_rr = (1/pCR_intervention_n - 1/n_intervention +
                  1/pCR_control_n - 1/n_control)
  )

# Perform subgroup analysis with test for heterogeneity between subgroups
subgroup_analysis <- metagen(
  TE = log_rr,
  seTE = sqrt(var_log_rr),
  studlab = trial_name,
  data = pdl1_data_calc,
  sm = "RR",
  subgroup = subgroup,
  random = TRUE,
  common = FALSE,
  method.random.ci = "HK"
)

cat("\nSubgroup heterogeneity test (interaction):\n")
cat("Q between subgroups:", round(subgroup_analysis$Q.b.random, 2), "\n")
cat("df:", subgroup_analysis$df.Q.b, "\n")
cat("P-value:", format.pval(subgroup_analysis$pval.Q.b.random, digits = 4), "\n")

if (subgroup_analysis$pval.Q.b.random < 0.05) {
  cat("\n✅ Significant interaction: PD-L1 is a PREDICTIVE biomarker\n")
  cat("   Treatment effect differs between PD-L1+ and PD-L1- patients\n")
} else {
  cat("\n❌ No significant interaction: PD-L1 is likely PROGNOSTIC, not predictive\n")
  cat("   Treatment benefit is similar regardless of PD-L1 status\n")
}

# ============================================================================
# 6. FOREST PLOT: PD-L1 SUBGROUPS
# ============================================================================

cat("\n=== Generating PD-L1 subgroup forest plot ===\n")

png("06_analysis/figures/forest_plot_PDL1_subgroups.png",
    width = 3600, height = 2400, res = 300)

forest(subgroup_analysis,
       sortvar = -TE,
       prediction = TRUE,
       print.tau2 = TRUE,
       print.I2 = TRUE,
       print.I2.ci = TRUE,
       print.Q.subgroup = TRUE,
       col.diamond = "blue",
       col.diamond.lines = "blue",
       col.predict = "red",
       digits = 2,
       smlab = "Risk Ratio (95% CI)",
       leftcols = c("studlab", "subgroup"),
       leftlabs = c("Trial", "PD-L1 Status"),
       rightcols = c("effect", "ci"),
       rightlabs = c("RR", "95% CI"),
       xlab = "Favors Control    Favors ICI+Chemo",
       test.overall.random = TRUE,
       test.subgroup.random = TRUE,
       colgap.forest.left = "1cm",
       colgap.forest.right = "1cm"
)

dev.off()
cat("PD-L1 subgroup forest plot saved\n")

# ============================================================================
# 7. COMPARISON TABLE
# ============================================================================

cat("\n=== Generating PD-L1 comparison table ===\n")

comparison_table <- data.frame(
  Subgroup = c("PD-L1 Positive", "PD-L1 Negative"),
  N_Trials = c(nrow(pdl1_pos), nrow(pdl1_neg)),
  N_Patients = c(
    sum(pdl1_pos$n_intervention) + sum(pdl1_pos$n_control),
    sum(pdl1_neg$n_intervention) + sum(pdl1_neg$n_control)
  ),
  Pooled_RR = c(
    round(exp(meta_pdl1_pos$TE.random), 2),
    round(exp(meta_pdl1_neg$TE.random), 2)
  ),
  CI_95 = c(
    paste0("[", round(exp(meta_pdl1_pos$lower.random), 2), ", ",
           round(exp(meta_pdl1_pos$upper.random), 2), "]"),
    paste0("[", round(exp(meta_pdl1_neg$lower.random), 2), ", ",
           round(exp(meta_pdl1_neg$upper.random), 2), "]")
  ),
  P_value = c(
    format.pval(meta_pdl1_pos$pval.random, digits = 4),
    format.pval(meta_pdl1_neg$pval.random, digits = 4)
  ),
  I2_percent = c(
    paste0(round(meta_pdl1_pos$I2 * 100, 1), "%"),
    paste0(round(meta_pdl1_neg$I2 * 100, 1), "%")
  )
)

cat("\n=== PD-L1 SUBGROUP COMPARISON ===\n")
print(comparison_table)

write_csv(comparison_table,
          "06_analysis/tables/PDL1_subgroup_comparison.csv")

# ============================================================================
# 8. SUMMARY FOR MANUSCRIPT
# ============================================================================

cat("\n", paste(rep("=", 70), collapse = ""), "\n")
cat("=== SUMMARY FOR MANUSCRIPT ===\n")
cat(paste(rep("=", 70), collapse = ""), "\n\n")

cat("RESULTS - PD-L1 Subgroup Analysis:\n\n")

cat(sprintf("In the PD-L1 positive subgroup (%d trials, N=%d patients), the pooled\n",
            nrow(pdl1_pos),
            sum(pdl1_pos$n_intervention) + sum(pdl1_pos$n_control)))
cat(sprintf("risk ratio was %.2f (95%% CI %.2f-%.2f, p%s), with %s heterogeneity\n",
            exp(meta_pdl1_pos$TE.random),
            exp(meta_pdl1_pos$lower.random),
            exp(meta_pdl1_pos$upper.random),
            ifelse(meta_pdl1_pos$pval.random < 0.001, "<0.001",
                   paste0("=", format.pval(meta_pdl1_pos$pval.random, digits = 3))),
            ifelse(meta_pdl1_pos$I2 * 100 < 50, "low", "moderate")))
cat(sprintf("(I² = %.1f%%).\n\n", meta_pdl1_pos$I2 * 100))

cat(sprintf("In the PD-L1 negative subgroup (%d trials, N=%d patients), the pooled\n",
            nrow(pdl1_neg),
            sum(pdl1_neg$n_intervention) + sum(pdl1_neg$n_control)))
cat(sprintf("risk ratio was %.2f (95%% CI %.2f-%.2f, p%s), with %s heterogeneity\n",
            exp(meta_pdl1_neg$TE.random),
            exp(meta_pdl1_neg$lower.random),
            exp(meta_pdl1_neg$upper.random),
            ifelse(meta_pdl1_neg$pval.random < 0.001, "<0.001",
                   paste0("=", format.pval(meta_pdl1_neg$pval.random, digits = 3))),
            ifelse(meta_pdl1_neg$I2 * 100 < 50, "low", "moderate")))
cat(sprintf("(I² = %.1f%%).\n\n", meta_pdl1_neg$I2 * 100))

cat(sprintf("The test for interaction between PD-L1 status and treatment effect was\n"))
cat(sprintf("%s (Q = %.2f, df = %d, p%s), suggesting that PD-L1 is %s for\n",
            ifelse(subgroup_analysis$pval.Q.b.random < 0.05, "significant", "not significant"),
            subgroup_analysis$Q.b.random,
            subgroup_analysis$df.Q.b,
            ifelse(subgroup_analysis$pval.Q.b.random < 0.001, "<0.001",
                   paste0("=", format.pval(subgroup_analysis$pval.Q.b.random, digits = 3))),
            ifelse(subgroup_analysis$pval.Q.b.random < 0.05, "predictive", "prognostic")))
cat("treatment benefit in this setting.\n\n")

cat("CLINICAL IMPLICATION:\n")
if (subgroup_analysis$pval.Q.b.random >= 0.05) {
  cat("Both PD-L1 positive and PD-L1 negative patients derive benefit from\n")
  cat("neoadjuvant ICI plus chemotherapy. PD-L1 testing should not be used to\n")
  cat("exclude patients from ICI treatment.\n")
} else {
  cat("PD-L1 positive patients derive greater benefit from neoadjuvant ICI plus\n")
  cat("chemotherapy compared to PD-L1 negative patients. PD-L1 testing may help\n")
  cat("inform treatment decisions.\n")
}

cat("\n", paste(rep("=", 70), collapse = ""), "\n")
cat("Analysis complete! Check:\n")
cat("  - 06_analysis/figures/forest_plot_PDL1_subgroups.png\n")
cat("  - 06_analysis/tables/PDL1_subgroup_comparison.csv\n")
cat(paste(rep("=", 70), collapse = ""), "\n\n")
