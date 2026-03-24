#!/usr/bin/env Rscript
# =============================================================================
# NMA Step 04: Forest Plot — All Treatments vs Placebo
# Project: G-CSF Prophylaxis in Chemotherapy-Induced Neutropenia
# =============================================================================

library(netmeta)
library(meta)
library(ggplot2)

analysis_dir <- "projects/gcsf-neutropenia/06_analysis"
load(file.path(analysis_dir, "nma_model.RData"))

# --- NMA forest plot: treatments vs placebo ---
png(
  file.path(analysis_dir, "figures", "forest_nma.png"),
  width = 10, height = 7, units = "in", res = 300
)
forest(
  nma,
  reference.group = "placebo",
  sortvar = TE,
  smlab = paste0(
    "Febrile Neutropenia: G-CSF vs Placebo\n",
    "Random-Effects NMA (REML)"
  ),
  label.left = "Favours G-CSF",
  label.right = "Favours Placebo",
  drop.reference.group = TRUE,
  col.square = "#2C3E50",
  col.diamond = "#E74C3C",
  xlab = "Risk Ratio (log scale)"
)
dev.off()
cat("NMA forest plot saved to figures/forest_nma.png\n")

# --- Direct evidence forest plots per comparison ---
load(file.path(analysis_dir, "nma_data.RData"))

comparisons <- unique(extraction$nma_comparison)

for (comp in comparisons) {
  comp_data <- pw_meta[pw_meta$studlab %in%
    extraction$study_id[extraction$nma_comparison == comp], ]

  if (nrow(comp_data) < 2) next

  ma <- metagen(
    TE = comp_data$TE,
    seTE = comp_data$seTE,
    studlab = comp_data$studlab,
    sm = "RR",
    method.tau = "REML",
    comb.fixed = FALSE,
    comb.random = TRUE
  )

  fname <- gsub("_", "-", comp)
  png(
    file.path(analysis_dir, "figures", paste0("forest_direct_", fname, ".png")),
    width = 10, height = max(4, 2 + nrow(comp_data) * 0.5),
    units = "in", res = 300
  )
  forest(
    ma,
    smlab = paste0("FN: ", gsub("_", " ", comp), "\nDirect Evidence"),
    label.left = "Favours Treatment",
    label.right = "Favours Comparator"
  )
  dev.off()
  cat("Saved forest_direct_", fname, ".png\n")
}

cat("All forest plots generated.\n")
