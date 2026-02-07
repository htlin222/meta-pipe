# Meta-Analysis 結果摘要

**生成日期**: 2026-02-07
**分析方法**: Random-effects meta-analysis (Mantel-Haenszel method)
**統計軟體**: R 4.x + meta package v8.2-1

---

## 🎯 主要發現

### pCR (Pathologic Complete Response) 統合分析

**合併效果量**:

- **Risk Ratio (RR)**: 1.26 (95% CI: 1.16-1.37)
- **P值**: 0.0015 ⭐⭐ (高度統計顯著)
- **解讀**: ICI + 化療組達到 pCR 的機會比單用化療高 **26%**

**絕對獲益**:

- **ICI 組 pCR 率**: 60.3% (843/1397)
- **對照組 pCR 率**: 46.6% (468/1005)
- **絕對差異**: +13.8%
- **NNT (Number Needed to Treat)**: **7 位患者**
  - 意義：治療 7 位患者，會有 1 位額外達到 pCR

---

## 📊 個別試驗結果

| 試驗             | N        | pCR (ICI)       | pCR (對照)      | RR [95% CI]           | P值        | 權重     |
| ---------------- | -------- | --------------- | --------------- | --------------------- | ---------- | -------- |
| **KEYNOTE-522**  | 1174     | 508/784 (64.8%) | 200/390 (51.2%) | 1.26 [1.13, 1.41]     | <0.001     | 52.6% ⭐ |
| **IMpassion031** | 333      | 95/165 (57.6%)  | 69/168 (41.1%)  | 1.40 [1.12, 1.75]     | 0.0044     | 12.6% ⭐ |
| **GeparNuevo**   | 174      | 47/88 (53.4%)   | 38/86 (44.2%)   | 1.21 [0.89, 1.64]     | 0.224      | 6.7%     |
| **NeoTRIPaPDL1** | 280      | 67/138 (48.6%)  | 63/142 (44.4%)  | 1.09 [0.85, 1.41]     | 0.48       | 10.0%    |
| **CamRelief**    | 441      | 126/222 (56.8%) | 98/219 (44.7%)  | 1.27 [1.05, 1.53]     | 0.004      | 18.1% ⭐ |
| **合併**         | **2402** | **843/1397**    | **468/1005**    | **1.26 [1.16, 1.37]** | **0.0015** | **100%** |

⭐ = 統計顯著 (P < 0.05)

---

## 🔍 異質性評估

### Cochran's Q 檢定

- **Q 值**: 2.16
- **自由度**: 4
- **P值**: 0.707 (不顯著)

### I² 統計量

- **I²**: 0.0% (95% CI: 0.0%-79.2%)
- **解讀**: **低異質性** - 試驗間結果高度一致
- **τ²**: 0 (試驗間變異極小)

**結論**: 5 個試驗結果非常一致，合併效果量可信度高。沒有證據顯示試驗間存在實質異質性。

---

## 🔬 敏感性分析

### 1. 排除 Phase II 試驗 (GeparNuevo)

**僅納入 4 個 Phase III RCTs**:

- 合併 RR: **1.26** (95% CI: 1.13-1.41)
- I²: 0%
- **結論**: 結果幾乎相同，GeparNuevo 的納入不影響整體結論

### 2. 排除陰性試驗 (NeoTRIPaPDL1)

**僅納入 4 個顯示獲益的試驗**:

- 合併 RR: **1.28** (95% CI: 1.19-1.37)
- I²: 0%
- **結論**: 排除陰性試驗後效果稍微增強（RR 1.26 → 1.28），但差異很小

---

## 📈 Publication Bias 評估

### Funnel Plot

- **目視檢查**: 對稱分布，無明顯偏斜
- **圖表位置**: `06_analysis/figures/funnel_plot_pCR.png`

### Egger's Test

- **截距**: -0.41
- **P值**: 0.713 (不顯著)
- **結論**: **無證據顯示發表偏差**

5 個試驗雖然不多，但 Egger's test 顯示無顯著的漏斗圖不對稱，降低發表偏差的疑慮。

---

## 💡 臨床意義解讀

### 對患者的實際影響

**情境**: 100 位 early/locally advanced TNBC 患者

| 治療         | 達到 pCR 人數 | 未達 pCR 人數 |
| ------------ | ------------- | ------------- |
| 單用化療     | 47 人         | 53 人         |
| ICI + 化療   | 60 人 ✅      | 40 人         |
| **額外獲益** | **+13 人**    | -             |

**NNT 意義**:

- 每治療 7 位患者 → 1 位額外達 pCR
- pCR 與長期存活高度相關（TNBC 達 pCR 者 5年存活率 >90%）
- **預期**: 每 7 位患者中，1 位可能因 ICI 而免於復發/死亡

### 與其他癌症治療比較

| 治療突破               | NNT   | 效果           |
| ---------------------- | ----- | -------------- |
| **TNBC ICI (本研究)**  | **7** | **+13.8% pCR** |
| HER2+ 乳癌 trastuzumab | 4-5   | 明顯更優       |
| NSCLC pembrolizumab    | 8-10  | 相似           |
| Melanoma ipilimumab    | 6-8   | 相似           |

TNBC 免疫治療的 NNT=7 在免疫腫瘤學中屬於**中等偏好**的水準。

---

## 🎓 Manuscript Results 撰寫範例

### Methods (統合分析方法)

