const pptxgen = require("pptxgenjs");
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.author = "Lin HT, Yeh JT";
pres.title = "meta-pipe: an AI-assisted, reproducible pipeline for systematic review and meta-analysis";

// Restrained academic palette: charcoal text, one deep-blue accent, light grey tint
const INK = "1F2933";
const BLUE = "1F4E79";
const MUTED = "5B6770";
const TINT = "EEF2F5";
const RULE = "C8D0D8";
const WHITE = "FFFFFF";
const HIGHLIGHT = "9A3412"; // used sparingly for gate thresholds

const HEAD = "Cambria";
const BODY = "Calibri";
const MONO = "Courier New";
const W = 13.33;
const H = 7.5;
const M = 0.7;

function text(slide, t, o) {
  slide.addText(t, Object.assign({ fontFace: BODY, color: INK, isTextBox: true, margin: 0, valign: "top" }, o));
}

function title(slide, t) {
  text(slide, t, { x: M, y: 0.5, w: W - 2 * M, h: 0.7, fontSize: 28, bold: true, color: INK, fontFace: HEAD });
}

function section(slide, t) {
  text(slide, t, { x: M, y: 0.22, w: 8, h: 0.28, fontSize: 11, color: BLUE, fontFace: BODY, charSpacing: 1.5 });
}

function tag(slide, x, y, label, w) {
  const tw = w || 0.55;
  slide.addShape(pres.ShapeType.rect, { x, y, w: tw, h: 0.32, fill: { color: BLUE }, line: { color: BLUE } });
  text(slide, label, { x, y, w: tw, h: 0.32, align: "center", valign: "middle", fontSize: 11, bold: true, color: WHITE, fontFace: MONO });
}

function box(slide, x, y, w, h, fill, lineColor) {
  slide.addShape(pres.ShapeType.rect, { x, y, w, h, fill: { color: fill || TINT }, line: { color: lineColor || fill || TINT, width: 0.75 } });
}

function arrow(slide, x, y, len) {
  slide.addShape(pres.ShapeType.rightArrow, { x, y, w: len, h: 0.26, fill: { color: RULE }, line: { color: RULE } });
}

function footer(slide, n) {
  text(slide, "meta-pipe  ·  github.com/htlin222/meta-pipe", { x: M, y: H - 0.45, w: 6, h: 0.25, fontSize: 9, color: MUTED });
  text(slide, String(n), { x: W - M - 1, y: H - 0.45, w: 1, h: 0.25, fontSize: 9, color: MUTED, align: "right" });
}

function bullets(slide, items, o) {
  const runs = items.map((s, i) => ({ text: s, options: { bullet: { indent: 12 }, breakLine: i < items.length - 1, paraSpaceAfter: 7 } }));
  text(slide, runs, Object.assign({ fontSize: 13, color: INK }, o));
}

function note(slide, t, y) {
  text(slide, t, { x: M, y: y || 6.45, w: W - 2 * M, h: 0.45, fontSize: 10.5, color: MUTED, italic: true });
}

const STAGES = [
  ["00", "Topic intake", "TOPIC.txt, feasibility report"],
  ["01", "Protocol", "pico.yaml, eligibility.md"],
  ["02", "Search", "round-01/dedupe.bib"],
  ["03", "Screening", "decisions.csv, agreement.md"],
  ["04", "Full text", "manifest.csv, fulltext_decisions.csv"],
  ["05", "Extraction", "extraction.csv, data-dictionary.md"],
  ["06", "Analysis", "figures/, tables/, renv.lock"],
  ["07", "Manuscript", "*.qmd, index.pdf"],
  ["08", "Review", "grade_summary.csv, rob2_assessment.csv"],
  ["09", "QA", "final_qa_report.md"],
  ["10", "Submission", "PROSPERO record, journal package"],
];

let n = 0;

// ---------- 1. Title ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  text(s, "meta-pipe", { x: M, y: 1.6, w: 11, h: 0.9, fontSize: 44, bold: true, color: INK, fontFace: HEAD });
  text(s, "An AI-assisted, reproducible pipeline for systematic review and meta-analysis", { x: M, y: 2.55, w: 11.5, h: 1.0, fontSize: 24, color: INK, fontFace: HEAD });
  slide_rule(s, 3.85);
  text(s, "Hsieh-Ting Lin, Jiunn-Tyng Yeh", { x: M, y: 4.1, w: 8, h: 0.4, fontSize: 16, color: INK });
  text(s, "Source code and example project: github.com/htlin222/meta-pipe", { x: M, y: 4.55, w: 10, h: 0.35, fontSize: 13, color: MUTED });
  text(s, "Academic and non-commercial use licence  ·  2026", { x: M, y: 4.9, w: 10, h: 0.35, fontSize: 13, color: MUTED });
  s.addNotes("Overview of the pipeline architecture, its quality controls, one worked example, and current limitations. The software and the example project are public.");
}

function slide_rule(s, y) {
  s.addShape(pres.ShapeType.line, { x: M, y, w: W - 2 * M, h: 0, line: { color: RULE, width: 1 } });
}

