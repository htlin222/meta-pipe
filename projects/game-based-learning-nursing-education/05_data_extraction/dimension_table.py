#!/usr/bin/env python3
"""Render the dimension cross-tabulation (the originally requested table) as
a Markdown table and a grouped bar figure, over the 88 included studies."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJ = Path(__file__).resolve().parents[1]
dims = json.loads((PROJ/"05_data_extraction"/"dimension_counts.json").read_text(encoding="utf-8"))

GROUPS = [
 ("研究對象 Participant", "participant_type"),
 ("遊戲類型 Game type", "game_type"),
 ("NWKM 成效層級 (可複選)", "nwkm_levels(L*)"),
 ("專科領域 Specialty", "specialty"),
 ("介入時長 Duration", "duration"),
 ("平台/載具 Platform", "platform"),
 ("對照組 Comparator", "comparator_type"),
]
lines = ["# Dimension cross-tabulation of included studies (n = 88)",
         "",
         "Counts are number of included studies in each category. NWKM levels can",
         "co-occur within a study, so that block sums to >88. All other blocks sum to 88.",
         "",
         "| 項目 Dimension | 層面 Category | 研究數 n |",
         "|---|---|---|"]
for title, key in GROUPS:
    items = sorted(dims[key].items(), key=lambda kv: -kv[1])
    for i,(cat,n) in enumerate(items):
        lines.append(f"| {title if i==0 else ''} | {cat} | {n} |")
(Path(PROJ/"05_data_extraction"/"dimension_table.md")).write_text("\n".join(lines)+"\n", encoding="utf-8")

# figure: 7 horizontal bar subplots
fig, axes = plt.subplots(4, 2, figsize=(12, 13))
axes = axes.flatten()
for ax,(title,key) in zip(axes, GROUPS):
    items = sorted(dims[key].items(), key=lambda kv: kv[1])
    cats=[c for c,_ in items]; vals=[v for _,v in items]
    ax.barh(cats, vals, color="#2b6cb0")
    for y,v in enumerate(vals): ax.text(v+0.3, y, str(v), va="center", fontsize=8)
    ax.set_title(title, fontsize=10, fontweight="bold")
    ax.tick_params(axis="y", labelsize=8)
    for sp in ["top","right"]: ax.spines[sp].set_visible(False)
axes[-1].axis("off")
fig.suptitle("Included studies by dimension (n = 88)", fontsize=13, fontweight="bold")
plt.tight_layout(rect=[0,0,1,0.98])
plt.savefig(PROJ/"figures"/"dimension_bars.png", dpi=200, bbox_inches="tight")
print("Saved dimension_table.md and dimension_bars.png")
