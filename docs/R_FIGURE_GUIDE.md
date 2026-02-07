# R Figure Generation Guide for Meta-Analysis

**Purpose**: Generate publication-quality figures at 300 DPI using R
**When to use**: Stage 06 (Analysis) and Stage 07 (Manuscript)

---

## R Package Ecosystem

When generating figures, consult these authoritative sources for package documentation:

### Core Package Repositories

1. **[CRAN](https://cran.r-project.org/)** — The Comprehensive R Archive Network
   - Official R package repository (19,000+ packages)
   - All packages peer-reviewed and tested
   - Use: `install.packages("package_name")`
   - Browse: https://cran.r-project.org/web/packages/available_packages_by_name.html

2. **[Bioconductor](https://bioconductor.org/)** — Bioinformatics & Genomics
   - Specialized packages for biological data analysis
   - Use: `BiocManager::install("package_name")`
   - Browse: https://bioconductor.org/packages/release/BiocViews.html

3. **[Tidyverse](https://www.tidyverse.org/)** — Modern Data Science
   - Core packages: ggplot2, dplyr, tidyr, readr
   - Consistent API design
   - Use: `install.packages("tidyverse")`
   - Learn: https://www.tidyverse.org/learn/

4. **[rOpenSci](https://ropensci.org/)** — Peer-Reviewed Scientific Tools
   - Community-driven, open peer review
   - High-quality packages for reproducible research
   - Browse: https://ropensci.org/packages/

5. **[R-universe](https://r-universe.dev/)** — Next-Gen Package Discovery
   - Search across CRAN, Bioconductor, GitHub
   - View dependencies and reverse dependencies
   - Browse: https://r-universe.dev/search/

---

## Essential Packages for Meta-Analysis Figures

### Meta-Analysis Core

```r
# Install meta-analysis packages
install.packages(c("meta", "metafor", "dmetar"))

# Load packages
library(meta)      # Simple interface for meta-analysis
library(metafor)   # Comprehensive meta-analysis tools
library(dmetar)    # Companion to "Doing Meta-Analysis in R"
```

**Documentation**:

- meta: https://cran.r-project.org/web/packages/meta/
- metafor: https://www.metafor-project.org/
- dmetar: https://dmetar.protectlab.org/

### Plotting & Visualization

```r
# Install core visualization packages
install.packages(c(
  "ggplot2",      # Grammar of graphics
  "patchwork",    # Combine multiple plots
  "cowplot",      # Publication-ready themes
  "ggpubr",       # Publication-ready plots
  "forestplot"    # Specialized forest plots
))

# Install professional theme packages
install.packages(c(
  "ggthemes",     # Professional themes (Economist, WSJ, etc.)
  "hrbrthemes",   # Typography-focused themes
  "tvthemes",     # TV show inspired themes
  "viridis",      # Colorblind-friendly palettes
  "scico",        # Scientific color maps
  "ggsci",        # Scientific journal color palettes
  "ggthemr"       # Easy theme switching (from GitHub)
))

# ggthemr requires installation from GitHub
# install.packages("devtools")
# devtools::install_github("Mikata-Project/ggthemr")
```

**Key packages**:

1. **ggplot2** — Grammar of Graphics
   - Flexible, publication-quality plots
   - [Documentation](https://ggplot2.tidyverse.org/)
   - [Gallery](https://r-graph-gallery.com/ggplot2-package.html)

2. **patchwork** — Multi-Panel Figures
   - Intuitive syntax: `plot1 + plot2`
   - [Documentation](https://patchwork.data-imaginist.com/)
   - Perfect for journal submissions

3. **cowplot** — Publication Themes
   - Clean themes for publications
   - [Documentation](https://wilkelab.org/cowplot/)
   - Panel labeling: `plot_grid(labels="AUTO")`

4. **forestplot** — Specialized Forest Plots
   - High-level forest plot interface
   - [Documentation](https://cran.r-project.org/web/packages/forestplot/)

### Professional Themes & Color Palettes

**Why use professional themes?**

- **Consistency**: Journal-quality aesthetics across all figures
- **Accessibility**: Colorblind-friendly palettes (viridis, scico)
- **Impact**: Professional appearance increases credibility
- **Time savings**: Pre-designed themes eliminate trial-and-error

#### Recommended Theme Packages

1. **ggthemr** — Easy Theme Switching
   - [GitHub](https://github.com/Mikata-Project/ggthemr)
   - One-line theme application
   - Themes: `flat`, `fresh`, `pale`, `earth`, `grape`
   - **Use for**: Clean, modern figures with consistent color schemes

2. **hrbrthemes** — Typography-Focused
   - [CRAN](https://cran.r-project.org/web/packages/hrbrthemes/)
   - Professional typography with Roboto Condensed fonts
   - Minimal distractions, focus on data
   - **Use for**: High-impact journal submissions (Nature, Science)

3. **tvthemes** — Stylized Themes
   - [GitHub](https://github.com/Ryo-N7/tvthemes)
   - TV show inspired (Avatar, Brooklyn 99, etc.)
   - Fun for presentations, not recommended for publications
   - **Use for**: Conference talks, lab meetings

4. **ggthemes** — Professional Standards
   - [CRAN](https://cran.r-project.org/web/packages/ggthemes/)
   - Economist, WSJ, FiveThirtyEight styles
   - `theme_tufte()` for minimalist design
   - **Use for**: Matching target journal style (Economist theme for health policy)

5. **viridis** — Colorblind-Friendly
   - [CRAN](https://cran.r-project.org/web/packages/viridis/)
   - Perceptually uniform color maps
   - 5 palettes: viridis, magma, inferno, plasma, cividis
   - **Use for**: ALL color gradients (mandatory for accessibility)

6. **scico** — Scientific Color Maps
   - [CRAN](https://cran.r-project.org/web/packages/scico/)
   - 30+ scientific color palettes
   - Perceptually uniform, colorblind-safe
   - **Use for**: Heatmaps, continuous variables

7. **ggsci** — Journal Color Palettes
   - [CRAN](https://cran.r-project.org/web/packages/ggsci/)
   - Nature, NEJM, Lancet, JAMA color schemes
   - `scale_color_nejm()`, `scale_fill_lancet()`
   - **Use for**: Matching target journal aesthetics

---

## Professional Theme Usage

### Quick Start: Apply Themes to Your Plots

#### Method 1: ggthemr (Simplest)

```r
library(ggplot2)
library(ggthemr)

# Set theme once, applies to ALL subsequent plots
ggthemr("fresh")  # Options: flat, fresh, pale, earth, grape, light, chalk

# All plots now use this theme automatically
p1 <- ggplot(mtcars, aes(mpg, wt)) + geom_point()
p2 <- ggplot(iris, aes(Sepal.Length, Sepal.Width, color = Species)) + geom_point()

# Reset to default ggplot2 theme
ggthemr_reset()
```

**Best themes for publications**:

- `fresh` — Clean, modern (recommended for most journals)
- `pale` — Soft colors, high contrast
- `flat` — Minimal, professional

#### Method 2: hrbrthemes (Best Typography)

```r
library(ggplot2)
library(hrbrthemes)

# Apply to individual plot
p <- ggplot(mtcars, aes(mpg, wt)) +
  geom_point() +
  theme_ipsum() +              # Main theme
  labs(title = "Highway MPG vs Weight")

# Variations
theme_ipsum_rc()  # Roboto Condensed (recommended)
theme_ipsum_ps()  # IBM Plex Sans
theme_ipsum_tw()  # Titillium Web
```

**Why use hrbrthemes?**

- Professional typography out-of-the-box
- High contrast for readability
- Minimal grid lines (focuses attention on data)
- Used by data journalism (FiveThirtyEight style)

#### Method 3: ggsci (Journal Color Palettes)

```r
library(ggplot2)
library(ggsci)

# Match Nature journal colors
p <- ggplot(data, aes(x, y, color = group)) +
  geom_point() +
  scale_color_npg() +           # Nature Publishing Group
  theme_minimal()

# Other journal palettes
scale_color_nejm()   # New England Journal of Medicine
scale_color_lancet() # The Lancet
scale_color_jama()   # JAMA
scale_color_jco()    # Journal of Clinical Oncology
```

**When to use**:

- Submitting to specific journal → use that journal's palette
- General medical journal → use NEJM or Lancet
- Oncology → use JCO palette

#### Method 4: viridis (Colorblind-Safe)

```r
library(ggplot2)
library(viridis)

# For continuous variables
p <- ggplot(data, aes(x, y, color = value)) +
  geom_point() +
  scale_color_viridis_c(option = "plasma")  # Options: A-H

# For discrete groups
p <- ggplot(data, aes(x, y, color = group)) +
  geom_point() +
  scale_color_viridis_d(option = "viridis")

# Options explained
# "viridis" (A) — Default, purple to yellow
# "magma"   (B) — Dark purple to white
# "inferno" (C) — Black to yellow
# "plasma"  (D) — Purple to pink to yellow (recommended)
# "cividis" (E) — Blue to yellow (best for colorblind)
```

**Mandatory use cases**:

- Heatmaps
- Continuous color scales
- Any plot where color represents data value
- Plots that might be printed in grayscale

#### Method 5: Combining Multiple Packages

```r
library(ggplot2)
library(hrbrthemes)
library(ggsci)

# Professional plot with best practices
p <- ggplot(data, aes(x, y, color = treatment)) +
  geom_point(size = 3, alpha = 0.7) +
  geom_smooth(method = "loess", se = TRUE) +
  scale_color_lancet() +        # Lancet color palette
  theme_ipsum_rc() +            # Professional typography
  labs(
    title = "Treatment Effect Over Time",
    subtitle = "RCT data from 5 trials (N=2,402)",
    x = "Time (months)",
    y = "Response Rate (%)",
    color = "Treatment"
  )

ggsave("figures/treatment_effect.png", width = 10, height = 6, dpi = 300)
```

---

## Figure Generation Workflow

### 1. Forest Plots (Primary Outcome)

**Using metafor with professional themes**:

```r
library(metafor)
library(meta)
library(ggplot2)
library(ggsci)

# Load extraction data
data <- read.csv("05_extraction/extraction.csv")

# Calculate risk ratios
res <- metabin(
  event.e = events_ici,
  n.e = total_ici,
  event.c = events_control,
  n.c = total_control,
  data = data,
  studlab = study_id,
  sm = "RR",
  method = "MH",
  fixed = FALSE,
  random = TRUE
)

# Create forest plot with Lancet colors
png("07_manuscript/figures/figure1_forest.png",
    width = 10, height = 8, units = "in", res = 300)

# Use Lancet color palette (professional medical journal style)
lancet_colors <- pal_lancet()(2)  # Get 2 colors from Lancet palette

forest(res,
       xlim = c(0.5, 2.0),
       xlab = "Risk Ratio",
       slab = data$study_id,
       col.square = lancet_colors[1],    # Lancet blue
       col.diamond = lancet_colors[2],   # Lancet red
       comb.fixed = FALSE,
       comb.random = TRUE,
       print.I2 = TRUE,
       print.pval.Q = TRUE)

dev.off()
```

**Alternative: Using ggplot2 forest plot with hrbrthemes**:

```r
library(ggplot2)
library(hrbrthemes)
library(ggsci)

# Create custom forest plot data
forest_data <- data.frame(
  study = data$study_id,
  rr = exp(res$TE),
  ci_lower = exp(res$TE - 1.96 * res$seTE),
  ci_upper = exp(res$TE + 1.96 * res$seTE),
  weight = res$w.random
)

# Create ggplot forest plot with professional theme
p <- ggplot(forest_data, aes(x = rr, y = study)) +
  geom_vline(xintercept = 1, linetype = "dashed", color = "gray50") +
  geom_point(aes(size = weight), color = pal_lancet()(1)) +
  geom_errorbarh(aes(xmin = ci_lower, xmax = ci_upper), height = 0.2) +
  scale_x_log10() +
  theme_ipsum_rc() +
  labs(
    title = "Forest Plot: Pathologic Complete Response",
    x = "Risk Ratio (95% CI)",
    y = NULL,
    size = "Weight"
  )

ggsave("07_manuscript/figures/figure1_forest_ggplot.png",
       width = 10, height = 8, dpi = 300)
```

**Using forest() from meta package**:

```r
# Alternative: Simpler interface
library(meta)

res <- metabin(
  event.e, n.e, event.c, n.c,
  data = data,
  studlab = study_id,
  sm = "RR"
)

# Export forest plot
png("07_manuscript/figures/figure1_forest.png",
    width = 10, height = 8, units = "in", res = 300)
forest(res)
dev.off()
```

### 2. Multi-Panel Figures with patchwork

**Combine efficacy outcomes (pCR, EFS, OS)**:

```r
library(ggplot2)
library(patchwork)

# Create individual plots
p1 <- forest(res_pcr) + ggtitle("A. Pathologic Complete Response")
p2 <- forest(res_efs) + ggtitle("B. Event-Free Survival")
p3 <- forest(res_os) + ggtitle("C. Overall Survival")

# Combine with patchwork
combined <- p1 / p2 / p3

# Export at 300 DPI
ggsave("07_manuscript/figures/figure1_efficacy.png",
       plot = combined,
       width = 10, height = 12, dpi = 300)
```

**Using cowplot for panel labels**:

```r
library(cowplot)

# Combine with automatic panel labels
combined <- plot_grid(
  p1, p2, p3,
  labels = c("A", "B", "C"),
  ncol = 1,
  rel_heights = c(1, 1, 1)
)

# Export
ggsave("07_manuscript/figures/figure1_efficacy.png",
       plot = combined,
       width = 10, height = 12, dpi = 300)
```

### 3. Subgroup Analysis

```r
# Subgroup forest plot
res_subgroup <- metabin(
  event.e, n.e, event.c, n.c,
  data = data,
  studlab = study_id,
  subgroup = pdl1_status,
  sm = "RR"
)

png("07_manuscript/figures/figure2_subgroup.png",
    width = 12, height = 10, units = "in", res = 300)

forest(res_subgroup,
       overall = TRUE,
       overall.hetstat = TRUE,
       test.subgroup = TRUE,
       print.subgroup.name = TRUE)

dev.off()
```

### 4. Funnel Plots (Publication Bias)

```r
# Create funnel plot
png("07_manuscript/figures/figure3_funnel.png",
    width = 8, height = 8, units = "in", res = 300)

funnel(res,
       xlab = "Risk Ratio (log scale)",
       studlab = TRUE)

dev.off()

# Enhanced funnel plot with contour
library(metafor)
funnel(res,
       level = c(90, 95, 99),
       shade = c("white", "gray", "darkgray"),
       refline = 0)
```

### 5. Risk of Bias Summary

```r
library(ggplot2)
library(tidyr)

# Load RoB data
rob_data <- read.csv("03_screening/quality_rob2.csv")

# Reshape for plotting
rob_long <- rob_data %>%
  pivot_longer(
    cols = starts_with("domain"),
    names_to = "domain",
    values_to = "judgement"
  )

# Create RoB plot
p <- ggplot(rob_long, aes(x = domain, fill = judgement)) +
  geom_bar(position = "fill") +
  scale_fill_manual(
    values = c("Low" = "green", "Some concerns" = "yellow", "High" = "red")
  ) +
  labs(y = "Proportion", x = "Risk of Bias Domain") +
  theme_minimal() +
  coord_flip()

ggsave("07_manuscript/figures/figure4_rob.png",
       plot = p, width = 10, height = 6, dpi = 300)
```

---

## Best Practices

### Theme Selection Guide

**Choose theme based on target journal**:

| Journal Type              | Recommended Theme    | Color Palette             | Reason                                  |
| ------------------------- | -------------------- | ------------------------- | --------------------------------------- |
| Nature, Science, Cell     | hrbrthemes + ggsci   | `scale_color_npg()`       | Professional typography, journal colors |
| Lancet, NEJM, JAMA        | hrbrthemes           | `scale_color_lancet()`    | Medical journal standards               |
| PLOS ONE                  | ggthemr("fresh")     | viridis                   | Open access, colorblind-safe required   |
| Oncology journals         | hrbrthemes           | `scale_color_jco()`       | Specialty palette                       |
| Any journal (safe choice) | hrbrthemes + viridis | `scale_color_viridis_d()` | Accessible, professional                |

**Meta-analysis specific recommendations**:

```r
library(ggplot2)
library(hrbrthemes)
library(ggsci)

# Set up once at start of script
theme_set(theme_ipsum_rc(base_size = 12))  # Consistent theme for all plots

# For forest plots (categorical outcomes)
scale_color_lancet()  # Clear distinction between studies

# For funnel plots (continuous)
scale_color_viridis_c(option = "plasma")  # Publication bias gradient

# For subgroup analysis
scale_fill_jco()  # Multiple subgroups need distinct colors
```

### Color Palette Decision Tree

```
Need colors?
├─ Continuous variable (e.g., p-value, effect size)
│  └─ Use viridis or scico (colorblind-safe)
│     └─ ggplot(...) + scale_color_viridis_c()
│
├─ Categorical groups (2-8 groups)
│  ├─ Medical journal submission?
│  │  └─ Use ggsci journal palette
│  │     └─ scale_color_nejm() or scale_color_lancet()
│  └─ General publication?
│     └─ Use viridis discrete
│        └─ scale_color_viridis_d()
│
└─ Heatmap or intensity plot
   └─ Use scico or viridis
      └─ scale_fill_scico(palette = "bilbao")
```

### Export Settings

**Always use these settings**:

```r
# For ggplot2
ggsave("filename.png",
       width = 10,        # inches
       height = 8,        # inches
       dpi = 300,         # publication quality
       units = "in")

# For base R / meta package
png("filename.png",
    width = 10,           # inches
    height = 8,           # inches
    units = "in",
    res = 300)           # resolution

# Your plotting code here

dev.off()
```

### File Organization

```
06_analysis/
├── scripts/
│   ├── 01_forest_pcr.R          # Primary outcome
│   ├── 02_forest_secondary.R    # Secondary outcomes
│   ├── 03_subgroup.R            # Subgroup analysis
│   ├── 04_funnel.R              # Publication bias
│   └── 05_assemble_panels.R     # Multi-panel figures
└── figures/
    ├── figure1_pcr.png          # Individual plots
    ├── figure2_efs.png
    ├── figure3_os.png
    └── combined_efficacy.png    # Multi-panel

07_manuscript/
└── figures/                     # Final publication figures
    ├── figure1_efficacy.png     # 3-panel: pCR + EFS + OS
    ├── figure2_subgroup.png     # Subgroup forest plot
    ├── figure3_funnel.png       # Funnel plot
    └── figure4_rob.png          # Risk of bias summary
```

### Reproducibility

**Create master script**:

```r
# 06_analysis/generate_all_figures.R

# Set working directory
setwd("/Users/htlin/meta-pipe/06_analysis")

# Load data
source("scripts/00_load_data.R")

# Generate figures in order
source("scripts/01_forest_pcr.R")
source("scripts/02_forest_secondary.R")
source("scripts/03_subgroup.R")
source("scripts/04_funnel.R")
source("scripts/05_assemble_panels.R")

# Copy to manuscript folder
file.copy(
  list.files("figures", pattern = "^figure.*\\.png$", full.names = TRUE),
  "../07_manuscript/figures/",
  overwrite = TRUE
)

cat("All figures generated successfully!\n")
```

**Run from command line**:

```bash
cd /Users/htlin/meta-pipe/06_analysis
Rscript generate_all_figures.R
```

---

## Common Issues & Solutions

### Issue 1: Package Not Found

```r
# Error: package 'meta' not found

# Solution: Install from CRAN
install.packages("meta")

# Or check CRAN mirror
options(repos = c(CRAN = "https://cloud.r-project.org/"))
install.packages("meta")
```

### Issue 2: Font Issues in PDF Export

```r
# Error: font family not found

# Solution: Use cairo device
ggsave("figure.png", device = "png", type = "cairo")

# Or for PDF
cairo_pdf("figure.pdf", width = 10, height = 8)
# Your plot here
dev.off()
```

### Issue 3: Figure Too Small / Text Unreadable

```r
# Problem: Text too small in exported figure

# Solution: Increase base_size in theme
library(ggplot2)

p <- ggplot(data, aes(x, y)) +
  geom_point() +
  theme_minimal(base_size = 14)  # Increase from default 11

ggsave("figure.png", width = 10, height = 8, dpi = 300)
```

### Issue 4: Multi-Panel Alignment

```r
# Problem: Panels misaligned in cowplot

# Solution: Use align and axis parameters
library(cowplot)

plot_grid(
  p1, p2, p3,
  labels = c("A", "B", "C"),
  align = "v",        # Align vertically
  axis = "l",         # Align on left axis
  ncol = 1
)
```

---

## Journal-Specific Requirements

### Nature/Lancet/NEJM

- **DPI**: 300-600 for line art, 300 for photos
- **Format**: TIFF or PNG (not JPEG)
- **Fonts**: Arial or Helvetica, 6-8pt minimum
- **Width**: Single column (89mm) or double (183mm)

**R code for Lancet-style figures**:

```r
library(ggplot2)

# Lancet theme
theme_lancet <- theme_minimal(base_size = 10) +
  theme(
    text = element_text(family = "Arial"),
    axis.line = element_line(size = 0.5),
    panel.grid.minor = element_blank()
  )

# Apply to plot
p <- ggplot(data, aes(x, y)) +
  geom_point() +
  theme_lancet

# Export at journal width
ggsave("figure.png",
       width = 183, height = 150,  # mm
       units = "mm", dpi = 300)
```

### JAMA

- **DPI**: 300-600
- **Format**: TIFF preferred
- **Fonts**: Arial, 8-10pt
- **File size**: <10 MB per figure

### PLoS ONE

- **DPI**: 300-600
- **Format**: PNG, TIFF, or EPS
- **Dimensions**: Width ≤ 6.83 inches (single) or 10.05 inches (double)

---

## Quick Reference

### Package Installation

```r
# Core meta-analysis
install.packages(c("meta", "metafor", "dmetar"))

# Visualization
install.packages(c("ggplot2", "patchwork", "cowplot", "ggpubr"))

# Professional themes (RECOMMENDED for all projects)
install.packages(c(
  "hrbrthemes",   # Best typography
  "ggthemes",     # Professional themes
  "viridis",      # Colorblind-safe (MANDATORY)
  "scico",        # Scientific colormaps
  "ggsci"         # Journal palettes
))

# Install ggthemr from GitHub
# devtools::install_github("Mikata-Project/ggthemr")

# Optional: TV themes (for presentations only)
# devtools::install_github("Ryo-N7/tvthemes")

# Utilities
install.packages(c("tidyverse", "scales", "RColorBrewer"))
```

### Theme Setup Template

**Copy this to the start of every analysis script**:

```r
#!/usr/bin/env Rscript
# Setup: Load packages and set theme

# Load packages
library(ggplot2)
library(hrbrthemes)  # Typography
library(ggsci)       # Journal colors
library(viridis)     # Colorblind-safe
library(patchwork)   # Multi-panel

# Set global theme for ALL plots
theme_set(
  theme_ipsum_rc(
    base_size = 12,           # Readable text
    axis_title_size = 14,
    plot_title_size = 16
  )
)

# Now all ggplot objects inherit this theme automatically
```

### Template: Basic Forest Plot

```r
library(meta)

# Read data
data <- read.csv("05_extraction/extraction.csv")

# Meta-analysis
res <- metabin(
  event.e, n.e, event.c, n.c,
  data = data,
  studlab = study_id,
  sm = "RR"
)

# Export forest plot
png("figure.png", width=10, height=8, units="in", res=300)
forest(res)
dev.off()
```

### Template: Multi-Panel with patchwork

```r
library(patchwork)

# Combine plots
combined <- p1 / p2 / p3 +
  plot_annotation(
    title = "Efficacy Outcomes",
    tag_levels = "A"
  )

# Export
ggsave("combined.png", width=10, height=12, dpi=300)
```

---

## Additional Resources

### Tutorials

1. **Doing Meta-Analysis in R** (Harrer et al.)
   - https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/
   - Comprehensive guide for meta-analysis in R

2. **R Graphics Cookbook** (Chang)
   - https://r-graphics.org/
   - ggplot2 examples for publication

3. **Data Visualization with R** (Kabacoff)
   - https://rkabacoff.github.io/datavis/
   - Modern visualization techniques

### Getting Help

When searching for R packages or help:

1. **Search CRAN**: https://cran.r-project.org/web/packages/
2. **Search R-universe**: https://r-universe.dev/search/
3. **Stack Overflow**: Tag questions with `[r]` and `[meta-analysis]`
4. **RStudio Community**: https://community.rstudio.com/

### Package Documentation

```r
# View package help
help(package = "meta")

# View function help
?forest

# View vignettes
vignette(package = "meta")
browseVignettes("meta")
```

---

## Theme & Color Package Comparison

### When to Use Each Package

| Package        | Best For                 | Pros                                    | Cons                                    | Install |
| -------------- | ------------------------ | --------------------------------------- | --------------------------------------- | ------- |
| **hrbrthemes** | All publications         | Professional typography, minimal design | Requires font installation              | CRAN    |
| **ggthemr**    | Quick styling            | One-line setup, applies globally        | Limited customization                   | GitHub  |
| **ggthemes**   | Matching specific styles | Economist, WSJ, Tufte themes            | Some themes too stylized                | CRAN    |
| **viridis**    | Color scales             | Colorblind-safe, perceptually uniform   | Limited to continuous scales            | CRAN    |
| **scico**      | Heatmaps                 | Scientific colormaps, 30+ palettes      | Overkill for simple plots               | CRAN    |
| **ggsci**      | Medical journals         | Exact journal color matching            | Only discrete colors                    | CRAN    |
| **tvthemes**   | Presentations            | Fun, eye-catching                       | Not professional enough for publication | GitHub  |

### Complete Setup Example

**Master script for all meta-analysis figures**:

```r
#!/usr/bin/env Rscript
# master_figures.R — Generate all publication figures

# ============================================================
# SETUP: Load all packages
# ============================================================

library(meta)         # Meta-analysis
library(metafor)      # Advanced meta-analysis
library(ggplot2)      # Plotting
library(patchwork)    # Multi-panel
library(hrbrthemes)   # Professional theme
library(ggsci)        # Journal colors
library(viridis)      # Colorblind-safe
library(dplyr)        # Data manipulation

# ============================================================
# THEME CONFIGURATION
# ============================================================

# Set global theme for consistency
theme_set(
  theme_ipsum_rc(
    base_size = 12,
    axis_title_size = 14,
    plot_title_size = 16,
    strip_text_size = 12
  ) +
  theme(
    legend.position = "bottom",
    plot.title.position = "plot"
  )
)

# ============================================================
# COLOR PALETTES
# ============================================================

# Define palettes for consistency
colors_lancet <- pal_lancet()(9)      # For categorical (up to 9 groups)
colors_nejm <- pal_nejm()(8)          # For medical outcomes
colors_jco <- pal_jco()(10)           # For oncology
palette_viridis <- "plasma"           # For continuous

# ============================================================
# DATA LOADING
# ============================================================

data <- read.csv("../05_extraction/extraction.csv")

# ============================================================
# FIGURE 1: PRIMARY OUTCOME (Forest Plot)
# ============================================================

res_pcr <- metabin(
  event.e = events_pcr_ici,
  n.e = total_ici,
  event.c = events_pcr_control,
  n.c = total_control,
  data = data,
  studlab = study_id,
  sm = "RR"
)

# Export as PNG (base R plot)
png("../07_manuscript/figures/figure1_pcr.png",
    width = 10, height = 8, units = "in", res = 300)

forest(res_pcr,
       col.square = colors_lancet[1],
       col.diamond = colors_lancet[2],
       print.I2 = TRUE,
       print.pval.Q = TRUE)

dev.off()

# ============================================================
# FIGURE 2: SUBGROUP ANALYSIS (ggplot)
# ============================================================

p_subgroup <- ggplot(subgroup_data, aes(x = subgroup, y = rr, fill = subgroup)) +
  geom_col() +
  geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper), width = 0.2) +
  scale_fill_lancet() +              # Use Lancet colors
  labs(
    title = "Subgroup Analysis: Pathologic Complete Response",
    x = "Subgroup",
    y = "Risk Ratio (95% CI)"
  )

ggsave("../07_manuscript/figures/figure2_subgroup.png",
       width = 10, height = 6, dpi = 300)

# ============================================================
# FIGURE 3: PUBLICATION BIAS (Funnel Plot)
# ============================================================

funnel_data <- data.frame(
  se = res_pcr$seTE,
  effect = res_pcr$TE
)

p_funnel <- ggplot(funnel_data, aes(x = effect, y = se)) +
  geom_point(aes(color = se), size = 3) +
  geom_vline(xintercept = 0, linetype = "dashed") +
  scale_color_viridis_c(option = "plasma") +  # Colorblind-safe gradient
  scale_y_reverse() +
  labs(
    title = "Funnel Plot: Publication Bias Assessment",
    x = "Log Risk Ratio",
    y = "Standard Error",
    color = "SE"
  )

ggsave("../07_manuscript/figures/figure3_funnel.png",
       width = 8, height = 8, dpi = 300)

# ============================================================
# FIGURE 4: MULTI-PANEL (Combine all outcomes)
# ============================================================

combined <- p_pcr / p_efs / p_os +
  plot_annotation(
    title = "Efficacy Outcomes: ICI vs Control",
    tag_levels = "A"
  )

ggsave("../07_manuscript/figures/figure4_efficacy.png",
       width = 10, height = 14, dpi = 300)

# ============================================================
# SUMMARY
# ============================================================

cat("\n✅ All figures generated successfully!\n")
cat("   - Figure 1: Primary outcome (forest plot)\n")
cat("   - Figure 2: Subgroup analysis\n")
cat("   - Figure 3: Funnel plot\n")
cat("   - Figure 4: Multi-panel efficacy\n")
cat("\n📁 Output directory: 07_manuscript/figures/\n")
cat("📏 Resolution: 300 DPI (publication quality)\n")
cat("🎨 Theme: hrbrthemes + Lancet colors\n")
```

### Why These Packages Matter

**Before (default ggplot2)**:

```r
# Default ggplot2 — looks amateur
ggplot(data, aes(x, y, color = group)) +
  geom_point()
# Result: Gray background, poor contrast, generic colors
```

**After (professional themes)**:

```r
# With hrbrthemes + ggsci — publication-ready
library(hrbrthemes)
library(ggsci)

ggplot(data, aes(x, y, color = group)) +
  geom_point(size = 3) +
  scale_color_lancet() +
  theme_ipsum_rc() +
  labs(title = "Professional Figure")

# Result: Clean background, readable fonts, journal colors
# Time saved: 30-60 minutes per figure (no manual tweaking)
```

**Key Benefits**:

1. **Speed**: No trial-and-error with colors and fonts
2. **Consistency**: All figures have matching style
3. **Accessibility**: Colorblind-safe palettes prevent exclusion
4. **Credibility**: Professional appearance increases trust
5. **Journal alignment**: Match target journal aesthetics

---

**Last Updated**: 2024-02-07
**Maintainer**: See CLAUDE.md for project instructions
