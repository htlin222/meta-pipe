# 可重複使用工具總結

**日期**: 2026-02-06
**目的**: 記錄從此專案中提取並泛化的可重複使用工具

---

## 📊 總覽

本次 CDK4/6 inhibitor meta-analysis 專案中，我們建立了多個可重複使用的腳本，這些工具已經被泛化並移至適當的 `ma-*` 模組中，可供未來任何系統性文獻回顧專案使用。

---

## ✅ 已整合的工具 (3個)

### 1. **bib_subset_by_ids.py** 🔍

**功能**: 根據 CSV 中的 record ID 提取 BibTeX 子集

**位置**: `ma-search-bibliography/scripts/bib_subset_by_ids.py`

**使用場景**:

- Stage 03→04: 篩選後提取全文審查記錄
- Stage 04→05: 全文審查後提取納入研究
- 任何需要從 BibTeX 檔案中篩選特定記錄的情境

**關鍵功能**:

```bash
# 基本使用
uv run bib_subset_by_ids.py \
  --in-csv screening.csv \
  --in-bib full.bib \
  --out-bib subset.bib

# 進階：條件篩選
uv run bib_subset_by_ids.py \
  --in-csv screening.csv \
  --in-bib full.bib \
  --out-bib included.bib \
  --filter-column final_decision \
  --filter-value Include
```

**新增參數**:

- `--id-column`: 指定 CSV 中的 ID 欄位 (預設: `record_id`)
- `--filter-column`: 條件篩選欄位
- `--filter-value`: 篩選條件值

---

### 2. **download_oa_pdfs.py** 📥

**功能**: 從 Unpaywall API 結果自動下載開放取用 PDF

**位置**: `ma-fulltext-management/scripts/download_oa_pdfs.py`

**使用場景**:

- Stage 04: 全文檢索自動化下載
- 任何需要批次下載 PDF 的情境

**關鍵功能**:

```bash
uv run download_oa_pdfs.py \
  --in-csv unpaywall_results.csv \
  --pdf-dir pdfs/ \
  --out-log download.log \
  --sleep 1 \
  --max-retries 3 \
  --timeout 30
```

**新增功能**:

- ✅ 重試機制 (`--max-retries`)
- ✅ 速率限制 (`--sleep`)
- ✅ 超時設定 (`--timeout`)
- ✅ PDF 格式驗證 (magic bytes)
- ✅ 詳細錯誤記錄
- ✅ 跳過已存在檔案

**預期成功率**:

- Gold OA: 80-90%
- Green OA: 60-70%
- Hybrid OA: 20-30% (大多需要機構存取)
- Bronze OA: 10-20%

---

### 3. **analyze_unpaywall.py** 📈

**功能**: 分析 Unpaywall API 結果並產生統計報告

**位置**: `ma-fulltext-management/scripts/analyze_unpaywall.py`

**使用場景**:

- 評估開放取用涵蓋率
- 預估 PDF 檢索成功率
- 研究計畫預算估算

**關鍵功能**:

```bash
uv run analyze_unpaywall.py \
  --in-csv unpaywall_results.csv \
  --out-md summary.md
```

**輸出內容**:

- 開放取用比例
- OA 類型分布 (Gold/Green/Hybrid/Bronze)
- 主機類型 (Publisher/Repository)
- 授權類型統計
- PDF 檢索潛力評估

**範例輸出**:

```
📊 Unpaywall Analysis Results
Total records queried: 52
Open Access (OA): 38 (73.1%)
  - With PDF URL: 38 (73.1%)
Closed Access: 13 (25.0%)

OA Types:
  - gold      : 16 (42.1% of OA)
  - hybrid    : 14 (36.8% of OA)
  - bronze    :  5 (13.2% of OA)
  - green     :  3 ( 7.9% of OA)
```

---

## 📚 文件更新

### 1. CLAUDE.md

**更新章節**: Stage 04: Fulltext

新增完整的 Stage 03→04 工作流程命令：

1. 提取 BibTeX 子集
2. 查詢 Unpaywall API
3. 分析 OA 涵蓋率
4. 自動下載 PDF

### 2. ma-fulltext-management/README.md

