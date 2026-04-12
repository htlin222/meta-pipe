# =============================================================================
# nma_11_cnma.R — Component Network Meta-Analysis (CNMA)
# =============================================================================
# Purpose: Decompose combination treatments into components, test interactions,
#          and optionally reconnect disconnected networks via additive assumption
# Input: net_re, nma_data from nma_04_models.R
# Output: Component effects, interaction tests, model comparisons
# Framework: Frequentist (netmeta::discomb) PRIMARY, Bayesian (multinma) SENSITIVITY
# Reference: Rücker et al. (2020) — Component NMA framework
# =============================================================================

source("nma_04_models.R")

# =============================================================================
# SECTION A: DATA PREPARATION FOR CNMA
# =============================================================================

cat("=== Component Network Meta-Analysis (CNMA) ===\n")
cat("Purpose: Decompose combination treatments into individual components\n\n")

# --- 1. Identify combination treatments ---
# Combination treatments should contain "+" in their name
# e.g., "DrugA+DrugB", "ACEI+ARB", "Chemo+Immuno"
all_treatments <- sort(unique(c(nma_data$treat1, nma_data$treat2)))

combo_treatments <- all_treatments[grepl("\\+", all_treatments)]
single_treatments <- all_treatments[!grepl("\\+", all_treatments)]

cat("All treatments:", paste(all_treatments, collapse = ", "), "\n")
cat("Combination treatments:", paste(combo_treatments, collapse = ", "), "\n")
cat("Single treatments:", paste(single_treatments, collapse = ", "), "\n\n")

if (length(combo_treatments) == 0) {
  cat("WARNING: No combination treatments found (no '+' in treatment names).\n")
  cat("CNMA requires at least some combination treatments.\n")
  cat("If your treatments are combinations, rename them with '+' separator.\n")
  cat("Example: 'ACEI_ARB' → 'ACEI+ARB'\n")
  cat("\nSkipping CNMA analysis.\n")
  stop("No combination treatments found. CNMA not applicable.")
}

# --- 2. Parse components from treatment names ---
# Extract unique components from all treatment labels
parse_components <- function(treatment) {
  trimws(unlist(strsplit(treatment, "\\+")))
}

all_components <- unique(unlist(lapply(all_treatments, parse_components)))
cat("Unique components:", paste(all_components, collapse = ", "), "\n")
cat("Number of components:", length(all_components), "\n\n")

# --- 3. Create component indicator matrix ---
# Each treatment gets a row with 1/0 for each component it contains
component_matrix <- data.frame(
  treatment = all_treatments,
  stringsAsFactors = FALSE
)

for (comp in all_components) {
  component_matrix[[comp]] <- sapply(all_treatments, function(trt) {
    as.integer(comp %in% parse_components(trt))
  })
}

cat("Component matrix:\n")
print(component_matrix)
cat("\n")

# --- 4. Define inactive treatment (reference) ---
# Typically "placebo", "control", or the treatment with fewest components
# Adapt this to your data:
inactive_treatment <- NULL

# Auto-detect: try common names
for (candidate in c("placebo", "Placebo", "PLACEBO", "control", "Control",
                     "sham", "Sham", "standard care", "SOC")) {
  if (candidate %in% all_treatments) {
    inactive_treatment <- candidate
    break
  }
}

if (is.null(inactive_treatment)) {
  # Fall back to single treatment with most studies
  cat("No placebo/control found. Using most common single treatment as reference.\n")
  single_counts <- nma_data %>%
    tidyr::pivot_longer(cols = c(treat1, treat2), values_to = "trt") %>%
    filter(trt %in% single_treatments) %>%
    count(trt, sort = TRUE)
  inactive_treatment <- single_counts$trt[1]
}

cat("Inactive (reference) treatment:", inactive_treatment, "\n\n")

# =============================================================================
# SECTION B: FREQUENTIST CNMA — ADDITIVE MODEL (PRIMARY)
# =============================================================================

cat("=== Frequentist CNMA: Additive Model (Primary Analysis) ===\n")

