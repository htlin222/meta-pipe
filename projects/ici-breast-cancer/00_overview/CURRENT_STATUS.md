# 當前專案狀態

## TNBC 新輔助免疫療法系統性回顧與統合分析

**更新日期**: 2026-02-07 08:45 AM
**專案進度**: Phase 2 完成（提前 8 天！）🎉
**整體狀態**: ✅ 優秀，準備進入篩選階段

---

## ✅ 已完成階段

### 準備階段（4 小時）

- ✅ 可行性評估：15/16 分（94%，優秀）
- ✅ 95 篇相關文獻、5-8 個 RCT 預期
- ✅ 決策：**GO** - 進行完整系統性回顧

### Phase 1：方案發展（第 1-2 週）

- ✅ PICO 定義（`01_protocol/pico.yaml`）
- ✅ 納入排除標準（`01_protocol/eligibility.md`）
- ✅ 檢索策略（`01_protocol/search_strategy.md`）
- ✅ PROSPERO 註冊草稿（`01_protocol/prospero_registration.md`）
- ✅ 資料萃取表單（`05_extraction/data-dictionary.md`）
- ✅ Rayyan 設定指南（`docs/RAYYAN_SETUP.md`）
- ✅ Zotero 設定指南（`docs/ZOTERO_SETUP.md`）

### Phase 2：文獻檢索（第 3 週）

- ✅ PubMed 檢索：122 筆紀錄
- ✅ 去重處理：122 筆獨特紀錄
- ✅ 轉換成篩選格式（CSV）
- ✅ 驗證關鍵研究：5/5 都已抓到 ✓

---

## 📊 檢索結果摘要

| 資料庫               | 狀態      | 紀錄數 | 檔案                            |
| -------------------- | --------- | ------ | ------------------------------- |
| **PubMed/MEDLINE**   | ✅ 完成   | 122    | `02_search/round-01/pubmed.bib` |
| **Cochrane CENTRAL** | ⚠️ 需手動 | -      | （需機構訂閱）                  |
| **Embase**           | ⏳ 待處理 | -      | （需機構訂閱）                  |

**當前總計**: 122 筆（僅 PubMed）
**預期最終**: 150-180 筆（多資料庫後）

---

## ✓ 關鍵研究驗證

所有 5 個已知重要試驗都已在 PubMed 結果中：

1. ✅ **KEYNOTE-522** (Schmid et al.) - Pembrolizumab
2. ✅ **IMpassion031** (Mittendorf et al.) - Atezolizumab
3. ✅ **CamRelief** (Chen et al. 2025) - Camrelizumab
4. ✅ **GeparNuevo** (Loibl et al.) - Durvalumab
5. ✅ **NeoTRIP** (Gianni et al.) - Atezolizumab

**敏感度**: 5/5 = 100% ✅

---

## 📁 已建立檔案

### 方案檔案

```
01_protocol/
├── pico.yaml                    # PICO 定義
├── eligibility.md               # 納入排除標準
├── search_strategy.md           # 檢索策略（所有資料庫）
└── prospero_registration.md     # PROSPERO 註冊文件
```

### 檢索結果

```
02_search/round-01/
├── pubmed.bib                   # 122 筆 PubMed 紀錄
├── pubmed_log.md                # 檢索記錄
├── dedupe.bib                   # 去重後（目前同 pubmed.bib）
├── dedupe.log                   # 去重報告
└── SEARCH_COMPLETION_REPORT.md  # 檢索階段完成報告
```

### 篩選準備

```
03_screening/round-01/
└── decisions.csv                # 122 筆待篩選紀錄
```

### 設定指南

```
docs/
├── RAYYAN_SETUP.md              # Rayyan 雙人獨立篩選指南
└── ZOTERO_SETUP.md              # Zotero 文獻管理指南
```

### 萃取準備

```
05_extraction/
└── data-dictionary.md           # 160+ 欄位資料萃取表單
```

---

## 🎯 下一步驟

### 選項 A：補充其他資料庫（建議）⭐

**原因**：系統性回顧標準要求多資料庫檢索

**行動**（2-3 小時）：

