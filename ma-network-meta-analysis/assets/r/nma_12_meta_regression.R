# =============================================================================
# nma_12_meta_regression.R — NMA Meta-Regression & Subgroup Analysis
# =============================================================================
# Purpose: Explore heterogeneity sources via NMA meta-regression (continuous
#          and categorical covariates) and subgroup NMA analyses
# Input: net_re, nma_data from nma_04_models.R
# Output: Regression coefficients, bubble plots, subgroup comparisons
# Reference: Donegan et al. (2013) — Assessing key assumptions of NMA
# =============================================================================

source("nma_04_models.R")

# =============================================================================
# SECTION A: NMA META-REGRESSION (CONTINUOUS COVARIATES)
# =============================================================================

cat("=== NMA Meta-Regression ===\n")
cat("Tests whether study-level covariates explain heterogeneity in the network.\n\n")

# --- 1. Define covariates ---
# Adapt to your extraction data columns.
# These should be study-level (same value for all arms within a study).
# Common covariates: mean_age, year, sample_size, follow_up_months, risk_of_bias_score

continuous_covariates <- c()  # e.g., c("mean_age", "year", "follow_up_months")
categorical_covariates <- c() # e.g., c("risk_of_bias", "region", "blinding")

# Check which covariates are available in nma_data
available_cols <- names(nma_data)
cat("Available columns in nma_data:", paste(available_cols, collapse = ", "), "\n\n")

# --- 2. Fit meta-regression for each continuous covariate ---
if (length(continuous_covariates) > 0) {
  cat("--- Continuous Covariate Meta-Regression ---\n")

  metareg_results <- list()

  for (covar in continuous_covariates) {
    if (!covar %in% available_cols) {
      cat("Skipping", covar, "- not found in data\n")
      next
    }

    # Check for sufficient non-missing values
    n_available <- sum(!is.na(nma_data[[covar]]))
    if (n_available < 5) {
      cat("Skipping", covar, "- only", n_available, "non-missing values\n")
      next
    }

    cat("\nMeta-regression:", covar, "\n")

    reg <- tryCatch({
      netmetareg(net_re, formula = as.formula(paste("~", covar)))
    }, error = function(e) {
      cat("  Failed:", conditionMessage(e), "\n")
      NULL
    })

    if (!is.null(reg)) {
      cat("  Coefficient:", round(coef(reg)[covar], 4), "\n")
      cat("  p-value:", format.pval(reg$pval.random[covar], digits = 4), "\n")
      cat("  Residual tau²:", round(reg$tau2, 4),
          "(baseline:", round(net_re$tau2, 4), ")\n")

      tau2_reduction <- (1 - reg$tau2 / net_re$tau2) * 100
      cat("  tau² reduction:", round(tau2_reduction, 1), "%\n")

      metareg_results[[covar]] <- list(
        covariate     = covar,
        coefficient   = coef(reg)[covar],
        se            = reg$se[covar],
        pvalue        = reg$pval.random[covar],
        tau2_residual = reg$tau2,
        tau2_baseline = net_re$tau2,
        tau2_reduction_pct = tau2_reduction
      )

      # Bubble plot
      png(file.path(FIG_DIR, paste0("nma_metareg_", covar, ".png")),
          width = FIG_WIDTH, height = FIG_HEIGHT, units = "in", res = FIG_DPI)

      bubble(reg,
             xlab     = covar,
             ylab     = paste("Treatment effect (", net_re$sm, ")"),
             main     = paste("NMA Meta-Regression:", covar),
             col      = "steelblue",
             studlab  = TRUE,
             cex.studlab = 0.7)

      dev.off()
      cat("  Bubble plot saved to",
          file.path(FIG_DIR, paste0("nma_metareg_", covar, ".png")), "\n")
    }
  }

  # Summary table
  if (length(metareg_results) > 0) {
    metareg_df <- do.call(rbind, lapply(metareg_results, function(x) {
      data.frame(
        Covariate    = x$covariate,
        Coefficient  = round(x$coefficient, 4),
        SE           = round(x$se, 4),
        p_value      = format.pval(x$pvalue, digits = 4),
        tau2_residual = round(x$tau2_residual, 4),
        tau2_reduction_pct = round(x$tau2_reduction_pct, 1),
        stringsAsFactors = FALSE
      )
    }))

    write_csv(metareg_df, file.path(TBL_DIR, "nma_metareg_results.csv"))
    cat("\nMeta-regression summary saved to",
        file.path(TBL_DIR, "nma_metareg_results.csv"), "\n")
    print(metareg_df)
  }
} else {
  cat("No continuous covariates specified.\n")
  cat("Adapt continuous_covariates vector at the top of this script.\n\n")
}

