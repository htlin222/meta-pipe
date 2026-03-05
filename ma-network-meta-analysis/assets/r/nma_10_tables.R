# =============================================================================
# nma_10_tables.R — Export League Table & Rankings as Publication Tables
# =============================================================================
# Purpose: Create gt/PNG tables for manuscript inclusion
# Input: net_re from nma_04_models.R, rankings from nma_07_ranking.R
# Output: tables/league_table.png, tables/nma_summary.png
# =============================================================================

source("nma_04_models.R")

library(gt)
library(flextable)

# --- 1. League table ---
# Full league table (Bayesian + frequentist) is generated in nma_08_league_table.R
# This script focuses on the summary table and export formats.
cat("Note: Full league table is in nma_08_league_table.R\n")

# --- 2. Compute P-score ranking (needed for summary table) ---
ranking <- netrank(net_re, small.values = "undesirable")

# --- 3. Summary table: all treatments vs reference ---
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

  sm <- net_re$sm
  if (sm %in% c("RR", "OR", "HR")) {
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
