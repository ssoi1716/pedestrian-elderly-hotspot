# -*- coding: utf-8 -*-
"""본 분석: 가설 검증, 우선순위 지수 설계, 시나리오 비교"""
import os, json
import numpy as np, pandas as pd
from scipy import stats
from pipeline import build, OUT, RADIUS_M, RECUR_MIN

R = {}
df, g, OBS = build()
R["기본"] = dict(원자료=len(df), 관측연도=OBS, 클러스터=len(g),
                 누적사망=int(g.누적사망.sum()), 누적사고=int(g.누적사고.sum()),
                 누적중상=int(g.누적중상.sum()))

# ---------- H1. 재출현 분포 ----------
dist = {k: int((g.재출현연도수 >= k).sum()) for k in range(1, OBS+1)}
R["H1_분포"] = {f"{k}개연도이상": {"지점": v, "비율%": round(v/len(g)*100, 1)} for k, v in dist.items()}
top14 = g[g.재출현연도수 == OBS].sort_values("누적사망", ascending=False)
R["H1_전기간연속"] = [
    dict(지점명=r.지점명, 시도=r.시도, 사망=int(r.누적사망), 사고=int(r.누적사고))
    for r in top14.itertuples()]

# ---------- H2. 피해 집중 ----------
rec, one = g[g.재출현], g[g.재출현연도수 == 1]
u, p = stats.mannwhitneyu(rec.누적사망, one.누적사망, alternative="greater")
R["H2"] = dict(
    재출현지점=len(rec), 단발지점=len(one),
    재출현_지점당사망=round(rec.누적사망.mean(), 2), 단발_지점당사망=round(one.누적사망.mean(), 2),
    배수=round(rec.누적사망.mean()/one.누적사망.mean(), 1),
    재출현_지점당사고=round(rec.누적사고.mean(), 1), 단발_지점당사고=round(one.누적사고.mean(), 1),
    지점점유율=round(len(rec)/len(g)*100, 1),
    사망점유율=round(rec.누적사망.sum()/g.누적사망.sum()*100, 1),
    사고점유율=round(rec.누적사고.sum()/g.누적사고.sum()*100, 1),
    MannWhitneyU=float(u), p=float(p))

# ---------- H3. 시설유형별 (단일 배정, 중복 제거) ----------
base = g.재출현.mean()*100
fac = g.groupby("시설유형").agg(지점=("재출현","size"), 재출현=("재출현","sum"),
                                사망=("누적사망","sum")).query("지점>=20")
fac["재출현율%"] = (fac.재출현/fac.지점*100).round(1)
fac["기준선대비%p"] = (fac["재출현율%"] - base).round(1)
fac = fac.sort_values("재출현율%", ascending=False)
R["H3_기준선%"] = round(base, 1)
R["H3"] = fac.reset_index().to_dict("records")
ct = pd.crosstab(g.시설유형.where(g.시설유형.isin(fac.index), "기타분류"), g.재출현)
chi2, pv, dof, _ = stats.chi2_contingency(ct)
R["H3_검정"] = dict(chi2=round(float(chi2),1), dof=int(dof), p=float(pv))
# 학교 vs 전통시장 직접 대비
for a, b in [("학교","전통시장")]:
    ga, gb = g[g.시설유형==a], g[g.시설유형==b]
    odds, pf = stats.fisher_exact([[int(gb.재출현.sum()), len(gb)-int(gb.재출현.sum())],
                                   [int(ga.재출현.sum()), len(ga)-int(ga.재출현.sum())]])
    R["H3_학교vs시장"] = dict(학교재출현율=round(ga.재출현.mean()*100,1),
                              시장재출현율=round(gb.재출현.mean()*100,1),
                              오즈비=round(float(odds),1), p=float(pf))

