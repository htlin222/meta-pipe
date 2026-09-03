# meta-pipe Workflow Presentation

`meta-pipe-workflow.pptx` — 16 張投影片，介紹 meta-pipe 的端到端工作流程（繁體中文，附講者備註）。

| # | 主題 |
|---|------|
| 1 | 封面 |
| 2 | 為什麼需要一條流水線（100+ 小時 vs 約 14 小時） |
| 3 | 核心理念：Skills 驅動、可重現工具鏈、品質閘門 |
| 4 | 流程總覽：11 個階段、4 個區塊 |
| 5 | Stage 00–02：主題、計畫、搜尋（4 小時可行性評估） |
| 6 | Stage 03–04：雙人篩選、分析類型確認閘門 |
| 7 | Stage 05：LLM 輔助資料萃取 |
| 8 | Stage 06：依分析類型分流（pairwise / NMA / pooled / narrative） |
| 9 | Stage 07–10：手稿、審查、出版品質、投稿 |
| 10 | 品質閘門一覽表 |
| 11 | 範例專案：ICI in TNBC |
| 12 | 各階段時間投資（原生圖表） |
| 13 | Agent Teams 平行模式 |
| 14 | 人機分工 |
| 15 | 三步驟開始新專案 |
| 16 | 結語 |

## Rebuild

```bash
cd docs/presentation
npm install pptxgenjs
node build_deck.js   # writes meta-pipe-workflow.pptx
```

字型：`Microsoft JhengHei`（Office 內建）；程式碼片段用 `Courier New`。
