# Phase 4: 全文審查快速開始

## TNBC 新輔助免疫療法系統性回顧

**日期**: 2026-02-07
**階段**: Phase 4 - 全文取得與審查
**待審查文獻**: 90 篇（27 納入 + 63 maybe）

---

## 📊 當前狀態

### 已完成

- ✅ 標題/摘要 AI 篩選：122 → 90 篇
- ✅ BibTeX 子集創建：`04_fulltext/round-01/fulltext_subset.bib`
- ✅ 準備 PDF 下載目錄

### 待完成

- ⏳ 取得 PDF 檔案（~90 篇）
- ⏳ 全文審查驗證納入標準
- ⏳ 最終納入決定（預期 8-15 個 RCT）

---

## 🎯 Phase 4 目標

### 主要任務

1. **PDF 取得** (3-5 天)
   - 自動檢索 Open Access PDF（Unpaywall）
   - 手動下載需訂閱的文獻
   - 預期 40-60% 可自動取得

2. **全文審查** (1-2 週)
   - 閱讀全文驗證納入標準
   - 記錄排除原因
   - 識別重複報告

3. **最終納入清單** (2-3 天)
   - 整理最終納入的 RCT
   - 記錄 PRISMA 流程數據
   - 準備進入資料萃取

---

## 📁 檔案結構

```
04_fulltext/round-01/
├── fulltext_subset.bib          # 90 篇需要全文的文獻 ✅
├── unpaywall_results.csv        # Unpaywall OA 狀態（待建立）
├── unpaywall_summary.md         # OA 統計摘要（待建立）
├── pdf_download.log             # PDF 下載記錄（待建立）
├── pdfs/                        # PDF 檔案儲存位置
│   ├── Schmid2024_KEYNOTE522.pdf
│   ├── Mittendorf2025_IMpassion031.pdf
│   └── ... (待下載)
└── fulltext_decisions.csv       # 全文審查決定（待建立）
```

---

## 🚀 Step 1: PDF 自動檢索（推薦）

### Option A: 使用 Unpaywall API（免費）

Unpaywall 可以找到 40-60% 的 Open Access PDF。

**手動方法（由於 API 問題）**：

1. **訪問 Unpaywall 網站**
   - 安裝瀏覽器外掛：https://unpaywall.org/products/extension
   - 當訪問論文頁面時，會自動顯示 OA 版本

2. **從文獻清單開始**：

   ```bash
   # 查看需要下載的文獻清單
   grep ",include," 03_screening/round-01/decisions_screened.csv | cut -d',' -f5,8
   ```

3. **優先下載關鍵試驗**：
   - KEYNOTE-522 (多篇)
   - IMpassion031
   - CamRelief
   - GeparNuevo
   - 其他納入的 27 篇

---

## 🔍 Step 2: 手動 PDF 取得

對於非 OA 文獻：

### 方法 1: 機構訂閱存取

1. **透過圖書館代理**
   - 連接 VPN（如果在校外）
   - 訪問期刊網站
   - 直接下載 PDF

2. **主要出版商**：
   - NEJM, JAMA系列
   - Lancet Oncology
   - Nature Medicine
   - ESMO Open
   - Annals of Oncology

### 方法 2: 聯絡作者

對於無法取得的文獻：

1. 找通訊作者 email
2. 發送禮貌請求：

```
Subject: Request for full text: [Paper Title]

Dear Dr. [Author],

I am conducting a systematic review on neoadjuvant immunotherapy
for triple-negative breast cancer. I would greatly appreciate if
you could share a PDF of your publication:

[Full Citation]

This will be used solely for academic purposes in our meta-analysis.

Thank you for your consideration.

Best regards,
[Your Name]
```

### 方法 3: ResearchGate / Academia.edu

許多作者會在這些平台分享論文。

---

## 📋 Step 3: 組織 PDF 檔案

### 命名規範

建議格式：`FirstAuthor_Year_TrialName.pdf`

範例：

