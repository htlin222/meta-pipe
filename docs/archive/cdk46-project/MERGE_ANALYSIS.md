# 專案分支合併分析報告

**日期**: 2026-02-06
**專案**: CDK4/6i Meta-Analysis (projects/cdk46-breast)
**目的**: 識別應合併到主分支的可重用內容

---

## 📊 總覽

專案分支中有 **21 個新增檔案**需要評估是否應合併到 `main` 分支。

分類：
- ✅ **應該合併**: 13 個檔案（通用工具和文檔）
- ⚠️ **選擇性合併**: 3 個檔案（可選功能）
- ❌ **不應合併**: 5 個檔案（專案特定內容）

---

## ✅ 應該合併到 Main 分支（13 個）

### 1. 核心基礎設施工具（3 個）

#### `ma-end-to-end/scripts/validate_module_registry.py`
- **用途**: 驗證所有腳本都有正確的文檔覆蓋
- **價值**: 防止文檔與代碼不同步
- **依賴**: module-management skill
- **理由**: 任何未來專案都需要這個 QA 工具
- **優先級**: 🔴 HIGH

#### `ma-peer-review/scripts/init_rob2_assessment.py`
- **用途**: 初始化 RCT 的 RoB 2 評估表
- **價值**: RCT 風險評估是系統性回顧的核心步驟
- **依賴**: rob2-template.md
- **理由**: 標準化工具，適用所有 RCT meta-analysis
- **優先級**: 🟡 MEDIUM

#### `ma-peer-review/scripts/init_robins_i_assessment.py`
- **用途**: 初始化觀察性研究的 ROBINS-I 評估表
- **價值**: 觀察性研究風險評估
- **依賴**: robins-i-template.md
- **理由**: 標準化工具，適用所有包含觀察性研究的回顧
- **優先級**: 🟡 MEDIUM

---

### 2. Stage 01: Protocol 工具（1 個）

#### `tooling/python/generate_prospero_protocol.py`
- **用途**: 從 pico.yaml 生成 PROSPERO 註冊文件
- **價值**: 自動化 PROSPERO 註冊流程
- **依賴**: pico.yaml 格式
- **理由**: PROSPERO 註冊是系統性回顧的標準步驟
- **優先級**: 🟡 MEDIUM
- **需要文檔更新**: AGENTS.md (Stage 01 section)

---

### 3. Stage 02: Search 工具（2 個）

#### `tooling/python/bib_to_csv.py`
- **用途**: BibTeX → CSV 轉換，用於篩選
- **價值**: 篩選階段必備工具
- **依賴**: bibtexparser
- **理由**: Stage 02→03 轉換的標準步驟
- **優先級**: 🔴 HIGH
- **需要文檔更新**: AGENTS.md (Stage 03 前置步驟)

#### `tooling/python/csv_to_bib_subset.py`
- **用途**: 從 CSV 提取 BibTeX 子集（已有 ma-search-bibliography/scripts/bib_subset_by_ids.py）
- **狀態**: **與現有工具重複**
- **建議**: ⚠️ **不合併**，改用已有的 `bib_subset_by_ids.py`

---

### 4. Stage 04: Fulltext 工具（3 個，已部分合併）

#### `tooling/python/download_oa_pdfs.py`
- **狀態**: ✅ **已合併到 main** (`ma-fulltext-management/scripts/`)
- **動作**: 無需處理

#### `tooling/python/analyze_unpaywall.py`
- **狀態**: ✅ **已合併到 main** (`ma-fulltext-management/scripts/`)
- **動作**: 無需處理

#### `tooling/python/prepare_fulltext_review.py`
- **用途**: 整合多個步驟（bib subset, Unpaywall, PDF download）
- **價值**: 一鍵式全文檢索流程
- **依賴**: 多個已合併的工具
- **理由**: 簡化 Stage 04 工作流程
- **優先級**: 🟡 MEDIUM
- **需要文檔更新**: AGENTS.md (Stage 04 section)

---

### 5. Stage 05: Extraction 工具（4 個）

#### `tooling/python/create_pdf_manifest.py`
- **用途**: 從 PDF JSONL 創建 LLM extraction 用的 manifest
- **價值**: LLM 輔助提取的前置步驟
- **依賴**: extract_pdf_text.py 的輸出
- **理由**: LLM extraction workflow 的標準步驟
- **優先級**: 🔴 HIGH
- **需要文檔更新**: AGENTS.md (Stage 05 section)

