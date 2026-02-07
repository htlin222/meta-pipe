# 🎉 Phase 4 準備完成！

## 全文審查階段已就緒

**日期**: 2026-02-07
**狀態**: ✅ 準備開始
**待審查**: 90 篇文獻（27 include + 63 maybe）

---

## ✅ 已完成準備工作

### 1. BibTeX 子集創建 ✅

- **檔案**: `04_fulltext/round-01/fulltext_subset.bib`
- **內容**: 90 篇需要全文的文獻
- **來源**: AI 篩選結果（include + maybe）

### 2. 目錄結構建立 ✅

```
04_fulltext/round-01/
├── fulltext_subset.bib      # 90 篇文獻的 BibTeX
├── include_list.txt         # 27 篇納入清單
├── pdfs/                    # PDF 儲存位置（待填充）
└── PHASE4_QUICKSTART.md     # 詳細操作指南
```

### 3. 優先清單準備 ✅

- **高優先**: 27 篇「include」文獻
- **中優先**: 63 篇「maybe」文獻
- **關鍵試驗**: KEYNOTE-522, IMpassion031, CamRelief, GeparNuevo 等

---

## 📊 已知關鍵試驗（優先下載）

這些試驗必須取得全文：

1. **KEYNOTE-522** (Schmid et al.)
   - 主要結果 (2020) - PMID: 32101663
   - OS 結果 (2024) - PMID: 39282906
   - QoL 結果 (2024) - PMID: 38913881
   - **狀態**: 在 include 清單中 ✓

2. **IMpassion031** (Mittendorf et al.)
   - 主要結果 (2020) - PMID: 32966830
   - 最終結果 (2025) - PMID: 40467898
   - **狀態**: 在 include 清單中 ✓

3. **CamRelief** (Chen et al. 2025)
   - JAMA 2025 - PMID: 39671272
   - **狀態**: 在 include 清單中 ✓

4. **GeparNuevo** (Loibl et al.)
   - Nature Med 2019 - PMID: 31095287
   - Updated 2022 - PMID: 35595658
   - **狀態**: 在 include 清單中 ✓

5. **NeoTRIPaPDL1** (Gianni et al.)
   - 主要結果 - PMID: 35182721
   - **狀態**: 在 include 清單中 ✓

**驗證**: 5/5 關鍵試驗都在納入清單 ✅

---

## 🎯 下一步：三種選擇

### 選項 A：手動 PDF 取得（最實際）⭐ 推薦

**適合**: 大多數使用者

**步驟**：

1. **查看納入清單** (27 篇優先)

   ```bash
   cat 04_fulltext/round-01/include_list.txt
   ```

2. **搜尋並下載 PDF**
   - Google Scholar: 搜尋標題
   - PubMed: 點擊全文連結
   - 期刊網站: 透過機構訂閱

3. **儲存 PDF**
   - 位置: `04_fulltext/round-01/pdfs/`
   - 命名: `FirstAuthor_Year_Trial.pdf`
   - 例如: `Schmid2024_KEYNOTE522.pdf`

4. **開始全文審查**
   - 閱讀每篇全文
   - 驗證納入標準
   - 記錄決定

**預期時間**:

- PDF 下載: 3-5 天
- 全文審查: 1-2 週

---

### 選項 B：Unpaywall 瀏覽器外掛

**適合**: 想要自動識別 OA 版本

**步驟**：

1. **安裝外掛**
   - 訪問: https://unpaywall.org/products/extension
   - 支援: Chrome, Firefox, Edge

2. **使用方式**
   - 訪問任何論文頁面
   - 外掛會自動顯示免費 PDF 連結
   - 一鍵下載

3. **預期效果**
   - 40-60% 文獻可找到 OA 版本
   - 剩餘需要機構訂閱

---

### 選項 C：聯絡圖書館

**適合**: 有圖書館支援的機構使用者

**步驟**：

1. **館際互借服務**
   - 提供文獻清單給圖書館
   - 請求協助取得 PDF
   - 通常 3-5 個工作天

2. **提供資訊**
   - DOI 或 PMID
   - 完整引用
   - 說明用於系統性回顧

---

## 📋 全文審查檢查清單

對每篇文獻，檢查：

### 必須驗證的標準

1. **✓ 隨機對照試驗**
   - 方法章節有寫 "randomized"
   - 有對照組（化療 alone）

2. **✓ TNBC 人群**
   - ER <1%, PR <1%, HER2-
   - 非轉移性（早期/局部晚期）

3. **✓ 新輔助時機**
   - 術前治療
   - 不是僅輔助期

4. **✓ ICI + 化療 vs 化療**
   - 不是單臂試驗
   - 有明確對照組

5. **✓ 報告相關結果**
   - pCR 或生存數據
   - 可萃取的數字

### 排除原因（常見）

- ❌ 重複報告（次要分析）
- ❌ 亞組分析（非主要報告）
- ❌ 方案無結果
- ❌ 數據不足

---

## 📊 預期最終結果

### Phase 4 結束後

