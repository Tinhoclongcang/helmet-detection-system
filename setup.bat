@echo off
chcp 65001 >nul
color 0A

echo.
echo ========================================
echo   CHUONG TRINH CAI DAT TU DONG
echo   HE THONG GIAM SAT MU BAO HIEM
echo ========================================
echo.

echo [1/4] Kiem tra Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] LOI: Python chua duoc cai dat!
    echo     Hay tai Python 3.11.9 tu: https://www.python.org/downloads/
    echo     Nho tick chon "Add Python to PATH"
    pause
    exit /b 1
)
python --version
echo [OK] Python da san sang

echo.
echo [2/4] Kiem tra pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [X] LOI: pip khong hoat dong!
    pause
    exit /b 1
)
echo [OK] pip da san sang

echo.
echo [3/4] Cai dat cac thu vien...
echo     (Co the mat 5-10 phut tuy toc do mang)
echo.
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [X] LOI: Cai dat thu vien that bai!
    pause
    exit /b 1
)
echo [OK] Cac thu vien da duoc cai dat

echo.
echo [4/4] Kiem tra model AI...
if not exist "best.pt" (
    echo [X] LOI: Khong tim thay file best.pt
    pause
    exit /b 1
)
if not exist "yolov8n.pt" (
    echo [X] LOI: Khong tim thay file yolov8n.pt
    pause
    exit /b 1
)
echo [OK] Cac model AI da san sang

echo.
echo ========================================
echo   CAI DAT THANH CONG!
echo ========================================
echo.
echo Khoi dong he thong: start.bat
echo Xem huong dan: HUONG_DAN_CAI_DAT.md
echo.
pause