# =============================================================================
# SECTION B: NMA META-REGRESSION (CATEGORICAL COVARIATES)
# =============================================================================

if (length(categorical_covariates) > 0) {
  cat("\n--- Categorical Covariate Meta-Regression ---\n")

  cat_metareg_results <- list()

  for (covar in categorical_covariates) {
    if (!covar %in% available_cols) {
      cat("Skipping", covar, "- not found in data\n")
      next
    }

    # Check for sufficient categories
    categories <- unique(nma_data[[covar]][!is.na(nma_data[[covar]])])
    if (length(categories) < 2) {
      cat("Skipping", covar, "- only", length(categories), "category\n")
      next
    }

    cat("\nMeta-regression:", covar, "(categories:", paste(categories, collapse = ", "), ")\n")

    reg <- tryCatch({
      netmetareg(net_re, formula = as.formula(paste("~ factor(", covar, ")")))
    }, error = function(e) {
      cat("  Failed:", conditionMessage(e), "\n")
      NULL
    })

    if (!is.null(reg)) {
      cat("  Coefficients:\n")
      print(round(coef(reg), 4))
      cat("  Residual tau²:", round(reg$tau2, 4), "\n")

      cat_metareg_results[[covar]] <- reg
    }
  }
} else {
  cat("No categorical covariates specified.\n")
  cat("Adapt categorical_covariates vector at the top of this script.\n\n")
}

# =============================================================================
# SECTION C: SUBGROUP NMA
# =============================================================================

cat("\n=== Subgroup NMA ===\n")
cat("Fits separate NMA models within subgroups to compare treatment effects.\n\n")

# Define subgroup variable (must be study-level, categorical)
# Adapt to your data:
subgroup_var <- NULL  # e.g., "risk_of_bias_level", "geographic_region"