// ---------- 2. Motivation ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "MOTIVATION");
  title(s, "Why formalise the review workflow as a pipeline");
  const probs = [
    ["Labour", "Searching, de-duplication, dual screening, and extraction are repetitive, high-volume tasks in which errors propagate to the pooled estimate."],
    ["Reporting standards", "PRISMA 2020 (27 items; 32 for network meta-analysis), GRADE, and RoB 2 or ROBINS-I each impose their own documentation requirements."],
    ["Reproducibility", "Decisions are typically dispersed across spreadsheets and e-mail. Months later, the reason a study was included or excluded is often unrecoverable."],
  ];
  probs.forEach((p, i) => {
    const y = 1.55 + i * 1.5;
    text(s, p[0], { x: M, y, w: 2.6, h: 0.4, fontSize: 16, bold: true, color: BLUE, fontFace: HEAD });
    text(s, p[1], { x: 3.4, y, w: 4.6, h: 1.35, fontSize: 13, color: INK });
  });
  box(s, 8.5, 1.55, 4.15, 3.95, TINT);
  text(s, "Design response", { x: 8.8, y: 1.75, w: 3.6, h: 0.4, fontSize: 16, bold: true, color: INK, fontFace: HEAD });
  bullets(s, [
    "Each stage writes a fixed set of artefacts to a numbered directory.",
    "Each stage is specified in a version-controlled skill file that the agent executes.",
    "Transitions between stages are conditional on quantitative quality gates.",
    "Every search and screening round is retained; nothing is overwritten.",
  ], { x: 8.8, y: 2.3, w: 3.6, h: 3.5, fontSize: 12.5 });
  footer(s, n);
  s.addNotes("Three recurring problems in systematic reviews, and the corresponding design decisions. The pipeline does not change the methodology; it enforces its documentation.");
}

// ---------- 3. Design principles ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "ARCHITECTURE");
  title(s, "Design principles");
  const items = [
    ["Stage-wise artefacts", "Eleven numbered stages (00–10). Each has defined inputs, outputs, and a completion checklist in 09_qa/pipeline-checklist.md."],
    ["Executable protocols", "Each stage is described in a SKILL.md file: commands, validation criteria, expected outputs. The agent follows the file rather than improvising."],
    ["Quality gates", "Inter-rater agreement, figure resolution, checklist completion, and a readiness score must reach preset thresholds before the next stage begins."],
    ["Reproducible tool chain", "Python via uv, R via renv (renv.lock), manuscripts via Quarto. Artefacts are hashed (SHA-256) and checkpointed before major steps."],
  ];
  const cw = (W - 2 * M - 0.4) / 2;
  const ch = 2.25;
  items.forEach((it, i) => {
    const x = M + (i % 2) * (cw + 0.4);
    const y = 1.55 + Math.floor(i / 2) * (ch + 0.3);
    box(s, x, y, cw, ch, TINT);
    text(s, it[0], { x: x + 0.3, y: y + 0.25, w: cw - 0.6, h: 0.4, fontSize: 17, bold: true, color: BLUE, fontFace: HEAD });
    text(s, it[1], { x: x + 0.3, y: y + 0.75, w: cw - 0.6, h: ch - 0.9, fontSize: 13, color: INK });
  });
  footer(s, n);
  s.addNotes("Four principles. The second is the distinctive one: the behaviour of the agent is specified in files that are reviewed and versioned like code.");
}

// ---------- 4. Pipeline overview ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "PIPELINE");
  title(s, "Stages and principal artefacts");
  const phases = [
    ["Foundation", "sequential", [0, 1, 2]],
    ["Screening", "dual review", [3, 4]],
    ["Processing", "sequential", [5, 6]],
    ["Synthesis", "manuscript and QA", [7, 8, 9, 10]],
  ];
  const gapX = 0.4;
  const cw = (W - 2 * M - 3 * gapX) / 4;
  phases.forEach((p, i) => {
    const x = M + i * (cw + gapX);
    box(s, x, 1.5, cw, 4.9, TINT);
    text(s, p[0], { x: x + 0.25, y: 1.65, w: cw - 0.5, h: 0.35, fontSize: 15, bold: true, color: INK, fontFace: HEAD });
    text(s, p[1], { x: x + 0.25, y: 2.0, w: cw - 0.5, h: 0.3, fontSize: 10.5, color: MUTED, italic: true });
    p[2].forEach((si, j) => {
      const st = STAGES[si];
      const y = 2.5 + j * 0.95;
      tag(s, x + 0.25, y, st[0], 0.5);
      text(s, st[1], { x: x + 0.9, y: y - 0.02, w: cw - 1.1, h: 0.32, fontSize: 13, bold: true, color: INK });
      text(s, st[2], { x: x + 0.9, y: y + 0.3, w: cw - 1.1, h: 0.5, fontSize: 9.5, color: MUTED, fontFace: MONO });
    });
    if (i < 3) arrow(s, x + cw + 0.07, 3.8, gapX - 0.14);
  });
  note(s, "Project layout: projects/<name>/01_protocol … 09_qa. Project directories are excluded from version control except the reference example.", 6.55);
  footer(s, n);
  s.addNotes("Read left to right. Stage 03 is the only stage designed for two independent reviewers; stages 07–09 can proceed in parallel once analysis is complete.");
}