# discomb() requires component columns in the data
# It automatically creates the component design matrix
cnma_add <- discomb(
  TE, seTE, treat1, treat2, studlab,
  data      = nma_data,
  sm        = "RR",          # Adapt: "RR", "OR", "MD", "SMD"
  random    = TRUE,
  fixed     = TRUE,
  inactive  = inactive_treatment
)

cat("Additive CNMA summary:\n")
summary(cnma_add)

# Component-level effects
cat("\n--- Component Effects (Additive Model) ---\n")
cat("These represent the marginal effect of adding each component\n")
cat("relative to the inactive treatment.\n\n")

# Forest plot of component effects
png(file.path(FIG_DIR, "cnma_components_additive.png"),
    width = FIG_WIDTH, height = max(6, length(all_components) * 1.2),
    units = "in", res = FIG_DPI)

forest(cnma_add,
       leftcols  = c("studlab", "treat1", "treat2"),
       leftlabs  = c("Study", "Treatment 1", "Treatment 2"))

dev.off()
cat("Component forest plot saved to",
    file.path(FIG_DIR, "cnma_components_additive.png"), "\n")

# Q-test: compare standard NMA vs additive CNMA
cat("\n--- Model Comparison: Standard NMA vs Additive CNMA ---\n")
cat("Q_diff (additive model Q - standard NMA Q) tests the additivity assumption.\n")
cat("If p > 0.05: additive model is adequate.\n")
cat("If p < 0.05: additivity assumption may not hold; consider interaction model.\n\n")

cat("Additive CNMA heterogeneity:\n")
cat("  Q =", cnma_add$Q, "(df =", cnma_add$df.Q, ", p =",
    format.pval(cnma_add$pval.Q, digits = 4), ")\n")
cat("  tau² =", round(cnma_add$tau2, 4), "\n")
cat("  I² =", round(cnma_add$I2 * 100, 1), "%\n\n")

# Compare with standard NMA tau²
cat("Standard NMA tau²:", round(net_re$tau2, 4), "\n")
cat("Additive CNMA tau²:", round(cnma_add$tau2, 4), "\n")
if (cnma_add$tau2 < net_re$tau2) {
  cat("→ Additive CNMA reduces heterogeneity (component model explains some variation).\n")
} else {
  cat("→ Additive CNMA does not reduce heterogeneity.\n")
}

# =============================================================================
# SECTION C: FREQUENTIST CNMA — INTERACTION MODEL
# =============================================================================

cat("\n=== Frequentist CNMA: Interaction Model ===\n")

# Fit interaction model (if sufficient data)
# The interaction model allows synergy/antagonism between components
cnma_int <- tryCatch({
  discomb(
    TE, seTE, treat1, treat2, studlab,
    data      = nma_data,
    sm        = "RR",
    random    = TRUE,
    fixed     = TRUE,
    inactive  = inactive_treatment,
    C.matrix  = "full"  # Full model includes interaction terms
  )
}, error = function(e) {
  cat("Interaction model could not be fitted.\n")
  cat("Reason:", conditionMessage(e), "\n")
  cat("This may occur if there are insufficient studies to estimate interactions.\n")
  NULL
})

