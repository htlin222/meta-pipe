# ---------------------------------------------------------------------------
# 02a_pre_pool_diagnostics.R — Pre-pooling assumption checks
#
# Run AFTER 02_effect_sizes.R, BEFORE 03_models.R
#
# Produces a traffic-light advisory (GREEN / YELLOW / RED) based on:
#   1. Study count (k)
#   2. Heterogeneity (I², Q-test, tau²)
#   3. Prediction interval (does it cross null?)
#   4. Effect direction consistency
#   5. Outlier detection (studentized residuals)
#
# Outputs:
#   - pooling_advisory   (R list object for downstream scripts)
#   - 02a_diagnostics_report.md  (human-readable report)
#
# References:
#   - Cochrane Handbook §10.10 (when not to pool)
#   - Higgins & Thompson 2002 (I² interpretation)
#   - IntHout et al. 2016 (prediction intervals)
#   - Riley et al. 2011 (prediction intervals in MA)
# ---------------------------------------------------------------------------

library(metafor)

# Traffic-light level ordering for max() comparisons
.level_rank <- c(GREEN = 1L, YELLOW = 2L, RED = 3L)
.rank_to_level <- c("GREEN", "YELLOW", "RED")

.worse_level <- function(current, candidate) {
  .rank_to_level[max(.level_rank[current], .level_rank[candidate])]
}

# ---------------------------------------------------------------------------
# Core diagnostic function: assess one effect-size set
# ---------------------------------------------------------------------------
.assess_pooling <- function(es, label) {
  k <- nrow(es)
  report <- list(label = label, k = k, checks = list(), level = "GREEN")

  # --- Check 1: Minimum study count ---
  if (k < 2) {
    report$level <- "RED"
    report$checks$study_count <- list(
      k = k,
      flag = "Only 1 study — pooling is not possible; report the single study result directly"
    )
    return(report)
  }
  if (k == 2) {
    report$checks$study_count <- list(
      k = k,
      flag = "Only 2 studies — pooled estimate has very limited reliability; tau² is poorly estimated"
    )
    report$level <- .worse_level(report$level, "YELLOW")
  } else {
    report$checks$study_count <- list(k = k)
  }

  # --- Check 2: Fit preliminary RE model for diagnostics ---
  prelim <- tryCatch(
    rma(yi = es$yi, vi = es$vi, method = "REML"),
    error = function(e) NULL
  )
  if (is.null(prelim)) {
    report$level <- "RED"
    report$checks$model_fit <- list(
      flag = "Random-effects model failed to converge — check data quality"
    )
    return(report)
  }

  # --- Check 3: Heterogeneity ---
  i2 <- prelim$I2
  q_pval <- prelim$QEp
  tau2 <- prelim$tau2
  report$checks$heterogeneity <- list(I2 = i2, Q_pval = q_pval, tau2 = tau2)

  if (i2 > 75) {
    report$level <- .worse_level(report$level, "RED")
    report$checks$heterogeneity$flag <-
      "I\u00b2 > 75%: substantial heterogeneity — pooled estimate may be misleading; explore sources before interpreting"
  } else if (i2 > 50) {
    report$level <- .worse_level(report$level, "YELLOW")
    report$checks$heterogeneity$flag <-
      "I\u00b2 50-75%: moderate heterogeneity — interpret pooled estimate with caution, explore sources"
  }

  # --- Check 4: Prediction interval ---
  pred <- predict(prelim)
  pi_lower <- pred$pi.lb
  pi_upper <- pred$pi.ub
  report$checks$prediction_interval <- list(lower = pi_lower, upper = pi_upper)

  if (!is.na(pi_lower) && !is.na(pi_upper)) {
    if (sign(pi_lower) != sign(pi_upper)) {
      report$checks$prediction_interval$flag <-
        "Prediction interval crosses null — the true effect may vary in direction across settings"
      report$level <- .worse_level(report$level, "YELLOW")
    }
  } else {
    report$checks$prediction_interval$flag <-
      "Prediction interval could not be computed (k too small)"
  }

  # --- Check 5: Effect direction consistency ---
  n_pos <- sum(es$yi > 0)
  n_neg <- sum(es$yi < 0)
  n_zero <- sum(es$yi == 0)
  pct_agreement <- max(n_pos, n_neg) / k * 100
  report$checks$direction <- list(
    positive = n_pos, negative = n_neg, zero = n_zero,
    agreement_pct = pct_agreement
  )

  if (pct_agreement < 60) {
    report$level <- .worse_level(report$level, "RED")
    report$checks$direction$flag <-
      "< 60% effect direction agreement — studies may not be estimating the same underlying effect"
  } else if (pct_agreement < 75) {
    report$level <- .worse_level(report$level, "YELLOW")
    report$checks$direction$flag <-
      "< 75% direction agreement — consider subgroup analysis before interpreting pooled estimate"
  }

  # --- Check 6: Outlier detection (externally studentized residuals) ---
  if (k >= 3) {
    rstud <- tryCatch(rstudent(prelim), error = function(e) NULL)
    if (!is.null(rstud)) {
      outlier_idx <- which(abs(rstud$z) > 2)
      if (length(outlier_idx) > 0) {
        report$checks$outliers <- list(
          studies = as.character(es$slab[outlier_idx]),
          flag = sprintf(
            "%d potential outlier(s) detected (|z| > 2) — run sensitivity analysis excluding: %s",
            length(outlier_idx),
            paste(es$slab[outlier_idx], collapse = ", ")
          )
        )
        report$level <- .worse_level(report$level, "YELLOW")
      } else {
        report$checks$outliers <- list(studies = character(0))
      }
    }
  }

  report
}

