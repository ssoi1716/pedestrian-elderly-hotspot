# -*- coding: utf-8 -*-
"""
보행 고령자 사고다발지역 재출현 구조 분석 - 전처리 및 지표 산출
데이터: 도로교통공단 교통사고정보 개방시스템 (https://opendata.koroad.or.kr)
"""
import os, re, json
import numpy as np
import pandas as pd

SEED = 42
np.random.seed(SEED)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
OUT  = os.path.join(BASE, "outputs")
os.makedirs(OUT, exist_ok=True)

RADIUS_M   = 150   # 클러스터 반경. 민감도 검증 결과 100~250m 전 구간에서 결론 방향 동일
RECUR_MIN  = 3     # 재출현 정의: 3개 연도 이상 지정

FILES = {
    "보행노인":        "oldmandown.csv",
    "보행자":          "pedstriansdown.csv",
    "자전거":          "bicycledown.csv",
    "보행어린이":      "childdown.csv",
    "어린이보호구역내": "schoolzonedown.csv",
}

# 2026년 기준으로 정규화. 데이터 내 확인된 개편 3건:
#   2023년 강원도 → 강원특별자치도 / 전라북도 → 전북특별자치도
#   2026년 전라남도 + 광주광역시 → 전남광주통합특별시
SIDO_MAP = {
    "서울":"서울특별시","서울특별시":"서울특별시",
    "부산":"부산광역시","부산광역시":"부산광역시",
    "대구":"대구광역시","대구광역시":"대구광역시",
    "인천":"인천광역시","인천광역시":"인천광역시",
    "대전":"대전광역시","대전광역시":"대전광역시",
    "울산":"울산광역시","울산광역시":"울산광역시",
    "세종":"세종특별자치시","세종특별자치시":"세종특별자치시",
    "경기":"경기도","경기도":"경기도",
    "강원":"강원특별자치도","강원도":"강원특별자치도","강원특별자치도":"강원특별자치도",
    "충북":"충청북도","충청북도":"충청북도",
    "충남":"충청남도","충청남도":"충청남도",
    "전북":"전북특별자치도","전라북도":"전북특별자치도","전북특별자치도":"전북특별자치도",
    "전남":"전남광주통합특별시","전라남도":"전남광주통합특별시",
    "광주":"전남광주통합특별시","광주광역시":"전남광주통합특별시",
    "전남광주통합특별시":"전남광주통합특별시",
    "경북":"경상북도","경상북도":"경상북도",
    "경남":"경상남도","경상남도":"경상남도",
    "제주":"제주특별자치도","제주특별자치도":"제주특별자치도",
}

def load(key):
    """인코딩 불일치 대응: 파일별로 CP949/UTF-8 자동 판별"""
    path = os.path.join(DATA, FILES[key])
    for enc in ("cp949", "utf-8-sig", "utf-8"):
        try:
            df = pd.read_csv(path, encoding=enc)
            if "사고다발지id" in df.columns:
                df.attrs["encoding"] = enc
                return df
        except Exception:
            continue
    raise RuntimeError(f"load fail: {path}")

def preprocess(df):
    """연도 파싱 + 시도명 정규화 + 시군구 추출"""
    df = df.copy()
    df["연도"] = df["사고다발지id"].astype(str).str[:4].astype(int)
    raw = df["시도시군구명"].astype(str).str.strip()
    raw = raw.str.replace(r"\d+$", "", regex=True).str.strip()   # 말미 일련번호 제거
    parts = raw.str.split(n=1)
    sido_raw = parts.str[0]
    df["시도"] = sido_raw.map(lambda s: SIDO_MAP.get(s, s))      # 약칭 → 정식 명칭
    df["시군구"] = parts.str[1].fillna("")
    return df.reset_index(drop=True)

