const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.author = "meta-pipe";
pres.title = "meta-pipe workflow";

// Palette: deep teal ink, teal primary, mint tint, coral accent
const INK = "0B2E33";
const TEAL = "0F5257";
const TEAL2 = "1C7C82";
const MINT = "E6F0EE";
const CORAL = "E4572E";
const TEXT = "263238";
const MUTED = "6B7C7E";
const WHITE = "FFFFFF";
const LINE = "C9DAD7";

const FONT = "Microsoft JhengHei";
const W = 13.33;
const H = 7.5;
const M = 0.6; // margin

function text(slide, t, o) {
  slide.addText(t, Object.assign({ fontFace: FONT, color: TEXT, isTextBox: true, margin: 0, valign: "top" }, o));
}

function title(slide, t, dark) {
  text(slide, t, { x: M, y: 0.45, w: W - 2 * M, h: 0.8, fontSize: 30, bold: true, color: dark ? WHITE : INK });
}

function kicker(slide, t, dark) {
  text(slide, t, { x: M, y: 0.2, w: 8, h: 0.3, fontSize: 12, color: dark ? "9FC5C2" : TEAL2, bold: true, charSpacing: 2 });
}

function circleNum(slide, x, y, n, size, fill, color) {
  slide.addShape(pres.ShapeType.ellipse, { x, y, w: size, h: size, fill: { color: fill }, line: { color: fill } });
  text(slide, String(n), { x, y, w: size, h: size, align: "center", valign: "middle", fontSize: size * 22, bold: true, color: color || WHITE, fontFace: "Arial" });
}

function card(slide, x, y, w, h, fill, shadow) {
  const o = { x, y, w, h, fill: { color: fill || MINT }, line: { color: fill || MINT }, rectRadius: 0.12 };
  if (shadow) o.shadow = { type: "outer", blur: 6, offset: 2, angle: 90, color: "000000", opacity: 0.12 };
  slide.addShape(pres.ShapeType.roundRect, o);
}

function arrowRight(slide, x, y, len, color) {
  slide.addShape(pres.ShapeType.rightArrow, { x, y, w: len, h: 0.3, fill: { color: color || LINE }, line: { color: color || LINE } });
}

function footer(slide, n, dark) {
  text(slide, "meta-pipe  ·  github.com/htlin222/meta-pipe", { x: M, y: H - 0.45, w: 6, h: 0.25, fontSize: 9, color: dark ? "7FA8A5" : MUTED, fontFace: "Arial" });
  text(slide, String(n), { x: W - M - 1, y: H - 0.45, w: 1, h: 0.25, fontSize: 9, color: dark ? "7FA8A5" : MUTED, align: "right", fontFace: "Arial" });
}

function bullets(slide, items, o) {
  const runs = items.map((s, i) => ({ text: s, options: { bullet: { indent: 14 }, breakLine: i < items.length - 1, paraSpaceAfter: 8 } }));
  text(slide, runs, Object.assign({ fontSize: 13, color: TEXT }, o));
}

const STAGES = [
  ["00", "主題發想", "TOPIC.txt"],
  ["01", "研究計畫", "pico.yaml"],
  ["02", "文獻搜尋", "dedupe.bib"],
  ["03", "雙人篩選", "decisions.csv"],
  ["04", "全文管理", "manifest.csv"],
  ["05", "資料萃取", "extraction.csv"],
  ["06", "統合分析", "figures/ tables/"],
  ["07", "手稿撰寫", "manuscript.pdf"],
  ["08", "同儕審查", "grade_summary.md"],
  ["09", "出版品質", "final_qa_report.md"],
  ["10", "投稿準備", "PROSPERO / submit"],
];

let n = 0;

// ---------- 1. Title ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: INK };
  text(s, "meta-pipe", { x: M, y: 1.5, w: 9, h: 1.2, fontSize: 60, bold: true, color: WHITE, fontFace: "Arial" });
  text(s, "AI 輔助的端到端 Meta-Analysis 工作流程", { x: M, y: 2.75, w: 11, h: 0.7, fontSize: 28, color: WHITE });
  text(s, "從 TOPIC.txt 到可投稿手稿  ·  Powered by Claude Code", { x: M, y: 3.5, w: 11, h: 0.5, fontSize: 16, color: "9FC5C2", italic: true });
  // stage motif row
  const size = 0.5;
  const gap = (W - 2 * M - 11 * size) / 10;
  STAGES.forEach((st, i) => {
    const x = M + i * (size + gap);
    circleNum(s, x, 5.2, st[0], size, i === 10 ? CORAL : TEAL2);
    text(s, st[1], { x: x - 0.25, y: 5.8, w: size + 0.5, h: 0.4, fontSize: 9, color: "9FC5C2", align: "center" });
  });
  text(s, "Lin HT, Yeh JT  ·  github.com/htlin222/meta-pipe", { x: M, y: H - 0.6, w: 8, h: 0.3, fontSize: 10, color: "7FA8A5", fontFace: "Arial" });
  s.addNotes("開場：meta-pipe 是一套以 Claude Code 驅動的 meta-analysis 流水線。輸入是一個 TOPIC.txt，輸出是可以投稿的手稿。下方 11 個階段（00–10）就是今天要走過的主線。");
}

