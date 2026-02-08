# 文件引用檢查報告

**日期**: 2026-02-07
**檢查範圍**: `docs/` 目錄所有 `.md` 文件（排除 `archive/`）

---

## 執行摘要

✅ **結果**: 所有 15 個文件都已被正確引用
❌ **孤兒文件**: 0 個

---

## 修復的孤兒文件

本次修復了 **3 個孤兒文件**，將它們連結到主工作流程：

### 1. `docs/RAYYAN_SETUP.md` (386 行)

- **用途**: Web-based 協作篩選工具設定指南
- **引用位置**: AGENTS.md (CLAUDE.md) Stage 03: Screening
- **引用方式**: `[Rayyan Setup Guide](docs/RAYYAN_SETUP.md)`
- **上下文**: 作為 CSV 篩選流程的替代方案

### 2. `docs/ZOTERO_SETUP.md` (612 行)

- **用途**: Zotero 參考文獻管理系統詳細設定
- **引用位置**: AGENTS.md (CLAUDE.md) Stage 02: Search
- **引用方式**: `[Zotero Setup Guide](docs/ZOTERO_SETUP.md)`
- **上下文**: Zotero integration 指令後的補充說明

### 3. `docs/UNPAYWALL_COMPARISON.md` (398 行)

- **用途**: Unpaywall API 版本比較與決策指南
- **引用位置**: AGENTS.md (CLAUDE.md) Stage 04: Fulltext
- **引用方式**: `[Unpaywall vs Alternatives](docs/UNPAYWALL_COMPARISON.md)`
- **上下文**: 與 UNPAYWALL_ROBUST.md 並列引用

---

## 所有文件引用狀態

| 文件                               | 引用次數 | 主要引用位置                                                                           |
| ---------------------------------- | -------- | -------------------------------------------------------------------------------------- |
| `API_SETUP.md`                     | 4        | CLAUDE.md, GETTING_STARTED.md                                                          |
| `JOURNAL_FORMATTING.md`            | 1        | CLAUDE.md                                                                              |
| `MANUSCRIPT_ASSEMBLY.md`           | 1        | CLAUDE.md                                                                              |
| `R_FIGURE_GUIDE.md`                | 1        | CLAUDE.md                                                                              |
| `r-guides/00-setup.md`             | 3        | R_FIGURE_GUIDE.md, r-guides/README.md, 09-package-selection.md                         |
| `r-guides/01-forest-plots.md`      | 5        | CLAUDE.md, R_FIGURE_GUIDE.md, r-guides/README.md, 00-setup.md, 09-package-selection.md |
| `r-guides/05-table1-gtsummary.md`  | 4        | CLAUDE.md, R_FIGURE_GUIDE.md, r-guides/README.md, 00-setup.md                          |
| `r-guides/09-package-selection.md` | 2        | R_FIGURE_GUIDE.md, r-guides/README.md                                                  |
| `r-guides/README.md`               | 2        | R_FIGURE_GUIDE.md                                                                      |
| `RAYYAN_SETUP.md`                  | 1        | CLAUDE.md (Stage 03) ✅ **新增**                                                       |
| `SKILL_GENERALIZATION.md`          | 1        | CLAUDE.md                                                                              |
| `TIME_GUIDANCE.md`                 | 1        | CLAUDE.md                                                                              |
| `UNPAYWALL_COMPARISON.md`          | 1        | CLAUDE.md (Stage 04) ✅ **新增**                                                       |
| `UNPAYWALL_ROBUST.md`              | 2        | CLAUDE.md, UNPAYWALL_COMPARISON.md                                                     |
| `ZOTERO_SETUP.md`                  | 1        | CLAUDE.md (Stage 02) ✅ **新增**                                                       |

---

## 文件網絡圖

```
CLAUDE.md (主文件) → AGENTS.md (符號連結)
├─ docs/API_SETUP.md
├─ docs/JOURNAL_FORMATTING.md
├─ docs/MANUSCRIPT_ASSEMBLY.md
├─ docs/TIME_GUIDANCE.md
├─ docs/SKILL_GENERALIZATION.md
├─ docs/RAYYAN_SETUP.md ✅
├─ docs/ZOTERO_SETUP.md ✅
├─ docs/UNPAYWALL_COMPARISON.md ✅
├─ docs/UNPAYWALL_ROBUST.md
└─ docs/R_FIGURE_GUIDE.md
   └─ docs/r-guides/
      ├─ README.md (導航中心)
      ├─ 00-setup.md
      ├─ 01-forest-plots.md
      ├─ 05-table1-gtsummary.md
      └─ 09-package-selection.md
```

---

## 檢查方法

```bash
# 1. 列出所有文件
find docs -name "*.md" -type f ! -path "*/archive/*" | sort

# 2. 檢查每個文件的引用
for doc in $(find docs -name "*.md" -type f ! -path "*/archive/*"); do
  filename=$(basename "$doc")
  refs=$(grep -l "$filename" CLAUDE.md README.md GETTING_STARTED.md docs/*.md docs/r-guides/*.md 2>/dev/null | wc -l)
  if [ "$refs" -eq 0 ]; then
    echo "❌ 孤兒: $doc"
  else
    echo "✓ 被引用 ($refs 次): $doc"
  fi
done
```

---

## 維護建議

### 定期檢查（建議頻率）

- ✅ 每次新增文件後立即檢查
- ✅ 每月定期稽核一次
- ✅ 重大重構後全面檢查

### 新增文件流程

1. 創建新文件於 `docs/` 或 `docs/r-guides/`
2. 立即在相關主文件中添加引用
3. 運行孤兒檢查腳本驗證
4. Commit 時包含引用更新

### 命名規範

- ✅ 使用描述性名稱（如 `RAYYAN_SETUP.md`）
- ✅ 大寫用於主題指南（SETUP, GUIDE, COMPARISON）
- ✅ 小寫數字開頭用於順序指南（01-forest-plots.md）

### 引用原則

- ✅ 主工作流程文件應引用所有重要指南
- ✅ 使用 Progressive Disclosure（主文件→子指南）
- ✅ 相關文件之間建立交叉引用
- ✅ 在適當的 Stage 或 Section 添加 "📖 See" 引用

---

## Git Commit 記錄

```
commit ad61067
Author: Claude + User
Date: 2026-02-07

docs: Link orphaned documentation files to main workflow

Fixed 3 orphan files by adding references in AGENTS.md:

1. docs/RAYYAN_SETUP.md - Stage 03: Screening section
2. docs/ZOTERO_SETUP.md - Stage 02: Search section
3. docs/UNPAYWALL_COMPARISON.md - Stage 04: Fulltext section

Result: All 15 documentation files now properly referenced
- 0 orphan files (was 3)
- All docs accessible from main workflow
```

---

## 結論

✅ **所有文件已正確組織**
✅ **無孤兒文件**
✅ **文件結構清晰，易於導航**
✅ **Progressive Disclosure 原則已實施**

文件引用網絡完整，使用者可以從主文件 (CLAUDE.md) 順利找到所有相關指南。
