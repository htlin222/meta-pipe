// meta-pipe web demo — replays the bundled example project stage by stage.
// Pure static: fetches demo_manifest.json, renders, and lets the visitor step
// through. The point is to surface the human-gate pauses, not to run anything.

const GATE_ICON = {
  input: "⌨", upload: "⬆", decision: "⑂", review: "✓", "human-action": "↗",
};
const GATE_WORD = {
  input: "INPUT REQUIRED", upload: "UPLOAD REQUIRED", decision: "DECISION REQUIRED",
  review: "HUMAN REVIEW", "human-action": "OFF-PLATFORM ACTION",
};

let M = null;            // manifest
let shown = 0;           // how many stages are revealed
let autoTimer = null;

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

  $("#btn-step").addEventListener("click", step);
  $("#btn-auto").addEventListener("click", toggleAuto);
  $("#btn-reset").addEventListener("click", reset);
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
    seg.dataset.i = i;
    seg.title = `${s.num} ${s.name}`;
    bar.append(seg);
  });
  paintProgress();
}

function paintProgress() {
  document.querySelectorAll("#progress .seg").forEach((seg, i) => {
    seg.className = "seg";
    if (i < shown - 1) seg.classList.add("done");
    else if (i === shown - 1) {
      const g = M.stages[i].gate;
      seg.classList.add(g ? "gate" : "active");
    }
  });
}

function buildStages() {
  const box = $("#stages");
  box.innerHTML = "";
  M.stages.forEach((s, i) => box.append(stageCard(s, i)));
  refreshStages();
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

  if (s.gate) c.append(gatePanel(s.gate));

  if (s.artifacts && s.artifacts.length) {
    const a = el("div", "artifacts");
    s.artifacts.forEach((art) => {
      if (!art.preview) return;
      const d = el("details", "art");
      const sum = el("summary", null, `<span class="kind">${esc(art.kind)}</span> ${esc(art.name)}`);
      d.append(sum, el("pre", "preview", esc(art.preview)));
      a.append(d);
    });
    if (a.children.length) c.append(a);
  }
  return c;
}

function gatePanel(g) {
  const p = el("div", "gate");
  p.append(el("div", "gh", `${GATE_ICON[g.type] || "⏸"} ⏸ PIPELINE PAUSES — ${GATE_WORD[g.type] || "OPERATOR INPUT"}`));
  p.append(el("div", "gl", esc(g.label)));
  p.append(el("div", "gd", esc(g.detail)));
  if (g.type === "upload") {
    p.append(el("div", "ghost-input upload", "⬆ &nbsp;Drop full-text PDFs here &nbsp;<span class='muted'>(disabled in demo)</span>"));
  } else if (g.type === "input") {
    p.append(el("div", "ghost-input", "⌨ &nbsp;[ research question text box ] &nbsp;<span class='muted'>(prefilled from TOPIC.txt in demo)</span>"));
  } else if (g.type === "decision") {
    p.append(el("div", "ghost-input", "⑂ &nbsp;( ◉ pairwise &nbsp; ○ network ) &nbsp;<span class='muted'>(operator must choose)</span>"));
  } else if (g.type === "review") {
    p.append(el("div", "ghost-input", "✓ &nbsp;[ approve ] &nbsp;[ edit ] &nbsp;<span class='muted'>(sign-off required)</span>"));
  }
  return p;
}

function refreshStages() {
  M.stages.forEach((s, i) => {
    $("#stage-" + i).classList.toggle("shown", i < shown);
  });
  paintProgress();
  const done = shown >= M.stages.length;
  $("#btn-step").disabled = done;
  $("#btn-step").textContent = shown === 0 ? "▶ Step through pipeline" : done ? "✓ Pipeline complete" : "▶ Next stage";
  $("#output").classList.toggle("hidden", !done);
  if (done) renderOutput();
}

function step() {
  if (shown < M.stages.length) {
    shown++;
    refreshStages();
    const node = $("#stage-" + (shown - 1));
    if (node) node.scrollIntoView({ behavior: "smooth", block: "center" });
  }
}

function toggleAuto() {
  if (autoTimer) { clearInterval(autoTimer); autoTimer = null; $("#btn-auto").textContent = "⏩ Auto-play"; return; }
  $("#btn-auto").textContent = "⏸ Pause";
  autoTimer = setInterval(() => {
    if (shown >= M.stages.length) { clearInterval(autoTimer); autoTimer = null; $("#btn-auto").textContent = "⏩ Auto-play"; return; }
    step();
  }, 900);
}

function reset() {
  if (autoTimer) { clearInterval(autoTimer); autoTimer = null; $("#btn-auto").textContent = "⏩ Auto-play"; }
  shown = 0;
  refreshStages();
  window.scrollTo({ top: 0, behavior: "smooth" });
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
    const li = el("li", null, `<strong>${esc(d.label)}</strong> — <span class="note">${esc(d.note)}</span>`);
    dl.append(li);
  });
}

boot();