// ---------- 2. Why ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: WHITE };
  kicker(s, "WHY");
  title(s, "為什麼需要一條流水線？");
  const pains = [
    ["重複勞動", "搜尋、去重、篩選、萃取，每一步都是大量機械式工作，卻又不能出錯。"],
    ["報告規範沉重", "PRISMA 2020 有 27 個項目（NMA 32 個），GRADE、RoB 2 各有一套規則。"],
    ["難以重現", "決策散落在信件與試算表裡，半年後連自己都無法回溯為何納入某篇研究。"],
  ];
  pains.forEach((p, i) => {
    const y = 1.6 + i * 1.45;
    circleNum(s, M, y + 0.05, i + 1, 0.55, TEAL);
    text(s, p[0], { x: M + 0.8, y, w: 5.5, h: 0.4, fontSize: 18, bold: true, color: INK });
    text(s, p[1], { x: M + 0.8, y: y + 0.45, w: 5.6, h: 0.9, fontSize: 13, color: TEXT });
  });
  // stats right
  card(s, 7.6, 1.6, 5.1, 2.0, MINT);
  text(s, "100+ 小時", { x: 7.9, y: 1.75, w: 4.6, h: 0.9, fontSize: 44, bold: true, color: MUTED });
  text(s, "傳統人工完成一篇 meta-analysis", { x: 7.9, y: 2.75, w: 4.6, h: 0.5, fontSize: 13, color: MUTED });
  card(s, 7.6, 3.85, 5.1, 2.0, INK);
  text(s, "約 14 小時", { x: 7.9, y: 4.0, w: 4.6, h: 0.9, fontSize: 44, bold: true, color: CORAL });
  text(s, "meta-pipe 範例專案（5 RCTs，N=2,402）", { x: 7.9, y: 5.0, w: 4.6, h: 0.5, fontSize: 13, color: "9FC5C2" });
  text(s, "一般專案估計 22–32 小時，取決於研究數與資料萃取複雜度。", { x: 7.6, y: 6.05, w: 5.1, h: 0.5, fontSize: 11, color: MUTED, italic: true });
  footer(s, n);
  s.addNotes("痛點三件事：重複勞動、報告規範、可重現性。右側對比：傳統 100+ 小時 vs 範例專案約 14 小時。提醒觀眾 14 小時是最順利的案例，一般預期 22–32 小時。");
}

// ---------- 3. Core idea ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: WHITE };
  kicker(s, "CORE IDEA");
  title(s, "核心理念");
  card(s, M, 1.5, W - 2 * M, 1.3, INK);
  text(s, "「TOPIC.txt 進，manuscript.pdf 出」", { x: M, y: 1.5, w: W - 2 * M, h: 0.8, fontSize: 30, bold: true, color: WHITE, align: "center", valign: "middle" });
  text(s, "每個階段有專屬 skill、固定的輸出檔案，以及進入下一階段前必須通過的品質閘門。", { x: M, y: 2.25, w: W - 2 * M, h: 0.45, fontSize: 13, color: "9FC5C2", align: "center" });
  const pillars = [
    ["Skills 驅動", "每個階段一個 ma-*/SKILL.md，寫明指令、驗證標準與輸出。Claude 依 skill 執行，不憑記憶即興。"],
    ["可重現工具鏈", "Python 用 uv、R 用 renv、手稿用 Quarto。每一輪搜尋與篩選保留 round-XX，永不覆寫。"],
    ["品質閘門", "kappa ≥ 0.60、圖片 ≥ 300 DPI、PRISMA 27/27、出版準備度 ≥ 95%。沒過門檻就不能往下走。"],
  ];
  const cw = (W - 2 * M - 2 * 0.4) / 3;
  pillars.forEach((p, i) => {
    const x = M + i * (cw + 0.4);
    card(s, x, 3.2, cw, 3.2, MINT);
    circleNum(s, x + 0.3, 3.5, i + 1, 0.5, TEAL);
    text(s, p[0], { x: x + 0.95, y: 3.5, w: cw - 1.2, h: 0.5, fontSize: 18, bold: true, color: INK, valign: "middle" });
    text(s, p[1], { x: x + 0.3, y: 4.2, w: cw - 0.6, h: 2.0, fontSize: 13, color: TEXT });
  });
  footer(s, n);
  s.addNotes("三根支柱：Skills 驅動（行為寫在 SKILL.md 裡，可版本控制）、可重現工具鏈（uv / renv / Quarto、round 制）、品質閘門（數字化門檻）。");
}

