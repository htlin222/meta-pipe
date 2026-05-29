#!/usr/bin/env python3
"""
Random-effects (DerSimonian-Laird) meta-analysis of L2 (knowledge/skill) outcomes
for game-based teaching vs conventional teaching in nursing education.

Effect measure: standardized mean difference (Hedges' g), intervention - control
(positive = game-based better).

NOTE: R is unavailable in this environment, so this is a from-scratch Python
implementation. Effect sizes were extracted from ABSTRACTS (AI-assisted) and must
be re-extracted from full text before submission. Only studies reporting group
means+SD+n (or a usable d + n) are pooled.
"""
import csv, math, json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent

def hedges_g(m1, sd1, n1, m2, sd2, n2):
    sp = math.sqrt(((n1-1)*sd1**2 + (n2-1)*sd2**2) / (n1+n2-2))
    d = (m1 - m2) / sp
    J = 1 - 3/(4*(n1+n2-2)-1)            # small-sample correction
    g = J*d
    var = (n1+n2)/(n1*n2) + g**2/(2*(n1+n2))
    return g, math.sqrt(var)

def g_from_d(d, n1, n2):
    J = 1 - 3/(4*(n1+n2-2)-1)
    g = J*d
    var = (n1+n2)/(n1*n2) + g**2/(2*(n1+n2))
    return g, math.sqrt(var)

# --- Build the analysis dataset (L2 knowledge/skill) ---
# Studies with complete means+SD+n, plus CheungYTD via reported d.
studies = []
def add(label, year, g, se, outcome):
    studies.append({"label":f"{label} ({year})","g":g,"se":se,"outcome":outcome})

# AntikchiM 2025 skill: 14.57(3.9) n41 vs 12.3(3.6) n41
g,se = hedges_g(14.57,3.9,41,12.3,3.6,41); add("Antikchi","2025",g,se,"skill")
# NasirzadeA 2024 skill: 16.4(2.2) n21 vs 11.8(3.8) n21
g,se = hedges_g(16.4,2.2,21,11.8,3.8,21); add("Nasirzade","2024",g,se,"skill")
# MaD 2021 knowledge(competence): 4.04(0.43) n51 vs 3.77(0.45) n53
g,se = hedges_g(4.04,0.43,51,3.77,0.45,53); add("Ma","2021",g,se,"knowledge")
# BlaniA 2020 knowledge(SCT): 59(9) n73 vs 58(8) n73
g,se = hedges_g(59,9,73,58,8,73); add("Blani","2020",g,se,"knowledge")
# CheungYTD 2024: reported Cohen's d=0.814, n13/13 (empathy/communication)
g,se = g_from_d(0.814,13,13); add("Cheung","2024",g,se,"skill")

# --- DerSimonian-Laird random-effects pool ---
ws = [1/s["se"]**2 for s in studies]
ys = [s["g"] for s in studies]
k = len(studies)
fe = sum(w*y for w,y in zip(ws,ys))/sum(ws)
Q = sum(w*(y-fe)**2 for w,y in zip(ws,ys))
df = k-1
C = sum(ws) - sum(w**2 for w in ws)/sum(ws)
tau2 = max(0,(Q-df)/C) if C>0 else 0
I2 = max(0,(Q-df)/Q)*100 if Q>0 else 0
ws_re = [1/(s["se"]**2+tau2) for s in studies]
pooled = sum(w*y for w,y in zip(ws_re,ys))/sum(ws_re)
se_pool = math.sqrt(1/sum(ws_re))
ci_lo, ci_hi = pooled-1.96*se_pool, pooled+1.96*se_pool
z = pooled/se_pool
# two-sided p
from math import erf
p = 2*(1-0.5*(1+erf(abs(z)/math.sqrt(2))))
# 95% prediction interval (approx, t df=k-2)
pi = None
if k>2:
    import statistics
    t = 2.776 if k-2==4 else 3.182 if k-2==3 else 4.303 if k-2==2 else 2.571
    sd_pred = math.sqrt(se_pool**2 + tau2)
    pi = (pooled - t*sd_pred, pooled + t*sd_pred)

results = {
  "k_studies": k, "model":"random-effects (DerSimonian-Laird)",
  "effect_measure":"Hedges' g (SMD), positive favors game-based",
  "pooled_g": round(pooled,3), "se": round(se_pool,3),
  "ci95": [round(ci_lo,3), round(ci_hi,3)],
  "z": round(z,3), "p_value": round(p,4),
  "Q": round(Q,3), "df": df, "tau2": round(tau2,4), "I2_percent": round(I2,1),
  "prediction_interval95": [round(pi[0],3), round(pi[1],3)] if pi else None,
  "studies": [{**s,"g":round(s["g"],3),"se":round(s["se"],3),
               "ci":[round(s["g"]-1.96*s["se"],2),round(s["g"]+1.96*s["se"],2)]} for s in studies],
}
Path(HERE/"meta_results.json").write_text(json.dumps(results,indent=2),encoding="utf-8")
print(json.dumps(results,indent=2))

# --- Forest plot ---
fig, ax = plt.subplots(figsize=(8, 0.6*k+2.2))
ys_pos = list(range(k,0,-1))
for s,yp in zip(studies,ys_pos):
    lo,hi = s["g"]-1.96*s["se"], s["g"]+1.96*s["se"]
    ax.plot([lo,hi],[yp,yp],color="#444",lw=1.3)
    ax.plot(s["g"],yp,"s",color="#2b6cb0",ms=7)
    ax.text(-0.05, yp, s["label"], ha="right", va="center", fontsize=9, transform=ax.get_yaxis_transform())
    ax.text(1.02, yp, f"{s['g']:.2f} [{lo:.2f}, {hi:.2f}]", ha="left", va="center", fontsize=8, transform=ax.get_yaxis_transform())
# diamond for pooled
yp=0
ax.fill([ci_lo,pooled,ci_hi,pooled],[yp,yp+0.28,yp,yp-0.28],color="#c53030")
ax.text(-0.05,yp,"Pooled (RE)",ha="right",va="center",fontsize=9,fontweight="bold",transform=ax.get_yaxis_transform())
ax.text(1.02,yp,f"{pooled:.2f} [{ci_lo:.2f}, {ci_hi:.2f}]",ha="left",va="center",fontsize=8,fontweight="bold",transform=ax.get_yaxis_transform())
ax.axvline(0,color="#999",ls="--",lw=0.8)
ax.set_ylim(-1,k+1); ax.set_yticks([])
ax.set_xlabel("Standardized mean difference (Hedges' g) — favors conventional ◄ ► favors game-based")
ax.set_title(f"Game-based vs conventional teaching, L2 learning outcomes\nRandom-effects pooled g={pooled:.2f} (95% CI {ci_lo:.2f}–{ci_hi:.2f}); I²={I2:.0f}%; k={k}",fontsize=10)
ax.spines[["top","right","left"]].set_visible(False)
plt.tight_layout()
plt.savefig(HERE/"forest_plot_L2.png",dpi=300,bbox_inches="tight")
print("\nSaved forest_plot_L2.png and meta_results.json")
