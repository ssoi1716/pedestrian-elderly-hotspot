# -*- coding: utf-8 -*-
"""보고서용 시각화. 라이트 테마, A4 인쇄 기준."""
import os, json
import numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from pipeline import build, OUT
import validate as V

FIG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "figures")
os.makedirs(FIG, exist_ok=True)

FONT = "Pretendard" if any("Pretendard" == f.name for f in fm.fontManager.ttflist) else "Malgun Gothic"
plt.rcParams.update({
    "font.family": FONT, "axes.unicode_minus": False,
    "figure.dpi": 200, "savefig.dpi": 200, "savefig.bbox": "tight",
    "axes.edgecolor": "#C9D1D9", "axes.linewidth": 0.8,
    "axes.labelcolor": "#3A4750", "text.color": "#1F2933",
    "xtick.color": "#5A6672", "ytick.color": "#5A6672",
    "xtick.labelsize": 9, "ytick.labelsize": 9, "axes.labelsize": 9.5,
    "axes.grid": True, "grid.color": "#EDF0F3", "grid.linewidth": 0.8,
    "legend.frameon": False, "legend.fontsize": 9,
})
RISK, ALT, NEU, PALE = "#C4342B", "#2E7DA8", "#9AA5B1", "#E8ECEF"

def title(ax, t, lead=None):
    """짧은 제목 + 리드 문장 분리 배치"""
    ax.set_title(t, loc="left", fontsize=11.5, fontweight="bold",
                 pad=26 if lead else 9, color="#1F2933")
    if lead:
        ax.text(0, 1.035, lead, transform=ax.transAxes, fontsize=9,
                color="#6B7885", va="bottom", ha="left")

df, g, OBS = build()

# ── Fig1. 전국 분포 + 시도별 ─────────────────────────────────
fig = plt.figure(figsize=(9.8, 5.1))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.42], wspace=.16)
axm = fig.add_subplot(gs[0, 0])
axm.scatter(g.경도, g.위도, s=1.6, c=PALE, linewidths=0)
rec = g[g.재출현]
axm.scatter(rec.경도, rec.위도, s=5.5, c=RISK, linewidths=0, alpha=.8)
axm.set_aspect(1/np.cos(np.radians(36)))
axm.set_xlim(125.6, 129.8); axm.set_ylim(33.0, 38.7)
axm.set_xticks([]); axm.set_yticks([]); axm.grid(False)
for sp in axm.spines.values(): sp.set_color("#E3E8ED")
axm.set_title("전국 3,094곳 중 재출현 577곳", loc="left", fontsize=9.4,
              fontweight="bold", pad=6, color="#1F2933")

sd = (g.groupby("시도").agg(지점=("재출현","size"), 재출현=("재출현","sum"))
        .sort_values("재출현").tail(10))
sd["율"] = sd.재출현/sd.지점*100
axb = fig.add_subplot(gs[0, 1])
axb.grid(False)
axb.barh(sd.index, sd.지점, color=PALE, height=.62, label="전체 지정 지점", zorder=3)
axb.barh(sd.index, sd.재출현, color=RISK, height=.62, label="3개 연도 이상 재출현", zorder=4)
for i,(k,r) in enumerate(sd.iterrows()):
    axb.text(r.지점+12, i, f"{int(r.재출현)}곳 · {r.율:.0f}%", va="center",
             fontsize=8.2, color="#3A4750")
axb.set_xlim(0, 900); axb.set_xlabel("지점 수"); axb.grid(axis="y", visible=False)
axb.spines[["top","right"]].set_visible(False)
axb.legend(loc="lower right", fontsize=8.4)
axb.set_title("시도별 재출현 지점 (상위 10)", loc="left", fontsize=9.4,
              fontweight="bold", pad=6, color="#1F2933")
fig.subplots_adjust(top=0.83, bottom=0.10, left=0.02, right=0.985)
fig.text(0.02, 0.985, "[그림 1] 보행노인 사고다발지역의 전국 분포와 시도별 재출현 (2013~2026)",
         ha="left", va="top", fontsize=11.5, fontweight="bold", color="#1F2933")
