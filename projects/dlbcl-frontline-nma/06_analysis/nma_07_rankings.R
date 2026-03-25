# =============================================================================
# nma_07_rankings.R — SUCRA Rankings + Rankograms
# =============================================================================

source("nma_04_models.R")

# =============================================================================
# BAYESIAN RANKINGS (PRIMARY)
# =============================================================================

cat("=== SUCRA Rankings (Bayesian) ===\n")

# For HR, lower is better (smaller HR = better PFS)
ranks <- rank.probability(bayes_re, preferredDirection = -1)
cat("Rank probability matrix:\n")
print(ranks)

sucra_vals <- sucra(ranks)
cat("\nSUCRA values:\n")
print(sucra_vals)

rank_df <- data.frame(
  Treatment = names(sucra_vals),
  SUCRA     = round(as.numeric(sucra_vals), 4)
) %>%
  arrange(desc(SUCRA)) %>%
  mutate(Rank = row_number())

cat("\n--- Rankings ---\n")
print(rank_df)
write_csv(rank_df, file.path(TBL_DIR, "nma_rankings.csv"))

# --- Rankogram ---
ranks_matrix <- as.matrix(ranks)
ranks_long <- data.frame(
  Treatment = rep(rownames(ranks_matrix), each = ncol(ranks_matrix)),
  Rank = rep(seq_len(ncol(ranks_matrix)), nrow(ranks_matrix)),
  Probability = as.vector(t(ranks_matrix))
)

p_rankogram <- ggplot(ranks_long, aes(x = Rank, y = Probability, fill = Treatment)) +
  geom_col(position = "dodge", alpha = 0.8) +
  facet_wrap(~Treatment, scales = "free_y") +
  scale_x_continuous(breaks = seq_len(nrow(ranks_matrix))) +
  scale_y_continuous(limits = c(0, 1)) +
  labs(title = "Rankograms — Frontline DLBCL Regimens (PFS)",
       subtitle = "Posterior rank probabilities (Bayesian NMA)",
       x = "Rank (1 = best PFS)", y = "Probability") +
  theme_minimal(base_size = 11) +
  theme(legend.position = "none", strip.text = element_text(face = "bold"))

ggsave(file.path(FIG_DIR, "nma_rankogram.png"), p_rankogram,
       width = 14, height = 10, dpi = FIG_DPI)

# --- SUCRA bar plot ---
p_sucra <- ggplot(rank_df, aes(x = reorder(Treatment, SUCRA), y = SUCRA)) +
  geom_col(fill = "steelblue", alpha = 0.8) +
  geom_text(aes(label = sprintf("%.1f%%", SUCRA * 100)), hjust = -0.1, size = 4) +
  coord_flip() +
  scale_y_continuous(limits = c(0, 1.15), labels = scales::percent_format(1)) +
  labs(title = "Treatment Ranking — Frontline DLBCL (PFS)",
       subtitle = "SUCRA from Bayesian NMA",
       x = NULL, y = "SUCRA") +
  theme_minimal(base_size = 12) +
  theme(panel.grid.major.y = element_blank())

ggsave(file.path(FIG_DIR, "nma_sucra_plot.png"), p_sucra,
       width = 10, height = 6, dpi = FIG_DPI)

# =============================================================================
# FREQUENTIST RANKINGS (SENSITIVITY)
# =============================================================================

cat("\n=== P-scores (Frequentist) ===\n")
pscore_ranking <- netrank(net_re, small.values = "desirable")

comparison_df <- data.frame(
  Treatment = names(pscore_ranking$Pscore.random),
  P_score   = round(pscore_ranking$Pscore.random, 4)
) %>%
  merge(rank_df[, c("Treatment", "SUCRA")], by = "Treatment") %>%
  arrange(desc(SUCRA))

cat("\n--- SUCRA vs P-score ---\n")
print(comparison_df)
write_csv(comparison_df, file.path(TBL_DIR, "nma_ranking_comparison.csv"))

# --- Rankings as gt table ---
rank_gt <- rank_df %>%
  gt() %>%
  tab_header(
    title = "Treatment Rankings — Frontline DLBCL (PFS)",
    subtitle = "SUCRA from Bayesian NMA (gemtc)"
  ) %>%
  fmt_number(columns = SUCRA, decimals = 3) %>%
  tab_style(style = cell_fill(color = "#e8f4f8"),
            locations = cells_body(rows = Rank == 1)) %>%
  tab_footnote("SUCRA: 0 = worst, 1 = best. Lower HR = better PFS.",
               locations = cells_column_labels(columns = SUCRA))

gtsave(rank_gt, file.path(TBL_DIR, "nma_rankings.png"), expand = 10)
cat("All ranking outputs generated.\n")
