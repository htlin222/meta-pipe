# =============================================================================
# nma_13_transitivity_tests.R — Statistical Transitivity Assessment
# =============================================================================
# Purpose: Supplement clinical transitivity assessment (nma-assumptions.md)
#          with quantitative statistical tests for effect modifier balance
# Input: net_re, nma_data from nma_04_models.R; study-level covariates
# Output: Transitivity test results, heatmap, traffic light table
# Note: These tests are NOT definitive — transitivity remains a clinical
#       judgment. Statistical tests provide supporting evidence only.
# Reference: Salanti (2012); Donegan et al. (2013)
# =============================================================================

source("nma_04_models.R")

# =============================================================================
# SECTION A: EFFECT MODIFIER DISTRIBUTION COMPARISON
# =============================================================================

cat("=== Statistical Transitivity Assessment ===\n")
cat("Tests whether potential effect modifiers are balanced across comparisons.\n")
cat("NOTE: These tests supplement — not replace — clinical judgment.\n\n")

# --- 1. Define potential effect modifiers ---
# Adapt to your extraction data columns.
# These should be study-level characteristics that could modify treatment effects.

continuous_modifiers  <- c()  # e.g., c("mean_age", "percent_female", "follow_up_months")
categorical_modifiers <- c()  # e.g., c("disease_stage", "line_of_therapy", "risk_of_bias")

available_cols <- names(nma_data)
cat("Available columns:", paste(available_cols, collapse = ", "), "\n\n")

# --- 2. Create comparison identifier ---
# Group studies by their pairwise comparison
nma_data$comparison <- paste(
  pmin(nma_data$treat1, nma_data$treat2),
  pmax(nma_data$treat1, nma_data$treat2),
  sep = " vs "
)

comparisons <- sort(unique(nma_data$comparison))
cat("Unique comparisons:", length(comparisons), "\n")
cat(paste(" -", comparisons), sep = "\n")
cat("\n")

# --- 3. Test continuous modifiers ---
continuous_results <- list()

if (length(continuous_modifiers) > 0) {
  cat("--- Continuous Effect Modifier Tests ---\n")
  cat("Using Kruskal-Wallis test (non-parametric ANOVA across comparisons)\n\n")

  for (modifier in continuous_modifiers) {
    if (!modifier %in% available_cols) {
      cat("Skipping", modifier, "- not found in data\n")
      next
    }

    # Remove missing values
    test_data <- nma_data[!is.na(nma_data[[modifier]]), ]

    # Need at least 2 comparisons with data
    comp_counts <- table(test_data$comparison)
    valid_comps <- names(comp_counts[comp_counts >= 1])

    if (length(valid_comps) < 2) {
      cat("Skipping", modifier, "- data in fewer than 2 comparisons\n")
      next
    }

    test_data <- test_data[test_data$comparison %in% valid_comps, ]

    # Kruskal-Wallis test
    kw <- tryCatch(
      kruskal.test(as.formula(paste(modifier, "~ comparison")), data = test_data),
      error = function(e) NULL
    )

    if (!is.null(kw)) {
      cat(modifier, ": H =", round(kw$statistic, 2),
          ", df =", kw$parameter,
          ", p =", format.pval(kw$p.value, digits = 4), "\n")

      # Concern level
      concern <- ifelse(kw$p.value < 0.01, "High",
                   ifelse(kw$p.value < 0.10, "Moderate", "Low"))
      cat("  → Concern:", concern, "\n")

      # Summary by comparison
      comp_summary <- test_data %>%
        group_by(comparison) %>%
        summarise(
          n      = n(),
          median = round(median(.data[[modifier]], na.rm = TRUE), 1),
          IQR    = paste0(round(quantile(.data[[modifier]], 0.25, na.rm = TRUE), 1),
                          "-",
                          round(quantile(.data[[modifier]], 0.75, na.rm = TRUE), 1)),
          .groups = "drop"
        )
      print(as.data.frame(comp_summary))
      cat("\n")

      continuous_results[[modifier]] <- list(
        modifier  = modifier,
        statistic = kw$statistic,
        df        = kw$parameter,
        p_value   = kw$p.value,
        concern   = concern
      )
    }
  }
}

