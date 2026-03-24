#!/usr/bin/env Rscript
# =============================================================================
# NMA Step 09: Sensitivity Analyses
# Project: G-CSF Prophylaxis in Chemotherapy-Induced Neutropenia
# =============================================================================

library(netmeta)
library(readr)
library(dplyr)

analysis_dir <- "projects/gcsf-neutropenia/06_analysis"
load(file.path(analysis_dir, "nma_data.RData"))
load(file.path(analysis_dir, "nma_model.RData"))

# --- Helper function: run NMA and extract key results ---
run_sensitivity <- function(data, label, ref = "placebo") {
  cat(sprintf("\n=== Sensitivity Analysis: %s ===\n", label))
  cat(sprintf("Studies included: %d\n", length(unique(data$studlab))))

  tryCatch({
    sens_nma <- netmeta(
      TE = data$TE,
      seTE = data$seTE,
      treat1 = data$treat1,
      treat2 = data$treat2,
      studlab = data$studlab,
      sm = "RR",
      reference.group = ref,
      comb.fixed = FALSE,
      comb.random = TRUE,
      method.tau = "REML"
    )

    # Extract results vs placebo
    results <- data.frame(
      sensitivity = label,
      treatment = sens_nma$trts[sens_nma$trts != ref],
      stringsAsFactors = FALSE
    )
    for (trt in results$treatment) {
      results$RR[results$treatment == trt] <- round(exp(sens_nma$TE.random[trt, ref]), 2)
      results$lower[results$treatment == trt] <- round(exp(sens_nma$lower.random[trt, ref]), 2)
      results$upper[results$treatment == trt] <- round(exp(sens_nma$upper.random[trt, ref]), 2)
      results$pval[results$treatment == trt] <- round(sens_nma$pval.random[trt, ref], 4)
    }
    results$tau2 <- round(sens_nma$tau^2, 4)
    results$I2 <- round(sens_nma$I2 * 100, 1)

    print(results)
    return(results)
  }, error = function(e) {
    cat("Error:", e$message, "\n")
    return(NULL)
  })
}

# --- 1. Main analysis (baseline) ---
main_results <- run_sensitivity(pw_meta, "Main analysis")

# --- 2. Exclude high-RoB studies ---
high_rob_studies <- rob$study_id[rob$overall_rob == "high"]
cat("\nHigh-RoB studies to exclude:", paste(high_rob_studies, collapse = ", "), "\n")

pw_low_rob <- pw_meta %>% filter(!studlab %in% high_rob_studies)
rob_results <- run_sensitivity(pw_low_rob, "Exclude high-RoB")

# --- 3. Exclude dose-finding study (Buchner2014) ---
pw_no_dose <- pw_meta %>% filter(studlab != "Buchner2014")
dose_results <- run_sensitivity(pw_no_dose, "Exclude Buchner2014 (dose-finding)")

# --- 4. Exclude co-intervention study (TimmerBonte2005) ---
pw_no_coint <- pw_meta %>% filter(studlab != "TimmerBonte2005")
coint_results <- run_sensitivity(pw_no_coint, "Exclude TimmerBonte2005 (co-intervention)")

# --- 5. Exclude both Buchner2014 and TimmerBonte2005 ---
pw_strict <- pw_meta %>% filter(!studlab %in% c("Buchner2014", "TimmerBonte2005"))
strict_results <- run_sensitivity(pw_strict, "Exclude both problematic studies")

# --- 6. Double-blind studies only ---
open_label <- extraction$study_id[extraction$blinding == "open-label"]
cat("\nOpen-label studies:", paste(open_label, collapse = ", "), "\n")
pw_blinded <- pw_meta %>% filter(!studlab %in% open_label)

# Check if network remains connected
blinded_trts <- unique(c(pw_blinded$treat1, pw_blinded$treat2))
cat("Treatments in blinded-only analysis:", paste(blinded_trts, collapse = ", "), "\n")

if (length(blinded_trts) >= 3 && "placebo" %in% blinded_trts) {
  blinded_results <- run_sensitivity(pw_blinded, "Double-blind studies only")
} else {
  cat("Network disconnected in blinded-only analysis; skipping.\n")
  blinded_results <- NULL
}

# --- Combine all sensitivity results ---
all_sens <- bind_rows(
  main_results,
  rob_results,
  dose_results,
  coint_results,
  strict_results,
  blinded_results
)

write_csv(all_sens, file.path(analysis_dir, "tables", "sensitivity_analyses.csv"))
cat("\nSensitivity analyses saved to tables/sensitivity_analyses.csv\n")

# --- Summary comparison ---
cat("\n=== Sensitivity Analysis Summary ===\n")
cat("Checking robustness: Are conclusions consistent across analyses?\n\n")

for (trt in unique(all_sens$treatment)) {
  trt_data <- all_sens[all_sens$treatment == trt, ]
  cat(sprintf("--- %s vs placebo ---\n", trt))
  for (i in 1:nrow(trt_data)) {
    row <- trt_data[i, ]
    sig <- ifelse(row$pval < 0.05, "SIG", "NS")
    cat(sprintf(
      "  %-40s RR=%.2f (%.2f-%.2f) [%s]\n",
      row$sensitivity, row$RR, row$lower, row$upper, sig
    ))
  }
  cat("\n")
}