# ---------- 우선순위 지수 3안 비교 ----------
def coverage(rank_col, ns=(100, 200, 300, 577)):
    s = g.sort_values(rank_col, ascending=False)
    tot_d, tot_a = g.누적사망.sum(), g.누적사고.sum()
    out = {}
    for n in ns:
        h = s.head(n)
        out[n] = dict(사망커버율=round(h.누적사망.sum()/tot_d*100, 1),
                      사고커버율=round(h.누적사고.sum()/tot_a*100, 1),
                      평균재출현연도=round(h.재출현연도수.mean(), 1),
                      최근5년내포함률=round((h.최종연도 >= 2022).mean()*100, 1))
    return out
R["우선순위_3안"] = {
    "A안 누적사망 단순정렬": coverage("누적사망"),
    "B안 재출현연도수 정렬": coverage("재출현연도수"),
    "C안 사망x지속성":       coverage("RPI_사망기준"),
    "D안 누적사고":          coverage("누적사고"),
    "E안 PRI 사상x지속성(채택)": coverage("PRI"),
}
top = g.sort_values("PRI", ascending=False).head(30)
R["최우선30"] = [dict(순위=i+1, 지점명=r.지점명, 시도=r.시도, 시군구=r.시군구,
                      시설유형=r.시설유형, 재출현연도=int(r.재출현연도수),
                      사망=int(r.누적사망), 사고=int(r.누적사고), PRI=round(r.PRI,1))
                 for i, r in enumerate(top.itertuples())]

# ---------- 시도별 ----------
sido = g.groupby("시도").agg(지점=("재출현","size"), 재출현=("재출현","sum"),
                             사망=("누적사망","sum"), PRI합=("PRI","sum"))
sido["재출현율%"] = (sido.재출현/sido.지점*100).round(1)
R["시도별"] = sido.sort_values("재출현", ascending=False).reset_index().to_dict("records")

# ---------- 시계열 ----------
yr = df.groupby("연도").agg(지점=("사고다발지id","size"), 사망=("사망자수","sum"), 사고=("사고건수","sum"))
cidyear = df.groupby(["cid","연도"]).size().reset_index()
first = df.groupby("cid").연도.min()
cidyear["신규"] = cidyear.apply(lambda r: first[r.cid] == r.연도, axis=1)
newrate = cidyear.groupby("연도").신규.mean()*100
yr["신규지점비율%"] = newrate.round(1)
R["시계열"] = yr.reset_index().to_dict("records")

# ---------- 민감도 ----------
from pipeline import build as _b
sens = []
for r_ in (100, 150, 200, 250):
    _, gg, _o = _b(radius_m=r_)
    rr = gg[gg.재출현연도수 >= RECUR_MIN]
    sens.append(dict(반경=r_, 클러스터=len(gg), 재출현=len(rr),
                     비율=round(len(rr)/len(gg)*100,1),
                     사망점유=round(rr.누적사망.sum()/gg.누적사망.sum()*100,1),
                     사고점유=round(rr.누적사고.sum()/gg.누적사고.sum()*100,1)))
R["민감도"] = sens

with open(os.path.join(OUT, "03_분석결과.json"), "w", encoding="utf-8") as f:
    json.dump(R, f, ensure_ascii=False, indent=2, default=str)
g.sort_values("PRI", ascending=False).to_csv(os.path.join(OUT, "04_우선순위_전체.csv"), encoding="utf-8-sig")
top.to_csv(os.path.join(OUT, "05_최우선30.csv"), encoding="utf-8-sig")

print(json.dumps({k: R[k] for k in ["기본","H2","H3_검정","H3_학교vs시장"]}, ensure_ascii=False, indent=2))
print("\n[시설유형]"); print(fac.to_string())
print("\n[우선순위 3안 - 사망커버율]")
for k, v in R["우선순위_3안"].items():
    print(f"  {k:24s}", {n: v[n]["사망커버율"] for n in v})
print("\n[민감도]"); print(pd.DataFrame(sens).to_string(index=False))