// ---------- 4. Pipeline overview ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: WHITE };
  kicker(s, "OVERVIEW");
  title(s, "流程總覽：11 個階段、4 個區塊");
  const phases = [
    ["Foundation", "循序", [0, 1, 2]],
    ["Screening", "可平行", [3, 4]],
    ["Processing", "循序", [5, 6]],
    ["Synthesis", "可平行", [7, 8, 9, 10]],
  ];
  const gapX = 0.45;
  const cw = (W - 2 * M - 3 * gapX) / 4;
  phases.forEach((p, i) => {
    const x = M + i * (cw + gapX);
    card(s, x, 1.5, cw, 5.2, MINT);
    text(s, p[0], { x: x + 0.25, y: 1.65, w: cw - 0.5, h: 0.4, fontSize: 16, bold: true, color: INK, fontFace: "Arial" });
    text(s, p[1], { x: x + 0.25, y: 2.05, w: cw - 0.5, h: 0.3, fontSize: 11, color: p[1] === "可平行" ? CORAL : MUTED, bold: true });
    p[2].forEach((si, j) => {
      const st = STAGES[si];
      const y = 2.55 + j * 1.0;
      circleNum(s, x + 0.25, y, st[0], 0.45, si === 10 ? CORAL : TEAL);
      text(s, st[1], { x: x + 0.85, y: y - 0.02, w: cw - 1.1, h: 0.3, fontSize: 14, bold: true, color: INK });
      text(s, st[2], { x: x + 0.85, y: y + 0.28, w: cw - 1.1, h: 0.3, fontSize: 10, color: MUTED, fontFace: "Arial" });
    });
    if (i < 3) arrowRight(s, x + cw + 0.08, 3.9, gapX - 0.16, TEAL2);
  });
  footer(s, n);
  s.addNotes("四個區塊：Foundation（00–02，循序）、Screening（03–04，雙人篩選可平行）、Processing（05–06，循序）、Synthesis（07–10，手稿與 QA 可平行）。每個階段旁邊是它的代表輸出檔。");
}

// ---------- 5. Stage 00-02 ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: WHITE };
  kicker(s, "STAGE 00 – 02");
  title(s, "從問題到文獻：主題、計畫、搜尋");
  const rows = [
    ["00", "主題發想與可行性", "「brainstorm」互動式收斂研究問題；產出 TOPIC.txt。"],
    ["01", "研究計畫", "PICO → pico.yaml、eligibility.md、search-plan.md；決定初步分析類型（≥3 種治療 → nma_candidate）。"],
    ["02", "文獻搜尋", "PubMed + Scopus 為最低要求（PRISMA 需 ≥2 資料庫），可加 Embase、Cochrane；以 round-01/ 保存 queries、results.bib、dedupe.bib。"],
  ];
  rows.forEach((r, i) => {
    const y = 1.6 + i * 1.5;
    circleNum(s, M, y, r[0], 0.55, TEAL);
    text(s, r[1], { x: M + 0.8, y, w: 6.2, h: 0.4, fontSize: 18, bold: true, color: INK });
    text(s, r[2], { x: M + 0.8, y: y + 0.45, w: 6.4, h: 1.0, fontSize: 12.5, color: TEXT });
  });
  // gate card
  card(s, 8.2, 1.6, 4.5, 3.9, INK);
  text(s, "強制第一步", { x: 8.5, y: 1.8, w: 4.0, h: 0.35, fontSize: 12, bold: true, color: CORAL, charSpacing: 2 });
  text(s, "4 小時可行性評估", { x: 8.5, y: 2.15, w: 4.0, h: 0.6, fontSize: 22, bold: true, color: WHITE });
  bullets(s, [
    "先確認研究數量夠不夠、結局定義是否一致",
    "評估過才能開始寫計畫或萃取資料",
    "目的：避免在無法回答的問題上浪費 10–40 小時",
    "產出 FEASIBILITY_REPORT.md",
  ], { x: 8.5, y: 2.95, w: 3.95, h: 2.4, fontSize: 12.5, color: "E6F0EE" });
  footer(s, n);
  s.addNotes("重點是「可行性評估」這個強制閘門：用 4 小時換取不浪費 10–40 小時。資料庫最低要求 PubMed + Scopus。分析類型在此只是初步判定，要等篩選完才確認。");
}