# ---------------------------------------------------------------------------
# Run diagnostics
# ---------------------------------------------------------------------------
pooling_advisory <- list()

if (exists("cont_es") && nrow(cont_es) > 0) {
  pooling_advisory$continuous <- .assess_pooling(cont_es, "Continuous outcomes")
}
if (exists("bin_es") && nrow(bin_es) > 0) {
  pooling_advisory$binary <- .assess_pooling(bin_es, "Binary outcomes")
}

# Overall advisory = worst level across all outcome types
overall_level <- "GREEN"
for (adv in pooling_advisory) {
  overall_level <- .worse_level(overall_level, adv$level)
}
pooling_advisory$overall <- overall_level

# ---------------------------------------------------------------------------
# Generate markdown diagnostic report
# ---------------------------------------------------------------------------
.write_diagnostic_report <- function(advisory) {
  lines <- character()
  .add <- function(...) lines <<- c(lines, ...)

  .add("# Pre-Pooling Diagnostic Report", "")
  .add(sprintf("**Overall Advisory: %s**", advisory$overall), "")

  level_meaning <- c(
    GREEN  = "All assumptions reasonably met. Proceed with pooling.",
    YELLOW = paste(
      "Some concerns identified. Proceed with caution;",
      "interpret pooled estimate alongside prediction intervals",
      "and sensitivity analyses."
    ),
    RED    = paste(
      "Major concerns. Pooled estimate may be misleading.",
      "Consider narrative synthesis, or investigate and address",
      "heterogeneity sources before relying on pooled results."
    )
  )
  .add(sprintf("> %s", level_meaning[advisory$overall]), "")

  for (name in setdiff(names(advisory), "overall")) {
    adv <- advisory[[name]]
    .add(sprintf("## %s (k = %d) \u2014 %s", adv$label, adv$k, adv$level), "")

    for (check_name in names(adv$checks)) {
      check <- adv$checks[[check_name]]
      if (is.list(check)) {
        if (!is.null(check$flag)) {
          .add(sprintf("- **%s**: %s", check_name, check$flag))
        }
        for (metric in setdiff(names(check), c("flag", "studies"))) {
          val <- check[[metric]]
          if (is.numeric(val) && length(val) == 1) {
            .add(sprintf("  - %s = %.2f", metric, val))
          }
        }
        if (!is.null(check$studies) && length(check$studies) > 0) {
          .add(sprintf("  - studies: %s", paste(check$studies, collapse = ", ")))
        }
      } else {
        .add(sprintf("- **%s**: %s", check_name, check))
      }
    }
    .add("")
  }

  .add("---")
  .add("*Generated by `02a_pre_pool_diagnostics.R`*")
  .add(sprintf("*Date: %s*", Sys.time()))

  writeLines(lines, "02a_diagnostics_report.md")
}

.write_diagnostic_report(pooling_advisory)

# ---------------------------------------------------------------------------
# Console summary
# ---------------------------------------------------------------------------
cat("\n===== PRE-POOLING DIAGNOSTICS =====\n")
cat(sprintf("Overall advisory: %s\n", pooling_advisory$overall))
for (name in setdiff(names(pooling_advisory), "overall")) {
  adv <- pooling_advisory[[name]]
  cat(sprintf("  %s (k=%d): %s\n", adv$label, adv$k, adv$level))
  for (check_name in names(adv$checks)) {
    check <- adv$checks[[check_name]]
    if (is.list(check) && !is.null(check$flag)) {
      cat(sprintf("    - %s\n", check$flag))
    } else if (is.character(check)) {
      cat(sprintf("    - %s\n", check))
    }
  }
}
if (pooling_advisory$overall == "RED") {
  cat("\n  *** WARNING: Consider narrative synthesis instead of pooling ***\n")
}
cat("Report saved to: 02a_diagnostics_report.md\n")
cat("====================================\n\n")
