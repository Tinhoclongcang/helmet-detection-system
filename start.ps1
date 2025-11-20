# Script khoi dong he thong
Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  HE THONG GIAM SAT MU BAO HIEM" -ForegroundColor Green
Write-Host "  TRUONG THCS GO DEN" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "[1/3] Kiem tra thu vien..." -ForegroundColor Yellow
try {
    python -c "import flask, cv2, ultralytics" 2>$null
    Write-Host "OK: Tat ca thu vien da san sang`n" -ForegroundColor Green
} catch {
    Write-Host "[LOI] Chua cai dat thu vien!" -ForegroundColor Red
    Write-Host "Chay lenh: pip install flask opencv-python ultralytics" -ForegroundColor Yellow
    Read-Host "Nhan Enter de thoat"
    exit 1
}

Write-Host "[2/3] Kiem tra model..." -ForegroundColor Yellow
if (!(Test-Path "best.pt")) {
    Write-Host "[LOI] Khong tim thay file best.pt`n" -ForegroundColor Red
    Read-Host "Nhan Enter de thoat"
    exit 1
}
Write-Host "OK: Model da san sang`n" -ForegroundColor Green

Write-Host "[3/3] Khoi dong server..." -ForegroundColor Yellow
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  SERVER DANG CHAY" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nTruy cap: " -NoNewline; Write-Host "http://localhost:5000" -ForegroundColor Yellow
Write-Host "Debug:    " -NoNewline; Write-Host "http://localhost:5000/debug" -ForegroundColor Yellow
Write-Host "`nNhan CTRL+C de dung server" -ForegroundColor Red
Write-Host "========================================`n" -ForegroundColor Cyan

# Mo trinh duyet tu dong
Start-Sleep -Seconds 2
Start-Process "http://localhost:5000"

# Chay server
python app.py