#### `tooling/python/create_extraction_template.py`
- **用途**: 從 data dictionary 創建空白 extraction CSV
- **價值**: 標準化 extraction 表格
- **依賴**: data-dictionary.md
- **理由**: 手動或 LLM extraction 的起點
- **優先級**: 🔴 HIGH
- **需要文檔更新**: AGENTS.md (Stage 05 section)

#### `tooling/python/update_extraction_manual.py`
- **用途**: 合併 LLM 提取結果與人工修正
- **價值**: LLM+人工混合工作流程
- **依賴**: extraction CSV 格式
- **理由**: Quality control 步驟
- **優先級**: 🟡 MEDIUM

#### `tooling/python/update_manifest_with_results.py`
- **用途**: 更新 manifest 與提取結果
- **價值**: 追蹤提取進度
- **依賴**: manifest 和 extraction CSV
- **理由**: 項目管理工具
- **優先級**: 🟢 LOW（可選）

---

### 6. 文檔與 Skill（3 個）

#### `.claude/skills/module-management.md`
- **用途**: 模組與文檔一致性管理
- **價值**: QA 流程標準化
- **依賴**: validate_module_registry.py
- **理由**: 防止文檔腐爛（documentation rot）
- **優先級**: 🔴 HIGH

#### `ma-peer-review/references/rob2-template.md`
- **用途**: RoB 2 評估模板
- **價值**: RCT 風險評估標準範本
- **依賴**: init_rob2_assessment.py
- **理由**: 標準化風險評估流程
- **優先級**: 🟡 MEDIUM

#### `ma-peer-review/references/robins-i-template.md`
- **用途**: ROBINS-I 評估模板
- **價值**: 觀察性研究風險評估標準範本
- **依賴**: init_robins_i_assessment.py
- **理由**: 標準化風險評估流程
- **優先級**: 🟡 MEDIUM

---

## ⚠️ 選擇性合併（3 個）

### 1. `tooling/python/auto_screening.py`
- **用途**: AI 輔助篩選（基於關鍵字）
- **問題**: 高度專案特定（CDK4/6i 關鍵字硬編碼）
- **建議**:
  - **選項 A**: 泛化成可配置的關鍵字篩選工具
  - **選項 B**: 保留在專案分支作為範例
- **優先級**: 🟢 LOW（可選功能）

### 2. `tooling/python/check_key_trials_oa.py`
- **用途**: 檢查 10 個關鍵試驗的 OA 狀態
- **問題**: 完全專案特定（hardcoded trial names）
- **建議**: **不合併**，保留作為範例
- **優先級**: ❌ 不合併

### 3. `tooling/python/check_outcome_completeness.py`
- **用途**: 檢查 meta-analysis 可行性（outcome data 完整性）
- **價值**: 這是可行性評估的重要步驟！
- **問題**: 當前實作專案特定（hardcoded exclusion IDs）
- **建議**:
  - **選項 A**: 泛化成通用 outcome completeness checker
  - **選項 B**: 整合到 FEASIBILITY_CHECKLIST.md 的 Hour 3
- **優先級**: 🟡 MEDIUM（應該泛化）

---

## ❌ 不應合併到 Main（2 個）

### 1. `BRANCH_STRUCTURE.md`
- **性質**: 專案回顧文檔
- **內容**: CDK4/6i 專案的分支歷史記錄
- **理由**: 專案特定，不適用未來專案
- **建議**: 保留在專案分支

### 2. `PROJECT_LESSONS_LEARNED.md`
- **性質**: 專案回顧文檔
- **內容**: CDK4/6i 專案的完整經驗總結
- **理由**: 專案特定案例研究
- **建議**: 保留在專案分支
- **註**: 核心教訓（可行性評估）已提取到 `FEASIBILITY_CHECKLIST.md`（已在 main）

---

## 📋 建議合併清單

### 🔴 HIGH Priority（必須合併，5 個）

1. ✅ `ma-end-to-end/scripts/validate_module_registry.py` + skill
2. ✅ `tooling/python/bib_to_csv.py`
3. ✅ `tooling/python/create_pdf_manifest.py`
4. ✅ `tooling/python/create_extraction_template.py`
5. ✅ `.claude/skills/module-management.md`

