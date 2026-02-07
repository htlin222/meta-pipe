# 圖表產生工作流程更新：從 Python 轉換至 R

**更新日期**: 2024-02-07
**狀態**: ✅ 完成
**影響範圍**: 所有圖表產生與組裝工作流程

---

## 📋 總結

本次更新將整個 meta-analysis 專案的圖表產生工作流程從 Python (PIL/Pillow) 轉換為 R (ggplot2/patchwork/cowplot)，以提高重現性、整合性與發表品質。

---

## 🎯 主要變更

### 1. 新增文件

#### `/Users/htlin/meta-pipe/docs/R_FIGURE_GUIDE.md` (630+ 行)

**內容**:

- R 套件生態系統參考 (CRAN, Bioconductor, Tidyverse, rOpenSci, R-universe)
- 完整工作流程範例 (森林圖、多面板圖、亞組分析)
- 發表品質匯出設定 (ggsave, dpi=300)
- 期刊特定要求 (Nature/Lancet/JAMA)
- 疑難排解指南
- 專業主題套件 (ggthemr, hrbrthemes, viridis, ggsci)

**使用時機**:

- Stage 06 (Analysis): 產生所有統計圖表
- Stage 07 (Manuscript): 組裝多面板圖表

**套件資源**:

1. **CRAN** (cran.r-project.org) — R 套件官方總倉庫
2. **Bioconductor** (bioconductor.org) — 生物資訊學專用套件庫
3. **Tidyverse** (tidyverse.org) — 資料科學核心套件群 (dplyr、ggplot2)
4. **rOpenSci** (ropensci.org) — 經同儕審查的科學研究套件
5. **R-universe** (r-universe.dev) — 新一代套件搜尋整合平台

---

### 2. 更新現有文件

#### `CLAUDE.md` (主要代理指令檔)

**變更**:

- 新增 "R Figure Generation" 到 Essential 文件列表
- Stage 06 (Analysis) 現在強調 **R-only 工作流程**
- 移除 Python 圖表產生參考
- 新增 R 套件資源連結
- 加入 `ggsave()` 範例 (300 DPI 要求)

**關鍵指令更新**:

```r
# 原本 (Python)
# python assemble_figures.py figure1.png vertical ...

# 現在 (R)
library(patchwork)
combined <- p1 / p2 / p3
ggsave("figure1.png", width=10, height=12, dpi=300)
```

---

#### `docs/MANUSCRIPT_ASSEMBLY.md`

**變更**:

- Phase 3 (Figure Assembly) 現在使用 R 套件 (patchwork, cowplot)
- 移除 Python PIL/Pillow 參考
- 新增 R 多面板組裝範例
- 更新最佳實踐：使用 R `ggsave()`
- 新增「不要使用 Python 繪圖」指南

**新工作流程**:

```r
# 使用 patchwork 組合圖表
library(patchwork)

# 垂直排列
combined <- p1 / p2 / p3

# 水平排列
combined <- p1 | p2 | p3

# 網格排列 (2x2)
combined <- (p1 | p2) / (p3 | p4)

# 匯出
ggsave("figure.png", width=10, height=12, dpi=300)
```

---

#### `~/.claude/skills/scientific-figure-assembly/SKILL.md`

**變更**:

- 技能描述改為強調 R 工作流程
- `allowed-tools` 改為包含 `Rscript`
- 重新結構化內容：
  - **推薦**: Method 1: patchwork (ggplot2)
  - **推薦**: Method 2: cowplot (通用)
  - **不推薦**: Python 方法 (標記為 Legacy)

**新範例**:

```r
# 完整 meta-analysis 森林圖組裝
library(meta)
library(patchwork)

# 建立個別圖表
res_pcr <- metabin(event.e, n.e, event.c, n.c, data=data)
res_efs <- metagen(TE, seTE, data=data)
res_os <- metagen(TE, seTE, data=data)

# 組合
combined <- forest(res_pcr) / forest(res_efs) / forest(res_os) +
  plot_annotation(tag_levels = "A")

# 匯出 300 DPI
ggsave("figure1_efficacy.png", width=10, height=14, dpi=300)
```

---

## 📦 R 套件依賴

### 核心套件 (必裝)

```r
# Meta-analysis
install.packages(c("meta", "metafor", "dmetar"))

# 視覺化
install.packages(c("ggplot2", "patchwork", "cowplot"))
```

### 專業主題套件 (建議)

```r
# 色彩與主題
install.packages(c(
  "viridis",      # 色盲友善色彩
  "scico",        # 科學色彩圖
  "ggsci",        # 期刊色彩方案 (Nature, NEJM, Lancet)
  "ggthemes",     # 專業主題 (Economist, WSJ)
  "hrbrthemes"    # 排版專注主題
))

# ggthemr 需從 GitHub 安裝
# devtools::install_github("Mikata-Project/ggthemr")
```

---

## 🔄 工作流程比較

### 舊工作流程 (Python)

