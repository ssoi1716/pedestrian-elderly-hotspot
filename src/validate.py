# -*- coding: utf-8 -*-
"""지수 선택의 실증 검증
표본내 적합(과거 피해 설명력)과 표본외 예측(미래 피해 예측력)을 분리해 비교한다.
"""
import os, json
import numpy as np, pandas as pd
from pipeline import build, OUT

SPLITS = (2019, 2020, 2021, 2022, 2023)
TOP_N  = 300

def make_index(a, obs):
    a = a.copy(); a["지속성"] = a.연도수/obs
    return a.assign(**{
        "A 누적사망":        a.사망,
        "B 재출현연도수":    a.연도수,
        "C 사망x지속성":     a.사망*a.지속성,
        "D 누적사고":        a.사고,
        "E 사고x지속성":     a.사고*a.지속성,
        "F 누적중상":        a.중상,
        "G 중상x지속성":     a.중상*a.지속성,
        "H 사상x지속성(PRI)": a.사상*a.지속성,
    })

COLS = ["A 누적사망","B 재출현연도수","C 사망x지속성","D 누적사고",
        "E 사고x지속성","F 누적중상","G 중상x지속성","H 사상x지속성(PRI)"]

def run():
    df, g, OBS = build()
    rows = []
    for cut in SPLITS:
        tr, te = df[df.연도 <= cut], df[df.연도 > cut]
        obs = tr.연도.nunique()
        a = make_index(tr.groupby("cid").agg(
            연도수=("연도","nunique"), 사망=("사망자수","sum"), 사고=("사고건수","sum"),
            중상=("중상자수","sum"), 사상=("사상자수","sum")), obs)
        b = te.groupby("cid").agg(미래사망=("사망자수","sum"))
        m = a.join(b, how="left").fillna(0); tot = m.미래사망.sum()
        r = {"학습": f"2013~{cut}", "검증": f"{cut+1}~2026", "검증연수": te.연도.nunique(), "미래사망": int(tot)}
        for c in COLS:
            r[c] = round(m.sort_values([c, "사고"], ascending=False).head(TOP_N).미래사망.sum()/tot*100, 1)
        rows.append(r)
    t = pd.DataFrame(rows)

    # 무작위 기준선
    tr = df[df.연도 <= 2021]; te = df[df.연도 > 2021]
    m = tr.groupby("cid").size().to_frame("n").join(
        te.groupby("cid").사망자수.sum().to_frame("미래사망"), how="left").fillna(0)
    tot = m.미래사망.sum()
    rng = np.random.default_rng(42)
    rand = [m.sample(TOP_N, random_state=int(x)).미래사망.sum()/tot*100 for x in rng.integers(0, 10**6, 300)]

    summary = pd.DataFrame({
        "평균 예측커버율%": t[COLS].mean().round(1),
        "평균 순위": t[COLS].rank(axis=1, ascending=False).mean().round(2),
        "최소": t[COLS].min().round(1), "최대": t[COLS].max().round(1),
    }).sort_values("평균 순위")

    out = dict(상위N=TOP_N, 분할별=t.to_dict("records"),
               요약=summary.reset_index().rename(columns={"index":"지수"}).to_dict("records"),
               무작위기준선=dict(평균=round(float(np.mean(rand)),1), p95=round(float(np.percentile(rand,95)),1)))
    with open(os.path.join(OUT, "06_지수검증.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    return t, summary, out

if __name__ == "__main__":
    t, s, out = run()
    print(f"[표본외 예측력] 상위 {TOP_N}곳 선정 시 검증구간 사망자 커버율\n")
    print(t.to_string(index=False))
    print("\n[요약]"); print(s.to_string())
    print(f"\n무작위 {TOP_N}곳: 평균 {out['무작위기준선']['평균']}%, 95분위 {out['무작위기준선']['p95']}%")
