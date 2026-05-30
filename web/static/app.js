// meta-pipe web interface — prepare, then walk it yourself. Bilingual (EN / 中文).
//
// No auto-play. You first tick everything meta-pipe needs prepared before it can
// run (incl. PROSPERO, which the researcher registers themselves), then clear
// each gate that exists in meta-pipe's own program by hand. Narrative text is
// bilingual via L(); code / paths / prompts / medical values stay English.

let LANG = localStorage.getItem("mp_lang") || "en";

// Chrome strings (the UI itself). {n}/{f}/{m} are simple placeholders.
const STR = {
  en: {
    badge_demo: "DEMO · replay of bundled example",
    prep_h: "Before you run — prepare these",
    prep_desc: "meta-pipe needs all of this in place before the pipeline starts — including registering the protocol on PROSPERO yourself (the author's position is that registration is out of scope for the tool). Tick each to unlock the run.",
    prepared: "Prepared",
    required: "required",
    begin: "▶ Begin — walk it yourself",
    reset: "↺ Reset",
    gates_cleared: "meta-pipe gates cleared",
    gbadge: "meta-pipe gate",
    pauses: "PIPELINE PAUSES",
    gw_input: "INPUT REQUIRED", gw_upload: "UPLOAD REQUIRED", gw_decision: "DECISION REQUIRED",
    gw_approval: "OPERATOR APPROVAL", gw_checkpoint: "QUALITY CHECKPOINT",
    basis: "basis",
    llm_h: "🔧 LLM configuration — this is what actually screens the records",
    llm_model: "model", llm_prompt: "screening prompt (editable)",
    apply_config: "Apply config",
    llm_loaded: "loaded {f} ({n} chars) — not executed in demo",
    llm_capture: 'config captured: model="{m}", prompt {n} chars — not executed in demo',
    dcap_same: "All {n} records — Reviewer 1, Reviewer 2 and the final decision hold the same values:",
    dcap_cols: "Decision columns across {n} records:",
    g_confirm: "Confirm analysis type",
    g_pdf: "I have supplied the PDFs — continue",
    g_approve: "Approve & continue", g_request: "Request changes",
    g_threshold: "Threshold met — proceed", g_submit: "Submit",
    upload_drop: "⬆ Choose paywalled PDFs (demo: nothing is uploaded)",
    cp_hint: "meta-pipe will not advance unless this threshold passes. In this finished example it does.",
    cont: "Continue →", finish: "Finish — show output",
    out_h: "Final output", prisma_h: "PRISMA 2020 flow", abs_h: "Manuscript abstract", deliv_h: "Deliverables",
    sug_h: "Our suggestions — gates we would add",
    sug_desc: "These are our opinion about what a strict systematic review needs and meta-pipe does not yet enforce. They are not part of the upstream pull request — they live only on this page. Each says why we would add it.",
    sug_badge: "our suggestion", why: "Why",
    about_h: "About this interface",
    about_b: "Rather than auto-playing a polished run, this interface makes you <strong>prepare the prerequisites</strong> and then <strong>clear each meta-pipe gate yourself</strong>, so it is honest about how much the pipeline depends on the operator. Every gate is grounded in meta-pipe's own program and cites its <code>basis</code>; gates we think are <em>missing</em> are kept separate, labelled as ours, and left off the pull request. At screening it also shows the <strong>actual model and prompt</strong> meta-pipe uses — editable and uploadable. It replays the bundled <code>ici-breast-cancer</code> example without running anything.",
    intro: "A web interface for the meta-pipe pipeline. <strong>There is no auto-play.</strong> First you prepare everything meta-pipe needs <em>before</em> it can run; then you advance one stage at a time, clearing each gate that exists in <strong>meta-pipe's own program</strong> by hand. Every gate cites its <code>basis</code> in the repo. At screening you can open and edit the actual <strong>LLM configuration</strong> meta-pipe uses. It replays the bundled <code>ici-breast-cancer</code> example — no API key, no execution.",
    foot: 'Demo replay · meta-pipe by Lin &amp; Yeh · UI is an optional add-on (<code>web/</code>). Live mode requires Claude API billing.',
    lang_btn: "中文",
  },
  zh: {
    badge_demo: "DEMO · 重播內建範例",
    prep_h: "開始之前 — 先準備這些",
    prep_desc: "meta-pipe 在 pipeline 啟動前需要這些全部就緒——包含自行上 PROSPERO 註冊計畫書（原作的立場是註冊不在工具範圍內）。逐項勾選以解鎖執行。",
    prepared: "已準備",
    required: "必填",
    begin: "▶ 開始 — 親手走一遍",
    reset: "↺ 重置",
    gates_cleared: "已清除 meta-pipe gate",
    gbadge: "meta-pipe gate",
    pauses: "PIPELINE 暫停",
    gw_input: "需要輸入", gw_upload: "需要上傳", gw_decision: "需要決策",
    gw_approval: "操作者核准", gw_checkpoint: "品質檢查點",
    basis: "依據",
    llm_h: "🔧 LLM 設定 — 實際拿來篩選紀錄的就是這個",
    llm_model: "model", llm_prompt: "篩選 prompt（可編輯）",
    apply_config: "套用設定",
    llm_loaded: "已載入 {f}（{n} 字元）— demo 不會執行",
    llm_capture: '已擷取設定：model="{m}"、prompt {n} 字元 — demo 不會執行',
    dcap_same: "全部 {n} 筆 — Reviewer 1、Reviewer 2 與最終決定的數值完全相同：",
    dcap_cols: "{n} 筆的決定欄位：",
    g_confirm: "確認分析型別",
    g_pdf: "我已提供 PDF — 繼續",
    g_approve: "核准並繼續", g_request: "要求修改",
    g_threshold: "門檻已達 — 繼續", g_submit: "送出",
    upload_drop: "⬆ 選擇付費 PDF（demo：不會真的上傳）",
    cp_hint: "除非此門檻通過，否則 meta-pipe 不會前進。在這份完成的範例中它通過了。",
    cont: "繼續 →", finish: "完成 — 顯示結果",
    out_h: "最終結果", prisma_h: "PRISMA 2020 流程圖", abs_h: "稿件摘要", deliv_h: "產出物",
    sug_h: "我們的建議 — 我們會補上的 gate",
    sug_desc: "這些是我們對「嚴謹系統性回顧需要、而 meta-pipe 尚未強制」的看法。它們不在上游 pull request 內——只存在於本頁。每條都說明為什麼我們會補。",
    sug_badge: "我們的建議", why: "為什麼",
    about_h: "關於這個介面",
    about_b: "這個介面不會自動播放一段光鮮的流程，而是讓你<strong>先備好前置條件</strong>，再<strong>親手清掉每一道 meta-pipe gate</strong>，因此能誠實呈現 pipeline 有多依賴操作者。每道 gate 都依據 meta-pipe 自己的程式，並標出 <code>basis</code>；我們認為<em>缺少</em>的 gate 另外分開、標明是我們的，不放進 pull request。在篩選階段也會顯示 meta-pipe 實際用的<strong>model 與 prompt</strong>——可編輯、可上傳。它重播內建的 <code>ici-breast-cancer</code> 範例，不會真的執行任何東西。",
    intro: "meta-pipe pipeline 的網頁介面。<strong>沒有自動播放。</strong>你要先把 meta-pipe 在執行<em>之前</em>需要的東西全部備好；接著一次一階前進，<strong>親手</strong>清掉每一道存在於 <strong>meta-pipe 自己程式</strong>裡的 gate。每道 gate 都標出在 repo 裡的 <code>basis</code>。在篩選階段你可以打開並編輯 meta-pipe 實際用的 <strong>LLM 設定</strong>。它重播內建的 <code>ici-breast-cancer</code> 範例 — 無需 API key、不會執行。",
    foot: 'Demo 重播 · meta-pipe by Lin &amp; Yeh · 介面為選用附加（<code>web/</code>）。live 模式需 Claude API 計費。',
    lang_btn: "EN",
  },
};

