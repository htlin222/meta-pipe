#!/usr/bin/env Rscript
# =============================================================================
# NMA Step 06: SUCRA / P-score Rankings
# Project: G-CSF Prophylaxis in Chemotherapy-Induced Neutropenia
# =============================================================================

library(netmeta)
library(ggplot2)
library(readr)

analysis_dir <- "projects/gcsf-neutropenia/06_analysis"
load(file.path(analysis_dir, "nma_model.RData"))

# --- Calculate P-scores (frequentist analogue of SUCRA) ---
# Lower RR = better (fewer FN events), so small.values = "desirable"
rank_result <- netrank(nma, small.values = "desirable")

cat("=== P-score Rankings ===\n")
print(rank_result)

# --- Create ranking table ---
ranking_df <- data.frame(
  treatment = names(rank_result$Pscore.random),
  p_score = round(rank_result$Pscore.random, 4),
  rank = rank(1 - rank_result$Pscore.random),
  stringsAsFactors = FALSE
)
ranking_df <- ranking_df[order(ranking_df$rank), ]

cat("\n=== Treatment Rankings (Best to Worst for FN Prevention) ===\n")
print(ranking_df)

write_csv(ranking_df, file.path(analysis_dir, "tables", "ranking_table.csv"))
cat("Ranking table saved to tables/ranking_table.csv\n")

# --- Rankogram ---
png(
  file.path(analysis_dir, "figures", "rankogram.png"),
  width = 8, height = 6, units = "in", res = 300
)

# Create rankogram-style bar plot using P-scores
rank_plot <- ggplot(ranking_df, aes(
  x = reorder(treatment, -p_score),
  y = p_score,
  fill = treatment
)) +
  geom_col(width = 0.6, alpha = 0.85) +
  geom_text(aes(label = sprintf("%.3f", p_score)),
    vjust = -0.5, size = 4
  ) +
  scale_fill_manual(values = c(
    "lipegfilgrastim" = "#9B59B6",
    "pegfilgrastim" = "#2ECC71",
    "filgrastim" = "#3498DB",
    "placebo" = "#E74C3C"
  )) +
  labs(
    title = "P-score Rankings: G-CSF Treatments for FN Prevention",
    subtitle = "Higher P-score = more effective at reducing febrile neutropenia",
    x = "Treatment",
    y = "P-score"
  ) +
  ylim(0, 1.1) +
  theme_minimal(base_size = 14) +
  theme(
    legend.position = "none",
    plot.title = element_text(face = "bold"),
    axis.text.x = element_text(angle = 0, hjust = 0.5)
  )

print(rank_plot)
dev.off()
cat("Rankogram saved to figures/rankogram.png\n")
