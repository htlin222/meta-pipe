# =============================================================================
# nma_01_setup.R — Environment Setup for Frontline DLBCL NMA
# =============================================================================
# Project: Updated NMA of frontline DLBCL chemoimmunotherapy regimens
# Primary: Bayesian NMA (gemtc) | Sensitivity: Frequentist (netmeta)
# =============================================================================

# --- 1. Install packages (skip if already installed) ---
pkgs <- c("gemtc", "rjags", "coda", "netmeta", "meta", "metafor",
          "ggplot2", "gt", "readr", "dplyr", "tidyr", "patchwork", "scales")

for (p in pkgs) {
  if (!requireNamespace(p, quietly = TRUE)) install.packages(p)
}

# --- 2. Verify JAGS ---
jags_ok <- tryCatch({
  library(rjags)
  cat("JAGS version:", .jags.version(), "\n")
  TRUE
}, error = function(e) {
  warning("JAGS not found. Install from: https://mcmc-jags.sourceforge.io/")
  FALSE
})

# --- 3. Global options ---
options(digits = 4, scipen = 999, warn = 1)

# MCMC defaults
MCMC_N_ADAPT  <- 5000
MCMC_N_ITER   <- 50000
MCMC_THIN     <- 10
MCMC_N_CHAINS <- 4

# Figure defaults
FIG_WIDTH  <- 10
FIG_HEIGHT <- 8
FIG_DPI    <- 300
FIG_DIR    <- "figures"
TBL_DIR    <- "tables"

if (!dir.exists(FIG_DIR)) dir.create(FIG_DIR, recursive = TRUE)
if (!dir.exists(TBL_DIR)) dir.create(TBL_DIR, recursive = TRUE)

# --- 4. Load libraries ---
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
library(patchwork)

cat("NMA environment ready.\n")
cat("gemtc:", as.character(packageVersion("gemtc")), "\n")
cat("netmeta:", as.character(packageVersion("netmeta")), "\n")
