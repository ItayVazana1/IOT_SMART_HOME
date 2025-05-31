@echo off
echo ================================================
echo 🧹 Removing Python virtual environment...
echo ================================================

IF EXIST "venv\" (
    rmdir /S /Q venv
    echo ✅ venv folder deleted.
) ELSE (
    echo ⚠️  No venv folder found.
)

pause