```bash
# Step 1: R 產生個別圖表
Rscript 01_forest_plot.R  # 產生 forest_plot.png

# Step 2: Python 組裝
uv run python assemble_figures.py figure1.png vertical \
  forest_pcr.png forest_efs.png forest_os.png

# 問題:
# - 需要切換語言 (R → Python)
# - 額外依賴 (Pillow)
# - 難以整合統計資訊
```

### 新工作流程 (R)

```r
# 全程在 R 中完成
library(meta)
library(patchwork)

# Step 1: 分析與繪圖
res_pcr <- metabin(...)
res_efs <- metagen(...)
res_os <- metagen(...)

# Step 2: 組裝 (同一個 R session)
combined <- forest(res_pcr) / forest(res_efs) / forest(res_os)

# Step 3: 匯出
ggsave("figure1.png", width=10, height=14, dpi=300)

# 優點:
# ✅ 單一語言 (R)
# ✅ 無需外部依賴
# ✅ 直接整合統計結果
# ✅ 更易重現
```

---

## 📊 圖表類型範例

### 1. 森林圖 (Forest Plots)

```r
library(meta)

# 二元結局 (RR, OR)
res <- metabin(event.e, n.e, event.c, n.c, data=data, sm="RR")

# 連續結局 (HR from log-HR)
res <- metagen(TE=log_hr, seTE=se_log_hr, data=data, sm="HR")

# 匯出
png("forest_plot.png", width=10, height=8, units="in", res=300)
forest(res)
dev.off()
```

### 2. 多面板組合 (使用 patchwork)

```r
library(patchwork)

# 垂直排列 (常見於 meta-analysis)
figure1 <- p_pcr / p_efs / p_os +
  plot_annotation(
    title = "Figure 1. Efficacy Outcomes",
    tag_levels = "A"
  )

ggsave("figure1.png", width=10, height=14, dpi=300)

# 網格排列 (2x2 亞組分析)
figure2 <- (p_age | p_sex) / (p_stage | p_histology) +
  plot_annotation(tag_levels = "A")

ggsave("figure2.png", width=14, height=12, dpi=300)
```

### 3. 漏斗圖 (Publication Bias)

```r
# 基本漏斗圖
funnel(res, studlab=TRUE)

# 加強型漏斗圖 (contour-enhanced)
library(metafor)
funnel(res,
       level = c(90, 95, 99),
       shade = c("white", "gray", "darkgray"),
       refline = 0)

# 匯出
ggsave("funnel_plot.png", width=8, height=8, dpi=300)
```

### 4. 使用專業主題

```r
library(ggsci)
library(viridis)

# 使用 Lancet 色彩方案
p <- ggplot(data, aes(x, y, color=group)) +
  geom_point() +
  scale_color_lancet() +
  theme_minimal(base_size=12)

# 使用色盲友善色彩 (必須!)
p <- ggplot(data, aes(x, y, fill=value)) +
  geom_tile() +
  scale_fill_viridis_c(option="viridis") +
  theme_minimal()

ggsave("figure.png", width=10, height=8, dpi=300)
```

---

## 🎨 期刊特定要求

### Nature, Science, Cell

```r
# 使用 Arial/Helvetica 字型
library(ggplot2)

theme_nature <- theme_minimal(base_size=10) +
  theme(
    text = element_text(family="Arial"),
    axis.line = element_line(size=0.5),
    panel.grid.minor = element_blank()
  )

p <- ggplot(...) + theme_nature

# 匯出為期刊寬度 (單欄 89mm, 雙欄 183mm)
ggsave("figure.png",
       width=183, height=150, units="mm", dpi=300)
```

### Lancet (使用 ggsci 套件)

```r
library(ggsci)

p <- ggplot(data, aes(x, y, color=group)) +
  geom_point() +
  scale_color_lancet() +  # Lancet 官方色彩
  theme_minimal(base_size=10)

ggsave("figure.png", width=183, units="mm", dpi=300)
```

### JAMA

```r
# JAMA 要求
# - 300-600 DPI
# - TIFF 格式優先
# - Arial 字型 8-10pt

ggsave("figure.tiff",
       width=10, height=8, dpi=600,
       compression="lzw")
```

---

## ✅ 品質檢查清單

### 匯出前檢查

- [ ] 所有圖表使用 `dpi=300` 或更高
- [ ] 面板標籤 (A, B, C) 正確且清晰
- [ ] 字型大小在最終印刷尺寸下可讀 (≥8pt)
- [ ] 使用色盲友善色彩 (viridis/scico)
- [ ] 軸標籤、圖例完整
- [ ] 檔案大小合理 (<10 MB for PNG)

### R 腳本品質

- [ ] 所有套件明確載入 (`library()`)
- [ ] 可重現 (沒有硬編碼路徑)
- [ ] 註解清楚
- [ ] 使用 `here::here()` 或相對路徑
- [ ] 版本控制 (git commit R scripts)

---

## 🔧 疑難排解

### 問題 1: 套件找不到

```r
# 錯誤: package 'patchwork' not found

# 解決: 從 CRAN 安裝
install.packages("patchwork")

# 或檢查 CRAN mirror
options(repos = c(CRAN = "https://cloud.r-project.org/"))
install.packages("patchwork")
```