fig.text(0.02, 0.925, "재출현 지점은 수도권·부산권과 남동 해안권에 집중됨. 부산은 재출현율 23.0%로 전국 최고",
         ha="left", va="top", fontsize=8.8, color="#6B7885")
fig.savefig(os.path.join(FIG, "fig1_분포지도.png")); plt.close(fig)

# ── Fig2. 피해 집중도 ────────────────────────────────────────
rec, one = g[g.재출현], g[~g.재출현]
labels = ["지점 수", "누적 사고건수", "누적 사상자수", "누적 사망자수"]
tot = [len(g), g.누적사고.sum(), g.누적사상.sum(), g.누적사망.sum()]
share = [len(rec)/len(g)*100, rec.누적사고.sum()/g.누적사고.sum()*100,
         rec.누적사상.sum()/g.누적사상.sum()*100, rec.누적사망.sum()/g.누적사망.sum()*100]
fig, ax = plt.subplots(figsize=(8.4, 3.3))
y = np.arange(len(labels))[::-1]
ax.barh(y, 100, color=PALE, height=.58, zorder=2)
ax.barh(y, share, color=[NEU, RISK, RISK, RISK], height=.58, zorder=3)
for yy, lab, sh, tt in zip(y, labels, share, tot):
    ax.text(sh+1.5, yy, f"{sh:.1f}%", va="center", fontsize=10, fontweight="bold", color="#1F2933", zorder=4)
    ax.text(101.5, yy, f"전체 {int(tt):,}", va="center", fontsize=8.6, color="#8A96A3", zorder=4)
ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9.8)
ax.set_xlim(0, 125); ax.set_xticks([0,20,40,60,80,100]); ax.set_xticklabels(["0","20","40","60","80","100%"])
ax.set_xlabel("재출현 지점 577곳이 차지하는 비중")
ax.grid(visible=False); ax.spines[["top","right","left"]].set_visible(False)
title(ax, "[그림 2] 전체의 18.6%인 재출현 지점에 피해가 집중됨",
      "지점 수 비중 대비 사망자 비중이 2.5배. 맨휘트니 U 검정 p<0.001")
fig.savefig(os.path.join(FIG, "fig2_피해집중.png")); plt.close(fig)

# ── Fig3. 시설유형별 재출현율 ────────────────────────────────
base = g.재출현.mean()*100
fac = (g.groupby("시설유형").agg(지점=("재출현","size"), 율=("재출현","mean"))
         .query("지점>=20 and 시설유형!='기타'").assign(율=lambda d: d.율*100).sort_values("율"))
fig, ax = plt.subplots(figsize=(8.4, 4.1))
cols = [RISK if v >= base+10 else (ALT if v <= base-5 else NEU) for v in fac.율]
ax.barh(fac.index, fac.율, color=cols, height=.66, zorder=3)
ax.axvline(base, color="#5A6672", lw=1.1, ls="--", zorder=2)
ax.text(base+.7, len(fac)-0.35, f"전체 기준선 {base:.1f}%", fontsize=8.8, color="#5A6672", va="center")
for i,(k,v) in enumerate(zip(fac.index, fac.율)):
    ax.text(v+1.2, i, f"{v:.1f}%  (n={int(fac.지점[k])})", va="center", fontsize=8.6,
            color="#3A4750", zorder=4)
ax.set_ylim(-0.7, len(fac)-0.2)
ax.set_xlim(0, 70); ax.set_xlabel("재출현율 (3개 연도 이상 지정 비율, %)"); ax.grid(axis="y", visible=False)
title(ax, "[그림 3] 상시 보호 제도의 유무가 재출현율을 가름",
      "어린이보호구역이 적용되는 학교 인근은 10.0%, 제도 공백인 전통시장 인근은 53.7%")
fig.savefig(os.path.join(FIG, "fig3_시설유형.png")); plt.close(fig)