// ---------- 5. Stages 00-02 ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "STAGES 00–02");
  title(s, "Topic intake, protocol, and search");
  const rows = [
    ["00", "Topic intake and feasibility", "A structured feasibility assessment (bounded at four hours) precedes any protocol work: expected number of eligible studies, consistency of outcome definitions, and availability of extractable data. Output: FEASIBILITY_REPORT.md."],
    ["01", "Protocol", "PICO recorded in pico.yaml; eligibility criteria, outcomes, and search plan as Markdown. A preliminary analysis type is assigned: two interventions → pairwise; three or more → NMA candidate, pending confirmation after screening."],
    ["02", "Search", "PubMed and Scopus are the minimum (PRISMA requires at least two databases); Embase and Cochrane are optional. Each round is stored under 02_search/round-XX/ with queries.txt, results.bib, dedupe.bib, and log.md."],
  ];
  rows.forEach((r, i) => {
    const y = 1.6 + i * 1.7;
    tag(s, M, y + 0.03, r[0]);
    text(s, r[1], { x: M + 0.75, y, w: 5, h: 0.4, fontSize: 16, bold: true, color: INK, fontFace: HEAD });
    text(s, r[2], { x: M + 0.75, y: y + 0.45, w: 11.2, h: 1.1, fontSize: 12.5, color: INK });
  });
  footer(s, n);
  s.addNotes("The feasibility gate is deliberately early and time-boxed. The analysis type is provisional at this point; it is confirmed at stage 03b once the design mix of included studies is known.");
}

// ---------- 6. Stages 03-04 ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "STAGES 03–04");
  title(s, "Screening, analysis-type confirmation, and full text");
  // diagram
  const by = 1.65;
  box(s, M, by, 2.0, 0.7, TINT);
  text(s, "Reviewer 1", { x: M, y: by, w: 2.0, h: 0.7, fontSize: 13, align: "center", valign: "middle", color: INK });
  box(s, M, by + 1.0, 2.0, 0.7, TINT);
  text(s, "Reviewer 2", { x: M, y: by + 1.0, w: 2.0, h: 0.7, fontSize: 13, align: "center", valign: "middle", color: INK });
  arrow(s, M + 2.15, by + 0.22, 0.5);
  arrow(s, M + 2.15, by + 1.22, 0.5);
  box(s, M + 2.8, by + 0.3, 1.9, 1.1, WHITE, BLUE);
  text(s, "Cohen's κ ≥ 0.60", { x: M + 2.8, y: by + 0.35, w: 1.9, h: 0.5, fontSize: 13, bold: true, align: "center", valign: "middle", color: BLUE });
  text(s, "quality gate", { x: M + 2.8, y: by + 0.85, w: 1.9, h: 0.4, fontSize: 10.5, align: "center", color: MUTED, italic: true });
  arrow(s, M + 4.85, by + 0.72, 0.5);
  box(s, M + 5.5, by + 0.3, 1.7, 1.1, TINT);
  text(s, "Conflict resolution\nincluded.bib", { x: M + 5.5, y: by + 0.3, w: 1.7, h: 1.1, fontSize: 12, align: "center", valign: "middle", color: INK });
  bullets(s, [
    "Two independent screening passes (ai_screen.py, reviewer 1 and 2); decisions and rationale recorded in decisions.csv.",
    "Agreement computed with dual_review_agreement.py; the same gate applies to full-text eligibility (stage 04b, PRISMA 2020 item 16).",
    "Full texts retrieved via Unpaywall and indexed in manifest.csv; only FT_Final_Decision = include proceeds to extraction.",
  ], { x: M, y: 4.05, w: 7.3, h: 2.4, fontSize: 12.5 });
  // gate card
  box(s, 8.6, 1.55, 4.05, 4.1, TINT);
  text(s, "Stage 03b — analysis-type confirmation", { x: 8.85, y: 1.75, w: 3.6, h: 0.6, fontSize: 15, bold: true, color: INK, fontFace: HEAD });
  bullets(s, [
    "Tabulate study designs among included records.",
    "Assess network connectivity and transitivity.",
    "If more than 30% of studies are single-arm, downgrade from NMA to pairwise analysis with pooled proportions.",
    "Record the decision in analysis-type-decision.md and pico.yaml.",
    "Stage 06 cannot start until analysis_type.confirmed is set.",
  ], { x: 8.85, y: 2.45, w: 3.6, h: 3.1, fontSize: 12 });
  footer(s, n);
  s.addNotes("Two independent passes are required by design. The 03b gate is where the NMA versus pairwise decision is made explicit and documented, rather than left implicit in the analysis script.");
}

