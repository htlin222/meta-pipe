# =============================================================================
# nma_08_league_table.R — League Table + Heatmap
# =============================================================================

source("nma_04_models.R")

library(gt)

# --- 1. League table ---
ranking <- netrank(net_re, small.values = "desirable")
league <- netleague(net_re, random = TRUE, seq = ranking, digits = 2)

league_df <- as.data.frame(league$random)
write_csv(league_df, file.path(TBL_DIR, "nma_league_table.csv"))

# --- 2. League table heatmap ---
treat_order <- names(sort(ranking$Pscore.random, decreasing = TRUE))
n_treats <- length(treat_order)
league_matrix <- league$random

heatmap_rows <- list()
for (i in seq_len(n_treats)) {
  for (j in seq_len(n_treats)) {
    if (i == j) next
    cell_text <- league_matrix[i, j]
    if (is.na(cell_text) || cell_text == "") next

    m <- regmatches(cell_text, regexec(
      "([0-9.-]+)\\s*[\\[\\(]([0-9.-]+)[,;]\\s*([0-9.-]+)[\\]\\)]", cell_text
    ))[[1]]

    if (length(m) == 4) {
      est <- as.numeric(m[2])
      lo  <- as.numeric(m[3])
      hi  <- as.numeric(m[4])
      sig <- (lo > 1) || (hi < 1)

      heatmap_rows[[length(heatmap_rows) + 1]] <- data.frame(
        row_treat = rownames(league_matrix)[i],
        col_treat = colnames(league_matrix)[j],
        estimate = est, lower = lo, upper = hi, sig = sig,
        label = trimws(cell_text), stringsAsFactors = FALSE
      )
    }
  }
}

if (length(heatmap_rows) > 0) {
  heatmap_df <- do.call(rbind, heatmap_rows)
  heatmap_df$row_treat <- factor(heatmap_df$row_treat, levels = treat_order)
  heatmap_df$col_treat <- factor(heatmap_df$col_treat, levels = treat_order)
  heatmap_df$fill_val <- log(heatmap_df$estimate)
  fill_limit <- max(abs(heatmap_df$fill_val), na.rm = TRUE)

  p_heatmap <- ggplot(heatmap_df, aes(x = col_treat, y = row_treat)) +
    geom_tile(aes(fill = fill_val), color = "white", linewidth = 0.8) +
    geom_text(aes(label = label, fontface = ifelse(sig, "bold", "plain")),
              size = 2.8, color = "black") +
    scale_fill_gradient2(low = "#2166AC", mid = "white", high = "#B2182B",
                         midpoint = 0, limits = c(-fill_limit, fill_limit),
                         name = "log(HR)") +
    scale_x_discrete(position = "top") +
    labs(title = "League Table — Frontline DLBCL NMA (PFS)",
         subtitle = "HR (95% CI). Bold = significant. Blue favours row, Red favours column.",
         x = NULL, y = NULL) +
    theme_minimal(base_size = 12) +
    theme(axis.text.x = element_text(angle = 45, hjust = 0, face = "bold"),
          axis.text.y = element_text(face = "bold"),
          panel.grid = element_blank())

  fig_size <- max(8, n_treats * 1.4)
  ggsave(file.path(TBL_DIR, "league_table_heatmap.png"), p_heatmap,
         width = fig_size, height = fig_size * 0.85, dpi = FIG_DPI, bg = "white")
  cat("League table heatmap saved.\n")
}

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