# --- 4. Test categorical modifiers ---
categorical_results <- list()

if (length(categorical_modifiers) > 0) {
  cat("--- Categorical Effect Modifier Tests ---\n")
  cat("Using Chi-squared / Fisher's exact test across comparisons\n\n")

  for (modifier in categorical_modifiers) {
    if (!modifier %in% available_cols) {
      cat("Skipping", modifier, "- not found in data\n")
      next
    }

    test_data <- nma_data[!is.na(nma_data[[modifier]]), ]

    # Contingency table: comparison × modifier category
    ct <- table(test_data$comparison, test_data[[modifier]])

    if (nrow(ct) < 2 || ncol(ct) < 2) {
      cat("Skipping", modifier, "- insufficient variation\n")
      next
    }

    # Use Fisher's exact test if any expected cell < 5
    expected <- chisq.test(ct)$expected
    use_fisher <- any(expected < 5)

    test_result <- tryCatch({
      if (use_fisher) {
        fisher.test(ct, simulate.p.value = TRUE, B = 10000)
      } else {
        chisq.test(ct)
      }
    }, error = function(e) NULL)

    if (!is.null(test_result)) {
      test_name <- ifelse(use_fisher, "Fisher's exact", "Chi-squared")
      cat(modifier, "(", test_name, "): p =",
          format.pval(test_result$p.value, digits = 4), "\n")

      concern <- ifelse(test_result$p.value < 0.01, "High",
                   ifelse(test_result$p.value < 0.10, "Moderate", "Low"))
      cat("  → Concern:", concern, "\n")

      cat("  Contingency table:\n")
      print(ct)
      cat("\n")

      categorical_results[[modifier]] <- list(
        modifier  = modifier,
        test      = test_name,
        p_value   = test_result$p.value,
        concern   = concern
      )
    }
  }
}

# =============================================================================
# SECTION B: NETWORK META-REGRESSION AS TRANSITIVITY PROXY
# =============================================================================

cat("\n=== Meta-Regression Transitivity Proxy ===\n")
cat("If adding a covariate substantially changes NMA results,\n")
cat("that covariate may violate transitivity.\n\n")

all_modifiers <- c(continuous_modifiers, categorical_modifiers)
regression_proxy_results <- list()

for (modifier in all_modifiers) {
  if (!modifier %in% available_cols) next
  if (sum(!is.na(nma_data[[modifier]])) < 5) next

  cat("Testing:", modifier, "\n")

  # Fit NMA with and without the covariate
  reg_adjusted <- tryCatch({
    if (modifier %in% continuous_modifiers) {
      netmetareg(net_re, formula = as.formula(paste("~", modifier)))
    } else {
      netmetareg(net_re, formula = as.formula(paste("~ factor(", modifier, ")")))
    }
  }, error = function(e) NULL)

  if (!is.null(reg_adjusted)) {
    tau2_change <- (reg_adjusted$tau2 - net_re$tau2) / net_re$tau2 * 100

    cat("  tau² unadjusted:", round(net_re$tau2, 4), "\n")
    cat("  tau² adjusted:", round(reg_adjusted$tau2, 4), "\n")
    cat("  Change:", round(tau2_change, 1), "%\n")

    # Large tau² reduction suggests the covariate explains heterogeneity
    # which may indicate it's an effect modifier violating transitivity
    if (abs(tau2_change) > 20) {
      cat("  → NOTABLE: >20% change in tau² — potential transitivity concern\n")
    }
    cat("\n")

    regression_proxy_results[[modifier]] <- list(
      modifier      = modifier,
      tau2_before   = net_re$tau2,
      tau2_after    = reg_adjusted$tau2,
      tau2_change_pct = tau2_change
    )
  }
}