// ---------- 6. Stage 03-04 ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: WHITE };
  kicker(s, "STAGE 03 – 04");
  title(s, "篩選與全文：雙人審查、分析類型確認");
  // dual review diagram (left)
  text(s, "AI 雙人獨立篩選", { x: M, y: 1.5, w: 6, h: 0.4, fontSize: 18, bold: true, color: INK });
  const bx = M, by = 2.1;
  card(s, bx, by, 2.1, 0.8, MINT);
  text(s, "Reviewer 1", { x: bx, y: by, w: 2.1, h: 0.8, fontSize: 14, bold: true, color: TEAL, align: "center", valign: "middle", fontFace: "Arial" });
  card(s, bx, by + 1.1, 2.1, 0.8, MINT);
  text(s, "Reviewer 2", { x: bx, y: by + 1.1, w: 2.1, h: 0.8, fontSize: 14, bold: true, color: TEAL, align: "center", valign: "middle", fontFace: "Arial" });
  arrowRight(s, bx + 2.25, by + 0.25, 0.6, TEAL2);
  arrowRight(s, bx + 2.25, by + 1.35, 0.6, TEAL2);
  card(s, bx + 3.0, by + 0.35, 1.6, 1.2, INK);
  text(s, "κ ≥ 0.60", { x: bx + 3.0, y: by + 0.4, w: 1.6, h: 0.6, fontSize: 20, bold: true, color: CORAL, align: "center", valign: "middle", fontFace: "Arial" });
  text(s, "品質閘門", { x: bx + 3.0, y: by + 0.95, w: 1.6, h: 0.4, fontSize: 11, color: "9FC5C2", align: "center" });
  arrowRight(s, bx + 4.75, by + 0.8, 0.6, TEAL2);
  card(s, bx + 5.5, by + 0.35, 1.6, 1.2, MINT);
  text(s, "衝突裁決\nincluded.bib", { x: bx + 5.5, y: by + 0.35, w: 1.6, h: 1.2, fontSize: 12, bold: true, color: INK, align: "center", valign: "middle" });
  bullets(s, [
    "ai_screen.py 分別以 reviewer 1 / 2 執行，決策記錄於 decisions.csv",
    "dual_review_agreement.py 計算 Cohen's kappa，寫入 agreement.md",
    "Stage 04：以 Unpaywall 取得 PDF，建立 manifest.csv",
    "Stage 04b：全文適格性再做一次雙人篩選（PRISMA 2020 第 16 項）",
  ], { x: M, y: 4.35, w: 7.2, h: 2.5, fontSize: 12.5 });
  // gate card right
  card(s, 8.2, 1.5, 4.5, 4.4, MINT);
  text(s, "STAGE 03b", { x: 8.5, y: 1.7, w: 4.0, h: 0.3, fontSize: 11, bold: true, color: TEAL2, charSpacing: 2, fontFace: "Arial" });
  text(s, "分析類型確認閘門", { x: 8.5, y: 2.0, w: 4.0, h: 0.5, fontSize: 20, bold: true, color: INK });
  bullets(s, [
    "統計納入研究的設計類型",
    "評估網絡連通性與 transitivity",
    "單臂研究 >30% → 強烈建議降級為 pairwise + pooled proportion",
    "結果寫入 analysis-type-decision.md 與 pico.yaml",
    "未確認分析類型，不得進入 Stage 06",
  ], { x: 8.5, y: 2.7, w: 3.95, h: 3.1, fontSize: 12.5 });
  footer(s, n);
  s.addNotes("左：雙人 AI 篩選流程，kappa ≥ 0.60 才能過。右：NMA 候選專案在此決定是走 NMA 還是降級為 pairwise。這是整條流水線最重要的方法學決策點之一。");
}

// ---------- 7. Stage 05 ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: WHITE };
  kicker(s, "STAGE 05");
  title(s, "資料萃取：LLM 先做，人再複核");
  const steps = [
    ["1", "抽出 PDF 文字", "extract_pdf_text.py"],
    ["2", "LLM 結構化萃取", "llm_extract_cli.py --cli claude"],
    ["3", "人工複核與修正", "編輯 extraction.csv"],
    ["4", "自動驗證", "validate_extraction.py"],
  ];
  const gapX = 0.5;
  const cw = (W - 2 * M - 3 * gapX) / 4;
  steps.forEach((st, i) => {
    const x = M + i * (cw + gapX);
    card(s, x, 1.6, cw, 1.9, i === 2 ? INK : MINT);
    circleNum(s, x + 0.25, 1.85, st[0], 0.45, i === 2 ? CORAL : TEAL);
    text(s, st[1], { x: x + 0.25, y: 2.45, w: cw - 0.5, h: 0.4, fontSize: 15, bold: true, color: i === 2 ? WHITE : INK });
    text(s, st[2], { x: x + 0.25, y: 2.9, w: cw - 0.5, h: 0.4, fontSize: 10.5, color: i === 2 ? "9FC5C2" : MUTED, fontFace: "Courier New" });
    if (i < 3) arrowRight(s, x + cw + 0.1, 2.4, gapX - 0.2, TEAL2);
  });
  // stats
  const stats = [
    ["65–70%", "相較人工的時間節省"],
    ["100%", "PDF 處理成功率（範例專案）"],
    ["US$0–5", "每篇 meta-analysis 的 LLM 成本"],
  ];
  stats.forEach((st, i) => {
    const x = M + i * 4.1;
    text(s, st[0], { x, y: 4.0, w: 3.8, h: 0.8, fontSize: 36, bold: true, color: TEAL, fontFace: "Arial" });
    text(s, st[1], { x, y: 4.8, w: 3.8, h: 0.4, fontSize: 12, color: MUTED });
  });
  bullets(s, [
    "輸入僅限 FT_Final_Decision = include 的研究",
    "同時完成偏誤風險評估：RCT 用 RoB 2，觀察性研究用 ROBINS-I",
    "輸出 extraction.csv、extraction.sqlite 與 data-dictionary.md；低信心欄位以 flag_low_confidence.py 標記",
  ], { x: M, y: 5.45, w: W - 2 * M, h: 1.4, fontSize: 12.5 });
  footer(s, n);
  s.addNotes("萃取採「LLM 先做、人再複核」。步驟 3 反白，強調人工複核是必要環節，不可省略。數字來自範例專案經驗。");
}

