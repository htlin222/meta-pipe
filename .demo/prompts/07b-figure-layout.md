Stage 07b — fix the layout defects in the presentation figure set. The statistics are right and the DPI is right; the typography collides. These are slides meant to be read at four metres, and right now several of them cannot be read at arm's length.

Work in `06_analysis/figures/presentation/` via the `pres_*.R` scripts. Do not recompute the model — reuse `nma_models.rds` / the existing tables. Re-render at the same 16:9 geometry and the same verified 300 dpi, and re-run `verify_png_dpi.py` at the end.

Each of these is a specific observed defect, not a style preference:

**04_sucra_ranking.png — value labels sit on top of the bars.** `0.43`, `0.36`, `0.59`, `0.15` and `0.02` are drawn at the bar ends and collide with the in-bar annotations (`3 trials · 241 pts`, `▲ 2 trials only — rank unstable`). Either move the SUCRA value outside the bar to its right with a clear gap, or move the trial-count annotation out of the bar — not both inside. The short bars at the bottom (`0.15`, `0.02`) have no room for an inside label at all, so the value must go outside for every row, consistently.

**05_effect_vs_evidence.png — the left cluster is unreadable.** `Anti-HER2 + immunotherapy · 1 trial · RR 1.94`, `T-DXd-based · 1 trial · RR 1.93` and `Neratinib + trastuzumab + chemo · 2 trials · RR 1.50` overlap each other and the `thin evidence` band label. Use `ggrepel::geom_text_repel` with enough force and `min.segment.length = 0` so leader lines are drawn, or place labels for the amber points on alternating sides. Move the `thin evidence` band label out of the point region entirely — put it at the top or bottom edge of the band.

**03_forest_pcr.png and 07_summary_slide.png — the marker is glued to the number.** `1.50▲ 2 trials` and `0.53▲ 2 trials` render with no space, because the value and the annotation are drawn as separate layers at colliding x positions. Give the right-hand annotation column a fixed x with its own gutter: value right-aligned in one column, `▲` and the trial count left-aligned in the next, with visible space between.

**07_summary_slide.png — two credible intervals run off the panel.** The amber bars for `Anti-HER2 + immunotherapy` and `T-DXd-based` extend past the right edge into the annotation area. Widen the x range so every interval terminates inside the panel, or, if that squashes the rest, clip them explicitly with an arrowhead at the panel edge and say in the caption that the interval continues. Do not let a bar silently touch the border — the reader cannot tell whether it ended there or was cut.

**01_network_geometry.png — the anchor label sits under the node.** `Trastuzumab + chemo / 14 trials · 1,380 pts` overlaps the anchor circle and the edges radiating from it. Offset the anchor's label clear of the node, or draw it with a halo/background so it reads over the edges.

Also check the footnote wrapping while you are there: on the summary slide `τ = 0.27` breaks across two lines mid-expression. Keep a statistic on one line.

Finally, rebuild `00_contact_sheet.png` from the corrected figures.

Write `06_analysis/figures/presentation/LAYOUT_FIXES.md` recording, per figure, the defect and what you changed — that file is how this step is checked, so write it once the figures are actually re-rendered.

Finish with: which defect you fixed in which script, the measured dpi per file, and any figure you judge still too crowded at 4 m.
