# =============================================================================
# nma_03_network_graph.R — Network Geometry for Frontline DLBCL NMA
# =============================================================================

source("nma_02_data_prep.R")

# --- 1. Check connectivity ---
nc <- netconnection(treat1, treat2, studlab, data = nma_data)
cat("Network connectivity:\n")
print(nc)

if (nc$n.subnets > 1) {
  stop("DISCONNECTED NETWORK: ", nc$n.subnets, " sub-networks.")
} else {
  cat("Network is fully connected.\n")
}

# --- 2. Fit netmeta for graph ---
net_graph <- netmeta(TE, seTE, treat1, treat2, studlab,
                     data = nma_data, sm = "HR",
                     random = TRUE, fixed = FALSE,
                     method.tau = "REML",
                     reference.group = "RCHOP")

# --- 3. Network graph ---
png(file.path(FIG_DIR, "network_graph.png"),
    width = 10, height = 10, units = "in", res = FIG_DPI)

netgraph(net_graph,
         seq = "optimal",
         number.of.studies = TRUE,
         cex.points = 5,
         col.points = "steelblue",
         col = "grey40",
         plastic = FALSE,
         thickness = "number.of.studies",
         multiarm = FALSE,
         points = TRUE,
         cex.number = 1.2,
         offset = 0.05,
         main = "Network of Frontline DLBCL Regimens")

dev.off()
cat("Network graph saved.\n")

# --- 4. Print edge/node summary ---
cat("\n--- Edge Summary ---\n")
edge_counts <- nma_data %>%
  group_by(treat1, treat2) %>%
  summarise(n_studies = n(), .groups = "drop")
print(as.data.frame(edge_counts))

cat("\nNote: Star-shaped network with R-CHOP as common node.\n")
cat("Lena-R-CHOP has 2 studies (ROBUST + ECOG-E1412).\n")
cat("All other nodes have 1 study each.\n")
