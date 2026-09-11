# -*- coding: utf-8 -*-
"""참가신청서 HTML 생성 (공식 붙임1 양식 내용을 그대로 옮김)
서명과 개인정보는 인쇄 후 자필 기재 -> 스캔 PDF로 제출한다.
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))
TEAM = "청신호"

CSS = """
@page { size: A4; margin: 16mm 16mm 14mm 16mm; }
* { box-sizing: border-box; }
body { font-family: Pretendard, 'Malgun Gothic', sans-serif; color:#111;
       font-size: 9.1pt; line-height: 1.55; margin:0; -webkit-print-color-adjust: exact; }
.page { page-break-after: always; }
.page:last-child { page-break-after: auto; }
.hd { text-align:center; margin-bottom: 7mm; }
.hd .kick { font-size:9.4pt; color:#333; }
.hd h1 { font-size: 18pt; margin: 3mm 0 0; letter-spacing: 6px; }
h2 { font-size: 10.4pt; margin: 5mm 0 2mm; padding: 1.2mm 2mm; background:#EDEFF2;
     border-left: 3px solid #111; }
table { width:100%; border-collapse: collapse; font-size: 9pt; margin-bottom: 2mm; }
th, td { border: .8px solid #666; padding: 2.1mm 2mm; vertical-align: middle; }
th { background:#F2F4F6; font-weight:600; text-align:center; }
td.c { text-align:center; }
ol { padding-left: 5mm; margin: 1mm 0 2mm; }
ol li { margin-bottom: 1mm; }
ul { padding-left: 4.5mm; margin: 1mm 0 2mm; }
p { margin: 0 0 1.6mm; }
.chk { font-size: 10pt; letter-spacing: .5px; }
.agree { border:.8px solid #666; padding: 2.2mm 3mm; margin: 2mm 0 3mm; text-align:center; font-size:9.4pt; }
.sub { font-size: 8.2pt; color:#444; }
.sign { margin-top: 6mm; page-break-before: always; }
.sign .date { text-align:center; font-size:10.4pt; margin: 6mm 0 7mm; letter-spacing:1px; }
.sign table td { padding: 4.2mm 2mm; }
.fill { color:#999; }
.note { font-size:8pt; color:#555; margin-top:2mm; }
"""

HTML = """<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">
<title>__TEAM___참가신청서</title><style>__CSS__</style></head><body>

<section class="page">
<div class="hd">
  <div class="kick">- AI와 함께하는 교통문제 해결을 위한 데이터 분석 공모전 -</div>
  <h1>참가신청서</h1>
</div>

<h2>[참가자 정보]</h2>
<table>
<tr><th style="width:18%">지원형태</th><td colspan="4" class="chk">□ 개인 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ■ 팀</td></tr>
<tr><th>신청자명</th><td colspan="4"><b>__TEAM__</b> <span class="sub">※ 팀일 경우 팀명 기재</span></td></tr>
<tr><th>구분</th><th style="width:20%">이름</th><th style="width:22%">소속</th><th style="width:22%">이메일</th><th>연락처</th></tr>
<tr><td class="c">대 표</td><td></td><td></td><td></td><td></td></tr>
<tr><td class="c">팀원1</td><td></td><td></td><td></td><td></td></tr>
<tr><td class="c">팀원2</td><td></td><td></td><td></td><td></td></tr>
</table>

<h2>[개인정보 수집·이용]</h2>
<p>(재)숲과나눔 풀씨행동연구소와 한겨레신문은 본 공모전 운영을 위하여 「개인정보 보호법」 제15조, 제22조에 따라
아래와 같이 개인정보를 수집·이용하고자 하며, 이에 대한 동의를 받고자 합니다.</p>
<ol>
<li>수집·이용 주체 : (재)숲과나눔 풀씨행동연구소</li>
<li>수집·이용 목적
  <ul><li>신청·접수 및 자격 확인, 신청자 관리 등 공모전 관련 업무</li>
      <li>진행 안내, 결과 통지, 홍보 및 고지 등 운영에 필요한 연락</li></ul></li>
<li>수집 항목 : 성명, 소속, 이메일, 연락처 등 개인식별 정보</li>
<li>보유·이용 기간 : 수집일로부터 2년(기간 경과 후 지체없이 파기. 단, 관계 법령에 따라 보존이 필요한 경우 해당 법령이 정한 기간)</li>
<li>제3자 제공 : 수집된 개인정보는 정보주체의 별도 동의가 있거나 법령에 근거가 있는 경우를 제외하고 제3자에게 제공하지 않습니다.</li>
<li>동의 거부 권리 : 개인정보 수집·이용에 대한 동의를 거부할 권리가 있습니다. 다만 위 항목은 공모전 접수·운영에 필수적인 정보이므로, 동의하지 않을 경우 참가가 제한될 수 있습니다.</li>
</ol>
<div class="agree">개인정보 수집·이용에 동의하십니까? &nbsp;&nbsp;&nbsp;&nbsp; □ 동의함 &nbsp;&nbsp;&nbsp;&nbsp; □ 동의하지 않음</div>
</section>

<section class="page">
<h2>[공모전 규정 및 준수사항]</h2>
<p>본인은 아래 규정을 성실히 준수하며, 허위 기재 등으로 인한 모든 책임은 본인에게 있음을 확인합니다.</p>
<ol>
<li>참가자는 저작권 문제가 해결된 데이터·도구만 사용합니다.</li>
<li>결과물 제작에 사용하는 모든 소스의 사용권을 사전에 확인해야 하며, 이용 가능 여부를 참가자 본인이 입증합니다.</li>
<li>응모작의 저작권은 참가자에게 귀속되며, 저작권과 관련된 민·형사상 책임 또한 참가자에게 있습니다.</li>
<li>데이터 이용과 관련하여 아래 사항에 동의합니다.
  <ul><li>기존 콘텐츠의 표절(자기표절 포함), 타인(또는 업체)의 대리 제작 사례를 출품하지 않았으며, 동일·유사 사례를 타 공모전에 출품한 사실이 없습니다.</li>
      <li>저작권 침해, 도용, 모방, 표절, 대리(대행) 제작, 타 공모전 출품 등 불공정 행위가 확인될 경우 수상 이후라도 수상을 취소하며, 상금을 전액 반환합니다.</li>
      <li>추후 논문·출판물 등 본 공모전 제공 데이터로부터 성과물이 발생한 경우, 반드시 데이터 출처를 명시합니다.</li></ul></li>
<li>심사점수는 비공개로 합니다.</li>
<li>팀으로 수상하는 경우 상금은 대표자에게 지급되며, 분배는 팀원 간 협의 사항으로 주최 측은 관여하지 않습니다.</li>
<li>상금은 제세공과금 공제 후 지급됩니다.</li>
<li>주최 및 공동주최 기관은 수상작에 한하여 정책 수립·개선, 전시, 홍보, 보도, 교육 등 비영리·공익 목적 범위에서 수상작을 비독점적으로 이용(게시·전시·복제·배포·전송)할 수 있으며, 이용 시 참가자(팀)의 성명을 표시합니다. 이용 기간은 공모전 종료 후 3년으로 하며, 공모전 결과 기록·아카이브 목적의 홈페이지 게시는 그 이후에도 유지할 수 있습니다. 참가자는 수상 이후에도 자신의 응모작을 자유롭게 이용할 수 있습니다. 응모자는 공개된 아이디어 자체는 법적으로 보호받기 어려울 수 있음을 인지하고, 필요한 저작권 또는 지식재산권을 사전에 확보합니다.</li>
<li>수상자는 최종 제출물을 주최 측에 제출하고, 숲과나눔 홈페이지 등 공개에 동의하며, 결과물 활용 및 공개를 위한 요청에 협조합니다.</li>
<li>본 공모전에 제출된 모든 서류는 일체 반환되지 않습니다.</li>
<li>수상 이후라도 타 유사 행사 기수상 사실이 확인되거나, 타인의 지식재산권을 침해한 경우 수상을 취소하고 상금을 회수합니다.</li>
<li>적합한 결과가 없는 경우 수상자를 선정하지 않을 수 있으며, 수상 내역은 조정될 수 있습니다.</li>
<li>수상자는 상금 지급 및 제세공과금 원천징수 등 관계 법령상 의무 이행에 필요한 정보와 서류(성명, 주민등록번호, 계좌 정보 등)를 수상 확정 후 주최 측이 안내하는 별도 서식으로 제출합니다. 해당 정보는 목적 달성 또는 법정 보존기간 경과 후 지체없이 파기합니다.</li>
<li>기타 사항은 주최 측 결정에 따릅니다.</li>
</ol>
</section>

<section class="page">
<h2>[데이터 수집·활용 및 분석 시 준수사항]</h2>
<p><b>○ 데이터의 수집 및 이용</b></p>
<ol>
<li>참가자는 데이터를 적법한 방법으로 수집·취득해야 하며, 데이터 제공기관 또는 서비스의 이용약관, 라이선스, 계약조건 및 별도의 이용허락 범위를 준수해야 합니다.</li>
<li>데이터에 접근하거나 비용을 지불하여 구매했다는 사실만으로 해당 데이터를 자유롭게 복제·공개·재배포하거나 제3자에게 제공할 수 있는 것은 아닙니다. 참가자는 공모전 출품, 분석 결과 공개 및 주최기관의 공익적 활용이 허용되는지 사전에 확인해야 합니다.</li>
<li>참가자는 데이터의 출처, 제공기관 또는 수집 주체, 수집·취득 방법, 수집기간 또는 기준시점, 주요 변수와 이용조건을 결과물에 밝혀야 합니다.</li>
<li>접근권한 우회, 무단 계정 사용, 이용약관에 위배되는 자동수집 또는 크롤링 등 부적절한 방법으로 데이터를 수집해서는 안 됩니다.</li>
<li>주최 측이 요청하는 경우 참가자는 데이터의 적법한 취득 및 이용권한을 확인할 수 있는 자료를 제출해야 합니다.</li>
</ol>
<p><b>○ 민간데이터 이용</b></p>
<ol>
<li>기업, 기관, 플랫폼 또는 개인이 보유한 민간데이터를 활용하는 경우, 데이터 분석·가공과 공모전 출품, 분석 결과 공개가 허용되는 범위에서만 사용해야 합니다.</li>
<li>영업비밀, 기업 내부자료, 비밀유지의무가 적용되는 자료 또는 외부 공개가 제한된 데이터는 권리자의 명시적인 허락 없이 사용하거나 제출해서는 안 됩니다.</li>
<li>민간데이터의 저작권, 데이터베이스제작자의 권리 및 이용조건을 확인해야 하며, 데이터의 전부 또는 상당 부분을 허락 없이 복제·배포해서는 안 됩니다.</li>
</ol>
<p><b>○ 시민과학 데이터 및 직접 수집 데이터 이용</b></p>
<ol>
<li>참가자가 직접 관찰·조사·측정·설문·사진촬영 등을 통해 데이터를 수집하는 경우 관련 법령을 준수하고, 개인정보·위치정보 및 사생활을 침해하지 않도록 해야 합니다. 필요한 경우 조사 대상자의 동의를 받아야 합니다.</li>
<li>직접 수집하거나 시민과학 플랫폼 등을 통해 확보한 데이터는 수집 주체·방법·기간·지역 등 주요 정보를 밝히고, 해당 데이터의 이용조건과 라이선스를 준수해야 합니다.</li>
</ol>
<p><b>○ AI 활용</b></p>
<ol>
<li>AI를 이용하여 데이터를 수집·정제·분석하거나 결과물을 작성한 경우에는 사용한 AI 서비스, 활용 범위와 주요 프롬프트를 밝혀야 합니다. 다만 맞춤법 검사, 단순 번역, 문장 교정 등 결과에 실질적인 영향을 미치지 않는 단순 이용은 제외할 수 있습니다.</li>
<li>AI를 사용하여 생성·보완한 데이터와 분석 결과는 참가자가 직접 검증해야 하며, 오류, 편향 또는 허위 정보 생성 가능성을 확인해야 합니다.</li>
<li>개인정보, 개인위치정보, 영업비밀, 비공개 자료 또는 외부 전송이 제한된 데이터를 외부 AI 서비스에 입력해서는 안 됩니다.</li>
<li>데이터를 AI 서비스에 입력하는 경우 해당 서비스의 데이터 저장, 학습 활용, 재이용 및 제3자 제공 조건을 사전에 확인해야 합니다.</li>
<li>특정 AI 서비스나 프로그램을 사용해야만 결과를 확인할 수 있는 경우, 심사 및 향후 활용 과정에서 과도한 비용이나 개인정보 제공 등 특별한 이용 제약이 없어야 합니다.</li>
</ol>
<p><b>○ 데이터 보관 및 책임</b></p>
<ol>
<li>개인정보와 비공개 데이터는 분석 목적 달성 후 관계 법령 또는 이용계약에 따라 보관해야 하는 경우를 제외하고 안전하게 삭제해야 합니다.</li>
<li>데이터 이용과 관련한 저작권, 개인정보, 초상권, 영업비밀, 이용약관 및 라이선스 위반 등에 대한 책임은 참가자에게 있습니다.</li>
<li>데이터의 무단 수집·이용·제공, 허위 데이터 작성, 분석 결과 조작 또는 개인정보 침해 등이 확인된 경우 주최 측은 심사 대상에서 제외할 수 있습니다.</li>
<li>위반 사실이 수상 이후 확인된 경우에도 수상을 취소하고 상금을 회수할 수 있습니다.</li>
</ol>
<div class="agree">위 [공모전 규정 및 준수사항]과 [데이터 수집·활용 및 분석 시 준수사항]을 확인하였으며<br>
이를 준수할 것을 서약하십니까? &nbsp;&nbsp;&nbsp;&nbsp; □ 동의함 &nbsp;&nbsp;&nbsp;&nbsp; □ 동의하지 않음</div>

<div class="sign">
<h2>[서약 및 서명]</h2>
<p>상기 본인(개인 또는 팀장) 및 팀원 전원은 위 각 항목에 대한 동의·서약 내용에 따라 본 공모전에 참가를 확인합니다.</p>
<div class="date">2026년 &nbsp;&nbsp;&nbsp;&nbsp; 월 &nbsp;&nbsp;&nbsp;&nbsp; 일</div>
<table>
<tr><td style="width:16%" class="c">이름(대 표)</td><td style="width:34%"></td><td style="width:12%" class="c">서명</td><td></td></tr>
<tr><td class="c">이름(팀원1)</td><td></td><td class="c">서명</td><td></td></tr>
<tr><td class="c">이름(팀원2)</td><td></td><td class="c">서명</td><td></td></tr>
</table>
</div>
</section>

</body></html>"""

HTML = HTML.replace("__CSS__", CSS).replace("__TEAM__", TEAM)
path = os.path.join(OUT, TEAM + "_참가신청서.html")
with open(path, "w", encoding="utf-8") as f:
    f.write(HTML)
print("HTML:", path)