// ---------- 7. Stage 05 ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "STAGE 05");
  title(s, "Data extraction with investigator verification");
  const steps = [
    ["1", "Text extraction", "extract_pdf_text.py"],
    ["2", "Structured extraction", "llm_extract_cli.py"],
    ["3", "Investigator verification", "edit extraction.csv"],
    ["4", "Validation", "validate_extraction.py"],
  ];
  const gapX = 0.45;
  const cw = (W - 2 * M - 3 * gapX) / 4;
  steps.forEach((st, i) => {
    const x = M + i * (cw + gapX);
    box(s, x, 1.55, cw, 1.85, i === 2 ? WHITE : TINT, i === 2 ? BLUE : TINT);
    text(s, st[0], { x: x + 0.25, y: 1.75, w: 0.5, h: 0.35, fontSize: 12, bold: true, color: BLUE, fontFace: MONO });
    text(s, st[1], { x: x + 0.25, y: 2.15, w: cw - 0.5, h: 0.65, fontSize: 14, bold: true, color: INK, fontFace: HEAD });
    text(s, st[2], { x: x + 0.25, y: 2.9, w: cw - 0.5, h: 0.4, fontSize: 10.5, color: MUTED, fontFace: MONO });
    if (i < 3) arrow(s, x + cw + 0.09, 2.35, gapX - 0.18);
  });
  bullets(s, [
    "Input is restricted to studies with FT_Final_Decision = include.",
    "Extraction schema is defined in advance (create_extraction_template.py) and documented in data-dictionary.md; a normalised copy is stored as extraction.sqlite.",
    "Fields with low model confidence are flagged (flag_low_confidence.py) for targeted review.",
    "Risk of bias is assessed in the same stage: RoB 2 for randomised trials, ROBINS-I for non-randomised studies.",
  ], { x: M, y: 3.75, w: 7.6, h: 2.8, fontSize: 12.5 });
  box(s, 8.8, 3.75, 3.85, 2.55, TINT);
  text(s, "Observed in the example project", { x: 9.05, y: 3.9, w: 3.4, h: 0.35, fontSize: 12, bold: true, color: INK });
  bullets(s, [
    "All included PDFs were processed.",
    "Some fields required manual correction.",
    "Extraction time approximately 2–3 h versus an estimated 4–6 h manually.",
    "Model cost under US$5 per review.",
  ], { x: 9.05, y: 4.3, w: 3.4, h: 1.9, fontSize: 11.5 });
  footer(s, n);
  s.addNotes("Step 3 is not optional. The model produces a first pass; the investigator verifies every extracted value against the source. Figures in the right-hand box are from one project's log and should not be generalised.");
}

// ---------- 8. Stage 06 ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "STAGE 06");
  title(s, "Analysis: routed by confirmed analysis type");
  box(s, M, 1.75, 2.8, 1.2, WHITE, BLUE);
  text(s, "analysis_type\n.confirmed", { x: M, y: 1.75, w: 2.8, h: 1.2, fontSize: 13, bold: true, color: BLUE, align: "center", valign: "middle", fontFace: MONO });
  const branches = [
    ["pairwise", "Pairwise meta-analysis", "R scripts 01–12: pooled estimates, forest and funnel plots, heterogeneity, sensitivity and subgroup analyses, meta-regression."],
    ["nma", "Network meta-analysis", "nma_01–10: Bayesian NMA, ranking, inconsistency. Extensions: nma_11 component NMA, nma_12 meta-regression, nma_13 transitivity tests."],
    ["pooled_proportion", "Pooled proportion", "Single-arm or proportion data; used when the NMA candidate is downgraded at stage 03b."],
    ["narrative", "Narrative synthesis", "Structured synthesis without pooling when quantitative combination is not appropriate."],
  ];
  const bx = 4.9, bw = W - M - 4.9, bh = 1.02;
  branches.forEach((b, i) => {
    const y = 1.5 + i * (bh + 0.18);
    s.addShape(pres.ShapeType.line, { x: M + 2.8, y: Math.min(2.35, y + bh / 2), w: bx - 0.1 - (M + 2.8), h: Math.abs(y + bh / 2 - 2.35), line: { color: RULE, width: 1 }, flipV: y + bh / 2 < 2.35 });
    box(s, bx, y, bw, bh, TINT);
    text(s, b[0], { x: bx + 0.25, y: y + 0.12, w: 2.5, h: 0.28, fontSize: 10.5, color: BLUE, fontFace: MONO, bold: true });
    text(s, b[1], { x: bx + 0.25, y: y + 0.42, w: 2.7, h: 0.5, fontSize: 13.5, bold: true, color: INK, fontFace: HEAD });
    text(s, b[2], { x: bx + 3.0, y: y + 0.12, w: bw - 3.25, h: bh - 0.24, fontSize: 11.5, color: INK, valign: "middle" });
  });
  bullets(s, [
    "R with renv; package versions recorded in renv.lock.",
    "Figures exported at 300 dpi or higher; multi-panel figures assembled with assemble_figures.py.",
    "Outputs in figures/ and tables/ are referenced directly by the manuscript.",
  ], { x: M, y: 3.35, w: 3.9, h: 3.0, fontSize: 12 });
  footer(s, n);
  s.addNotes("The routing is data-driven: the value written at stage 03b selects the script set. The NMA path includes a statistical transitivity check in addition to the qualitative assessment at 03b.");
}

