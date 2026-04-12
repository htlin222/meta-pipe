# =============================================================================
# nma_01_setup.R — Environment Setup for Network Meta-Analysis
# =============================================================================
# Purpose: Initialize renv, install NMA packages, set global options
# Paradigm: Bayesian (gemtc) = PRIMARY, Frequentist (netmeta) = SENSITIVITY
# Packages: renv, gemtc, rjags, netmeta, meta, metafor, ggplot2, gt, flextable
# Output: renv.lock with pinned package versions
# Note: Requires JAGS installed on system (https://mcmc-jags.sourceforge.io/)
# =============================================================================

# --- 1. Initialize renv ---
if (!requireNamespace("renv", quietly = TRUE)) {
  install.packages("renv")
}
renv::init()

# --- 2. Install core NMA packages ---
install.packages(c(
  # Primary: Bayesian NMA
  "gemtc",         # Bayesian NMA via JAGS (primary analysis)
  "rjags",         # R interface to JAGS
  "coda",          # MCMC diagnostics (trace plots, Rhat, ESS)

  # Sensitivity: Frequentist NMA
  "netmeta",       # Frequentist NMA (sensitivity analysis / supplement)
                   # discomb() for CNMA, netmetareg() for meta-regression (>= 2.5)

  # Advanced: Bayesian CNMA (multinma)
  "multinma",      # Bayesian NMA with component regression (requires Stan)

  # Shared utilities
  "meta",          # Forest plots, pairwise helpers, pairwise()
  "metafor",       # Effect size calculation
  "dmetar",        # Meta-analysis helpers
  "ggplot2",       # Visualization
  "gt",            # Publication-quality tables
  "flextable",     # Word-compatible tables
  "readr",         # CSV reading
  "dplyr",         # Data manipulation
  "tidyr",         # Data reshaping
  "webshot2",      # PNG export for gt tables
  "patchwork"      # Multi-panel figures
))

# --- 3. Verify JAGS installation ---
jags_ok <- tryCatch({
  library(rjags)
  cat("JAGS version:", .jags.version(), "\n")
  TRUE
}, error = function(e) {
  warning("JAGS not found. Install from: https://mcmc-jags.sourceforge.io/")
  warning("Bayesian NMA (gemtc) requires JAGS. Falling back to netmeta only.")
  FALSE
})

# --- 3b. Verify Stan/multinma installation (for Bayesian CNMA) ---
multinma_ok <- tryCatch({
  library(multinma)
  cat("multinma version:", as.character(packageVersion("multinma")), "\n")
  TRUE
}, error = function(e) {
  warning("multinma not available. Bayesian CNMA will be skipped.")
  warning("Install: install.packages('multinma') (requires rstan or cmdstanr)")
  FALSE
})

# --- 4. Snapshot renv ---
renv::snapshot()

# --- 5. Global options ---
options(
  digits = 4,
  scipen = 999,
  warn = 1
)

# --- 6. MCMC defaults ---
MCMC_N_ADAPT  <- 5000    # Adaptation iterations
MCMC_N_ITER   <- 50000   # Sampling iterations (increase if poor convergence)
MCMC_THIN     <- 10      # Thinning interval
MCMC_N_CHAINS <- 4       # Number of MCMC chains

# --- 7. Figure export defaults ---
FIG_WIDTH  <- 10
FIG_HEIGHT <- 8
FIG_DPI    <- 300
FIG_DIR    <- "figures"
TBL_DIR    <- "tables"

if (!dir.exists(FIG_DIR)) dir.create(FIG_DIR, recursive = TRUE)
if (!dir.exists(TBL_DIR)) dir.create(TBL_DIR, recursive = TRUE)

# --- 8. Load libraries ---
library(gemtc)
library(coda)
library(netmeta)
library(meta)
library(metafor)
library(ggplot2)
library(gt)
library(readr)
library(dplyr)
library(tidyr)

cat("NMA environment setup complete.\n")
cat("Primary: gemtc (Bayesian) | Sensitivity: netmeta (frequentist)\n")
cat("CNMA: netmeta::discomb() (primary) | multinma (Bayesian sensitivity)\n")
cat("gemtc version:", as.character(packageVersion("gemtc")), "\n")
cat("netmeta version:", as.character(packageVersion("netmeta")), "\n")
if (jags_ok) cat("JAGS: OK\n") else cat("JAGS: NOT FOUND\n")
if (multinma_ok) cat("multinma: OK (Stan backend)\n") else cat("multinma: NOT FOUND\n")
