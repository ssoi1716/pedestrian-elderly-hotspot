# -*- coding: utf-8 -*-
"""분석보고서 HTML 생성 -> Chrome headless로 PDF 변환"""
import os, base64, json

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG  = os.path.join(BASE, "03_분석", "figures")
OUT  = os.path.join(BASE, "04_보고서")
TEAM = "청신호"
MEMBERS = "○○○ · ○○○ · ○○○"
REPO = "https://github.com/ssoi1716/pedestrian-elderly-hotspot"


def img(name):
    with open(os.path.join(FIG, name), "rb") as f:
        return "data:image/png;base64," + base64.b64encode(f.read()).decode()


CSS = """
@page { size: A4; margin: 15mm 15mm 13mm 15mm; }
* { box-sizing: border-box; }
body { font-family: Pretendard, 'Malgun Gothic', sans-serif; color:#1F2933;
       font-size: 9.15pt; line-height: 1.55; margin:0; -webkit-print-color-adjust: exact; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
h1 { font-size: 15pt; margin: 0 0 2mm; letter-spacing:-.3px; }
h2 { font-size: 11pt; margin: 5mm 0 2mm; padding-bottom: 1.6mm;
     border-bottom: 1.6px solid #1F2933; letter-spacing:-.2px; }
h2:first-of-type { margin-top: 0; }
h3 { font-size: 9.7pt; margin: 3.2mm 0 1.3mm; color:#243B53; }
p { margin: 0 0 1.5mm; }
ul { margin: 0 0 2mm; padding-left: 4.2mm; }
li { margin-bottom: .65mm; }
table { width:100%; border-collapse: collapse; font-size: 8.1pt; margin: 1.6mm 0 2mm; }
th, td { border: .6px solid #CBD2D9; padding: 1.05mm 1.5mm; text-align:left; vertical-align: top; }
th { background:#EEF1F4; font-weight:600; color:#243B53; }
td.n, th.n { text-align: right; font-variant-numeric: tabular-nums; }
.fig { margin: 2mm 0 .8mm; page-break-inside: avoid; }
table, .kpi, h3 { page-break-inside: avoid; }

.fig img { width:100%; display:block; }
.cap { font-size: 7.9pt; color:#6B7885; margin-top: .8mm; }
.lead { background:#F4F6F8; border-left: 2.6px solid #1F2933; padding: 2.2mm 3mm; margin: 0 0 3mm; font-size:9.3pt; }
.kpi { display:flex; gap:2.6mm; margin: 2.5mm 0 3mm; }
.kpi div { flex:1; border:.6px solid #CBD2D9; border-top:2.4px solid #C4342B; padding:2.2mm 2.4mm; }
.kpi b { display:block; font-size:13.5pt; line-height:1.15; color:#C4342B; font-variant-numeric: tabular-nums; }
.kpi span { font-size:7.7pt; color:#5A6672; display:block; margin-top:.6mm; line-height:1.45; }
.note { font-size:8pt; color:#6B7885; margin-top:1.2mm; }
.hl { background: #FDF3E7; padding: 0 .6mm; font-weight:600; }
.cover { text-align:center; padding-top: 60mm; }
.cover .kick { font-size:9.6pt; color:#5A6672; letter-spacing:1.6px; }
.cover h1 { font-size: 19pt; line-height:1.45; margin: 7mm 0 4mm; }
.cover .sub { font-size:10.6pt; color:#3A4750; }
.cover .meta { margin-top: 44mm; font-size:9.4pt; color:#3A4750; line-height:2; }
"""

R = json.load(open(os.path.join(BASE, "03_분석", "outputs", "03_분석결과.json"), encoding="utf-8"))
V = json.load(open(os.path.join(BASE, "03_분석", "outputs", "06_지수검증.json"), encoding="utf-8"))
top30 = R["최우선30"]


def rows_top(n=8):
    out = []
    for r in top30[:n]:
        out.append(
            "<tr><td class='n'>{순위}</td><td>{지점명}</td><td>{시설유형}</td>"
            "<td class='n'>{재출현연도}</td><td class='n'>{사망}</td>"
            "<td class='n'>{사고}</td><td class='n'>{PRI}</td></tr>".format(**r))
    return "\n".join(out)