// ---------- 9. Stages 07-10 ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "STAGES 07–10");
  title(s, "Manuscript, appraisal, quality assurance, submission");
  const cards = [
    ["07", "Manuscript", ["A manuscript outline is drafted and approved by the investigator before any section is written.", "Sections, tables, and figures assembled in Quarto; rendered to HTML and PDF.", "Citations managed as BibTeX from the outset."]],
    ["08", "Appraisal", ["GRADE certainty assessment per outcome.", "Summary of Findings table.", "Consolidated RoB 2 / ROBINS-I assessments."]],
    ["09", "Quality assurance", ["PRISMA 2020 checklist (27 or 32 items) and cross-reference audit.", "Automated claim audit against twelve over-statement patterns.", "Publication readiness score (0–100%) across eight components."]],
    ["10", "Submission", ["PROSPERO registration document.", "Journal-specific formatting (word limits, table and figure counts).", "Final consistency checks before the package is assembled."]],
  ];
  const gapX = 0.3;
  const cw = (W - 2 * M - 3 * gapX) / 4;
  cards.forEach((c, i) => {
    const x = M + i * (cw + gapX);
    box(s, x, 1.55, cw, 3.7, TINT);
    tag(s, x + 0.25, 1.8, c[0], 0.5);
    text(s, c[1], { x: x + 0.9, y: 1.78, w: cw - 1.1, h: 0.4, fontSize: 15, bold: true, color: INK, fontFace: HEAD, valign: "middle" });
    bullets(s, c[2], { x: x + 0.25, y: 2.5, w: cw - 0.5, h: 2.6, fontSize: 11.5 });
  });
  footer(s, n);
  s.addNotes("Two controls are worth noting: outline approval before drafting at stage 07, and the claim audit at stage 09, which flags language stronger than the evidence supports.");
}

// ---------- 10. Quality gates ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "QUALITY GATES");
  title(s, "Stage transitions are conditional on preset thresholds");
  const hdr = { bold: true, color: WHITE, fill: { color: BLUE }, fontFace: BODY, fontSize: 12.5, valign: "middle" };
  const cell = (t, o) => ({ text: t, options: Object.assign({ fontFace: BODY, fontSize: 12, color: INK, valign: "middle" }, o || {}) });
  const rows = [
    [{ text: "Transition", options: hdr }, { text: "Criterion", options: hdr }, { text: "Threshold", options: hdr }, { text: "Instrument", options: hdr }],
    [cell("00 → 01"), cell("Feasibility assessment completed"), cell("FEASIBILITY_REPORT.md present"), cell("feasibility checklist", { fontFace: MONO, fontSize: 10.5 })],
    [cell("03 → 04"), cell("Title/abstract screening agreement"), cell("Cohen's κ ≥ 0.60"), cell("dual_review_agreement.py", { fontFace: MONO, fontSize: 10.5 })],
    [cell("03b → 06"), cell("Analysis type confirmed"), cell("analysis_type.confirmed set"), cell("analysis-type-decision.md", { fontFace: MONO, fontSize: 10.5 })],
    [cell("04 → 05"), cell("Full-text screening agreement"), cell("Cohen's κ ≥ 0.60"), cell("dual_review_agreement.py", { fontFace: MONO, fontSize: 10.5 })],
    [cell("05 → 06"), cell("Extraction completeness"), cell("All included studies extracted and validated"), cell("validate_extraction.py", { fontFace: MONO, fontSize: 10.5 })],
    [cell("06 → 07"), cell("Figure resolution"), cell("≥ 300 dpi"), cell("validate_stage_transition.py", { fontFace: MONO, fontSize: 10.5 })],
    [cell("07 → 08"), cell("Manuscript outline approved"), cell("Investigator sign-off"), cell("manuscript_outline.md", { fontFace: MONO, fontSize: 10.5 })],
    [cell("09"), cell("Reporting and readiness"), cell("PRISMA 27/27 (NMA 32/32); readiness ≥ 95%"), cell("publication_readiness_score.py", { fontFace: MONO, fontSize: 10.5 })],
  ];
  s.addTable(rows, { x: M, y: 1.5, w: W - 2 * M, colW: [1.5, 3.4, 3.9, 3.13], rowH: 0.48, border: { type: "solid", color: RULE, pt: 0.75 }, fill: { color: WHITE }, margin: 0.07 });
  note(s, "Gates are evaluated by validate_stage_transition.py, which writes 09_qa/stage_transition_report.md. In parallel (agent-team) mode the same checks run as hooks at each hand-off.", 6.2);
  footer(s, n);
  s.addNotes("The thresholds are conventional (kappa 0.60 as substantial agreement; 300 dpi as a common journal minimum). The point is that they are checked mechanically and recorded.");
}