# =============================================================================
# SECTION C: DIRECT vs FULL NMA COMPARISON (Salanti 2012 approach)
# =============================================================================

cat("\n=== Direct vs Full NMA Comparison ===\n")
cat("Compares direct-only estimates with full NMA estimates.\n")
cat("Systematic discrepancies may suggest transitivity violations.\n")
cat("(This complements node-splitting in nma_05_inconsistency.R)\n\n")

# Get node-splitting results (direct vs indirect vs NMA)
ns <- netsplit(net_re)
ns_df <- as.data.frame(ns)

if (nrow(ns_df) > 0 && "direct" %in% names(ns_df) && "nma" %in% names(ns_df)) {
  cat("Comparisons with both direct and indirect evidence:\n\n")

  # Calculate absolute differences between direct and NMA estimates
  if ("TE.direct" %in% names(ns_df) && "TE.nma" %in% names(ns_df)) {
    ns_df$diff_direct_nma <- abs(ns_df$TE.direct - ns_df$TE.nma)

    cat("Direct vs NMA estimate differences:\n")
    for (i in seq_len(nrow(ns_df))) {
      cat(sprintf("  %s: |direct - NMA| = %.3f",
                  ns_df$comparison[i],
                  ns_df$diff_direct_nma[i]))
      if (!is.na(ns_df$p.value[i]) && ns_df$p.value[i] < 0.10) {
        cat(" ** (p < 0.10)")
      }
      cat("\n")
    }

    # Overall assessment
    n_sig <- sum(ns_df$p.value < 0.10, na.rm = TRUE)
    n_total <- sum(!is.na(ns_df$p.value))

    cat("\nComparisons with p < 0.10 (local inconsistency):",
        n_sig, "/", n_total, "\n")

    if (n_sig == 0) {
      cat("→ No significant direct-indirect discrepancies.\n")
      cat("  Transitivity assumption appears supported by evidence.\n")
    } else if (n_sig / n_total < 0.20) {
      cat("→ Few discrepancies detected. Investigate specific comparisons.\n")
    } else {
      cat("→ Multiple discrepancies. Transitivity may be violated.\n")
      cat("  Consider meta-regression to identify the effect modifier.\n")
    }
  }
} else {
  cat("Node-splitting results not available or insufficient for comparison.\n")
}

# =============================================================================
# SECTION D: TRANSITIVITY ASSESSMENT SUMMARY
# =============================================================================

cat("\n=== Transitivity Assessment Summary ===\n")

# Compile all results into a traffic light table
traffic_light <- data.frame(
  Modifier   = character(),
  Test       = character(),
  p_value    = numeric(),
  Concern    = character(),
  stringsAsFactors = FALSE
)

for (res in continuous_results) {
  traffic_light <- rbind(traffic_light, data.frame(
    Modifier = res$modifier,
    Test     = "Kruskal-Wallis",
    p_value  = res$p_value,
    Concern  = res$concern,
    stringsAsFactors = FALSE
  ))
}

for (res in categorical_results) {
  traffic_light <- rbind(traffic_light, data.frame(
    Modifier = res$modifier,
    Test     = res$test,
    p_value  = res$p_value,
    Concern  = res$concern,
    stringsAsFactors = FALSE
  ))
}