1. **手動 Cochrane Library 檢索**（15 分鐘）
   - 訪問 https://www.cochranelibrary.com/
   - 使用 `01_protocol/search_strategy.md` 中的 Cochrane 策略
   - 匯出為 BibTeX 或 RIS
   - 預期：20-30 筆紀錄

2. **手動 ClinicalTrials.gov 檢索**（15 分鐘）
   - 訪問 https://clinicaltrials.gov/
   - 條件："Triple-Negative Breast Cancer"
   - 介入："pembrolizumab OR atezolizumab OR durvalumab" + "neoadjuvant"
   - 篩選：介入性研究，Phase 2/3
   - 預期：15-25 筆試驗

3. **（選項）聯絡圖書館**（如有 Embase 訂閱）
   - 請求協助進行 Embase 檢索
   - 使用 `01_protocol/search_strategy.md` 中的 Embase 策略
   - 預期：120-150 筆紀錄

4. **合併與去重**（30 分鐘）

   ```bash
   cd /Users/htlin/meta-pipe/tooling/python

   # 合併所有資料庫
   uv run ../../ma-search-bibliography/scripts/multi_db_dedupe.py \
     --in-bib ../../02_search/round-01/pubmed.bib \
     --in-bib ../../02_search/round-01/cochrane.bib \
     --out-merged ../../02_search/round-01/merged.bib \
     --out-bib ../../02_search/round-01/dedupe.bib \
     --out-log ../../02_search/round-01/dedupe_multi.log

   # 重新產生篩選 CSV
   uv run bib_to_csv.py \
     --in-bib ../../02_search/round-01/dedupe.bib \
     --out-csv ../../03_screening/round-01/decisions.csv
   ```

**預期最終結果**：150-180 筆獨特紀錄

---

### 選項 B：直接進入篩選（較快但不建議）

**如果選擇此選項**：

1. **設定 Rayyan**（30 分鐘）
   - 遵循 `docs/RAYYAN_SETUP.md`
   - 匯入 `03_screening/round-01/decisions.csv`
   - 邀請共同審查者

2. **試點篩選**（1 小時）
   - 與共同審查者一起篩選 10 篇文獻
   - 澄清邊界案例
   - 必要時調整納入/排除標準

3. **獨立篩選**（每位審查者 6-8 小時）
   - 兩位審查者獨立篩選全部 122 筆紀錄
   - 使用 Rayyan 盲性模式
   - 預期完成：1-2 週

---

## 📅 時程更新

| 原訂計畫        | 實際進度    | 狀態         |
| --------------- | ----------- | ------------ |
| 第 1-2 週：方案 | 第 1 週完成 | ✅ 提前 1 週 |
| 第 3 週：檢索   | 第 1 週完成 | ✅ 提前 2 週 |
| 第 4-5 週：篩選 | 可立即開始  | ⏩ 提前 8 天 |

**提前天數**: +8 天 🚀
**預計投稿日期**: 2026-05-12（原 2026-05-20）

**原因**：

- 自動化腳本運作順暢
- 方案準備效率高
- 無技術問題

---

## 🎓 學習重點

### 已掌握技能

1. ✅ PICO 架構設計
2. ✅ 多資料庫檢索策略
3. ✅ 自動化文獻管理
4. ✅ 可行性評估方法

### 正在學習

1. 🟡 Rayyan 雙人獨立篩選
2. 🟡 全文檢索與 PDF 管理
3. 🟡 LLM 輔助資料萃取

### 將要學習

1. ⏳ R 統合分析
2. ⏳ 風險偏差評估
3. ⏳ PRISMA 流程圖
4. ⏳ GRADE 證據品質評估

---

## 💡 建議行動（今天）

### 必要（你需要做）

1. **決定是否補充其他資料庫**（10 分鐘思考）
   - 選項 A：補充 Cochrane + ClinicalTrials.gov（建議）
   - 選項 B：直接用 PubMed 122 筆進行篩選

2. **（如果還沒做）提交 PROSPERO**（2 小時）
   - 審查 `01_protocol/prospero_registration.md`
   - 訪問 https://www.crd.york.ac.uk/prospero/
   - 提交註冊
   - 儲存註冊編號（CRD42026XXXXX）

### 選擇性（本週）

3. **設定 Zotero**（45 分鐘）
   - 遵循 `docs/ZOTERO_SETUP.md`
   - 安裝 Zotero + Better BibTeX
   - 匯入 5 個試點研究
   - 設定自動匯出到 `07_manuscript/references.bib`