// ---------- 11. Validation ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "VALIDATION");
  title(s, "Benchmark against published meta-analyses");
  const steps = [
    ["Import", "Datasets from the CRAN package metadat (over 500 published meta-analyses) are converted to the pipeline's extraction.csv schema.", "import_metadat.py"],
    ["Analyse", "The standard stage 06 scripts are run unchanged on the imported data, producing summary estimates, forest plots, and heterogeneity statistics.", "06_analysis/*.R"],
    ["Compare", "Pooled estimates and confidence intervals are compared with the values reported in the source publication; discrepancies are reported per dataset.", "validate_pipeline.py"],
  ];
  const gapX = 0.4;
  const cw = (W - 2 * M - 2 * gapX) / 3;
  steps.forEach((st, i) => {
    const x = M + i * (cw + gapX);
    box(s, x, 1.55, cw, 2.9, TINT);
    text(s, st[0], { x: x + 0.3, y: 1.75, w: cw - 0.6, h: 0.4, fontSize: 17, bold: true, color: BLUE, fontFace: HEAD });
    text(s, st[1], { x: x + 0.3, y: 2.25, w: cw - 0.6, h: 1.6, fontSize: 12.5, color: INK });
    text(s, st[2], { x: x + 0.3, y: 3.95, w: cw - 0.6, h: 0.35, fontSize: 10.5, color: MUTED, fontFace: MONO });
    if (i < 2) arrow(s, x + cw + 0.07, 2.85, gapX - 0.14);
  });
  bullets(s, [
    "Purpose: regression testing of the statistical code path, independent of any single project.",
    "Scope: covers stage 06 (pairwise). Search, screening, and extraction are not exercised by this benchmark, since metadat supplies already-extracted data.",
    "The full suite is run with run_validation_suite.sh; validation projects live under tooling/projects/validation-*/.",
  ], { x: M, y: 4.75, w: W - 2 * M, h: 1.7, fontSize: 12.5 });
  footer(s, n);
  s.addNotes("This benchmark tests whether the analysis scripts reproduce published pooled estimates. It says nothing about screening or extraction accuracy; those are addressed by the dual-review gates and investigator verification.");
}

// ---------- 12. Worked example ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "WORKED EXAMPLE");
  title(s, "Neoadjuvant ICI in triple-negative breast cancer");
  text(s, "Five randomised trials, 2,402 patients. ICI plus chemotherapy versus chemotherapy alone. Random-effects model (Mantel–Haenszel, Hartung–Knapp).", { x: M, y: 1.35, w: W - 2 * M, h: 0.4, fontSize: 12.5, color: MUTED });
  const hdr = { bold: true, color: WHITE, fill: { color: BLUE }, fontFace: BODY, fontSize: 12.5, valign: "middle" };
  const cell = (t, o) => ({ text: t, options: Object.assign({ fontFace: BODY, fontSize: 12.5, color: INK, valign: "middle" }, o || {}) });
  const rows = [
    [{ text: "Outcome", options: hdr }, { text: "Trials", options: hdr }, { text: "Effect (95% CI)", options: hdr }, { text: "I²", options: hdr }, { text: "GRADE", options: hdr }],
    [cell("Pathologic complete response"), cell("5"), cell("RR 1.26 (1.16–1.37)"), cell("0%"), cell("High")],
    [cell("Event-free survival"), cell("3"), cell("HR 0.66 (0.51–0.86)"), cell("0%"), cell("Moderate")],
    [cell("Overall survival"), cell("2"), cell("HR 0.48 (0.00–128.7)"), cell("—"), cell("Low")],
    [cell("Serious adverse events"), cell("5"), cell("RR 1.50 (1.13–1.98)"), cell("—"), cell("—")],
  ];
  s.addTable(rows, { x: M, y: 1.9, w: 7.7, colW: [2.9, 0.8, 2.1, 0.7, 1.2], rowH: 0.5, border: { type: "solid", color: RULE, pt: 0.75 }, fill: { color: WHITE }, margin: 0.07 });
  text(s, "Absolute pCR difference 13.8 percentage points (NNT 7). Egger's test p = 0.71. Sensitivity analyses excluding the phase II trial or the negative trial gave RR 1.26 and 1.28.", { x: M, y: 4.55, w: 7.7, h: 0.8, fontSize: 11.5, color: INK });
  box(s, 8.8, 1.9, 3.85, 3.6, TINT);
  text(s, "Pipeline record", { x: 9.05, y: 2.05, w: 3.4, h: 0.4, fontSize: 14, bold: true, color: INK, fontFace: HEAD });
  bullets(s, [
    "122 records after de-duplication; 5 trials included.",
    "Manuscript of 4,921 words with seven tables, within Lancet Oncology limits.",
    "Approximately 14 hours of investigator time recorded end to end.",
    "Screening in this project used a single AI pass; κ was therefore not computed. Later projects use the dual-review gate.",
  ], { x: 9.05, y: 2.55, w: 3.4, h: 2.9, fontSize: 11.5 });
  note(s, "All artefacts are in projects/ici-breast-cancer/ (00_overview to 09_qa). Overall survival pooled only two trials; the wide interval reflects the Hartung–Knapp adjustment with k = 2.", 6.45);
  footer(s, n);
  s.addNotes("The example is complete and public. Note two caveats: the OS estimate is from two trials only, and screening was single-pass, which the current pipeline would not permit.");
}