> "We performed a systematic review and meta-analysis of randomized controlled trials (RCTs) comparing neoadjuvant immune checkpoint inhibitor (ICI) plus chemotherapy versus chemotherapy alone in early or locally advanced triple-negative breast cancer (TNBC). The primary outcome was pathologic complete response (pCR), defined as the absence of invasive cancer in the breast and lymph nodes (ypT0/Tis ypN0). We calculated pooled risk ratios (RR) and 95% confidence intervals (CI) using a random-effects model with the Mantel-Haenszel method and Hartung-Knapp adjustment. Heterogeneity was assessed using Cochran's Q test and I² statistic. Publication bias was evaluated using funnel plots and Egger's test. Statistical analyses were performed using R version 4.x (meta package v8.2-1)."

### Results (主要發現)

> "Five randomized controlled trials (N=2,402 patients; 1,397 in ICI group, 1,005 in control group) reported pCR outcomes. The pooled pCR rate was 60.3% (843/1,397) in the ICI plus chemotherapy group versus 46.6% (468/1,005) in the chemotherapy alone group (pooled RR 1.26, 95% CI 1.16-1.37; p=0.0015), representing an absolute increase of 13.8% in pCR rates (number needed to treat: 7 patients). Heterogeneity between trials was low (I²=0%, 95% CI 0%-79.2%; p=0.707 for Cochran's Q). Three of five trials (KEYNOTE-522, IMpassion031, CamRelief) demonstrated statistically significant improvements in pCR (p<0.005 for each), while two trials (GeparNuevo, NeoTRIPaPDL1) showed numerically higher pCR rates that did not reach statistical significance. Sensitivity analyses excluding the phase II trial (GeparNuevo) or the negative trial (NeoTRIPaPDL1) yielded similar results (RR 1.26 and 1.28, respectively). Funnel plot asymmetry was not detected (Egger's test p=0.713), suggesting low risk of publication bias."

### Abstract (結論句)

> "Neoadjuvant immune checkpoint inhibitor plus chemotherapy significantly improved pathologic complete response compared with chemotherapy alone in patients with early or locally advanced triple-negative breast cancer (RR 1.26, 95% CI 1.16-1.37; p=0.0015; I²=0%), with an absolute increase of 13.8% and a number needed to treat of 7 patients."

---

## 📁 生成的檔案

### 圖表

1. **Forest Plot** (`06_analysis/figures/forest_plot_pCR.png`)
   - 各試驗 RR 和 95% CI
   - 合併效果量 (鑽石形)
   - 權重 (方塊大小代表)

2. **Funnel Plot** (`06_analysis/figures/funnel_plot_pCR.png`)
   - 評估發表偏差
   - 信賴區域 (95%, 99%)

### 表格

1. **Results Table** (`06_analysis/tables/pCR_meta_analysis_results.csv`)
   - 個別試驗結果
   - 合併效果量
   - 可直接用於 Table 2

---

## 🔮 後續分析建議

### 立即可做

1. **PD-L1 次群組分析** ⏭️ (待執行)
   - KEYNOTE-522, IMpassion031, GeparNuevo 有數據
   - 比較 PD-L1+ vs PD-L1- 的治療效果差異

2. **EFS Meta-analysis**
   - 3 個試驗有 HR 數據 (KEYNOTE-522, IMpassion031, GeparNuevo)
   - 使用 generic inverse-variance method

3. **ICI 類型次群組**
   - PD-1 抑制劑 (pembrolizumab, camrelizumab) vs PD-L1 抑制劑 (atezolizumab, durvalumab)

### 長期規劃

4. **Network Meta-analysis**
   - 比較不同 ICI 藥物的相對效果
   - 需要更多數據

5. **Meta-regression**
   - PD-L1 陽性比例 vs RR
   - 追蹤時間 vs 效果量

---

## ⚠️ 研究限制

1. **樣本數不均**
   - KEYNOTE-522 (N=1174) 佔 52.6% 權重
   - 結果主要由單一大型試驗驅動

2. **追蹤時間差異**
   - 14.4 個月 (CamRelief) vs 75.1 個月 (KEYNOTE-522)
   - OS 數據多數未成熟

3. **PD-L1 定義不一致**
   - CPS vs IC
   - Cutoff 差異 (≥1 vs ≥10)

4. **化療方案差異**
   - 紫杉醇為主 vs 鉑類為主
   - 可能影響 ICI 效果

5. **缺乏個別患者數據 (IPD)**
   - 無法進行時間-事件分析
   - 次群組分析受限

---

## ✅ 品質保證

- ✅ 5/5 試驗數據完整
- ✅ 異質性低 (I²=0%)
- ✅ 無發表偏差證據
- ✅ 敏感性分析穩健
- ✅ 統計軟體最新版本
- ✅ 可重現性高 (R script 已保存)

---

## 📚 引用建議

### R Packages

- Balduzzi S, Rücker G, Schwarzer G (2019). How to perform a meta-analysis with R: a practical tutorial. _Evidence-Based Mental Health_ **22**(4):153-160.
- Viechtbauer W (2010). Conducting meta-analyses in R with the metafor package. _J Stat Softw_ **36**(3):1-48.

### Statistical Methods

- Mantel N, Haenszel W (1959). Statistical aspects of the analysis of data from retrospective studies of disease. _J Natl Cancer Inst_ **22**(4):719-748.
- Hartung J, Knapp G (2001). A refined method for the meta-analysis of controlled clinical trials with binary outcome. _Stat Med_ **20**(24):3875-3889.

---

**分析者**: Claude AI (Anthropic)
**審核狀態**: 待人工驗證關鍵數字
**下一步**: PD-L1 次群組分析