### 問題 2: 字型問題

```r
# 錯誤: font family not found

# 解決: 使用 cairo device
ggsave("figure.png", device="png", type="cairo")

# 或對於 PDF
cairo_pdf("figure.pdf", width=10, height=8)
# 你的圖表程式碼
dev.off()
```

### 問題 3: 文字太小

```r
# 問題: 匯出後文字無法閱讀

# 解決: 增加 base_size
p <- ggplot(data, aes(x, y)) +
  geom_point() +
  theme_minimal(base_size=14)  # 從預設 11 增加

ggsave("figure.png", width=10, height=8, dpi=300)
```

### 問題 4: 面板對齊問題

```r
# 使用 cowplot 的 align 參數
library(cowplot)

plot_grid(
  p1, p2, p3,
  labels = c("A", "B", "C"),
  align = "v",        # 垂直對齊
  axis = "l",         # 左軸對齊
  ncol = 1
)
```

---

## 📚 學習資源

### 線上書籍

1. **Doing Meta-Analysis in R** (Harrer et al.)
   - https://bookdown.org/MathiasHarrer/Doing_Meta_Analysis_in_R/
   - 使用 R 進行 meta-analysis 的完整指南

2. **R Graphics Cookbook** (Chang)
   - https://r-graphics.org/
   - ggplot2 發表級圖表範例

3. **Data Visualization with R** (Kabacoff)
   - https://rkabacoff.github.io/datavis/
   - 現代視覺化技術

### 套件文件

```r
# 檢視套件說明
help(package = "patchwork")

# 檢視函數說明
?ggsave

# 檢視 vignettes
vignette(package = "patchwork")
browseVignettes("patchwork")
```

### 線上資源

- **patchwork**: https://patchwork.data-imaginist.com/
- **cowplot**: https://wilkelab.org/cowplot/
- **ggplot2**: https://ggplot2.tidyverse.org/
- **metafor**: https://www.metafor-project.org/

---

## 🚀 下一步

### 現有專案遷移

如果你有現有的 Python 圖表組裝腳本：

1. **保留原始 R 繪圖腳本** (如 `01_forest_plot.R`)
2. **移除 Python 組裝步驟**
3. **在 R 腳本中直接使用 patchwork 組合**
4. **測試輸出品質** (檢查 DPI, 對齊, 標籤)
5. **更新文件** (記錄新工作流程)

### 新專案

1. **從 R 開始** - 不要產生中間 PNG 檔案
2. **在 R session 中組合** - 使用 patchwork/cowplot
3. **單次匯出** - 直接匯出最終圖表
4. **版本控制 R 腳本** - 而非 PNG 檔案

---

## 📝 Commit 資訊

本次更新包含以下 commits:

### meta-pipe 專案

1. **Switch figure generation from Python to R** (8125281)
   - 建立 R_FIGURE_GUIDE.md (450+ 行)
   - 更新 CLAUDE.md (Stage 06 強調 R)
   - 更新 MANUSCRIPT_ASSEMBLY.md (移除 Python)

2. **Add professional R theme packages to figure guide** (5cd84f2)
   - Linter 自動加入專業主題套件文件
   - viridis, scico, ggsci, ggthemr, hrbrthemes

### skills 倉庫

1. **Update scientific-figure-assembly skill to use R** (4a33027)
   - 改為 R-first 工作流程
   - Python 方法標記為 Legacy
   - 新增完整 R 範例

---

## 🎯 影響評估

### 正面影響

✅ **單一語言工作流程** - 全程在 R 中完成，減少上下文切換
✅ **更好整合** - 統計分析與視覺化無縫整合
✅ **發表品質** - R 套件預設即為發表品質
✅ **易於重現** - 單一 R 腳本即可重現所有圖表
✅ **更易維護** - 減少依賴 (不需 Python Pillow)
✅ **更好文件** - R 社群文件豐富 (CRAN, R-universe)

### 學習曲線

⚠️ **需學習 patchwork/cowplot** - 但語法簡單直觀
⚠️ **R 套件生態** - 需熟悉 CRAN, Bioconductor 等資源
✅ **有豐富範例** - R_FIGURE_GUIDE.md 提供完整範例

### 向後相容性

⚠️ **Python 腳本仍可用** - 標記為 Legacy，但仍可執行
⚠️ **現有圖表需重新產生** - 建議使用 R 重新產生以統一工作流程
✅ **漸進式遷移** - 可逐步將 Python 腳本轉換為 R

---

## 📧 支援

如有問題，請參考：

1. **R_FIGURE_GUIDE.md** - 完整工作流程與疑難排解
2. **MANUSCRIPT_ASSEMBLY.md** - 手稿組裝指南
3. **CLAUDE.md** - 主要代理指令
4. **R 套件文件** - 使用 `?function_name` 或 `help(package="package_name")`

---

**更新完成日期**: 2024-02-07
**下次審查**: 專案完成後進行技能泛化