// ---------- 8. Stage 06 ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: WHITE };
  kicker(s, "STAGE 06");
  title(s, "統合分析：依分析類型自動分流");
  card(s, M, 1.7, 2.9, 1.4, INK);
  text(s, "analysis_type\n.confirmed", { x: M, y: 1.7, w: 2.9, h: 1.4, fontSize: 15, bold: true, color: WHITE, align: "center", valign: "middle", fontFace: "Courier New" });
  const branches = [
    ["pairwise", "Pairwise MA", "R 腳本 01–12：forest、funnel、敏感度、次群組、meta-regression"],
    ["nma", "Network MA", "nma_01–10 Bayesian NMA；nma_11 CNMA、nma_12 meta-regression、nma_13 transitivity"],
    ["pooled_proportion", "Pooled proportion", "單臂或比例資料的合併估計"],
    ["narrative", "Narrative synthesis", "資料無法量化合併時的結構化敘述"],
  ];
  const bx = 5.0, bw = 7.7, bh = 1.05;
  branches.forEach((b, i) => {
    const y = 1.45 + i * (bh + 0.2);
    slide_line(s, M + 2.9, 2.4, bx - 0.1, y + bh / 2);
    card(s, bx, y, bw, bh, MINT);
    text(s, b[0], { x: bx + 0.25, y: y + 0.12, w: 2.4, h: 0.3, fontSize: 11, color: TEAL2, fontFace: "Courier New", bold: true });
    text(s, b[1], { x: bx + 0.25, y: y + 0.42, w: 2.6, h: 0.5, fontSize: 15, bold: true, color: INK, fontFace: "Arial" });
    text(s, b[2], { x: bx + 2.9, y: y + 0.15, w: bw - 3.15, h: bh - 0.3, fontSize: 11.5, color: TEXT, valign: "middle" });
  });
  bullets(s, [
    "R + renv 鎖定套件版本（renv.lock）",
    "所有圖片 ≥ 300 DPI，多面板圖以 assemble_figures.py 組合",
    "輸出 figures/、tables/ 直接供手稿引用",
  ], { x: M, y: 3.5, w: 4.0, h: 3.0, fontSize: 12.5 });
  footer(s, n);
  s.addNotes("由 pico.yaml 的 analysis_type.confirmed 決定走哪條路。pairwise 走 R 01–12；NMA 走 nma_01–13，包含 transitivity 統計檢定。所有結果用 renv 鎖版本。");
}

function slide_line(s, x1, y1, x2, y2) {
  s.addShape(pres.ShapeType.line, { x: x1, y: Math.min(y1, y2), w: x2 - x1, h: Math.abs(y2 - y1), line: { color: LINE, width: 1.5 }, flipV: y2 < y1 });
}

// ---------- 9. Stage 07-10 ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: WHITE };
  kicker(s, "STAGE 07 – 10");
  title(s, "從手稿到投稿");
  const cards = [
    ["07", "手稿撰寫", ["先填 manuscript_outline.md，取得使用者同意才動筆", "Quarto 組裝五大段落與表格", "6–8 小時達到 90% 可投稿"]],
    ["08", "同儕審查", ["GRADE 證據品質分級", "Summary of Findings 表", "RoB 2 / ROBINS-I 彙整"]],
    ["09", "出版品質", ["publication_readiness_score.py：0–100% 客觀評分", "claim_audit.py：12 種過度宣稱型態", "PRISMA 27/27、交叉引用檢查"]],
    ["10", "投稿準備", ["PROSPERO 登錄文件", "期刊格式（Lancet / JAMA / Nat Med）", "品質精修：90% → 95–98%"]],
  ];
  const gapX = 0.35;
  const cw = (W - 2 * M - 3 * gapX) / 4;
  cards.forEach((c, i) => {
    const x = M + i * (cw + gapX);
    card(s, x, 1.5, cw, 3.7, i === 3 ? INK : MINT);
    circleNum(s, x + 0.25, 1.75, c[0], 0.5, i === 3 ? CORAL : TEAL);
    text(s, c[1], { x: x + 0.9, y: 1.75, w: cw - 1.1, h: 0.5, fontSize: 18, bold: true, color: i === 3 ? WHITE : INK, valign: "middle" });
    bullets(s, c[2], { x: x + 0.25, y: 2.5, w: cw - 0.5, h: 2.5, fontSize: 12.5, color: i === 3 ? "E6F0EE" : TEXT });
  });
  footer(s, n);
  s.addNotes("07 有一個「大綱先核准」的閘門。09 的重點是把主觀的「準備好了嗎」變成 0–100% 的客觀分數，以及自動抓過度宣稱。10 的品質精修可把接受率再拉高約 10%。");
}

