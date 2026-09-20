# =============================================================================
# nma_07_ranking.R — Treatment Rankings: SUCRA + Rankograms (Bayesian Primary)
# =============================================================================
# Purpose: Compute SUCRA rankings and rankograms from Bayesian posterior;
#          P-scores from frequentist model as sensitivity
# Input: bayes_re from nma_04_models.R, net_re for sensitivity
# Output: tables/nma_rankings.csv, figures/nma_rankogram.png, figures/nma_sucra.png
# =============================================================================

source("nma_04_models.R")

# =============================================================================
# SECTION A: BAYESIAN RANKINGS (PRIMARY)
# =============================================================================

cat("=== Treatment Rankings (SUCRA from Bayesian Posterior) ===\n")

# --- 1. Compute rank probabilities ---
# preferredDirection: 1 = higher values better, -1 = lower values better
NMA_PREF_DIR <- if (NMA_SMALL_VALUES == "desirable") -1 else 1
ranks <- rank.probability(bayes_re, preferredDirection = NMA_PREF_DIR)
cat("Rank probability matrix:\n")
print(ranks)

# --- 2. Calculate SUCRA ---
sucra <- sucra(ranks)
cat("\nSUCRA values:\n")
print(sucra)

# Build ranking data frame
rank_df <- data.frame(
  Treatment = names(sucra),
  SUCRA     = round(as.numeric(sucra), 4),
  stringsAsFactors = FALSE
) %>%
  arrange(desc(SUCRA))

rank_df$Rank <- seq_len(nrow(rank_df))

cat("\n--- Rankings by SUCRA ---\n")
print(rank_df)

# Save rankings
write_csv(rank_df, file.path(TBL_DIR, "nma_rankings.csv"))

# --- 3. Rankogram (rank probability plot) ---
cat("\nGenerating rankogram...\n")

# Convert rank probabilities to long format for ggplot
ranks_matrix <- as.matrix(ranks)
ranks_long <- as.data.frame(ranks_matrix) %>%
  mutate(Treatment = rownames(ranks_matrix)) %>%
  tidyr::pivot_longer(
    cols = -Treatment,
    names_to = "Rank",
    values_to = "Probability"
  ) %>%
  mutate(Rank = as.integer(gsub("Rank ", "", Rank)))

p_rankogram <- ggplot(ranks_long, aes(x = Rank, y = Probability, fill = Treatment)) +
  geom_col(position = "dodge", alpha = 0.8) +
  facet_wrap(~Treatment, scales = "free_y") +
  scale_x_continuous(breaks = seq_len(nrow(ranks_matrix))) +
  scale_y_continuous(limits = c(0, 1)) +
  labs(
    title = "Rankograms (Rank Probability Distribution)",
    subtitle = "Bayesian posterior rank probabilities",
    x = "Rank (1 = best)",
    y = "Probability"
  ) +
  theme_minimal(base_size = 11) +
  theme(
    legend.position = "none",
    strip.text = element_text(face = "bold"),
    plot.title = element_text(face = "bold")
  )

ggsave(file.path(FIG_DIR, "nma_rankogram.png"), p_rankogram,
       width = 12, height = max(6, nrow(ranks_matrix) * 1.5),
       dpi = FIG_DPI)
cat("Rankogram saved to", file.path(FIG_DIR, "nma_rankogram.png"), "\n")

# --- 4. SUCRA bar plot ---
p_sucra <- ggplot(rank_df, aes(x = reorder(Treatment, SUCRA), y = SUCRA)) +
  geom_col(fill = "steelblue", alpha = 0.8) +
  geom_text(aes(label = sprintf("%.1f%%", SUCRA * 100)), hjust = -0.1, size = 3.5) +
  coord_flip() +
  scale_y_continuous(limits = c(0, 1.15), breaks = seq(0, 1, 0.2),
                     labels = scales::percent_format(accuracy = 1)) +
  labs(
    title = "Treatment Ranking (SUCRA)",
    subtitle = "Surface Under the Cumulative Ranking curve (Bayesian posterior)",
    x = NULL,
    y = "SUCRA"
  ) +
  theme_minimal(base_size = 12) +
  theme(
    panel.grid.major.y = element_blank(),
    plot.title = element_text(face = "bold")
  )

ggsave(file.path(FIG_DIR, "nma_sucra_plot.png"), p_sucra,
       width = FIG_WIDTH, height = max(4, nrow(rank_df) * 0.6),
       dpi = FIG_DPI)
cat("SUCRA plot saved to", file.path(FIG_DIR, "nma_sucra_plot.png"), "\n")

# --- 5. League table (Bayesian) ---
cat("\n=== League Table (Bayesian Posterior Medians + 95% CrI) ===\n")
# Extract relative effects from gemtc
rel_effects <- relative.effect(bayes_re, t1 = rank_df$Treatment[1])
cat("Relative effects vs", rank_df$Treatment[1], ":\n")
print(summary(rel_effects))

# =============================================================================
# SECTION B: FREQUENTIST RANKINGS (SENSITIVITY)
# =============================================================================

cat("\n=== P-scores (Frequentist Sensitivity) ===\n")
pscore_ranking <- netrank(net_re, small.values = NMA_SMALL_VALUES)

pscore_df <- data.frame(
  Treatment = names(pscore_ranking$Pscore.random),
  P_score   = round(pscore_ranking$Pscore.random, 4),
  stringsAsFactors = FALSE
) %>%
  arrange(desc(P_score))

# Merge SUCRA and P-scores for comparison
comparison_df <- merge(rank_df[, c("Treatment", "SUCRA")],
                       pscore_df, by = "Treatment") %>%
  arrange(desc(SUCRA))

cat("\n--- SUCRA vs P-score Comparison ---\n")
print(comparison_df)
write_csv(comparison_df, file.path(TBL_DIR, "nma_ranking_comparison.csv"))

# --- 6. Rankings as gt table (PNG) ---
rank_gt <- rank_df %>%
  gt() %>%
  tab_header(
    title = "Treatment Rankings (SUCRA)",
    subtitle = "Bayesian NMA posterior rank probabilities"
  ) %>%
  fmt_number(columns = SUCRA, decimals = 3) %>%
  cols_label(
    Treatment = "Treatment",
    SUCRA     = "SUCRA",
    Rank      = "Rank"
  ) %>%
  tab_style(
    style = cell_fill(color = "#e8f4f8"),
    locations = cells_body(rows = Rank == 1)
  ) %>%
  tab_footnote(
    footnote = "SUCRA: Surface Under the Cumulative Ranking curve (0 = worst, 1 = best)",
    locations = cells_column_labels(columns = SUCRA)
  )

gtsave(rank_gt, file.path(TBL_DIR, "nma_rankings.png"), expand = 10)
cat("Rankings table (PNG) saved to", file.path(TBL_DIR, "nma_rankings.png"), "\n")

# League tables (Bayesian primary + frequentist supplement) are built in nma_10_tables.R
