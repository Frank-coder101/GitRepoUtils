@echo off
echo Setting up CLI User Simulator (CUS) Project
echo ==========================================

:: Navigate to the project directory
cd /d "C:\Users\gibea\Documents\GitRepoUtils\CUSTool"

:: Create necessary directories
echo Creating necessary directories...
if not exist "Logs" mkdir Logs
if not exist "Logs\CUSErrors" mkdir Logs\CUSErrors
if not exist "Logs\CUSEvents" mkdir Logs\CUSEvents
if not exist "NewErrors" mkdir NewErrors
if not exist "NewEvents" mkdir NewEvents

:: Install required Python packages
echo Installing required Python packages...
"C:\Program Files\Python313\python.exe" -m pip install --upgrade pip
"C:\Program Files\Python313\python.exe" -m pip install -r requirements.txt

:: Create a sample simulation dictionary file if it doesn't exist
echo Creating sample simulation dictionary...
if not exist "simulation_dictionary.txt" (
    echo {> simulation_dictionary.txt
    echo   "Please enter your choice": "1\n",>> simulation_dictionary.txt
    echo   "Continue? (y/n)": "y\n",>> simulation_dictionary.txt
    echo   "Enter password": "password123\n">> simulation_dictionary.txt
    echo }>> simulation_dictionary.txt
)

:: Create a sample output log file
echo Creating sample output log file...
if not exist "Logs\output.log" (
    echo Sample log content > Logs\output.log
)

:: Run unit tests
echo Running unit tests...
"C:\Program Files\Python313\python.exe" -m pytest test_CUS.py -v > Logs\test_results.log 2>&1

:: Display test results
echo Test Results:
type Logs\test_results.log

:: Check for errors in CUS.py
echo Checking for syntax errors in CUS.py...
"C:\Program Files\Python313\python.exe" -m py_compile CUS.py
if errorlevel 1 (
    echo ERROR: Syntax errors found in CUS.py
    pause
    exit /b 1
) else (
    echo SUCCESS: No syntax errors found in CUS.py
)

:: Run CUS.py (optional - uncomment to auto-run)
:: echo Starting CUS.py...
:: "C:\Program Files\Python313\python.exe" CUS.py

echo.
echo Setup complete! You can now run CUS.py manually if needed.
echo Use: "C:\Program Files\Python313\python.exe" CUS.py
echo.
pause