// ---------- 10. Quality gates table ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: WHITE };
  kicker(s, "QUALITY GATES");
  title(s, "品質閘門：沒過門檻，不進下一站");
  const hdr = { bold: true, color: WHITE, fill: { color: TEAL }, fontFace: FONT, fontSize: 13, valign: "middle" };
  const cell = (t, o) => ({ text: t, options: Object.assign({ fontFace: FONT, fontSize: 12.5, color: TEXT, valign: "middle" }, o || {}) });
  const rows = [
    [{ text: "轉換點", options: hdr }, { text: "閘門", options: hdr }, { text: "門檻", options: hdr }],
    [cell("00 → 01"), cell("可行性評估"), cell("4 小時評估完成，FEASIBILITY_REPORT.md", { bold: true })],
    [cell("03 → 04"), cell("題目/摘要篩選一致性"), cell("Cohen's kappa ≥ 0.60", { bold: true })],
    [cell("03b → 06"), cell("分析類型確認"), cell("analysis_type.confirmed 已填寫", { bold: true })],
    [cell("04 → 05"), cell("全文篩選一致性"), cell("kappa ≥ 0.60", { bold: true })],
    [cell("05 → 06"), cell("萃取完整性"), cell("所有納入研究皆已萃取並通過驗證", { bold: true })],
    [cell("06 → 07"), cell("圖片品質"), cell("所有圖片 ≥ 300 DPI", { bold: true })],
    [cell("07 → 08"), cell("手稿大綱"), cell("使用者核准 manuscript_outline.md", { bold: true })],
    [cell("09"), cell("出版準備度"), cell("PRISMA 27/27（NMA 32/32）、readiness ≥ 95%", { bold: true })],
  ];
  s.addTable(rows, { x: M, y: 1.5, w: W - 2 * M, colW: [2.2, 4.0, 5.93], rowH: 0.5, border: { type: "solid", color: LINE, pt: 0.75 }, fill: { color: WHITE }, margin: 0.08 });
  text(s, "Agent Teams 模式下，這些閘門由 hooks 在階段轉換時自動執行；單一 session 模式則由 validate_stage_transition.py 產生報告。", { x: M, y: 6.3, w: W - 2 * M, h: 0.5, fontSize: 11.5, color: MUTED, italic: true });
  footer(s, n);
  s.addNotes("這頁是整個 workflow 的「憲法」。每個轉換點都有可量化的門檻，validate_stage_transition.py 會產出 09_qa/stage_transition_report.md。");
}

// ---------- 11. Case study ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: INK };
  kicker(s, "CASE STUDY", true);
  title(s, "範例專案：免疫檢查點抑制劑於三陰性乳癌（新輔助）", true);
  const stats = [
    ["5", "納入 RCT"],
    ["2,402", "病人數 N"],
    ["RR 1.26", "pCR，95% CI 1.16–1.37"],
    ["⊕⊕⊕⊕", "GRADE 證據品質 HIGH"],
    ["4,921 字", "符合 Lancet Oncology 字數"],
    ["~14 小時", "從 TOPIC.txt 到手稿"],
  ];
  const gapX = 0.35, gapY = 0.35;
  const cw = (W - 2 * M - 2 * gapX) / 3;
  const ch = 1.9;
  stats.forEach((st, i) => {
    const col = i % 3, row = Math.floor(i / 3);
    const x = M + col * (cw + gapX);
    const y = 1.55 + row * (ch + gapY);
    card(s, x, y, cw, ch, "143F44");
    text(s, st[0], { x: x + 0.3, y: y + 0.25, w: cw - 0.6, h: 0.9, fontSize: i === 5 ? 34 : 36, bold: true, color: i === 5 ? CORAL : WHITE, fontFace: i === 3 ? "Arial" : "Arial" });
    text(s, st[1], { x: x + 0.3, y: y + 1.2, w: cw - 0.6, h: 0.5, fontSize: 13, color: "9FC5C2" });
  });
  text(s, "檔案位置：projects/ici-breast-cancer/  ·  從 00_overview 到 09_qa 完整保留，可作為新專案範本。", { x: M, y: 6.25, w: W - 2 * M, h: 0.4, fontSize: 11.5, color: "9FC5C2", italic: true });
  footer(s, n, true);
  s.addNotes("這是 repo 裡唯一被 git 追蹤的完整專案。主要結局 pCR：RR 1.26、I² = 0%、NNT 7。所有階段檔案都在，可直接當範本。");
}

