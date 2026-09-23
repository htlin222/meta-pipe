# Shakedown repairs

These are the mid-run repair steps from the first end-to-end run. They exist
because the gaps they close were discovered while the pipeline was already
moving, not because a clean run needs them.

| step | what it repaired | now folded into |
|---|---|---|
| `02b-search-round02.md` | Scopus credentials arrived mid-run | `02-search.md` verifies credentials up front |
| `02c-terms-round03.md` | missing agent names, and a corpus with no abstracts | `02-search.md` carries the full agent list and enriches abstracts before screening ends |
| `07b-figure-layout.md` | value labels, clipped intervals, overlapping point labels | `07-figures.md` lists each defect to check for |
| `08b-attrition-discussion.md` | eligible-but-not-networked studies were one box in PRISMA | `08-manuscript.md` requires the breakdown and the reports-versus-trials distinction |

`steps.conf` here is the step table as the shakedown actually ran it, kept so the
sequence that produced `projects/neo-her2-ebc/` stays reconstructible.

A clean run uses `.demo/steps.conf` and needs none of this.
