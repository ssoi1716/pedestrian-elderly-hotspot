# -*- coding: utf-8 -*-
"""전체 분석 재현: 데이터 수집 -> 전처리 -> 가설 검정 -> 지수 검증 -> 시각화"""
import os, sys, subprocess
BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, "src")
sys.path.insert(0, SRC)

steps = [
    ("원본 데이터 수집",   "download_data.py"),
    ("전처리·클러스터링",  "pipeline.py"),
    ("가설 검정",          "analysis.py"),
    ("지수 검증",          "validate.py"),
    ("시각화",             "figures.py"),
]
for label, script in steps:
    print(f"\n{'='*60}\n[{label}] {script}\n{'='*60}")
    r = subprocess.run([sys.executable, os.path.join(SRC, script)], cwd=SRC,
                       env={**os.environ, "PYTHONIOENCODING": "utf-8"})
    if r.returncode != 0:
        sys.exit(f"실패: {script}")
print("\n완료. outputs/ 와 figures/ 를 확인하세요.")