4. **設定 Rayyan**（30 分鐘）
   - 遵循 `docs/RAYYAN_SETUP.md`
   - 建立審查專案
   - 邀請共同審查者
   - **不要**先上傳文獻（等補充其他資料庫後）

---

## ⚠️ 重要提醒

### PROSPERO 註冊

- 🔴 **重要**：在開始篩選前註冊
- ⏱️ **預期批准時間**：5-10 天
- 📝 **批准後**：更新 `01_protocol/pico.yaml` 加入 PROSPERO ID

### 檢索品質

- 當前僅 PubMed（單一資料庫）
- 系統性回顧最佳實踐：≥2 個資料庫
- 建議補充至少 Cochrane Library

### 協作準備

- 確認共同審查者的可用性
- 預留 6-8 小時給篩選工作
- 準備好解決衝突的時間（2-3 小時）

---

## 📞 需要幫助？

### 技術問題

- 檢索腳本問題：檢查 `.env` 檔案中的 API keys
- CSV 格式問題：使用 `bib_to_csv.py` 重新產生
- 去重問題：檢查 `dedupe.log` 中的詳細資訊

### 方法學問題

- PICO 不確定：審查 `01_protocol/pico.yaml`
- 納入標準不清楚：審查 `01_protocol/eligibility.md`
- 檢索策略：審查 `01_protocol/search_strategy.md`

### 流程問題

- 下一步不確定：閱讀 `PROJECT_START_PLAN.md`
- 階段完成檢查：參考 `02_search/SEARCH_COMPLETION_REPORT.md`

---

## 📊 專案健康指標

| 指標         | 狀態                  | 註記           |
| ------------ | --------------------- | -------------- |
| **時程**     | ✅ 提前 8 天          | 優秀           |
| **品質**     | ✅ 所有關鍵研究已抓到 | 100% 敏感度    |
| **完整性**   | 🟡 僅 PubMed          | 建議補充資料庫 |
| **文件**     | ✅ 完整               | 所有階段有記錄 |
| **可重現性** | ✅ 優秀               | 腳本 + 版控    |

**整體評估**: 🎉 **優秀** - 專案進展順利，品質高，提前進度

---

**狀態**: ✅ PHASE 2 完成，準備 PHASE 3
**信心水準**: 非常高
**下個里程碑**: 完成篩選（預期 2 週內）
**整體專案時程**: **提前 8 天** 🚀

---

---

## 🔄 最新更新（2026-02-07 09:00）

### Phase 3 準備完成 ✅

**新增檔案**：

- `03_screening/SCREENING_QUICKSTART.md` - 篩選階段快速開始指南（中文）

**下一步行動**（你需要選擇）：

#### 選項 A：Rayyan 雙人獨立篩選（強烈建議）⭐

1. 訪問 https://www.rayyan.ai/ 註冊
2. 遵循 `docs/RAYYAN_SETUP.md` 設定（30 分鐘）
3. 上傳 `02_search/round-01/dedupe.bib`
4. 邀請共同審查者
5. 試點篩選（10 篇，1 小時）
6. 獨立篩選（每人 6-8 小時，分散 1-2 週）
7. 解決衝突（2-3 小時）

**預期結果**：

- 納入全文審查：15-25 篇（~20%）
- Cohen's kappa：≥0.60
- 符合 PRISMA、Cochrane 標準 ✅

#### 選項 B：單人快速篩選（不建議）⚠️

- 在 Excel/Sheets 打開 `03_screening/round-01/decisions.csv`
- 逐行填寫 `decision_r1` 欄位
- **警告**：不符合系統性回顧標準，可能被審查者批評

---

**詳細指南**：請閱讀 `03_screening/SCREENING_QUICKSTART.md`

**必讀文件**：

- 納入排除標準：`01_protocol/eligibility.md`
- Rayyan 設定：`docs/RAYYAN_SETUP.md`
- 快速開始：`03_screening/SCREENING_QUICKSTART.md` ⭐ 新增

---

**文件版本**: 1.1
**最後更新**: 2026-02-07 09:00 AM GMT+8
**更新者**: Meta-analysis pipeline automation
