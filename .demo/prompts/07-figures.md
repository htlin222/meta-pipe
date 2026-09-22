Stage 06b — the presentation figure set. The journal figures already exist; this step builds the versions that go on a screen in front of a room, which is a different design problem: read at four metres, one idea per slide, no dependence on a caption the audience cannot see.

Load the `dataviz` skill before writing any plotting code, and follow it.

Build these into `06_analysis/figures/presentation/`, at ≥300 DPI, 16:9, with a consistent palette and type scale across the whole set:

1. **Network geometry** — nodes sized by patients, edges weighted by trials, the trastuzumab + chemotherapy anchor visually obvious. Label nodes with regimen names, not abbreviations the audience has to decode.
2. **League table heatmap** — colour by effect size, annotate each cell with the estimate and interval. Orientation stated in the title itself ("row versus column"), because a mis-read league table is the classic way this figure misleads.
3. **Forest plot, pCR** — every regimen against trastuzumab + chemotherapy, ordered by effect, reference line drawn, number of trials per comparison shown alongside.
4. **SUCRA / rankogram** — with the caveat rendered *in the figure*, not only in the caption: mark the nodes whose rank rests on one or two trials.
5. **Efficacy-versus-toxicity trade-off** — pCR effect on one axis, cardiac or grade ≥3 toxicity on the other, point size by evidence volume. This is the figure a clinician actually acts on, and it is the one most decks omit.
6. **PRISMA-NMA flow** — clean enough to project.
7. **A single summary slide figure** — the one image that carries the study's answer if only one figure survives the talk.

Then assemble a contact sheet of the full set with `uv run tooling/python/assemble_figures.py` (or an equivalent) so the set can be reviewed at a glance.

Requirements that apply to all of them: legible at 4 m, colour-blind safe, no red/green as the only distinction, units and n on the axes, and every figure readable without its caption. Verify the DPI of each output file rather than assuming the device honoured the setting.

Finish with: the file list, the DPI you verified, the palette rationale, and which single figure you would put on the summary slide.