- `Schmid2024_KEYNOTE522_OS.pdf`
- `Mittendorf2025_IMpassion031_Final.pdf`
- `Chen2025_CamRelief.pdf`
- `Loibl2022_GeparNuevo.pdf`

### 儲存位置

```bash
04_fulltext/round-01/pdfs/
```

---

## ✅ Step 4: 全文審查流程

### 審查檢查清單

對每篇全文，驗證：

#### 1. 研究設計 ✓

- [ ] 確認是隨機對照試驗
- [ ] 確認有對照組（化療 alone）
- [ ] 檢查樣本數（每組 ≥20 人）

#### 2. 人群 ✓

- [ ] 確認是 TNBC（ER <1%, PR <1%, HER2-）
- [ ] 確認是早期/局部晚期（非轉移性）
- [ ] 檢查是否有非 TNBC 混合（如有，是否報告 TNBC 亞組）

#### 3. 介入 ✓

- [ ] 確認新輔助時機（術前）
- [ ] 確認 ICI + 化療 vs 化療
- [ ] 記錄 ICI 類型（pembrolizumab, atezolizumab等）

#### 4. 結果 ✓

- [ ] 確認報告 pCR 或生存結果
- [ ] 檢查是否有可萃取的數據
- [ ] 確認不是僅有方案無結果

#### 5. 重複檢查 ✓

- [ ] 檢查是否與其他納入文獻重複
- [ ] 如是同一試驗的不同報告，標註關係

### 決定類別

- **✅ Include**: 符合所有納入標準，進入資料萃取
- **❌ Exclude**: 不符合標準，記錄原因
  - Wrong population (非 TNBC)
  - Wrong intervention (非新輔助/無 ICI)
  - Wrong comparator (無對照組)
  - Wrong study design (非 RCT)
  - Insufficient data (無可萃取數據)
  - Duplicate (重複報告)

---

## 📝 Step 5: 記錄全文審查結果

創建 `fulltext_decisions.csv`：

```csv
record_id,title,pdf_obtained,fulltext_decision,exclusion_reason_fulltext,notes_fulltext
Schmid2024_OS,Overall Survival with Pembrolizumab...,yes,include,,KEYNOTE-522 OS results
Mittendorf2025,Peri-operative atezolizumab...,yes,include,,IMpassion031 final
Chen2025,Camrelizumab vs Placebo...,yes,include,,CamRelief JAMA
...
```

---

## 📊 預期結果

### PDF 取得率

| 來源             | 預期比例 | 數量（90篇中） |
| ---------------- | -------- | -------------- |
| Open Access 自動 | 40-50%   | 36-45 篇       |
| 機構訂閱         | 30-40%   | 27-36 篇       |
| 作者請求         | 5-10%    | 5-9 篇         |
| 無法取得         | 5-10%    | 5-9 篇         |

### 全文審查後

| 決定     | 預期數量 | 百分比 |
| -------- | -------- | ------ |
| 最終納入 | 8-15 RCT | 9-17%  |
| 全文排除 | 75-82    | 83-91% |

**主要排除原因**（全文階段）：

1. 重複報告（同一試驗的次要分析）：~40%
2. 亞組分析不符標準：~20%
3. 方案無結果：~15%
4. 數據不足以萃取：~10%
5. 其他：~15%

---

## 🕐 時間規劃

### Week 1 (Day 1-5)

| 天數    | 任務                            | 時間     |
| ------- | ------------------------------- | -------- |
| Day 1-2 | PDF 自動檢索 + 手動下載關鍵試驗 | 4-6 小時 |
| Day 3-4 | 繼續 PDF 取得（機構訂閱）       | 3-4 小時 |
| Day 5   | 整理 PDF，建立檔案命名          | 1-2 小時 |

**Week 1 目標**: 取得 60-70 篇 PDF

### Week 2 (Day 6-10)

| 天數     | 任務                           | 時間      |
| -------- | ------------------------------ | --------- |
| Day 6-8  | 全文審查第一輪（27 include）   | 8-10 小時 |
| Day 9-10 | 全文審查第二輪（maybe 高優先） | 6-8 小時  |

