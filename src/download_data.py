# -*- coding: utf-8 -*-
"""원본 데이터 재수집 스크립트
도로교통공단 교통사고정보 개방시스템(https://opendata.koroad.or.kr)이 제공하는
공식 CSV 다운로드 경로를 사용한다. 로그인과 인증키가 필요하지 않다.
원본 데이터는 저장소에 포함하지 않으며 본 스크립트로 각자 내려받는다.
"""
import os, sys, requests

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
HOST = "https://opendata.koroad.or.kr"

FILES = {
    "oldmandown.csv":     ("보행노인 사고다발지역",           "/api/selectOldmanDataSet.do"),
    "pedstriansdown.csv": ("보행자 사고다발지역",             "/api/selectPedstriansDataSet.do"),
    "childdown.csv":      ("보행어린이 사고다발지역",         "/api/selectChildDataSet.do"),
    "schoolzonedown.csv": ("어린이보호구역내 어린이 사고다발지역", "/api/selectSchoolChildDataSet.do"),
    "bicycledown.csv":    ("자전거 사고다발지역",             "/api/selectBicycleDataSet.do"),
}

def main():
    os.makedirs(DATA, exist_ok=True)
    s = requests.Session()
    s.headers["User-Agent"] = "Mozilla/5.0 (research; contest submission)"
    for fname, (label, page) in FILES.items():
        s.get(HOST + page, timeout=60)                      # 세션 확보
        url = f"{HOST}/api/down/{fname.replace('.csv', '.jsp')}"
        r = s.get(url, timeout=300)
        r.raise_for_status()
        path = os.path.join(DATA, fname)
        with open(path, "wb") as f:
            f.write(r.content)
        print(f"{label:28s} {len(r.content)/1024:8.0f} KB  -> data/{fname}")

if __name__ == "__main__":
    main()