**新建文件** (400+ 行)

**包含內容**:

- 完整工作流程說明
- 每個腳本的詳細文檔
- 疑難排解指南
- 預期檢索成功率
- 最佳實踐建議

### 3. 分析文件

**SCRIPT_ANALYSIS.md**: 腳本可重用性分析
**MIGRATION_SUMMARY.md**: 遷移過程記錄

---

## 🔧 泛化過程

### 從專案特定 → 通用工具

**Before** (tooling/python/):

```python
# 硬編碼路徑
csv_path = Path("../../04_fulltext/round-01/unpaywall_results.csv")
pdf_dir = Path("../../04_fulltext/round-01/pdfs")
```

**After** (ma-\* modules):

```python
# 可配置路徑
parser.add_argument("--in-csv", required=True, type=Path)
parser.add_argument("--pdf-dir", required=True, type=Path)
```

**改進項目**:

1. ✅ 所有路徑參數化
2. ✅ 添加錯誤驗證
3. ✅ 改進錯誤訊息
4. ✅ 增加重試邏輯
5. ✅ 添加詳細文檔

---

## 💡 使用範例：完整 Stage 04 工作流程

```bash
cd /Users/htlin/meta-pipe/tooling/python

# Step 1: 提取全文審查記錄 (Include + Uncertain)
uv run ../../ma-search-bibliography/scripts/bib_subset_by_ids.py \
  --in-csv ../../03_screening/round-01/decisions_screened.csv \
  --in-bib ../../02_search/round-01/dedupe.bib \
  --out-bib ../../04_fulltext/round-01/fulltext_subset.bib

# Step 2: 查詢 Unpaywall API
uv run ../../ma-fulltext-management/scripts/unpaywall_fetch.py \
  --in-bib ../../04_fulltext/round-01/fulltext_subset.bib \
  --out-csv ../../04_fulltext/round-01/unpaywall_results.csv \
  --out-log ../../04_fulltext/round-01/unpaywall_fetch.log \
  --email "${UNPAYWALL_EMAIL}"

# Step 3: 分析 OA 涵蓋率
uv run ../../ma-fulltext-management/scripts/analyze_unpaywall.py \
  --in-csv ../../04_fulltext/round-01/unpaywall_results.csv \
  --out-md ../../04_fulltext/round-01/unpaywall_summary.md

# Step 4: 自動下載 PDF
uv run ../../ma-fulltext-management/scripts/download_oa_pdfs.py \
  --in-csv ../../04_fulltext/round-01/unpaywall_results.csv \
  --pdf-dir ../../04_fulltext/round-01/pdfs \
  --out-log ../../04_fulltext/round-01/pdf_download.log \
  --sleep 1 \
  --max-retries 3
```

**預期結果**:

- ✅ 20-40% PDF 自動下載成功
- 📄 詳細記錄檔說明失敗原因
- 📊 Markdown 報告顯示 OA 統計
- 🎯 清楚知道哪些需要手動檢索

---

## 🎯 專案特定工具 (未遷移)

保留在 `tooling/python/` 的腳本：

| 腳本                              | 原因                       |
| --------------------------------- | -------------------------- |
| `check_key_trials_oa.py`          | 硬編碼 CDK4/6 試驗名稱     |
| `auto_screening.py`               | 需要 YAML 配置才能泛化     |
| `update_manifest_with_results.py` | 需要進一步泛化工作         |
| `prepare_fulltext_review.py`      | 已足夠通用，可考慮未來遷移 |

---

## 📈 效益分析

### 當前專案

✅ 清楚記錄檢索工作流程
✅ 可重現的命令序列
✅ 詳細日誌便於疑難排解

### 未來專案

✅ **節省時間**: 每個專案節省 4-6 小時 (無需重寫 PDF 檢索)
✅ **標準化**: 所有專案使用相同工作流程
✅ **最佳實踐**: 錯誤處理、重試邏輯已內建
✅ **完整文檔**: 新團隊成員可快速上手

### 團隊協作

✅ 其他研究人員可使用這些工具
✅ 清楚的文檔便於新成員理解
✅ 跨專案標準化工作流程

---

## 🔮 未來增強 (可選)

### 中優先級

