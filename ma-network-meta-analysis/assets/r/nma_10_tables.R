# =============================================================================
# nma_10_tables.R — Export League Tables & Rankings as Publication Tables
# =============================================================================
# Purpose: League tables (Bayesian PRIMARY + frequentist SUPPLEMENT), colour-coded
#          league-table heatmaps, and a summary table vs reference
# Input:   bayes_re + net_re from nma_04_models.R;
#          NMA_SM / NMA_SMALL_VALUES from nma_01_setup.R
# Output:  tables/nma_league_table_bayesian.csv       posterior median [95% CrI]
#          tables/nma_league_table_frequentist.csv    REML estimate [95% CI]
#          tables/nma_league_table_netleague.csv/.xlsx raw netmeta::netleague() output
#          tables/league_table_heatmap.png            primary (Bayesian if available)
#          tables/league_table_heatmap_frequentist.png
#          tables/nma_summary.png / nma_summary.csv
#
# ORIENTATION — read before interpreting any league table:
#   * Tables and heatmaps built by THIS script: every cell = ROW treatment vs
#     COLUMN treatment, network estimate. Both triangles are filled (reciprocal).
#   * netmeta::netleague() output (the *_netleague.* files) is different:
#     LOWER triangle = network estimate (column vs row),
#     UPPER triangle = DIRECT pairwise estimate (row vs column).
#     Never colour-code that matrix as if both triangles were the same thing.
#   * gemtc::relative.effect.table()[t1, t2, ] = effect of t2 relative to t1
#     (column vs row); it is transposed below to match the row-vs-column rule.
# =============================================================================

source("nma_04_models.R")

library(gt)
library(flextable)
library(ggplot2)
library(tidyr)

is_ratio <- NMA_SM %in% c("RR", "OR", "HR")
null_val <- if (is_ratio) 1 else 0
has_bayes <- exists("bayes_re")

# --- 0. Helpers -------------------------------------------------------------

# Long-format league data from square effect matrices on the analysis scale
# (log scale for ratio measures). est/lower/upper[i, j] = treatment i vs j.
# fill_val is signed so that NEGATIVE always means "favours row".
league_long <- function(est, lower, upper, trts, treat_order, digits = 2) {
  fmt <- paste0("%.", digits, "f")
  rows <- list()
  for (a in treat_order) for (b in treat_order) {
    if (a == b) next
    i <- match(a, trts); j <- match(b, trts)
    e <- est[i, j]; lo <- lower[i, j]; hi <- upper[i, j]
    if (is.na(e)) next
    if (is_ratio) { e <- exp(e); lo <- exp(lo); hi <- exp(hi) }
    signed <- if (is_ratio) log(e) else e          # < 0: row has lower values
    rows[[length(rows) + 1]] <- data.frame(
      row_treat = a, col_treat = b,
      estimate = e, lower = lo, upper = hi,
      sig      = (lo > null_val) || (hi < null_val),
      label    = sprintf(paste0(fmt, " [", fmt, "; ", fmt, "]"), e, lo, hi),
      fill_val = if (NMA_SMALL_VALUES == "desirable") signed else -signed,
      stringsAsFactors = FALSE
    )
  }
  out <- do.call(rbind, rows)
  out$row_treat <- factor(out$row_treat, levels = treat_order)
  out$col_treat <- factor(out$col_treat, levels = treat_order)
  out
}

# Square character matrix (row vs column) for CSV export
league_wide <- function(long_df, treat_order) {
  m <- matrix("", length(treat_order), length(treat_order),
              dimnames = list(treat_order, treat_order))
  diag(m) <- treat_order
  for (k in seq_len(nrow(long_df))) {
    m[as.character(long_df$row_treat[k]), as.character(long_df$col_treat[k])] <- long_df$label[k]
  }
  cbind(data.frame(Treatment = treat_order, stringsAsFactors = FALSE),
        as.data.frame(m, stringsAsFactors = FALSE))
}

