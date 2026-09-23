Stage 06b — the presentation figure set. The journal figures already exist; this step builds the versions that go on a screen in front of a room, which is a different design problem: read at four metres, one idea per slide, no dependence on a caption the audience cannot see.

Load the `dataviz` skill before writing any plotting code, and follow it.

Build these into `06_analysis/figures/presentation/`, at ≥300 DPI, 16:9, with a consistent palette and type scale across the whole set:

1. **Network geometry** — nodes sized by patients, edges weighted by trials, the trastuzumab + chemotherapy anchor visually obvious. Label nodes with regimen names, not abbreviations the audience has to decode.
2. **League table heatmap** — colour by effect size, annotate each cell with the estimate and interval. **Inherit the orientation Stage 06 asserted; do not re-derive it here.** State it in the title itself ("row versus column") rather than the caption. A mis-read league table is the classic way this figure misleads, and it is undetectable by eye because every cell is still a plausible risk ratio — on synthetic data the raw `netleague()` cell for a treatment that was decisively better read 0.29 instead of 3.48.
3. **Forest plot, pCR** — every regimen against trastuzumab + chemotherapy, ordered by effect, reference line drawn, number of trials per comparison shown alongside.
4. **SUCRA / rankogram** — with the caveat rendered _in the figure_, not only in the caption: mark the nodes whose rank rests on one or two trials.
5. **Effect against evidence strength** — pCR effect on one axis, the evidence behind it on the other (number of trials, or patients, or credible-interval width), point size by sample size. The trade-off plot this slot was meant to hold needed cardiac and grade ≥3 toxicity, and this run's abstract-only sourcing left those at ~10% coverage, so it cannot honestly be drawn. This replacement answers the question that is still answerable: which of these rankings are actually supported, and which rest on one trial. Mark the single-trial nodes so the audience sees them without being told.
6. **PRISMA-NMA flow** — clean enough to project.
7. **A single summary slide figure** — the one image that carries the study's answer if only one figure survives the talk.

Then assemble a contact sheet of the full set with `uv run tooling/python/assemble_figures.py` (or an equivalent) so the set can be reviewed at a glance.

**Use a device that actually records the resolution.** R's `png(..., res = 300)` on this machine writes the right number of pixels and no `pHYs` chunk at all, so the file declares no resolution and every reader — including a journal's checker — sees 72 dpi. Three devices were tested and write it correctly: `ragg::agg_png(..., res = 300)`, `png(..., res = 300, type = "cairo")`, and `ggsave(..., dpi = 300)`. Use one of those for every figure in this set and in `06_analysis/figures/`.

Then **verify it by reading the `pHYs` chunk**, not by trusting the call and not by file size. The repo's own readiness check uses "larger than 100 KB" as a DPI proxy, and that proxy points the wrong way: in the test, the 98 KB file was the one with no resolution and the 30 KB file was a true 300 dpi. Write the verification into a small script under `06_analysis/` so the check is reproducible, and report the measured dpi per file.

**Layout defects a previous run shipped, so check for these specifically.** Each was only visible once the file was opened:
- value labels drawn at a bar's end collide with anything annotated inside the bar, and short bars have no room for an inside label at all — put the value in its own right-hand gutter, consistently for every row
- a right-hand annotation built from two layers at colliding x positions renders as `1.50▲ 2 trials` with no space. Give value and annotation separate columns with a visible gutter
- a credible interval that reaches the panel edge is unreadable: the reader cannot tell whether it ended there or was clipped. Widen the axis so every interval terminates inside, or clip explicitly with an arrowhead and say so
- overlapping point labels in a scatter need `ggrepel` with `min.segment.length = 0` so leader lines are drawn; band labels belong at the band's edge, not among the points
- a node label centred on its node sits under the edges radiating from it — offset it or give it a halo
- keep a statistic on one line: `τ = 0.27` must not break across a wrap

Requirements that apply to all of them: legible at 4 m, colour-blind safe, no red/green as the only distinction, units and n on the axes, and every figure readable without its caption.

Finish with: the file list, the DPI you verified, the palette rationale, and which single figure you would put on the summary slide.