if (!is.null(subgroup_var) && subgroup_var %in% available_cols) {

  subgroups <- unique(nma_data[[subgroup_var]][!is.na(nma_data[[subgroup_var]])])
  cat("Subgroup variable:", subgroup_var, "\n")
  cat("Subgroups:", paste(subgroups, collapse = ", "), "\n\n")

  subgroup_results <- list()

  for (sg in subgroups) {
    cat("--- Subgroup:", sg, "---\n")

    sg_data <- nma_data[nma_data[[subgroup_var]] == sg, ]
    cat("Studies in subgroup:", length(unique(sg_data$studlab)), "\n")

    # Check connectivity within subgroup
    nc_sg <- tryCatch(
      netconnection(sg_data$treat1, sg_data$treat2, sg_data$studlab),
      error = function(e) NULL
    )

    if (is.null(nc_sg) || nc_sg$n.subnets > 1) {
      cat("Subgroup network is disconnected. Skipping NMA for this subgroup.\n\n")
      next
    }

    # Fit subgroup NMA
    net_sg <- tryCatch(
      netmeta(TE, seTE, treat1, treat2, studlab,
              data = sg_data, sm = "RR",
              random = TRUE, method.tau = "REML"),
      error = function(e) {
        cat("NMA failed for subgroup:", conditionMessage(e), "\n")
        NULL
      }
    )

    if (!is.null(net_sg)) {
      cat("tau²:", round(net_sg$tau2, 4), "\n")
      cat("I²:", round(net_sg$I2 * 100, 1), "%\n\n")

      subgroup_results[[sg]] <- list(
        subgroup   = sg,
        n_studies  = length(unique(sg_data$studlab)),
        tau2       = net_sg$tau2,
        I2         = net_sg$I2,
        net        = net_sg
      )

      # Subgroup forest plot
      png(file.path(FIG_DIR, paste0("nma_subgroup_", sg, ".png")),
          width = FIG_WIDTH, height = FIG_HEIGHT, units = "in", res = FIG_DPI)

      forest(net_sg,
             reference.group = net_re$reference.group,
             sortvar = TE,
             label.left  = paste("Favours", net_re$reference.group),
             label.right = "Favours treatment")

      dev.off()
      cat("Forest plot saved to",
          file.path(FIG_DIR, paste0("nma_subgroup_", sg, ".png")), "\n\n")
    }
  }

  # --- Subgroup comparison table ---
  if (length(subgroup_results) > 1) {
    cat("--- Subgroup Comparison ---\n")

    subgroup_df <- do.call(rbind, lapply(subgroup_results, function(x) {
      data.frame(
        Subgroup    = x$subgroup,
        N_studies   = x$n_studies,
        tau2        = round(x$tau2, 4),
        I2_pct      = round(x$I2 * 100, 1),
        stringsAsFactors = FALSE
      )
    }))

    write_csv(subgroup_df, file.path(TBL_DIR, "nma_subgroup_comparison.csv"))
    cat("Subgroup comparison saved to",
        file.path(TBL_DIR, "nma_subgroup_comparison.csv"), "\n")
    print(subgroup_df)
  }

} else {
  cat("No subgroup variable specified (or not found in data).\n")
  cat("Set subgroup_var at the top of Section C to enable subgroup NMA.\n")
  cat("Example: subgroup_var <- 'risk_of_bias_level'\n\n")
}

# =============================================================================
# SECTION D: OUTPUTS
# =============================================================================

cat("\n=== Meta-Regression & Subgroup Summary ===\n")

# Heterogeneity explained summary
het_summary <- data.frame(
  Model     = "Full NMA (no covariates)",
  tau2      = round(net_re$tau2, 4),
  I2_pct    = round(net_re$I2 * 100, 1),
  stringsAsFactors = FALSE
)

if (exists("metareg_results") && length(metareg_results) > 0) {
  for (covar_name in names(metareg_results)) {
    res <- metareg_results[[covar_name]]
    het_summary <- rbind(het_summary, data.frame(
      Model  = paste("Adjusted for", covar_name),
      tau2   = round(res$tau2_residual, 4),
      I2_pct = NA,
      stringsAsFactors = FALSE
    ))
  }
}

write_csv(het_summary, file.path(TBL_DIR, "nma_heterogeneity_explained.csv"))
cat("Heterogeneity summary saved to",
    file.path(TBL_DIR, "nma_heterogeneity_explained.csv"), "\n")
print(het_summary)

# --- Save report ---
sink("nma_metareg_report.txt")
cat("==========================================\n")
cat("NMA META-REGRESSION & SUBGROUP REPORT\n")
cat("==========================================\n\n")

cat("--- Heterogeneity Explained ---\n")
print(het_summary)

if (exists("metareg_df") && nrow(metareg_df) > 0) {
  cat("\n--- Meta-Regression Coefficients ---\n")
  print(metareg_df)
}

if (exists("subgroup_df") && nrow(subgroup_df) > 0) {
  cat("\n--- Subgroup Comparison ---\n")
  print(subgroup_df)
}
sink()

cat("\nMeta-regression report saved to nma_metareg_report.txt\n")