league_heatmap <- function(long_df, title, estimate_label, interval_label, file) {
  n_treats   <- nlevels(long_df$row_treat)
  fill_limit <- max(abs(long_df$fill_val), na.rm = TRUE)
  cell_font  <- if (n_treats <= 5) 3.2 else if (n_treats <= 8) 2.8 else 2.2
  p <- ggplot(long_df, aes(x = col_treat, y = row_treat)) +
    geom_tile(aes(fill = fill_val), color = "white", linewidth = 0.8) +
    geom_text(aes(label = label, fontface = ifelse(sig, "bold", "plain")),
              size = cell_font, color = "black") +
    scale_fill_gradient2(
      low = "#2166AC", mid = "white", high = "#B2182B",
      midpoint = 0, limits = c(-fill_limit, fill_limit),
      name = NULL, breaks = c(-fill_limit, fill_limit),
      labels = c("Favours row", "Favours column")
    ) +
    scale_x_discrete(position = "top") +
    scale_y_discrete(limits = rev) +          # best treatment on top
    labs(
      title = title,
      subtitle = paste0(
        "Each cell = row vs column: ", estimate_label, " ", NMA_SM,
        " [95% ", interval_label, "]. Bold = interval excludes ", null_val, ".\n",
        "Treatments ordered best to worst."
      ),
      x = NULL, y = NULL
    ) +
    theme_minimal(base_size = 12) +
    theme(
      axis.text.x.top = element_text(angle = 45, hjust = 0, vjust = 0, face = "bold"),
      axis.text.y   = element_text(face = "bold"),
      panel.grid    = element_blank(),
      plot.title    = element_text(face = "bold", size = 14),
      plot.subtitle = element_text(size = 9, color = "grey40", margin = margin(b = 4 * max(nchar(levels(long_df$row_treat))))),
      legend.position = "right"
    )
  fig_size <- max(6, n_treats * 1.4)
  ggsave(file.path(TBL_DIR, file), plot = p,
         width = fig_size, height = fig_size * 0.85, dpi = FIG_DPI, bg = "white")
  cat("Heatmap saved to", file.path(TBL_DIR, file), "\n")
  invisible(p)
}

# --- 1. Treatment order (best -> worst) ---
ranking <- netrank(net_re, small.values = NMA_SMALL_VALUES)
if (has_bayes) {
  pref_dir    <- if (NMA_SMALL_VALUES == "desirable") -1 else 1
  sucra_vals  <- sucra(rank.probability(bayes_re, preferredDirection = pref_dir))
  treat_order <- names(sort(sucra_vals, decreasing = TRUE))     # by SUCRA (primary)
} else {
  treat_order <- names(sort(ranking$Pscore.random, decreasing = TRUE))  # by P-score
}

# --- 1a. Bayesian league table (PRIMARY) ---
if (has_bayes) {
  cat("Building Bayesian league table (posterior median + 95% CrI)...\n")
  ret <- relative.effect.table(bayes_re)          # [t1, t2, ] = t2 relative to t1
  league_b <- league_long(
    est = t(ret[, , "50%"]), lower = t(ret[, , "2.5%"]), upper = t(ret[, , "97.5%"]),
    trts = dimnames(ret)[[1]], treat_order = treat_order
  )
  write_csv(league_wide(league_b, treat_order),
            file.path(TBL_DIR, "nma_league_table_bayesian.csv"))
  league_heatmap(league_b, "League Table (Bayesian NMA)",
                 "posterior median", "CrI", "league_table_heatmap.png")
} else {
  cat("bayes_re not found — Bayesian league table skipped.\n")
}

# --- 1b. Frequentist league table (SUPPLEMENT) ---
cat("Building frequentist league table (REML, 95% CI)...\n")
league_f <- league_long(
  est = net_re$TE.random, lower = net_re$lower.random, upper = net_re$upper.random,
  trts = net_re$trts, treat_order = treat_order
)
write_csv(league_wide(league_f, treat_order),
          file.path(TBL_DIR, "nma_league_table_frequentist.csv"))
league_heatmap(league_f, "League Table (Frequentist NMA, sensitivity)",
               "REML estimate", "CI",
               if (has_bayes) "league_table_heatmap_frequentist.png" else "league_table_heatmap.png")