if (!is.null(cnma_int)) {
  cat("Interaction CNMA summary:\n")
  summary(cnma_int)

  # --- Interaction test ---
  cat("\n--- Interaction Test ---\n")
  cat("Tests whether component effects are purely additive or have interactions.\n")

  # Compare additive vs interaction via Q-difference
  q_diff   <- cnma_add$Q - cnma_int$Q
  df_diff  <- cnma_add$df.Q - cnma_int$df.Q
  p_interaction <- pchisq(q_diff, df = df_diff, lower.tail = FALSE)

  cat("Q_additive:", round(cnma_add$Q, 2), "(df =", cnma_add$df.Q, ")\n")
  cat("Q_interaction:", round(cnma_int$Q, 2), "(df =", cnma_int$df.Q, ")\n")
  cat("Q_difference:", round(q_diff, 2), "(df =", df_diff, ")\n")
  cat("p-value for interaction:", format.pval(p_interaction, digits = 4), "\n\n")

  if (p_interaction < 0.05) {
    cat("SIGNIFICANT INTERACTION detected (p < 0.05).\n")
    cat("The combination effect differs from the sum of individual components.\n")
    cat("Report the interaction model results and discuss clinical meaning.\n")
  } else {
    cat("No significant interaction (p >= 0.05).\n")
    cat("The additive model is adequate — component effects are approximately additive.\n")
    cat("Report the additive model as primary.\n")
  }

  # Save interaction test results
  interaction_results <- data.frame(
    Model      = c("Additive", "Interaction", "Difference"),
    Q          = c(round(cnma_add$Q, 2), round(cnma_int$Q, 2), round(q_diff, 2)),
    df         = c(cnma_add$df.Q, cnma_int$df.Q, df_diff),
    p_value    = c(format.pval(cnma_add$pval.Q, digits = 4),
                   format.pval(cnma_int$pval.Q, digits = 4),
                   format.pval(p_interaction, digits = 4)),
    tau2       = c(round(cnma_add$tau2, 4), round(cnma_int$tau2, 4), NA),
    stringsAsFactors = FALSE
  )

  write_csv(interaction_results, file.path(TBL_DIR, "cnma_interaction_test.csv"))
  cat("Interaction test results saved to",
      file.path(TBL_DIR, "cnma_interaction_test.csv"), "\n")
} else {
  cat("Interaction model not available. Reporting additive model only.\n")
}

# =============================================================================
# SECTION D: BAYESIAN CNMA (multinma — SENSITIVITY)
# =============================================================================

cat("\n=== Bayesian CNMA (multinma — Sensitivity Analysis) ===\n")

if (exists("multinma_ok") && multinma_ok) {

  # --- 1. Prepare data for multinma ---
  # multinma uses its own data format; adapt from nma_data
  # For contrast-based data:
  cat("Preparing data for Bayesian CNMA (multinma)...\n")

  bayes_cnma <- tryCatch({

    # Create multinma network with component information
    # Arm-based data preferred for multinma; adapt as needed:
    #
    # For arm-based data (events + totals):
    # mnma_data <- set_agd_arm(arm_data,
    #   study = study_id,
    #   trt = treatment,
    #   r = events,
    #   n = total_n,
    #   trt_ref = inactive_treatment
    # )
    #
    # For contrast-based data (relative effects):
    # mnma_data <- set_agd_contrast(contrast_data,
    #   study = studlab,
    #   trt = treat,
    #   y = TE,
    #   se = seTE,
    #   trt_ref = inactive_treatment
    # )

    # Fit Bayesian additive CNMA
    # The component model in multinma uses regression on component indicators
    # Adapt the formula to your component structure:
    #
    # bayes_fit <- nma(mnma_data,
    #   trt_effects = "random",
    #   regression = ~ component1 + component2 + ...,
    #   prior_intercept = normal(scale = 10),
    #   prior_trt = normal(scale = 10),
    #   prior_het = half_normal(scale = 1),
    #   iter = 4000,
    #   warmup = 2000,
    #   chains = 4
    # )

    cat("NOTE: Bayesian CNMA requires manual adaptation of the multinma data\n")
    cat("format and component regression formula for your specific dataset.\n")
    cat("See nma_11_cnma.R comments for template code.\n")
    cat("Uncomment and adapt the sections above.\n")
    NULL
  }, error = function(e) {
    cat("Bayesian CNMA failed:", conditionMessage(e), "\n")
    NULL
  })

  if (!is.null(bayes_cnma)) {
    # Convergence diagnostics
    cat("\n--- Bayesian CNMA Convergence Diagnostics ---\n")
    # print(summary(bayes_cnma))

    # Compare Bayesian vs frequentist
    cat("\n--- Bayesian vs Frequentist CNMA Concordance ---\n")
    cat("If results are concordant, report in manuscript:\n")
    cat("'Bayesian CNMA (multinma/Stan) yielded consistent results\n")
    cat(" with the frequentist CNMA (Supplement Table SX).'\n")
  }

} else {
  cat("multinma not installed. Skipping Bayesian CNMA.\n")
  cat("To enable: install.packages('multinma') (requires rstan or cmdstanr)\n")
  cat("Frequentist CNMA (discomb) results remain the primary analysis.\n")
}

