@echo off
echo Starting keyboard simulator...

REM Optional: Create virtual environment (comment out if not needed)
REM python -m venv venv
REM call venv\Scripts\activate.bat

REM Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

REM Run the script
python simulate_keys.py

pause
