# R Package Setup for Meta-Analysis

**When to use**: First time setting up R for meta-analysis
**Time**: 10-15 minutes
**Prerequisite**: R and RStudio installed

---

## Quick Install (Copy & Paste)

### The Recommended Stack (Start Here)

**For 95% of meta-analyses, install these packages:**

```r
# The Typical Stack (covers ~80% of analyses)
install.packages(c(
  "metafor",        # Core: effect sizes, models, meta-regression (handles 80%)
  "meta",           # Quick forest plots for RCTs (+10%)
  "dmetar",         # Publication bias helpers (+5%)
  "clubSandwich",   # Robust variance for multilevel models (+3%)
  "PublicationBias" # Sensitivity analyses (+2%)
))
# Total coverage: ~95-98% of typical workflows
```

**Why this combination?**

- Based on expert recommendation: `metafor + meta + dmetar + clubSandwich + PublicationBias`
- Covers ~95% of meta-analysis needs
- Minimal package count (5 packages)
- Install time: ~2-3 minutes

### Visualization & Tables

```r
# Visualization
install.packages(c("ggplot2", "patchwork", "cowplot"))

# Tables
install.packages(c("gtsummary", "gt", "flextable"))

# Themes & Colors
install.packages(c("hrbrthemes", "ggsci", "viridis"))

# Data manipulation
install.packages("tidyverse")
```

**Total time**: ~8-12 minutes depending on internet speed

---

## What Each Package Does

### The Recommended Stack (Essential)

```r
install.packages(c("metafor", "meta", "dmetar", "clubSandwich", "PublicationBias"))
```

- **metafor**: The backbone of meta-analysis in R (80% coverage)
  - [Website](https://www.metafor-project.org/)
  - Use for: effect sizes (escalc), models (rma), meta-regression, heterogeneity
  - **Why essential**: Handles 50+ effect size types, 10+ tau² estimators, most flexible

- **meta**: Quick forest plots and simple analyses (+10% coverage)
  - [CRAN](https://cran.r-project.org/web/packages/meta/)
  - Use for: auto forest plots (metabin, metacont), simple RCT meta-analysis
  - **Why essential**: Publication-ready plots with one command

- **dmetar**: Convenient bias tools (+5% coverage)
  - [Website](https://dmetar.protectlab.org/)
  - Use for: p-curve, limit meta-analysis, helper functions
  - **Why essential**: Simplifies publication bias assessment

- **clubSandwich**: Robust variance for multilevel models (+3% coverage)
  - [CRAN](https://cran.r-project.org/web/packages/clubSandwich/)
  - Use for: cluster-robust standard errors with rma.mv()
  - **Why essential**: Handles dependent effect sizes (multiple outcomes per study)

- **PublicationBias**: Sensitivity analyses (+2% coverage)
  - [CRAN](https://cran.r-project.org/web/packages/PublicationBias/)
  - Use for: Mathur & VanderWeele methods, selection model sensitivity
  - **Why essential**: Advanced publication bias detection

### Visualization

```r
install.packages(c("ggplot2", "patchwork", "cowplot"))
```

- **ggplot2**: Grammar of graphics
  - [Website](https://ggplot2.tidyverse.org/)
  - Use for: all custom plots

- **patchwork**: Combine multiple plots
  - [Website](https://patchwork.data-imaginist.com/)
  - Use for: multi-panel figures (`p1 / p2 / p3`)

- **cowplot**: Publication-ready plot layouts
  - [Website](https://wilkelab.org/cowplot/)
  - Use for: precise control over panel arrangement

### Tables

```r
install.packages(c("gtsummary", "gt", "flextable"))
```

- **gtsummary**: Summary tables with statistics
  - [Website](https://www.danieldsjoberg.com/gtsummary/)
  - Use for: Table 1, regression tables

- **gt**: Grammar of tables (for HTML/PDF)
  - [Website](https://gt.rstudio.com/)
  - Use for: export gtsummary to HTML

- **flextable**: Tables for Word/PowerPoint
  - [Website](https://ardata-fr.github.io/flextable-book/)
  - Use for: export gtsummary to DOCX

### Themes & Colors

```r
install.packages(c("hrbrthemes", "ggsci", "viridis"))
```

- **hrbrthemes**: Professional typography
  - [CRAN](https://cran.r-project.org/web/packages/hrbrthemes/)
  - Use for: clean, readable plots

- **ggsci**: Scientific journal color palettes
  - [CRAN](https://cran.r-project.org/web/packages/ggsci/)
  - Use for: Lancet, NEJM, Nature colors

- **viridis**: Colorblind-safe palettes
  - [CRAN](https://cran.r-project.org/web/packages/viridis/)
  - Use for: heatmaps, continuous scales

---

## Verify Installation

```r
# Test that packages loaded successfully
library(meta)
library(ggplot2)
library(gtsummary)
library(patchwork)

# If no errors, you're ready to go!
cat("✅ All packages installed successfully!\n")
```

---

## Optional: GitHub Packages

Some packages require installation from GitHub:

```r
# Install devtools first
install.packages("devtools")

# ggthemr - easy theme switching
devtools::install_github("Mikata-Project/ggthemr")
```

---

## Troubleshooting

### Problem: Package installation fails

```r
# Try changing CRAN mirror
options(repos = c(CRAN = "https://cloud.r-project.org/"))
install.packages("meta")
```

### Problem: "non-zero exit status"

**Solution**: Install system dependencies first (macOS)

```bash
# In Terminal, not R
brew install cairo
brew install harfbuzz
brew install fribidi
```

**Solution**: Install system dependencies (Ubuntu/Debian)

```bash
sudo apt-get install libcairo2-dev
sudo apt-get install libharfbuzz-dev
sudo apt-get install libfribidi-dev
```

---

## See Also

- [01-forest-plots.md](01-forest-plots.md) - Start making forest plots
- [05-table1-gtsummary.md](05-table1-gtsummary.md) - Create Table 1
- [07-themes-colors.md](07-themes-colors.md) - Choose colors and themes