# ── Fig4. 지수 예측력 + 시나리오 (2패널) ──────────────────────
t, summ, out = V.run()
summ = summ.sort_values("평균 예측커버율%")
fig = plt.figure(figsize=(9.8, 4.0))
gs = fig.add_gridspec(1, 2, width_ratios=[1.06, 1], wspace=.30)

ax = fig.add_subplot(gs[0, 0])
cols = [RISK if "A 누적사망" in i else (ALT if "PRI" in i else NEU) for i in summ.index]
ax.barh(summ.index, summ["평균 예측커버율%"], color=cols, height=.62, zorder=3,
        xerr=[summ["평균 예측커버율%"]-summ["최소"], summ["최대"]-summ["평균 예측커버율%"]],
        error_kw=dict(ecolor="#B8C2CC", lw=1.0, capsize=2.2, zorder=4))
rb = out["무작위기준선"]["평균"]
ax.axvline(rb, color="#5A6672", lw=1.0, ls="--", zorder=2)
ax.text(rb+1.2, len(summ)-0.45, f"무작위 {rb}%", fontsize=8.2, color="#5A6672", va="center")
for i, v in enumerate(summ["평균 예측커버율%"]):
    ax.text(v+1.2, i, f"{v:.1f}", va="center", fontsize=8.4, color="#3A4750", zorder=4)
ax.set_xlim(0, 80); ax.set_ylim(-0.7, len(summ)-0.2)
ax.set_xlabel("검증 구간 사망자 커버율 (5개 분할 평균, %)")
ax.tick_params(axis="y", labelsize=8.4); ax.grid(axis="y", visible=False)
ax.set_title("지수별 표본외 예측력 (상위 300곳 선정)", loc="left",
             fontsize=9.4, fontweight="bold", pad=6, color="#1F2933")

tr, te = df[df.연도<=2021], df[df.연도>2021]
o = tr.연도.nunique()
a_ = tr.groupby("cid").agg(연도수=("연도","nunique"), 사망=("사망자수","sum"), 사상=("사상자수","sum"))
a_["PRI"] = a_.사상*a_.연도수/o
b_ = te.groupby("cid").사망자수.sum().to_frame("미래사망")
m = a_.join(b_, how="left").fillna(0); tot = m.미래사망.sum()
ns = np.arange(25, 1001, 25)
ax2 = fig.add_subplot(gs[0, 1])
for lab, (c, col) in {"사상자×지속성 (채택)": ("PRI", ALT), "누적 사망자": ("사망", RISK)}.items():
    s2 = m.sort_values([c, "사상"], ascending=False)
    ax2.plot(ns, [s2.head(n).미래사망.sum()/tot*100 for n in ns], color=col, lw=1.9, label=lab)
ax2.plot(ns, ns/len(m)*100, color=NEU, lw=1.1, ls="--", label="무작위 선택")
ax2.axvline(300, color="#5A6672", lw=.9, ls=":")
ax2.set_xlabel("개선 대상 지점 수 (상위 N곳)")
ax2.set_ylabel("검증 구간 사망자 커버율 (%)", fontsize=8.8)
ax2.set_xlim(0, 1000); ax2.set_ylim(0, 92); ax2.legend(loc="lower right", fontsize=8.2)
ax2.set_title("개선 대상 규모별 커버율 (2022~2026 실측)", loc="left",
              fontsize=9.4, fontweight="bold", pad=6, color="#1F2933")

fig.subplots_adjust(top=0.78, bottom=0.155, left=0.135, right=0.985)
fig.text(0.022, 0.985, "[그림 4] 과거 사망자 기준 우선순위는 미래 예측에서 최하위",
         ha="left", va="top", fontsize=11.5, fontweight="bold", color="#1F2933")
fig.text(0.022, 0.925, "누적 사망자 정렬 47.3% 대 사상자×지속성 정렬 63.6%. 오차막대는 5개 분할의 최소~최대",
         ha="left", va="top", fontsize=8.8, color="#6B7885")
fig.savefig(os.path.join(FIG, "fig4_지수검증.png")); plt.close(fig)

print("saved:", sorted(os.listdir(FIG)))
