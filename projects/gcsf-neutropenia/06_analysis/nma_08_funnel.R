#!/usr/bin/env Rscript
# =============================================================================
# NMA Step 08: Comparison-Adjusted Funnel Plot
# Project: G-CSF Prophylaxis in Chemotherapy-Induced Neutropenia
# =============================================================================

library(netmeta)
library(meta)

analysis_dir <- "projects/gcsf-neutropenia/06_analysis"
load(file.path(analysis_dir, "nma_model.RData"))

# --- Comparison-adjusted funnel plot ---
png(
  file.path(analysis_dir, "figures", "funnel_plot.png"),
  width = 8, height = 7, units = "in", res = 300
)

funnel(
  nma,
  order = c("placebo", "filgrastim", "pegfilgrastim", "lipegfilgrastim"),
  pch = c(16, 17, 18, 15),
  col = c("#E74C3C", "#3498DB", "#2ECC71", "#9B59B6"),
  legend = TRUE,
  pos.legend = "topright",
  main = "Comparison-Adjusted Funnel Plot\nG-CSF NMA for Febrile Neutropenia"
)

dev.off()
cat("Funnel plot saved to figures/funnel_plot.png\n")

# --- Egger's test for small-study effects (per direct comparison) ---
cat("\n=== Small-Study Effects Assessment ===\n")
load(file.path(analysis_dir, "nma_data.RData"))

comparisons <- unique(extraction$nma_comparison)
for (comp in comparisons) {
  comp_data <- pw_meta[pw_meta$studlab %in%
    extraction$study_id[extraction$nma_comparison == comp], ]

  if (nrow(comp_data) >= 3) {
    ma <- metagen(
      TE = comp_data$TE,
      seTE = comp_data$seTE,
      studlab = comp_data$studlab,
      sm = "RR"
    )
    egger <- metabias(ma, method.bias = "Egger")
    cat(sprintf(
      "%s: Egger's p = %.4f %s\n",
      comp, egger$p.value,
      ifelse(egger$p.value < 0.10, "(potential bias)", "(no evidence of bias)")
    ))
  } else {
    cat(sprintf("%s: Too few studies (k=%d) for Egger's test\n", comp, nrow(comp_data)))
  }
}
