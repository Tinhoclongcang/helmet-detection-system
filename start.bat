@echo off
title He Thong Giam Sat - THCS Go Den
color 0A
echo.
echo ========================================
echo   HE THONG GIAM SAT MU BAO HIEM
echo   TRUONG THCS GO DEN
echo ========================================
echo.
echo [1/3] Kiem tra thu vien...
python -c "import flask, cv2, ultralytics; print('OK: Tat ca thu vien da san sang')" 2>nul
if errorlevel 1 (
    echo [LOI] Chua cai dat thu vien!
    echo Chay lenh: pip install flask opencv-python ultralytics
    pause
    exit /b 1
)
echo.

echo [2/3] Kiem tra model...
if not exist "best.pt" (
    echo [LOI] Khong tim thay file best.pt
    pause
    exit /b 1
)
echo OK: Model da san sang
echo.

echo [3/3] Khoi dong server...
echo.
echo ========================================
echo   SERVER DANG CHAY
echo ========================================
echo.
echo Truy cap: http://localhost:5000
echo Debug:    http://localhost:5000/debug
echo.
echo Nhan CTRL+C de dung server
echo ========================================
echo.

python app.py

pause