// ---------- 12. Time chart ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: WHITE };
  kicker(s, "TIME INVESTMENT");
  title(s, "各階段時間投資（小時）");
  const labels = ["01 計畫", "02 搜尋", "03 篩選", "04 全文", "05 萃取", "06 分析", "07 手稿"];
  s.addChart(pres.ChartType.bar, [
    { name: "最低", labels, values: [1, 2, 3, 2, 4, 4, 6] },
    { name: "最高", labels, values: [2, 3, 4, 4, 6, 5, 8] },
  ], {
    x: M, y: 1.5, w: 7.6, h: 5.0,
    barDir: "col", barGrouping: "clustered", barGapWidthPct: 60,
    chartColors: [TEAL2, INK],
    showTitle: false,
    showLegend: true, legendPos: "b", legendFontFace: FONT, legendFontSize: 11, legendColor: MUTED,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFontFace: "Arial", dataLabelFontSize: 10, dataLabelColor: TEXT,
    catAxisLabelFontFace: FONT, catAxisLabelFontSize: 11, catAxisLabelColor: TEXT, catGridLine: { style: "none" },
    valAxisLabelFontFace: "Arial", valAxisLabelFontSize: 10, valAxisLabelColor: MUTED, valGridLine: { color: "E5ECEB", size: 0.5 },
    valAxisMaxVal: 9, valAxisMinVal: 0, valAxisMajorUnit: 2,
    catAxisLineShow: false, valAxisLineShow: false,
  });
  card(s, 8.7, 1.5, 4.0, 1.7, INK);
  text(s, "22–32 小時", { x: 9.0, y: 1.65, w: 3.5, h: 0.8, fontSize: 32, bold: true, color: CORAL, fontFace: "Arial" });
  text(s, "端到端總時數（一般專案）", { x: 9.0, y: 2.45, w: 3.5, h: 0.4, fontSize: 12, color: "9FC5C2" });
  bullets(s, [
    "Stage 05 以 LLM 輔助可縮至 2–3 小時（節省 65%）",
    "關鍵路徑是 05 → 07：分析到手稿約 10–14 小時",
    "07 手稿是最耗時階段，因此有「大綱先核准」機制避免返工",
    "臨床詮釋、討論重點與作者聲明仍由人負責",
  ], { x: 8.7, y: 3.45, w: 4.0, h: 3.2, fontSize: 12 });
  footer(s, n);
  s.addNotes("長條是各階段的時間區間（最低/最高）。總計 22–32 小時。05 若用 LLM 萃取可明顯縮短。手稿是最大宗，所以用大綱核准來防止返工。");
}

// ---------- 13. Agent teams ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: WHITE };
  kicker(s, "AGENT TEAMS  ·  EXPERIMENTAL");
  title(s, "平行模式：多個 Claude Code 分工協作");
  const phases = [
    ["Phase 1", "循序", ["protocol-architect", "search-specialist"]],
    ["Phase 2", "平行", ["screener-a", "screener-b"]],
    ["Phase 3", "循序", ["fulltext-manager", "data-extractor", "statistician"]],
    ["Phase 4", "平行", ["manuscript-writer", "qa-auditor"]],
  ];
  const gapX = 0.4;
  const cw = (W - 2 * M - 3 * gapX) / 4;
  phases.forEach((p, i) => {
    const x = M + i * (cw + gapX);
    const par = p[1] === "平行";
    card(s, x, 1.5, cw, 3.3, MINT);
    text(s, p[0], { x: x + 0.25, y: 1.65, w: cw - 0.5, h: 0.35, fontSize: 15, bold: true, color: INK, fontFace: "Arial" });
    text(s, p[1], { x: x + 0.25, y: 2.0, w: cw - 0.5, h: 0.3, fontSize: 11, bold: true, color: par ? CORAL : MUTED });
    p[2].forEach((r, j) => {
      const y = 2.5 + j * 0.7;
      card(s, x + 0.25, y, cw - 0.5, 0.55, par ? INK : WHITE);
      text(s, r, { x: x + 0.25, y, w: cw - 0.5, h: 0.55, fontSize: 11.5, bold: true, color: par ? WHITE : TEAL, align: "center", valign: "middle", fontFace: "Courier New" });
    });
    if (i < 3) arrowRight(s, x + cw + 0.06, 3.0, gapX - 0.12, TEAL2);
  });
  bullets(s, [
    "Lead 讀取 /ma-agent-teams 劇本，建立共享任務清單並依相依順序生成 teammates",
    "每個 teammate 只擁有自己的目錄（如 statistician 只寫 06_analysis/**），避免互相覆寫",
    "screener-a 與 screener-b 完成前禁止互通訊息，確保雙人篩選真正獨立",
    "統計與手稿角色使用 Opus，其餘使用 Sonnet；hooks 在階段轉換時自動執行品質閘門",
  ], { x: M, y: 5.1, w: W - 2 * M, h: 1.8, fontSize: 12 });
  footer(s, n);
  s.addNotes("實驗性功能，需 Claude Code v2.1.32+ 並開啟 CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS。核心是「目錄所有權」與「篩選者隔離」。適合 ≥5 篇研究、且有 ≥2 個獨立階段可平行的專案。");
}

// ---------- 14. Human vs AI ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: WHITE };
  kicker(s, "DIVISION OF LABOR");
  title(s, "人機分工：AI 做結構，人做判斷");
  const cw = (W - 2 * M - 0.5) / 2;
  card(s, M, 1.5, cw, 4.3, MINT);
  text(s, "Claude 負責（節省 60–80% 時間）", { x: M + 0.35, y: 1.7, w: cw - 0.7, h: 0.5, fontSize: 18, bold: true, color: TEAL });
  bullets(s, [
    "搜尋策略、去重、雙人篩選初判",
    "PDF 取得與文字抽取、結構化資料萃取",
    "R 腳本產生、圖表與多面板組圖",
    "手稿架構、表格模板、參考文獻管理",
    "PRISMA 檢核表填寫、過度宣稱偵測、交叉引用檢查",
    "進度追蹤、session log、checkpoint",
  ], { x: M + 0.35, y: 2.4, w: cw - 0.7, h: 3.2, fontSize: 14 });
  card(s, M + cw + 0.5, 1.5, cw, 4.3, INK);
  text(s, "人負責（需要領域專業）", { x: M + cw + 0.85, y: 1.7, w: cw - 0.7, h: 0.5, fontSize: 18, bold: true, color: CORAL });
  bullets(s, [
    "研究問題與 PICO 的臨床意義",
    "可行性評估與分析類型的最終決定",
    "篩選衝突裁決、萃取資料複核",
    "臨床詮釋、討論重點的取捨",
    "圖說的科學細節、作者貢獻與利益衝突聲明",
    "每個閘門的「核准」動作",
  ], { x: M + cw + 0.85, y: 2.4, w: cw - 0.7, h: 3.2, fontSize: 14, color: "E6F0EE" });
  footer(s, n);
  s.addNotes("強調這不是全自動：AI 產出結構與草稿，所有臨床判斷、方法學決策與核准仍在人手上。這也是可審計性的來源。");
}