// ---------- 13. Time ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "RESOURCE USE");
  title(s, "Investigator time by stage");
  const labels = ["01 Protocol", "02 Search", "03 Screening", "04 Full text", "05 Extraction", "06 Analysis", "07 Manuscript"];
  s.addChart(pres.ChartType.bar, [
    { name: "Lower estimate", labels, values: [1, 2, 3, 2, 4, 4, 6] },
    { name: "Upper estimate", labels, values: [2, 3, 4, 4, 6, 5, 8] },
  ], {
    x: M, y: 1.5, w: 7.7, h: 4.9,
    barDir: "col", barGrouping: "clustered", barGapWidthPct: 70,
    chartColors: ["9FB3C8", BLUE],
    showTitle: false,
    showLegend: true, legendPos: "b", legendFontFace: BODY, legendFontSize: 11, legendColor: MUTED,
    showValue: true, dataLabelPosition: "outEnd", dataLabelFontFace: BODY, dataLabelFontSize: 10, dataLabelColor: INK,
    catAxisLabelFontFace: BODY, catAxisLabelFontSize: 10.5, catAxisLabelColor: INK, catGridLine: { style: "none" },
    valAxisLabelFontFace: BODY, valAxisLabelFontSize: 10, valAxisLabelColor: MUTED, valGridLine: { color: "E3E8ED", size: 0.5 },
    valAxisTitle: "Hours", showValAxisTitle: true, valAxisTitleFontFace: BODY, valAxisTitleFontSize: 10.5, valAxisTitleColor: MUTED,
    valAxisMaxVal: 9, valAxisMinVal: 0, valAxisMajorUnit: 2,
    catAxisLineShow: false, valAxisLineShow: false,
  });
  box(s, 8.8, 1.5, 3.85, 4.9, TINT);
  text(s, "Reading the estimates", { x: 9.05, y: 1.7, w: 3.4, h: 0.4, fontSize: 14, bold: true, color: INK, fontFace: HEAD });
  bullets(s, [
    "Total 22–32 hours end to end, from the project log of one completed review.",
    "Stage 05 assumes LLM-assisted extraction with verification; manual extraction was estimated at 4–6 hours.",
    "Stage 07 is the largest component; the outline-approval step exists to limit rewriting.",
    "Estimates exclude stages 08–10 and will vary with the number of included studies.",
  ], { x: 9.05, y: 2.2, w: 3.4, h: 4.0, fontSize: 11.5 });
  footer(s, n);
  s.addNotes("These are single-project estimates recorded in the repository's time guidance, not a measured distribution. Treat them as indicative.");
}

// ---------- 14. Human oversight ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "HUMAN OVERSIGHT");
  title(s, "Division of responsibility");
  const cw = (W - 2 * M - 0.4) / 2;
  box(s, M, 1.55, cw, 3.95, TINT);
  text(s, "Automated (agent, under skill files)", { x: M + 0.3, y: 1.75, w: cw - 0.6, h: 0.45, fontSize: 15, bold: true, color: INK, fontFace: HEAD });
  bullets(s, [
    "Search strategy drafting, query execution, de-duplication",
    "Independent screening passes and agreement statistics",
    "PDF retrieval, text extraction, first-pass structured extraction",
    "R script generation, figure and table production",
    "Manuscript scaffolding, reference management, checklist completion",
    "Claim audit, cross-reference checks, readiness scoring",
    "Session logging, checkpoints, artefact hashing",
  ], { x: M + 0.3, y: 2.35, w: cw - 0.6, h: 3.7, fontSize: 12.5 });
  box(s, M + cw + 0.4, 1.55, cw, 3.95, WHITE, BLUE);
  text(s, "Investigator", { x: M + cw + 0.7, y: 1.75, w: cw - 0.6, h: 0.45, fontSize: 15, bold: true, color: BLUE, fontFace: HEAD });
  bullets(s, [
    "Research question, PICO, and eligibility criteria",
    "Feasibility decision and final analysis-type decision",
    "Adjudication of screening conflicts",
    "Verification of every extracted value against the source",
    "Risk-of-bias and GRADE judgements",
    "Clinical interpretation and discussion",
    "Approval at each gate; authorship and disclosure statements",
  ], { x: M + cw + 0.7, y: 2.35, w: cw - 0.6, h: 3.7, fontSize: 12.5 });
  footer(s, n);
  s.addNotes("The agent produces drafts and structure. Every methodological judgement and every gate approval is made by the investigator and is recorded in the decision log.");
}

