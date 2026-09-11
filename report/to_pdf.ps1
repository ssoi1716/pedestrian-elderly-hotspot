param([string]$Html, [string]$Pdf)
$tmp = "C:\Users\user\AppData\Local\Temp\claude\rpt"
New-Item -ItemType Directory -Force $tmp | Out-Null
Copy-Item $Html "$tmp\report.html" -Force
$exe = "C:\Program Files\Google\Chrome\Application\chrome.exe"
$stamp = Get-Date -Format "HHmmssfff"
$out = "$tmp\r_$stamp.pdf"
$a = @("--headless=new","--disable-gpu","--no-first-run","--no-default-browser-check",
  "--no-pdf-header-footer","--virtual-time-budget=25000",
  "--print-to-pdf=$out","--user-data-dir=$tmp\prof_$stamp",
  "file:///C:/Users/user/AppData/Local/Temp/claude/rpt/report.html")
$p = Start-Process -FilePath $exe -PassThru -NoNewWindow -ArgumentList $a
$p | Wait-Process -Timeout 150 -ErrorAction SilentlyContinue
if (Test-Path $out) {
  Copy-Item $out $Pdf -Force
  $s = [System.Text.Encoding]::ASCII.GetString((Get-Content $Pdf -Raw -Encoding Byte))
  "페이지 {0} | {1:N0} KB | {2}" -f ([regex]::Matches($s,'/Type\s*/Page[^s]').Count), ((Get-Item $Pdf).Length/1KB), $Pdf
} else { "PDF 생성 실패" }
