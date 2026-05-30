// meta-pipe web interface — you walk it yourself.
//
// There is no auto-play. The pipeline advances one stage at a time, and every
// human gate must be cleared by hand (type the topic, choose the analysis type,
// upload the PDFs, approve the extraction). At screening the real LLM config is
// surfaced and editable. It replays the bundled ici-breast-cancer example.

const GATE_ICON = {
  input: "⌨", upload: "⬆", decision: "⑂", review: "✓", "human-action": "↗",
};
const GATE_WORD = {
  input: "INPUT REQUIRED", upload: "UPLOAD REQUIRED", decision: "DECISION REQUIRED",
  review: "HUMAN REVIEW", "human-action": "OFF-PLATFORM ACTION",
};

let M = null;
let frontier = -1;          // active stage index; < frontier = done, > = hidden
let cleared = {};           // stage index -> gate cleared?
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
  buildProgress();
  buildStages();
  $("#gen").textContent = "Generated " + (M.project.generated_at || "");
  $("#btn-begin").addEventListener("click", begin);
  $("#btn-reset").addEventListener("click", reset);
  updateCounter();
}

function gateStages() {
  return M.stages.filter((s) => s.gate).length;
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

function buildProgress() {
  const bar = $("#progress");
  bar.innerHTML = "";
  M.stages.forEach((s, i) => {
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
    else if (i === frontier) seg.classList.add(M.stages[i].gate ? "gate" : "active");
  });
}

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

  // The gate panel + the action zone (Continue / gate control) live at the end.
  if (s.gate) c.append(gatePanel(s.gate));
  c.append(el("div", "actionzone"));
  return c;
}

// --- the LLM configuration reveal (screening) ------------------------------

function llmPanel(llm) {
  const p = el("section", "llm card-in");
  p.append(el("div", "llm-h", "🔧 LLM configuration — this is what actually screens the records"));
  p.append(el("div", "llm-src", `source: <code>${esc(llm.source)}</code>`));

  const model = el("label", "llm-field");
  model.innerHTML = "<span>model</span>";
  const modelIn = el("input", "llm-input");
  modelIn.type = "text";
  modelIn.value = llm.model || "";
  model.append(modelIn);
  p.append(model);

  const pf = el("label", "llm-field");
  pf.innerHTML = "<span>screening prompt (editable)</span>";
  const ta = el("textarea", "llm-prompt");
  ta.value = llm.prompt || "";
  ta.rows = 10;
  pf.append(ta);
  p.append(pf);

  // upload / apply your own config
  const row = el("div", "llm-actions");
  const file = el("input", "llm-file");
  file.type = "file";
  file.accept = ".txt,.md,.json,.py";
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

  // the reviewer mechanism + the identical-columns proof
  p.append(el("div", "llm-mech", esc(llm.reviewer_mechanism)));
  if (llm.decisions && llm.decisions.counts) p.append(decisionsTable(llm.decisions));
  return p;
}

function decisionsTable(d) {
  const wrap = el("div", "llm-decisions");
  const cap = d.identical
    ? `All ${d.total} records — Reviewer 1, Reviewer 2 and the final decision hold the same values:`
    : `Decision columns across ${d.total} records:`;
  wrap.append(el("div", "llm-cap", cap));
  const t = el("table", "dtbl");
  const order = ["include", "maybe", "exclude"];
  const thead = el("tr", null, "<th>column</th>" + order.map((o) => `<th>${o}</th>`).join(""));
  t.append(thead);
  (d.columns || []).forEach((col) => {
    const c = d.counts[col] || {};
    t.append(el("tr", null, `<td><code>${esc(col)}</code></td>` + order.map((o) => `<td>${c[o] ?? 0}</td>`).join("")));
  });
  wrap.append(t);
  return wrap;
}

// --- gates -----------------------------------------------------------------

function gatePanel(g) {
  const p = el("div", "gate");
  p.append(el("div", "gh", `${GATE_ICON[g.type] || "⏸"} ⏸ PIPELINE PAUSES — ${GATE_WORD[g.type] || "OPERATOR INPUT"}`));
  p.append(el("div", "gl", esc(g.label)));
  p.append(el("div", "gd", esc(g.detail)));
  return p;
}

// The interactive control the user must operate to clear a gate, injected into
// the active stage's action zone.
function gateControl(i, g, onClear) {
  const box = el("div", "gctl");
  const done = () => { cleared[i] = true; onClear(); };

  if (g.type === "input") {
    const ta = el("textarea", "gctl-ta");
    ta.rows = 3;
    ta.value = (M.stages[i].artifacts && M.stages[i].artifacts[0] && M.stages[i].artifacts[0].preview) || "";
    const b = el("button", "primary small", "Submit research question");
    b.addEventListener("click", done);
    box.append(ta, b);
  } else if (g.type === "decision") {
    const opt = el("div", "gctl-radios");
    opt.innerHTML =
      '<label><input type="radio" name="atype' + i + '" value="pairwise" checked> pairwise</label>' +
      '<label><input type="radio" name="atype' + i + '" value="network"> network (NMA)</label>';
    const b = el("button", "primary small", "Confirm analysis type");
    b.addEventListener("click", done);
    box.append(opt, b);
  } else if (g.type === "upload") {
    const drop = el("label", "gctl-drop", "⬆ Choose paywalled PDFs (demo: nothing is uploaded)");
    const file = el("input", null);
    file.type = "file";
    file.multiple = true;
    file.style.display = "none";
    drop.append(file);
    const b = el("button", "primary small", "I have supplied the PDFs — continue");
    b.addEventListener("click", done);
    box.append(drop, b);
  } else if (g.type === "review") {
    const b1 = el("button", "primary small", "Approve & continue");
    const b2 = el("button", "ghost small", "Request changes");
    b1.addEventListener("click", done);
    b2.addEventListener("click", done);
    box.append(b1, b2);
  } else if (g.type === "human-action") {
    const lab = el("label", "gctl-check");
    lab.innerHTML = '<input type="checkbox"> I have registered the protocol on PROSPERO myself';
    const b = el("button", "primary small", "Continue");
    b.disabled = true;
    lab.querySelector("input").addEventListener("change", (e) => { b.disabled = !e.target.checked; });
    b.addEventListener("click", done);
    box.append(lab, b);
  } else {
    const b = el("button", "primary small", "Continue");
    b.addEventListener("click", done);
    box.append(b);
  }
  return box;
}

// --- flow ------------------------------------------------------------------

function begin() {
  if (started) return;
  started = true;
  frontier = 0;
  $("#btn-begin").classList.add("hidden");
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

    if (s.gate && !cleared[i]) {
      az.append(gateControl(i, s.gate, advance));
    } else {
      const b = el("button", "primary", i === M.stages.length - 1 ? "Finish — show output" : "Continue →");
      b.addEventListener("click", advance);
      az.append(b);
    }
  });
  paintProgress();
  updateCounter();
}

function updateCounter() {
  const total = gateStages();
  let done = 0;
  M.stages.forEach((s, i) => { if (s.gate && (cleared[i] || i < frontier)) done++; });
  $("#counter").textContent = `Human gates cleared: ${started ? done : 0} / ${total}`;
}

function reset() {
  started = false;
  frontier = -1;
  cleared = {};
  $("#btn-begin").classList.remove("hidden");
  $("#output").classList.add("hidden");
  render();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function scrollToStage(i) { scrollToEl($("#stage-" + i)); }
function scrollToEl(node) { if (node) node.scrollIntoView({ behavior: "smooth", block: "center" }); }

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
