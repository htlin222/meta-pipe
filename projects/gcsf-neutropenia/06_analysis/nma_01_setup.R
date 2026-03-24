#!/usr/bin/env Rscript
# =============================================================================
# NMA Step 01: Setup and Data Preparation
# Project: G-CSF Prophylaxis in Chemotherapy-Induced Neutropenia
# Primary outcome: Febrile neutropenia incidence (RR)
# =============================================================================

# --- Load packages ---
library(meta)
library(netmeta)
library(dmetar)
library(ggplot2)
library(readr)
library(dplyr)
library(tidyr)

# --- Set working directory ---
setwd(here::here())
analysis_dir <- "projects/gcsf-neutropenia/06_analysis"

# --- Read extraction data ---
extraction <- read_csv(
  "projects/gcsf-neutropenia/05_extraction/round-01/extraction.csv",
  show_col_types = FALSE
)
rob <- read_csv(
  "projects/gcsf-neutropenia/05_extraction/rob_assessment.csv",
  show_col_types = FALSE
)

cat("Loaded", nrow(extraction), "studies\n")
cat("NMA comparisons:\n")
print(table(extraction$nma_comparison))

# --- Map treatments to standardized nodes ---
# 4 treatment nodes:
#   1. placebo (includes "no GCSF", "standard care", "antibiotics alone")
#   2. filgrastim
#   3. pegfilgrastim
#   4. lipegfilgrastim

extraction <- extraction %>%
  mutate(
    treat1 = case_when(
      nma_comparison == "filgrastim_vs_placebo" ~ "filgrastim",
      nma_comparison == "pegfilgrastim_vs_placebo" ~ "pegfilgrastim",
      nma_comparison == "pegfilgrastim_vs_filgrastim" ~ "pegfilgrastim",
      nma_comparison == "lipegfilgrastim_vs_pegfilgrastim" ~ "lipegfilgrastim"
    ),
    treat2 = case_when(
      nma_comparison == "filgrastim_vs_placebo" ~ "placebo",
      nma_comparison == "pegfilgrastim_vs_placebo" ~ "placebo",
      nma_comparison == "pegfilgrastim_vs_filgrastim" ~ "filgrastim",
      nma_comparison == "lipegfilgrastim_vs_pegfilgrastim" ~ "pegfilgrastim"
    )
  )

# --- Prepare pairwise data for netmeta ---
# For dichotomous outcomes, we use log(RR) and SE(log(RR))
pw_data <- extraction %>%
  mutate(
    event1 = fn_events_intervention,
    n1 = n_intervention,
    event2 = fn_events_control,
    n2 = n_control
  ) %>%
  select(
    study_id, first_author, year,
    treat1, treat2,
    event1, n1, event2, n2,
    nma_comparison, risk_of_bias_overall
  )

# Calculate log(RR) and SE for each study using metabin
pw_meta <- pairwise(
  treat = list(treat1, treat2),
  event = list(event1, event2),
  n = list(n1, n2),
  studlab = study_id,
  data = pw_data,
  sm = "RR"
)

cat("\n--- Pairwise data prepared ---\n")
cat("Number of pairwise comparisons:", nrow(pw_meta), "\n")
cat("Treatments:", unique(c(pw_meta$treat1, pw_meta$treat2)), "\n")

# --- Merge RoB data ---
pw_meta <- pw_meta %>%
  left_join(rob %>% select(study_id, overall_rob), by = "study_id")

# --- Save prepared data ---
write_csv(pw_meta, file.path(analysis_dir, "tables", "prepared_pairwise_data.csv"))
save(pw_meta, extraction, rob, file = file.path(analysis_dir, "nma_data.RData"))

cat("\nSetup complete. Data saved to", analysis_dir, "\n")
