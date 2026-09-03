# meta-pipe workflow presentation

`meta-pipe-workflow.pptx` — 16 slides (English, 16:9) describing the pipeline for an academic audience. Speaker notes are included on every slide.

| # | Slide |
|---|-------|
| 1 | Title |
| 2 | Motivation: labour, reporting standards, reproducibility |
| 3 | Design principles |
| 4 | Stages 00–10 and principal artefacts |
| 5 | Stages 00–02: topic intake, protocol, search |
| 6 | Stages 03–04: dual screening, analysis-type confirmation, full text |
| 7 | Stage 05: extraction with investigator verification |
| 8 | Stage 06: analysis routed by confirmed analysis type |
| 9 | Stages 07–10: manuscript, appraisal, QA, submission |
| 10 | Quality gates (table) |
| 11 | Validation against metadat benchmark datasets |
| 12 | Worked example: neoadjuvant ICI in TNBC |
| 13 | Investigator time by stage (chart) |
| 14 | Division of responsibility |
| 15 | Limitations and current work |
| 16 | Availability, requirements, citation |

All figures are taken from the repository documentation and the example project log. Single-project estimates are labelled as such on the slides.

## Rebuild

```bash
cd docs/presentation
npm install pptxgenjs
node build_deck.js   # writes meta-pipe-workflow.pptx
```

Fonts: Cambria (headings), Calibri (body), Courier New (file names and commands).