**Week 2 目標**: 審查完成 40-50 篇

### Week 3 (Day 11-14)

| 天數      | 任務                 | 時間     |
| --------- | -------------------- | -------- |
| Day 11-12 | 完成剩餘 maybe 審查  | 4-6 小時 |
| Day 13    | 聯絡作者請求缺失 PDF | 2-3 小時 |
| Day 14    | 整理最終納入清單     | 2-3 小時 |

**Week 3 目標**: 完成全文審查，確定最終納入

---

## 🎯 成功標準

### 必須達成

- [ ] ≥80% PDF 取得率（72/90 篇）
- [ ] 所有 27 篇「include」都有全文審查
- [ ] 最終納入 5-15 個獨特 RCT
- [ ] 所有排除都有明確原因
- [ ] 關鍵試驗（5個）都在最終納入清單

### 品質檢查

- [ ] 沒有明顯符合標準的 RCT 被排除
- [ ] 重複報告都已識別並連結
- [ ] PRISMA 流程數據準備完整

---

## 📞 遇到問題？

### PDF 取得困難

**問題**: 無法透過機構存取

- **解決**: 聯絡圖書館館際互借服務
- **備案**: 直接聯絡作者

**問題**: 會議摘要沒有全文

- **解決**: 檢查是否有後續完整出版
- **決定**: 如僅摘要但數據充分，可納入並註記

### 全文審查疑問

**問題**: 混合人群但有 TNBC 亞組

- **決定**: 如亞組數據可單獨萃取，納入

**問題**: 同一試驗多篇報告

- **決定**:
  - 主要結果 pCR：納入主要出版
  - 更新追蹤（OS）：納入最新報告
  - 次要分析：視是否有新數據

**問題**: 數據不完整

- **決定**:
  - 聯絡作者請求補充數據
  - 如無回應，決定是否排除

---

## 🔄 與其他階段的連接

### 往前（Phase 3 篩選）

- 輸入：`03_screening/round-01/decisions_screened.csv`
- 90 篇需要全文（include + maybe）

### 往後（Phase 5 萃取）

- 輸出：`04_fulltext/round-01/fulltext_decisions.csv`
- 8-15 個最終納入 RCT
- 輸入到資料萃取階段

---

## 📝 PRISMA 流程圖數據

記錄以下數據（用於 PRISMA 圖）：

- 進入全文審查：90 篇
- 全文排除：\_\_ 篇
  - 錯誤人群：\_\_ 篇
  - 錯誤介入：\_\_ 篇
  - 錯誤設計：\_\_ 篇
  - 重複報告：\_\_ 篇
  - 數據不足：\_\_ 篇
- **最終納入分析**：** 8-15 個 RCT**

---

## ✅ 下一步行動

### 今天（立即開始）

1. **查看納入的 27 篇清單**

   ```bash
   grep ",include," 03_screening/round-01/decisions_screened.csv | cut -d',' -f5,8 | head -10
   ```

2. **開始下載關鍵試驗 PDF**
   - 搜尋「KEYNOTE-522 pdf」
   - 搜尋「IMpassion031 pdf」
   - 搜尋「CamRelief JAMA 2025 pdf」

3. **儲存到正確位置**
   ```bash
   # 移動下載的 PDF
   mv ~/Downloads/schmid2024.pdf 04_fulltext/round-01/pdfs/Schmid2024_KEYNOTE522.pdf
   ```

### 本週

4. **系統性 PDF 收集**
   - 使用 Unpaywall 瀏覽器外掛
   - 透過機構 VPN 訪問期刊
   - 記錄無法取得的文獻

5. **開始全文審查**
   - 優先審查 27 篇「include」
   - 記錄審查結果

---

**狀態**: ⏳ Phase 4 進行中
**當前任務**: PDF 取得
**預期完成**: 3 週內
**下個里程碑**: 完成全文審查，確定最終納入清單

---

**版本**: 1.0
**日期**: 2026-02-07
**更新者**: Meta-analysis pipeline
