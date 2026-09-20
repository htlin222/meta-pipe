# =============================================================================
# nma_03_network_graph.R — Network Geometry Visualization
# =============================================================================
# Purpose: Visualize network structure, check connectivity
# Input: nma_data from nma_02_data_prep.R
# Output: figures/network_graph.png, connectivity report
# =============================================================================

source("nma_02_data_prep.R")

# --- 1. Check network connectivity ---
nc <- netconnection(treat1, treat2, studlab, data = nma_data)
cat("Network connectivity:\n")
print(nc)

if (nc$n.subnets > 1) {
  warning("DISCONNECTED NETWORK: ", nc$n.subnets, " sub-networks detected.")
  cat("Sub-networks:\n")
  print(nc$subnet)
  cat("\nNMA requires a connected network. Consider:\n")
  cat("  1. Adding multi-arm studies that bridge sub-networks\n")
  cat("  2. Removing disconnected treatments\n")
  cat("  3. Using component NMA (analyze sub-networks separately)\n")
} else {
  cat("Network is fully connected (single component).\n")
}

# --- 2. Network graph (basic) ---
png(file.path(FIG_DIR, "network_graph.png"),
    width = FIG_WIDTH, height = FIG_HEIGHT, units = "in", res = FIG_DPI)

netgraph(
  netmeta(TE, seTE, treat1, treat2, studlab, data = nma_data,
          sm = NMA_SM, random = TRUE, method.tau = "REML"),
  seq = "optimal",
  number.of.studies = TRUE,
  cex.points = 3,
  col.points = "steelblue",
  col = "grey60",
  plastic = FALSE,
  thickness = "number.of.studies",
  multiarm = TRUE,
  col.multiarm = "purple",
  points = TRUE
)

dev.off()
cat("Network graph saved to", file.path(FIG_DIR, "network_graph.png"), "\n")

# --- 3. Network graph (ggplot2 alternative for customization) ---
# Extract edge/node data for custom plotting if needed
treatments <- sort(unique(c(nma_data$treat1, nma_data$treat2)))
n_treatments <- length(treatments)

edge_counts <- nma_data %>%
  group_by(treat1, treat2) %>%
  summarise(n_studies = n(), .groups = "drop")

node_counts <- nma_data %>%
  tidyr::pivot_longer(cols = c(treat1, treat2), values_to = "treatment") %>%
  group_by(treatment) %>%
  summarise(n_studies = n(), .groups = "drop")

cat("\n--- Edge Summary ---\n")
print(as.data.frame(edge_counts))
cat("\n--- Node Summary ---\n")
print(as.data.frame(node_counts))
