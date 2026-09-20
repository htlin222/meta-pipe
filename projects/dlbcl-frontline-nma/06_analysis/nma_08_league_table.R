# =============================================================================
# nma_08_league_table.R — League Table + Heatmap
# =============================================================================

source("nma_04_models.R")

library(gt)

# Analysis settings (HR for PFS: lower = better)
NMA_SM           <- "HR"
NMA_SMALL_VALUES <- "desirable"
is_ratio <- TRUE
null_val <- 1

# ORIENTATION: every cell built here = ROW treatment vs COLUMN treatment
# (network estimate, both triangles filled). This differs from
# netmeta::netleague(), whose lower triangle = network (column vs row) and
# upper triangle = DIRECT estimates (row vs column) — do not colour-code that.

# --- 0. Helpers (same as framework nma_10_tables.R) ---
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
  p <- ggplot(long_df, aes(x = col_treat, y = row_treat)) +
    geom_tile(aes(fill = fill_val), color = "white", linewidth = 0.8) +
    geom_text(aes(label = label, fontface = ifelse(sig, "bold", "plain")),
              size = 2.8, color = "black") +
    scale_fill_gradient2(low = "#2166AC", mid = "white", high = "#B2182B",
                         midpoint = 0, limits = c(-fill_limit, fill_limit),
                         name = NULL, breaks = c(-fill_limit, fill_limit),
                         labels = c("Favours row", "Favours column")) +
    scale_x_discrete(position = "top") +
    scale_y_discrete(limits = rev) +          # best treatment on top
    labs(title = title,
         subtitle = paste0("Each cell = row vs column: ", estimate_label, " HR [95% ",
                           interval_label, "]. Bold = interval excludes 1.\n",
                           "Treatments ordered best to worst."),
         x = NULL, y = NULL) +
    theme_minimal(base_size = 12) +
    theme(axis.text.x.top = element_text(angle = 45, hjust = 0, vjust = 0, face = "bold"),
          axis.text.y = element_text(face = "bold"),
          panel.grid = element_blank(),
          plot.subtitle = element_text(size = 9, color = "grey40", margin = margin(b = 4 * max(nchar(levels(long_df$row_treat))))))
  fig_size <- max(8, n_treats * 1.4)
  ggsave(file.path(TBL_DIR, file), p, width = fig_size, height = fig_size * 0.85,
         dpi = FIG_DPI, bg = "white")
  cat("Heatmap saved to", file.path(TBL_DIR, file), "\n")
  invisible(p)
}

# --- 1. Treatment order (best -> worst, by SUCRA) ---
ranking     <- netrank(net_re, small.values = NMA_SMALL_VALUES)
sucra_vals  <- sucra(rank.probability(bayes_re, preferredDirection = -1))
treat_order <- names(sort(sucra_vals, decreasing = TRUE))

# --- 2a. Bayesian league table (PRIMARY) ---
ret <- relative.effect.table(bayes_re)            # [t1, t2, ] = t2 relative to t1
league_b <- league_long(t(ret[, , "50%"]), t(ret[, , "2.5%"]), t(ret[, , "97.5%"]),
                        dimnames(ret)[[1]], treat_order)
write_csv(league_wide(league_b, treat_order), file.path(TBL_DIR, "nma_league_table_bayesian.csv"))
league_heatmap(league_b, "League Table — Frontline DLBCL NMA (PFS, Bayesian)",
               "posterior median", "CrI", "league_table_heatmap.png")

# --- 2b. Frequentist league table (SUPPLEMENT) ---
league_f <- league_long(net_re$TE.random, net_re$lower.random, net_re$upper.random,
                        net_re$trts, treat_order)
write_csv(league_wide(league_f, treat_order), file.path(TBL_DIR, "nma_league_table_frequentist.csv"))
league_heatmap(league_f, "League Table — Frontline DLBCL NMA (PFS, frequentist sensitivity)",
               "REML estimate", "CI", "league_table_heatmap_frequentist.png")

# Raw netleague (lower = network, column vs row; upper = direct, row vs column)
league <- netleague(net_re, random = TRUE, common = FALSE, seq = ranking, digits = 2)
write_csv(as.data.frame(league$random), file.path(TBL_DIR, "nma_league_table_netleague.csv"))

# --- 3. Summary table vs R-CHOP ---
treatments <- sort(net_re$trts)
treatments <- treatments[treatments != "RCHOP"]

summary_data <- data.frame(Treatment = treatments, stringsAsFactors = FALSE)
for (i in seq_along(treatments)) {
  idx <- which(net_re$trts == treatments[i])
  ref_idx <- which(net_re$trts == "RCHOP")
  te <- net_re$TE.random[idx, ref_idx]
  lo <- net_re$lower.random[idx, ref_idx]
  hi <- net_re$upper.random[idx, ref_idx]
  summary_data$HR[i] <- sprintf("%.2f (%.2f-%.2f)", exp(te), exp(lo), exp(hi))
}
summary_data$P_score <- sapply(treatments, function(t) round(ranking$Pscore.random[t], 3))
summary_data$Rank <- rank(-summary_data$P_score)
summary_data <- summary_data[order(summary_data$Rank), ]

summary_gt <- summary_data %>%
  gt() %>%
  tab_header(title = "NMA Summary — Frontline DLBCL (PFS)",
             subtitle = "All treatments vs R-CHOP (random-effects)") %>%
  cols_label(HR = "HR (95% CI)", P_score = "P-score") %>%
  tab_style(style = cell_fill(color = "#e8f4f8"),
            locations = cells_body(rows = Rank == 1))

gtsave(summary_gt, file.path(TBL_DIR, "nma_summary.png"), expand = 10)
write_csv(summary_data, file.path(TBL_DIR, "nma_summary.csv"))
cat("All league tables generated.\n")
