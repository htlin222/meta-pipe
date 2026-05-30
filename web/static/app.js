// meta-pipe web interface — you prepare, then you walk it yourself.
//
// No auto-play. First you tick off everything meta-pipe needs prepared before it
// can run (incl. PROSPERO, which the researcher registers themselves). Then you
// advance one stage at a time, clearing each gate that exists in meta-pipe's own
// program by hand. Gates carry a `basis` pointing at where in the repo they come
// from. Our own suggested gates (what meta-pipe lacks) are shown separately and
// are NOT part of the upstream PR.

const GATE_ICON = { input: "⌨", upload: "⬆", decision: "⑂", approval: "✓", checkpoint: "⛳" };
const GATE_WORD = {
  input: "INPUT REQUIRED", upload: "UPLOAD REQUIRED", decision: "DECISION REQUIRED",
  approval: "OPERATOR APPROVAL", checkpoint: "QUALITY CHECKPOINT",
};

let M = null;
let frontier = -1;
let clearedGate = {};       // "stage:gate" -> bool
let prepChecked = {};       // prep index -> bool
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
  renderHeader();
  renderPrep();
  buildProgress();
  buildStages();
  $("#gen").textContent = "Generated " + (M.project.generated_at || "");
  $("#btn-begin").addEventListener("click", begin);
  $("#btn-reset").addEventListener("click", reset);
  loadSuggestions();
  updateGates();
}

function totalProgramGates() {
  return M.stages.reduce((n, s) => n + (s.gates ? s.gates.length : 0), 0);
}

