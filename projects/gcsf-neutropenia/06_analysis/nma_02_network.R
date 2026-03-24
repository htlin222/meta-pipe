#!/usr/bin/env Rscript
# =============================================================================
# NMA Step 02: Network Graph Visualization
# Project: G-CSF Prophylaxis in Chemotherapy-Induced Neutropenia
# =============================================================================

library(netmeta)
library(ggplot2)

analysis_dir <- "projects/gcsf-neutropenia/06_analysis"
load(file.path(analysis_dir, "nma_data.RData"))

# --- Run NMA (needed for netgraph) ---
nma <- netmeta(
  TE = TE,
  seTE = seTE,
  treat1 = treat1,
  treat2 = treat2,
  studlab = studlab,
  data = pw_meta,
  sm = "RR",
  reference.group = "placebo",
  comb.fixed = FALSE,
  comb.random = TRUE,
  method.tau = "REML"
)

# --- Network plot ---
png(
  file.path(analysis_dir, "figures", "network_plot.png"),
  width = 8, height = 8, units = "in", res = 300
)

netgraph(
  nma,
  seq = c("placebo", "filgrastim", "pegfilgrastim", "lipegfilgrastim"),
  labels = c(
    "Placebo/\nNo G-CSF",
    "Filgrastim",
    "Pegfilgrastim",
    "Lipegfilgrastim"
  ),
  number.of.studies = TRUE,
  plastic = FALSE,
  thickness = "number.of.studies",
  points = TRUE,
  cex.points = 3,
  col = "#2C3E50",
  col.points = c("#E74C3C", "#3498DB", "#2ECC71", "#9B59B6"),
  multiarm = TRUE,
  main = "Network of G-CSF Treatments for FN Prevention"
)

dev.off()
cat("Network plot saved to figures/network_plot.png\n")

# --- Print network characteristics ---
cat("\n--- Network Characteristics ---\n")
cat("Number of treatments:", nma$n, "\n")
cat("Number of studies:", nma$k, "\n")
cat("Number of pairwise comparisons:", nma$m, "\n")
cat("Network is connected:", nma$n.subnets == 1, "\n")