// ---------- 15. Getting started ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: WHITE };
  kicker(s, "GETTING STARTED");
  title(s, "三步驟開始一個新專案");
  const steps = [
    ["1", "建立專案骨架", "uv run tooling/python/init_project.py --name my-ma", "產生 01_protocol/ … 09_qa/ 與 TOPIC.txt"],
    ["2", "寫下研究問題", "projects/my-ma/TOPIC.txt", "貼上主題、族群、介入、比較與結局；沒有題目可先說「brainstorm」"],
    ["3", "對 Claude Code 說", "\"Start project my-ma\"", "之後用「continue」「status」續接，Stage 06 後說「complete manuscript」"],
  ];
  steps.forEach((st, i) => {
    const y = 1.55 + i * 1.5;
    circleNum(s, M, y + 0.1, st[0], 0.6, i === 2 ? CORAL : TEAL);
    text(s, st[1], { x: M + 0.9, y, w: 4.0, h: 0.45, fontSize: 18, bold: true, color: INK });
    text(s, st[3], { x: M + 0.9, y: y + 0.5, w: 4.6, h: 0.8, fontSize: 12, color: TEXT });
    card(s, 6.4, y + 0.05, 6.3, 0.75, INK);
    text(s, st[2], { x: 6.65, y: y + 0.05, w: 5.9, h: 0.75, fontSize: 13, color: "E6F0EE", fontFace: "Courier New", valign: "middle" });
  });
  card(s, M, 6.1, W - 2 * M, 0.75, MINT);
  text(s, "環境需求：uv（Python ≥ 3.12）· R ≥ 4.2 + renv · Quarto · .env 內的 API 金鑰   |   一次性安裝 bash setup.sh，隨時用 bash verify_environment.sh 檢查", { x: M + 0.3, y: 6.1, w: W - 2 * M - 0.6, h: 0.75, fontSize: 11.5, color: TEXT, valign: "middle" });
  footer(s, n);
  s.addNotes("示範時可以直接開終端機跑這三步。提醒：所有 Python 都用 uv run，不直接呼叫 python3；專案目錄預設不進 git。");
}

// ---------- 16. Closing ----------
{
  const s = pres.addSlide();
  n++;
  s.background = { color: INK };
  kicker(s, "TAKEAWAYS", true);
  title(s, "帶走三件事", true);
  const items = [
    ["一條線", "TOPIC.txt 進、手稿出，11 個階段各有 skill、輸出與閘門。"],
    ["可重現", "uv、renv、Quarto 鎖定環境；round 制保留每一輪決策，可審計、可回溯。"],
    ["人在迴圈", "AI 做結構與草稿，臨床判斷與每個核准仍由研究者掌握。"],
  ];
  items.forEach((it, i) => {
    const y = 1.7 + i * 1.3;
    circleNum(s, M, y, i + 1, 0.6, CORAL);
    text(s, it[0], { x: M + 0.9, y: y - 0.02, w: 3.0, h: 0.6, fontSize: 22, bold: true, color: WHITE, valign: "middle" });
    text(s, it[1], { x: M + 3.9, y: y + 0.05, w: 8.5, h: 0.6, fontSize: 14, color: "E6F0EE", valign: "middle" });
  });
  card(s, M, 5.7, W - 2 * M, 1.0, "143F44");
  text(s, "github.com/htlin222/meta-pipe", { x: M + 0.3, y: 5.7, w: 6, h: 1.0, fontSize: 18, bold: true, color: WHITE, valign: "middle", fontFace: "Arial" });
  text(s, "Lin HT, Yeh JT. meta-pipe: AI-assisted, end-to-end meta-analysis pipeline with reproducible tooling. 2026.", { x: 6.6, y: 5.7, w: 6.1, h: 1.0, fontSize: 11, color: "9FC5C2", valign: "middle", fontFace: "Arial" });
  footer(s, n, true);
  s.addNotes("收尾：一條線、可重現、人在迴圈。邀請觀眾 clone repo，從 projects/ici-breast-cancer 開始看。");
}

pres.writeFile({ fileName: "meta-pipe-workflow.pptx" }).then(f => console.log("wrote", f));
