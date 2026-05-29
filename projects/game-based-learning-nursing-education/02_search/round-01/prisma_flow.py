#!/usr/bin/env python3
"""PRISMA 2020 flow diagram (Python/matplotlib; R unavailable)."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parents[2] / "figures"
OUT.mkdir(parents=True, exist_ok=True)

fig, ax = plt.subplots(figsize=(9.5, 11))
ax.set_xlim(0, 10); ax.set_ylim(0, 14); ax.axis("off")

def box(x, y, w, h, text, fc="#eaf2fb"):
    ax.add_patch(FancyBboxPatch((x-w/2, y-h/2), w, h, boxstyle="round,pad=0.05",
                 linewidth=1, edgecolor="#2b6cb0", facecolor=fc))
    ax.text(x, y, text, ha="center", va="center", fontsize=9, wrap=True)

def arrow(x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                 mutation_scale=14, color="#444", lw=1.2))

# left column (main flow), right column (exclusions)
box(3.3, 13.0, 5.2, 1.2,
    "Records identified from databases (n = 640)\nPubMed 205 · Scopus 292 · Europe PMC 143", fc="#dbeafe")
box(8.0, 13.0, 3.0, 1.0, "Duplicate records removed\n(n = 325)", fc="#f7fafc")
arrow(5.9, 13.0, 6.5, 13.0)

box(3.3, 11.0, 5.2, 1.0, "Records screened (title/abstract)\n(n = 315)")
arrow(3.3, 12.4, 3.3, 11.5)
box(8.0, 11.0, 3.0, 1.0, "Records excluded\n(n = 199)", fc="#f7fafc")
arrow(5.9, 11.0, 6.5, 11.0)

box(3.3, 9.0, 5.2, 1.0, "Reports sought / assessed for eligibility\n(n = 116)")
arrow(3.3, 10.5, 3.3, 9.5)
box(8.0, 8.7, 3.2, 1.9,
    "Reports excluded (n = 28)\nComparator also gamified (C1) 11\nNot an RCT / design (S1) 9\nWrong population (P1) 6\nNo quant. outcome (O1) 1\nNo game element (I1) 1", fc="#f7fafc")
arrow(5.9, 9.0, 6.4, 8.9)

box(3.3, 6.7, 5.6, 1.5,
    "Studies included in review (n = 88)\nRCT confirmed from abstract: 61\nPending full-text RCT confirmation: 27", fc="#dcfce7")
arrow(3.3, 8.5, 3.3, 7.45)

box(3.3, 4.4, 5.6, 1.3,
    "Included in quantitative synthesis\n(meta-analysis, L2 outcomes): n = 5\n(studies with extractable group statistics)", fc="#dcfce7")
arrow(3.3, 5.95, 3.3, 5.05)

# phase labels
for y, lab in [(13.0,"Identification"), (11.0,"Screening"), (9.0,"Eligibility"), (5.5,"Included")]:
    ax.text(0.15, y, lab, rotation=90, va="center", ha="center", fontsize=10,
            fontweight="bold", color="#2b6cb0")

ax.set_title("PRISMA 2020 Flow Diagram\nGame-based Teaching Strategies in Nursing Education (RCTs)",
             fontsize=12, fontweight="bold")
plt.tight_layout()
for ext in ("png", "pdf"):
    plt.savefig(OUT / f"prisma_flow.{ext}", dpi=300, bbox_inches="tight")
print("Saved", OUT / "prisma_flow.png")