const t = (k) => (STR[LANG] && STR[LANG][k] != null) ? STR[LANG][k] : (STR.en[k] != null ? STR.en[k] : k);
// L: resolve a bilingual {en,zh} narrative field; pass plain strings through.
const L = (v) => (v && typeof v === "object" && !Array.isArray(v) && ("en" in v || "zh" in v)) ? (v[LANG] != null ? v[LANG] : v.en) : v;

let M = null, SUGG = [];
let frontier = -1;
let clearedGate = {};
let prepChecked = {};
let started = false;

const $ = (s) => document.querySelector(s);
const el = (tag, cls, html) => {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (html != null) e.innerHTML = html;
  return e;
};
const esc = (s) => (s || "").replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));

async function boot() {
  try {
    M = await (await fetch("demo_manifest.json", { cache: "no-cache" })).json();
  } catch (e) {
    $("#proj-title").textContent = "Failed to load demo_manifest.json";
    return;
  }
  applyStaticI18n();
  renderHeader();
  renderPrep();
  buildProgress();
  buildStages();
  $("#gen").textContent = "Generated " + (M.project.generated_at || "");
  $("#btn-begin").addEventListener("click", begin);
  $("#btn-reset").addEventListener("click", reset);
  $("#btn-lang").addEventListener("click", toggleLang);
  loadSuggestions();
  updateGates();
}

