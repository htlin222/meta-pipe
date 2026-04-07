library(meta)
library(metafor)

# Expect objects cont_es or bin_es from 02_effect_sizes.R
# Expect pooling_advisory from 02a_pre_pool_diagnostics.R (optional)
#
# Defaults: REML + Hartung-Knapp (Cochrane mandate, July 2025)
#   method.tau = "REML"  -> replaces DerSimonian-Laird for tau² estimation
#   hakn = TRUE          -> Hartung-Knapp-Sidik-Jonkman adjustment for CIs/p-values
#   test = "knha"        -> metafor equivalent of hakn = TRUE

# ---------------------------------------------------------------------------
# Helper: print advisory-aware model summary
# ---------------------------------------------------------------------------
.print_model_summary <- function(model, pred, advisory_level, label) {
  cat(sprintf("\n--- %s ---\n", label))

  if (!is.null(advisory_level) && advisory_level == "RED") {
    cat("*** ADVISORY: RED — interpret this pooled estimate with extreme caution ***\n")
    cat("*** Consider narrative synthesis; see 02a_diagnostics_report.md ***\n\n")
  } else if (!is.null(advisory_level) && advisory_level == "YELLOW") {
    cat("* ADVISORY: YELLOW — interpret alongside prediction interval & sensitivity analyses *\n\n")
  }

  cat(sprintf("Pooled estimate (%s): %.4f\n", model$sm, model$TE.random))
  cat(sprintf("  95%% CI: [%.4f, %.4f]\n", model$lower.random, model$upper.random))
  cat(sprintf("  p-value: %.4f\n", model$pval.random))

  # Always show prediction interval (Riley et al. 2011)
  if (!is.null(pred) && !is.na(pred$pi.lb)) {
    cat(sprintf("  95%% Prediction Interval: [%.4f, %.4f]\n", pred$pi.lb, pred$pi.ub))
    if (sign(pred$pi.lb) != sign(pred$pi.ub)) {
      cat("  ^ Prediction interval crosses null: effect direction uncertain in future settings\n")
    }
  }

  cat(sprintf("  I² = %.1f%%, tau² = %.4f, k = %d\n", model$I2, model$tau2, model$k))
  cat("\n")
}

# ---------------------------------------------------------------------------
# Determine advisory levels per outcome type
# ---------------------------------------------------------------------------
.get_advisory_level <- function(outcome_type) {
  if (!exists("pooling_advisory")) return(NULL)
  adv <- pooling_advisory[[outcome_type]]
  if (!is.null(adv)) adv$level else NULL
}

# ---------------------------------------------------------------------------
# Continuous outcomes
# ---------------------------------------------------------------------------
if (exists("cont_es")) {
  cont_model <- metagen(
    TE = cont_es$yi,
    seTE = sqrt(cont_es$vi),
    studlab = cont_es$slab,
    sm = "SMD",
    method.tau = "REML",
    hakn = TRUE,
    prediction = TRUE
  )

  cont_rma <- rma(yi = cont_es$yi, vi = cont_es$vi, method = "REML", test = "knha")
  cont_pred <- predict(cont_rma)

  .print_model_summary(
    cont_model, cont_pred,
    .get_advisory_level("continuous"),
    "Continuous outcomes (SMD)"
  )
}

# ---------------------------------------------------------------------------
# Binary outcomes
# ---------------------------------------------------------------------------
if (exists("bin_es")) {
  bin_model <- metagen(
    TE = bin_es$yi,
    seTE = sqrt(bin_es$vi),
    studlab = bin_es$slab,
    sm = "RR",
    method.tau = "REML",
    hakn = TRUE,
    prediction = TRUE
  )

  bin_rma <- rma(yi = bin_es$yi, vi = bin_es$vi, method = "REML", test = "knha")
  bin_pred <- predict(bin_rma)

  .print_model_summary(
    bin_model, bin_pred,
    .get_advisory_level("binary"),
    "Binary outcomes (RR)"
  )
}

# ---------------------------------------------------------------------------
# Save model caveats for downstream scripts (plots, tables, manuscript)
# ---------------------------------------------------------------------------
model_caveats <- character()
if (exists("pooling_advisory")) {
  if (pooling_advisory$overall == "RED") {
    model_caveats <- c(model_caveats,
      "PRE-POOLING ADVISORY: RED — substantial concerns identified.",
      "The pooled estimate may be misleading due to high heterogeneity,",
      "inconsistent effect directions, or insufficient studies.",
      "See 02a_diagnostics_report.md for details.",
      "Consider narrative synthesis as an alternative to pooling."
    )
  } else if (pooling_advisory$overall == "YELLOW") {
    model_caveats <- c(model_caveats,
      "PRE-POOLING ADVISORY: YELLOW — moderate concerns identified.",
      "Interpret pooled estimate alongside prediction intervals",
      "and sensitivity analyses. See 02a_diagnostics_report.md."
    )
  }
}
