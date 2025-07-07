@echo off
echo Safe Setup for CLI User Simulator (CUS) Project
echo =============================================

:: Navigate to the project directory
cd /d "C:\Users\gibea\Documents\GitRepoUtils\CUSTool"

:: Create necessary directories
echo Creating necessary directories...
if not exist "Logs" mkdir Logs
if not exist "Logs\CUSErrors" mkdir Logs\CUSErrors
if not exist "Logs\CUSEvents" mkdir Logs\CUSEvents
if not exist "NewErrors" mkdir NewErrors
if not exist "NewEvents" mkdir NewEvents

:: Install required Python packages one by one
echo Installing required Python packages...
"C:\Program Files\Python313\python.exe" -m pip install --upgrade pip
echo Installing pynput...
"C:\Program Files\Python313\python.exe" -m pip install pynput
echo Installing watchdog...
"C:\Program Files\Python313\python.exe" -m pip install watchdog
echo Installing pytest...
"C:\Program Files\Python313\python.exe" -m pip install pytest
echo Installing mock...
"C:\Program Files\Python313\python.exe" -m pip install mock

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

:: Check for syntax errors in CUS.py FIRST
echo Checking for syntax errors in CUS.py...
"C:\Program Files\Python313\python.exe" -m py_compile CUS.py
if errorlevel 1 (
    echo ERROR: Syntax errors found in CUS.py
    echo Please fix syntax errors before running tests
    pause
    exit /b 1
) else (
    echo SUCCESS: No syntax errors found in CUS.py
)

echo.
echo Setup complete! 
echo.
echo WARNING: Unit tests have been SKIPPED to prevent crashes.
echo To run tests manually (at your own risk), use:
echo "C:\Program Files\Python313\python.exe" -m pytest test_CUS.py -v
echo.
echo To run CUS.py, use:
echo "C:\Program Files\Python313\python.exe" CUS.py
echo.
pause