function toggleLang() {
  LANG = LANG === "en" ? "zh" : "en";
  localStorage.setItem("mp_lang", LANG);
  document.documentElement.lang = LANG === "zh" ? "zh-Hant" : "en";
  applyStaticI18n();
  renderHeader();
  renderPrep();
  buildStages();   // rebuild cards so metrics / LLM panel / artifacts pick up the new language
  renderSuggestions();
  if (started && frontier >= M.stages.length) renderOutput(true);
}

function applyStaticI18n() {
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.innerHTML = t(node.getAttribute("data-i18n"));
  });
  $("#btn-lang").textContent = t("lang_btn");
  $("#btn-begin").textContent = t("begin");
  $("#btn-reset").textContent = t("reset");
}

function totalProgramGates() {
  return M.stages.reduce((n, s) => n + (s.gates ? s.gates.length : 0), 0);
}

function renderHeader() {
  const p = M.project;
  $("#proj-title").textContent = L(p.title);
  $("#proj-subtitle").textContent = L(p.subtitle);
  const h = $("#headline");
  h.innerHTML = "";
  (p.headline || []).forEach((k) => {
    const kpi = el("div", "kpi");
    kpi.append(el("div", "v", esc(k.value)), el("div", "l", esc(L(k.label))));
    h.append(kpi);
  });
}

// --- pre-run preparation ---------------------------------------------------

function renderPrep() {
  const list = $("#prep-list");
  list.innerHTML = "";
  (M.prep || []).forEach((p, i) => {
    const row = el("label", "prep-item");
    const cb = el("input");
    cb.type = "checkbox";
    cb.checked = !!prepChecked[i];
    cb.disabled = started;
    cb.addEventListener("change", () => { prepChecked[i] = cb.checked; updatePrep(); });
    const body = el("div", "prep-body");
    body.append(
      el("div", "prep-title", esc(L(p.title)) + (p.required ? ` <span class="req">${t("required")}</span>` : "")),
      el("div", "prep-detail", esc(L(p.detail))),
      el("div", "prep-basis", t("basis") + ": " + esc(p.basis))
    );
    row.append(cb, body);
    list.append(row);
  });
  updatePrep();
}

function prepReady() {
  return (M.prep || []).every((p, i) => !p.required || prepChecked[i]);
}

function updatePrep() {
  const total = (M.prep || []).length;
  const done = (M.prep || []).filter((_, i) => prepChecked[i]).length;
  $("#prep-counter").textContent = `${t("prepared")}: ${done} / ${total}`;
  $("#btn-begin").disabled = started || !prepReady();
}

// --- progress --------------------------------------------------------------

function buildProgress() {
  const bar = $("#progress");
  bar.innerHTML = "";
  M.stages.forEach((s) => {
    const seg = el("div", "seg");
    seg.title = `${s.num} ${L(s.name)}`;
    bar.append(seg);
  });
  paintProgress();
}

function paintProgress() {
  document.querySelectorAll("#progress .seg").forEach((seg, i) => {
    seg.className = "seg";
    if (i < frontier) seg.classList.add("done");
    else if (i === frontier) seg.classList.add((M.stages[i].gates || []).length ? "gate" : "active");
  });
}

// --- stages ----------------------------------------------------------------

function buildStages() {
  const box = $("#stages");
  box.innerHTML = "";
  M.stages.forEach((s, i) => box.append(stageCard(s, i)));
  render();
}

function stageCard(s, i) {
  const c = el("article", "stage");
  c.id = "stage-" + i;
  const head = el("div", "head");
  head.append(el("span", "num", s.num), el("h2", null, esc(L(s.name))), el("span", "skill", esc(s.skill || "")));
  c.append(head);
  c.append(el("p", "summary", esc(L(s.summary))));

  if (s.metrics && s.metrics.length) {
    const m = el("div", "metrics");
    s.metrics.forEach((x) => m.append(el("span", "m", `${esc(L(x.label))} <b>${esc(x.value)}</b>`)));
    c.append(m);
  }
  if (s.llm) c.append(llmPanel(s.llm));

  if (s.artifacts && s.artifacts.length) {
    const a = el("div", "artifacts");
    s.artifacts.forEach((art) => {
      if (!art.preview) return;
      const d = el("details", "art");
      d.append(
        el("summary", null, `<span class="kind">${esc(art.kind)}</span> ${esc(art.name)}`),
        el("pre", "preview", esc(art.preview))
      );
      a.append(d);
    });
    if (a.children.length) c.append(a);
  }
  c.append(el("div", "actionzone"));
  return c;
}