if (nrow(traffic_light) > 0) {
  cat("\n--- Traffic Light Table ---\n")
  cat("Green (Low): p >= 0.10 — modifier balanced across comparisons\n")
  cat("Yellow (Moderate): 0.01 <= p < 0.10 — some imbalance\n")
  cat("Red (High): p < 0.01 — significant imbalance, transitivity concern\n\n")

  traffic_light$p_value <- format.pval(traffic_light$p_value, digits = 4)
  print(traffic_light)

  write_csv(traffic_light, file.path(TBL_DIR, "transitivity_tests.csv"))
  cat("\nTraffic light table saved to",
      file.path(TBL_DIR, "transitivity_tests.csv"), "\n")

  # Heatmap visualization (if ggplot2 available)
  if (nrow(traffic_light) >= 2) {
    traffic_light_plot <- traffic_light
    traffic_light_plot$p_numeric <- as.numeric(traffic_light_plot$p_value)

    png(file.path(FIG_DIR, "transitivity_heatmap.png"),
        width = FIG_WIDTH, height = max(4, nrow(traffic_light_plot) * 0.8),
        units = "in", res = FIG_DPI)

    p <- ggplot(traffic_light_plot, aes(x = "Balance", y = Modifier)) +
      geom_tile(aes(fill = Concern), color = "white", linewidth = 1) +
      geom_text(aes(label = p_value), size = 4) +
      scale_fill_manual(
        values = c("Low" = "#4CAF50", "Moderate" = "#FFC107", "High" = "#F44336"),
        name   = "Concern Level"
      ) +
      theme_minimal() +
      labs(
        title = "Transitivity Assessment: Effect Modifier Balance",
        subtitle = "p-values for distribution across network comparisons",
        x = NULL, y = NULL
      ) +
      theme(axis.text.x = element_blank(),
            panel.grid = element_blank())

    print(p)
    dev.off()
    cat("Heatmap saved to", file.path(FIG_DIR, "transitivity_heatmap.png"), "\n")
  }

  # Overall assessment
  n_high <- sum(traffic_light$Concern == "High")
  n_mod  <- sum(traffic_light$Concern == "Moderate")

  cat("\n--- Overall Transitivity Assessment ---\n")
  cat("High concern modifiers:", n_high, "\n")
  cat("Moderate concern modifiers:", n_mod, "\n")

  if (n_high == 0 && n_mod == 0) {
    cat("→ All modifiers balanced. Statistical evidence supports transitivity.\n")
  } else if (n_high == 0) {
    cat("→ Some imbalance detected. Clinical assessment should confirm.\n")
  } else {
    cat("→ Significant imbalance detected. Transitivity may be violated.\n")
    cat("  Consider sensitivity analysis excluding problematic comparisons.\n")
    cat("  Downgrade GRADE certainty for affected comparisons.\n")
  }

} else {
  cat("No effect modifiers specified for testing.\n")
  cat("Adapt continuous_modifiers and categorical_modifiers at the top of this script.\n")
  cat("Even without statistical tests, complete the clinical transitivity table\n")
  cat("in nma-assumptions.md (study characteristics by comparison).\n")
}

# --- Save comprehensive report ---
sink("transitivity_assessment_report.txt")
cat("================================================\n")
cat("TRANSITIVITY ASSESSMENT REPORT\n")
cat("================================================\n\n")

cat("NOTE: Statistical transitivity tests are SUPPLEMENTARY.\n")
cat("Transitivity remains primarily a clinical judgment.\n")
cat("See nma-assumptions.md for the clinical assessment table.\n\n")

if (nrow(traffic_light) > 0) {
  cat("--- Effect Modifier Balance (Traffic Light) ---\n")
  print(traffic_light)
}

if (length(regression_proxy_results) > 0) {
  cat("\n--- Meta-Regression Proxy ---\n")
  for (res in regression_proxy_results) {
    cat(res$modifier, ": tau² change =", round(res$tau2_change_pct, 1), "%\n")
  }
}

cat("\n--- Direct vs NMA Comparison ---\n")
if (exists("ns_df") && nrow(ns_df) > 0) {
  cat("Comparisons with local inconsistency (p < 0.10):", n_sig, "/", n_total, "\n")
}

cat("\n--- Interpretation ---\n")
cat("Combine these statistical results with the clinical transitivity\n")
cat("assessment table (study characteristics by comparison) for a\n")
cat("comprehensive evaluation of the transitivity assumption.\n")
sink()

cat("\nTransitivity assessment report saved to transitivity_assessment_report.txt\n")