def cluster(df, radius_m=RADIUS_M):
    """단일 연결 클러스터링. 위도 정렬 후 밴드 탐색으로 O(n·k)"""
    lat = df["위도"].to_numpy(float); lon = df["경도"].to_numpy(float)
    n = len(df); parent = np.arange(n)
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[rb] = ra
    order = np.argsort(lat); lat_sorted = lat[order]
    dlat = radius_m / 111_000.0
    r2 = radius_m * radius_m
    for ii, i in enumerate(order):
        hi = np.searchsorted(lat_sorted, lat[i] + dlat, side="right")
        for j in order[ii+1:hi]:
            dy = (lat[i] - lat[j]) * 111_000.0
            dx = (lon[i] - lon[j]) * 111_000.0 * np.cos(np.radians(lat[i]))
            if dx*dx + dy*dy <= r2: union(i, j)
    return np.array([find(i) for i in range(n)])

FACILITY = [
    ("전통시장",       r"시장"),
    ("약국",           r"약국"),
    ("주민센터·행정",  r"주민센터|행정복지|면사무소|읍사무소|시청|군청|구청"),
    ("병원·의원",      r"병원|의원|보건소"),
    ("역·터미널",      r"터미널|정류장|역앞|역 앞|전철역|지하철"),
    ("학교",           r"학교|초교|중교|고교|대학"),
    ("은행",           r"은행|농협|새마을금고|신협"),
    ("마트·상가",      r"마트|상가|백화점|쇼핑"),
    ("교차로·사거리",  r"교차로|사거리|삼거리|오거리"),
]

def facility_label(name):
    """지점명 시설 분류. 우선순위 순 단일 배정으로 중복 계상 방지"""
    s = str(name)
    for label, pat in FACILITY:
        if re.search(pat, s): return label
    return "기타"

def build(key="보행노인", radius_m=RADIUS_M):
    df = preprocess(load(key))
    df["cid"] = cluster(df, radius_m)
    g = df.groupby("cid").agg(
        재출현연도수=("연도", "nunique"),
        지정횟수=("연도", "size"),
        최초연도=("연도", "min"),
        최종연도=("연도", "max"),
        누적사고=("사고건수", "sum"),
        누적사상=("사상자수", "sum"),
        누적사망=("사망자수", "sum"),
        누적중상=("중상자수", "sum"),
        위도=("위도", "mean"),
        경도=("경도", "mean"),
    )
    last = df.sort_values("연도").groupby("cid").last()
    g["지점명"] = last["지점명"]; g["시도"] = last["시도"]; g["시군구"] = last["시군구"]
    g["시설유형"] = g["지점명"].map(facility_label)
    g["재출현"] = g["재출현연도수"] >= RECUR_MIN
    obs = df["연도"].nunique()
    g["지속성"] = g["재출현연도수"] / obs
    # 지속위험지수(PRI) = 누적 사상자수 x 지속성
    # 사망자수 기반 지수는 시간분할 검증에서 일관되게 열등했음(validate.py 참조).
    # 사망은 희소사건이라 과거 사망자수가 미래 위험의 노이즈 큰 대리변수가 됨.
    g["PRI"] = g["누적사상"] * g["지속성"]
    g["RPI_사망기준"] = g["누적사망"] * g["지속성"]   # 비교용 대조 지수
    return df, g, obs

if __name__ == "__main__":
    df, g, obs = build()
    df.to_csv(os.path.join(OUT, "01_전처리_보행노인.csv"), index=False, encoding="utf-8-sig")
    g.sort_values("PRI", ascending=False).to_csv(os.path.join(OUT, "02_클러스터_지표.csv"), encoding="utf-8-sig")
    print(f"원자료 {len(df):,}건 / 관측연도 {obs}년 / 클러스터 {len(g):,}곳")
    print(f"재출현({RECUR_MIN}개연도+) {int(g.재출현.sum()):,}곳 ({g.재출현.mean()*100:.1f}%)")
    print(f"누적 사망 {int(g.누적사망.sum()):,}명 / 사고 {int(g.누적사고.sum()):,}건")
    print(f"시도 정규화 후 고유값 {df.시도.nunique()}개")