// --- the LLM configuration reveal (screening) ------------------------------

function llmPanel(llm) {
  const p = el("section", "llm");
  p.append(el("div", "llm-h", t("llm_h")));
  p.append(el("div", "llm-src", `source: <code>${esc(llm.source)}</code>`));

  const model = el("label", "llm-field");
  model.innerHTML = `<span>${t("llm_model")}</span>`;
  const modelIn = el("input", "llm-input");
  modelIn.type = "text"; modelIn.value = llm.model || "";
  model.append(modelIn);
  p.append(model);

  const pf = el("label", "llm-field");
  pf.innerHTML = `<span>${t("llm_prompt")}</span>`;
  const ta = el("textarea", "llm-prompt");
  ta.value = llm.prompt || ""; ta.rows = 10;
  pf.append(ta);
  p.append(pf);

  const row = el("div", "llm-actions");
  const file = el("input", "llm-file"); file.type = "file"; file.accept = ".txt,.md,.json,.py";
  const apply = el("button", "ghost small", t("apply_config"));
  const note = el("span", "llm-note", "");
  file.addEventListener("change", () => {
    const f = file.files && file.files[0];
    if (!f) return;
    f.text().then((tx) => { ta.value = tx; note.textContent = t("llm_loaded").replace("{f}", f.name).replace("{n}", tx.length); });
  });
  apply.addEventListener("click", () => {
    note.textContent = t("llm_capture").replace("{m}", modelIn.value.slice(0, 40)).replace("{n}", ta.value.length);
  });
  row.append(file, apply, note);
  p.append(row);

  p.append(el("div", "llm-mech", esc(L(llm.reviewer_mechanism))));
  if (llm.decisions && llm.decisions.counts) p.append(decisionsTable(llm.decisions));
  return p;
}

function decisionsTable(d) {
  const wrap = el("div", "llm-decisions");
  const cap = (d.identical ? t("dcap_same") : t("dcap_cols")).replace("{n}", d.total);
  wrap.append(el("div", "llm-cap", cap));
  const tb = el("table", "dtbl");
  const order = ["include", "maybe", "exclude"];
  tb.append(el("tr", null, "<th>column</th>" + order.map((o) => `<th>${o}</th>`).join("")));
  (d.columns || []).forEach((col) => {
    const c = d.counts[col] || {};
    tb.append(el("tr", null, `<td><code>${esc(col)}</code></td>` + order.map((o) => `<td>${c[o] ?? 0}</td>`).join("")));
  });
  wrap.append(tb);
  return wrap;
}

// --- gates -----------------------------------------------------------------

function gatePanel(i, gi, g, onClear) {
  const p = el("div", "gate type-" + g.type);
  p.append(el("div", "gh",
    `<span class="gbadge">${t("gbadge")}</span> ${GATE_ICON[g.type] || "⏸"} ${t("pauses")} — ${t("gw_" + g.type)}`));
  p.append(el("div", "gl", esc(L(g.label))));
  p.append(el("div", "gd", esc(L(g.detail))));
  if (g.basis) p.append(el("div", "gbasis", t("basis") + ": " + esc(g.basis)));
  p.append(gateControl(i, gi, g, onClear));
  return p;
}

const GATE_ICON = { input: "⌨", upload: "⬆", decision: "⑂", approval: "✓", checkpoint: "⛳" };

function gateControl(i, gi, g, onClear) {
  const box = el("div", "gctl");
  const done = () => { clearedGate[i + ":" + gi] = true; onClear(); };

  if (g.type === "decision") {
    const opt = el("div", "gctl-radios");
    opt.innerHTML =
      '<label><input type="radio" name="d' + i + gi + '" value="pairwise" checked> pairwise</label>' +
      '<label><input type="radio" name="d' + i + gi + '" value="network"> network (NMA)</label>';
    const b = el("button", "primary small", t("g_confirm"));
    b.addEventListener("click", done);
    box.append(opt, b);
  } else if (g.type === "upload") {
    const drop = el("label", "gctl-drop", t("upload_drop"));
    const file = el("input"); file.type = "file"; file.multiple = true; file.style.display = "none";
    drop.append(file);
    const b = el("button", "primary small", t("g_pdf"));
    b.addEventListener("click", done);
    box.append(drop, b);
  } else if (g.type === "input") {
    const ta = el("textarea", "gctl-ta"); ta.rows = 3;
    const b = el("button", "primary small", t("g_submit"));
    b.addEventListener("click", done);
    box.append(ta, b);
  } else if (g.type === "checkpoint") {
    const b = el("button", "primary small", t("g_threshold"));
    b.addEventListener("click", done);
    box.append(el("div", "gctl-hint", t("cp_hint")), b);
  } else {
    const b1 = el("button", "primary small", t("g_approve"));
    const b2 = el("button", "ghost small", t("g_request"));
    b1.addEventListener("click", done); b2.addEventListener("click", done);
    box.append(b1, b2);
  }
  return box;
}