# Raw netmeta::netleague() — lower = network (column vs row), upper = DIRECT (row vs column)
league_nm <- netleague(net_re, random = TRUE, common = FALSE, seq = ranking, digits = 2)
write_csv(as.data.frame(league_nm$random),
          file.path(TBL_DIR, "nma_league_table_netleague.csv"))
if (requireNamespace("writexl", quietly = TRUE)) {
  tryCatch(
    netleague(net_re, random = TRUE, common = FALSE, seq = ranking, digits = 2,
              path = file.path(TBL_DIR, "nma_league_table_netleague.xlsx"), overwrite = TRUE),
    error = function(e) cat("netleague Excel export skipped:", conditionMessage(e), "\n")
  )
}

# --- 2. Summary table: all treatments vs reference ---
ref_treat <- net_re$reference.group
if (is.null(ref_treat)) {
  ref_treat <- sort(net_re$trts)[1]
}

# Extract pairwise estimates vs reference
treatments <- sort(net_re$trts)
treatments <- treatments[treatments != ref_treat]

summary_data <- data.frame(
  Treatment = treatments,
  stringsAsFactors = FALSE
)

for (i in seq_along(treatments)) {
  idx <- which(net_re$trts == treatments[i])
  ref_idx <- which(net_re$trts == ref_treat)

  # Random-effects estimates
  te <- net_re$TE.random[idx, ref_idx]
  lower <- net_re$lower.random[idx, ref_idx]
  upper <- net_re$upper.random[idx, ref_idx]

  if (is_ratio) {
    summary_data$Estimate[i] <- sprintf("%.2f (%.2f-%.2f)", exp(te), exp(lower), exp(upper))
  } else {
    summary_data$Estimate[i] <- sprintf("%.2f (%.2f-%.2f)", te, lower, upper)
  }
}

# Add P-scores
pscore <- ranking$Pscore.random
summary_data$P_score <- sapply(treatments, function(t) round(pscore[t], 3))
summary_data$Rank <- rank(-summary_data$P_score)

# Sort by rank
summary_data <- summary_data[order(summary_data$Rank), ]

cat("\n--- NMA Summary Table ---\n")
print(summary_data)

# --- 3. Export as gt table (PNG) ---
summary_gt <- summary_data %>%
  gt() %>%
  tab_header(
    title = "Network Meta-Analysis Summary",
    subtitle = paste("All treatments vs", ref_treat, "(random-effects model)")
  ) %>%
  cols_label(
    Treatment = "Treatment",
    Estimate  = paste0(net_re$sm, " (95% CI)"),
    P_score   = "P-score",
    Rank      = "Rank"
  ) %>%
  tab_style(
    style = cell_fill(color = "#e8f4f8"),
    locations = cells_body(rows = Rank == 1)
  ) %>%
  tab_footnote(
    footnote = paste("Random-effects model (REML). Effect measure:", net_re$sm),
    locations = cells_column_labels(columns = Estimate)
  ) %>%
  tab_footnote(
    footnote = "P-score: probability of being the best treatment (0-1)",
    locations = cells_column_labels(columns = P_score)
  )

gtsave(summary_gt, file.path(TBL_DIR, "nma_summary.png"), expand = 10)
cat("Summary table saved to", file.path(TBL_DIR, "nma_summary.png"), "\n")

# --- 4. Export as flextable (DOCX-compatible) ---
summary_ft <- flextable(summary_data) %>%
  set_header_labels(
    Treatment = "Treatment",
    Estimate  = paste0(net_re$sm, " (95% CI)"),
    P_score   = "P-score",
    Rank      = "Rank"
  ) %>%
  theme_vanilla() %>%
  autofit()

save_as_image(summary_ft, file.path(TBL_DIR, "nma_summary_ft.png"), res = FIG_DPI)
cat("Flextable version saved to", file.path(TBL_DIR, "nma_summary_ft.png"), "\n")

# --- 5. Save all tables as CSV ---
write_csv(summary_data, file.path(TBL_DIR, "nma_summary.csv"))
cat("\nAll NMA tables exported to", TBL_DIR, "\n")
