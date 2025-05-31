@echo off
:: ================================================
:: Setup Python Virtual Environment (Windows)
:: ================================================

echo ================================================
echo Setting up Python virtual environment...
echo ================================================
python -m venv venv

echo ================================================
echo Activating virtual environment...
echo ================================================
call venv\Scripts\activate

echo ================================================
echo Upgrading pip...
echo ================================================
pip install --upgrade pip

echo ================================================
echo Installing dependencies from requirements.txt...
echo ================================================
pip install -r iot_app/requirements.txt

echo ================================================
echo Setup complete.
echo You can now run: python iot_app/app/main.py
echo ================================================
pause