### 🟡 MEDIUM Priority（應該合併，6 個）

6. ✅ `ma-peer-review/scripts/init_rob2_assessment.py` + template
7. ✅ `ma-peer-review/scripts/init_robins_i_assessment.py` + template
8. ✅ `tooling/python/generate_prospero_protocol.py`
9. ✅ `tooling/python/prepare_fulltext_review.py`
10. ✅ `tooling/python/update_extraction_manual.py`
11. ⚠️ `tooling/python/check_outcome_completeness.py`（需泛化）

### 🟢 LOW Priority（可選，2 個）

12. ⚠️ `tooling/python/auto_screening.py`（需泛化）
13. ⚠️ `tooling/python/update_manifest_with_results.py`

---

## 🚀 合併執行計劃

### Phase 1: 核心工具（5 個檔案）

```bash
git checkout main

# 1. Module management infrastructure
git checkout projects/cdk46-breast -- .claude/skills/module-management.md
git checkout projects/cdk46-breast -- ma-end-to-end/scripts/validate_module_registry.py

# 2. Stage 02→03 workflow
git checkout projects/cdk46-breast -- tooling/python/bib_to_csv.py

# 3. Stage 05 extraction workflow
git checkout projects/cdk46-breast -- tooling/python/create_pdf_manifest.py
git checkout projects/cdk46-breast -- tooling/python/create_extraction_template.py

git add -A
git commit -m "Add core meta-analysis workflow tools from CDK4/6i project"
```

### Phase 2: Risk of Bias 工具（4 個檔案）

```bash
# 4. RoB assessment tools
git checkout projects/cdk46-breast -- ma-peer-review/scripts/init_rob2_assessment.py
git checkout projects/cdk46-breast -- ma-peer-review/references/rob2-template.md
git checkout projects/cdk46-breast -- ma-peer-review/scripts/init_robins_i_assessment.py
git checkout projects/cdk46-breast -- ma-peer-review/references/robins-i-template.md

git add -A
git commit -m "Add Risk of Bias assessment tools (RoB 2 and ROBINS-I)"
```

### Phase 3: 輔助工具（3 個檔案）

```bash
# 5. Supporting tools
git checkout projects/cdk46-breast -- tooling/python/generate_prospero_protocol.py
git checkout projects/cdk46-breast -- tooling/python/prepare_fulltext_review.py
git checkout projects/cdk46-breast -- tooling/python/update_extraction_manual.py

git add -A
git commit -m "Add PROSPERO generator and fulltext workflow tools"
```

### Phase 4: 文檔更新

更新 `AGENTS.md` 加入新工具的使用說明（見下一節）

---

## 📝 需要的文檔更新

### `AGENTS.md` 需要新增的章節

#### Stage 01: Protocol
```markdown
# Generate PROSPERO registration document from pico.yaml
uv add pyyaml
uv run generate_prospero_protocol.py \
  --pico ../../01_protocol/pico.yaml \
  --out ../../01_protocol/prospero_registration.md
```

#### Stage 02→03: Search to Screening
```markdown
# Convert BibTeX to CSV for screening
uv run bib_to_csv.py \
  --in-bib ../../02_search/round-01/dedupe.bib \
  --out-csv ../../03_screening/round-01/decisions.csv
```

#### Stage 03: Risk of Bias Assessment
```markdown
# RoB 2 for RCTs
uv run ../../ma-peer-review/scripts/init_rob2_assessment.py \
  --extraction ../../05_extraction/round-01/extraction.csv \
  --out-csv ../../03_screening/round-01/quality_rob2.csv \
  --out-md ../../03_screening/round-01/rob2_assessment.md

# ROBINS-I for cohort/observational studies
uv run ../../ma-peer-review/scripts/init_robins_i_assessment.py \
  --extraction ../../05_extraction/round-01/extraction.csv \
  --out-csv ../../03_screening/round-01/quality_robins_i.csv \
  --out-md ../../03_screening/round-01/robins_i_assessment.md
```

#### Stage 04: Fulltext (simplified workflow)
```markdown
# One-command fulltext workflow
uv run prepare_fulltext_review.py \
  --screening-csv ../../03_screening/round-01/decisions.csv \
  --search-bib ../../02_search/round-01/dedupe.bib \
  --pdf-dir ../../04_fulltext/round-01/pdfs \
  --email "your@email.com"
```

