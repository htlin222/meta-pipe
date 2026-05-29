#!/usr/bin/env python3
"""RoB 2 traffic-light figure + GRADE summary table.
Judgments are preliminary and ABSTRACT-BASED (full text required to finalise).
Levels: L=low, S=some concerns, H=high."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
HERE.mkdir(parents=True, exist_ok=True)

# RoB2 domains: D1 randomization, D2 deviations, D3 missing data, D4 measurement, D5 selective reporting
DOMAINS = ["D1\nRandomization", "D2\nDeviations", "D3\nMissing data", "D4\nMeasurement", "D5\nSelective rep.", "Overall"]
# Abstract-based judgments for the 5 pooled studies (S=some concerns where full text needed)
rob = {
 "Antikchi 2025 (skill)":      ["S","S","S","S","S","S"],
 "Nasirzade 2024 (skill)":     ["S","S","S","L","S","S"],
 "Ma 2021 (knowledge)":        ["S","S","L","L","S","S"],
 "Blani 2020 (knowledge)":     ["S","S","S","L","S","S"],
 "Cheung 2024 (skill)":        ["S","H","S","S","S","H"],
}
colors = {"L":"#2e7d32","S":"#f9a825","H":"#c62828"}
labels = {"L":"+","S":"–","H":"x"}

with open(HERE/"rob2.csv","w",newline="",encoding="utf-8") as f:
    w=csv.writer(f); w.writerow(["study"]+[d.replace("\n"," ") for d in DOMAINS])
    for s,v in rob.items(): w.writerow([s]+v)

fig, ax = plt.subplots(figsize=(8.5, 0.6*len(rob)+2))
studies=list(rob.keys())
for i,s in enumerate(studies):
    yp=len(studies)-i
    for j,val in enumerate(rob[s]):
        ax.scatter(j+1, yp, s=520, c=colors[val], edgecolors="#333", zorder=3)
        ax.text(j+1, yp, labels[val], ha="center", va="center", color="white", fontsize=11, fontweight="bold")
    ax.text(0.4, yp, s, ha="right", va="center", fontsize=9)
ax.set_xticks(range(1,len(DOMAINS)+1)); ax.set_xticklabels(DOMAINS, fontsize=8)
ax.set_yticks([]); ax.set_xlim(0.3,len(DOMAINS)+1.2); ax.set_ylim(0.3,len(studies)+0.8)
for sp in ax.spines.values(): sp.set_visible(False)
import matplotlib.patches as mpatches
leg=[mpatches.Patch(color=colors["L"],label="Low"),mpatches.Patch(color=colors["S"],label="Some concerns"),mpatches.Patch(color=colors["H"],label="High")]
ax.legend(handles=leg, loc="upper center", bbox_to_anchor=(0.5,-0.12), ncol=3, frameon=False, fontsize=9)
ax.set_title("Risk of Bias (RoB 2) — pooled studies\n(preliminary, abstract-based; full text required)", fontsize=11, fontweight="bold")
plt.tight_layout()
plt.savefig(HERE/"rob2_traffic_light.png", dpi=300, bbox_inches="tight")

# GRADE summary
grade = """# GRADE Summary of Findings (preliminary, abstract-based)

Comparison: Game-based teaching vs conventional teaching, nursing education (RCTs).
Effect measure: standardized mean difference (Hedges' g).

| NWKM level / outcome | Studies (n) | Pooled effect (95% CI) | Certainty | Reasons for downgrading |
|---|---|---|---|---|
| **L2 Knowledge / skill** | 5 RCTs | g = 0.65 (0.24–1.05) | **Low** ⊕⊕◯◯ | −1 risk of bias (allocation/blinding unverified, abstract-based); −1 inconsistency (I²=71%, PI crosses 0) |
| **L1 Reaction / engagement / satisfaction** | narrative (≥10 RCTs report, few extractable) | favors game-based (not pooled) | **Very low** ⊕◯◯◯ | −1 risk of bias; −1 inconsistency; −1 imprecision (no pooled estimate, self-report) |
| **L3 Clinical behavior change** | 2 RCTs (narrative) | insufficient data | **Very low** ⊕◯◯◯ | sparse data, indirectness, imprecision |
| **L4 Patient / system outcome** | 0 RCTs | not assessed | — | no eligible studies reported L4 outcomes |

RCTs start at HIGH certainty and are downgraded per GRADE domains (risk of bias,
inconsistency, indirectness, imprecision, publication bias). Publication bias was not
formally assessed (<10 pooled studies; funnel plot uninformative).

**Caveat:** Certainty ratings are provisional. Effect sizes were extracted from
abstracts by an automated AI pipeline; full-text extraction, dual independent RoB 2
scoring, and consensus are required before these ratings can be considered final.
"""
Path(HERE/"grade_summary.md").write_text(grade, encoding="utf-8")
print("Saved rob2_traffic_light.png, rob2.csv, grade_summary.md")