// --- flow ------------------------------------------------------------------

function begin() {
  if (started || !prepReady()) return;
  started = true;
  frontier = 0;
  $("#btn-begin").classList.add("hidden");
  $("#prep").classList.add("locked");
  $("#prep-list").querySelectorAll("input").forEach((c) => (c.disabled = true));
  render();
  scrollToStage(0);
}

function advance() {
  frontier++;
  render();
  if (frontier < M.stages.length) scrollToStage(frontier);
  else { $("#output").classList.remove("hidden"); renderOutput(true); scrollToEl($("#output")); }
}

function render() {
  M.stages.forEach((s, i) => {
    const card = $("#stage-" + i);
    card.classList.toggle("shown", i <= frontier && started);
    card.classList.toggle("active", i === frontier && started);
    card.classList.toggle("done", i < frontier);

    // re-render dynamic narrative on language toggle
    card.querySelector(".head h2").textContent = L(s.name);
    card.querySelector(".summary").textContent = L(s.summary);

    const az = card.querySelector(".actionzone");
    az.innerHTML = "";
    if (i !== frontier || !started) return;
    const gates = s.gates || [];
    const nextGate = gates.findIndex((_, gi) => !clearedGate[i + ":" + gi]);
    if (nextGate !== -1) {
      az.append(gatePanel(i, nextGate, gates[nextGate], advance));
    } else {
      const b = el("button", "primary", i === M.stages.length - 1 ? t("finish") : t("cont"));
      b.addEventListener("click", advance);
      az.append(b);
    }
  });
  paintProgress();
  updateGates();
}

function updateGates() {
  const total = totalProgramGates();
  let done = 0;
  M.stages.forEach((s, i) => (s.gates || []).forEach((_, gi) => {
    if (clearedGate[i + ":" + gi] || i < frontier) done++;
  }));
  $("#counter").textContent = `${t("gates_cleared")}: ${started ? done : 0} / ${total}`;
}

function reset() {
  started = false; frontier = -1; clearedGate = {};
  $("#btn-begin").classList.remove("hidden");
  $("#prep").classList.remove("locked");
  renderPrep();
  $("#output").classList.add("hidden");
  render();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function scrollToStage(i) { scrollToEl($("#stage-" + i)); }
function scrollToEl(node) { if (node) node.scrollIntoView({ behavior: "smooth", block: "center" }); }

// --- suggestions (our opinion; present only on our deployed page) ----------

async function loadSuggestions() {
  try {
    const r = await fetch("suggestions.json", { cache: "no-cache" });
    if (!r.ok) return;
    SUGG = (await r.json()).suggestions || [];
  } catch (e) { return; }
  renderSuggestions();
}

function renderSuggestions() {
  if (!SUGG.length) return;
  const box = $("#suggest-list");
  box.innerHTML = "";
  SUGG.forEach((s) => {
    const c = el("div", "suggest-item");
    c.append(
      el("div", "suggest-h", `<span class="sbadge">${t("sug_badge")}</span> ${esc(L(s.title))}`),
      el("div", "suggest-where", esc(L(s.where))),
      el("div", "suggest-why", t("why") + ": " + esc(L(s.why)))
    );
    box.append(c);
  });
  $("#suggestions").classList.remove("hidden");
}

function renderOutput(force) {
  const o = M.output || {};
  if (o.prisma_svg && force) {
    fetch(o.prisma_svg).then((r) => r.text()).then((svg) => { $("#prisma").innerHTML = svg; }).catch(() => {});
  }
  $("#abstract").textContent = o.abstract || "";
  const dl = $("#downloads");
  dl.innerHTML = "";
  (o.downloads || []).forEach((d) => {
    dl.append(el("li", null, `<strong>${esc(L(d.label))}</strong> — <span class="note">${esc(L(d.note))}</span>`));
  });
}

boot();