#### Stage 05: Extraction
```markdown
# Step 1: Extract PDF text
uv add pdfplumber
uv run extract_pdf_text.py \
  --pdf-dir ../../04_fulltext/round-01/pdfs \
  --out-jsonl ../../05_extraction/round-01/pdf_texts.jsonl \
  --pattern "*.pdf"

# Step 2: Create extraction template
uv run create_extraction_template.py \
  --pdf-jsonl ../../05_extraction/round-01/pdf_texts.jsonl \
  --data-dict ../../05_extraction/data-dictionary.md \
  --out-csv ../../05_extraction/round-01/extraction_template.csv

# Step 3: Create LLM manifest
uv run create_pdf_manifest.py \
  --pdf-jsonl ../../05_extraction/round-01/pdf_texts.jsonl \
  --out-csv ../../05_extraction/round-01/manifest.csv

# Step 4: LLM extraction (using Claude CLI)
uv run llm_extract_cli.py \
  --pdf-jsonl ../../05_extraction/round-01/pdf_texts.jsonl \
  --data-dict ../../05_extraction/data-dictionary.md \
  --out-jsonl ../../05_extraction/round-01/llm_extracted_all.jsonl \
  --cli claude

# Step 5: Manual review and updates
# (Edit extraction.csv manually to correct LLM errors)

# Step 6: Update extraction with manual corrections
uv run update_extraction_manual.py \
  --llm-jsonl ../../05_extraction/round-01/llm_extracted_all.jsonl \
  --manual-csv ../../05_extraction/round-01/extraction_manual.csv \
  --out-csv ../../05_extraction/round-01/extraction.csv
```

---

## 💡 建議的泛化工作

### `check_outcome_completeness.py` 泛化

**當前問題**: Hardcoded exclusion IDs

**泛化版本**:
```python
#!/usr/bin/env python3
"""Check outcome data completeness for meta-analysis feasibility."""

def check_outcomes(csv_path, exclude_ids=None):
    """
    Check which studies have complete outcome data.

    Args:
        csv_path: Path to extraction CSV
        exclude_ids: Optional list of study IDs to exclude
    """
    exclude_ids = exclude_ids or []

    # Outcome fields (configurable via data-dictionary.md)
    outcome_fields = {
        "PFS": ["pfs_hr", "pfs_ci_lower", "pfs_ci_upper"],
        "OS": ["os_hr", "os_ci_lower", "os_ci_upper"],
        "ORR": ["orr_arm1", "orr_arm2"],
    }

    # ... rest of logic ...

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--exclude-ids", nargs="*", default=[])
    parser.add_argument("--min-studies", type=int, default=3,
                       help="Minimum studies needed for meta-analysis")
    args = parser.parse_args()

    check_outcomes(args.csv, args.exclude_ids)
```

**整合到可行性評估**:
- 這應該是 `FEASIBILITY_CHECKLIST.md` Hour 3 的腳本化版本
- 可以作為 Hour 2（試提取）後的自動化檢查

---

## 📊 合併後的預期狀態

### Main 分支會新增

- **12 個 Python 腳本**（通用工具）
- **3 個模板檔案**（RoB 評估）
- **1 個 Skill**（module-management）
- **AGENTS.md 更新**（新增 7 個命令區塊）

### 總程式碼增加

- ~2,500 行 Python（可重用工具）
- ~600 行 Markdown（模板和文檔）

### ROI for Future Projects

每個未來專案可節省：
- Stage 01: 1-2 小時（PROSPERO 自動生成）
- Stage 02→03: 0.5 小時（BibTeX 轉換）
- Stage 03: 2-3 小時（RoB 評估範本）
- Stage 04: 3-4 小時（全文檢索自動化）
- Stage 05: 8-10 小時（LLM extraction workflow）

**Total: 15-20 小時 / 專案**

---

## ✅ 下一步行動

1. **用戶確認**: 確認上述合併計劃
2. **執行合併**: Phase 1 → Phase 2 → Phase 3
3. **更新文檔**: 更新 AGENTS.md
4. **測試驗證**: 在 main 分支執行 validate_module_registry.py
5. **Push 到遠端**: git push origin main
6. **專案分支歸檔**: 切回專案分支，確認專案記錄完整

---

**準備好開始合併了嗎？**
