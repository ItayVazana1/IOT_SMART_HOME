@echo off
:: ================================================
:: Remove Python Virtual Environment (Windows)
:: ================================================

echo ================================================
echo Removing Python virtual environment...
echo ================================================

:: Check if the 'venv' folder exists
IF EXIST "venv\" (
    rmdir /S /Q venv
    echo Virtual environment folder 'venv' deleted successfully.
) ELSE (
    echo No virtual environment folder found.
)

pause
