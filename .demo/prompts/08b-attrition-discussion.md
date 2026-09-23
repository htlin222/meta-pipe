Stage 08b — quantify the attrition in the Discussion, and clear the last typographic defects. Same standing rules.

## The number that needs saying out loud

87 studies passed full-text eligibility. **21 entered the network.** The other 66 were excluded not because they were ineligible but because no usable per-arm pCR pair could be extracted from what was retrievable — overwhelmingly a consequence of abstract-only sourcing. That is 76% of the eligible evidence, and at present it appears as one box in the PRISMA diagram.

Write it into the Discussion as its own paragraph in the limitations, and make it concrete rather than apologetic:

1. **How many and why.** Break the 66 down by the reason the arm-level pair was unusable — no pCR figure at all, a single pooled percentage with no arm split, an arm percentage with no arm denominator, arms that could not be mapped to a node. Take the counts from `05_extraction/` rather than estimating them.
2. **What it cost the network.** Which nodes lost trials, and did any node lose enough to change its status from replicated to single-trial? If `N8`, `N9` or `N10` would have had more than one trial with full-text access, say so — that is the difference between a rank you can report and one you must caveat.
3. **Which direction the bias runs, if any.** Were the 66 systematically newer, smaller, non-English, or conference-only? If they skew toward the newest agents, the network under-represents exactly the regimens clinicians are asking about, and that is a sharper limitation than "some studies could not be included". If they do not skew, say that too — an absence of bias is worth stating when you have checked.
4. **What would fix it.** Institutional full-text access, and Embase plus CENTRAL. Name the two concretely so a reader can judge how much of this is a property of the method versus a property of this run's access.

Add the breakdown as a supplementary table (`table_s12_not_networked.md` / `.csv`), and reference it from both the Discussion and the PRISMA figure's caption.

Do not soften this into "some studies could not be networked". The honest framing is that the analysis rests on a quarter of the eligible evidence, and the reader is entitled to the arithmetic.

## Remaining typography

Both are small and both are in the presentation set:

- `04_sucra_ranking.png` — the title breaks so that the single word `trials` falls onto line 2. Rebalance the wrap. The legend swatches also sit flush against their labels (`3 or more trials`, `▲ 2 trials or fewer`) with no gap; add space between the key and its text.
- `06_prisma_flow.png` — in the first box, `= 4,026` is clipped by the box border and the outgoing arrow overlaps the text. Grow the box or reduce the padding so the third line sits inside it.

Re-render, re-verify the dpi, and rebuild the contact sheet.

Write `.progress/steps/08b.done` when the Discussion paragraph, the supplementary table and the two figures are all in place.

Finish with: the 66-study breakdown by reason, whether any node's status would have changed, whether the excluded set skews, and confirmation that the manuscript re-rendered.
