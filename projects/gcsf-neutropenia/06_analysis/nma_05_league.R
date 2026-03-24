#!/usr/bin/env Rscript
# =============================================================================
# NMA Step 05: League Table (All Pairwise Comparisons)
# Project: G-CSF Prophylaxis in Chemotherapy-Induced Neutropenia
# =============================================================================

library(netmeta)
library(readr)

analysis_dir <- "projects/gcsf-neutropenia/06_analysis"
load(file.path(analysis_dir, "nma_model.RData"))

# --- Generate league table ---
league <- netleague(nma, random = TRUE, digits = 2)

cat("=== League Table (Random Effects) ===\n")
print(league)

# --- Extract all pairwise comparisons as a tidy table ---
treatments <- nma$trts
n_trts <- length(treatments)

league_df <- data.frame(
  treatment1 = character(),
  treatment2 = character(),
  RR = numeric(),
  lower = numeric(),
  upper = numeric(),
  pvalue = numeric(),
  stringsAsFactors = FALSE
)

for (i in 1:(n_trts - 1)) {
  for (j in (i + 1):n_trts) {
    t1 <- treatments[i]
    t2 <- treatments[j]
    league_df <- rbind(league_df, data.frame(
      treatment1 = t1,
      treatment2 = t2,
      RR = round(exp(nma$TE.random[t1, t2]), 2),
      lower = round(exp(nma$lower.random[t1, t2]), 2),
      upper = round(exp(nma$upper.random[t1, t2]), 2),
      pvalue = round(nma$pval.random[t1, t2], 4),
      stringsAsFactors = FALSE
    ))
  }
}

# --- Save league table ---
write_csv(league_df, file.path(analysis_dir, "tables", "league_table.csv"))
cat("League table saved to tables/league_table.csv\n")

# --- Print formatted results ---
cat("\n=== All Pairwise Comparisons ===\n")
for (i in 1:nrow(league_df)) {
  row <- league_df[i, ]
  sig <- ifelse(row$pvalue < 0.05, "*", "")
  cat(sprintf(
    "%s vs %s: RR = %.2f (95%% CI: %.2f-%.2f), p = %.4f %s\n",
    row$treatment1, row$treatment2,
    row$RR, row$lower, row$upper, row$pvalue, sig
  ))
}