def rows_sens():
    return "\n".join(
        "<tr><td>{0}m{1}</td><td class='n'>{2:,}</td><td class='n'>{3}</td>"
        "<td class='n'>{4}%</td><td class='n'>{5}%</td><td class='n'>{6}%</td></tr>".format(
            s["반경"], " (채택)" if s["반경"] == 150 else "", s["클러스터"],
            s["재출현"], s["비율"], s["사망점유"], s["사고점유"])
        for s in R["민감도"])


HTML = """<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">
<title>__TEAM___분석보고서</title><style>__CSS__</style></head><body>

<section class="page cover">
  <div class="kick">AI와 함께하는 교통문제 해결을 위한 데이터 분석 공모전</div>
  <h1>14년째 같은 자리<br>보행 고령자 사고다발지역의 재출현 구조와<br>개선 우선순위 도출</h1>
  <div class="sub">도로교통공단 사고다발지역 6,282건(2013~2026) 전수 분석</div>
  <div class="meta">
    팀명 __TEAM__<br>팀원 __MEMBERS__<br>제출일 2026년 10월 21일<br>
    분석 코드 __REPO__
  </div>
</section>

<section class="page">
<h2>1. 분석 배경 및 목적</h2>
<div class="lead">
보행 중 사망하는 고령자의 위험 지점은 이미 좌표로 특정되어 매년 공표되고 있음.
그럼에도 <b>동일 지점이 14년간 반복 등재</b>되고 있으며, 전 기간 연속 등재 지점이 9곳 존재함.
본 분석의 문제의식은 위험의 미인지가 아니라 <b>진단과 개선 조치의 단절</b>임.
</div>

<h3>1-1. 현황</h3>
<ul>
<li>도로교통공단은 2013년부터 매년 보행노인 사고다발지역을 지정·공표하고 있으며 누적 지정은 6,282건임.</li>
<li>해당 지점의 14년 누적 피해는 사고 27,734건, 사상자 29,146명, 사망 2,000명임.</li>
<li>어린이는 <b>어린이보호구역 내 사고다발지역</b>이 별도 데이터셋으로 관리되나 노인보호구역 기준 데이터셋은 도로교통공단 개방 데이터 15종 중 부재함. 어린이는 상시 보호구역과 사고 통계가 연동 관리되는 반면 고령자는 그 연결 구조가 없음.</li>
</ul>

<h3>1-2. 문제 정의</h3>
<ul>
<li><b>누가</b>: 보행 중인 65세 이상 고령자. 승용차로 수단 대체가 어렵고, 보행 속도가 느려 횡단 중 노출 시간이 길며, 동일 충돌에서 사망 전이 확률이 높은 집단임.</li>
<li><b>어디서</b>: 도로교통공단 지정 보행노인 사고다발지역. 좌표와 폴리곤으로 이미 특정되어 있음.</li>
<li><b>무엇이 문제인가</b>: 위험 지점 목록이 매년 갱신·공개되나 동일 지점이 이듬해 재등재됨. 목록이 개선 우선순위로 전환되지 않음.</li>
</ul>

<h3>1-3. 분석 목적</h3>
<ul>
<li>사고다발지역 지정의 <b>재출현 구조</b>를 정량화하고 재출현을 좌우하는 공간적 조건을 규명해 <b>제도 공백 영역</b>을 식별함.</li>
<li>한정된 개선 재원을 배분할 <b>우선순위 지수</b>를 설계하고 지수의 우열을 표본외 예측으로 실증함.</li>
</ul>

<h3>1-4. 참여 동기</h3>
<p>공모 취지인 이동 격차는 수단의 부재만이 아니라 <b>같은 거리를 걸어도 사망 확률이 다른 상태</b>로도 나타남. 개선 대상을 특정하는 일이 이동 격차 해소의 출발점이라 판단해 본 주제를 선정함.</p>

<h2>2. 활용 데이터</h2>
<table>
<tr><th style="width:21%">활용 데이터(명)</th><th style="width:12%">제공기관(명)</th><th style="width:17%">출처 플랫폼(명)</th><th>URL</th></tr>
<tr><td>보행노인 사고다발지역<br>(주 분석 대상, 6,282행)</td><td>도로교통공단</td><td>교통사고정보 개방시스템</td><td>https://opendata.koroad.or.kr/api/down/oldmandown.jsp</td></tr>
<tr><td>보행자 사고다발지역<br>(2,402행)</td><td>도로교통공단</td><td>교통사고정보 개방시스템</td><td>https://opendata.koroad.or.kr/api/down/pedstriansdown.jsp</td></tr>
<tr><td>보행어린이 사고다발지역<br>(1,300행)</td><td>도로교통공단</td><td>교통사고정보 개방시스템</td><td>https://opendata.koroad.or.kr/api/down/childdown.jsp</td></tr>
<tr><td>어린이보호구역 내 어린이 사고다발지역(646행)</td><td>도로교통공단</td><td>교통사고정보 개방시스템</td><td>https://opendata.koroad.or.kr/api/down/schoolzonedown.jsp</td></tr>
<tr><td>자전거 사고다발지역<br>(5,305행)</td><td>도로교통공단</td><td>교통사고정보 개방시스템</td><td>https://opendata.koroad.or.kr/api/down/bicycledown.jsp</td></tr>
</table>
<p class="note">선정 이유: ① 전국 단일 출처로 지역 간 정의가 일관됨 ② 지점별 좌표와 폴리곤(GeoJSON)이 내장되어 별도 공간데이터 결합 없이 공간 분석이 가능함 ③ 2013~2026년 14년 시계열로 재출현 판정이 가능함 ④ 지점명에 인근 시설 정보가 포함되어 외부 시설 데이터 없이 공간 맥락 추출이 가능함 ⑤ 로그인·인증키 없이 공식 CSV 경로로 취득 가능하며 이용허락범위에 제한이 없음. 전량 2026년 9월 12일 수집.</p>

<h2>3. 분석과정 및 방법</h2>

<h3>3-1. 전처리에서 확인한 데이터 구조 변화</h3>
<p>동일 출처임에도 파일별·연도별 정의가 달라 보정 없이는 시계열 비교가 성립하지 않음. 세 건을 확인해 보정함.</p>
<table>
<tr><th style="width:24%">항목</th><th>확인 내용</th><th style="width:30%">처리</th></tr>
<tr><td>선정 임계 변경</td><td>지점당 최소 사고건수가 2013~2021년 2건에서 <b>2022년 5건으로 상향</b>됨. 연간 지정 지점이 507곳에서 269곳으로 감소함</td><td>재출현을 건수가 아닌 <b>목록 등재 여부</b>로 정의해 임계 변경의 영향을 차단함</td></tr>
<tr><td>대상사고 정의 변경</td><td>경상자수가 2021년 733명에서 2022년 58명으로 급감해 2025년 0명으로 수렴함. 사망·중상 중심으로 전환됨</td><td>연도 간 절대 비교를 배제하고 지점 단위 누적값으로만 비교함</td></tr>
<tr><td>행정구역 개편</td><td>2023년 강원도·전라북도의 특별자치도 전환, 2026년 전라남도·광주광역시 통합이 표기에 반영됨. 시도명이 정식·약칭 혼용됨</td><td>2026년 기준 16개 시도로 정규화함</td></tr>
</table>
<p class="note">부수 확인: 5개 파일 중 어린이보호구역 파일만 UTF-8이고 나머지는 CP949임. 파일별 인코딩 자동 판별 로직을 적용함.</p>

<h3>3-2. 동일 지점 판정</h3>
<ul>
<li>지점 좌표가 연도마다 재산출되어 미세하게 이동하므로 좌표 일치로는 재출현 판정이 불가함.</li>
<li><b>단일 연결 클러스터링</b>으로 <b>150m</b> 이내 지점을 동일 지점으로 병합함. 원자료 6,282건이 3,094곳으로 정리됨.</li>
<li>반경 근거: 사고다발지역 폴리곤 반경이 약 100m 규모이므로 인접한 두 원의 중심 간 거리를 허용하는 값으로 설정함.</li>
<li>민감도: 100~250m 전 구간에서 소수 지점 집중이라는 결론 방향이 동일함. 재출현 비율만 13.0%에서 27.0%로 변동함.</li>
</ul>
<p class="note">반경별 결과: 100m 3,689곳 중 480곳(13.0%, 사망 35.1%) · <b>150m 3,094곳 중 577곳(18.6%, 사망 46.0%, 채택)</b> · 200m 2,654곳 중 627곳(23.6%, 사망 54.6%) · 250m 2,316곳 중 626곳(27.0%, 사망 61.4%).</p>

<h3>3-3. 분석 절차</h3>
<ul>
<li><b>1단계 재출현 판정</b>: 지점별 등재 연도 수를 산출하고 3개 연도 이상을 재출현으로 정의함(관측 14년 기준 상위 약 5분의 1).</li>
<li><b>2단계 피해 집중 검정</b>: 재출현 지점과 단발 지점의 지점당 누적 사망자를 맨휘트니 U 검정으로 비교함.</li>
<li><b>3단계 공간 맥락 추출</b>: 지점명 텍스트에서 시설 키워드를 단일 배정 규칙으로 분류하고 유형별 재출현율을 카이제곱 검정으로 비교함. 우선순위 배정으로 중복 계상을 차단함.</li>
<li><b>4단계 우선순위 지수 설계와 검증</b>: 후보 지수 8종을 구성한 뒤 <b>시간 분할 검증</b>으로 표본외 예측력을 비교함. 학습 구간으로 순위를 만들고 검증 구간의 실제 사망자를 얼마나 포착하는지 측정함. 분할 지점을 2019~2023년까지 5회 이동해 견고성을 확인함.</li>
</ul>

<h2>4. AI 기술 활용</h2>
<table>
<tr><th style="width:20%">단계</th><th style="width:16%">사용 서비스</th><th>활용 범위와 주요 프롬프트</th></tr>
<tr><td>데이터 탐색</td><td>Claude<br>(Anthropic)</td><td>개방 포털의 CSV 직통 경로 탐색과 컬럼 구조 파악. 주요 프롬프트: "도로교통공단 개방시스템에서 로그인 없이 내려받을 수 있는 사고다발지역 CSV 경로를 찾고 컬럼 구성과 인코딩을 확인해 줘"</td></tr>
<tr><td>전처리 설계</td><td>Claude</td><td>연도별 집계값 대조를 통한 정의 변화 탐지. 주요 프롬프트: "연도별 사상자·사망·중상·경상 합계를 대조해 선정 기준이 바뀐 시점을 특정해 줘"</td></tr>
<tr><td>분석 설계·구현</td><td>Claude</td><td>재출현 판정 방식과 지수 후보 구성 검토, 클러스터링·시간분할 검증·시각화 스크립트 구현. 주요 프롬프트: "좌표가 매년 재산출되는 지점 데이터에서 동일 지점을 판정하는 방법과 반경 민감도 검증 설계를 제안해 줘", "위도 정렬 밴드 탐색으로 O(n·k) 단일 연결 클러스터링을 구현해 줘"</td></tr>
<tr><td>결과 검증</td><td>Claude</td><td>산출 수치의 재계산 대조 및 해석 반례 점검. 주요 프롬프트: "이 결과가 단순히 통행량이 많은 곳을 잡아낸 것에 불과하다는 반론에 어떻게 답할 수 있는지 점검해 줘"</td></tr>
</table>
<p class="note">AI가 생성한 코드와 수치는 전량 원본 CSV로 재계산해 대조함. 개인정보·비공개 자료를 외부 AI 서비스에 입력하지 않았으며 사용 데이터는 전량 공개 데이터임. 지수 채택과 최종 해석은 분석자가 수행함.</p>

<h2>5. 분석 내용 및 결과</h2>
<div class="kpi">
  <div><b>577곳</b><span>3개 연도 이상 재출현<br>전체 3,094곳의 18.6%</span></div>
  <div><b>46.0%</b><span>재출현 지점이 점유한<br>14년 누적 사망자 비중</span></div>
  <div><b>9곳</b><span>2013~2026년<br>전 기간 연속 등재</span></div>
  <div><b>10.0 : 53.7</b><span>학교 인근 대 전통시장 인근<br>재출현율(%)</span></div>
</div>

<h3>5-1. 위험은 특정 지점에 고정되어 있음</h3>
<p>3,094곳 중 <b>577곳(18.6%)</b>이 3개 연도 이상 반복 등재됨. 14년 전 기간 연속 등재 지점이 9곳이며,
최다 지점인 여수시 교동 여객선터미널입구교차로는 누적 사망 26명, 사고 234건을 기록함.</p>
<div class="fig"><img src="__FIG1__"></div>
<p class="cap">회색 점은 전체 지점, 강조 점은 각 범주. 재출현 지점은 수도권·부산권과 남동 해안권에 집중됨.</p>

<h3>5-2. 재출현 지점에 피해가 집중됨</h3>
<p>재출현 지점의 지점당 누적 사망자는 <b>1.59명</b>으로 단발 지점 0.38명의 <b>4.2배</b>임(맨휘트니 U 검정, p&lt;0.001).
전체 지점의 18.6%가 누적 사망자의 46.0%, 사고의 59.7%를 점유함.</p>
<div class="fig"><img src="__FIG2__"></div>
<p class="cap">재출현 지점 577곳이 각 피해 지표에서 차지하는 비중. 지점 수 비중 대비 사망자 비중이 2.5배임.</p>

<h3>5-3. 상시 보호 제도의 유무가 재출현율을 가름</h3>
<p>지점명에서 추출한 시설 유형별 재출현율이 유형에 따라 크게 갈림(카이제곱 295.2, 자유도 9, p&lt;0.001).
<b>어린이보호구역이 상시 적용되는 학교 인근은 10.0%</b>로 전체 기준선 18.6%를 밑도는 반면,
<b>고령자 통행이 밀집하지만 대응 규제 공간이 없는 전통시장 인근은 53.7%</b>로 기준선의 약 3배임
(피셔 정확검정 오즈비 10.4, p&lt;0.001).</p>
<div class="fig"><img src="__FIG3__"></div>
<p class="cap">n은 해당 유형으로 분류된 지점 수. 20곳 미만 유형과 잔여 범주는 제외함.</p>
<p class="note">해석 주의: 약국은 국내 지점 표기 관행상 근린 상업지의 대리 지표로 기능함. 약국 자체를 위험 요인으로 해석하지 않으며 전통시장과 함께 <b>고령자 생활 동선이 집중되는 근린 상업지</b>로 판독함.</p>

<h3>5-4. 우선순위 지수는 직관과 반대로 작동함</h3>
<p>개선 대상 선정에 가장 직관적인 기준은 누적 사망자임. 그러나 <b>시간 분할 검증 결과 이 기준이 8개 후보 중 최하위</b>였음.
학습 구간으로 순위를 만들고 검증 구간의 실제 사망자를 얼마나 포착하는지 측정했으며 분할 지점을 5회 이동해 확인함.</p>
<div class="fig"><img src="__FIG4__"></div>
<p class="cap">왼쪽은 상위 300곳 선정 시 검증 구간 사망자 커버율(5개 분할 평균, 2019~2023년 경계). 오른쪽은 2013~2021년 자료로 순위를 만들고 2022~2026년 실측으로 검증한 커버율 곡선.</p>
<ul>
<li>누적 사망자 정렬은 평균 <b>47.3%</b>로 전 분할에서 최하위였음. 사망은 희소 사건이라 과거 사망자 수가 미래 위험의 노이즈 큰 대리변수로 작동함.</li>
<li>채택 지수인 <b>지속위험지수(PRI) = 누적 사상자수 × 지속성</b>이 평균 <b>63.6%</b>로 최상위였음. 지속성은 등재 연도 수를 관측 연도 수로 나눈 값임.</li>
</ul>

<h3>5-5. 개선 대상 300곳 선정 시나리오</h3>
<table>
<tr><th>선정 기준</th><th class="n">검증 구간 사망자 커버</th><th class="n">검증 구간 사고 커버</th><th class="n">무작위 대비</th></tr>
<tr><td><b>지속위험지수 PRI (채택)</b></td><td class="n"><b>67.2%</b> (221/329명)</td><td class="n"><b>66.4%</b></td><td class="n">6.5배</td></tr>
<tr><td>누적 사망자 정렬</td><td class="n">48.0% (158/329명)</td><td class="n">37.4%</td><td class="n">4.7배</td></tr>
<tr><td>무작위 선택</td><td class="n">10.3%</td><td class="n">—</td><td class="n">1.0배</td></tr>
</table>
<p>동일하게 300곳을 개선하더라도 선정 기준에 따라 예방 가능 범위가 <b>19.2%p</b> 달라짐. 검증 구간 실측으로는 사망자 63명분의 차이임.</p>

<p class="note">PRI 상위 300곳의 평균 등재 연도는 7.1년이며, 이 중 <b>119곳(39.7%)</b>이 전통시장 또는 약국 인근, 즉 근린 상업지에 위치함. 최우선 8곳 목록은 부록 참조.</p>


<h2>6. 정책제안 및 기대효과</h2>

<h3>6-1. 제안 1. 노인보호구역 지정 우선순위를 지속위험지수 기반으로 전환</h3>
<ul>
<li><b>적용 대상</b>: 지방자치단체 교통행정 부서와 관할 경찰서. 노인보호구역 지정 권한 주체임.</li>
<li><b>내용</b>: 지정 후보지 선정 시 누적 사망자 대신 <b>사상자 빈도와 등재 지속성을 결합한 지수</b>를 적용함.</li>
<li><b>정량 기대효과</b>: 동일하게 300곳을 지정할 때 향후 5년 사망자 포착 범위가 <b>48.0%에서 67.2%로 19.2%p 상승</b>함. 검증 구간 실측 기준 <span class="hl">사망자 63명분의 차이</span>이며 추가 재원 없이 선정 기준 변경만으로 달성됨.</li>
<li><b>실행 절차</b>: ① 도로교통공단이 공표하는 사고다발지역 목록에 지점 식별자와 지속성 지표를 병기 ② 지자체가 관할 상위 지점을 지정 검토 대상으로 접수 ③ 현장 실사 후 지정 또는 대체 조치 시행</li>
</ul>

<h3>6-2. 제안 2. 근린 상업지를 노인보호구역 지정 대상 공간에 명시</h3>
<ul>
<li><b>근거</b>: 학교 인근 재출현율 10.0%와 전통시장 인근 53.7%의 격차는 상시 보호구역 제도의 적용 여부와 일치함. 제도가 작동하는 공간에서는 반복 위험이 억제됨.</li>
<li><b>내용</b>: 노인복지시설 중심의 현행 지정 관행에 <b>전통시장·상설시장과 근린 상업가로</b>를 명시적으로 추가함. 고령자 통행의 실제 발생원을 반영하는 조치임.</li>
<li><b>정량 기대효과</b>: PRI 상위 300곳 중 119곳이 해당 공간에 위치하므로 이 유형만 우선 처리해도 최우선 대상의 39.7%를 포괄함.</li>
</ul>

<h3>6-3. 제안 3. 재출현 지표의 연례 공표</h3>
<ul>
<li><b>내용</b>: 사고다발지역 공표 시 <b>연속 등재 연수</b>를 함께 공개함. 현행 공표는 당해 연도 단면만 제공해 지점의 만성 여부를 판별할 수 없음.</li>
<li><b>기대효과</b>: 개선 조치가 이뤄진 지점이 목록에서 이탈하는지 추적 가능해져 진단과 조치의 단절이 해소됨. 지자체 간 개선 성과 비교의 공통 척도로도 기능함.</li>
<li><b>구현 비용</b>: 신규 데이터 수집이 불필요함. 기존 공표 자료에 지점 식별자를 부여하는 수준으로 산출 가능함.</li>
</ul>

<h3>6-4. 탄소중립 기여 경로</h3>
<p>수송부문 온실가스의 약 97%가 도로교통에서 발생하며 감축은 통행의 수단 전환에 좌우됨.
고령자의 근거리 통행은 보행 의존도가 높으나 보행 환경이 위험할수록 택시와 자가용 동승으로 전환됨.
본 분석이 특정한 577개 지점은 <b>고령자 보행 이탈이 집중적으로 발생하는 지점</b>이며 개선 시
근거리 통행의 보행 분담률 유지에 기여함.</p>
<p class="note">정량 환산 유보: 지점별 통행량과 수단 전환 탄력성 자료를 확보하지 못해 감축량을 산정하지 않음. 통행량 자료 확보 시 지점별 보행 통행 유지량과 전환 계수를 곱해 산출 가능하며 이를 후속 과제로 제시함. 근거 없는 수치 제시를 지양하고 경로만 제시함.</p>

<h3>6-5. 확장 가능성</h3>
<ul>
<li>분석에 사용한 데이터는 <b>전국 단일 출처</b>이므로 동일 절차를 모든 지자체에 그대로 적용 가능함. 지역별 별도 데이터 수집이 불필요함.</li>
<li>동일 방법론을 보행자 전체·보행 어린이·자전거 데이터셋에 적용 가능하며(동일 스키마), 보행량·시설·도로 속성 자료를 결합하면 노출량 보정 모형으로 확장 가능함.</li>
</ul>

<h3>6-6. 한계</h3>
<ul>
<li><b>노출량 미보정</b>: 재출현 지점이 통행량이 많은 지점일 가능성을 본 데이터만으로 배제할 수 없음. 본 분석의 주장은 위험의 원인 규명이 아니라 <b>위험의 공간적 고정성과 그에 따른 우선순위</b>임.</li>
<li><b>시설 분류의 대리성</b>: 지점명 키워드는 실제 시설 위치 데이터가 아닌 표기 관행에 의존함. 시설 위치 데이터 결합 시 재검증이 필요함.</li>
<li><b>개입 효과 미검증</b>: 본 분석은 개선 대상 선정 기준의 우열을 검증했을 뿐 보호구역 지정 자체의 사고 저감 효과를 인과적으로 추정하지 않음. 지정 전후 비교는 별도 설계가 필요함.</li>
</ul>
</section>

<section class="page">
<h2>7. 분석도구 및 참고문헌</h2>
<h3>7-1. 분석 도구</h3>
<ul>
<li>Python 3.14, pandas 3.0, NumPy 2.5, SciPy 1.18, Matplotlib 3.11</li>
<li>분석 코드 전문: __REPO__</li>
<li>구성: 전처리·클러스터링(pipeline.py), 가설 검정(analysis.py), 지수 검증(validate.py), 시각화(figures.py), 보고서 생성(build_report.py)</li>
<li>재현 방법: 저장소의 download_data.py로 원본 CSV를 재수집한 뒤 run_all.py 실행. 난수 시드는 42로 고정함.</li>
</ul>
<h3>7-2. 데이터 출처</h3>
<ul>
<li>도로교통공단, 교통사고정보 개방시스템, 보행노인·보행자·보행어린이·어린이보호구역내·자전거 사고다발지역, https://opendata.koroad.or.kr, 2026년 9월 12일 수집.</li>
<li>공공데이터포털, 한국도로교통공단 보행자 교통사고 다발지역, https://www.data.go.kr/data/15105289/openapi.do, 이용허락범위 제한 없음 확인.</li>
</ul>
<h3>7-3. 참고 자료</h3>
<ul>
<li>행정안전부 통합데이터분석센터, 인공지능 기반 데이터분석으로 교통약자 이동권 획기적 강화, 보도자료, 2023년 10월 16일.</li>
<li>서울특별시, 2025 서울시 빅데이터캠퍼스 공모전 결과, https://news.seoul.go.kr/gov/archives/572845.</li>
<li>재단법인 숲과나눔, AI와 함께하는 교통문제 해결을 위한 데이터 분석 공모전 공고, https://koreashe.org/notice/?uid=95427.</li>
</ul>
<h3>7-4. 산출 데이터</h3>
<ul>
<li>전처리 결과(6,282행), 지점별 지표(3,094곳), 우선순위 전체 순위, 최우선 30곳, 가설 검정 결과, 지수 검증 결과를 저장소 outputs 폴더에 수록함.</li>
</ul>

<h3>7-5. 부록: 최우선 개선 대상 8곳</h3>
<p>지속위험지수(PRI) 상위 8곳임. 전체 3,094곳의 지수와 순위는 저장소 <code>outputs/04_우선순위_전체.csv</code>에 수록함.</p>
<table>
<tr><th class="n" style="width:6%">순위</th><th>지점명</th><th style="width:13%">시설유형</th><th class="n" style="width:9%">등재연도</th><th class="n" style="width:8%">사망</th><th class="n" style="width:8%">사고</th><th class="n" style="width:8%">PRI</th></tr>
__TOP__
</table>
<p class="note">전체 3,094곳의 지수와 순위는 분석 코드 저장소의 결과 파일에 수록함.</p>
</section>

</body></html>"""

HTML = (HTML.replace("__CSS__", CSS).replace("__TEAM__", TEAM)
            .replace("__MEMBERS__", MEMBERS).replace("__REPO__", REPO)
            .replace("__SENS__", rows_sens()).replace("__TOP__", rows_top(8))
            .replace("__FIG1__", img("fig1_분포지도.png"))
            .replace("__FIG2__", img("fig2_피해집중.png"))
            .replace("__FIG3__", img("fig3_시설유형.png"))
            .replace("__FIG4__", img("fig4_지수검증.png"))
)

path_html = os.path.join(OUT, TEAM + "_분석보고서.html")
with open(path_html, "w", encoding="utf-8") as f:
    f.write(HTML)
print("HTML:", path_html, "%.0fKB" % (os.path.getsize(path_html) / 1024))