function renderHeader() {
  const p = M.project;
  $("#proj-title").textContent = p.title;
  $("#proj-subtitle").textContent = p.subtitle;
  const h = $("#headline");
  h.innerHTML = "";
  (p.headline || []).forEach((k) => {
    const kpi = el("div", "kpi");
    kpi.append(el("div", "v", esc(k.value)), el("div", "l", esc(k.label)));
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
    cb.addEventListener("change", () => { prepChecked[i] = cb.checked; updatePrep(); });
    const body = el("div", "prep-body");
    body.append(
      el("div", "prep-title", esc(p.title) + (p.required ? ' <span class="req">required</span>' : "")),
      el("div", "prep-detail", esc(p.detail)),
      el("div", "prep-basis", "basis: " + esc(p.basis))
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
  $("#prep-counter").textContent = `Prepared: ${done} / ${total}`;
  $("#btn-begin").disabled = started || !prepReady();
}

// --- progress --------------------------------------------------------------

function buildProgress() {
  const bar = $("#progress");
  bar.innerHTML = "";
  M.stages.forEach((s) => {
    const seg = el("div", "seg");
    seg.title = `${s.num} ${s.name}`;
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
  head.append(el("span", "num", s.num), el("h2", null, esc(s.name)), el("span", "skill", esc(s.skill || "")));
  c.append(head);
  c.append(el("p", "summary", esc(s.summary)));

  if (s.metrics && s.metrics.length) {
    const m = el("div", "metrics");
    s.metrics.forEach((x) => m.append(el("span", "m", `${esc(x.label)} <b>${esc(x.value)}</b>`)));
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
  p.append(el("div", "llm-h", "🔧 LLM configuration — this is what actually screens the records"));
  p.append(el("div", "llm-src", `source: <code>${esc(llm.source)}</code>`));

  const model = el("label", "llm-field");
  model.innerHTML = "<span>model</span>";
  const modelIn = el("input", "llm-input");
  modelIn.type = "text"; modelIn.value = llm.model || "";
  model.append(modelIn);
  p.append(model);

  const pf = el("label", "llm-field");
  pf.innerHTML = "<span>screening prompt (editable)</span>";
  const ta = el("textarea", "llm-prompt");
  ta.value = llm.prompt || ""; ta.rows = 10;
  pf.append(ta);
  p.append(pf);

  const row = el("div", "llm-actions");
  const file = el("input", "llm-file"); file.type = "file"; file.accept = ".txt,.md,.json,.py";
  const apply = el("button", "ghost small", "Apply config");
  const note = el("span", "llm-note", "");
  file.addEventListener("change", () => {
    const f = file.files && file.files[0];
    if (!f) return;
    f.text().then((t) => { ta.value = t; note.textContent = `loaded ${f.name} (${t.length} chars) — not executed in demo`; });
  });
  apply.addEventListener("click", () => {
    note.textContent = `config captured: model="${modelIn.value.slice(0, 40)}", prompt ${ta.value.length} chars — not executed in demo`;
  });
  row.append(file, apply, note);
  p.append(row);

  p.append(el("div", "llm-mech", esc(llm.reviewer_mechanism)));
  if (llm.decisions && llm.decisions.counts) p.append(decisionsTable(llm.decisions));
  return p;
}

function decisionsTable(d) {
  const wrap = el("div", "llm-decisions");
  wrap.append(el("div", "llm-cap", d.identical
    ? `All ${d.total} records — Reviewer 1, Reviewer 2 and the final decision hold the same values:`
    : `Decision columns across ${d.total} records:`));
  const t = el("table", "dtbl");
  const order = ["include", "maybe", "exclude"];
  t.append(el("tr", null, "<th>column</th>" + order.map((o) => `<th>${o}</th>`).join("")));
  (d.columns || []).forEach((col) => {
    const c = d.counts[col] || {};
    t.append(el("tr", null, `<td><code>${esc(col)}</code></td>` + order.map((o) => `<td>${c[o] ?? 0}</td>`).join("")));
  });
  wrap.append(t);
  return wrap;
}

// --- gates -----------------------------------------------------------------

function gatePanel(i, gi, g, onClear) {
  const p = el("div", "gate type-" + g.type);
  p.append(el("div", "gh",
    `<span class="gbadge">meta-pipe gate</span> ${GATE_ICON[g.type] || "⏸"} PIPELINE PAUSES — ${GATE_WORD[g.type] || "OPERATOR INPUT"}`));
  p.append(el("div", "gl", esc(g.label)));
  p.append(el("div", "gd", esc(g.detail)));
  if (g.basis) p.append(el("div", "gbasis", "basis: " + esc(g.basis)));
  p.append(gateControl(i, gi, g, onClear));
  return p;
}

function gateControl(i, gi, g, onClear) {
  const box = el("div", "gctl");
  const done = () => { clearedGate[i + ":" + gi] = true; onClear(); };

  if (g.type === "decision") {
    const opt = el("div", "gctl-radios");
    opt.innerHTML =
      '<label><input type="radio" name="d' + i + gi + '" value="pairwise" checked> pairwise</label>' +
      '<label><input type="radio" name="d' + i + gi + '" value="network"> network (NMA)</label>';
    const b = el("button", "primary small", "Confirm analysis type");
    b.addEventListener("click", done);
    box.append(opt, b);
  } else if (g.type === "upload") {
    const drop = el("label", "gctl-drop", "⬆ Choose paywalled PDFs (demo: nothing is uploaded)");
    const file = el("input"); file.type = "file"; file.multiple = true; file.style.display = "none";
    drop.append(file);
    const b = el("button", "primary small", "I have supplied the PDFs — continue");
    b.addEventListener("click", done);
    box.append(drop, b);
  } else if (g.type === "input") {
    const ta = el("textarea", "gctl-ta"); ta.rows = 3;
    const b = el("button", "primary small", "Submit");
    b.addEventListener("click", done);
    box.append(ta, b);
  } else if (g.type === "checkpoint") {
    const b = el("button", "primary small", "Threshold met — proceed");
    b.addEventListener("click", done);
    box.append(el("div", "gctl-hint", "meta-pipe will not advance unless this threshold passes. In this finished example it does."), b);
  } else { // approval
    const b1 = el("button", "primary small", "Approve & continue");
    const b2 = el("button", "ghost small", "Request changes");
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
  else { $("#output").classList.remove("hidden"); renderOutput(); scrollToEl($("#output")); }
}

function render() {
  M.stages.forEach((s, i) => {
    const card = $("#stage-" + i);
    card.classList.toggle("shown", i <= frontier && started);
    card.classList.toggle("active", i === frontier && started);
    card.classList.toggle("done", i < frontier);

    const az = card.querySelector(".actionzone");
    az.innerHTML = "";
    if (i !== frontier || !started) return;

    const gates = s.gates || [];
    const nextGate = gates.findIndex((_, gi) => !clearedGate[i + ":" + gi]);
    if (nextGate !== -1) {
      az.append(gatePanel(i, nextGate, gates[nextGate], advance));
    } else {
      const b = el("button", "primary", i === M.stages.length - 1 ? "Finish — show output" : "Continue →");
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
  $("#counter").textContent = `meta-pipe gates cleared: ${started ? done : 0} / ${total}`;
}

function reset() {
  started = false; frontier = -1; clearedGate = {};
  $("#btn-begin").classList.remove("hidden");
  $("#prep").classList.remove("locked");
  $("#prep-list").querySelectorAll("input").forEach((c) => (c.disabled = false));
  $("#output").classList.add("hidden");
  updatePrep();
  render();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function scrollToStage(i) { scrollToEl($("#stage-" + i)); }
function scrollToEl(node) { if (node) node.scrollIntoView({ behavior: "smooth", block: "center" }); }

// --- suggestions (our opinion; present only on our deployed page) ----------

async function loadSuggestions() {
  let data;
  try {
    const r = await fetch("suggestions.json", { cache: "no-cache" });
    if (!r.ok) return;
    data = await r.json();
  } catch (e) { return; }
  const items = (data && data.suggestions) || [];
  if (!items.length) return;
  const box = $("#suggest-list");
  box.innerHTML = "";
  items.forEach((s) => {
    const c = el("div", "suggest-item");
    c.append(
      el("div", "suggest-h", `<span class="sbadge">our suggestion</span> ${esc(s.title)}`),
      el("div", "suggest-where", esc(s.where)),
      el("div", "suggest-why", "Why: " + esc(s.why))
    );
    box.append(c);
  });
  $("#suggestions").classList.remove("hidden");
}

let outputRendered = false;
function renderOutput() {
  if (outputRendered) return;
  outputRendered = true;
  const o = M.output || {};
  if (o.prisma_svg) {
    fetch(o.prisma_svg).then((r) => r.text()).then((svg) => { $("#prisma").innerHTML = svg; }).catch(() => {});
  }
  $("#abstract").textContent = o.abstract || "";
  const dl = $("#downloads");
  dl.innerHTML = "";
  (o.downloads || []).forEach((d) => {
    dl.append(el("li", null, `<strong>${esc(d.label)}</strong> — <span class="note">${esc(d.note)}</span>`));
  });
}

boot();
