@echo off
chcp 65001 >nul
cd /d %~dp0

echo.
echo ================================================
echo Launching IoT Smart Home Application...
echo ================================================

REM Activate virtual environment if exists
IF EXIST "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

REM Set PYTHONPATH to root folder (so Python finds 'iot_app')
SET PYTHONPATH=%CD%

REM Run main.py
echo.
echo Running the application...
python iot_app\app\main.py

echo.
echo Program exited.
pause