1. **泛化 auto_screening.py**
   - 將關鍵字清單移至 YAML 配置
   - 移至 `ma-screening-quality` 模組

2. **泛化 update_manifest_with_results.py**
   - 使其兼容任何檢索 CSV
   - 重命名為 `update_retrieval_manifest.py`

3. **移動 prepare_fulltext_review.py**
   - 已足夠通用
   - 只需重新定位至 `ma-fulltext-management`

### 低優先級

1. **建立 PDF 檢索技能 (Skill)**
   - 記錄最佳實踐
   - 包含機構存取工作流程

2. **添加整合測試**
   - 測試完整 Stage 03→04 工作流程
   - 驗證所有腳本協同運作

---

## 📁 檔案結構

```
meta-pipe/
├── ma-search-bibliography/
│   └── scripts/
│       └── bib_subset_by_ids.py          [NEW - 通用]
│
├── ma-fulltext-management/
│   ├── scripts/
│   │   ├── unpaywall_fetch.py            [已存在]
│   │   ├── download_oa_pdfs.py           [NEW - 通用]
│   │   └── analyze_unpaywall.py          [NEW - 通用]
│   └── README.md                          [NEW - 400+ 行文檔]
│
├── tooling/python/
│   ├── SCRIPT_ANALYSIS.md                 [NEW - 分析報告]
│   ├── MIGRATION_SUMMARY.md              [NEW - 遷移記錄]
│   ├── check_key_trials_oa.py            [保留 - 專案特定]
│   ├── auto_screening.py                 [保留 - 待泛化]
│   └── prepare_fulltext_review.py        [保留 - 可考慮遷移]
│
├── CLAUDE.md                              [更新 - Stage 04 章節]
└── REUSABLE_TOOLS_SUMMARY.md             [NEW - 本文件]
```

---

## ✨ 關鍵成就

### 程式碼品質

✅ **錯誤處理**: 所有腳本都有完整的錯誤驗證
✅ **日誌記錄**: 詳細的成功/失敗記錄
✅ **重試邏輯**: 自動處理暫時性失敗
✅ **參數化**: 所有路徑都可配置
✅ **文檔**: 每個腳本都有詳細的 docstring 和 help

### 可用性

✅ **清楚的參數名稱**: `--in-csv`, `--out-bib` 等
✅ **有意義的錯誤訊息**: 告訴使用者如何修復
✅ **進度指示**: 即時顯示下載進度
✅ **總結報告**: 執行後顯示統計資訊

### 可維護性

✅ **模組化設計**: 每個腳本單一職責
✅ **可測試**: 函數與 main 分離
✅ **版本控制**: 在 git 中追蹤
✅ **文檔完整**: README 涵蓋所有使用場景

---

## 🎓 經驗教訓

### 做得好的地方

1. **先在 tooling/python 開發** - 更容易迭代測試
2. **使用真實資料測試** - 發現邊界情況
3. **完整的日誌記錄** - 使除錯更容易
4. **重試邏輯** - 處理暫時性失敗

### 可以改進的地方

1. **更早規劃可重用性** - 初期有些硬編碼路徑
2. **同步撰寫測試** - 會更早發現問題
3. **隨寫隨記錄** - 比事後寫文檔更容易

---

## 📞 下一步建議

### 立即可做

1. ✅ 開始在未來專案中使用這些工具
2. ✅ 參考 `ma-fulltext-management/README.md` 了解詳細用法
3. ✅ 遵循 CLAUDE.md 中的 Stage 04 工作流程

### 未來考慮

1. ⭐ 為其他 Stage 建立類似的可重用工具
2. ⭐ 添加整合測試確保工具協同運作
3. ⭐ 建立技能檔案記錄最佳實踐

---

## 🎉 總結

**成功整合**: 3 個主要工具
**文檔建立**: 2 份完整指南 (README + Migration)
**影響範圍**: 所有未來系統性文獻回顧專案

**估計每個專案節省時間**: 4-6 小時
**長期效益**: 標準化工作流程 + 降低錯誤率 + 更快上手

---

**整合完成日期**: 2026-02-06
**下次檢視**: 下一個系統性文獻回顧專案開始前