# =============================================================================
# SECTION E: DISCONNECTED NETWORK RECONNECTION
# =============================================================================

cat("\n=== Disconnected Network Reconnection ===\n")

# Check if the standard NMA network was disconnected
nc <- netconnection(treat1, treat2, studlab, data = nma_data)

if (nc$n.subnets > 1) {
  cat("DISCONNECTED NETWORK detected (", nc$n.subnets, " sub-networks).\n")
  cat("CNMA additive model may reconnect the network by assuming\n")
  cat("that combination effects equal the sum of component effects.\n\n")

  cat("WARNING: This is a STRONG assumption. The reconnected network\n")
  cat("results should be reported as SENSITIVITY ANALYSIS only.\n")
  cat("The additivity assumption must be clinically justified.\n\n")

  # discomb() automatically handles disconnected networks
  # The additive model creates implicit links through shared components
  cat("The additive CNMA model above already includes the reconnected network.\n")
  cat("Compare these results with the standard NMA (which excluded disconnected treatments).\n")

} else {
  cat("Network is fully connected. No reconnection needed.\n")
  cat("CNMA results complement the standard NMA.\n")
}

# =============================================================================
# SECTION F: CNMA-SPECIFIC OUTPUTS
# =============================================================================

cat("\n=== CNMA Output Summary ===\n")

# --- Model comparison table ---
model_comparison <- data.frame(
  Model     = c("Standard NMA (netmeta)", "Additive CNMA", "Interaction CNMA"),
  tau2      = c(round(net_re$tau2, 4),
                round(cnma_add$tau2, 4),
                ifelse(!is.null(cnma_int), round(cnma_int$tau2, 4), NA)),
  I2_pct    = c(round(net_re$I2 * 100, 1),
                round(cnma_add$I2 * 100, 1),
                ifelse(!is.null(cnma_int), round(cnma_int$I2 * 100, 1), NA)),
  Q         = c(round(net_re$Q, 2),
                round(cnma_add$Q, 2),
                ifelse(!is.null(cnma_int), round(cnma_int$Q, 2), NA)),
  df        = c(net_re$df.Q,
                cnma_add$df.Q,
                ifelse(!is.null(cnma_int), cnma_int$df.Q, NA)),
  stringsAsFactors = FALSE
)

write_csv(model_comparison, file.path(TBL_DIR, "cnma_model_comparison.csv"))
cat("Model comparison table saved to",
    file.path(TBL_DIR, "cnma_model_comparison.csv"), "\n")
print(model_comparison)

# --- Save comprehensive report ---
sink("cnma_report.txt")
cat("========================================\n")
cat("COMPONENT NETWORK META-ANALYSIS REPORT\n")
cat("========================================\n\n")

cat("Reference treatment (inactive):", inactive_treatment, "\n")
cat("Combination treatments:", paste(combo_treatments, collapse = ", "), "\n")
cat("Components identified:", paste(all_components, collapse = ", "), "\n\n")

cat("--- Component Matrix ---\n")
print(component_matrix)

cat("\n--- Additive CNMA (Primary) ---\n")
summary(cnma_add)

if (!is.null(cnma_int)) {
  cat("\n--- Interaction CNMA ---\n")
  summary(cnma_int)
  cat("\n--- Interaction Test ---\n")
  cat("Q_difference:", round(q_diff, 2), "(df =", df_diff,
      ", p =", format.pval(p_interaction, digits = 4), ")\n")
}

cat("\n--- Model Comparison ---\n")
print(model_comparison)

cat("\n--- Network Connectivity ---\n")
cat("Sub-networks:", nc$n.subnets, "\n")
if (nc$n.subnets > 1) {
  cat("CNMA reconnected the network via additive assumption (sensitivity only).\n")
}
sink()

cat("\nCNMA report saved to cnma_report.txt\n")
cat("CNMA analysis complete.\n")