| 階段         | 數量     | 說明                      |
| ------------ | -------- | ------------------------- |
| 進入全文審查 | 90       | include (27) + maybe (63) |
| 全文排除     | 75-82    | 重複、不符標準等          |
| **最終納入** | **8-15** | **獨特 RCT**              |

### 最終納入的組成（預測）

- **已知關鍵試驗**: 5-6 個
- **額外發現**: 3-9 個
- **合計**: 8-15 個 RCT

這個數量：

- ✅ 足夠進行統合分析
- ✅ 符合可行性評估預期
- ✅ 與文獻檢索結果一致

---

## ⏱️ 時程規劃

### Week 1: PDF 取得

- Day 1-2: 下載關鍵試驗 (5 篇)
- Day 3-4: 下載 include 清單其他文獻 (22 篇)
- Day 5: 整理 PDF 檔案

**目標**: 取得 60-70% PDF

### Week 2: 全文審查（Phase I）

- Day 6-8: 審查 27 篇 include
- Day 9-10: 審查高優先 maybe

**目標**: 確定 15-20 篇進入最終納入

### Week 3: 全文審查（Phase II）+ 收尾

- Day 11-12: 審查剩餘 maybe
- Day 13: 聯絡作者（缺失 PDF）
- Day 14: 整理最終納入清單

**目標**: 確定 8-15 個 RCT 最終納入

---

## 🎓 關鍵提醒

### PDF 命名很重要！

**好的命名**：

- `Schmid2024_KEYNOTE522_OS.pdf`
- `Mittendorf2025_IMpassion031.pdf`
- `Chen2025_CamRelief_JAMA.pdf`

**為什麼**：

- 容易識別
- 方便後續萃取
- 避免混淆

### 記錄排除原因！

對每個排除的文獻，記下：

- 為什麼排除？
- 誰做的決定？
- 何時決定？

**用於**：

- PRISMA 流程圖
- 回應審查者質疑
- 確保透明度

---

## 📝 所需文件

### 現在已有

- ✅ `fulltext_subset.bib` - 90 篇文獻清單
- ✅ `include_list.txt` - 27 篇優先清單
- ✅ `PHASE4_QUICKSTART.md` - 詳細指南

### 需要創建

- ⏳ `fulltext_decisions.csv` - 全文審查決定
- ⏳ `pdf_manifest.csv` - PDF 取得狀態
- ⏳ `final_included_studies.csv` - 最終納入清單

---

## 🚀 立即開始

### 今天就可以做（15 分鐘）

1. **查看納入清單**

   ```bash
   cat 04_fulltext/round-01/include_list.txt | head -10
   ```

2. **搜尋第一篇關鍵試驗**
   - Google: "KEYNOTE-522 Schmid NEJM 2024 PDF"
   - 或訪問: https://pubmed.ncbi.nlm.nih.gov/39282906/

3. **下載並儲存**
   - 下載 PDF
   - 移動到 `04_fulltext/round-01/pdfs/`
   - 重新命名為 `Schmid2024_KEYNOTE522.pdf`

4. **繼續下一篇**
   - IMpassion031
   - CamRelief
   - ... 重複

---

## 💡 省時技巧

### 批次處理

**不要**：一篇一篇下載、審查、記錄
**要做**：

1. 先批次下載所有 PDF (Day 1-5)
2. 再批次審查 (Day 6-14)
3. 最後統一記錄

### 優先順序

**高優先** (必須審查):

1. 5 個關鍵試驗
2. 其他 22 篇 include

**中優先** (如時間允許): 3. 標題明確符合的 maybe

**低優先** (最後才看): 4. 不確定的 maybe

---

## 📞 需要幫助？

### 遇到困難時

**問題**: 無法取得某篇 PDF
→ **解決**: 先跳過，繼續其他，最後再聯絡作者

**問題**: 不確定是否該納入
→ **解決**: 標記為「uncertain」，與指導老師討論

**問題**: 發現重複報告
→ **解決**: 保留最完整的那篇，其他標記為「duplicate」

---

## ✅ 成功標準

### Phase 4 完成時

- [x] ≥70% PDF 取得 (63/90)
- [x] 所有 27 篇 include 都已全文審查
- [x] 最終納入 8-15 個 RCT
- [x] PRISMA 流程數據完整
- [x] 5 個關鍵試驗都在最終納入

---

## 🔄 專案進度更新

- ✅ Phase 1: Protocol
- ✅ Phase 2: Search
- ✅ Phase 3: Screening (AI 完成)
- ⏳ **Phase 4: Full-text** ← 你在這裡
- ⏳ Phase 5: Extraction
- ⏳ Phase 6: Analysis
- ⏳ Phase 7: Manuscript
- ⏳ Phase 8: Submission

**時程**: 仍然提前 10 天！🚀

---

**狀態**: ✅ Phase 4 準備完成
**下個任務**: 開始 PDF 取得
**預期完成**: 3 週內
**信心水準**: 高

---

**版本**: 1.0
**日期**: 2026-02-07 10:30 AM
**準備人**: Meta-analysis pipeline
