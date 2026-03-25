# =============================================================================
# nma_10_run_all.R — Run Complete DLBCL Frontline NMA Pipeline
# =============================================================================
# Execute all NMA scripts in order
# =============================================================================

cat("=== Running Frontline DLBCL NMA Pipeline ===\n")
cat("Start time:", format(Sys.time()), "\n\n")

tryCatch({
  cat("Step 1/7: Setup...\n")
  source("nma_01_setup.R")

  cat("\nStep 2/7: Data preparation...\n")
  source("nma_02_data_prep.R")

  cat("\nStep 3/7: Network graph...\n")
  source("nma_03_network_graph.R")

  cat("\nStep 4/7: Models (Bayesian + Frequentist)...\n")
  source("nma_04_models.R")

  cat("\nStep 5/7: Inconsistency assessment...\n")
  source("nma_05_inconsistency.R")

  cat("\nStep 6/7: Forest plots...\n")
  source("nma_06_forest_plots.R")

  cat("\nStep 7/7: Rankings + League table + Sensitivity...\n")
  source("nma_07_rankings.R")
  source("nma_08_league_table.R")
  source("nma_09_sensitivity.R")

  cat("\n=== Pipeline Complete ===\n")
  cat("End time:", format(Sys.time()), "\n")
  cat("\nOutputs:\n")
  cat("  Figures:", paste(list.files("figures", pattern = "\\.png$"), collapse = ", "), "\n")
  cat("  Tables:", paste(list.files("tables", pattern = "\\.(csv|png)$"), collapse = ", "), "\n")

}, error = function(e) {
  cat("\nERROR:", e$message, "\n")
  cat("Pipeline failed at the step above.\n")
})
