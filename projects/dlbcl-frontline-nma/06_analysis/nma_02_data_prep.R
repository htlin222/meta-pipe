# =============================================================================
# nma_02_data_prep.R — Data Preparation for Frontline DLBCL NMA
# =============================================================================
# Input: ../05_extraction/nma_pfs_input.csv
# Output: nma_data (contrast-based, log-HR scale for netmeta/gemtc)
# =============================================================================

source("nma_01_setup.R")

# --- 1. Read extraction data ---
raw <- read_csv("../05_extraction/nma_pfs_input.csv", show_col_types = FALSE)
cat("Trials loaded:", nrow(raw), "\n")

# --- 2. Prepare PFS NMA data (primary outcome) ---
# Convert HR to log-HR and compute seTE from CI
nma_pfs <- raw %>%
  mutate(
    studlab = trial,
    treat1  = intervention,
    treat2  = comparator,
    TE      = log(pfs_hr),
    # Compute SE from 95% CI: SE = (log(upper) - log(lower)) / (2 * 1.96)
    seTE    = case_when(
      !is.na(pfs_hr_lci) & !is.na(pfs_hr_uci) ~
        (log(pfs_hr_uci) - log(pfs_hr_lci)) / (2 * 1.96),
      # For REMoDL-B 5y: approximate from p-value
      trial == "REMoDL-B_5y" ~ abs(log(pfs_hr)) / qnorm(1 - 0.085/2),
      TRUE ~ NA_real_
    )
  ) %>%
  filter(!is.na(TE), !is.na(seTE)) %>%
  select(studlab, treat1, treat2, TE, seTE,
         n_intervention, n_comparator, median_fu_months, population)

cat("\n--- PFS NMA Data ---\n")
print(as.data.frame(nma_pfs))

# --- 3. Prepare OS NMA data (secondary outcome) ---
nma_os <- raw %>%
  filter(!is.na(os_hr), !is.na(os_hr_lci), !is.na(os_hr_uci)) %>%
  mutate(
    studlab = trial,
    treat1  = intervention,
    treat2  = comparator,
    TE      = log(os_hr),
    seTE    = (log(os_hr_uci) - log(os_hr_lci)) / (2 * 1.96)
  ) %>%
  select(studlab, treat1, treat2, TE, seTE)

cat("\n--- OS NMA Data ---\n")
print(as.data.frame(nma_os))

# --- 4. Standardize treatment names ---
# Ensure consistent naming across all data
treatment_labels <- c(
  "Pola-R-CHP"       = "PolaRCHP",
  "R-CHOP+ibrutinib"  = "IbrutRCHOP",
  "R2-CHOP"           = "LenaRCHOP",
  "R2CHOP"            = "LenaRCHOP",
  "RB-CHOP"           = "BortRCHOP",
  "G-CHOP"            = "GCHOP",
  "DA-EPOCH-R"        = "DA_EPOCH_R",
  "R-CHOP"            = "RCHOP"
)

# Display labels for figures (maps internal names to pretty labels)
treatment_display <- c(
  "PolaRCHP"    = "Pola-R-CHP",
  "IbrutRCHOP"  = "Ibrut+R-CHOP",
  "LenaRCHOP"   = "Lena+R-CHOP",
  "BortRCHOP"   = "Bort+R-CHOP",
  "GCHOP"       = "G-CHOP",
  "DA_EPOCH_R"  = "DA-EPOCH-R",
  "RCHOP"       = "R-CHOP"
)

nma_pfs <- nma_pfs %>%
  mutate(
    treat1 = recode(treat1, !!!treatment_labels),
    treat2 = recode(treat2, !!!treatment_labels)
  )

nma_os <- nma_os %>%
  mutate(
    treat1 = recode(treat1, !!!treatment_labels),
    treat2 = recode(treat2, !!!treatment_labels)
  )

# --- 5. Validate ---
cat("\n--- Validation ---\n")
cat("PFS: ", nrow(nma_pfs), "contrasts,",
    length(unique(c(nma_pfs$treat1, nma_pfs$treat2))), "treatments\n")
cat("Treatments:", paste(sort(unique(c(nma_pfs$treat1, nma_pfs$treat2))), collapse = ", "), "\n")
cat("OS: ", nrow(nma_os), "contrasts,",
    length(unique(c(nma_os$treat1, nma_os$treat2))), "treatments\n")

# Note: lenalidomide has 2 trials (ROBUST + ECOG-E1412) → same node
cat("\nNote: ROBUST (ABC-only) and ECOG-E1412 (all DLBCL) both map to Lena-R-CHOP node.\n")
cat("Sensitivity analysis excluding ROBUST should be run separately.\n")

# Use nma_pfs as the primary working dataset
nma_data <- nma_pfs
write_csv(nma_data, "nma_prepared_data.csv")
cat("\nPrepared data saved.\n")