// ---------- 15. Limitations ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "LIMITATIONS");
  title(s, "Limitations and current work");
  const cw = (W - 2 * M - 0.4) / 2;
  text(s, "Limitations", { x: M, y: 1.55, w: cw, h: 0.4, fontSize: 16, bold: true, color: BLUE, fontFace: HEAD });
  bullets(s, [
    "Time and cost figures derive from one completed project; no controlled comparison with a conventional workflow has been performed.",
    "LLM extraction produced errors that required manual correction; the error rate has not been quantified systematically.",
    "The example project used single-pass AI screening, so its screening agreement is unknown.",
    "The metadat benchmark validates the analysis code only, not search, screening, or extraction.",
    "Two AI reviewers share a model family; their agreement is not equivalent to agreement between two human reviewers.",
  ], { x: M, y: 2.05, w: cw, h: 4.2, fontSize: 12.5 });
  text(s, "Current work", { x: M + cw + 0.4, y: 1.55, w: cw, h: 0.4, fontSize: 16, bold: true, color: BLUE, fontFace: HEAD });
  bullets(s, [
    "Parallel execution with role-specific agents (screening and synthesis stages), with hooks enforcing the same gates; experimental.",
    "Extending the validation suite beyond stage 06.",
    "Prospective comparison of AI-assisted and human dual screening on the same record set.",
    "NMA extensions: component NMA, meta-regression, and statistical transitivity tests are implemented and await validation.",
  ], { x: M + cw + 0.4, y: 2.05, w: cw, h: 4.2, fontSize: 12.5 });
  footer(s, n);
  s.addNotes("State these plainly. The strongest claim the current evidence supports is that the pipeline enforces documentation and reproducibility; efficiency claims rest on one project.");
}

// ---------- 16. Availability ----------
{
  const s = pres.addSlide(); n++;
  s.background = { color: WHITE };
  section(s, "AVAILABILITY");
  title(s, "Software, requirements, and citation");
  text(s, "Running a new project", { x: M, y: 1.55, w: 6, h: 0.4, fontSize: 15, bold: true, color: INK, fontFace: HEAD });
  const cmds = [
    ["1", "uv run tooling/python/init_project.py --name <project>", "Creates the numbered directory tree and TOPIC.txt"],
    ["2", "projects/<project>/TOPIC.txt", "Record population, intervention, comparator, outcomes"],
    ["3", "\"Start project <project>\"  (in Claude Code)", "Runs the feasibility assessment, then stages 01 onward"],
  ];
  cmds.forEach((c, i) => {
    const y = 2.05 + i * 1.05;
    text(s, c[0], { x: M, y: y + 0.05, w: 0.4, h: 0.4, fontSize: 13, bold: true, color: BLUE, fontFace: MONO });
    box(s, M + 0.45, y, 6.6, 0.55, TINT);
    text(s, c[1], { x: M + 0.65, y, w: 6.3, h: 0.55, fontSize: 11.5, color: INK, fontFace: MONO, valign: "middle" });
    text(s, c[2], { x: M + 0.45, y: y + 0.58, w: 6.6, h: 0.35, fontSize: 11, color: MUTED });
  });
  box(s, 8.4, 1.55, 4.25, 4.75, TINT);
  text(s, "Requirements", { x: 8.65, y: 1.7, w: 3.8, h: 0.4, fontSize: 14, bold: true, color: INK, fontFace: HEAD });
  bullets(s, [
    "Python ≥ 3.12 via uv",
    "R ≥ 4.2 with renv",
    "Quarto",
    "Database API keys in .env (PubMed, Scopus; Unpaywall for full text)",
  ], { x: 8.65, y: 2.15, w: 3.8, h: 1.7, fontSize: 12 });
  text(s, "Licence", { x: 8.65, y: 3.95, w: 3.8, h: 0.35, fontSize: 14, bold: true, color: INK, fontFace: HEAD });
  text(s, "Academic and non-commercial use.", { x: 8.65, y: 4.3, w: 3.8, h: 0.35, fontSize: 12, color: INK });
  text(s, "Citation", { x: 8.65, y: 4.8, w: 3.8, h: 0.35, fontSize: 14, bold: true, color: INK, fontFace: HEAD });
  text(s, "Lin HT, Yeh JT. meta-pipe: AI-assisted, end-to-end meta-analysis pipeline with reproducible tooling. 2026. https://github.com/htlin222/meta-pipe", { x: 8.65, y: 5.15, w: 3.8, h: 1.0, fontSize: 10.5, color: INK });
  s.addShape(pres.ShapeType.line, { x: M, y: 5.45, w: 7.05, h: 0, line: { color: RULE, width: 1 } });
  text(s, "Example project with all intermediate artefacts: projects/ici-breast-cancer/", { x: M, y: 5.6, w: 7.05, h: 0.4, fontSize: 11.5, color: MUTED });
  footer(s, n);
  s.addNotes("Everything shown is in the repository, including the example project with all intermediate artefacts.");
}

pres.writeFile({ fileName: "meta-pipe-workflow.pptx" }).then(f => console.log("wrote", f));
