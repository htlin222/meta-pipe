# =============================================================================
# nma_06_forest_plots.R — NMA Forest Plots
# =============================================================================
# Purpose: Generate forest plots by reference treatment at 300 DPI
# Input: net_re from nma_04_models.R
# Output: figures/nma_forest_*.png
# =============================================================================

source("nma_04_models.R")

# --- 1. Set reference treatment ---
# Change to your control/reference treatment
ref_treat <- net_re$reference.group
if (is.null(ref_treat)) {
  ref_treat <- sort(unique(c(nma_data$treat1, nma_data$treat2)))[1]
  cat("No reference group set. Using:", ref_treat, "\n")
}

# --- 2. Forest plot: all treatments vs reference ---
cat("Generating forest plot vs", ref_treat, "...\n")

png(file.path(FIG_DIR, paste0("nma_forest_vs_", gsub(" ", "_", ref_treat), ".png")),
    width = 12, height = max(6, length(net_re$trts) * 0.8), units = "in", res = FIG_DPI)

forest(net_re,
       reference.group = ref_treat,
       sortvar = TE,
       smlab = paste("Treatments vs", ref_treat),
       drop.reference.group = TRUE,
       label.left  = paste("Favours", ref_treat),
       label.right = "Favours treatment")

dev.off()
cat("Forest plot saved.\n")

# --- 3. Forest plot: fixed vs random comparison ---
# Re-fit with both models for comparison
net_both <- netmeta(
  TE, seTE, treat1, treat2, studlab,
  data       = nma_data,
  sm         = NMA_SM,
  random     = TRUE,
  fixed      = TRUE,
  method.tau = "REML",
  reference.group = ref_treat
)

png(file.path(FIG_DIR, "nma_forest_fixed_vs_random.png"),
    width = 14, height = max(6, length(net_re$trts) * 0.8), units = "in", res = FIG_DPI)

forest(net_both,
       reference.group = ref_treat,
       sortvar = TE,
       drop.reference.group = TRUE)

dev.off()
cat("Fixed vs random forest plot saved.\n")

# --- 4. Pairwise forest plots for key comparisons (optional) ---
# Generate individual comparison forest plots
treatments <- sort(net_re$trts)
for (i in seq_along(treatments)) {
  if (treatments[i] == ref_treat) next

  fname <- file.path(FIG_DIR, paste0("nma_forest_",
                                      gsub(" ", "_", treatments[i]),
                                      "_vs_",
                                      gsub(" ", "_", ref_treat),
                                      ".png"))

  png(fname, width = 10, height = 6, units = "in", res = FIG_DPI)

  forest(net_re,
         reference.group = ref_treat,
         sortvar = TE,
         drop.reference.group = TRUE,
         smlab = paste(treatments[i], "vs", ref_treat))

  dev.off()
}

cat("All NMA forest plots generated in", FIG_DIR, "\n")
